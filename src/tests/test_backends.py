import unittest

from experiments.backends import CharacterTokenizer, StaticBackend
from experiments.config import InferenceConfig, ModelConfig, RetryConfig
from experiments.records import Message


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


if __name__ == "__main__":
    unittest.main()
