"""Difficulty analysis based on reproducible human techniques and controlled search."""

from __future__ import annotations

from dataclasses import dataclass

from .grid import Grid, is_complete_solution, validate_partial
from .schema import Difficulty, DifficultyCertificate
from .solver import SearchStats, solve
from .techniques import INTERMEDIATE_TECHNIQUES, SINGLE_TECHNIQUES, TechniqueState


@dataclass(frozen=True, slots=True)
class DifficultyAnalysis:
    difficulty: Difficulty
    certificate: DifficultyCertificate


def analyze_difficulty(puzzle: Grid) -> DifficultyAnalysis:
    """Classify a valid puzzle using fixed technique order and deterministic tie-breaking."""

    validate_partial(puzzle)
    state = TechniqueState.from_grid(puzzle)
    steps = 0
    used: list[str] = []

    while not state.solved:
        progress = False
        for name, technique in SINGLE_TECHNIQUES + INTERMEDIATE_TECHNIQUES:
            if technique(state):
                steps += 1
                if name not in used:
                    used.append(name)
                progress = True
                break
        if not progress:
            break

    if state.solved:
        solved = state.grid()
        if not is_complete_solution(solved):
            raise ValueError("technique solver produced an invalid completed grid")
        intermediate_names = {name for name, _ in INTERMEDIATE_TECHNIQUES}
        difficulty: Difficulty = "medium" if intermediate_names.intersection(used) else "easy"
        return DifficultyAnalysis(
            difficulty,
            DifficultyCertificate(
                deduction_steps=steps,
                techniques=tuple(used),
                backtracking_required=False,
                maximum_search_depth=0,
                search_nodes=0,
            ),
        )

    stats = SearchStats()
    if solve(state.grid(), stats=stats) is None:
        raise ValueError("puzzle is unsatisfiable")
    return DifficultyAnalysis(
        "hard",
        DifficultyCertificate(
            deduction_steps=steps,
            techniques=tuple(used),
            backtracking_required=True,
            maximum_search_depth=stats.maximum_depth,
            search_nodes=stats.nodes,
        ),
    )
