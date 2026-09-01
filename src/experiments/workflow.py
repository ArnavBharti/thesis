"""Small helpers for the manual, one-job-at-a-time workflow."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import ExperimentConfig, ModelConfig

INFERENCE_EXPERIMENTS = ("exp2", "exp4", "exp6", "exp7", "exp8", "exp9", "exp10")


@dataclass(frozen=True, slots=True)
class ModelWorkflowStatus:
    qualification_complete: bool
    experiments: dict[str, tuple[bool, ...]]
    finalization_complete: bool

    @property
    def inference_complete(self) -> bool:
        return self.qualification_complete and all(all(parts) for parts in self.experiments.values())

    @property
    def complete(self) -> bool:
        return self.inference_complete and self.finalization_complete


def model_directory(config: ExperimentConfig, model: ModelConfig) -> Path:
    return config.output_directory / config.run_id / model.name


def experiments_for(model: ModelConfig) -> tuple[str, ...]:
    """Experiment 7 needs an exact tokenizer, which closed API models do not expose."""

    if model.backend == "openai_compatible" and not model.tokenizer_id:
        return tuple(name for name in INFERENCE_EXPERIMENTS if name != "exp7")
    return INFERENCE_EXPERIMENTS


def qualification_complete(config: ExperimentConfig, model: ModelConfig) -> bool:
    return qualification_result(config, model) is True


def qualification_result(config: ExperimentConfig, model: ModelConfig) -> bool | None:
    path = model_directory(config, model) / "qualification-status.json"
    try:
        return bool(json.loads(path.read_text(encoding="utf-8")).get("passed"))
    except FileNotFoundError:
        return None
    except (OSError, json.JSONDecodeError, AttributeError):
        raise ValueError(f"invalid qualification status: {path}")


def completion_marker(
    config: ExperimentConfig,
    model: ModelConfig,
    experiment: str,
    shard_index: int,
    shard_count: int,
) -> Path:
    filename = f"part-{shard_index + 1:03d}-of-{shard_count:03d}.complete.json"
    return model_directory(config, model) / experiment / filename


def write_completion_marker(
    config: ExperimentConfig,
    model: ModelConfig,
    experiment: str,
    shard_index: int,
    shard_count: int,
    eligible_requests: int,
) -> Path:
    path = completion_marker(config, model, experiment, shard_index, shard_count)
    value = {
        "status": "COMPLETE",
        "model": model.name,
        "experiment": experiment,
        "part": shard_index + 1,
        "parts": shard_count,
        "eligible_requests": eligible_requests,
    }
    text = json.dumps(value, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") != text:
        raise ValueError(f"completion marker differs from the current job: {path}")
    temporary = path.with_suffix(".tmp")
    temporary.write_text(text, encoding="utf-8", newline="\n")
    temporary.replace(path)
    return path


def experiment_part_complete(
    config: ExperimentConfig,
    model: ModelConfig,
    experiment: str,
    part: int,
) -> bool:
    parts = config.shard_count(experiment)
    if not 1 <= part <= parts:
        raise ValueError(f"part must be between 1 and {parts}")
    if experiment == "exp7":
        status_path = model_directory(config, model) / "exp7" / "status.json"
        try:
            return json.loads(status_path.read_text(encoding="utf-8")).get("status") == "NOT_RUN"
        except FileNotFoundError:
            pass
        except (OSError, json.JSONDecodeError, AttributeError):
            raise ValueError(f"invalid Experiment 7 status: {status_path}")
    marker = completion_marker(config, model, experiment, part - 1, parts)
    try:
        value = json.loads(marker.read_text(encoding="utf-8"))
        return (
            value.get("status") == "COMPLETE"
            and value.get("part") == part
            and value.get("parts") == parts
        )
    except FileNotFoundError:
        return False
    except (OSError, json.JSONDecodeError, AttributeError):
        raise ValueError(f"invalid completion marker: {marker}")


def finalization_complete(config: ExperimentConfig, model: ModelConfig) -> bool:
    directory = model_directory(config, model)
    return (directory / "exp3" / "representation-registry.jsonl").exists() and (
        directory / "analysis" / "summary.json"
    ).exists()


def workflow_status(config: ExperimentConfig, model: ModelConfig) -> ModelWorkflowStatus:
    experiments = {
        experiment: tuple(
            experiment_part_complete(config, model, experiment, part)
            for part in range(1, config.shard_count(experiment) + 1)
        )
        for experiment in experiments_for(model)
    }
    return ModelWorkflowStatus(
        qualification_complete(config, model),
        experiments,
        finalization_complete(config, model),
    )


def status_dict(config: ExperimentConfig, model: ModelConfig) -> dict[str, Any]:
    status = workflow_status(config, model)
    return {
        "model": model.name,
        "qualification": status.qualification_complete,
        "experiments": {
            name: {"complete_parts": sum(parts), "total_parts": len(parts)}
            for name, parts in status.experiments.items()
        },
        "finalization": status.finalization_complete,
        "complete": status.complete,
    }
