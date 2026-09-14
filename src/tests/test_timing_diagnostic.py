import unittest
from pathlib import Path

from diagnose_timing import select_timing_puzzle
from lib.config import load_config


class TimingDiagnosticTests(unittest.TestCase):
    def test_selects_one_reproducible_puzzle_per_difficulty(self) -> None:
        root = Path(__file__).resolve().parents[1]
        config = load_config(root / "config" / "local-models.json")

        selected = [
            select_timing_puzzle(config, tier)
            for tier in ("easy", "medium", "hard")
        ]

        self.assertEqual(
            [record.difficulty for record in selected],
            ["easy", "medium", "hard"],
        )
        self.assertEqual(len({record.puzzle_id for record in selected}), 3)

    def test_selected_models_fit_sharanga_qos(self) -> None:
        root = Path(__file__).resolve().parents[1]
        config = load_config(root / "config" / "local-models.json")

        expected = {
            "gpt-oss-120b-local": ("gpu_h100_4", 1),
            "qwen-3.5-122b-local": ("gpu_h200_8", 2),
        }
        for name, (partition, gpus) in expected.items():
            model = config.model(name)
            self.assertEqual((model.slurm.partition, model.slurm.gpus), (partition, gpus))
            self.assertLessEqual(model.slurm.cpus, 8 if gpus == 2 else 12)

        self.assertEqual(
            {model.name for model in config.enabled_models},
            set(expected),
        )


if __name__ == "__main__":
    unittest.main()
