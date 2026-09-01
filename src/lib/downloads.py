"""Reusable Hugging Face snapshot download and verification functions."""

from __future__ import annotations

from pathlib import Path

from .config import ModelConfig


def local_models(models: tuple[ModelConfig, ...]) -> tuple[ModelConfig, ...]:
    return tuple(
        model
        for model in models
        if model.enabled and model.backend not in {"openai_compatible", "static"}
    )


def ensure_snapshot(
    model: ModelConfig,
    cache_directory: Path | None,
    *,
    verify_only: bool,
) -> Path:
    direct_path = Path(model.resolved_model_id)
    if direct_path.exists():
        return direct_path.resolve()
    if not model.revision:
        raise SystemExit(f"local model {model.name} does not pin an immutable revision")
    try:
        from huggingface_hub import snapshot_download
    except ImportError as error:
        raise SystemExit("huggingface-hub is required; install the project with .[local]") from error
    try:
        return Path(
            snapshot_download(
                repo_id=model.resolved_model_id,
                revision=model.revision,
                cache_dir=str(cache_directory) if cache_directory else None,
                local_files_only=verify_only,
            )
        )
    except Exception as error:
        action = "verify" if verify_only else "download"
        raise SystemExit(f"could not {action} {model.name}: {error}") from error
