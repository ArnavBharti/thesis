import tempfile
import unittest
from pathlib import Path

from experiments.backends import StaticBackend
from experiments.config import InferenceConfig, ModelConfig, RetryConfig
from experiments.executor import ExperimentExecutor
from experiments.records import ExperimentRequest, Message
from experiments.storage import ResultStore


class ExecutorTests(unittest.TestCase):
    def test_execution_is_resumable(self) -> None:
        model = ModelConfig(name="mock", model_id="mock", extra={"response": "expected"})
        backend = StaticBackend(model, InferenceConfig(), RetryConfig(attempts=1))
        request = ExperimentRequest(
            experiment="exp6",
            condition="control",
            model="mock",
            messages=(Message("user", "test"),),
            metadata={"evaluation_kind": "exact_text", "expected_text": "expected"},
        )
        with tempfile.TemporaryDirectory() as directory:
            store = ResultStore(Path(directory) / "results.jsonl")
            executor = ExperimentExecutor(backend, store, RetryConfig(attempts=1))
            first = executor.run([request])
            second = executor.run([request])
            self.assertEqual(first.executed, 1)
            self.assertEqual(first.correct, 1)
            self.assertEqual(second.executed, 0)
            self.assertEqual(second.completed_before_run, 1)

    def test_shards_partition_requests(self) -> None:
        model = ModelConfig(name="mock", model_id="mock", extra={"response": "x"})
        requests = [
            ExperimentRequest(
                experiment="test",
                condition=str(index),
                model="mock",
                messages=(Message("user", str(index)),),
                metadata={"evaluation_kind": "exact_text", "expected_text": "x"},
            )
            for index in range(20)
        ]
        eligible = 0
        with tempfile.TemporaryDirectory() as directory:
            for shard in range(4):
                backend = StaticBackend(model, InferenceConfig(), RetryConfig(attempts=1))
                store = ResultStore(Path(directory) / f"{shard}.jsonl")
                summary = ExperimentExecutor(
                    backend, store, RetryConfig(attempts=1), shard_index=shard, shard_count=4
                ).run(requests)
                eligible += summary.eligible
        self.assertEqual(eligible, len(requests))


if __name__ == "__main__":
    unittest.main()
