#!/usr/bin/env python3
"""Step 7: run one of six main-benchmark parts for one model."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from lib.requests import sudoku_request
from lib.samples import load_sample_plan
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
    parser.add_argument("--part", type=int, required=True, help="part number from 1 through 6")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--test-only", action="store_true")
    parser.add_argument("--execute", action="store_true", help=argparse.SUPPRESS)
    arguments = parser.parse_args()

    config, model = load_enabled_model(arguments.config, arguments.model)
    parts = config.shard_count("exp4")
    if not 1 <= arguments.part <= parts:
        raise SystemExit(f"--part must be between 1 and {parts}")
    if not qualification_complete(config, model):
        raise SystemExit(f"{model.name} has not passed Step 4")
    load_sample_plan(config)
    if experiment_part_complete(config, model, "exp4", arguments.part):
        print(f"SKIP: main benchmark part {arguments.part}/{parts} is complete for {model.name}")
        return 0

    if not arguments.execute:
        path = write_python_job(
            config,
            model,
            Path(__file__),
            f"exp4-part-{arguments.part:03d}-of-{parts:03d}",
            (
                model.name,
                "--part",
                str(arguments.part),
                "--config",
                str(arguments.config.resolve()),
            ),
        )
        return finish_submission(path, dry_run=arguments.dry_run, test_only=arguments.test_only)

    records = read_records(config.dataset_path)
    main_sample = load_sample_plan(config).records("main", records)
    representation_names = tuple(ALPHABETS)
    requests = tuple(
        sudoku_request("exp4", representation, model, record, ALPHABETS[representation])
        for record in main_sample
        for representation in representation_names
    )
    summary = execute_requests(
        config,
        model,
        "exp4",
        requests,
        part=arguments.part,
        parts=parts,
        manifest_notes={"puzzles": len(main_sample), "representations": list(representation_names)},
    )
    print(json.dumps(asdict(summary), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
