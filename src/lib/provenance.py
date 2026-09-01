"""Runtime provenance captured once per model run."""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

from .config import ExperimentConfig, ModelConfig


def collect_provenance(config: ExperimentConfig, model: ModelConfig) -> dict[str, Any]:
    return {
        "run_id": config.run_id,
        "model": model.name,
        "model_id": model.resolved_model_id,
        "tokenizer_id": model.resolved_tokenizer_id,
        "revision": model.revision,
        "backend": model.backend,
        "dtype": model.dtype,
        "tensor_parallel_size": model.tensor_parallel_size,
        "python": sys.version,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "git_commit": _git_commit(),
        "dataset_sha256": _sha256_file(config.dataset_path),
        "environment": {
            key: os.environ.get(key)
            for key in (
                "SLURM_JOB_ID",
                "SLURM_ARRAY_JOB_ID",
                "SLURM_ARRAY_TASK_ID",
                "SLURM_JOB_NODELIST",
                "CUDA_VISIBLE_DEVICES",
            )
            if os.environ.get(key) is not None
        },
        "packages": {
            package: _package_version(package)
            for package in ("torch", "transformers", "accelerate", "vllm")
        },
        "gpu": _gpu_metadata(),
    }


def write_provenance_once(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        stable_keys = ("run_id", "model", "model_id", "revision", "dataset_sha256")
        if any(existing.get(key) != value.get(key) for key in stable_keys):
            raise ValueError(f"existing provenance at {path} belongs to a different run")
        return
    path.write_text(encoded, encoding="utf-8", newline="\n")


def _package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def _git_commit() -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def _gpu_metadata() -> list[dict[str, str]]:
    try:
        output = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=index,name,uuid,memory.total,driver_version",
                "--format=csv,noheader,nounits",
            ],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return []
    keys = ("index", "name", "uuid", "memory_total_mib", "driver_version")
    return [dict(zip(keys, (part.strip() for part in line.split(",")), strict=True)) for line in output.splitlines()]


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
