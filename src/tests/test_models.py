import unittest

from lib.config import ModelConfig
from lib.models import BackendError, HuggingFaceTokenizerAdapter, final_answer_text
from lib.records import Message


class FakeTokenizer:
    chat_template = "template"

    def __init__(self) -> None:
        self.arguments = None

    def apply_chat_template(self, messages, **arguments):
        self.arguments = arguments
        return messages[0]["content"]


class ModelHelpersTests(unittest.TestCase):
    def test_chat_template_receives_reasoning_effort(self) -> None:
        tokenizer = FakeTokenizer()
        adapter = HuggingFaceTokenizerAdapter(
            tokenizer,
            "fake",
            {"reasoning_effort": "medium"},
        )

        self.assertEqual(adapter.format_chat((Message("user", "solve"),)), "solve")
        self.assertEqual(tokenizer.arguments["reasoning_effort"], "medium")
        self.assertTrue(tokenizer.arguments["add_generation_prompt"])

    def test_think_tags_leave_only_the_final_answer(self) -> None:
        model = ModelConfig(
            name="reasoning-model",
            model_id="model",
            extra={"reasoning_output": "think_tags"},
        )
        raw = "reasoning about the puzzle\n</think>\n\n1 2 3"

        self.assertEqual(final_answer_text(raw, model), "1 2 3")
        self.assertEqual(final_answer_text("unfinished reasoning", model), "")

    def test_unknown_reasoning_output_is_rejected(self) -> None:
        model = ModelConfig(
            name="reasoning-model",
            model_id="model",
            extra={"reasoning_output": "unknown"},
        )

        with self.assertRaises(BackendError):
            final_answer_text("answer", model)


if __name__ == "__main__":
    unittest.main()
