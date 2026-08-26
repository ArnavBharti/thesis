"""Strict configuration loading for model inference and experimental execution."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

BackendName = Literal["auto", "transformers", "vllm", "openai_compatible"]


@dataclass(frozen=True, slots=True)
class RetryConfig:
    attempts: int = 5
    initial_delay_seconds: float = 2.0
    maximum_delay_seconds: float = 30.0
    timeout_seconds: float = 600.0

    def __post_init__(self) -> None:
        if self.attempts < 1:
            raise ValueError("retry attempts must be positive")
        if self.initial_delay_seconds < 0 or self.maximum_delay_seconds < 0:
            raise ValueError("retry delays must be non-negative")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout must be positive")


@dataclass(frozen=True, slots=True)
class InferenceConfig:
    max_new_tokens: int = 2048
    temperature: float = 0.0
    top_p: float = 1.0
    seed: int = 20260826

    def __post_init__(self) -> None:
        if self.max_new_tokens < 81:
            raise ValueError("max_new_tokens must leave room for a completed Sudoku grid")
        if self.temperature < 0:
            raise ValueError("temperature cannot be negative")
        if not 0 < self.top_p <= 1:
            raise ValueError("top_p must be in (0, 1]")


@dataclass(frozen=True, slots=True)
class ModelConfig:
    name: str
    model_id: str
    backend: BackendName = "auto"
    tokenizer_id: str | None = None
    revision: str | None = None
    dtype: str = "auto"
    tensor_parallel_size: int = 1
    trust_remote_code: bool = False
    local_files_only: bool = True
    api_base: str | None = None
    api_key_env: str | None = None
    enabled: bool = True
    extra: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name or not self.model_id:
            raise ValueError("each model requires a non-empty name and model_id")
        if self.tensor_parallel_size < 1:
            raise ValueError("tensor_parallel_size must be positive")
        if self.backend == "openai_compatible" and not self.api_base:
            raise ValueError(f"model {self.name}: openai_compatible requires api_base")

    @property
    def resolved_model_id(self) -> str:
        return os.path.expandvars(os.path.expanduser(self.model_id))

    @property
    def resolved_tokenizer_id(self) -> str:
        value = self.tokenizer_id or self.model_id
        return os.path.expandvars(os.path.expanduser(value))


@dataclass(frozen=True, slots=True)
class ExperimentConfig:
    run_id: str
    dataset_path: Path
    output_directory: Path
    master_seed: int
    models: tuple[ModelConfig, ...]
    inference: InferenceConfig = InferenceConfig()
    retry: RetryConfig = RetryConfig()
    pilot_per_tier: int = 20
    mechanism_per_tier: int = 20
    ablation_per_tier: int = 10
    slurm_shards: int = 24

    def __post_init__(self) -> None:
        if not self.run_id or any(character.isspace() for character in self.run_id):
            raise ValueError("run_id must be a non-empty identifier without whitespace")
        names = [model.name for model in self.models]
        if len(names) != len(set(names)):
            raise ValueError("model names must be unique")
        if min(self.pilot_per_tier, self.mechanism_per_tier, self.ablation_per_tier) < 1:
            raise ValueError("subset sizes must be positive")
        if self.slurm_shards < 1:
            raise ValueError("slurm_shards must be positive")

    def model(self, name: str) -> ModelConfig:
        for model in self.models:
            if model.name == name:
                return model
        raise KeyError(f"unknown model {name!r}")

    @property
    def enabled_models(self) -> tuple[ModelConfig, ...]:
        return tuple(model for model in self.models if model.enabled)


def load_config(path: Path) -> ExperimentConfig:
    config_path = path.resolve()
    try:
        raw = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read experiment configuration {config_path}: {error}") from error

    base = config_path.parent
    try:
        models = tuple(ModelConfig(**value) for value in raw["models"])
        inference = InferenceConfig(**raw.get("inference", {}))
        retry = RetryConfig(**raw.get("retry", {}))
        dataset_path = _resolve_path(base, raw.get("dataset_path", "../data/puzzles.jsonl"))
        output_directory = _resolve_path(base, raw.get("output_directory", "../experiment_outputs"))
        return ExperimentConfig(
            run_id=raw["run_id"],
            dataset_path=dataset_path,
            output_directory=output_directory,
            master_seed=raw.get("master_seed", 20260826),
            models=models,
            inference=inference,
            retry=retry,
            pilot_per_tier=raw.get("pilot_per_tier", 20),
            mechanism_per_tier=raw.get("mechanism_per_tier", 20),
            ablation_per_tier=raw.get("ablation_per_tier", 10),
            slurm_shards=raw.get("slurm_shards", 24),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(f"invalid experiment configuration {config_path}: {error}") from error


def _resolve_path(base: Path, value: str) -> Path:
    expanded = Path(os.path.expandvars(os.path.expanduser(value)))
    return expanded.resolve() if expanded.is_absolute() else (base / expanded).resolve()
