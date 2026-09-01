import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from lib.config import load_config
from lib.samples import build_sample_plan, freeze_sample_plan, load_sample_plan
from lib.sudoku.dataset import read_records

ROOT = Path(__file__).resolve().parents[1]


class SamplePlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_config(ROOT / "config" / "experiments.example.json")
        cls.records = read_records(ROOT / "data" / "puzzles.jsonl")

    def test_reduced_samples_are_balanced_nested_and_non_overlapping(self) -> None:
        plan = build_sample_plan(self.config, self.records)
        self.assertEqual(len(plan.pilot_ids), 60)
        self.assertEqual(len(plan.main_ids), 150)
        self.assertEqual(len(plan.mechanism_ids), 30)
        self.assertEqual(len(plan.ablation_ids), 15)
        self.assertTrue(set(plan.pilot_ids).isdisjoint(plan.main_ids))
        self.assertLessEqual(set(plan.mechanism_ids), set(plan.main_ids))
        self.assertLessEqual(set(plan.ablation_ids), set(plan.mechanism_ids))
        for name, per_tier in (("pilot", 20), ("main", 50), ("mechanism", 10), ("ablation", 5)):
            selected = plan.records(name, self.records)
            counts = {tier: sum(record.difficulty == tier for record in selected) for tier in ("easy", "medium", "hard")}
            self.assertEqual(counts, {"easy": per_tier, "medium": per_tier, "hard": per_tier})

    def test_plan_is_deterministic_and_idempotently_frozen(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = replace(self.config, output_directory=Path(directory))
            first = build_sample_plan(config, self.records)
            second = build_sample_plan(config, self.records)
            self.assertEqual(first, second)
            freeze_sample_plan(config, first)
            freeze_sample_plan(config, first)
            self.assertEqual(load_sample_plan(config), first)


if __name__ == "__main__":
    unittest.main()
