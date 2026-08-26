import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    "run_pipeline", Path(__file__).resolve().parents[1] / "run_pipeline.py"
)
assert SPEC is not None and SPEC.loader is not None
run_pipeline = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(run_pipeline)


class PipelineRunnerTests(unittest.TestCase):
    def test_missing_state_is_treated_as_empty(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "state.json"
            with patch.object(run_pipeline, "STATE_PATH", missing):
                self.assertEqual(
                    run_pipeline._read_state(),
                    {"state_version": run_pipeline.STATE_VERSION, "steps": {}},
                )

    def test_state_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            data_directory = Path(directory)
            state_path = data_directory / "pipeline-state.json"
            state = {"state_version": run_pipeline.STATE_VERSION, "steps": {"tests": {}}}
            with (
                patch.object(run_pipeline, "DATA_DIRECTORY", data_directory),
                patch.object(run_pipeline, "STATE_PATH", state_path),
            ):
                run_pipeline._write_state(state)
                self.assertEqual(run_pipeline._read_state(), state)

    def test_fingerprints_change_with_configuration(self) -> None:
        first = run_pipeline._fingerprints(1, 1)
        second = run_pipeline._fingerprints(2, 1)
        self.assertNotEqual(first["generate"], second["generate"])
        self.assertNotEqual(first["audit"], second["audit"])


if __name__ == "__main__":
    unittest.main()
