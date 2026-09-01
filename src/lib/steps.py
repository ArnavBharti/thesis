"""Shared mechanics used by the readable numbered execution scripts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from .config import ExperimentConfig, ModelConfig, load_config
from .execution import ExecutionSummary, ExperimentExecutor
from .models import build_backend, probe_model
from .protocol import freeze_step_requests
from .provenance import collect_provenance, write_provenance_once
from .records import ExperimentRequest, shard_for
from .results import ResultStore, store_reused_result
from .workflow import model_directory, write_completion_marker


def load_enabled_model(config_path: Path, model_name: str) -> tuple[ExperimentConfig, ModelConfig]:
    config = load_config(config_path)
    try:
        model = config.model(model_name)
    except KeyError as error:
        choices = ", ".join(item.name for item in config.enabled_models)
        raise SystemExit(f"unknown model {model_name!r}; choose one of: {choices}") from error
    if not model.enabled:
        raise SystemExit(f"model {model_name!r} is disabled")
    return config, model


def execute_requests(
    config: ExperimentConfig,
    model: ModelConfig,
    step_name: str,
    all_requests: Iterable[ExperimentRequest],
    *,
    inference_requests: Iterable[ExperimentRequest] | None = None,
    reused_results: Mapping[str, dict[str, Any]] | None = None,
    initial_results: Mapping[str, dict[str, Any]] | None = None,
    part: int = 1,
    parts: int = 1,
    manifest_notes: dict[str, object] | None = None,
) -> ExecutionSummary:
    """Freeze, resume, execute, and mark one experiment part complete."""

    if not 1 <= part <= parts:
        raise ValueError(f"part must be between 1 and {parts}")
    all_requests = tuple(all_requests)
    inference_requests = tuple(inference_requests if inference_requests is not None else all_requests)
    freeze_step_requests(config, model, step_name, all_requests, notes=manifest_notes)

    shard_index = part - 1
    path = model_directory(config, model) / step_name / f"shard-{shard_index:03d}-of-{parts:03d}.jsonl"
    store = ResultStore(path)
    eligible = tuple(
        request
        for request in all_requests
        if shard_for(request.request_id, parts) == shard_index
    )

    reused = reused_results or {}
    for request in eligible:
        source = reused.get(request.request_id)
        if source is not None:
            store_reused_result(store, request, source)

    inference_ids = {request.request_id for request in inference_requests}
    missing_inference = tuple(
        request
        for request in eligible
        if request.request_id in inference_ids and not store.contains(request.request_id)
    )

    executed = correct = incorrect = not_evaluated = 0
    completed_before = len(eligible) - len(missing_inference)
    if missing_inference:
        available, reason = probe_model(model)
        if not available:
            raise SystemExit(f"model {model.name} is unavailable: {reason}")
        backend = build_backend(model, config.inference, config.retry)
        try:
            directory = model_directory(config, model)
            write_provenance_once(
                directory / "provenance.json",
                collect_provenance(config, model),
            )
            executor = ExperimentExecutor(
                backend,
                store,
                config.retry,
                shard_index=0,
                shard_count=1,
            )
            summary = executor.run(
                missing_inference,
                initial_results=initial_results,
            )
            executed = summary.executed
            correct = summary.correct
            incorrect = summary.incorrect
            not_evaluated = summary.not_evaluated
        finally:
            backend.close()

    missing = [request.request_id for request in eligible if not store.contains(request.request_id)]
    if missing:
        raise ValueError(
            f"{len(missing)} requests have neither inference nor a reusable source in {step_name}"
        )
    write_completion_marker(
        config,
        model,
        step_name,
        shard_index,
        parts,
        len(eligible),
    )
    return ExecutionSummary(
        eligible=len(eligible),
        completed_before_run=completed_before,
        executed=executed,
        correct=correct,
        incorrect=incorrect,
        not_evaluated=not_evaluated,
    )


def write_status(path: Path, value: dict[str, object]) -> None:
    text = json.dumps(value, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") != text:
        raise ValueError(f"status differs from the existing file: {path}")
    temporary = path.with_suffix(".tmp")
    temporary.write_text(text, encoding="utf-8", newline="\n")
    temporary.replace(path)
