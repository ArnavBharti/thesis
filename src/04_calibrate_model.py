#!/usr/bin/env python3
"""Step 4 calibration: test one fixed profile on held-out Arabic Sudoku puzzles."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from lib.calibration import PROFILES, apply_calibration_profile
from lib.config import load_config
from lib.protocol import freeze_json
from lib.requests import sudoku_request
from lib.results import iter_result_values
from lib.samples import build_sample_plan
from lib.selection import select_stratified
from lib.slurm import finish_submission, write_python_job
from lib.steps import execute_requests
from lib.sudoku.dataset import audit_records, read_records
from lib.sudoku.representations import ALPHABETS
from lib.workflow import model_directory

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "config" / "experiments.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", choices=sorted(PROFILES))
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--test-only", action="store_true")
    parser.add_argument("--execute", action="store_true", help=argparse.SUPPRESS)
    arguments = parser.parse_args()

    base_config = load_config(arguments.config)
    config, model = apply_calibration_profile(base_config, arguments.profile)
    existing = calibration_status(config, model)
    if existing is not None:
        print(json.dumps(existing, sort_keys=True))
        return 0 if existing["ready"] else 1

    if not arguments.execute:
        path = write_python_job(
            config,
            model,
            Path(__file__),
            "calibration",
            (arguments.profile, "--config", str(arguments.config.resolve())),
        )
        return finish_submission(path, dry_run=arguments.dry_run, test_only=arguments.test_only)

    records = read_records(config.dataset_path)
    audit = audit_records(records)
    if not audit["valid"]:
        raise SystemExit("dataset audit failed: " + "; ".join(audit["errors"]))

    plan = build_sample_plan(base_config, records)
    reserved = set(plan.pilot_ids) | set(plan.main_ids)
    calibration_pool = tuple(record for record in records if record.puzzle_id not in reserved)
    selected = select_stratified(
        calibration_pool,
        10,
        seed=config.master_seed,
        namespace="configuration-readiness-v1",
    )
    puzzles = tuple(record for record in selected if record.difficulty == "easy")[:5]
    puzzles += tuple(record for record in selected if record.difficulty == "hard")

    requests = tuple(
        sudoku_request(
            "calibration",
            "arabic_digits",
            model,
            record,
            ALPHABETS["arabic_digits"],
            metadata={"calibration_profile": arguments.profile},
        )
        for record in puzzles
    )
    summary = execute_requests(config, model, "calibration", requests)
    status = calibration_status(config, model)
    if status is None:
        raise RuntimeError("calibration finished without a complete result file")
    freeze_json(model_directory(config, model) / "calibration-status.json", status)
    print(json.dumps({"summary": asdict(summary), "calibration": status}, sort_keys=True))
    if not status["ready"]:
        raise SystemExit(f"{arguments.profile} did not pass calibration")
    return 0


def calibration_status(config, model):
    paths = tuple((model_directory(config, model) / "calibration").glob("shard-*.jsonl"))
    values = tuple(iter_result_values(paths))
    if len(values) != 15:
        return None
    easy = [value for value in values if value["request"]["metadata"]["difficulty"] == "easy"]
    hard = [value for value in values if value["request"]["metadata"]["difficulty"] == "hard"]
    easy_correct = sum(value["evaluation"]["outcome"] == "CORRECT" for value in easy)
    hard_correct = sum(value["evaluation"]["outcome"] == "CORRECT" for value in hard)
    operational_failures = sum(
        value["evaluation"]["outcome"] == "NOT_EVALUATED" for value in values
    )
    return {
        "requests": len(values),
        "easy_correct": easy_correct,
        "easy_total": len(easy),
        "hard_correct": hard_correct,
        "hard_total": len(hard),
        "operational_failures": operational_failures,
        "ready": easy_correct >= 4 and hard_correct >= 2 and operational_failures == 0,
    }


if __name__ == "__main__":
    raise SystemExit(main())
