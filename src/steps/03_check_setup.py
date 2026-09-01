#!/usr/bin/env python3
"""Step 3: check the dataset, local models, and API key."""

from __future__ import annotations

import argparse

from _shared import add_config_argument
from experiments.backends import probe_model
from experiments.config import load_config
from sudoku.dataset import audit_records, read_records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_config_argument(parser)
    parser.add_argument("--model", action="append", help="check only this model; repeat if needed")
    arguments = parser.parse_args()
    config = load_config(arguments.config)

    audit = audit_records(read_records(config.dataset_path))
    if audit["valid"]:
        print(f"Dataset: READY ({audit['record_count']} puzzles)")
    else:
        print("Dataset: FAILED")
        for error in audit["errors"]:
            print(f"  {error}")
        return 1

    models = config.enabled_models
    if arguments.model:
        requested = set(arguments.model)
        models = tuple(model for model in models if model.name in requested)
        missing = requested - {model.name for model in models}
        if missing:
            raise SystemExit("Unknown or disabled models: " + ", ".join(sorted(missing)))

    failed = False
    for model in models:
        ready, detail = probe_model(model)
        print(f"{model.name}: {'READY' if ready else 'MISSING'}")
        print(f"  {detail}")
        failed |= not ready
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
