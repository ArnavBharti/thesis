#!/usr/bin/env python3
"""Generate auditable LaTeX tables and plot data from completed GPT-OSS results."""

from __future__ import annotations

import argparse
import gzip
import json
import math
import statistics
from collections import Counter
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def read_shards(directory: Path) -> list[dict]:
    paths = sorted(directory.glob("shard-*.jsonl"))
    paths.extend(sorted(directory.glob("shard-*.jsonl.gz")))
    return [row for path in paths for row in read_jsonl(path)]


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
        "A_arabic_to_arabic": "A: Arabic input, Arabic output",
        "B_greek_to_greek": "B: Greek input, Greek output",
        "C_greek_to_arabic": "C: Greek input, Arabic output",
        "D_arabic_to_greek": "D: Arabic input, Greek output",
        "control_coordinate_retrieval": "Coordinate retrieval",
        "control_copy": "Greek row copy",
        "control_grid_conversion": "Grid conversion",
        "control_mapping_translation": "Mapping translation",
        "control_occurrence_count": "Occurrence count",
        "neutral_1_tokens": "One-token labels",
        "neutral_2_tokens": "Two-token labels",
        "neutral_3_tokens": "Three-token labels",
        "digits_ordinary": "Ordinary digits",
        "digits_permuted": "Permuted digits",
        "nonce_neutral": "Neutral nonce labels",
        "number_words_conflicting": "Conflicting number words",
        "number_words_ordinary": "Ordinary number words",
        "uppercase_random_1": "Uppercase permutation 1",
        "uppercase_random_2": "Uppercase permutation 2",
        "uppercase_random_3": "Uppercase permutation 3",
        "uppercase_random_4": "Uppercase permutation 4",
        "uppercase_random_5": "Uppercase permutation 5",
        "uppercase_standard": "Standard uppercase",
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


def has_result(row: dict, result_type: str) -> bool:
    return any(result["type"] == result_type for result in row["evaluation"]["results"])


def mcnemar_exact(first_only: int, second_only: int) -> float:
    discordant = first_only + second_only
    if not discordant:
        return 1.0
    smaller = min(first_only, second_only)
    cumulative = sum(math.comb(discordant, index) for index in range(smaller + 1)) / (2**discordant)
    return min(1.0, 2 * cumulative)


