import tempfile
import unittest
from pathlib import Path

from experiments.cases import CaseFactory
from experiments.config import load_config
from experiments.protocol import build_protocol_manifest, freeze_protocol
from sudoku.dataset import read_records


ROOT = Path(__file__).resolve().parents[1]


class ProtocolTests(unittest.TestCase):
    def test_manifest_has_frozen_main_call_count(self) -> None:
        config = load_config(ROOT / "config" / "experiments.example.json")
        factory = CaseFactory(config, read_records(config.dataset_path))
        manifest = build_protocol_manifest(config, config.model("qwen-local"), factory)
        self.assertEqual(manifest["experiments"]["exp4"]["request_count"], 2700)

    def test_freeze_rejects_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "protocol.json"
            freeze_protocol(path, {"version": 1})
            freeze_protocol(path, {"version": 1})
            with self.assertRaisesRegex(ValueError, "already frozen"):
                freeze_protocol(path, {"version": 2})


if __name__ == "__main__":
    unittest.main()
