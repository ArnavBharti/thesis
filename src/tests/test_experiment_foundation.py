import json
import tempfile
import unittest
from pathlib import Path

from lib.config import load_config
from lib.records import ExperimentRequest, Message, shard_for
from lib.selection import deterministic_permutation, select_stratified
from lib.sudoku.dataset import read_records


ROOT = Path(__file__).resolve().parents[1]


class ExperimentFoundationTests(unittest.TestCase):
    def test_example_configuration_loads(self) -> None:
        config = load_config(ROOT / "config" / "experiments.example.json")
        self.assertEqual(config.run_id, "thesis-confirmatory-lean-v5")
        self.assertEqual(config.main_per_tier, 50)
        self.assertEqual(config.inference.max_new_tokens, 28672)
        self.assertTrue(config.dataset_path.is_file())
        self.assertEqual(config.enabled_models[0].name, "qwen-local")
        self.assertEqual(
            config.model("qwen-local").extra["chat_template"]["reasoning_effort"],
            "medium",
        )

    def test_only_gpt_and_claude_use_openrouter(self) -> None:
        config = load_config(ROOT / "config" / "experiments.example.json")
        remote = {model.name for model in config.enabled_models if model.backend == "openai_compatible"}
        self.assertEqual(
            remote,
            {"gpt-5.6-terra-openrouter", "claude-sonnet-5-openrouter"},
        )

    def test_request_id_and_shard_are_stable(self) -> None:
        request = ExperimentRequest(
            experiment="exp4",
            condition="greek",
            model="test",
            messages=(Message("user", "prompt"),),
            puzzle_id="E001",
        )
        self.assertEqual(request.request_id, request.request_id)
        self.assertEqual(shard_for(request.request_id, 17), shard_for(request.request_id, 17))

    def test_selection_is_stratified_and_reproducible(self) -> None:
        records = read_records(ROOT / "data" / "puzzles.jsonl")
        first = select_stratified(records, 2, seed=42, namespace="test")
        second = select_stratified(records, 2, seed=42, namespace="test")
        self.assertEqual(first, second)
        self.assertEqual([record.difficulty for record in first], ["easy"] * 2 + ["medium"] * 2 + ["hard"] * 2)

    def test_permutation_is_seed_fixed(self) -> None:
        self.assertEqual(
            deterministic_permutation(range(9), seed=7, namespace="mapping"),
            deterministic_permutation(range(9), seed=7, namespace="mapping"),
        )


if __name__ == "__main__":
    unittest.main()
