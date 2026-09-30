#!/usr/bin/env python3
"""Generate dependency-free scientific figures and detailed evidence appendices."""

import argparse
import json
import statistics
import sys
from collections import Counter
from html import escape
from pathlib import Path

from analyze_evidence import MODELS, ROOT, TIERS, markdown_table, read_rows, summarize


class SVG:
    def __init__(self, width, height):
        self.items = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="white"/>']

    def text(self, x, y, text, size=14, color="#182635", weight="normal", anchor="start"):
        self.items.append(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(text))}</text>')

    def rect(self, x, y, width, height, color, stroke="none"):
        self.items.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="3" fill="{color}" stroke="{stroke}"/>')

    def line(self, x1, y1, x2, y2, color="#93a1ad"):
        self.items.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}"/>')

    def save(self, path):
        path.write_text("\n".join(self.items + ["</svg>"]) + "\n", encoding="utf-8")


NAMES = {"arabic_digits": "Arabic digits", "uppercase_latin": "Uppercase Latin", "lowercase_latin": "Lowercase Latin", "greek_letters": "Greek letters", "bengali_numerals": "Bengali numerals", "devanagari_numerals": "Devanagari numerals", "abstract_symbols": "Abstract symbols", "nonce_labels": "Nonce labels", "emoji": "Emoji"}


def heatmap(audit, output):
    svg = SVG(960, 455)
    svg.text(24, 30, "Main accuracy by alphabet and difficulty", 23, weight="bold")
    svg.text(24, 52, "Cells show correct / saved requests. These are not independent repeated solves.", 13)
    order = list(NAMES)
    for index, (name, prefix) in enumerate(MODELS.items()):
        data = audit["steps"][prefix + "/exp4"]
        x = 24 + index * 475
        status = "complete" if data["audit"]["complete"] else f"PARTIAL {data['summary']['n']}/540"
        svg.text(x, 88, f"{name}: {status}", 19, weight="bold")
        for j, tier in enumerate(TIERS):
            svg.text(x + 190 + j * 84 + 37, 116, tier.title(), 14, anchor="middle")
        for i, condition in enumerate(order):
            y = 129 + i * 30
            svg.text(x, y + 20, NAMES[condition], 14)
            for j, tier in enumerate(TIERS):
                s = data["condition_tiers"][condition][tier]
                p = s["correct"] / s["n"] if s["n"] else 0
                color = f"rgb({int(236 - 189 * p)},{int(245 - 115 * p)},{int(249 - 96 * p)})"
                svg.rect(x + 190 + j * 84, y, 76, 27, color)
                svg.text(x + 228 + j * 84, y + 19, f"{s['correct']}/{s['n']}", 14, "white" if p > .65 else "#182635", anchor="middle")
    svg.text(24, 432, "Same frozen 60 puzzles. Nine representations. Darker cells indicate higher realized accuracy.", 13)
    svg.save(output / "accuracy_heatmap.svg")


def errors(audit, output):
    svg = SVG(960, 365)
    svg.text(24, 30, "Main outcomes: correctness and failure types", 23, weight="bold")
    colors = {"correct": "#287b67", "incorrect_grid": "#b96a37", "truncated": "#a94259", "other_output_error": "#7c74a9"}
    labels = {"correct": "Correct", "incorrect_grid": "Incorrect grid", "truncated": "Truncated", "other_output_error": "Other output error"}
    for i, (key, color) in enumerate(colors.items()):
        svg.rect(24 + i * 230, 49, 14, 14, color)
        svg.text(44 + i * 230, 61, labels[key], 13)
    for index, (name, prefix) in enumerate(MODELS.items()):
        data = audit["steps"][prefix + "/exp4"]
        for j, tier in enumerate(TIERS):
            y = 91 + (index * 3 + j) * 37
            s = data["tiers"][tier]
            svg.text(24, y + 19, f"{name} {tier}", 14)
            x = 185
            for key, color in colors.items():
                width = 590 * s[key] / s["n"]
                if width:
                    svg.rect(x, y, width, 27, color)
                    if width > 27:
                        svg.text(x + width / 2, y + 19, s[key], 13, "white", anchor="middle")
                x += width
            svg.text(794, y + 19, f"n={s['n']}, mean={s['mean_seconds']:.0f}s", 13)
    complete = all(audit["steps"][prefix + "/exp4"]["audit"]["complete"] for prefix in MODELS.values())
    coverage = "Each tier has 180 requests per model." if complete else "Partial Qwen coverage is identified by n."
    svg.text(24, 341, "Categories are exclusive. Zero recorded operational errors. " + coverage, 13)
    svg.save(output / "failure_decomposition.svg")


