#!/usr/bin/env python3
"""Build self-contained experiment accounts from the verified local dossier.

This is a document builder, not an inference or analysis implementation.
It never reads raw reasoning, accesses SSH, or changes frozen artifacts.
"""

import gzip
import json
import re
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SNAPSHOT = ROOT / "evidence/snapshots/2026-10-03-complete"
MODELS = {
    "GPT-OSS": "local-models-v1/gpt-oss-120b-local",
    "Qwen": "qwen-3.8-27b-v2/qwen-3.8-27b-local",
}
STEPS = {"B": ("qualification", "exp2"), "C": ("exp4",),
         "D": ("exp6",), "E": ("exp7",), "F": ("exp8",),
         "G": ("exp9",), "H": ("exp10",)}
METHODS = {"A": (1, 2, 3, 4), "B": (5, 6, 7, 8, 9, 10),
           "C": (1, 4, 5, 6, 7, 8, 9, 10, 16),
           "D": (5, 7, 9, 11), "E": (7, 9, 12),
           "F": (5, 7, 9, 13), "G": (7, 9, 14),
           "H": (5, 6, 7, 9, 15), "I": (7, 16)}
LENSES = {"A": (2, 12), "B": (5, 11, 12),
          "C": (1, 2, 3, 4, 5, 6, 11, 12), "D": (2, 3, 7, 8),
          "E": (5, 6, 12), "F": (1, 6, 7, 9), "G": (3, 9, 12),
          "H": (5, 10, 11, 12), "I": (12,)}
RECIPES = {
    "A": ["Generate and carve candidates with the saved seed and uniqueness check described below.",
          "Reject candidates that fail the requested procedural tier or duplicate a stored grid.",
          "Write the 300 certified records and manifest, then deterministically select the samples.",
          "Revalidate uniqueness, solutions, certificates, dataset hash, and sample relationships locally."],
    "B": ["Run separate timing diagnostics before interpreting a token-limited screen as a competence test.",
          "Inspect final-grid correctness, finish reason, prompt plus generation tokens, and inference time.",
          "Apply the approved model-specific five-easy qualification rule without rewriting its threshold.",
          "Run all 15 pilot puzzles in four alphabets, retaining every requested outcome.",
          "Review operational feasibility and latency, then freeze the independent model protocol."],
    "C": ["Load the frozen 60 puzzle IDs, dataset hash, model revision, and nine ordered alphabets.",
          "Bijectively encode each puzzle and reference solution into each alphabet, preserving all cells.",
          "Build 540 requests per model with the saved prompt and effective settings below.",
          "Assign requests to deterministic hash shards, execute through Slurm, and checkpoint each result.",
          "Resume interrupted shards by skipping saved request IDs, without correctness-based resampling.",
          "Check eligible counts, request digest, unique IDs, shard membership, and every completion marker.",
          "Score only extracted final answers and calculate paired retention and the explicitly exploratory model comparison."],
    "D": ["Select the 15 nested mechanism puzzles and build all four input/output Sudoku combinations.",
          "Copy each model's matching Arabic and Greek main outcomes into the two baseline conditions.",
          "Make the two cross-Sudoku calls and five supplied-grid control calls per puzzle.",
          "Evaluate Sudoku with its output alphabet, but controls by their saved exact-text answer.",
          "Check 135 records and the marker. Report 60 Sudoku outcomes and 75 controls separately."],
    "E": ["Load the exact pinned model tokenizer on a compute allocation, not the login node.",
          "Construct deterministic candidate bins and require equal isolated and leading-space token counts.",
          "Select nine labels per bin, encode each of 15 puzzles in all three constructed alphabets.",
          "Make 45 fresh calls and retain prompt-token, mean-clue-token, byte, and code-point metadata.",
          "Score the final grids, describe all three bins, and report the registered regression's actual fit status."],
    "F": ["Create six fixed uppercase assignments and the five digit, number-word, and nonce conditions.",
          "Apply each assignment consistently to clues and solutions for all 15 mechanism puzzles.",
          "Reuse matching standard-uppercase, ordinary-digit, and nonce main outputs: 45 records.",
          "Make the other 120 calls, verify 165 records and the marker, and compare matched outcomes.",
          "Distinguish assignment perturbation from an explicit conflicting arithmetic instruction."],
    "G": ["Use the nine nested ablation puzzles, not a newly selected favorable subset.",
          "Build all 19 options below. Change one option family at a time, not a full factorial.",
          "Make 171 fresh calls, including independently generated conditions with identical default prompts.",
          "Normalize each answer under its requested output contract before Sudoku evaluation.",
          "Verify the full artifact despite the teardown timeout, then report every condition, including low scores."],
    "H": ["Retrieve 27 matching main initial answers: nine ablation puzzles times three alphabets.",
          "Branch the same initial answer into four conditions without another independent initial solve.",
          "Run one or two unconditional generic revision stages, or one checker stage only on initial failures.",
          "Keep correct initials unchanged in the checker arm. Record each called stage and evaluation.",
          "Verify 108 final outcome records and compare fixes, regressions, eligible failures, and cumulative time."],
    "I": ["Verify all required inference experiments and their frozen source/configuration/sample checks.",
          "For GPT-OSS, use the isolated exact frozen export instead of bypassing the changed-source guard.",
          "Run numbered Step 13 as CPU-only analysis, preserving its source and scheduler evidence.",
          "Check registry rows, analysis record counts, exit state and logs, then back up with checksums.",
          "Keep report-only exploratory Holm and bootstrap calculations distinct from registered analyses."],
}
SCRIPTS = {"A": "01_prepare_data.py", "B": "historical diagnose_timing.py, 03_run_timing_diagnostic.py, 04_qualify_model.py and 05_run_pilot.py",
           "C": "06_freeze_protocol.py and 07_run_main_benchmark.py",
           "D": "08_run_input_output_cross.py", "E": "09_run_token_length.py",
           "F": "10_run_binding.py", "G": "11_run_ablations.py",
           "H": "12_run_revisions.py", "I": "13_analyze_results.py"}


