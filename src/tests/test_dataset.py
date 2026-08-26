import tempfile
import unittest
from pathlib import Path

from sudoku.dataset import (
    DatasetConfig,
    audit_directory,
    generate_dataset,
    read_records,
    write_dataset,
)


class DatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = generate_dataset(DatasetConfig(master_seed=8675309, puzzles_per_tier=1))

    def test_pipeline_produces_each_tier(self) -> None:
        self.assertEqual([record.puzzle_id for record in self.result.records], ["E001", "M001", "H001"])
        self.assertEqual(
            [record.difficulty for record in self.result.records],
            ["easy", "medium", "hard"],
        )

    def test_serialized_dataset_passes_independent_audit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            write_dataset(self.result, output)
            self.assertEqual(read_records(output / "puzzles.jsonl"), self.result.records)
            audit = audit_directory(output)
            self.assertTrue(audit["valid"], audit["errors"])

    def test_same_seed_produces_identical_records(self) -> None:
        regenerated = generate_dataset(DatasetConfig(master_seed=8675309, puzzles_per_tier=1))
        self.assertEqual(self.result, regenerated)


if __name__ == "__main__":
    unittest.main()
