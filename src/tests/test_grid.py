import unittest

from sudoku.grid import Grid, cell_name, is_complete_solution, preserves_clues, validate_partial


PUZZLE = """\
5 3 . . 7 . . . .
6 . . 1 9 5 . . .
. 9 8 . . . . 6 .
8 . . . 6 . . . 3
4 . . 8 . 3 . . 1
7 . . . 2 . . . 6
. 6 . . . . 2 8 .
. . . 4 1 9 . . 5
. . . . 8 . . 7 9"""

SOLUTION = """\
5 3 4 6 7 8 9 1 2
6 7 2 1 9 5 3 4 8
1 9 8 3 4 2 5 6 7
8 5 9 7 6 1 4 2 3
4 2 6 8 5 3 7 9 1
7 1 3 9 2 4 8 5 6
9 6 1 5 3 7 2 8 4
2 8 7 4 1 9 6 3 5
3 4 5 2 8 6 1 7 9"""


class GridTests(unittest.TestCase):
    def test_parse_and_format_round_trip(self) -> None:
        grid = Grid.parse(PUZZLE)
        self.assertEqual(str(grid), PUZZLE)
        self.assertEqual(grid.clue_count, 30)
        self.assertEqual(len(grid.clue_mask), 81)

    def test_complete_solution_and_clue_preservation(self) -> None:
        puzzle = Grid.parse(PUZZLE)
        solution = Grid.parse(SOLUTION)
        self.assertTrue(is_complete_solution(solution))
        self.assertTrue(preserves_clues(puzzle, solution))

    def test_partial_duplicate_is_rejected(self) -> None:
        grid = Grid.parse(PUZZLE).with_cell(2, 5)
        with self.assertRaisesRegex(ValueError, "duplicate 5 in row 1"):
            validate_partial(grid)

    def test_cell_names_are_one_based(self) -> None:
        self.assertEqual(cell_name(0), "r1c1")
        self.assertEqual(cell_name(80), "r9c9")


if __name__ == "__main__":
    unittest.main()
