"""Creation and independent validation of solver-certified puzzle records."""

from __future__ import annotations

import hashlib

from .generator import GENERATOR_VERSION, GeneratedPuzzle
from .grid import is_complete_solution, preserves_clues
from .schema import Difficulty, PuzzleRecord
from .solver import SearchStats, count_solutions, solve


def certify(candidate: GeneratedPuzzle, puzzle_id: str, difficulty: Difficulty) -> PuzzleRecord:
    if candidate.analysis.difficulty != difficulty:
        raise ValueError("candidate difficulty does not match requested certificate tier")
    if not is_complete_solution(candidate.solution):
        raise ValueError("candidate solution is not a complete Sudoku grid")
    if not preserves_clues(candidate.puzzle, candidate.solution):
        raise ValueError("candidate solution changes a given clue")

    stats = SearchStats()
    solution_count = count_solutions(candidate.puzzle, limit=2, stats=stats)
    if solution_count != 1:
        raise ValueError(f"candidate has {solution_count} solutions under capped counting")
    exact_solution = solve(candidate.puzzle)
    if exact_solution != candidate.solution:
        raise ValueError("stored solution differs from the exact solver result")

    digest = hashlib.sha256(candidate.puzzle.compact.encode("ascii")).hexdigest()
    record = PuzzleRecord(
        puzzle_id=puzzle_id,
        difficulty=difficulty,
        puzzle=candidate.puzzle.compact,
        solution=candidate.solution.compact,
        clue_mask=candidate.puzzle.clue_mask,
        clue_count=candidate.puzzle.clue_count,
        seed=candidate.seed,
        generator_version=GENERATOR_VERSION,
        solver_certificate={
            "algorithm": "constraint_propagating_backtracking_mrv",
            "solution_count": solution_count,
            "solution_count_limit": 2,
            "search_nodes": stats.nodes,
            "maximum_search_depth": stats.maximum_depth,
        },
        difficulty_certificate=candidate.analysis.certificate,
        puzzle_sha256=digest,
    )
    record.validate()
    return record
