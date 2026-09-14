#!/usr/bin/env python3
"""Time one natural Qwen reasoning run on one held-out Sudoku puzzle."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, replace
from pathlib import Path

from lib.calibration import apply_calibration_profile
from lib.config import load_config
from lib.prompts import PromptOptions
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
DEFAULT_CONFIG = ROOT / "config" / "stronger-model-diagnostic.json"


def select_timing_puzzle(config, difficulty):
    records = read_records(config.dataset_path)
    audit = audit_records(records)
    if not audit["valid"]:
        raise RuntimeError("dataset audit failed: " + "; ".join(audit["errors"]))
    plan = build_sample_plan(config, records)
    reserved = set(plan.pilot_ids) | set(plan.main_ids)
    pool = tuple(record for record in records if record.puzzle_id not in reserved)
    selected = select_stratified(
        pool,
        1,
        seed=config.master_seed,
        namespace="qwen-natural-timing-v1",
    )
    return next(record for record in selected if record.difficulty == difficulty)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("difficulty", choices=("easy", "medium", "hard"))
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--test-only", action="store_true")
    parser.add_argument("--execute", action="store_true", help=argparse.SUPPRESS)
    arguments = parser.parse_args()

    base_config = load_config(arguments.config)
    config, model = apply_calibration_profile(base_config, "qwen-timed-reasoning")
    config = replace(config, run_id=f"qwen-natural-timing-v2-{arguments.difficulty}")
    puzzle = select_timing_puzzle(base_config, arguments.difficulty)
    request = sudoku_request(
        "timing-diagnostic",
        "arabic_digits",
        model,
        puzzle,
        ALPHABETS["arabic_digits"],
        options=PromptOptions(verify_before_answer=True),
        metadata={"diagnostic": "natural_reasoning_time"},
    )

    if not arguments.execute:
        path = write_python_job(
            config,
            model,
            Path(__file__),
            f"timing-{arguments.difficulty}",
            (arguments.difficulty, "--config", str(arguments.config.resolve())),
        )
        return finish_submission(path, dry_run=arguments.dry_run, test_only=arguments.test_only)

    summary = execute_requests(config, model, "timing-diagnostic", (request,))
    path = model_directory(config, model) / "timing-diagnostic" / "shard-000-of-001.jsonl"
    values = tuple(iter_result_values((path,)))
    if len(values) != 1:
        raise RuntimeError("timing diagnostic did not produce exactly one result")
    print(json.dumps({"summary": asdict(summary), "result": values[0]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