def write_retention_table(path: Path, rows: list[dict]) -> None:
    by_puzzle: dict[str, dict[str, bool]] = {}
    for row in rows:
        by_puzzle.setdefault(row["request"]["puzzle_id"], {})[row["request"]["condition"]] = (
            row["evaluation"]["outcome"] == "CORRECT"
        )
    conditions = sorted(next(iter(by_puzzle.values())))
    baseline_ids = [puzzle for puzzle, values in by_puzzle.items() if values["arabic_digits"]]
    lines = []
    for condition in conditions:
        if condition == "arabic_digits":
            continue
        retained = sum(by_puzzle[puzzle][condition] for puzzle in baseline_ids)
        first_only = sum(
            values["arabic_digits"] and not values[condition] for values in by_puzzle.values()
        )
        second_only = sum(
            not values["arabic_digits"] and values[condition] for values in by_puzzle.values()
        )
        lines.append(
            f"{latex_name(condition)} & {retained}/{len(baseline_ids)} & "
            f"{100 * retained / len(baseline_ids):.1f} & {first_only}/{second_only} & "
            f"{mcnemar_exact(first_only, second_only):.3f} \\\\"
        )
    lines.append(r"\bottomrule")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_binding_table(path: Path, rows: list[dict]) -> None:
    order = (
        "uppercase_standard",
        "uppercase_random_1",
        "uppercase_random_2",
        "uppercase_random_3",
        "uppercase_random_4",
        "uppercase_random_5",
        "digits_ordinary",
        "digits_permuted",
        "number_words_ordinary",
        "number_words_conflicting",
        "nonce_neutral",
    )
    lines = []
    for condition in order:
        selected = [row for row in rows if row["request"]["condition"] == condition]
        correct = sum(row["evaluation"]["outcome"] == "CORRECT" for row in selected)
        truncated = sum(row["generation"]["finish_reason"] == "length" for row in selected)
        lines.append(
            f"{latex_name(condition)} & {correct}/{len(selected)} & "
            f"{100 * correct / len(selected):.1f} & {truncated} \\\\"
        )
    lines.append(r"\bottomrule")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_binding_pairs(path: Path, rows: list[dict]) -> None:
    by_puzzle: dict[str, dict[str, bool]] = {}
    for row in rows:
        by_puzzle.setdefault(row["request"]["puzzle_id"], {})[row["request"]["condition"]] = (
            row["evaluation"]["outcome"] == "CORRECT"
        )
    pairs = (
        ("Digits", "digits_ordinary", "digits_permuted"),
        ("Number words", "number_words_ordinary", "number_words_conflicting"),
        ("Nonce/conflicting words", "nonce_neutral", "number_words_conflicting"),
    )
    lines = []
    for label, first, second in pairs:
        first_total = sum(values[first] for values in by_puzzle.values())
        second_total = sum(values[second] for values in by_puzzle.values())
        first_only = sum(values[first] and not values[second] for values in by_puzzle.values())
        second_only = sum(not values[first] and values[second] for values in by_puzzle.values())
        lines.append(
            f"{label} & {first_total}/15 & {second_total}/15 & "
            f"{first_only}/{second_only} \\\\"
        )
    lines.append(r"\bottomrule")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_ablation_table(path: Path, rows: list[dict]) -> None:
    variants = (
        ("Rules", "Minimal", "rules_minimal"),
        ("Rules", "Explicit constraints", "rules_explicit_constraints"),
        ("Rules", "Constraints and alphabet", "rules_constraints_alphabet"),
        ("Rules", "Fully explicit", "rules_fully_explicit"),
        ("Mapping", "Alphabet only", "mapping_alphabet_only"),
        ("Mapping", "To digits", "mapping_to_digits"),
        ("Mapping", "To abstract values", "mapping_to_abstract"),
        ("Output", "Spaced rows", "output_spaced"),
        ("Output", "Compact rows", "output_compact"),
        ("Output", "81-symbol string", "output_string81"),
        ("Output", "JSON", "output_json"),
        ("Empty marker", "Dot", "empty_dot"),
        ("Empty marker", "Zero", "empty_zero"),
        ("Empty marker", "Underscore", "empty_underscore"),
        ("Empty marker", r"\texttt{EMPTY}", "empty_word"),
        ("Latin case", "Uppercase", "latin_uppercase"),
        ("Latin case", "Lowercase", "latin_lowercase"),
        ("Nonce case", "Uppercase", "nonce_uppercase"),
        ("Nonce case", "Lowercase", "nonce_lowercase"),
    )
    lines = []
    previous = None
    for factor, label, condition in variants:
        if previous is not None and factor != previous:
            lines.append(r"\addlinespace")
        selected = [row for row in rows if row["request"]["condition"] == condition]
        correct = sum(row["evaluation"]["outcome"] == "CORRECT" for row in selected)
        lines.append(
            f"{factor} & {label} & {correct}/{len(selected)} & "
            f"{100 * correct / len(selected):.1f} \\\\"
        )
        previous = factor
    lines.append(r"\bottomrule")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    model = args.evidence / "local-models-v1" / "gpt-oss-120b-local"
    qualification = read_shards(model / "qualification")
    pilot = read_shards(model / "exp2")
    main = read_shards(model / "exp4")
    input_output = read_shards(model / "exp6")
    token_length = read_shards(model / "exp7")
    binding = read_shards(model / "exp8")
    ablations = read_shards(model / "exp9")
    if (
        len(qualification) != 5
        or len(pilot) != 60
        or len(main) != 540
        or len(input_output) != 135
        or len(token_length) != 45
        or len(binding) != 165
        or len(ablations) != 171
    ):
        raise SystemExit(
            "expected 5 qualification, 60 pilot, 540 main, 135 input/output, "
            "45 token-length, 165 binding, and 171 ablation rows"
        )

    pilot_difficulty = group_counts(pilot, lambda row: row["request"]["metadata"]["difficulty"])
    pilot_representation = group_counts(pilot, lambda row: row["request"]["condition"])
    main_difficulty = group_counts(main, lambda row: row["request"]["metadata"]["difficulty"])
    main_representation = group_counts(main, lambda row: row["request"]["condition"])
    input_output_condition = group_counts(input_output, lambda row: row["request"]["condition"])
    token_length_condition = group_counts(token_length, lambda row: row["request"]["condition"])
    write_group_table(args.output / "pilot_difficulty_rows.tex", pilot_difficulty)
    write_group_table(args.output / "pilot_representation_rows.tex", pilot_representation)
    write_group_table(args.output / "main_difficulty_rows.tex", main_difficulty)
    write_group_table(args.output / "main_representation_rows.tex", main_representation)
    write_group_table(args.output / "input_output_rows.tex", input_output_condition)
    write_group_table(args.output / "token_length_rows.tex", token_length_condition)
    write_binding_table(args.output / "binding_rows.tex", binding)
    write_binding_pairs(args.output / "binding_pair_rows.tex", binding)
    write_ablation_table(args.output / "ablation_rows.tex", ablations)
    write_retention_table(args.output / "main_retention_rows.tex", main)
    write_plot_data(args.output / "pilot_difficulty.dat", pilot_difficulty)
    write_plot_data(args.output / "pilot_representation.dat", pilot_representation)
    write_plot_data(args.output / "main_representation.dat", main_representation)

    pilot_latencies = [row["generation"]["latency_seconds"] for row in pilot]
    main_latencies = [row["generation"]["latency_seconds"] for row in main]
    pilot_tokens = [row["generation"]["completion_tokens"] for row in pilot]
    main_tokens = [row["generation"]["completion_tokens"] for row in main]
    parse_failure_types = {
        "WRONG_ROW_COUNT",
        "WRONG_CELL_COUNT",
        "FORMAT_ERROR",
        "INVALID_SYMBOL",
        "NO_FINAL_ANSWER",
        "UNICODE_ERROR",
    }
    parseable_main = [
        row
        for row in main
        if not any(has_result(row, result_type) for result_type in parse_failure_types)
    ]
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
        command("MainCorrect", "372/540"),
        command("MainAccuracy", "68.9\\%"),
        command("MainMeanLatency", f"{statistics.mean(main_latencies):.1f}"),
        command("MainMedianLatency", f"{statistics.median(main_latencies):.1f}"),
        command("MainMeanTokens", f"{statistics.mean(main_tokens):.0f}"),
        command("MainTruncations", str(sum(row["generation"]["finish_reason"] == "length" for row in main))),
        command("MainOperationalFailures", str(sum(bool(row.get("error")) for row in main))),
        command("MainFormatCompliant", str(sum(not has_result(row, "FORMAT_ERROR") for row in main))),
        command("MainParseable", str(len(parseable_main))),
        command("MainCluesPreserved", str(sum(not has_result(row, "GIVEN_MODIFIED") for row in parseable_main))),
        command("InputOutputCorrect", "120/135"),
        command("InputOutputOperationalFailures", str(sum(bool(row.get("error")) for row in input_output))),
        command("TokenLengthCorrect", "32/45"),
        command("TokenLengthOperationalFailures", str(sum(bool(row.get("error")) for row in token_length))),
        command("TokenLengthTruncations", str(sum(row["generation"]["finish_reason"] == "length" for row in token_length))),
        command("BindingCorrect", f"{sum(row['evaluation']['outcome'] == 'CORRECT' for row in binding)}/165"),
        command("BindingAccuracy", f"{100 * sum(row['evaluation']['outcome'] == 'CORRECT' for row in binding) / 165:.1f}\\%"),
        command("BindingOperationalFailures", str(sum(bool(row.get("error")) for row in binding))),
        command("BindingTruncations", str(sum(row["generation"]["finish_reason"] == "length" for row in binding))),
        command("AblationCorrect", f"{sum(row['evaluation']['outcome'] == 'CORRECT' for row in ablations)}/171"),
        command("AblationAccuracy", f"{100 * sum(row['evaluation']['outcome'] == 'CORRECT' for row in ablations) / 171:.1f}\\%"),
        command("AblationOperationalFailures", str(sum(bool(row.get("error")) for row in ablations))),
        command("AblationTruncations", str(sum(row["generation"]["finish_reason"] == "length" for row in ablations))),
    ]
    (args.output / "results.tex").write_text("\n".join(values) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
