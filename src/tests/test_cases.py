import unittest
from pathlib import Path

from experiments.backends import CharacterTokenizer
from experiments.cases import CaseFactory
from experiments.config import load_config
from sudoku.dataset import read_records


ROOT = Path(__file__).resolve().parents[1]


class CaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_config(ROOT / "config" / "experiments.example.json")
        cls.model = cls.config.model("qwen-local")
        cls.records = read_records(cls.config.dataset_path)
        cls.factory = CaseFactory(cls.config, cls.records)

    def test_qualification_has_five_requests(self) -> None:
        requests = list(self.factory.requests("qualification", self.model))
        self.assertEqual(len(requests), 5)
        self.assertEqual(len({request.request_id for request in requests}), 5)

    def test_pilot_has_sixty_times_four_requests(self) -> None:
        self.assertEqual(len(list(self.factory.requests("exp2", self.model))), 60 * 4)

    def test_main_experiment_has_300_times_nine_requests(self) -> None:
        self.assertEqual(len(list(self.factory.requests("exp4", self.model))), 300 * 9)

    def test_cross_experiment_has_four_solves_and_five_controls_per_puzzle(self) -> None:
        requests = list(self.factory.requests("exp6", self.model))
        self.assertEqual(len(requests), 60 * 9)

    def test_binding_experiment_has_eleven_conditions_per_puzzle(self) -> None:
        requests = list(self.factory.requests("exp8", self.model))
        self.assertEqual(len(requests), 60 * 11)

    def test_ablation_and_revision_counts(self) -> None:
        self.assertEqual(len(list(self.factory.requests("exp9", self.model))), 30 * 19)
        self.assertEqual(len(list(self.factory.requests("exp10", self.model))), 30 * 3 * 4)

    def test_token_experiment_fails_cleanly_when_tokenizer_cannot_make_sets(self) -> None:
        with self.assertRaisesRegex(ValueError, "could not construct"):
            list(self.factory.requests("exp7", self.model, tokenizer=CharacterTokenizer()))


if __name__ == "__main__":
    unittest.main()
