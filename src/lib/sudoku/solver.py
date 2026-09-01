"""Exact backtracking solver with a caller-supplied solution limit."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random

from .grid import BOXES, COLUMNS, ROWS, Grid, box_of, column_of, row_of, validate_partial

ALL_DIGITS_MASK = (1 << 9) - 1


@dataclass(slots=True)
class SearchStats:
    nodes: int = 0
    maximum_depth: int = 0


def _bit(value: int) -> int:
    return 1 << (value - 1)


def _digits(mask: int) -> list[int]:
    values: list[int] = []
    while mask:
        least = mask & -mask
        values.append(least.bit_length())
        mask ^= least
    return values


def _initial_masks(grid: Grid) -> tuple[list[int], list[int], list[int]]:
    validate_partial(grid)
    row_masks = [0] * 9
    column_masks = [0] * 9
    box_masks = [0] * 9
    for cell, value in enumerate(grid.cells):
        if value:
            digit = _bit(value)
            row_masks[row_of(cell)] |= digit
            column_masks[column_of(cell)] |= digit
            box_masks[box_of(cell)] |= digit
    return row_masks, column_masks, box_masks


def solve(
    grid: Grid,
    *,
    randomizer: Random | None = None,
    stats: SearchStats | None = None,
) -> Grid | None:
    """Return one exact solution, or ``None`` when the puzzle is unsatisfiable."""

    solutions = _search(grid, limit=1, randomizer=randomizer, stats=stats)
    return solutions[0] if solutions else None


def count_solutions(grid: Grid, limit: int = 2, *, stats: SearchStats | None = None) -> int:
    """Count solutions, stopping as soon as ``limit`` solutions have been found."""

    if limit < 1:
        raise ValueError("solution limit must be at least one")
    return len(_search(grid, limit=limit, stats=stats))


def _search(
    grid: Grid,
    *,
    limit: int,
    randomizer: Random | None = None,
    stats: SearchStats | None = None,
) -> list[Grid]:
    row_masks, column_masks, box_masks = _initial_masks(grid)
    values = list(grid.cells)
    solutions: list[Grid] = []
    search_stats = stats if stats is not None else SearchStats()

    def visit(depth: int) -> None:
        if len(solutions) >= limit:
            return
        search_stats.nodes += 1
        search_stats.maximum_depth = max(search_stats.maximum_depth, depth)

        selected_cell = -1
        selected_mask = 0
        selected_count = 10
        ties: list[tuple[int, int]] = []

        for cell, value in enumerate(values):
            if value:
                continue
            mask = ALL_DIGITS_MASK & ~(
                row_masks[row_of(cell)] | column_masks[column_of(cell)] | box_masks[box_of(cell)]
            )
            count = mask.bit_count()
            if count == 0:
                return
            if count < selected_count:
                selected_cell, selected_mask, selected_count = cell, mask, count
                ties = [(cell, mask)]
            elif count == selected_count:
                ties.append((cell, mask))

        if selected_cell < 0:
            solutions.append(Grid(tuple(values)))
            return

        if randomizer is not None and len(ties) > 1:
            selected_cell, selected_mask = randomizer.choice(ties)

        candidates = _digits(selected_mask)
        if randomizer is not None:
            randomizer.shuffle(candidates)

        row = row_of(selected_cell)
        column = column_of(selected_cell)
        box = box_of(selected_cell)
        for value in candidates:
            digit = _bit(value)
            values[selected_cell] = value
            row_masks[row] |= digit
            column_masks[column] |= digit
            box_masks[box] |= digit
            visit(depth + 1)
            values[selected_cell] = 0
            row_masks[row] ^= digit
            column_masks[column] ^= digit
            box_masks[box] ^= digit
            if len(solutions) >= limit:
                return

    visit(0)
    return solutions
