import unittest

from lib.config import ModelConfig
from lib.config import InferenceConfig
from lib.models import (
    BackendError,
    HuggingFaceTokenizerAdapter,
    bounded_final_options,
    final_answer_text,
    vllm_sampling_options,
)
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

    def test_model_sampling_settings_extend_frozen_inference_settings(self) -> None:
        model = ModelConfig(
            name="sampled-model",
            model_id="model",
            extra={"sampling": {"top_k": 20, "repetition_penalty": 1.05}},
        )
        inference = InferenceConfig(max_new_tokens=4096, temperature=0.7, top_p=0.9, seed=7)

        self.assertEqual(
            vllm_sampling_options(model, inference),
            {
                "max_tokens": 4096,
                "temperature": 0.7,
                "top_p": 0.9,
                "seed": 7,
                "top_k": 20,
                "repetition_penalty": 1.05,
            },
        )

    def test_unknown_model_sampling_setting_is_rejected(self) -> None:
        model = ModelConfig(
            name="sampled-model",
            model_id="model",
            extra={"sampling": {"unsupported": 1}},
        )
        with self.assertRaises(BackendError):
            vllm_sampling_options(model, InferenceConfig())

    def test_bounded_final_reserves_tokens_within_total_limit(self) -> None:
        model = ModelConfig(
            name="bounded-model",
            model_id="model",
            extra={
                "bounded_final": {
                    "mode": "close_think",
                    "reasoning_tokens": 3000,
                    "final_tokens": 1000,
                }
            },
        )
        self.assertEqual(
            bounded_final_options(model, InferenceConfig(max_new_tokens=4096)),
            {
                "mode": "close_think",
                "reasoning_tokens": 3000,
                "final_tokens": 1000,
            },
        )

    def test_bounded_final_cannot_exceed_total_limit(self) -> None:
        model = ModelConfig(
            name="bounded-model",
            model_id="model",
            extra={
                "bounded_final": {
                    "mode": "followup",
                    "reasoning_tokens": 3500,
                    "final_tokens": 1000,
                }
            },
        )
        with self.assertRaises(BackendError):
            bounded_final_options(model, InferenceConfig(max_new_tokens=4096))


if __name__ == "__main__":
    unittest.main()
