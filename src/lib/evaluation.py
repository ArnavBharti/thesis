"""Response evaluation, output normalization, and checker feedback."""

from __future__ import annotations

import json
from typing import Any

from .sudoku.evaluator import Evaluation, evaluate_response
from .sudoku.representations import SymbolAlphabet
from .sudoku.schema import grid_from_compact

from .records import ExperimentRequest, Generation

REFUSAL_MARKERS = (
    "i cannot",
    "i can't",
    "unable to",
    "cannot comply",
    "won't be able",
)


def evaluate_generation(
    request: ExperimentRequest,
    generation: Generation | None,
    *,
    operational_result: str | None = None,
) -> dict[str, Any]:
    if operational_result:
        return {"outcome": "NOT_EVALUATED", "results": [{"type": operational_result}]}
    if generation is None:
        return {"outcome": "INCORRECT", "results": [{"type": "NO_FINAL_ANSWER"}]}

    text = generation.text
    if request.metadata.get("evaluation_kind") == "exact_text":
        expected = str(request.metadata["expected_text"])
        if text.strip() == expected:
            return {"outcome": "CORRECT", "results": [{"type": "CORRECT"}]}
        if _looks_like_refusal(text):
            return {"outcome": "INCORRECT", "results": [{"type": "REFUSAL"}]}
        result = {"type": "FORMAT_ERROR", "expected": expected, "actual": text.strip()}
        if _is_truncated(generation):
            result = {"type": "TRUNCATED_OUTPUT", "finish_reason": generation.finish_reason}
        return {"outcome": "INCORRECT", "results": [result]}

    if not request.puzzle or not request.expected_solution:
        raise ValueError(f"request {request.request_id} lacks Sudoku evaluation data")
    if _looks_like_refusal(text):
        return {"outcome": "INCORRECT", "results": [{"type": "REFUSAL"}]}
    symbols = tuple(str(symbol) for symbol in request.metadata["output_symbols"])
    alphabet = SymbolAlphabet(request.output_alphabet or "output", symbols)
    output_format = str(request.metadata.get("output_format", "spaced"))
    try:
        normalized = normalize_output(text, alphabet, output_format)
    except (ValueError, json.JSONDecodeError) as error:
        if _looks_like_refusal(text):
            result = {"type": "REFUSAL"}
        elif _is_truncated(generation):
            result = {"type": "TRUNCATED_OUTPUT", "finish_reason": generation.finish_reason}
        else:
            result = {"type": "FORMAT_ERROR", "message": str(error)}
        return {"outcome": "INCORRECT", "results": [result]}

    evaluation = evaluate_response(
        grid_from_compact(request.puzzle),
        grid_from_compact(request.expected_solution),
        normalized,
        alphabet,
    )
    value = evaluation.to_dict()
    if value["outcome"] == "INCORRECT" and _is_truncated(generation):
        value["results"].insert(
            0,
            {"type": "TRUNCATED_OUTPUT", "finish_reason": generation.finish_reason},
        )
    return value


def normalize_output(text: str, alphabet: SymbolAlphabet, output_format: str) -> str:
    if output_format == "spaced":
        return text
    if output_format == "compact":
        rows = text.splitlines()
        if len(rows) != 9:
            raise ValueError(f"compact output must contain 9 rows, got {len(rows)}")
        parsed = [_segment(row, alphabet.symbols, expected=9) for row in rows]
        return "\n".join(" ".join(row) for row in parsed)
    if output_format == "string81":
        if "\n" in text or "\r" in text or any(character.isspace() for character in text):
            raise ValueError("81-symbol output must not contain whitespace")
        values = _segment(text, alphabet.symbols, expected=81)
        return "\n".join(" ".join(values[start : start + 9]) for start in range(0, 81, 9))
    if output_format == "json":
        value = json.loads(text)
        if (
            not isinstance(value, list)
            or len(value) != 9
            or any(not isinstance(row, list) or len(row) != 9 for row in value)
        ):
            raise ValueError("JSON output must be an array of 9 arrays of 9 strings")
        tokens = [token for row in value for token in row]
        if any(not isinstance(token, str) or token not in alphabet.symbols for token in tokens):
            raise ValueError("JSON output contains an invalid symbol")
        return "\n".join(" ".join(row) for row in value)
    raise ValueError(f"unknown output format {output_format!r}")


def checker_feedback(evaluation: dict[str, Any]) -> str:
    messages: list[str] = []
    for result in evaluation.get("results", []):
        label = result.get("type")
        if label == "GIVEN_MODIFIED":
            messages.append(
                f"Given cell {result['cell']} changed from {result['expected']} to {result['actual']}."
            )
        elif label in {"ROW_CONSTRAINT_ERROR", "COLUMN_CONSTRAINT_ERROR", "BOX_CONSTRAINT_ERROR"}:
            unit = label.split("_", 1)[0].lower()
            number = result[unit]
            details = []
            if result.get("duplicate"):
                details.append("duplicates " + ", ".join(result["duplicate"]))
            if result.get("missing"):
                details.append("is missing " + ", ".join(result["missing"]))
            messages.append(f"{unit.title()} {number} " + " and ".join(details) + ".")
        elif label in {"WRONG_CELL_COUNT", "WRONG_ROW_COUNT", "FORMAT_ERROR", "INVALID_SYMBOL"}:
            messages.append(f"{label}: the answer does not match the required 9x9 grid format.")
        elif label not in {"GLOBAL_BINDING_ERROR", "LOCAL_MAPPING_ERROR", "CORRECT"}:
            messages.append(f"{label}.")
    return "\n".join(messages) or "The answer is not a valid solution."


def _segment(text: str, symbols: tuple[str, ...], *, expected: int) -> list[str]:
    solutions: list[list[str]] = []

    def visit(position: int, values: list[str]) -> None:
        if len(solutions) > 1 or len(values) > expected:
            return
        if position == len(text):
            if len(values) == expected:
                solutions.append(values.copy())
            return
        for symbol in symbols:
            if text.startswith(symbol, position):
                values.append(symbol)
                visit(position + len(symbol), values)
                values.pop()

    visit(0, [])
    if len(solutions) != 1:
        raise ValueError(f"output cannot be uniquely segmented into {expected} valid symbols")
    return solutions[0]


def _looks_like_refusal(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in REFUSAL_MARKERS)


def _is_truncated(generation: Generation) -> bool:
    reason = (generation.finish_reason or "").lower()
    return reason in {"length", "max_tokens", "max_output_tokens"}
