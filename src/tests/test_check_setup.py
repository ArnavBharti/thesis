import importlib.util
import subprocess
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_setup", ROOT / "03_check_setup.py")
assert SPEC is not None and SPEC.loader is not None
CHECK_SETUP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK_SETUP)


class CheckSetupTests(unittest.TestCase):
    def test_cuda_versions_accept_matching_compiler(self) -> None:
        torch = SimpleNamespace(version=SimpleNamespace(cuda="13.0"))
        nvcc_result = subprocess.CompletedProcess([], 0, "Cuda tools, release 13.0, V13.0.88\n", "")
        with (
            patch.object(CHECK_SETUP.importlib, "import_module", return_value=torch),
            patch.object(CHECK_SETUP.Path, "glob", return_value=[Path("/venv/nvcc")]),
            patch.object(CHECK_SETUP.subprocess, "run", return_value=nvcc_result),
        ):
            ready, detail = CHECK_SETUP.check_cuda_versions()

        self.assertTrue(ready)
        self.assertIn("matches", detail)

    def test_cuda_versions_reject_mismatched_compiler(self) -> None:
        torch = SimpleNamespace(version=SimpleNamespace(cuda="13.0"))
        nvcc_result = subprocess.CompletedProcess([], 0, "Cuda tools, release 13.3, V13.3.73\n", "")
        with (
            patch.object(CHECK_SETUP.importlib, "import_module", return_value=torch),
            patch.object(CHECK_SETUP.Path, "glob", return_value=[Path("/venv/nvcc")]),
            patch.object(CHECK_SETUP.subprocess, "run", return_value=nvcc_result),
        ):
            ready, detail = CHECK_SETUP.check_cuda_versions()

        self.assertFalse(ready)
        self.assertIn("nvcc 13.3 does not match PyTorch CUDA 13.0", detail)


if __name__ == "__main__":
    unittest.main()
