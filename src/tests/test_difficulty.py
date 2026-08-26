import unittest

from sudoku.difficulty import analyze_difficulty
from sudoku.grid import Grid
from tests.test_grid import PUZZLE


EASY_PUZZLE = """\
. 3 4 6 7 8 9 1 2
6 . 2 1 9 5 3 4 8
1 9 . 3 4 2 5 6 7
8 5 9 . 6 1 4 2 3
4 2 6 8 . 3 7 9 1
7 1 3 9 2 . 8 5 6
9 6 1 5 3 7 . 8 4
2 8 7 4 1 9 6 . 5
3 4 5 2 8 6 1 7 ."""


class DifficultyTests(unittest.TestCase):
    def test_classifies_singles_only_puzzle_as_easy(self) -> None:
        analysis = analyze_difficulty(Grid.parse(EASY_PUZZLE))
        self.assertEqual(analysis.difficulty, "easy")
        self.assertFalse(analysis.certificate.backtracking_required)
        self.assertIn("naked_single", analysis.certificate.techniques)

    def test_analysis_is_deterministic(self) -> None:
        puzzle = Grid.parse(PUZZLE)
        self.assertEqual(analyze_difficulty(puzzle), analyze_difficulty(puzzle))


if __name__ == "__main__":
    unittest.main()
