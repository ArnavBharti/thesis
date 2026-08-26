import tempfile
import unittest
from pathlib import Path

from experiments.config import load_config
from submit_sharanga import write_job_files


ROOT = Path(__file__).resolve().parents[1]


class SharangaSubmissionTests(unittest.TestCase):
    def test_local_job_requests_gpus_and_uses_srun(self) -> None:
        config = load_config(ROOT / "config" / "experiments.example.json")
        with tempfile.TemporaryDirectory() as directory:
            jobs = write_job_files(
                config,
                config.model("qwen-local"),
                Path(directory),
                venv=Path(".venv"),
                python="python3",
            )
            text = jobs.main.read_text(encoding="utf-8")
            self.assertIn("#SBATCH --partition=gpu_h100_4", text)
            self.assertIn("#SBATCH --gres=gpu:1", text)
            self.assertIn("#SBATCH --array=0-23%4", text)
            self.assertIn("srun python3 run_experiments.py", text)
            self.assertIn("${SLURM_ARRAY_TASK_ID}", text)

    def test_openrouter_job_uses_compute_without_gpu(self) -> None:
        config = load_config(ROOT / "config" / "experiments.example.json")
        with tempfile.TemporaryDirectory() as directory:
            jobs = write_job_files(
                config,
                config.model("gpt-5.6-terra-openrouter"),
                Path(directory),
                venv=Path(".venv"),
                python="python3",
            )
            text = jobs.main.read_text(encoding="utf-8")
            self.assertIn("#SBATCH --partition=compute", text)
            self.assertNotIn("#SBATCH --gres", text)


if __name__ == "__main__":
    unittest.main()