def section(document, heading):
    """Return exactly one heading and its descendants, excluding sibling text."""
    lines = document.splitlines()
    positions = [i for i, line in enumerate(lines) if line == heading]
    if len(positions) != 1:
        raise ValueError(f"expected one heading: {heading}")
    start = positions[0]
    depth = len(heading.split(" ", 1)[0])
    stop = next((i for i in range(start + 1, len(lines))
                 if re.match(r"^#{1," + str(depth) + r"} ", lines[i])), len(lines))
    return "\n".join(lines[start:stop]).strip()


def demote(document, levels=2):
    return re.sub(r"^(#{1,4}) ", lambda match: "#" * levels + match[0], document, flags=re.M)


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |",
                      "| " + " | ".join(["---"] * len(headers)) + " |"] +
                     ["| " + " | ".join(str(value).replace("|", "\\|") for value in row) + " |" for row in rows])


def rows_for(model, step):
    directory = SNAPSHOT / "experiment_outputs" / MODELS[model] / step
    rows = []
    for path in sorted(directory.glob("shard-*.jsonl.gz")):
        with gzip.open(path, "rt", encoding="utf-8") as stream:
            rows.extend(json.loads(line) for line in stream if line.strip())
    return rows


def detailed_diagnostics(value):
    """Keep conditional denominators and overlapping failures explicit."""
    groups = {"All": value["summary"], **value["tiers"], **value["conditions"]}
    grid_rows = []
    for name, s in groups.items():
        if not s["sudoku_requests"]:
            grid_rows.append((name, "N/A: control", "N/A", "N/A", "N/A", "N/A"))
        else:
            p = s["parseable"]
            grid_rows.append((name, f'{p}/{s["sudoku_requests"]}',
                              f'{s["clues_preserved"]}/{p}', f'{s["valid_sudoku"]}/{p}',
                              s["clues_changed"], s["changed_clue_cells"]))
    output = "\n\n#### Parsing and mathematical checks for every group\n\n"
    output += "Clues and Sudoku-unit denominators are parseable grids, not all requests. N/A controls do not require Sudoku scoring. Counts of changed cells differ from counts of affected requests.\n\n"
    output += table(["Group", "Parsed / Sudoku", "Clues kept / parsed", "All units valid / parsed", "Clue-changing grids", "Changed clue cells"], grid_rows)
    output += "\n\n#### Full condition-by-difficulty failure and latency breakdown\n\n"
    output += "Grid, length, other, and operational columns are mutually exclusive failures. They sum with correct to N. Mean seconds describes the stored outcome's generation, not end-to-end revision cost or new-call-only cost.\n\n"
    values = []
    for condition, tiers in value["condition_tiers"].items():
        for tier, s in tiers.items():
            values.append((condition, tier, f'{s["correct"]}/{s["n"]}', s["incorrect_grid"],
                           s["truncated"], s["other_output_error"], s["operational_error"],
                           f'{s["mean_seconds"]:.2f}' if s["mean_seconds"] is not None else "N/A"))
    output += table(["Condition", "Tier", "Correct/N", "Grid", "Length", "Other", "Oper.", "Mean s"], values)
    output += "\n\n#### Overlapping final-output diagnostic incidences\n\nThese labels overlap. Do not add them to obtain a failure count.\n\n"
    output += table(["Label", "Requests"], sorted(value["summary"]["label_request_counts"].items()))
    if "revisions" in value:
        output += "\n\n#### Complete revision-arm transitions and cumulative costs\n\n"
        output += "End-to-end means include the reused initial answer and every called revision stage. Stage-level length stops can include shared initial copies, so they are not unique failed inference counts.\n\n"
        output += table(["Arm", "Correct/N", "Fixes", "Regressions", "New calls", "Added s", "End-to-end mean s", "Stage length stops"],
                        [(s["arm"], f'{s["correct"]}/{s["n"]}', s["fixed"], s["regressed"],
                          s["new_calls"], f'{s["extra_seconds"]:.2f}',
                          f'{s["mean_end_to_end_seconds"]:.2f}', s["all_stage_truncations"])
                         for s in value["revisions"]])
    return output