def revisions(audit, output):
    svg = SVG(960, 375)
    svg.text(24, 30, "GPT-OSS revision: accuracy and generation-time cost", 23, weight="bold")
    svg.text(24, 53, "27 shared initial answers: nine puzzles in three representations. No equal-compute baseline.", 13)
    arms = audit["steps"][MODELS["GPT-OSS"] + "/exp10"]["revisions"]
    svg.line(90, 295, 870, 295)
    svg.line(90, 295, 90, 85)
    for t in (300, 400, 500, 600, 700):
        x = 90 + (t - 250) * 780 / 450
        svg.line(x, 295, x, 300)
        svg.text(x, 319, t, 13, anchor="middle")
    for value in (60, 70, 80, 90):
        y = 295 - (value - 60) * 210 / 35
        svg.line(90, y, 870, y, "#e1e6eb")
        svg.text(76, y + 5, f"{value}%", 13, anchor="end")
    for r in arms:
        x = 90 + (r["mean_end_to_end_seconds"] - 250) * 780 / 450
        y = 295 - (100 * r["correct"] / 27 - 60) * 210 / 35
        svg.rect(x - 5, y - 5, 10, 10, "#245f86")
        name = r["arm"].replace("_", " ")
        svg.text(x + 11, y - 9, f"{name}: {r['correct']}/27", 13)
    svg.text(465, 354, "Mean total generation seconds, including the reused initial answer", 14, anchor="middle")
    svg.save(output / "revision_cost.svg")


def hierarchy(output):
    svg = SVG(960, 410)
    svg.text(24, 30, "Design: puzzles, requests, and evidence reuse", 23, weight="bold")
    boxes = [(350, 55, 260, 60, "Certified dataset", "300 puzzles: 100 per tier"),
             (40, 150, 270, 65, "Pilot: 15 puzzles", "4 alphabets = 60 calls/model"),
             (350, 150, 260, 65, "Main: 60 different puzzles", "9 alphabets = 540 calls/model"),
             (650, 150, 275, 65, "Paired final-grid scoring", "Format, clues, units, reference"),
             (220, 275, 260, 65, "Mechanism subset: 15", "Cross, token length, binding"),
             (580, 275, 300, 65, "Ablation subset: 9", "Prompts and shared-initial revisions")]
    for x, y, w, h, a, b in boxes:
        svg.rect(x, y, w, h, "#eff5f9", "#bfd1df")
        svg.text(x + w / 2, y + 24, a, 16, weight="bold", anchor="middle")
        svg.text(x + w / 2, y + 46, b, 13, anchor="middle")
    for line in [(480,115,175,150),(480,115,480,150),(610,182,650,182),(480,215,350,275),(480,215,730,275),(480,308,580,308)]:
        svg.line(*line, "#245f86")
    svg.text(24, 380, "Pilot and main are disjoint. Smaller sets are nested. Reused main outputs are not fresh model calls.", 14)
    svg.save(output / "design_hierarchy.svg")


