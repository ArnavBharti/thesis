"""Small, fixed model profiles used only before the confirmatory protocol is frozen."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from .config import ExperimentConfig, InferenceConfig, ModelConfig


@dataclass(frozen=True, slots=True)
class CalibrationProfile:
    name: str
    model_name: str
    inference: InferenceConfig
    extra: dict[str, Any]


PROFILES = {
    "qwen-official-thinking": CalibrationProfile(
        name="qwen-official-thinking",
        model_name="qwen-local",
        inference=InferenceConfig(
            max_new_tokens=16384,
            temperature=1.0,
            top_p=0.95,
            seed=20260826,
        ),
        extra={
            "chat_template": {
                "enable_thinking": True,
                "preserve_thinking": False,
                "reasoning_effort": "medium",
            },
            "reasoning_output": "think_tags",
            "sampling": {
                "top_k": 20,
                "min_p": 0.0,
                "presence_penalty": 0.0,
                "repetition_penalty": 1.0,
            },
        },
    ),
    "glm-official-thinking": CalibrationProfile(
        name="glm-official-thinking",
        model_name="glm-flash-local",
        inference=InferenceConfig(
            max_new_tokens=16384,
            temperature=1.0,
            top_p=0.95,
            seed=20260826,
        ),
        extra={
            "chat_template": {"enable_thinking": True},
            "reasoning_output": "think_tags",
            "sampling": {},
        },
    ),
    "kimi-sampled-guarded": CalibrationProfile(
        name="kimi-sampled-guarded",
        model_name="kimi-linear-local",
        inference=InferenceConfig(
            max_new_tokens=8192,
            temperature=0.7,
            top_p=0.9,
            seed=20260826,
        ),
        extra={
            "sampling": {
                "top_k": 20,
                "repetition_penalty": 1.05,
            },
        },
    ),
    "qwen-bounded-final": CalibrationProfile(
        name="qwen-bounded-final",
        model_name="qwen-local",
        inference=InferenceConfig(
            max_new_tokens=16384,
            temperature=1.0,
            top_p=0.95,
            seed=20260826,
        ),
        extra={
            "chat_template": {
                "enable_thinking": True,
                "preserve_thinking": False,
                "reasoning_effort": "medium",
            },
            "reasoning_output": "think_tags",
            "sampling": {
                "top_k": 20,
                "min_p": 0.0,
                "presence_penalty": 0.0,
                "repetition_penalty": 1.0,
            },
            "bounded_final": {
                "mode": "close_think",
                "reasoning_tokens": 15360,
                "final_tokens": 1024,
            },
        },
    ),
    "glm-bounded-final": CalibrationProfile(
        name="glm-bounded-final",
        model_name="glm-flash-local",
        inference=InferenceConfig(
            max_new_tokens=16384,
            temperature=1.0,
            top_p=0.95,
            seed=20260826,
        ),
        extra={
            "chat_template": {"enable_thinking": True},
            "reasoning_output": "think_tags",
            "sampling": {},
            "bounded_final": {
                "mode": "close_think",
                "reasoning_tokens": 15360,
                "final_tokens": 1024,
            },
        },
    ),
    "kimi-bounded-final": CalibrationProfile(
        name="kimi-bounded-final",
        model_name="kimi-linear-local",
        inference=InferenceConfig(
            max_new_tokens=8192,
            temperature=0.7,
            top_p=0.9,
            seed=20260826,
        ),
        extra={
            "sampling": {
                "top_k": 20,
                "repetition_penalty": 1.05,
            },
            "bounded_final": {
                "mode": "followup",
                "reasoning_tokens": 7168,
                "final_tokens": 1024,
            },
        },
    ),
}


def apply_calibration_profile(
    config: ExperimentConfig,
    profile_name: str,
) -> tuple[ExperimentConfig, ModelConfig]:
    """Return an isolated configuration for one declared calibration profile."""

    try:
        profile = PROFILES[profile_name]
    except KeyError as error:
        choices = ", ".join(sorted(PROFILES))
        raise ValueError(f"unknown calibration profile {profile_name!r}; choose one of: {choices}") from error

    model = config.model(profile.model_name)
    extra = _merge_extra(model.extra, profile.extra)
    calibrated_model = replace(model, extra=extra)
    calibrated_config = replace(
        config,
        run_id=f"configuration-calibration-v1-{profile.name}",
        inference=profile.inference,
        models=(calibrated_model,),
    )
    return calibrated_config, calibrated_model


def _merge_extra(original: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    result = dict(original)
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = {**result[key], **value}
        else:
            result[key] = value
    return result
