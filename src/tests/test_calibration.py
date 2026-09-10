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

    def test_nemotron_uses_documented_reasoning_off_settings(self) -> None:
        config, model = apply_calibration_profile(self.config, "nemotron-answer-only")
        self.assertEqual(config.inference.max_new_tokens, 256)
        self.assertEqual(config.inference.temperature, 0.0)
        self.assertEqual(config.inference.top_p, 1.0)
        self.assertEqual(model.extra["system_prompt"], "/no_think")
        self.assertIsNone(model.extra["reasoning_output"])
        self.assertIsNone(model.extra["bounded_final"])

    def test_nemotron_sampled_profile_changes_only_decoding_budget(self) -> None:
        config, model = apply_calibration_profile(
            self.config, "nemotron-answer-only-sampled"
        )
        self.assertEqual(config.inference.max_new_tokens, 1024)
        self.assertEqual(config.inference.temperature, 0.6)
        self.assertEqual(config.inference.top_p, 0.95)
        self.assertEqual(model.extra["system_prompt"], "/no_think")
        self.assertIsNone(model.extra["reasoning_output"])
        self.assertIsNone(model.extra["bounded_final"])

    def test_nemotron_constrained_profile_requires_exact_grid_shape(self) -> None:
        config, model = apply_calibration_profile(
            self.config, "nemotron-constrained-greedy"
        )
        self.assertEqual(config.inference.temperature, 0.0)
        regex = model.extra["structured_regex"]
        import re

        grid = "1 2 3 4 5 6 7 8 9\n" * 8 + "1 2 3 4 5 6 7 8 9"
        self.assertIsNotNone(re.fullmatch(regex, grid))
        self.assertIsNone(re.fullmatch(regex, "Here is the answer:\n" + grid))


if __name__ == "__main__":
    unittest.main()
