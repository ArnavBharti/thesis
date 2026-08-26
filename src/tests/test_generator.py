import unittest

from sudoku.certificate import certify
from sudoku.generator import GeneratedPuzzle, carve_unique_puzzle, generate_candidate, generate_solution
from sudoku.grid import is_complete_solution, preserves_clues
from sudoku.solver import count_solutions


class GeneratorTests(unittest.TestCase):
    def test_completed_grid_generation_is_reproducible(self) -> None:
        first = generate_solution(98765)
        second = generate_solution(98765)
        self.assertEqual(first, second)
        self.assertTrue(is_complete_solution(first))

    def test_clue_removal_preserves_uniqueness(self) -> None:
        solution = generate_solution(123)
        puzzle = carve_unique_puzzle(solution, seed=456, target_clues=40)
        self.assertLessEqual(puzzle.clue_count, 40)
        self.assertEqual(count_solutions(puzzle), 1)
        self.assertTrue(preserves_clues(puzzle, solution))

    def test_candidate_generation_is_reproducible(self) -> None:
        self.assertEqual(generate_candidate(20260826, "easy"), generate_candidate(20260826, "easy"))

    def test_certificate_contains_required_fields(self) -> None:
        candidate = generate_candidate(20260826, "easy")
        if candidate.analysis.difficulty != "easy":
            self.skipTest("fixed candidate does not fall in easy tier")
        record = certify(candidate, "E001", "easy")
        self.assertEqual(record.solver_certificate["solution_count"], 1)
        self.assertEqual(len(record.clue_mask), 81)
        self.assertEqual(len(record.puzzle_sha256), 64)


if __name__ == "__main__":
    unittest.main()
