#!/usr/bin/env python3
"""Step 13: write token diagnostics and final analysis for one finished model."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib.models import load_huggingface_tokenizer
from lib.protocol import verify_global_protocol
from lib.samples import load_sample_plan
from lib.slurm import cpu_resources, finish_submission, write_python_job
from lib.statistics import analyze_run
from lib.steps import load_enabled_model
from lib.sudoku.dataset import read_records
from lib.token_registry import prompt_token_registry, representation_registry, unicode_registry
from lib.workflow import experiment_complete, finalization_complete, model_directory

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "config" / "experiments.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--test-only", action="store_true")
    parser.add_argument("--execute", action="store_true", help=argparse.SUPPRESS)
    arguments = parser.parse_args()

    config, model = load_enabled_model(arguments.config, arguments.model)
    verify_global_protocol(config, load_sample_plan(config))
    required = ("exp2", "exp4", "exp6", "exp8", "exp9", "exp10")
    if model.backend != "openai_compatible" or model.tokenizer_id:
        required += ("exp7",)
    missing = [name for name in required if not experiment_complete(config, model, name)]
    if missing:
        raise SystemExit("unfinished experiments: " + ", ".join(missing))
    if finalization_complete(config, model):
        print(f"SKIP: final analysis already exists for {model.name}")
        return 0

    if not arguments.execute:
        path = write_python_job(
            config,
            model,
            Path(__file__),
            "final-analysis",
            (model.name, "--config", str(arguments.config.resolve())),
            resources=cpu_resources(),
        )
        return finish_submission(path, dry_run=arguments.dry_run, test_only=arguments.test_only)

    records = read_records(config.dataset_path)
    tokenizer = None
    if model.backend != "openai_compatible" or model.tokenizer_id:
        tokenizer = load_huggingface_tokenizer(model)

    rows = [
        {"kind": "symbol", **row}
        for row in (representation_registry(tokenizer) if tokenizer else unicode_registry())
    ]
    if tokenizer:
        rows.extend(prompt_token_registry(records, tokenizer))
    registry_path = model_directory(config, model) / "exp3" / "representation-registry.jsonl"
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_text = "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows
    )
    if registry_path.exists() and registry_path.read_text(encoding="utf-8") != registry_text:
        raise ValueError(f"token registry differs from its existing version: {registry_path}")
    registry_path.write_text(registry_text, encoding="utf-8", newline="\n")

    summary = analyze_run(model_directory(config, model))
    print(f"Token registry rows: {len(rows)}")
    print(f"Analyzed result records: {summary['record_count']}")
    print(f"DONE: {model.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
