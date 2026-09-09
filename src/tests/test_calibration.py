import unittest
from pathlib import Path

from lib.calibration import PROFILES, apply_calibration_profile
from lib.config import load_config


class CalibrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = load_config(
            Path(__file__).resolve().parents[1] / "config" / "experiments.example.json"
        )

    def test_profiles_are_one_model_and_have_separate_run_ids(self) -> None:
        for name, profile in PROFILES.items():
            config, model = apply_calibration_profile(self.config, name)
            self.assertEqual(model.name, profile.model_name)
            self.assertEqual(config.models, (model,))
            self.assertEqual(config.run_id, f"configuration-calibration-v1-{name}")

    def test_profiles_bound_output_length(self) -> None:
        for name in PROFILES:
            config, _ = apply_calibration_profile(self.config, name)
            self.assertLessEqual(config.inference.max_new_tokens, 16384)


if __name__ == "__main__":
    unittest.main()
