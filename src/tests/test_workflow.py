import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from experiments.config import load_config
from experiments.slurm import experiment_job, qualification_job
from experiments.workflow import (
    experiment_part_complete,
    experiments_for,
    workflow_status,
    write_completion_marker,
)


ROOT = Path(__file__).resolve().parents[1]


class WorkflowTests(unittest.TestCase):
    def test_experiment_four_has_24_manual_parts(self) -> None:
        config = load_config(ROOT / "config" / "experiments.example.json")
        self.assertEqual(config.shard_count("exp4"), 24)
        self.assertEqual(config.shard_count("exp2"), 1)

    def test_closed_models_skip_tokenizer_experiment(self) -> None:
        config = load_config(ROOT / "config" / "experiments.example.json")
        model = config.model("gpt-5.6-terra-openrouter")
        self.assertNotIn("exp7", experiments_for(model))

    def test_complete_study_uses_158_single_jobs(self) -> None:
        config = load_config(ROOT / "config" / "experiments.example.json")
        jobs = 0
        for model in config.enabled_models:
            jobs += 1  # qualification
            jobs += sum(config.shard_count(name) for name in experiments_for(model))
            jobs += 1  # finalization
        self.assertEqual(jobs, 158)

    def test_completion_markers_are_readable_and_idempotent(self) -> None:
        original = load_config(ROOT / "config" / "experiments.example.json")
        with tempfile.TemporaryDirectory() as directory:
            config = replace(original, output_directory=Path(directory))
            model = config.model("qwen-local")
            marker = write_completion_marker(config, model, "exp4", 0, 24, 113)
            write_completion_marker(config, model, "exp4", 0, 24, 113)
            self.assertTrue(experiment_part_complete(config, model, "exp4", 1))
            self.assertEqual(json.loads(marker.read_text())["eligible_requests"], 113)

    def test_status_starts_incomplete(self) -> None:
        original = load_config(ROOT / "config" / "experiments.example.json")
        with tempfile.TemporaryDirectory() as directory:
            config = replace(original, output_directory=Path(directory))
            status = workflow_status(config, config.model("qwen-local"))
            self.assertFalse(status.complete)
            self.assertEqual(len(status.experiments["exp4"]), 24)

    def test_slurm_file_contains_one_job_without_an_array(self) -> None:
        config = load_config(ROOT / "config" / "experiments.example.json")
        model = config.model("qwen-local")
        with tempfile.TemporaryDirectory() as directory, patch(
            "experiments.slurm.ROOT", Path(directory)
        ):
            path = experiment_job(
                ROOT / "config" / "experiments.example.json",
                config,
                model,
                "exp4",
                3,
            )
            text = path.read_text(encoding="utf-8")
            self.assertIn("#SBATCH --partition=gpu_h100_4", text)
            self.assertIn("#SBATCH --gres=gpu:1", text)
            self.assertNotIn("#SBATCH --array", text)
            self.assertIn("--shard-index 2 --shard-count 24", text)
            self.assertEqual(text.count("srun "), 1)

    def test_qualification_file_contains_only_qualification(self) -> None:
        config = load_config(ROOT / "config" / "experiments.example.json")
        model = config.model("gpt-5.6-terra-openrouter")
        with tempfile.TemporaryDirectory() as directory, patch(
            "experiments.slurm.ROOT", Path(directory)
        ):
            path = qualification_job(
                ROOT / "config" / "experiments.example.json", config, model
            )
            text = path.read_text(encoding="utf-8")
            self.assertIn("#SBATCH --partition=compute", text)
            self.assertNotIn("#SBATCH --gres", text)
            self.assertIn("--experiments qualification", text)


if __name__ == "__main__":
    unittest.main()
