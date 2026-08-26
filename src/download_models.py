#!/usr/bin/env python3
"""Idempotently download or verify every locally executed model snapshot."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Iterable

from experiments.config import ModelConfig, load_config

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "config" / "experiments.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--model", action="append", help="local model name; repeat to select several")
    parser.add_argument("--cache-dir", type=Path, help="Hugging Face cache (prefer Sharanga scratch storage)")
    parser.add_argument("--verify-only", action="store_true", help="fail instead of downloading missing snapshots")
    parser.add_argument("--dry-run", action="store_true", help="show pinned downloads without network or disk writes")
    return parser


def local_models(models: Iterable[ModelConfig]) -> tuple[ModelConfig, ...]:
    """Return enabled models whose weights must exist on the local filesystem."""

    return tuple(
        model
        for model in models
        if model.enabled and model.backend not in {"openai_compatible", "static"}
    )


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    config = load_config(arguments.config)
    selected = local_models(config.models)
    if arguments.model:
        requested = set(arguments.model)
        known = {model.name for model in selected}
        unknown = requested - known
        if unknown:
            raise SystemExit("unknown enabled local models: " + ", ".join(sorted(unknown)))
        selected = tuple(model for model in selected if model.name in requested)
    if not selected:
        raise SystemExit("no enabled local models selected")

    cache_dir = arguments.cache_dir.resolve() if arguments.cache_dir else None
    for model in selected:
        plan = _plan_row(model, cache_dir)
        if arguments.dry_run:
            print(json.dumps({**plan, "status": "planned"}, sort_keys=True))
            continue
        snapshot = _snapshot(model, cache_dir, local_files_only=arguments.verify_only)
        print(
            json.dumps(
                {**plan, "status": "verified" if arguments.verify_only else "ready", "snapshot_path": str(snapshot)},
                sort_keys=True,
            )
        )
    return 0


def _plan_row(model: ModelConfig, cache_dir: Path | None) -> dict[str, object]:
    path = Path(model.resolved_model_id)
    if not path.exists() and not model.revision:
        raise SystemExit(f"local model {model.name} must pin an immutable Hugging Face revision")
    return {
        "model": model.name,
        "repo_id": model.resolved_model_id,
        "revision": model.revision,
        "cache_dir": str(cache_dir) if cache_dir else os.environ.get("HF_HOME", "Hugging Face default"),
    }


def _snapshot(model: ModelConfig, cache_dir: Path | None, *, local_files_only: bool) -> Path:
    direct_path = Path(model.resolved_model_id)
    if direct_path.exists():
        return direct_path.resolve()
    try:
        from huggingface_hub import snapshot_download
    except ImportError as error:
        raise SystemExit("huggingface-hub is required: python -m pip install huggingface-hub") from error
    try:
        return Path(
            snapshot_download(
                repo_id=model.resolved_model_id,
                revision=model.revision,
                cache_dir=str(cache_dir) if cache_dir else None,
                local_files_only=local_files_only,
            )
        )
    except Exception as error:
        action = "verify" if local_files_only else "download"
        raise SystemExit(f"could not {action} {model.name}: {error}") from error


if __name__ == "__main__":
    raise SystemExit(main())