def prompt_inventory(step, model="GPT-OSS"):
    rows = rows_for(model, step)
    representatives = {}
    for row in sorted(rows, key=lambda row: (row["request"]["puzzle_id"], row["request"]["condition"])):
        representatives.setdefault(row["request"]["condition"], row["request"])
    output = f"\n\n### {model}: exact recorded treatments and prompt examples\n\n"
    output += "Ordered labels below map abstract values 1 through 9 to the visible symbols. These are saved request messages, not reconstructed reasoning or illustrative invented prompts. Request identifiers locate the full raw record.\n\n"
    output += table(["Condition", "Ordered input labels", "Ordered output labels", "Format / empty"],
                    [(condition, " ".join(r["metadata"].get("input_symbols", [])) or "supplied-grid control",
                      " ".join(r["metadata"].get("output_symbols", [])) or "exact text",
                      r["metadata"].get("output_format", "exact_text") + " / " + r["metadata"].get("empty_marker", "N/A"))
                     for condition, r in representatives.items()])
    # All cross/control and ablation treatments have distinct instructional
    # content. Binding/token labels are fully specified by the inventory and
    # use the same default prompt, so one full saved example suffices there.
    selected = representatives if step in ("exp6", "exp9") else dict(list(representatives.items())[:1])
    seen = {}
    for condition, request in selected.items():
        messages = request["messages"]
        signature = json.dumps(messages, ensure_ascii=False, sort_keys=True)
        output += f'\n\n#### Saved prompt: {condition} / {request["puzzle_id"]}\n\n'
        output += f'Request ID: `{request["request_id"]}`.\n\n'
        if signature in seen:
            output += f'Exactly identical to the prompt shown for `{seen[signature]}` within this block. It was nevertheless a separate generated condition.\n'
        else:
            seen[signature] = condition
            for message in messages:
                output += f'{message["role"]} message:\n\n```text\n{message["content"]}\n```\n'
    if step == "exp7":
        output += "\n\nCandidate construction uses a model/tokenizer-specific derived seed, shuffles uppercase candidate strings, scans at most 100,000 candidates, and retains the first nine suitable distinct labels per token-count bin. Candidates enumerate uppercase strings of length 1--4 and longer alternating consonant/vowel constructions. The constructor rejects bins with fewer than nine labels. The saved metadata gives nominal length and observed mean clue, byte, and code-point measures. The label sets are one realized construction per bin, not repeated alphabet sampling.\n"
    return output


