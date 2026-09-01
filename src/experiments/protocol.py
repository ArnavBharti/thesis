"""Protocol manifest creation and freeze checks before model inference."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .backends import TokenizerAdapter
from .cases import CaseFactory, INFERENCE_EXPERIMENTS
from .config import ExperimentConfig, ModelConfig


def build_protocol_manifest(
    config: ExperimentConfig,
    model: ModelConfig,
    factory: CaseFactory,
    *,
    tokenizer: TokenizerAdapter | None = None,
) -> dict[str, Any]:
    experiments: dict[str, Any] = {}
    for experiment in INFERENCE_EXPERIMENTS:
        if experiment == "exp7" and tokenizer is None:
            experiments[experiment] = {"request_count": None, "request_digest": None, "requires_tokenizer": True}
            continue
        try:
            requests = tuple(factory.requests(experiment, model, tokenizer=tokenizer))
            ids = sorted(request.request_id for request in requests)
            experiments[experiment] = {
                "request_count": len(ids),
                "request_digest": _digest_text("\n".join(ids)),
                "requires_tokenizer": experiment == "exp7",
            }
        except ValueError as error:
            experiments[experiment] = {
                "request_count": None,
                "request_digest": None,
                "requires_tokenizer": experiment == "exp7",
                "protocol_error": str(error),
            }
    return {
        "protocol_version": "1.0.0",
        "run_id": config.run_id,
        "master_seed": config.master_seed,
        "dataset_path": str(config.dataset_path),
        "dataset_sha256": _sha256_file(config.dataset_path),
        "model": asdict(model),
        "inference": asdict(config.inference),
        "retry": asdict(config.retry),
        "subset_sizes": {
            "pilot_per_tier": config.pilot_per_tier,
            "mechanism_per_tier": config.mechanism_per_tier,
            "ablation_per_tier": config.ablation_per_tier,
        },
        "experiment_shards": config.experiment_shards,
        "tokenizer": tokenizer.identity if tokenizer else None,
        "experiments": experiments,
    }


def freeze_protocol(path: Path, manifest: dict[str, Any]) -> None:
    encoded = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing != manifest:
            raise ValueError(
                f"protocol at {path} is already frozen with different inputs; use a new run_id"
            )
        return
    path.write_text(encoded, encoding="utf-8", newline="\n")


def _digest_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
