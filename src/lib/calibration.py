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
    verify_before_answer: bool = False
    time_limit: str | None = None
    run_version: int = 1


PROFILES = {
    "mistral-small-4-bounded": CalibrationProfile(
        name="mistral-small-4-bounded",
        model_name="mistral-small-4-local",
        inference=InferenceConfig(
            max_new_tokens=16384,
            temperature=0.6,
            top_p=0.95,
            seed=20260826,
        ),
        extra={
            "chat_template": {"reasoning_effort": "high"},
            "reasoning_output": "mistral_think_tags",
            "bounded_final": {
                "mode": "close_think",
                "reasoning_tokens": 15360,
                "final_tokens": 1024,
            },
        },
    ),
    "nemotron-answer-only": CalibrationProfile(
        name="nemotron-answer-only",
        model_name="nemotron-local",
        inference=InferenceConfig(
            max_new_tokens=256,
            temperature=0.0,
            top_p=1.0,
            seed=20260826,
        ),
        extra={
            "system_prompt": "/no_think",
            "reasoning_output": None,
            "bounded_final": None,
        },
    ),
    "nemotron-answer-only-sampled": CalibrationProfile(
        name="nemotron-answer-only-sampled",
        model_name="nemotron-local",
        inference=InferenceConfig(
            max_new_tokens=1024,
            temperature=0.6,
            top_p=0.95,
            seed=20260826,
        ),
        extra={
            "system_prompt": "/no_think",
            "reasoning_output": None,
            "bounded_final": None,
        },
    ),
    "nemotron-constrained-greedy": CalibrationProfile(
        name="nemotron-constrained-greedy",
        model_name="nemotron-local",
        inference=InferenceConfig(
            max_new_tokens=256,
            temperature=0.0,
            top_p=1.0,
            seed=20260826,
        ),
        extra={
            "system_prompt": "/no_think",
            "reasoning_output": None,
            "bounded_final": None,
            "structured_regex": r"[1-9]( [1-9]){8}(\n[1-9]( [1-9]){8}){8}",
        },
    ),
    "nemotron-verified-constrained": CalibrationProfile(
        name="nemotron-verified-constrained",
        model_name="nemotron-local",
        inference=InferenceConfig(
            max_new_tokens=256,
            temperature=0.0,
            top_p=1.0,
            seed=20260826,
        ),
        extra={
            "system_prompt": "/no_think",
            "reasoning_output": None,
            "bounded_final": None,
            "structured_regex": r"[1-9]( [1-9]){8}(\n[1-9]( [1-9]){8}){8}",
        },
        verify_before_answer=True,
        time_limit="0-00:30",
    ),
    "mistral-verified-constrained": CalibrationProfile(
        name="mistral-verified-constrained",
        model_name="mistral-small-4-local",
        inference=InferenceConfig(
            max_new_tokens=256,
            temperature=0.1,
            top_p=1.0,
            seed=20260826,
        ),
        extra={
            "chat_template": {"reasoning_effort": "none"},
            "reasoning_output": None,
            "bounded_final": None,
            "structured_regex": r"[1-9]( [1-9]){8}(\n[1-9]( [1-9]){8}){8}",
        },
        verify_before_answer=True,
        time_limit="0-00:30",
        run_version=2,
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
    slurm = replace(model.slurm, time_limit=profile.time_limit) if profile.time_limit else model.slurm
    calibrated_model = replace(model, extra=extra, slurm=slurm)
    calibrated_config = replace(
        config,
        run_id=f"configuration-calibration-v{profile.run_version}-{profile.name}",
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
