#!/usr/bin/env python3
"""Generate complete two-model paper tables from the locally audited capture."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = {"GPT-OSS": "local-models-v1/gpt-oss-120b-local",
          "Qwen": "qwen-3.8-27b-v2/qwen-3.8-27b-local"}
NAMES = {
    "exp6": "Input/output", "exp7": "Token length", "exp8": "Binding",
    "exp9": "Ablations", "exp10": "Revision outcomes",
}
ARMS = ("one_pass", "one_self_revision", "two_self_revisions", "checker_guided_revision")


def latex(value):
    return str(value).replace("_", r"\_")


def write_table(path, columns, headers, rows):
    lines = [r"\begin{tabular}{" + columns + "}", r"\toprule",
             " & ".join(headers) + r"\\", r"\midrule"]
    lines += [" & ".join(latex(v) for v in row) + r"\\" for row in rows]
    lines += [r"\bottomrule", r"\end{tabular}"]
    path.write_text("\n".join(lines) + "\n")


def main():
    audit = json.loads((ROOT / "paper/report/generated/audit.json").read_text())
    assert audit["snapshot"] == "evidence/snapshots/2026-10-03-complete"
    assert not audit["audit_errors"] and not audit["dataset_request_mismatches"]
    target = Path(__file__).resolve().parent / "generated"
    target.mkdir(exist_ok=True)
    summaries = []
    for step, label in NAMES.items():
        conditions = {}
        for model, prefix in MODELS.items():
            data = audit["steps"][prefix + "/" + step]
            assert data["audit"]["complete"] and data["audit"]["request_digest_matches"]
            assert not data["audit"]["errors"]
            assert not data["audit"]["re_evaluation_disagreements"]
            assert not data["audit"]["independent_correctness_disagreements"]
            s = data["summary"]
            summaries.append((label, model, f'{s["correct"]}/{s["n"]}',
                              s["incorrect_grid"], s["truncated"],
                              s["other_output_error"], s["operational_error"]))
            conditions[model] = data["conditions"]
        assert conditions["GPT-OSS"].keys() == conditions["Qwen"].keys()
        rows = []
        for condition in conditions["GPT-OSS"]:
            row = [condition.replace("_", " ").replace(":", ": ")]
            for model, prefix in MODELS.items():
                s = conditions[model][condition]
                row.append(f'{s["correct"]}/{s["n"]}')
                tiers = audit["steps"][prefix + "/" + step]["condition_tiers"][condition]
                row += [f'{tiers[t]["correct"]}/{tiers[t]["n"]}' for t in ("easy", "medium", "hard")]
            rows.append(row)
        write_table(target / (step + "_conditions.tex"), "p{4.4cm}rrrrrrrr",
                    ["Condition", "GPT all", "Easy", "Medium", "Hard", "Qwen all", "Easy", "Medium", "Hard"], rows)
    write_table(target / "followup_errors.tex", "llrrrrr",
                ["Experiment", "Model", "Correct/N", "Grid", "Length", "Other", "Operational"], summaries)
    rows = []
    for model, prefix in MODELS.items():
        arms = {r["arm"]: r for r in audit["steps"][prefix + "/exp10"]["revisions"]}
        for arm in ARMS:
            r = arms[arm]
            rows.append((model, arm.replace("_", " "), f'{r["correct"]}/{r["n"]}',
                         r["fixed"], r["regressed"], r["new_calls"],
                         f'{r["mean_end_to_end_seconds"]:.2f}'))
    write_table(target / "revision_table.tex", "llrrrrr",
                ["Model", "Arm", "Correct", "Fixed", "Regressed", "New calls", "Mean total (s)"], rows)
    print("Generated complete condition/tier, error, and revision tables for both models")


if __name__ == "__main__":
    main()
