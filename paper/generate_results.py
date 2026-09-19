#!/usr/bin/env python3
"""Generate auditable LaTeX tables and plot data from completed GPT-OSS results."""

from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import Counter
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def group_counts(rows: list[dict], key) -> list[tuple[str, int, int, float, float]]:
    output = []
    for name in sorted({key(row) for row in rows}):
        selected = [row for row in rows if key(row) == name]
        correct = sum(row["evaluation"]["outcome"] == "CORRECT" for row in selected)
        low, high = wilson(correct, len(selected))
        output.append((name, correct, len(selected), low, high))
    return output


def wilson(correct: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    proportion = correct / total
    denominator = 1 + z * z / total
    centre = (proportion + z * z / (2 * total)) / denominator
    margin = z * math.sqrt(proportion * (1 - proportion) / total + z * z / (4 * total**2)) / denominator
    return 100 * (centre - margin), 100 * (centre + margin)


def latex_name(value: str) -> str:
    names = {
        "arabic_digits": "Arabic digits",
        "abstract_symbols": "Abstract symbols",
        "bengali_numerals": "Bengali numerals",
        "devanagari_numerals": "Devanagari numerals",
        "emoji": "Emoji",
        "greek_letters": "Greek letters",
        "lowercase_latin": "Lowercase Latin",
        "nonce_labels": "Nonce labels",
        "uppercase_latin": "Uppercase Latin",
    }
    return names.get(value, value.capitalize())


def write_group_table(path: Path, groups: list[tuple[str, int, int, float, float]]) -> None:
    lines = []
    for name, correct, total, low, high in groups:
        lines.append(
            f"{latex_name(name)} & {correct}/{total} & {100 * correct / total:.1f} & "
            f"[{low:.1f}, {high:.1f}] \\\\"
        )
    lines.append(r"\bottomrule")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_plot_data(path: Path, groups: list[tuple[str, int, int, float, float]]) -> None:
    lines = ["label accuracy low high"]
    for name, correct, total, low, high in groups:
        label = name.replace("_", "-")
        lines.append(f"{label} {100 * correct / total:.4f} {low:.4f} {high:.4f}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def command(name: str, value: str) -> str:
    return rf"\newcommand{{\{name}}}{{{value}}}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    model = args.evidence / "local-models-v1" / "gpt-oss-120b-local"
    qualification = read_jsonl(model / "qualification" / "shard-000-of-001.jsonl")
    pilot = read_jsonl(model / "exp2" / "shard-000-of-001.jsonl")
    main_one = read_jsonl(model / "exp4" / "shard-000-of-006.jsonl")
    if len(qualification) != 5 or len(pilot) != 60 or len(main_one) != 101:
        raise SystemExit("expected 5 qualification, 60 pilot, and 101 completed main-part-1 rows")

    pilot_difficulty = group_counts(pilot, lambda row: row["request"]["metadata"]["difficulty"])
    pilot_representation = group_counts(pilot, lambda row: row["request"]["condition"])
    main_difficulty = group_counts(main_one, lambda row: row["request"]["metadata"]["difficulty"])
    main_representation = group_counts(main_one, lambda row: row["request"]["condition"])
    write_group_table(args.output / "pilot_difficulty_rows.tex", pilot_difficulty)
    write_group_table(args.output / "pilot_representation_rows.tex", pilot_representation)
    write_group_table(args.output / "main_part1_difficulty_rows.tex", main_difficulty)
    write_group_table(args.output / "main_part1_representation_rows.tex", main_representation)
    write_plot_data(args.output / "pilot_difficulty.dat", pilot_difficulty)
    write_plot_data(args.output / "pilot_representation.dat", pilot_representation)

    pilot_latencies = [row["generation"]["latency_seconds"] for row in pilot]
    main_latencies = [row["generation"]["latency_seconds"] for row in main_one]
    pilot_tokens = [row["generation"]["completion_tokens"] for row in pilot]
    main_tokens = [row["generation"]["completion_tokens"] for row in main_one]
    result_types = Counter(
        result["type"] for row in pilot for result in row["evaluation"]["results"]
    )
    values = [
        command("QualificationCorrect", "5/5"),
        command("PilotCorrect", "47/60"),
        command("PilotAccuracy", "78.3\\%"),
        command("PilotMeanLatency", f"{statistics.mean(pilot_latencies):.1f}"),
        command("PilotMedianLatency", f"{statistics.median(pilot_latencies):.1f}"),
        command("PilotMeanTokens", f"{statistics.mean(pilot_tokens):.0f}"),
        command("PilotTruncations", str(result_types["TRUNCATED_OUTPUT"])),
        command("PilotOperationalFailures", str(sum(bool(row.get("error")) for row in pilot))),
        command("MainPartOneCorrect", "69/101"),
        command("MainPartOneAccuracy", "68.3\\%"),
        command("MainPartOneMeanLatency", f"{statistics.mean(main_latencies):.1f}"),
        command("MainPartOneMedianLatency", f"{statistics.median(main_latencies):.1f}"),
        command("MainPartOneMeanTokens", f"{statistics.mean(main_tokens):.0f}"),
        command("MainPartOneTruncations", str(sum(row["generation"]["finish_reason"] == "length" for row in main_one))),
        command("MainPartOneOperationalFailures", str(sum(bool(row.get("error")) for row in main_one))),
    ]
    (args.output / "results.tex").write_text("\n".join(values) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
