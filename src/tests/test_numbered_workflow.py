import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from lib.config import load_config
from lib.selection import select_stratified
from lib.slurm import write_python_job
from lib.sudoku.dataset import read_records
from lib.sudoku.representations import ALPHABETS, encode_grid
from lib.sudoku.schema import grid_from_compact

ROOT = Path(__file__).resolve().parents[1]


class NumberedWorkflowTests(unittest.TestCase):
    def test_every_numbered_script_has_working_help(self) -> None:
        scripts = sorted(ROOT.glob("[0-9][0-9]_*.py"))
        self.assertEqual(len(scripts), 13)
        for script in scripts:
            result = subprocess.run(
                [sys.executable, str(script), "--help"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, f"{script.name}: {result.stderr}")

    def test_numbered_scripts_do_not_import_another_main(self) -> None:
        for script in ROOT.glob("[0-9][0-9]_*.py"):
            source = script.read_text(encoding="utf-8")
            self.assertNotIn("import main", source, script.name)
            self.assertNotIn("run_experiments", source, script.name)
            self.assertNotIn("run_pipeline", source, script.name)

    def test_slurm_job_runs_the_same_numbered_script_once(self) -> None:
        config = load_config(ROOT / "config" / "experiments.example.json")
        model = config.enabled_models[0]
        with tempfile.TemporaryDirectory() as directory, patch("lib.slurm.ROOT", Path(directory)):
            script = ROOT / "07_run_main_benchmark.py"
            path = write_python_job(config, model, script, "main-test", (model.name, "--part", "1"))
            text = path.read_text(encoding="utf-8")
            self.assertIn("07_run_main_benchmark.py", text)
            self.assertIn("--execute", text)
            self.assertNotIn("--array", text)
            self.assertEqual(text.count("srun "), 1)
            self.assertIn("export VLLM_CACHE_ROOT=", text)
            self.assertIn("export TORCHINDUCTOR_CACHE_DIR=", text)
            self.assertIn("export TRITON_CACHE_DIR=", text)
            self.assertIn("export FLASHINFER_WORKSPACE_BASE=", text)
            self.assertIn("site-packages/nvidia/cu*/bin/nvcc", text)
            self.assertIn('export CUDACXX="$NVCC_PATH"', text)

    def test_reduced_call_and_job_counts_are_frozen(self) -> None:
        qualification = 5 * 5
        pilot = 60 * 4 * 5
        main = 150 * 9 * 5
        input_output = 30 * 7 * 5
        token_length = 30 * 3 * 3
        binding = 30 * 8 * 5
        ablations = 15 * 19 * 5
        revision_minimum = 15 * 3 * 3 * 5
        revision_maximum = 15 * 3 * 4 * 5
        fixed = qualification + pilot + main + input_output + token_length + binding + ablations
        self.assertEqual(fixed + revision_minimum, 12_595)
        self.assertEqual(fixed + revision_maximum, 12_820)

        jobs = 5 + 5 + (6 * 5) + 5 + 3 + 5 + 5 + 5 + 5
        self.assertEqual(jobs, 68)

    def test_qualification_pilot_and_freeze_execute_and_rerun_cleanly(self) -> None:
        records = read_records(ROOT / "data" / "puzzles.jsonl")
        selected = select_stratified(records, 2, seed=20260826, namespace="qualification")[:5]
        representations = (
            "arabic_digits",
            "greek_letters",
            "emoji",
            "nonce_labels",
            "devanagari_numerals",
        )
        responses = [
            encode_grid(grid_from_compact(record.solution), ALPHABETS[name])
            for record, name in zip(selected, representations, strict=True)
        ]
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            config = {
                "run_id": "qualification-integration-test",
                "dataset_path": str(ROOT / "data" / "puzzles.jsonl"),
                "output_directory": str(temporary / "outputs"),
                "master_seed": 20260826,
                "pilot_per_tier": 20,
                "main_per_tier": 50,
                "mechanism_per_tier": 10,
                "ablation_per_tier": 5,
                "experiment_shards": {
                    "exp2": 1,
                    "exp4": 6,
                    "exp6": 1,
                    "exp7": 1,
                    "exp8": 1,
                    "exp9": 1,
                    "exp10": 1,
                },
                "retry": {"attempts": 1},
                "models": [
                    {
                        "name": "mock",
                        "model_id": "mock",
                        "backend": "static",
                        "extra": {"responses": responses},
                    }
                ],
            }
            config_path = temporary / "config.json"
            config_path.write_text(json.dumps(config), encoding="utf-8")
            command = [
                sys.executable,
                str(ROOT / "04_qualify_model.py"),
                "mock",
                "--config",
                str(config_path),
                "--execute",
            ]
            first = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            second = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("SKIP", second.stdout)

            pilot_command = [
                sys.executable,
                str(ROOT / "05_run_pilot.py"),
                "mock",
                "--config",
                str(config_path),
                "--execute",
            ]
            pilot = subprocess.run(pilot_command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(pilot.returncode, 0, pilot.stderr)
            pilot_file = (
                temporary
                / "outputs"
                / "qualification-integration-test"
                / "mock"
                / "exp2"
                / "shard-000-of-001.jsonl"
            )
            self.assertEqual(len(pilot_file.read_text(encoding="utf-8").splitlines()), 240)
            repeated_pilot = subprocess.run(pilot_command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(repeated_pilot.returncode, 0, repeated_pilot.stderr)
            self.assertIn("SKIP", repeated_pilot.stdout)

            freeze = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "06_freeze_protocol.py"),
                    "--config",
                    str(config_path),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(freeze.returncode, 0, freeze.stderr)
            sample_path = (
                temporary
                / "outputs"
                / "qualification-integration-test"
                / "sample-plan.json"
            )
            sample = json.loads(sample_path.read_text(encoding="utf-8"))
            self.assertEqual(len(sample["pilot_ids"]), 60)
            self.assertEqual(len(sample["main_ids"]), 150)

            main_command = [
                sys.executable,
                str(ROOT / "07_run_main_benchmark.py"),
                "mock",
                "--part",
                "1",
                "--config",
                str(config_path),
                "--execute",
            ]
            main = subprocess.run(main_command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(main.returncode, 0, main.stderr)
            main_file = (
                temporary
                / "outputs"
                / "qualification-integration-test"
                / "mock"
                / "exp4"
                / "shard-000-of-006.jsonl"
            )
            main_count = len(main_file.read_text(encoding="utf-8").splitlines())
            self.assertGreater(main_count, 180)
            self.assertLess(main_count, 270)
            repeated_main = subprocess.run(main_command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(repeated_main.returncode, 0, repeated_main.stderr)
            self.assertIn("SKIP", repeated_main.stdout)


if __name__ == "__main__":
    unittest.main()