def detailed_appendix(snapshot, audit, output):
    root = snapshot / "experiment_outputs"
    sections = ["# Detailed evidence and representative outputs", "This appendix expands the numerical tables with settings, sample checks, failure incidences, and final-only output examples."]
    plans = {name: json.loads((root / prefix.split('/')[0] / "sample-plan.json").read_text()) for name, prefix in MODELS.items()}
    sections += ["## Frozen samples", f"Main IDs identical across selected models: {plans['GPT-OSS']['main_ids'] == plans['Qwen']['main_ids']}."]
    for name, plan in plans.items():
        sections += [f"### {name}", f"Dataset SHA-256: `{plan['dataset_sha256']}`."]
        for sample in ("pilot", "main", "mechanism", "ablation"):
            sections += [f"{sample.title()} ({len(plan[sample + '_ids'])} puzzles): " + ", ".join(plan[sample + "_ids"]) + "."]
        prefix = MODELS[name]
        qualification = root / prefix / "qualification/shard-000-of-001.jsonl"
        if not qualification.exists():
            qualification = qualification.with_suffix(".jsonl.gz")
        qual = [r["request"]["puzzle_id"] for r in read_rows(qualification)]
        sections += [f"Qualification IDs: {', '.join(qual)}. Observed qualification/main overlap: {sorted(set(qual) & set(plan['main_ids']))}. Observed qualification/pilot overlap: {sorted(set(qual) & set(plan['pilot_ids']))}."]
    for name, prefix in MODELS.items():
        main = audit["steps"][prefix + "/exp4"]
        sections += [f"## {name} main failure-label incidences", "Each count is requests containing the label. Counts overlap and must not be summed.", markdown_table(["Label", "Requests"], sorted(main["summary"]["label_request_counts"].items()))]
        sections += ["### Parsing, clues, and Sudoku validity by alphabet", markdown_table(["Alphabet", "Saved", "Parsed", "Clues preserved / parsed", "Valid units / parsed", "Changed clue cells"], [(c, s["n"], s["parseable"], f"{s['clues_preserved']}/{s['parseable']}", f"{s['valid_sudoku']}/{s['parseable']}", s["changed_clue_cells"]) for c, s in main["conditions"].items()])]
        main_rows = [r for p in sorted((root / prefix / "exp4").glob("shard-*.jsonl*")) for r in read_rows(p)]
        from analyze_evidence import category, grid_diagnostics
        examples = []
        wanted = ["correct", "incorrect_grid", "truncated", "other_output_error"]
        for cat in wanted:
            chosen = next((r for r in main_rows if r["request"]["condition"] == "arabic_digits" and category(r) == cat), None)
            chosen = chosen or next((r for r in main_rows if category(r) == cat), None)
            if chosen:
                examples.append((cat, chosen))
        sections += ["### Representative final-only outputs", "Examples are deterministic first matches in sorted shard order. They illustrate categories, not prevalence. No reasoning trace is reproduced."]
        for cat, r in examples:
            g = r.get("generation") or {}
            sections += [f"#### {cat.replace('_', ' ').title()}: {r['request']['puzzle_id']} / {r['request']['condition']}", f"Request ID: `{r['request']['request_id']}`. Finish: `{g.get('finish_reason')}`. Latency: {g.get('latency_seconds', 0):.2f} seconds. Generation tokens: {g.get('completion_tokens')}. Labels: {', '.join(sorted({x['type'] for x in r['evaluation']['results']}))}."]
            text = g.get("text") or "[No extracted final answer]"
            # Long erroneous prose is not pasted unboundedly. This truncates the
            # report display only, not the preserved raw evidence or scoring.
            if len(text) > 1800:
                text = text[:1800] + "\n[Report excerpt ends; complete final text remains in raw evidence.]"
            sections += ["```text\n" + text + "\n```", "Independent grid audit: `" + json.dumps(grid_diagnostics(r), ensure_ascii=False) + "`."]
    sections += ["## Historical diagnostics: exact settings and tier counts", "Historical configurations changed. Their names are identifiers, not proof of equivalently controlled conditions."]
    historical_index = 0
    for key, data in audit["steps"].items():
        if key.startswith(tuple(MODELS.values())):
            continue
        manifest = json.loads((root / key / "request-manifest.json").read_text())
        model = manifest["model"]
        historical_index += 1
        effective = {**manifest["inference"], **model.get("extra", {}).get("sampling", {})}
        sections += [f"### Historical run {historical_index}: {key.split('/')[1]}", f"Evidence path: `{key}`.", f"Checkpoint: `{model['model_id']}`. Revision: `{model.get('revision')}`. Saved/expected: {data['audit']['saved']}/{data['audit']['expected']}. Marker and digest completion: {data['audit']['complete']}.", "Effective recorded inference and overrides: `" + json.dumps(effective, sort_keys=True) + "`.", "Model controls: `" + json.dumps({k:v for k,v in model.get('extra', {}).items() if k != 'protocol'}, ensure_ascii=False, sort_keys=True) + "`.", markdown_table(["Tier", "Correct / saved", "Wrong grid", "Truncated", "Other output error", "Operational", "Mean seconds"], [(t, f"{s['correct']}/{s['n']}", s["incorrect_grid"], s["truncated"], s["other_output_error"], s["operational_error"], f"{s['mean_seconds']:.2f}" if s["mean_seconds"] is not None else "NA") for t, s in data["tiers"].items() if s["n"]]), f"Parseable Sudoku grids {data['summary']['parseable']}/{data['summary']['sudoku_requests']}. Clues preserved {data['summary']['clues_preserved']}/{data['summary']['parseable']} parseable grids."]
    (output / "detailed_appendix.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "paper/report/generated")
    args = parser.parse_args()
    audit = json.loads((args.output / "audit.json").read_text())
    for generate in (heatmap, errors, revisions):
        generate(audit, args.output)
    hierarchy(args.output)
    detailed_appendix(args.snapshot, audit, args.output)
    print("Wrote four evidence figures and the detailed appendix")


if __name__ == "__main__":
    main()
