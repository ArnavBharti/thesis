import subprocess
import sys
import unittest
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
        result = subprocess.run(
            [sys.executable, "steps/07_show_status.py", "--model", "qwen-local"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("qualification: not complete", result.stdout)
        self.assertIn("steps/04_submit_qualification.py qwen-local", result.stdout)

    def test_qualification_dry_run_writes_one_job(self) -> None:
        result = subprocess.run(
            [sys.executable, "steps/04_submit_qualification.py", "qwen-local", "--dry-run"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("DRY RUN", result.stdout)
        self.assertIn("qualification.sbatch", result.stdout)


if __name__ == "__main__":
    unittest.main()