def verification(letter, audit):
    output = "\n\n### Verify this experiment locally, without inference\n\n"
    output += "Run from the repository root. This checks preserved bytes and re-scores saved final grids. It does not start SSH, download weights, load a model, or submit a job.\n\n```bash\n"
    output += "python3 paper/report/prepare_snapshot.py tmp/research-report/snapshot \\\n  evidence/snapshots/2026-10-03-complete --verify\n"
    output += "python3 paper/report/analyze_evidence.py \\\n  --snapshot evidence/snapshots/2026-10-03-complete \\\n  --output tmp/research-report/recheck\n```\n\n"
    output += "Require `dataset_valid: true`, no audit errors, no re-evaluation disagreements, and no independent-grid disagreements. The following local paths are relative to `evidence/snapshots/2026-10-03-complete/experiment_outputs/`.\n\n"
    for model, prefix in MODELS.items():
        for step in STEPS.get(letter, ()):
            key = prefix + "/" + step
            if key in audit["steps"]:
                a = audit["steps"][key]["audit"]
                output += f'- `{key}`: saved {a["saved"]}/{a["expected"]}, complete `{a["complete"]}`, matching request digest `{a["request_digest_matches"]}`. Inspect `shard-*.jsonl.gz`, `request-manifest.json`, and every `part-*.complete.json`.\n'
    output += "\nCompare the named experiment's entry in `tmp/research-report/recheck/audit.json` with the tables in this block. Check request messages, ordered symbols, tier and puzzle IDs for any disputed cell. Clue checks apply only after parsing. For reused conditions, also match the original main request and saved generation. For revisions, inspect stage costs and called-stage flags instead of summing duplicated final-row latency.\n"
    if letter == "I":
        output += "\nThe completed GPT-OSS Step 13 has a separate backup. Verify it too:\n\n```bash\npython3 paper/report/prepare_snapshot.py tmp/research-report/unused \\\n  evidence/snapshots/2026-09-30-gptoss-step13 --verify\n```\n\nInside that snapshot's `experiment_outputs/local-models-v1/gpt-oss-120b-local/`, check `exp3/representation-registry.jsonl.gz` (2,781 rows), `analysis/observations.jsonl.gz` (1,229 rows) and `analysis/summary.json`. The copied `.out.gz` and `.err.gz` establish the successful numbered-script execution. This checksum/count inspection requires no tokenizer loading.\n"
    return output


