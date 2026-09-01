import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class StepScriptTests(unittest.TestCase):
    def test_every_numbered_script_has_working_help(self) -> None:
        scripts = sorted((ROOT / "steps").glob("[0-9][0-9]_*.py"))
        self.assertEqual(len(scripts), 7)
        for script in scripts:
            result = subprocess.run(
                [sys.executable, str(script), "--help"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, msg=f"{script.name}: {result.stderr}")

    def test_status_script_prints_the_next_command(self) -> None:
        with self._temporary_config() as config:
            result = subprocess.run(
                [
                    sys.executable,
                    "steps/06_show_status.py",
                    "--config",
                    str(config),
                    "--model",
                    "qwen-local",
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
        self.assertIn("qualification: not complete", result.stdout)
        self.assertIn("steps/04_submit_qualification.py qwen-local", result.stdout)

    def test_qualification_dry_run_writes_one_job(self) -> None:
        with self._temporary_config() as config:
            result = subprocess.run(
                [
                    sys.executable,
                    "steps/04_submit_qualification.py",
                    "qwen-local",
                    "--config",
                    str(config),
                    "--dry-run",
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
        self.assertIn("DRY RUN", result.stdout)
        self.assertIn("qualification.sbatch", result.stdout)

    @contextmanager
    def _temporary_config(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = ROOT / "config" / "experiments.example.json"
            value = json.loads(source.read_text(encoding="utf-8"))
            value["run_id"] = "test-step-scripts"
            value["output_directory"] = str(directory / "outputs")
            value["dataset_path"] = str(ROOT / "data" / "puzzles.jsonl")
            path = directory / "experiments.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            yield path


if __name__ == "__main__":
    unittest.main()
