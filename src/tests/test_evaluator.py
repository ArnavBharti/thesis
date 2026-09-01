import unittest

from lib.sudoku.evaluator import evaluate_response, parse_response
from lib.sudoku.grid import Grid
from lib.sudoku.representations import ALPHABETS, encode_grid
from tests.test_grid import PUZZLE, SOLUTION


class EvaluatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.puzzle = Grid.parse(PUZZLE)
        self.solution = Grid.parse(SOLUTION)
        self.greek = ALPHABETS["greek_letters"]

    def test_accepts_exact_transformed_solution(self) -> None:
        evaluation = evaluate_response(
            self.puzzle,
            self.solution,
            encode_grid(self.solution, self.greek),
            self.greek,
        )
        self.assertEqual(evaluation.outcome, "CORRECT")
        self.assertEqual(evaluation.results, ({"type": "CORRECT"},))

    def test_reports_changed_clue_and_constraints(self) -> None:
        response = encode_grid(self.solution, self.greek).replace("ε", "ζ", 1)
        evaluation = evaluate_response(self.puzzle, self.solution, response, self.greek)
        labels = {result["type"] for result in evaluation.results}
        self.assertEqual(evaluation.outcome, "INCORRECT")
        self.assertIn("GIVEN_MODIFIED", labels)
        self.assertIn("ROW_CONSTRAINT_ERROR", labels)
        self.assertIn("BOX_CONSTRAINT_ERROR", labels)
        self.assertIn("LOCAL_MAPPING_ERROR", labels)

    def test_detects_a_consistent_global_permutation(self) -> None:
        permuted = Grid(tuple(2 if value == 1 else 1 if value == 2 else value for value in self.solution.cells))
        evaluation = evaluate_response(
            Grid.empty(), self.solution, encode_grid(permuted, self.greek), self.greek
        )
        labels = {result["type"] for result in evaluation.results}
        self.assertIn("GLOBAL_BINDING_ERROR", labels)

    def test_strict_parser_rejects_commas(self) -> None:
        response = encode_grid(self.solution, self.greek).replace(" ", ",")
        grid, errors = parse_response(response, self.greek)
        self.assertIsNone(grid)
        self.assertIn("FORMAT_ERROR", {error["type"] for error in errors})

    def test_operational_failure_is_not_evaluated(self) -> None:
        evaluation = evaluate_response(
            self.puzzle, self.solution, None, self.greek, operational_result="TIMEOUT"
        )
        self.assertEqual(evaluation.outcome, "NOT_EVALUATED")
        self.assertEqual(evaluation.results, ({"type": "TIMEOUT"},))


if __name__ == "__main__":
    unittest.main()
