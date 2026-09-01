import json
import unittest

from lib.prompts import PromptOptions, format_solution, solve_prompt
from lib.sudoku.grid import Grid
from lib.sudoku.representations import ALPHABETS
from tests.test_grid import PUZZLE, SOLUTION


class PromptTests(unittest.TestCase):
    def test_standard_prompt_matches_protocol_shape(self) -> None:
        prompt = solve_prompt(Grid.parse(PUZZLE), ALPHABETS["greek_letters"])
        self.assertIn("Valid input symbols:\nα β γ δ ε ζ η θ ι", prompt)
        self.assertIn("ε γ . . η . . . .", prompt)
        self.assertTrue(prompt.endswith("Return only 9 lines of 9 space-separated output symbols."))

    def test_cross_prompt_declares_mapping(self) -> None:
        prompt = solve_prompt(
            Grid.parse(PUZZLE),
            ALPHABETS["greek_letters"],
            ALPHABETS["arabic_digits"],
        )
        self.assertIn("α=1", prompt)

    def test_all_output_formats(self) -> None:
        solution = Grid.parse(SOLUTION)
        alphabet = ALPHABETS["greek_letters"]
        self.assertEqual(len(format_solution(solution, alphabet, "spaced").splitlines()), 9)
        self.assertEqual(len(format_solution(solution, alphabet, "compact").splitlines()[0]), 9)
        self.assertEqual(len(format_solution(solution, alphabet, "string81")), 81)
        self.assertEqual(len(json.loads(format_solution(solution, alphabet, "json"))), 9)


if __name__ == "__main__":
    unittest.main()
