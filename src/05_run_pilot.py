#!/usr/bin/env python3
"""Step 5: run the 60-puzzle pilot for one qualified model."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from lib.requests import sudoku_request
from lib.samples import build_sample_plan
from lib.slurm import finish_submission, write_python_job
from lib.steps import execute_requests, load_enabled_model
from lib.sudoku.dataset import read_records
from lib.sudoku.representations import ALPHABETS
from lib.workflow import experiment_part_complete, qualification_complete

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
    if not qualification_complete(config, model):
        raise SystemExit(f"{model.name} has not passed Step 4")
    if experiment_part_complete(config, model, "exp2", 1):
        print(f"SKIP: pilot already complete for {model.name}")
        return 0

    if not arguments.execute:
        path = write_python_job(
            config,
            model,
            Path(__file__),
            "exp2-pilot",
            (model.name, "--config", str(arguments.config.resolve())),
        )
        return finish_submission(path, dry_run=arguments.dry_run, test_only=arguments.test_only)

    records = read_records(config.dataset_path)
    pilot = build_sample_plan(config, records).records("pilot", records)
    representations = (
        "arabic_digits",
        "uppercase_latin",
        "greek_letters",
        "emoji",
    )
    requests = tuple(
        sudoku_request("exp2", representation, model, record, ALPHABETS[representation])
        for record in pilot
        for representation in representations
    )
    summary = execute_requests(config, model, "exp2", requests)
    print(json.dumps(asdict(summary), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
