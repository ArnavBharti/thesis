"""Deterministic Sudoku techniques used for difficulty certification."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from .grid import BOXES, CELL_COUNT, CELL_UNITS, COLUMNS, PEERS, ROWS, UNITS, Grid, box_of
from .solver import ALL_DIGITS_MASK


def _bit(value: int) -> int:
    return 1 << (value - 1)


def _single_value(mask: int) -> int:
    return mask.bit_length()


@dataclass(slots=True)
class TechniqueState:
    values: list[int]
    candidates: list[int]

    @classmethod
    def from_grid(cls, grid: Grid) -> TechniqueState:
        values = list(grid.cells)
        candidates = [0] * CELL_COUNT
        for cell, value in enumerate(values):
            if value:
                continue
            used = 0
            for peer in PEERS[cell]:
                peer_value = values[peer]
                if peer_value:
                    used |= _bit(peer_value)
            candidates[cell] = ALL_DIGITS_MASK & ~used
            if candidates[cell] == 0:
                raise ValueError("puzzle contains a cell with no candidates")
        return cls(values, candidates)

    @property
    def solved(self) -> bool:
        return all(self.values)

    def grid(self) -> Grid:
        return Grid(tuple(self.values))

    def place(self, cell: int, value: int) -> None:
        digit = _bit(value)
        if not self.candidates[cell] & digit:
            raise ValueError("attempted to place a value that is not a candidate")
        self.values[cell] = value
        self.candidates[cell] = 0
        for peer in PEERS[cell]:
            if not self.values[peer]:
                self.candidates[peer] &= ~digit
                if self.candidates[peer] == 0:
                    raise ValueError("deduction produced a cell with no candidates")


def apply_naked_single(state: TechniqueState) -> bool:
    for cell, mask in enumerate(state.candidates):
        if not state.values[cell] and mask.bit_count() == 1:
            state.place(cell, _single_value(mask))
            return True
    return False


def apply_hidden_single(state: TechniqueState) -> bool:
    for unit in UNITS:
        for value in range(1, 10):
            digit = _bit(value)
            cells = [cell for cell in unit if not state.values[cell] and state.candidates[cell] & digit]
            if len(cells) == 1:
                state.place(cells[0], value)
                return True
    return False


def apply_naked_pair(state: TechniqueState) -> bool:
    for unit in UNITS:
        pairs: dict[int, list[int]] = {}
        for cell in unit:
            mask = state.candidates[cell]
            if not state.values[cell] and mask.bit_count() == 2:
                pairs.setdefault(mask, []).append(cell)
        for mask in sorted(pairs):
            pair_cells = pairs[mask]
            if len(pair_cells) != 2:
                continue
            changed = False
            for cell in unit:
                if cell not in pair_cells and not state.values[cell] and state.candidates[cell] & mask:
                    state.candidates[cell] &= ~mask
                    if state.candidates[cell] == 0:
                        raise ValueError("naked pair removed every candidate from a cell")
                    changed = True
            if changed:
                return True
    return False


def apply_hidden_pair(state: TechniqueState) -> bool:
    for unit in UNITS:
        locations: dict[int, tuple[int, ...]] = {}
        for value in range(1, 10):
            digit = _bit(value)
            cells = tuple(cell for cell in unit if not state.values[cell] and state.candidates[cell] & digit)
            if len(cells) == 2:
                locations[value] = cells
        for first, second in combinations(sorted(locations), 2):
            if locations[first] != locations[second]:
                continue
            keep = _bit(first) | _bit(second)
            if any(state.candidates[cell] & ~keep for cell in locations[first]):
                for cell in locations[first]:
                    state.candidates[cell] &= keep
                return True
    return False


def apply_pointing_pair(state: TechniqueState) -> bool:
    for box in BOXES:
        box_cells = frozenset(box)
        for value in range(1, 10):
            digit = _bit(value)
            cells = [cell for cell in box if not state.values[cell] and state.candidates[cell] & digit]
            if len(cells) < 2:
                continue
            row_units = {cell // 9 for cell in cells}
            column_units = {cell % 9 for cell in cells}
            targets: tuple[int, ...] | None = None
            if len(row_units) == 1:
                targets = ROWS[next(iter(row_units))]
            elif len(column_units) == 1:
                targets = COLUMNS[next(iter(column_units))]
            if targets and _eliminate(state, targets, digit, excluded=box_cells):
                return True
    return False


def apply_box_line(state: TechniqueState) -> bool:
    for unit in ROWS + COLUMNS:
        unit_cells = frozenset(unit)
        for value in range(1, 10):
            digit = _bit(value)
            cells = [cell for cell in unit if not state.values[cell] and state.candidates[cell] & digit]
            if len(cells) < 2:
                continue
            boxes = {box_of(cell) for cell in cells}
            if len(boxes) == 1 and _eliminate(
                state, BOXES[next(iter(boxes))], digit, excluded=unit_cells
            ):
                return True
    return False


def _eliminate(
    state: TechniqueState,
    targets: tuple[int, ...],
    digit: int,
    *,
    excluded: frozenset[int],
) -> bool:
    changed = False
    for cell in targets:
        if cell not in excluded and not state.values[cell] and state.candidates[cell] & digit:
            state.candidates[cell] &= ~digit
            if state.candidates[cell] == 0:
                raise ValueError("candidate elimination removed every candidate from a cell")
            changed = True
    return changed


SINGLE_TECHNIQUES = (
    ("naked_single", apply_naked_single),
    ("hidden_single", apply_hidden_single),
)
INTERMEDIATE_TECHNIQUES = (
    ("naked_pair", apply_naked_pair),
    ("hidden_pair", apply_hidden_pair),
    ("pointing_pair", apply_pointing_pair),
    ("box_line", apply_box_line),
)