def registry_results(model="GPT-OSS"):
    path = SNAPSHOT / "experiment_outputs" / MODELS[model] / "exp3/representation-registry.jsonl.gz"
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        rows = [json.loads(line) for line in stream if line.strip()]
    output = f"\n\n### Completed {model} token diagnostics: exact scope and summary\n\n"
    output += "The registry has 81 symbol records (nine alphabets times nine labels) plus 2,700 prompt records (all 300 certified puzzles times nine alphabets), totaling 2,781. The 2,700 prompts are tokenizer diagnostics, not additional model solves. Symbol rows store exact Unicode code points, UTF-8 bytes, code points, graphemes, isolated and leading-space token IDs/counts, full-label-row token count, and tokenizer identity. Prompt rows store puzzle/tier/alphabet, clue count, visible clue tokens, mean clue tokens and total prompt tokens. The total-prompt measure tokenizes the user prompt, not the model's complete chat-template conversation.\n\n"
    symbols = []
    prompts = []
    for alphabet in dict.fromkeys(row["alphabet"] for row in rows):
        group = [row for row in rows if row["alphabet"] == alphabet]
        labels = [row for row in group if row["kind"] == "symbol"]
        texts = [row for row in group if row["kind"] == "prompt"]
        symbols.append((alphabet, f'{statistics.mean(r["tokens_isolation"] for r in labels):.2f}',
                        f'{statistics.mean(r["tokens_after_whitespace"] for r in labels):.2f}',
                        labels[0]["tokens_inside_row_total"],
                        f'{statistics.mean(r["utf8_bytes"] for r in labels):.2f}',
                        f'{statistics.mean(r["code_point_count"] for r in labels):.2f}'))
        prompts.append((alphabet, len(texts),
                        f'{statistics.mean(r["total_prompt_tokens"] for r in texts):.2f}',
                        min(r["total_prompt_tokens"] for r in texts),
                        max(r["total_prompt_tokens"] for r in texts)))
    output += table(["Alphabet", "Mean isolated tokens", "Mean after-space tokens", "Label-row tokens", "Mean bytes", "Mean code points"], symbols)
    output += "\n\n" + table(["Alphabet", "Prompt records", "Mean user-prompt tokens", "Min", "Max"], prompts)
    output += "\n\nThese descriptive token costs do not identify their causal contribution to accuracy. They span all 300 puzzles, not only the main 60. Do not regress main correctness against these aggregate means and call that the registered token-length experiment. Each selected model has a completed registry and saved final analysis in this capture.\n"
    return output


