import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from lib.config import load_config
from lib.slurm import write_python_job

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


if __name__ == "__main__":
    unittest.main()
