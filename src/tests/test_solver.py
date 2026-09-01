import random
import unittest

from lib.sudoku.grid import Grid, is_complete_solution, preserves_clues
from lib.sudoku.solver import SearchStats, count_solutions, solve
from tests.test_grid import PUZZLE, SOLUTION


class SolverTests(unittest.TestCase):
    def test_solves_outline_example(self) -> None:
        puzzle = Grid.parse(PUZZLE)
        self.assertEqual(solve(puzzle), Grid.parse(SOLUTION))
        self.assertEqual(count_solutions(puzzle), 1)

    def test_counts_only_to_limit(self) -> None:
        stats = SearchStats()
        self.assertEqual(count_solutions(Grid.empty(), limit=2, stats=stats), 2)
        self.assertGreater(stats.nodes, 0)

    def test_rejects_contradictory_grid(self) -> None:
        invalid = Grid.parse(PUZZLE).with_cell(2, 5)
        with self.assertRaises(ValueError):
            solve(invalid)

    def test_seeded_random_solution_is_reproducible(self) -> None:
        first = solve(Grid.empty(), randomizer=random.Random(1234))
        second = solve(Grid.empty(), randomizer=random.Random(1234))
        self.assertEqual(first, second)
        self.assertIsNotNone(first)
        assert first is not None
        self.assertTrue(is_complete_solution(first))
        self.assertTrue(preserves_clues(Grid.empty(), first))


if __name__ == "__main__":
    unittest.main()
