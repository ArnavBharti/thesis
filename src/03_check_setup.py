#!/usr/bin/env python3
"""Step 3: check the dataset, model files, and OpenRouter key."""

from __future__ import annotations

import argparse
import importlib
import sqlite3
import sys
from pathlib import Path

from lib.config import load_config
from lib.models import probe_model
from lib.sudoku.dataset import audit_records, read_records

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "config" / "experiments.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--model", action="append", help="check only this model; repeat if needed")
    arguments = parser.parse_args()

    config = load_config(arguments.config)
    audit = audit_records(read_records(config.dataset_path))
    print(f"Dataset: {'READY' if audit['valid'] else 'FAILED'} ({audit['record_count']} puzzles)")
    if not audit["valid"]:
        for error in audit["errors"]:
            print(f"  {error}")
        return 1

    models = config.enabled_models
    if arguments.model:
        requested = set(arguments.model)
        unknown = requested - {model.name for model in models}
        if unknown:
            raise SystemExit("unknown or disabled models: " + ", ".join(sorted(unknown)))
        models = tuple(model for model in models if model.name in requested)

    failed = False
    print(
        f"Python runtime: READY ({sys.version.split()[0]}, SQLite {sqlite3.sqlite_version})"
    )
    if any(model.backend == "vllm" for model in models):
        try:
            getattr(importlib.import_module("vllm"), "LLM")
        except Exception as error:
            print("vLLM import: FAILED")
            print(f"  {type(error).__name__}: {error}")
            failed = True
        else:
            print("vLLM import: READY")
    for model in models:
        ready, detail = probe_model(model)
        print(f"{model.name}: {'READY' if ready else 'MISSING'}")
        print(f"  {detail}")
        failed |= not ready
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
