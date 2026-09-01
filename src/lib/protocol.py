"""Freeze checks for global and per-step experiment protocols."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from .config import ExperimentConfig, ModelConfig
from .records import ExperimentRequest
from .samples import SamplePlan


def global_protocol(
    config: ExperimentConfig,
    sample_plan: SamplePlan,
) -> dict[str, object]:
    """Return the decisions that must be fixed before confirmatory inference."""

    return {
        "protocol_version": "2.0.0-lean",
        "run_id": config.run_id,
        "master_seed": config.master_seed,
        "dataset_path": str(config.dataset_path),
        "dataset_sha256": sample_plan.dataset_sha256,
        "sample_plan": asdict(sample_plan),
        "sample_sizes_per_tier": {
            "pilot": config.pilot_per_tier,
            "main": config.main_per_tier,
            "mechanism": config.mechanism_per_tier,
            "ablation": config.ablation_per_tier,
        },
        "inference": asdict(config.inference),
        "retry": asdict(config.retry),
        "experiment_shards": config.experiment_shards,
        "baseline_reuse": {
            "exp6": ["A_arabic_to_arabic", "B_greek_to_greek"],
            "exp8": ["uppercase_standard", "digits_ordinary", "nonce_neutral"],
            "exp10": "Each revision branch starts from its matching exp4 response.",
        },
    }


def freeze_json(path: Path, value: dict[str, object]) -> Path:
    """Write immutable JSON, or verify that the existing file is identical."""

    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_text(encoding="utf-8") != text:
            raise ValueError(f"frozen file differs at {path}; use a new run_id")
        return path
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8", newline="\n")
    temporary.replace(path)
    return path


def freeze_step_requests(
    config: ExperimentConfig,
    model: ModelConfig,
    step_name: str,
    requests: Iterable[ExperimentRequest],
    *,
    notes: dict[str, object] | None = None,
) -> Path:
    """Freeze the exact request IDs for one model and numbered experiment step."""

    request_ids = sorted(request.request_id for request in requests)
    value: dict[str, object] = {
        "run_id": config.run_id,
        "model": asdict(model),
        "step": step_name,
        "request_count": len(request_ids),
        "request_id_sha256": _digest("\n".join(request_ids)),
        "inference": asdict(config.inference),
        "retry": asdict(config.retry),
    }
    if notes:
        value["notes"] = notes
    path = (
        config.output_directory
        / config.run_id
        / model.name
        / step_name
        / "request-manifest.json"
    )
    return freeze_json(path, value)


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
