"""Single entry point for planning, probing, running, and analysing every experiment."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from sudoku.dataset import audit_records, read_records

from .analysis import analyze_run, write_qualification_status
from .backends import BackendError, TokenizerAdapter, build_backend, load_huggingface_tokenizer, probe_model
from .cases import DERIVED_EXPERIMENTS, INFERENCE_EXPERIMENTS, CaseFactory
from .config import ExperimentConfig, ModelConfig, load_config
from .executor import ExperimentExecutor
from .protocol import build_protocol_manifest, freeze_protocol
from .provenance import collect_provenance, write_provenance_once
from .records import shard_for
from .storage import ResultStore
from .token_registry import prompt_token_registry, representation_registry, unicode_registry

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "experiments.json"
ALL_EXPERIMENTS = (
    "qualification",
    "exp2",
    "exp3",
    "exp4",
    "exp5",
    "exp6",
    "exp7",
    "exp8",
    "exp9",
    "exp10",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the complete thesis experiment protocol.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--action", choices=("run", "plan", "probe", "analyze", "token-registry"), default="run")
    parser.add_argument("--model", action="append", help="model name; repeat to select multiple models")
    parser.add_argument("--experiments", default="all", help="comma-separated names or 'all'")
    parser.add_argument("--shard-index", type=int, default=0)
    parser.add_argument("--shard-count", type=int, default=1)
    parser.add_argument("--max-requests", type=int)
    parser.add_argument("--dry-run", action="store_true", help="enumerate requests without loading a model")
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    config = load_config(arguments.config)
    records = read_records(config.dataset_path)
    audit = audit_records(records)
    if not audit["valid"]:
        raise SystemExit("dataset audit failed: " + "; ".join(audit["errors"]))
    factory = CaseFactory(config, records)
    models = _selected_models(config, arguments.model)
    experiments = _selected_experiments(arguments.experiments)

    if arguments.action == "probe":
        return _probe(models)
    if arguments.action == "plan" or arguments.dry_run:
        return _plan(factory, models, experiments, arguments.shard_index, arguments.shard_count)
    if arguments.action == "analyze":
        for model in models:
            summary = analyze_run(_model_directory(config, model))
            print(json.dumps({"model": model.name, "record_count": summary["record_count"]}, sort_keys=True))
        return 0
    if arguments.action == "token-registry":
        for model in models:
            tokenizer = _load_optional_tokenizer(model)
            _write_token_registry(config, model, records, tokenizer)
        return 0

    if not 0 <= arguments.shard_index < arguments.shard_count:
        raise SystemExit("--shard-index must be in [0, --shard-count)")
    if "qualification" in experiments and arguments.shard_count != 1:
        raise SystemExit("qualification must run unsharded before other Slurm array jobs")

    for model in models:
        available, reason = probe_model(model)
        if not available:
            raise SystemExit(f"model {model.name} is unavailable: {reason}")
        backend = build_backend(model, config.inference, config.retry)
        try:
            try:
                tokenizer: TokenizerAdapter | None = backend.tokenizer()
            except BackendError:
                tokenizer = None
            model_directory = _model_directory(config, model)
            write_provenance_once(
                model_directory / "provenance.json",
                collect_provenance(config, model),
            )
            freeze_protocol(
                model_directory / "protocol-manifest.json",
                build_protocol_manifest(config, model, factory, tokenizer=tokenizer),
            )
            for experiment in experiments:
                if experiment == "exp3":
                    _write_token_registry(config, model, records, tokenizer)
                    continue
                if experiment == "exp5":
                    if arguments.shard_count == 1:
                        analyze_run(model_directory)
                    continue
                if experiment not in INFERENCE_EXPERIMENTS:
                    continue
                if experiment == "exp7" and tokenizer is None:
                    if arguments.shard_index == 0:
                        _write_not_run_status(
                            model_directory / "exp7" / "status.json",
                            "NOT_RUN_NO_EXACT_TOKENIZER_ACCESS",
                        )
                    print(json.dumps({"model": model.name, "experiment": experiment, "status": "skipped_no_exact_tokenizer"}, sort_keys=True))
                    continue
                if experiment != "qualification":
                    _require_qualification(model_directory)
                path = model_directory / experiment / (
                    f"shard-{arguments.shard_index:03d}-of-{arguments.shard_count:03d}.jsonl"
                )
                store = ResultStore(path)
                executor = ExperimentExecutor(
                    backend,
                    store,
                    config.retry,
                    shard_index=arguments.shard_index,
                    shard_count=arguments.shard_count,
                )
                try:
                    requests = factory.requests(experiment, model, tokenizer=tokenizer)
                except ValueError as error:
                    if experiment != "exp7":
                        raise
                    if arguments.shard_index == 0:
                        _write_not_run_status(
                            model_directory / "exp7" / "status.json",
                            "NOT_RUN_TOKEN_SET_CONSTRUCTION_FAILED: " + str(error),
                        )
                    print(json.dumps({"model": model.name, "experiment": experiment, "status": "skipped_token_set_construction", "detail": str(error)}, sort_keys=True))
                    continue
                summary = executor.run(requests, maximum_requests=arguments.max_requests)
                print(json.dumps({"model": model.name, "experiment": experiment, **asdict(summary)}, sort_keys=True))
                if experiment == "qualification":
                    qualification = write_qualification_status(model_directory)
                    print(json.dumps({"model": model.name, "qualification": qualification}, sort_keys=True))
                    if not qualification["passed"]:
                        raise SystemExit(f"model {model.name} failed qualification; protocol stopped")
            if arguments.shard_count == 1 and any(name in experiments for name in ("exp4", "exp5", "exp10")):
                analyze_run(model_directory)
        finally:
            backend.close()
    return 0


def _selected_models(config: ExperimentConfig, names: list[str] | None) -> tuple[ModelConfig, ...]:
    if names:
        try:
            return tuple(config.model(name) for name in names)
        except KeyError as error:
            raise SystemExit(str(error)) from error
    if not config.enabled_models:
        raise SystemExit("configuration has no enabled models")
    return config.enabled_models


def _selected_experiments(value: str) -> tuple[str, ...]:
    if value == "all":
        return ALL_EXPERIMENTS
    names = tuple(name.strip() for name in value.split(",") if name.strip())
    invalid = set(names) - set(ALL_EXPERIMENTS)
    if invalid:
        raise SystemExit("unknown experiments: " + ", ".join(sorted(invalid)))
    return names


def _probe(models: Iterable[ModelConfig]) -> int:
    failed = False
    for model in models:
        available, reason = probe_model(model)
        print(json.dumps({"model": model.name, "available": available, "detail": reason}, sort_keys=True))
        failed |= not available
    return 1 if failed else 0


def _load_optional_tokenizer(model: ModelConfig) -> TokenizerAdapter | None:
    if model.backend == "openai_compatible" and not model.tokenizer_id:
        return None
    try:
        return load_huggingface_tokenizer(model)
    except BackendError:
        return None


def _plan(
    factory: CaseFactory,
    models: Iterable[ModelConfig],
    experiments: Iterable[str],
    shard_index: int,
    shard_count: int,
) -> int:
    for model in models:
        for experiment in experiments:
            if experiment in DERIVED_EXPERIMENTS:
                print(json.dumps({"model": model.name, "experiment": experiment, "kind": "derived"}, sort_keys=True))
                continue
            if experiment == "exp7":
                total = factory.config.mechanism_per_tier * 3 * 3
                print(json.dumps({"model": model.name, "experiment": experiment, "planned_requests": total, "note": "exact count requires tokenizer"}, sort_keys=True))
                continue
            requests = tuple(factory.requests(experiment, model))
            in_shard = sum(shard_for(request.request_id, shard_count) == shard_index for request in requests)
            print(json.dumps({"model": model.name, "experiment": experiment, "planned_requests": len(requests), "requests_in_shard": in_shard}, sort_keys=True))
    return 0


def _write_token_registry(
    config: ExperimentConfig,
    model: ModelConfig,
    records: tuple,
    tokenizer: TokenizerAdapter | None,
) -> None:
    directory = _model_directory(config, model) / "exp3"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "representation-registry.jsonl"
    rows = [
        {"kind": "symbol", **row}
        for row in (representation_registry(tokenizer) if tokenizer else unicode_registry())
    ]
    if tokenizer:
        rows.extend(prompt_token_registry(records, tokenizer))
    text = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    if path.exists() and path.read_text(encoding="utf-8") != text:
        raise ValueError(f"token registry at {path} differs from the frozen version")
    path.write_text(text, encoding="utf-8", newline="\n")
    print(json.dumps({"model": model.name, "token_registry_rows": len(rows), "path": str(path)}, sort_keys=True))


def _write_not_run_status(path: Path, reason: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    value = {"status": "NOT_RUN", "reason": reason}
    encoded = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") != encoded:
        raise ValueError(f"existing status at {path} differs")
    path.write_text(encoded, encoding="utf-8", newline="\n")


def _require_qualification(model_directory: Path) -> None:
    path = model_directory / "qualification-status.json"
    try:
        status = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SystemExit("qualification has not completed successfully; run qualification first") from error
    if not status.get("passed"):
        raise SystemExit("qualification did not pass; refusing to run the main protocol")


def _model_directory(config: ExperimentConfig, model: ModelConfig) -> Path:
    return config.output_directory / config.run_id / model.name
