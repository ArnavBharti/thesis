"""Validated serializable records used by the generated dataset."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

from .grid import Grid, is_complete_solution, preserves_clues, validate_partial

Difficulty = Literal["easy", "medium", "hard"]


@dataclass(frozen=True, slots=True)
class DifficultyCertificate:
    deduction_steps: int
    techniques: tuple[str, ...]
    backtracking_required: bool
    maximum_search_depth: int
    search_nodes: int

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["techniques"] = list(self.techniques)
        return result


@dataclass(frozen=True, slots=True)
class PuzzleRecord:
    puzzle_id: str
    difficulty: Difficulty
    puzzle: str
    solution: str
    clue_mask: str
    clue_count: int
    seed: int
    generator_version: str
    solver_certificate: dict[str, Any]
    difficulty_certificate: DifficultyCertificate
    puzzle_sha256: str

    def validate(self) -> None:
        puzzle = grid_from_compact(self.puzzle)
        solution = grid_from_compact(self.solution)
        validate_partial(puzzle)
        if not is_complete_solution(solution):
            raise ValueError(f"{self.puzzle_id}: stored solution is invalid")
        if not preserves_clues(puzzle, solution):
            raise ValueError(f"{self.puzzle_id}: stored solution changes a clue")
        if puzzle.clue_mask != self.clue_mask:
            raise ValueError(f"{self.puzzle_id}: clue mask does not match puzzle")
        if puzzle.clue_count != self.clue_count:
            raise ValueError(f"{self.puzzle_id}: clue count does not match puzzle")

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["difficulty_certificate"] = self.difficulty_certificate.to_dict()
        return result


def grid_from_compact(value: str) -> Grid:
    if len(value) != 81:
        raise ValueError(f"compact grid must contain 81 characters, got {len(value)}")
    cells: list[int] = []
    for token in value:
        if token == ".":
            cells.append(0)
        elif token in "123456789":
            cells.append(int(token))
        else:
            raise ValueError(f"invalid compact grid token {token!r}")
    return Grid(tuple(cells))
