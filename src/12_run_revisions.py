#!/usr/bin/env python3
"""Step 12: compare self-revision with automatic-checker-guided revision."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from lib.requests import sudoku_request
from lib.results import index_results
from lib.samples import load_sample_plan
from lib.slurm import finish_submission, write_python_job
from lib.steps import execute_requests, load_enabled_model
from lib.sudoku.dataset import read_records
from lib.sudoku.representations import ALPHABETS
from lib.workflow import experiment_complete, experiment_part_complete

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
    if not experiment_complete(config, model, "exp4"):
        raise SystemExit(f"finish all Step 7 parts for {model.name} first")
    if experiment_part_complete(config, model, "exp10", 1):
        print(f"SKIP: revision experiment is complete for {model.name}")
        return 0
    if not arguments.execute:
        path = write_python_job(
            config,
            model,
            Path(__file__),
            "exp10-revisions",
            (model.name, "--config", str(arguments.config.resolve())),
        )
        return finish_submission(path, dry_run=arguments.dry_run, test_only=arguments.test_only)

    records = read_records(config.dataset_path)
    puzzles = load_sample_plan(config).records("ablation", records)
    representations = ("arabic_digits", "greek_letters", "emoji")
    revision_conditions = (
        "one_pass",
        "one_self_revision",
        "two_self_revisions",
        "checker_guided_revision",
    )
    main_results = index_results(
        (config.output_directory / config.run_id / model.name / "exp4").glob("shard-*.jsonl")
    )

    requests = []
    initial_results = {}
    for record in puzzles:
        for representation in representations:
            try:
                source = main_results[(record.puzzle_id, representation)]
            except KeyError as error:
                raise SystemExit(f"missing main result for {record.puzzle_id} {representation}") from error
            for revision_condition in revision_conditions:
                request = sudoku_request(
                    "exp10",
                    f"{representation}:{revision_condition}",
                    model,
                    record,
                    ALPHABETS[representation],
                    metadata={
                        "revision_condition": revision_condition,
                        "reused_initial_request_id": source["request"]["request_id"],
                    },
                )
                requests.append(request)
                initial_results[request.request_id] = source

    summary = execute_requests(
        config,
        model,
        "exp10",
        requests,
        initial_results=initial_results,
        manifest_notes={
            "puzzles": len(puzzles),
            "representations": list(representations),
            "shared_initial_answer": True,
            "new_calls_per_puzzle_representation": "3 or 4",
            "exploratory": True,
        },
    )
    print(json.dumps(asdict(summary), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
