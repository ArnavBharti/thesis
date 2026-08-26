import json
import unittest

from experiments.evaluation import checker_feedback, evaluate_generation, normalize_output
from experiments.records import ExperimentRequest, Generation, Message
from sudoku.grid import Grid
from sudoku.representations import ALPHABETS
from tests.test_grid import PUZZLE, SOLUTION


def request(output_format: str = "spaced") -> ExperimentRequest:
    alphabet = ALPHABETS["greek_letters"]
    return ExperimentRequest(
        experiment="test",
        condition="test",
        model="mock",
        messages=(Message("user", "solve"),),
        puzzle_id="T001",
        output_alphabet=alphabet.name,
        puzzle=Grid.parse(PUZZLE).compact,
        expected_solution=Grid.parse(SOLUTION).compact,
        metadata={
            "evaluation_kind": "sudoku",
            "output_symbols": list(alphabet.symbols),
            "output_format": output_format,
        },
    )


class ExperimentEvaluationTests(unittest.TestCase):
    def test_normalizes_json_output(self) -> None:
        alphabet = ALPHABETS["greek_letters"]
        rows = [[alphabet.symbol_for(value) for value in row] for row in Grid.parse(SOLUTION).rows()]
        normalized = normalize_output(json.dumps(rows), alphabet, "json")
        self.assertEqual(len(normalized.splitlines()), 9)

    def test_evaluates_correct_json_solution(self) -> None:
        alphabet = ALPHABETS["greek_letters"]
        rows = [[alphabet.symbol_for(value) for value in row] for row in Grid.parse(SOLUTION).rows()]
        generation = Generation(json.dumps(rows), "stop", 10, 81, 0.1)
        self.assertEqual(evaluate_generation(request("json"), generation)["outcome"], "CORRECT")

    def test_truncation_and_refusal_labels(self) -> None:
        truncated = Generation("α β", "length", 10, 2, 0.1)
        self.assertEqual(
            evaluate_generation(request(), truncated)["results"][0]["type"],
            "TRUNCATED_OUTPUT",
        )
        refusal = Generation("I cannot solve this.", "stop", 10, 5, 0.1)
        self.assertEqual(evaluate_generation(request(), refusal)["results"][0]["type"], "REFUSAL")

    def test_checker_feedback_does_not_supply_correct_cells(self) -> None:
        feedback = checker_feedback(
            {
                "outcome": "INCORRECT",
                "results": [
                    {"type": "ROW_CONSTRAINT_ERROR", "row": 4, "duplicate": ["ε"], "missing": ["θ"]}
                ],
            }
        )
        self.assertIn("Row 4", feedback)
        self.assertNotIn("correct value", feedback)


if __name__ == "__main__":
    unittest.main()
