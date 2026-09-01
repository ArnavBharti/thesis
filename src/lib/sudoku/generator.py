"""Seed-reproducible generation of complete grids and unique Sudoku puzzles."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random

from .difficulty import DifficultyAnalysis, analyze_difficulty
from .grid import CELL_COUNT, Grid
from .schema import Difficulty
from .solver import count_solutions, solve

GENERATOR_VERSION = "1.0.0"
TARGET_CLUE_RANGES: dict[Difficulty, tuple[int, int]] = {
    "easy": (40, 46),
    "medium": (24, 27),
    "hard": (22, 26),
}


@dataclass(frozen=True, slots=True)
class GeneratedPuzzle:
    puzzle: Grid
    solution: Grid
    seed: int
    analysis: DifficultyAnalysis


def generate_solution(seed: int) -> Grid:
    solution = solve(Grid.empty(), randomizer=Random(seed))
    if solution is None:  # pragma: no cover - the empty Sudoku grid is solvable
        raise RuntimeError("failed to generate a completed grid")
    return solution


def carve_unique_puzzle(solution: Grid, seed: int, target_clues: int) -> Grid:
    """Remove clues in seeded order, accepting only removals that preserve uniqueness."""

    if not 17 <= target_clues <= 80:
        raise ValueError("target clue count must be between 17 and 80")
    rng = Random(seed)
    cells = list(range(CELL_COUNT))
    rng.shuffle(cells)
    puzzle = solution
    for cell in cells:
        if puzzle.clue_count <= target_clues:
            break
        candidate = puzzle.with_cell(cell, 0)
        if count_solutions(candidate, limit=2) == 1:
            puzzle = candidate
    return puzzle


def generate_candidate(seed: int, requested_difficulty: Difficulty) -> GeneratedPuzzle:
    rng = Random(seed)
    solution_seed = rng.getrandbits(63)
    carve_seed = rng.getrandbits(63)
    low, high = TARGET_CLUE_RANGES[requested_difficulty]
    target_clues = rng.randint(low, high)
    solution = generate_solution(solution_seed)
    puzzle = carve_unique_puzzle(solution, carve_seed, target_clues)
    analysis = analyze_difficulty(puzzle)
    return GeneratedPuzzle(puzzle, solution, seed, analysis)


def find_candidate(
    starting_seed: int,
    requested_difficulty: Difficulty,
    *,
    maximum_attempts: int = 10_000,
) -> tuple[GeneratedPuzzle, int]:
    """Find the first candidate of a requested tier and return it with attempts consumed."""

    for offset in range(maximum_attempts):
        candidate = generate_candidate(starting_seed + offset, requested_difficulty)
        if candidate.analysis.difficulty == requested_difficulty:
            return candidate, offset + 1
    raise RuntimeError(
        f"could not generate a {requested_difficulty} puzzle in {maximum_attempts} attempts"
    )
