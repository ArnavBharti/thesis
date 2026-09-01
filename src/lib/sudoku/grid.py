"""Canonical immutable representation of a 9x9 Sudoku grid."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, Sequence

SIZE = 9
CELL_COUNT = SIZE * SIZE
DIGITS = frozenset(range(1, 10))
EMPTY = 0


def row_of(cell: int) -> int:
    return cell // SIZE


def column_of(cell: int) -> int:
    return cell % SIZE


def box_of(cell: int) -> int:
    return (row_of(cell) // 3) * 3 + column_of(cell) // 3


ROWS = tuple(tuple(row * SIZE + column for column in range(SIZE)) for row in range(SIZE))
COLUMNS = tuple(tuple(row * SIZE + column for row in range(SIZE)) for column in range(SIZE))
BOXES = tuple(
    tuple(
        (box_row * 3 + row) * SIZE + box_column * 3 + column
        for row in range(3)
        for column in range(3)
    )
    for box_row in range(3)
    for box_column in range(3)
)
UNITS = ROWS + COLUMNS + BOXES
CELL_UNITS = tuple(tuple(unit for unit in UNITS if cell in unit) for cell in range(CELL_COUNT))
PEERS = tuple(
    frozenset(peer for unit in CELL_UNITS[cell] for peer in unit if peer != cell)
    for cell in range(CELL_COUNT)
)


@dataclass(frozen=True, slots=True)
class Grid:
    """An immutable row-major grid where zero denotes an empty cell."""

    cells: tuple[int, ...]

    def __post_init__(self) -> None:
        if len(self.cells) != CELL_COUNT:
            raise ValueError(f"a grid must contain {CELL_COUNT} cells, got {len(self.cells)}")
        invalid = [(index, value) for index, value in enumerate(self.cells) if value not in range(10)]
        if invalid:
            index, value = invalid[0]
            raise ValueError(f"invalid value {value!r} at cell {cell_name(index)}")

    @classmethod
    def from_rows(cls, rows: Sequence[Sequence[int]]) -> Grid:
        if len(rows) != SIZE or any(len(row) != SIZE for row in rows):
            raise ValueError("a grid must contain exactly 9 rows of 9 cells")
        return cls(tuple(value for row in rows for value in row))

    @classmethod
    def parse(cls, text: str) -> Grid:
        rows = [line.split() for line in text.strip().splitlines()]
        if len(rows) != SIZE or any(len(row) != SIZE for row in rows):
            raise ValueError("expected exactly 9 lines of 9 space-separated cells")
        values: list[int] = []
        for row in rows:
            for token in row:
                if token == ".":
                    values.append(EMPTY)
                elif len(token) == 1 and token in "123456789":
                    values.append(int(token))
                else:
                    raise ValueError(f"invalid grid token {token!r}")
        return cls(tuple(values))

    @classmethod
    def empty(cls) -> Grid:
        return cls((EMPTY,) * CELL_COUNT)

    def rows(self) -> tuple[tuple[int, ...], ...]:
        return tuple(self.cells[start : start + SIZE] for start in range(0, CELL_COUNT, SIZE))

    def with_cell(self, cell: int, value: int) -> Grid:
        values = list(self.cells)
        values[cell] = value
        return Grid(tuple(values))

    @property
    def clue_count(self) -> int:
        return sum(value != EMPTY for value in self.cells)

    @property
    def clue_mask(self) -> str:
        return "".join("1" if value else "0" for value in self.cells)

    @property
    def compact(self) -> str:
        return "".join(str(value) if value else "." for value in self.cells)

    def __str__(self) -> str:
        return "\n".join(
            " ".join(str(value) if value else "." for value in row)
            for row in self.rows()
        )


def cell_name(cell: int) -> str:
    return f"r{row_of(cell) + 1}c{column_of(cell) + 1}"


def duplicate_values(grid: Grid) -> Iterator[tuple[str, int, int]]:
    """Yield (unit type, one-based unit number, duplicate value)."""

    for kind, units in (("row", ROWS), ("column", COLUMNS), ("box", BOXES)):
        for number, unit in enumerate(units, start=1):
            seen: set[int] = set()
            for cell in unit:
                value = grid.cells[cell]
                if value and value in seen:
                    yield kind, number, value
                seen.add(value)


def validate_partial(grid: Grid) -> None:
    duplicate = next(duplicate_values(grid), None)
    if duplicate:
        kind, number, value = duplicate
        raise ValueError(f"duplicate {value} in {kind} {number}")


def is_complete_solution(grid: Grid) -> bool:
    return grid.clue_count == CELL_COUNT and not any(duplicate_values(grid))


def preserves_clues(puzzle: Grid, solution: Grid) -> bool:
    return all(not clue or clue == solution.cells[cell] for cell, clue in enumerate(puzzle.cells))


def values_from(iterable: Iterable[int]) -> tuple[int, ...]:
    return tuple(iterable)
