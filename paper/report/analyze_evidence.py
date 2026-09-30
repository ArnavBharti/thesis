#!/usr/bin/env python3
"""Offline audit and paper-writing tables. Never loads models or changes protocols."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import math
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from lib.evaluation import evaluate_generation, normalize_output
from lib.records import ExperimentRequest, Generation, Message, shard_for
from lib.sudoku.dataset import audit_directory, read_records
from lib.sudoku.representations import SymbolAlphabet
from lib.statistics import _experiment_5, _experiment_7

MODELS = {
    "GPT-OSS": "local-models-v1/gpt-oss-120b-local",
    "Qwen": "qwen-3.8-27b-v2/qwen-3.8-27b-local",
}
TIERS = ("easy", "medium", "hard")
OUTPUT_ERRORS = {"FORMAT_ERROR", "INVALID_SYMBOL", "UNICODE_ERROR", "NO_FINAL_ANSWER", "REFUSAL"}


def read_json(path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as stream:
        return json.load(stream)


def read_rows(path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def outcome(row):
    return (row.get("evaluation") or {}).get("outcome")


def labels(row):
    return {r.get("type") for r in (row.get("evaluation") or {}).get("results", [])}


def truncated(row):
    return str((row.get("generation") or {}).get("finish_reason", "")).lower() in {
        "length", "max_tokens", "max_output_tokens"
    }


def category(row):
    # Mutually exclusive, unlike the overlapping per-cell evaluator labels.
    if row.get("status") != "OK" or outcome(row) == "NOT_EVALUATED":
        return "operational_error"
    if outcome(row) == "CORRECT":
        return "correct"
    if truncated(row):
        return "truncated"
    if labels(row) & OUTPUT_ERRORS:
        return "other_output_error"
    return "incorrect_grid"


def grid_diagnostics(row):
    """Independent grid checks after the protocol's representation normalization.

    None means unassessable, not a preserved clue or a valid Sudoku. This checker
    deliberately does not use the experiment evaluator's Sudoku constraint code.
    """
    request = row["request"]
    if request.get("metadata", {}).get("evaluation_kind") != "sudoku":
        return None
    generation = row.get("generation")
    if generation is None:
        return {"parseable": False}
    symbols = tuple(request["metadata"]["output_symbols"])
    alphabet = SymbolAlphabet("audit", symbols)
    try:
        text = normalize_output(generation["text"], alphabet, request["metadata"].get("output_format", "spaced"))
        text.encode("utf-8", errors="strict")
        rows = [line.split(" ") for line in text.splitlines()]
        if len(rows) != 9 or any(len(r) != 9 or any(s not in symbols for s in r) for r in rows):
            return {"parseable": False}
    except (ValueError, UnicodeError, json.JSONDecodeError):
        return {"parseable": False}
    values = [symbols.index(s) + 1 for row_values in rows for s in row_values]
    expected = [int(s) for s in request["expected_solution"]]
    puzzle = [int(s) if s != "." else 0 for s in request["puzzle"]]
    changed = [i for i, (clue, value) in enumerate(zip(puzzle, values)) if clue and clue != value]
    rows_valid = all(set(values[r * 9:r * 9 + 9]) == set(range(1, 10)) for r in range(9))
    columns_valid = all(set(values[c::9]) == set(range(1, 10)) for c in range(9))
    boxes_valid = all(
        {values[(br + r) * 9 + bc + c] for r in range(3) for c in range(3)} == set(range(1, 10))
        for br in (0, 3, 6) for bc in (0, 3, 6)
    )
    return {"parseable": True, "clues_preserved": not changed, "changed_clues": len(changed),
            "changed_cells": [f"r{i // 9 + 1}c{i % 9 + 1}" for i in changed],
            "rows_valid": rows_valid, "columns_valid": columns_valid, "boxes_valid": boxes_valid,
            "sudoku_valid": rows_valid and columns_valid and boxes_valid,
            "solution_equal": values == expected}


def summarize(rows):
    counts = Counter(category(r) for r in rows)
    latencies = [(r.get("generation") or {}).get("latency_seconds") for r in rows]
    latencies = [x for x in latencies if x is not None]
    checks = [grid_diagnostics(r) for r in rows]
    checks = [c for c in checks if c is not None]
    parseable = [c for c in checks if c.get("parseable")]
    # Reused records carry their original latency. This is an outcome-row mean,
    # not the new-call compute total for a mechanism experiment.
    return {"n": len(rows), "correct": counts["correct"], "incorrect_grid": counts["incorrect_grid"],
            "truncated": counts["truncated"], "other_output_error": counts["other_output_error"],
            "operational_error": counts["operational_error"],
            "finish_length_count": sum(truncated(r) for r in rows),
            "accuracy_percent": 100 * counts["correct"] / len(rows) if rows else None,
            "mean_seconds": statistics.mean(latencies) if latencies else None,
            "median_seconds": statistics.median(latencies) if latencies else None,
            "total_recorded_seconds": sum(latencies),
            "completion_tokens": sum((r.get("generation") or {}).get("completion_tokens") or 0 for r in rows),
            "sudoku_requests": len(checks), "parseable": len(parseable),
            "clues_preserved": sum(c["clues_preserved"] for c in parseable),
            "clues_changed": sum(not c["clues_preserved"] for c in parseable),
            "changed_clue_cells": sum(c["changed_clues"] for c in parseable),
            "valid_sudoku": sum(c["sudoku_valid"] for c in parseable),
            "rows_valid": sum(c["rows_valid"] for c in parseable),
            "columns_valid": sum(c["columns_valid"] for c in parseable),
            "boxes_valid": sum(c["boxes_valid"] for c in parseable),
            "label_request_counts": dict(Counter(label for r in rows for label in labels(r))),
            "reused_rows": sum(bool((r.get("generation") or {}).get("provider_metadata", {}).get("reused_from_request_id")) for r in rows)}


def deserialize_request(value):
    r = dict(value)
    r.pop("request_id", None)
    r["messages"] = tuple(Message(**m) for m in r["messages"])
    return ExperimentRequest(**r)


def re_evaluate(row):
    request = deserialize_request(row["request"])
    generation = Generation(**row["generation"]) if row.get("generation") else None
    return evaluate_generation(request, generation, operational_result=row["status"] if row["status"] != "OK" else None)


def audit_step(directory, rows, files):
    manifest_path = directory / "request-manifest.json"
    manifest = read_json(manifest_path) if manifest_path.exists() else None
    ids = [r["request"]["request_id"] for r in rows]
    digest = hashlib.sha256("\n".join(sorted(ids)).encode()).hexdigest()
    markers = [read_json(p) for p in sorted(directory.glob("*.complete.json"))]
    parts = []
    errors = []
    for path in files:
        shard, _, total = path.name.removesuffix(".gz").removesuffix(".jsonl").removeprefix("shard-").partition("-of-")
        index, count = int(shard), int(total)
        group = read_rows(path)
        marker = next((m for m in markers if m.get("part") == index + 1 and m.get("parts") == count), None)
        ok = bool(marker and marker.get("status") == "COMPLETE" and marker.get("eligible_requests") == len(group))
        parts.append({"part": index + 1, "saved": len(group), "eligible": marker.get("eligible_requests") if marker else None, "marker_valid": ok})
        if any(shard_for(r["request"]["request_id"], count) != index for r in group):
            errors.append(f"wrong hash shard: {path.name}")
        if marker and not ok:
            errors.append(f"marker/count mismatch: {path.name}")
    if len(ids) != len(set(ids)):
        errors.append("duplicate request IDs")
    disagreements = []
    independent_disagreements = []
    for row in rows:
        if deserialize_request(row["request"]).request_id != row["request"]["request_id"]:
            errors.append(f"request content hash mismatch: {row['request']['request_id']}")
        actual = re_evaluate(row)
        saved = row.get("evaluation") or {}
        if actual.get("outcome") != saved.get("outcome") or actual.get("results") != saved.get("results"):
            disagreements.append(row["request"]["request_id"])
        check = grid_diagnostics(row)
        if check is not None and row["status"] == "OK":
            correct = bool(check.get("parseable") and check.get("clues_preserved") and check.get("sudoku_valid") and check.get("solution_equal"))
            if correct != (outcome(row) == "CORRECT"):
                independent_disagreements.append(row["request"]["request_id"])
    complete = bool(not errors and not disagreements and not independent_disagreements and manifest and len(ids) == manifest["request_count"] and digest == manifest["request_id_sha256"] and parts and all(p["marker_valid"] for p in parts))
    return {"expected": manifest.get("request_count") if manifest else None, "saved": len(ids),
            "complete": complete, "request_digest_matches": bool(manifest and digest == manifest["request_id_sha256"]),
            "parts": parts, "errors": errors, "re_evaluation_disagreements": disagreements,
            "independent_correctness_disagreements": independent_disagreements}


def paired_retention(rows):
    indexed = defaultdict(dict)
    for row in rows:
        indexed[row["request"]["puzzle_id"]][row["request"]["condition"]] = outcome(row) == "CORRECT"
    result = []
    for condition in sorted({r["request"]["condition"] for r in rows} - {"arabic_digits"}):
        values = [v for v in indexed.values() if condition in v and "arabic_digits" in v]
        base = sum(v["arabic_digits"] for v in values)
        retained = sum(v["arabic_digits"] and v[condition] for v in values)
        b = sum(v["arabic_digits"] and not v[condition] for v in values)
        c = sum(not v["arabic_digits"] and v[condition] for v in values)
        n = b + c
        p = min(1.0, 2 * sum(math.comb(n, j) for j in range(min(b, c) + 1)) / 2 ** n) if n else 1.0
        result.append({"condition": condition, "paired_n": len(values), "baseline_correct": base,
                       "retained": retained, "baseline_only": b, "condition_only": c, "mcnemar_p": p})
    running = 0.0
    for rank, row in enumerate(sorted(result, key=lambda r: r["mcnemar_p"])):
        running = max(running, min(1.0, (len(result) - rank) * row["mcnemar_p"]))
        row["holm_p"] = running
    return result


def revision_summary(rows):
    result = []
    for arm in sorted({r["request"]["metadata"]["revision_condition"] for r in rows}):
        group = [r for r in rows if r["request"]["metadata"]["revision_condition"] == arm]
        fixed = regressed = calls = length_stages = 0
        extra_seconds = baseline_seconds = 0.0
        for row in group:
            stages = row["evaluation"]["stages"]
            first = stages[0]["evaluation"]["outcome"] == "CORRECT"
            last = stages[-1]["evaluation"]["outcome"] == "CORRECT"
            fixed += not first and last
            regressed += first and not last
            baseline_seconds += (stages[0].get("generation") or {}).get("latency_seconds", 0)
            for stage in stages:
                if stage.get("model_called"):
                    calls += 1
                    extra_seconds += (stage.get("generation") or {}).get("latency_seconds", 0)
                length_stages += truncated(stage)
        result.append({"arm": arm, **summarize(group), "fixed": fixed, "regressed": regressed,
                       "new_calls": calls, "all_stage_truncations": length_stages,
                       "extra_seconds": extra_seconds,
                       "mean_end_to_end_seconds": (baseline_seconds + extra_seconds) / len(group),
                       "by_tier": {t: summarize([r for r in group if r["request"]["metadata"]["difficulty"] == t]) for t in TIERS}})
    return result


def markdown_table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"] + ["| " + " | ".join(str(x).replace("|", "\\|") for x in row) + " |" for row in rows])


def table_rows(groups):
    return [(name, f"{s['correct']}/{s['n']}", f"{s['accuracy_percent']:.1f}", s["incorrect_grid"], s["truncated"], s["other_output_error"], s["operational_error"], f"{s['mean_seconds']:.2f}" if s["mean_seconds"] is not None else "NA") for name, s in groups]


HEADERS = ["Group", "Correct / total", "Accuracy %", "Invalid grid", "Truncated", "Other output error", "Operational", "Mean seconds"]


def percentile(values, probability):
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lo = int(position)
    hi = min(lo + 1, len(ordered) - 1)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (position - lo)


def cross_model(gpt, qwen):
    maps = [{(r["request"]["puzzle_id"], r["request"]["condition"]): r for r in rows} for rows in (gpt, qwen)]
    keys = sorted(maps[0].keys() & maps[1].keys())
    paired = [(maps[0][k], maps[1][k]) for k in keys]
    result = {"paired_requests": len(keys), "both_correct": sum(outcome(a) == outcome(b) == "CORRECT" for a, b in paired),
              "gpt_only": sum(outcome(a) == "CORRECT" and outcome(b) != "CORRECT" for a, b in paired),
              "qwen_only": sum(outcome(b) == "CORRECT" and outcome(a) != "CORRECT" for a, b in paired),
              "neither_correct": sum(outcome(a) != "CORRECT" and outcome(b) != "CORRECT" for a, b in paired)}
    def counts(group):
        return {"paired": len(group),
                "both_correct": sum(outcome(a) == outcome(b) == "CORRECT" for a, b in group),
                "gpt_only": sum(outcome(a) == "CORRECT" and outcome(b) != "CORRECT" for a, b in group),
                "qwen_only": sum(outcome(b) == "CORRECT" and outcome(a) != "CORRECT" for a, b in group),
                "neither_correct": sum(outcome(a) != "CORRECT" and outcome(b) != "CORRECT" for a, b in group)}
    result["by_tier"] = {t: counts([(a, b) for a, b in paired if a["request"]["metadata"]["difficulty"] == t]) for t in TIERS}
    result["by_condition"] = {c: counts([(a, b) for a, b in paired if a["request"]["condition"] == c]) for c in sorted({a["request"]["condition"] for a, b in paired})}
    # Only a complete 60 x 9 paired matrix supports this equal-weight summary.
    if len(keys) == 540:
        puzzle_values = defaultdict(list)
        tiers = {}
        for a, b in paired:
            pid = a["request"]["puzzle_id"]
            tiers[pid] = a["request"]["metadata"]["difficulty"]
            puzzle_values[pid].append(int(outcome(b) == "CORRECT") - int(outcome(a) == "CORRECT"))
        means = {p: statistics.mean(v) for p, v in puzzle_values.items()}
        tier_ids = [[p for p in sorted(means) if tiers[p] == t] for t in TIERS]
        rng = random.Random(20260930)
        boot = [100 * statistics.mean(means[rng.choice(group)] for group in tier_ids for _ in range(len(group))) for _ in range(10000)]
        result.update({"qwen_minus_gpt_pp": 100 * statistics.mean(means.values()),
                       "stratified_puzzle_bootstrap_95_pp": [percentile(boot, .025), percentile(boot, .975)],
                       "bootstrap_seed": 20260930, "bootstrap_replicates": 10000})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, required=True, help="Directory containing experiment_outputs")
    parser.add_argument("--output", type=Path, default=ROOT / "paper/report/generated")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    root = args.snapshot / "experiment_outputs"
    if not root.is_dir():
        raise SystemExit(f"missing snapshot experiment_outputs: {root}")
    all_steps = defaultdict(list)
    file_map = defaultdict(list)
    for path in sorted(root.rglob("shard-*.jsonl*")):
        key = str(path.parent.relative_to(root))
        all_steps[key].extend(read_rows(path))
        file_map[key].append(path)
    results = {}
    observations = []
    audit_errors = []
    for key, rows in all_steps.items():
        audit = audit_step(root / key, rows, file_map[key])
        if audit["errors"] or audit["re_evaluation_disagreements"] or audit["independent_correctness_disagreements"]:
            audit_errors.append(key)
        conditions = {c: summarize([r for r in rows if r["request"]["condition"] == c]) for c in sorted({r["request"]["condition"] for r in rows})}
        tiers = {t: summarize([r for r in rows if r["request"].get("metadata", {}).get("difficulty") == t]) for t in TIERS}
        cells = {c: {t: summarize([r for r in rows if r["request"]["condition"] == c and r["request"].get("metadata", {}).get("difficulty") == t]) for t in TIERS} for c in conditions}
        results[key] = {"summary": summarize(rows), "audit": audit, "conditions": conditions, "tiers": tiers, "condition_tiers": cells}
        if key.endswith("/exp4"):
            results[key]["retention"] = paired_retention(rows)
            results[key]["registered_retention"] = _experiment_5(rows)
        if key.endswith("/exp10"):
            results[key]["revisions"] = revision_summary(rows)
        if key.endswith("/exp7"):
            results[key]["registered_regression"] = _experiment_7(rows)
        for row in rows:
            request = row["request"]
            check = grid_diagnostics(row) or {}
            generation = row.get("generation") or {}
            observations.append({"step": key, "request_id": request["request_id"], "puzzle_id": request.get("puzzle_id"),
                                 "condition": request["condition"], "difficulty": request.get("metadata", {}).get("difficulty"),
                                 "status": row["status"], "outcome": outcome(row), "category": category(row),
                                 "finish_reason": generation.get("finish_reason"), "latency_seconds": generation.get("latency_seconds"),
                                 "completion_tokens": generation.get("completion_tokens"), "prompt_tokens": generation.get("prompt_tokens"),
                                 "parseable": check.get("parseable"), "clues_preserved": check.get("clues_preserved"),
                                 "changed_clues": check.get("changed_clues"), "sudoku_valid": check.get("sudoku_valid"),
                                 "failure_labels": ";".join(sorted(labels(row)))})
    dataset = audit_directory(ROOT / "src/data")
    records = read_records(ROOT / "src/data/puzzles.jsonl")
    by_id = {record.puzzle_id: record for record in records}
    dataset_mismatches = []
    for key, rows in all_steps.items():
        for row in rows:
            request = row["request"]
            record = by_id.get(request.get("puzzle_id"))
            if record is not None and request.get("metadata", {}).get("evaluation_kind") == "sudoku" and (request.get("puzzle") != record.puzzle or request.get("expected_solution") != record.solution):
                dataset_mismatches.append({"step": key, "request_id": request["request_id"]})
    if dataset_mismatches:
        audit_errors.append("request/dataset identity mismatch")
    dataset["clues"] = {t: {"n": len(values), "min": min(values), "max": max(values), "median": statistics.median(values)} for t in TIERS for values in [[r.clue_count for r in records if r.difficulty == t]]}
    dataset["technique_puzzle_counts"] = {t: dict(Counter(tech for r in records if r.difficulty == t for tech in r.difficulty_certificate.techniques)) for t in TIERS}
    comparison = cross_model(all_steps[MODELS["GPT-OSS"] + "/exp4"], all_steps[MODELS["Qwen"] + "/exp4"])
    summary = {"dataset": dataset, "steps": results, "cross_model": comparison, "audit_errors": audit_errors,
               "snapshot": str(args.snapshot), "record_count": len(observations), "dataset_request_mismatches": dataset_mismatches,
               "note": "Outcome categories are exclusive; label counts overlap. Active shards are not final accuracy."}
    (args.output / "audit.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (args.output / "observations.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(observations[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(observations)
    sections = ["# Verified results tables", "Generated locally from the backed-up result records. These tables are the numeric companion to the writing report."]
    for name, prefix in MODELS.items():
        for exp in ("qualification", "exp2", "exp4", "exp6", "exp7", "exp8", "exp9", "exp10"):
            key = prefix + "/" + exp
            if key not in results:
                continue
            data = results[key]
            sections += [f"## {name} {exp}", f"Evidence path: `{key}`. Saved {data['audit']['saved']} of {data['audit']['expected']}. Complete: {data['audit']['complete']}.",
                         markdown_table(HEADERS, table_rows([("All", data["summary"])] + [(t, s) for t, s in data["tiers"].items() if s["n"]]))]
            s = data["summary"]
            median_text = f"{s['median_seconds']:.2f} seconds" if s['median_seconds'] is not None else "unavailable"
            sections += [f"Parseable Sudoku grids: {s['parseable']}/{s['sudoku_requests']}. Clues preserved among parseable grids: {s['clues_preserved']}/{s['parseable']}. Valid Sudoku units together: {s['valid_sudoku']}/{s['parseable']}. Median record latency: {median_text}. Reused outcome rows: {s['reused_rows']}.",
                         markdown_table(HEADERS, table_rows(data["conditions"].items())),
                         "### Condition by difficulty", markdown_table(["Condition", "Easy", "Medium", "Hard"], [(c, *[f"{v[t]['correct']}/{v[t]['n']}" for t in TIERS]) for c, v in data["condition_tiers"].items()])]
            if "retention" in data:
                sections += ["### Paired comparisons against Arabic digits", markdown_table(["Alphabet", "Paired", "Retained / Arabic correct", "Arabic only", "Alphabet only", "Exact p", "Holm p"], [(r["condition"], r["paired_n"], f"{r['retained']}/{r['baseline_correct']}", r["baseline_only"], r["condition_only"], f"{r['mcnemar_p']:.4f}", f"{r['holm_p']:.4f}") for r in data["retention"]])]
                sections += ["### Difficulty-specific paired retention", "These use the registered retention procedure. The p-values below are unadjusted exploratory tier comparisons, not independent confirmation tests. The eight-comparison Holm family above covers the all-tier alphabet comparisons only.", markdown_table(["Alphabet", "Tier", "Retained / Arabic correct", "Arabic only", "Alphabet only", "Exact p"], [(r["condition"], r["difficulty"], f"{r['retained_correct']}/{r['arabic_correct']}", r["mcnemar_arabic_correct_only"], r["mcnemar_condition_correct_only"], f"{r['mcnemar_exact_two_sided_p']:.4f}") for r in data["registered_retention"] if r["difficulty"] != "all"])]
            if "revisions" in data:
                sections += ["### Shared-initial revision transitions and compute", markdown_table(["Arm", "Correct", "Fixed", "Regressed", "New calls", "Extra seconds", "Mean end-to-end seconds", "All-stage truncations"], [(r["arm"], r["correct"], r["fixed"], r["regressed"], r["new_calls"], f"{r['extra_seconds']:.2f}", f"{r['mean_end_to_end_seconds']:.2f}", r["all_stage_truncations"]) for r in data["revisions"]])]
    sections += ["## Historical diagnostics and all available outputs", "These are inventory counts, not a combined accuracy estimate. A missing marker or incomplete request digest prevents a completion claim.", markdown_table(["Evidence step", "Saved / expected", "Correct", "Truncated", "Operational", "Complete"], [(k, f"{v['audit']['saved']}/{v['audit']['expected']}", v["summary"]["correct"], v["summary"]["truncated"], v["summary"]["operational_error"], v["audit"]["complete"]) for k, v in results.items()]), "## Cross-model paired outcomes", "```json\n" + json.dumps({k:v for k,v in comparison.items() if not k.startswith('by_')}, indent=2) + "\n```"]
    for label, groups in (("Difficulty", comparison["by_tier"]), ("Alphabet", comparison["by_condition"])):
        sections += ["### Paired model outcomes by " + label.lower(), markdown_table([label, "Paired", "Both correct", "GPT-OSS only", "Qwen only", "Neither correct"], [(k, *[v[f] for f in ("paired", "both_correct", "gpt_only", "qwen_only", "neither_correct")]) for k, v in groups.items()])]
    sections += ["## Local integrity audit", "```json\n" + json.dumps({"dataset": dataset, "audit_errors": audit_errors}, indent=2) + "\n```"]
    (args.output / "results_tables.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")
    print(json.dumps({"saved_records": len(observations), "dataset_valid": dataset["valid"], "audit_errors": audit_errors, "comparison": comparison}, indent=2))
    return 1 if audit_errors or not dataset["valid"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
