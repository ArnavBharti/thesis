import unittest
from pathlib import Path

from diagnose_timing import select_timing_puzzle
from lib.config import load_config


class TimingDiagnosticTests(unittest.TestCase):
    def test_selects_one_reproducible_puzzle_per_difficulty(self) -> None:
        root = Path(__file__).resolve().parents[1]
        config = load_config(root / "config" / "stronger-model-diagnostic.json")

        selected = [
            select_timing_puzzle(config, tier)
            for tier in ("easy", "medium", "hard")
        ]

        self.assertEqual(
            [record.difficulty for record in selected],
            ["easy", "medium", "hard"],
        )
        self.assertEqual(len({record.puzzle_id for record in selected}), 3)


if __name__ == "__main__":
    unittest.main()
