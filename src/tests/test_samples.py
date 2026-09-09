import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from lib.config import load_config
from lib.protocol import freeze_json, global_protocol, verify_global_protocol
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
        self.assertEqual(len(plan.pilot_ids), 15)
        self.assertEqual(len(plan.main_ids), 60)
        self.assertEqual(len(plan.mechanism_ids), 15)
        self.assertEqual(len(plan.ablation_ids), 9)
        self.assertTrue(set(plan.pilot_ids).isdisjoint(plan.main_ids))
        self.assertLessEqual(set(plan.mechanism_ids), set(plan.main_ids))
        self.assertLessEqual(set(plan.ablation_ids), set(plan.mechanism_ids))
        for name, per_tier in (("pilot", 5), ("main", 20), ("mechanism", 5), ("ablation", 3)):
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

    def test_global_protocol_is_idempotent_and_freezes_models(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = replace(self.config, output_directory=Path(directory))
            plan = build_sample_plan(config, self.records)
            freeze_sample_plan(config, plan)
            value = global_protocol(config, plan)
            self.assertEqual(len(value["models"]), 4)
            path = config.output_directory / config.run_id / "protocol.json"
            freeze_json(path, value)
            verify_global_protocol(config, plan)


if __name__ == "__main__":
    unittest.main()
