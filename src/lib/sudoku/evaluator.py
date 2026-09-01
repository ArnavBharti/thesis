"""Strict response parser and deterministic evaluator for completed Sudoku grids."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Literal

from .grid import BOXES, COLUMNS, ROWS, Grid, cell_name
from .representations import SymbolAlphabet

Outcome = Literal["CORRECT", "INCORRECT", "NOT_EVALUATED"]
OPERATIONAL_RESULTS = frozenset({"API_ERROR", "TIMEOUT"})


@dataclass(frozen=True, slots=True)
class Evaluation:
    outcome: Outcome
    results: tuple[dict[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return {"outcome": self.outcome, "results": list(self.results)}


def parse_response(text: str, alphabet: SymbolAlphabet) -> tuple[Grid | None, list[dict[str, Any]]]:
    if not text:
        return None, [{"type": "NO_FINAL_ANSWER"}]
    try:
        text.encode("utf-8", errors="strict").decode("utf-8", errors="strict")
    except UnicodeError as error:
        return None, [{"type": "UNICODE_ERROR", "message": str(error)}]

    rows = text.splitlines()
    errors: list[dict[str, Any]] = []
    if len(rows) != 9:
        errors.append({"type": "WRONG_ROW_COUNT", "expected": 9, "actual": len(rows)})

    tokens_by_row = [row.split(" ") for row in rows]
    cell_count = sum(len(tokens) for tokens in tokens_by_row)
    if cell_count != 81:
        errors.append({"type": "WRONG_CELL_COUNT", "expected": 81, "actual": cell_count})

    exact_format = len(rows) == 9 and all(
        len(tokens) == 9 and all(token for token in tokens)
        for tokens in tokens_by_row
    )
    if not exact_format:
        errors.append(
            {
                "type": "FORMAT_ERROR",
                "message": "expected exactly 9 lines of 9 single-space-separated symbols",
            }
        )

    invalid_symbols: list[dict[str, Any]] = []
    for row_number, tokens in enumerate(tokens_by_row, start=1):
        for column_number, token in enumerate(tokens, start=1):
            if token and token not in alphabet.symbols:
                invalid_symbols.append(
                    {
                        "type": "INVALID_SYMBOL",
                        "cell": f"r{row_number}c{column_number}",
                        "actual": token,
                    }
                )
    errors.extend(invalid_symbols)
    if errors:
        return None, errors

    values = tuple(alphabet.value_for(token) for tokens in tokens_by_row for token in tokens)
    return Grid(values), []


def evaluate_response(
    puzzle: Grid,
    expected_solution: Grid,
    response: str | None,
    alphabet: SymbolAlphabet,
    *,
    operational_result: str | None = None,
) -> Evaluation:
    if operational_result is not None:
        if operational_result not in OPERATIONAL_RESULTS:
            raise ValueError(f"unknown operational result {operational_result!r}")
        return Evaluation("NOT_EVALUATED", ({"type": operational_result},))

    candidate, parse_errors = parse_response(response or "", alphabet)
    if candidate is None:
        return Evaluation("INCORRECT", tuple(parse_errors))

    results: list[dict[str, Any]] = []
    for cell, clue in enumerate(puzzle.cells):
        actual = candidate.cells[cell]
        if clue and clue != actual:
            results.append(
                {
                    "type": "GIVEN_MODIFIED",
                    "cell": cell_name(cell),
                    "expected": alphabet.symbol_for(clue),
                    "actual": alphabet.symbol_for(actual),
                }
            )

    for label, unit_name, units in (
        ("ROW_CONSTRAINT_ERROR", "row", ROWS),
        ("COLUMN_CONSTRAINT_ERROR", "column", COLUMNS),
        ("BOX_CONSTRAINT_ERROR", "box", BOXES),
    ):
        for number, unit in enumerate(units, start=1):
            values = [candidate.cells[cell] for cell in unit]
            counts = Counter(values)
            duplicates = sorted(value for value, count in counts.items() if count > 1)
            missing = sorted(set(range(1, 10)) - set(values))
            if duplicates or missing:
                result: dict[str, Any] = {"type": label, unit_name: number}
                if duplicates:
                    result["duplicate"] = [alphabet.symbol_for(value) for value in duplicates]
                if missing:
                    result["missing"] = [alphabet.symbol_for(value) for value in missing]
                results.append(result)

    if candidate != expected_solution:
        binding = _binding_error(expected_solution, candidate)
        results.append({"type": binding})

    if not results:
        return Evaluation("CORRECT", ({"type": "CORRECT"},))
    return Evaluation("INCORRECT", tuple(results))


def _binding_error(expected: Grid, actual: Grid) -> str:
    mapping: dict[int, int] = {}
    for expected_value, actual_value in zip(expected.cells, actual.cells, strict=True):
        existing = mapping.setdefault(expected_value, actual_value)
        if existing != actual_value:
            return "LOCAL_MAPPING_ERROR"
    if len(mapping) == 9 and len(set(mapping.values())) == 9 and any(key != value for key, value in mapping.items()):
        return "GLOBAL_BINDING_ERROR"
    return "LOCAL_MAPPING_ERROR"
