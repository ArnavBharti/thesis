import unittest

from lib.config import InferenceConfig, ModelConfig, RetryConfig
from lib.models import CharacterTokenizer, StaticBackend, vllm_runtime_options
from lib.records import Message


class BackendTests(unittest.TestCase):
    def test_static_backend_is_deterministic(self) -> None:
        model = ModelConfig(
            name="mock",
            model_id="mock",
            backend="auto",
            extra={"responses": ["first", "second"]},
        )
        backend = StaticBackend(model, InferenceConfig(), RetryConfig())
        messages = (Message("user", "test"),)
        self.assertEqual(backend.generate(messages).text, "first")
        self.assertEqual(backend.generate(messages).text, "second")

    def test_character_tokenizer_supports_diagnostics(self) -> None:
        tokenizer = CharacterTokenizer()
        self.assertEqual(tokenizer.encode("α"), [ord("α")])
        self.assertEqual(tokenizer.identity, "character-tokenizer-v1")

    def test_qwen_uses_triton_gdn_without_changing_frozen_config(self) -> None:
        model = ModelConfig(
            name="qwen-local",
            model_id="Qwen/Qwen3.8-27B",
            backend="vllm",
            extra={"vllm": {"max_model_len": 32768}},
        )
        self.assertNotIn("gdn_prefill_backend", model.extra["vllm"])
        options = vllm_runtime_options(model)
        self.assertEqual(options["gdn_prefill_backend"], "triton")
        self.assertEqual(options["max_num_seqs"], 1)


if __name__ == "__main__":
    unittest.main()
