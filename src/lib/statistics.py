"""Deterministic summaries and statistical analyses for experiment outputs."""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from .results import iter_result_values


def analyze_run(model_directory: Path, output_directory: Path | None = None) -> dict[str, Any]:
    paths = tuple(model_directory.glob("*/shard-*.jsonl"))
    values = tuple(iter_result_values(paths))
    if not values:
        raise ValueError(f"no result shards found below {model_directory}")
    output = output_directory or model_directory / "analysis"
    output.mkdir(parents=True, exist_ok=True)

    summary = {
        "record_count": len(values),
        "groups": _group_summaries(values),
        "failure_labels": _failure_labels(values),
        "qualification": qualification_summary(values),
        "pilot": _pilot_summary(values),
        "experiment_5": _experiment_5(values),
        "experiment_7_regression": _experiment_7(values),
        "experiment_10": _experiment_10(values),
    }
    (output / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    _write_observations(output / "observations.jsonl", values)
    return summary


def qualification_summary(values: Iterable[dict[str, Any]]) -> dict[str, Any]:
    qualified = [value for value in values if value["request"]["experiment"] == "qualification"]
    correct = sum(_outcome(value) == "CORRECT" for value in qualified)
    operational = sum(_outcome(value) == "NOT_EVALUATED" for value in qualified)
    return {
        "requests": len(qualified),
        "correct": correct,
        "operational_failures": operational,
        "passed": len(qualified) == 5 and correct == 5 and operational == 0,
    }


def write_qualification_status(model_directory: Path) -> dict[str, Any]:
    paths = tuple((model_directory / "qualification").glob("shard-*.jsonl"))
    summary = qualification_summary(iter_result_values(paths))
    (model_directory / "qualification-status.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return summary


def _group_summaries(values: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for value in values:
        request = value["request"]
        difficulty = str(request.get("metadata", {}).get("difficulty", "control"))
        groups[(request["experiment"], request["condition"], difficulty)].append(value)
    summaries: list[dict[str, Any]] = []
    for (experiment, condition, difficulty), group in sorted(groups.items()):
        outcomes = Counter(_outcome(value) for value in group)
        evaluated = outcomes["CORRECT"] + outcomes["INCORRECT"]
        interval = _wilson_interval(outcomes["CORRECT"], evaluated)
        summaries.append(
            {
                "experiment": experiment,
                "condition": condition,
                "difficulty": difficulty,
                "total": len(group),
                "correct": outcomes["CORRECT"],
                "incorrect": outcomes["INCORRECT"],
                "not_evaluated": outcomes["NOT_EVALUATED"],
                "accuracy": outcomes["CORRECT"] / evaluated if evaluated else None,
                "wilson_95": interval,
            }
        )
    return summaries


def _failure_labels(values: Iterable[dict[str, Any]]) -> dict[str, int]:
    labels: Counter[str] = Counter()
    for value in values:
        for result in (value.get("evaluation") or {}).get("results", []):
            if result.get("type") != "CORRECT":
                labels[result.get("type", "UNKNOWN")] += 1
    return dict(sorted(labels.items()))


def _pilot_summary(values: Iterable[dict[str, Any]]) -> dict[str, Any]:
    pilot = [
        value
        for value in values
        if value["request"]["experiment"] == "exp2"
        and value["request"]["condition"] == "arabic_digits"
    ]
    targets = {"easy": (0.80, 0.95), "medium": (0.40, 0.70), "hard": (0.10, 0.40)}
    result: dict[str, Any] = {}
    for tier, (lower, upper) in targets.items():
        group = [value for value in pilot if value["request"]["metadata"]["difficulty"] == tier]
        evaluated = [value for value in group if _outcome(value) != "NOT_EVALUATED"]
        correct = sum(_outcome(value) == "CORRECT" for value in evaluated)
        accuracy = correct / len(evaluated) if evaluated else None
        result[tier] = {
            "correct": correct,
            "evaluated": len(evaluated),
            "not_evaluated": len(group) - len(evaluated),
            "accuracy": accuracy,
            "target_range": [lower, upper],
            "within_target": accuracy is not None and lower <= accuracy <= upper,
        }
    return result


def _experiment_5(values: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    main = [value for value in values if value["request"]["experiment"] == "exp4"]
    by_condition: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for value in main:
        by_condition[value["request"]["condition"]][value["request"]["puzzle_id"]] = value
    baseline = by_condition.get("arabic_digits", {})
    summaries: list[dict[str, Any]] = []
    for condition, group in sorted(by_condition.items()):
        if condition == "arabic_digits":
            continue
        for difficulty in ("all", "easy", "medium", "hard"):
            paired_ids = [
                puzzle_id
                for puzzle_id in set(baseline).intersection(group)
                if difficulty == "all"
                or baseline[puzzle_id]["request"]["metadata"]["difficulty"] == difficulty
            ]
            arabic_correct = [puzzle_id for puzzle_id in paired_ids if _outcome(baseline[puzzle_id]) == "CORRECT"]
            retained = sum(_outcome(group[puzzle_id]) == "CORRECT" for puzzle_id in arabic_correct)
            operational = sum(_outcome(group[puzzle_id]) == "NOT_EVALUATED" for puzzle_id in arabic_correct)
            b = sum(
                _outcome(baseline[puzzle_id]) == "CORRECT" and _outcome(group[puzzle_id]) == "INCORRECT"
                for puzzle_id in paired_ids
            )
            c = sum(
                _outcome(baseline[puzzle_id]) == "INCORRECT" and _outcome(group[puzzle_id]) == "CORRECT"
                for puzzle_id in paired_ids
            )
            summaries.append(
                {
                    "condition": condition,
                    "difficulty": difficulty,
                    "arabic_correct": len(arabic_correct),
                    "retained_correct": retained,
                    "retention_rate": retained / len(arabic_correct) if arabic_correct else None,
                    "failure_rate": 1 - retained / len(arabic_correct) if arabic_correct else None,
                    "operational_failures_within_baseline": operational,
                    "mcnemar_arabic_correct_only": b,
                    "mcnemar_condition_correct_only": c,
                    "mcnemar_exact_two_sided_p": _mcnemar_exact(b, c),
                }
            )
    return summaries


def _experiment_7(values: Iterable[dict[str, Any]]) -> dict[str, Any] | None:
    rows: list[tuple[float, list[float]]] = []
    for value in values:
        request = value["request"]
        generation = value.get("generation") or {}
        if request["experiment"] != "exp7" or _outcome(value) == "NOT_EVALUATED":
            continue
        metadata = request["metadata"]
        if generation.get("prompt_tokens") is None:
            continue
        rows.append(
            (
                1.0 if _outcome(value) == "CORRECT" else 0.0,
                [
                    float(generation["prompt_tokens"]),
                    float(metadata["mean_clue_tokens"]),
                    float(metadata["mean_symbol_utf8_bytes"]),
                    float(metadata["mean_symbol_code_points"]),
                ],
            )
        )
    if len(rows) < 10:
        return None
    return _fit_logistic(rows, ("prompt_tokens", "mean_clue_tokens", "mean_utf8_bytes", "mean_code_points"))


def _experiment_10(values: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for value in values:
        if value["request"]["experiment"] == "exp10":
            groups[value["request"]["condition"]].append(value)
    summaries: list[dict[str, Any]] = []
    for condition, group in sorted(groups.items()):
        initial_correct = final_correct = fixed = regressed = calls = 0
        tokens = 0
        latency = 0.0
        for value in group:
            stages = (value.get("evaluation") or {}).get("stages", [])
            if not stages:
                continue
            first = stages[0]["evaluation"]["outcome"] == "CORRECT"
            final = stages[-1]["evaluation"]["outcome"] == "CORRECT"
            initial_correct += first
            final_correct += final
            fixed += not first and final
            regressed += first and not final
            calls += sum(stage.get("model_called", True) for stage in stages)
            for stage in stages:
                generation = stage.get("generation") or {}
                tokens += (generation.get("prompt_tokens") or 0) + (generation.get("completion_tokens") or 0)
                latency += generation.get("latency_seconds") or 0.0
        summaries.append(
            {
                "condition": condition,
                "requests": len(group),
                "initial_correct": initial_correct,
                "final_correct": final_correct,
                "wrong_answers_fixed": fixed,
                "correct_answers_regressed": regressed,
                "model_calls": calls,
                "total_tokens": tokens,
                "total_latency_seconds": latency,
            }
        )
    return summaries


def _fit_logistic(
    rows: list[tuple[float, list[float]]],
    names: tuple[str, ...],
) -> dict[str, Any]:
    columns = list(zip(*(features for _, features in rows), strict=True))
    means = [sum(column) / len(column) for column in columns]
    scales = [math.sqrt(sum((value - mean) ** 2 for value in column) / len(column)) or 1.0 for column, mean in zip(columns, means, strict=True)]
    design = [
        [1.0] + [(value - mean) / scale for value, mean, scale in zip(features, means, scales, strict=True)]
        for _, features in rows
    ]
    outcomes = [outcome for outcome, _ in rows]
    coefficients = [0.0] * len(design[0])
    converged = False
    for iteration in range(1, 101):
        probabilities = [_sigmoid(sum(beta * value for beta, value in zip(coefficients, row, strict=True))) for row in design]
        gradient = [
            sum(row[column] * (outcome - probability) for row, outcome, probability in zip(design, outcomes, probabilities, strict=True))
            for column in range(len(coefficients))
        ]
        information = [
            [
                sum(
                    row[first] * row[second] * probability * (1 - probability)
                    for row, probability in zip(design, probabilities, strict=True)
                )
                for second in range(len(coefficients))
            ]
            for first in range(len(coefficients))
        ]
        try:
            delta = _solve_linear(information, gradient)
        except ValueError:
            return {"observations": len(rows), "error": "singular information matrix"}
        coefficients = [value + change for value, change in zip(coefficients, delta, strict=True)]
        if max(abs(change) for change in delta) < 1e-8:
            converged = True
            break
    return {
        "observations": len(rows),
        "converged": converged,
        "iterations": iteration,
        "standardized_coefficients": dict(zip(("intercept", *names), coefficients, strict=True)),
        "feature_means": dict(zip(names, means, strict=True)),
        "feature_scales": dict(zip(names, scales, strict=True)),
    }


def _solve_linear(matrix: list[list[float]], vector: list[float]) -> list[float]:
    augmented = [row.copy() + [value] for row, value in zip(matrix, vector, strict=True)]
    size = len(vector)
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1e-12:
            raise ValueError("singular matrix")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        augmented[column] = [value / divisor for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(augmented[row], augmented[column], strict=True)
            ]
    return [augmented[row][-1] for row in range(size)]


def _sigmoid(value: float) -> float:
    if value >= 0:
        return 1 / (1 + math.exp(-value))
    exponential = math.exp(value)
    return exponential / (1 + exponential)


def _outcome(value: dict[str, Any]) -> str | None:
    return (value.get("evaluation") or {}).get("outcome")


def _wilson_interval(successes: int, total: int) -> list[float] | None:
    if not total:
        return None
    z = 1.959963984540054
    proportion = successes / total
    denominator = 1 + z * z / total
    centre = (proportion + z * z / (2 * total)) / denominator
    margin = z * math.sqrt(proportion * (1 - proportion) / total + z * z / (4 * total * total)) / denominator
    return [max(0.0, centre - margin), min(1.0, centre + margin)]


def _mcnemar_exact(first_only: int, second_only: int) -> float | None:
    discordant = first_only + second_only
    if discordant == 0:
        return 1.0
    smaller = min(first_only, second_only)
    cumulative = sum(math.comb(discordant, index) for index in range(smaller + 1)) / (2**discordant)
    return min(1.0, 2 * cumulative)


def _write_observations(path: Path, values: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for value in values:
            request = value["request"]
            generation = value.get("generation") or {}
            row = {
                "request_id": request["request_id"],
                "experiment": request["experiment"],
                "condition": request["condition"],
                "puzzle_id": request.get("puzzle_id"),
                "difficulty": request.get("metadata", {}).get("difficulty"),
                "outcome": _outcome(value),
                "status": value["status"],
                "prompt_tokens": generation.get("prompt_tokens"),
                "completion_tokens": generation.get("completion_tokens"),
                "latency_seconds": generation.get("latency_seconds"),
            }
            stream.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