def build_guide():
    narrative = (HERE / "writing_report.md").read_text()
    notes = (HERE / "experiment_guide_notes.md").read_text()
    tables = (HERE / "generated/results_tables.md").read_text()
    appendix = (HERE / "generated/detailed_appendix.md").read_text()
    audit = json.loads((HERE / "generated/audit.json").read_text())
    blocks = re.split(r"(?=^## [A-J]\. )", notes, flags=re.M)
    output = blocks[0]
    for block in blocks[1:]:
        letter = block[3]
        if letter == "J":
            output += block
            continue
        methods = "\n\n### Exact procedure and implementation details\n\n"
        methods += f'Numbered workflow entry point(s): `{SCRIPTS[letter]}`. These identify the implementation, not instructions to launch a new run.\n\n'
        methods += "\n".join(f'{i}. {step}' for i, step in enumerate(RECIPES[letter], 1))
        if letter in "DEFGH":
            methods += "\n\nThe model revisions, effective settings, extraction, and scoring rules below are shared with main. The listed 192 GB GPT-OSS RAM is its main allocation only. GPT-OSS follow-up jobs used 96 GB, one H100 and 12 CPUs. Qwen follow-ups request 96 GB, one H100 and 12 CPUs. Neither Slurm wall-time nor the context ceiling establishes a per-puzzle thinking-time deadline.\n"
        for number in METHODS[letter]:
            heading = next(line for line in narrative.splitlines() if line.startswith(f"## {number}. "))
            methods += "\n\n" + demote(section(narrative, heading))
        if letter in "ABCHDEFG":
            sample = section(appendix, "## Frozen samples")
            first = section(sample, "### GPT-OSS")
            relevant = {"A": ("Pilot", "Main", "Mechanism", "Ablation", "Qualification"),
                        "B": ("Pilot", "Qualification"), "C": ("Main",),
                        "D": ("Mechanism",), "E": ("Mechanism",), "F": ("Mechanism",),
                        "G": ("Ablation",), "H": ("Ablation",)}[letter]
            methods += "\n\n#### Exact puzzle IDs for this block\n\nBoth selected models use these same sample IDs.\n\n"
            methods += "\n\n".join(line for line in first.splitlines() if line.startswith(relevant))
        if letter in "DEFG":
            for model in MODELS:
                methods += prompt_inventory(STEPS[letter][0], model)
        if letter == "H":
            methods += "\n\n#### Exact revision instructions and conversation procedure\n\n"
            methods += "Generic revision instruction:\n\n```text\nCheck your answer and return a revised answer. Verify that it has exactly 81 cells, keeps every given clue unchanged, and satisfies every row, column, and 3x3 box. Return only 9 lines of 9 space-separated symbols.\n```\n\n"
            methods += "Checker-guided instruction template (`{checker_feedback}` is filled with recorded deterministic checker violations, not the reference solution):\n\n```text\nThe automatic checker found the following errors:\n{checker_feedback}\n\nCorrect the answer. Return only 9 lines of 9 space-separated symbols.\n```\n"
            methods += "\nThe executor first checks that the reused initial request messages exactly equal the branch's messages. Each revision appends an assistant message containing only `generation.text` (the extracted final answer) and the user revision instruction. A second generic revision retains the earlier conversation and appends the first revision's final answer plus another identical instruction. Hidden reasoning is not replayed as assistant content. The checker string comes from the previous evaluation's violations. A missing generation or non-OK operational state stops revision. Stage objects are saved under `evaluation.stages`, with `model_called`, generation and evaluation fields.\n"
            methods += "\nChecker feedback names changed clue cells with expected/actual values, and reports duplicates or missing values for a violated row, column or box. Format and invalid-symbol violations request the required 9x9 format. Global/local binding labels are not narrated as cognitive diagnoses. If no more specific message is available, the fallback is `The answer is not a valid solution.`\n"
        # Place exact methods before either model's results, without losing
        # the manually maintained reasoning/limitations paragraphs.
        anchor = next(line for line in block.splitlines() if line.startswith("### GPT-OSS"))
        block = block.replace(anchor, methods + "\n\n" + anchor, 1)
        for model, prefix in MODELS.items():
            additions = ""
            for step in STEPS.get(letter, ()):
                key = prefix + "/" + step
                if key not in audit["steps"]:
                    continue  # Missing outcomes are never manufactured.
                additions += "\n\n" + demote(section(tables, f"## {model} {step}"))
                additions += detailed_diagnostics(audit["steps"][key])
            if additions:
                heading = "### " + model + " results"
                model_section = section(block, heading)
                block = block.replace(model_section, model_section + additions)
        discussion = "\n\n#### Expanded interpretation, alternative explanations, and inference limits\n\n"
        for number in LENSES[letter]:
            heading = next(line for line in narrative.splitlines() if line.startswith(f"## Lens {number}:"))
            discussion += demote(section(narrative, heading)) + "\n\n"
        discussion += "Write the observed finding first, then its narrow interpretation, competing explanations, and the limit on generalization. An unrun control or suggested redesign is future work, never a completed result. Do not analyze hidden reasoning or infer a cognitive mechanism from final-grid errors alone.\n"
        if letter == "C":
            discussion += "\n\n![Main correctness by alphabet and difficulty. Cells retain their observed denominators.](generated/accuracy_heatmap.png)\n\n![Exclusive final-outcome categories by difficulty. Incorrect length-stopped generations are separate from other output errors.](generated/failure_decomposition.png)\n"
            discussion += "\n\n" + demote(section(tables, "## Cross-model paired outcomes"))
            for model in MODELS:
                discussion += "\n\n" + demote(section(appendix, f"## {model} main failure-label incidences"))
        if letter == "B":
            discussion += "\n\n### Complete historical screening record and exact settings\n\n"
            discussion += "These diagnostic histories explain configuration/model selection. They are not matched main comparisons. Saved partial runs establish only the listed observations, not unsaved requests or tier-wide inability. Model-family names, settings and denominators must stay attached to each result.\n\n"
            discussion += demote(section(appendix, "## Historical diagnostics: exact settings and tier counts"))
        if letter == "A":
            discussion += "\n\n![Disjoint pilot/main puzzles, nested diagnostic sets, and reused evidence.](generated/design_hierarchy.png)\n"
        if letter == "H":
            discussion += "\n\n![Revision accuracy versus cumulative generation cost from the common initial answers.](generated/revision_cost.png)\n"
        if letter == "I":
            for model in MODELS:
                discussion += registry_results(model)
        output += block.rstrip() + discussion + verification(letter, audit) + "\n\n"
    return output


def main():
    path = HERE / "experiment_guide.md"
    path.write_text(build_guide(), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
