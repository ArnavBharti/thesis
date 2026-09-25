#!/usr/bin/env python3
"""Step 3: rerun one timing puzzle under an isolated model configuration."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, replace
from pathlib import Path

from diagnose_timing import select_timing_puzzle
from lib.config import load_config
from lib.prompts import PromptOptions
from lib.requests import sudoku_request
from lib.results import iter_result_values
from lib.slurm import finish_submission, write_python_job
from lib.steps import execute_requests
from lib.sudoku.representations import ALPHABETS
from lib.workflow import model_directory


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model")
    parser.add_argument("difficulty", choices=("easy", "medium", "hard"))
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--test-only", action="store_true")
    parser.add_argument("--execute", action="store_true", help=argparse.SUPPRESS)
    arguments = parser.parse_args()

    base_config = load_config(arguments.config)
    model = base_config.model(arguments.model)
    config = replace(
        base_config,
        run_id=f"{base_config.run_id}-natural-timing-v3-{arguments.difficulty}",
        models=(model,),
    )
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
            (model.name, arguments.difficulty, "--config", str(arguments.config.resolve())),
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
