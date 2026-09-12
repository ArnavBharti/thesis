import unittest
from pathlib import Path

from diagnose_very_easy import PUZZLE, SOLUTION, diagnostic_request
from lib.calibration import apply_calibration_profile
from lib.config import load_config
from lib.sudoku.grid import preserves_clues
from lib.sudoku.schema import grid_from_compact
from lib.sudoku.solver import count_solutions


ROOT = Path(__file__).resolve().parents[1]


class VeryEasyDiagnosticTests(unittest.TestCase):
    def test_puzzle_is_separate_fixed_and_uniquely_solvable(self) -> None:
        puzzle = grid_from_compact(PUZZLE)
        solution = grid_from_compact(SOLUTION)
        self.assertEqual(puzzle.clue_count, 57)
        self.assertEqual(count_solutions(puzzle, limit=2), 1)
        self.assertTrue(preserves_clues(puzzle, solution))

    def test_request_reuses_verified_constrained_profiles(self) -> None:
        base = load_config(ROOT / "config" / "experiments.example.json")
        for profile_name in (
            "nemotron-verified-constrained",
            "mistral-verified-constrained",
        ):
            _, model = apply_calibration_profile(base, profile_name)
            request = diagnostic_request(model)
            self.assertEqual(request.puzzle_id, "VE001")
            self.assertEqual(request.metadata["difficulty"], "very_easy")
            self.assertIn("Before answering:", request.messages[-1].content)
            self.assertIn("structured_regex", model.extra)


if __name__ == "__main__":
    unittest.main()
