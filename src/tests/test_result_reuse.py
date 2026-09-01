import tempfile
import unittest
from pathlib import Path

from lib.records import ExperimentRequest, ExperimentResult, Generation, Message
from lib.results import ResultStore, iter_result_values, store_reused_result


class ResultReuseTests(unittest.TestCase):
    def test_reuse_stores_a_new_request_without_a_model_attempt(self) -> None:
        source_request = ExperimentRequest(
            experiment="exp4",
            condition="arabic_digits",
            model="test",
            messages=(Message("user", "same prompt"),),
            puzzle_id="E001",
        )
        source_result = ExperimentResult(
            request=source_request,
            status="OK",
            generation=Generation("answer", "stop", 10, 2, 1.0),
            evaluation={"outcome": "CORRECT", "results": [{"type": "CORRECT"}]},
            attempts=1,
            error=None,
            started_at="start",
            completed_at="end",
        ).to_dict()
        target = ExperimentRequest(
            experiment="exp6",
            condition="A_arabic_to_arabic",
            model="test",
            messages=(Message("user", "same prompt"),),
            puzzle_id="E001",
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "results.jsonl"
            store = ResultStore(path)
            self.assertTrue(store_reused_result(store, target, source_result))
            self.assertFalse(store_reused_result(store, target, source_result))
            value = next(iter(iter_result_values((path,))))
            self.assertEqual(value["attempts"], 0)
            self.assertEqual(
                value["generation"]["provider_metadata"]["reused_from_request_id"],
                source_request.request_id,
            )


if __name__ == "__main__":
    unittest.main()
