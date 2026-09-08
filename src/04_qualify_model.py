#!/usr/bin/env python3
"""Step 4: qualify one model on five representations."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from lib.requests import sudoku_request
from lib.selection import select_stratified
from lib.slurm import finish_submission, write_python_job
from lib.statistics import write_qualification_status
from lib.steps import execute_requests, load_enabled_model
from lib.sudoku.dataset import audit_records, read_records
from lib.sudoku.representations import ALPHABETS
from lib.workflow import model_directory, qualification_result

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
    result = qualification_result(config, model)
    if result is True:
        print(f"SKIP: {model.name} already passed qualification")
        return 0
    if result is False:
        raise SystemExit(f"{model.name} failed qualification; inspect its output and use a new run_id")

    if not arguments.execute:
        path = write_python_job(
            config,
            model,
            Path(__file__),
            "qualification",
            (model.name, "--config", str(arguments.config.resolve())),
        )
        return finish_submission(path, dry_run=arguments.dry_run, test_only=arguments.test_only)

    records = read_records(config.dataset_path)
    audit = audit_records(records)
    if not audit["valid"]:
        raise SystemExit("dataset audit failed: " + "; ".join(audit["errors"]))

    selected = select_stratified(
        records,
        5,
        seed=config.master_seed,
        namespace="qualification",
    )[:5]
    representation_names = (
        "arabic_digits",
        "greek_letters",
        "emoji",
        "nonce_labels",
        "devanagari_numerals",
    )
    requests = tuple(
        sudoku_request(
            "qualification",
            representation,
            model,
            record,
            ALPHABETS[representation],
        )
        for record, representation in zip(selected, representation_names, strict=True)
    )
    summary = execute_requests(config, model, "qualification", requests)
    status = write_qualification_status(model_directory(config, model))
    print(json.dumps({"summary": asdict(summary), "qualification": status}, sort_keys=True))
    if not status["passed"]:
        raise SystemExit(f"{model.name} did not solve all five qualification puzzles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
