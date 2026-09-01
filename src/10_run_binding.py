#!/usr/bin/env python3
"""Step 10: test arbitrary mappings, familiar labels, and semantic conflict."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from lib.requests import sudoku_request
from lib.results import index_results
from lib.samples import load_sample_plan
from lib.selection import deterministic_permutation
from lib.slurm import finish_submission, write_python_job
from lib.steps import execute_requests, load_enabled_model
from lib.sudoku.dataset import read_records
from lib.sudoku.representations import ALPHABETS, SymbolAlphabet
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
    if experiment_part_complete(config, model, "exp8", 1):
        print(f"SKIP: binding experiment is complete for {model.name}")
        return 0
    if not arguments.execute:
        path = write_python_job(
            config,
            model,
            Path(__file__),
            "exp8-binding",
            (model.name, "--config", str(arguments.config.resolve())),
        )
        return finish_submission(path, dry_run=arguments.dry_run, test_only=arguments.test_only)

    records = read_records(config.dataset_path)
    puzzles = load_sample_plan(config).records("mechanism", records)
    uppercase = ALPHABETS["uppercase_latin"]
    conditions: list[tuple[str, SymbolAlphabet, str | None]] = [
        ("uppercase_standard", uppercase, "uppercase_latin")
    ]
    for index in range(5):
        symbols = deterministic_permutation(
            uppercase.symbols,
            seed=config.master_seed,
            namespace=f"uppercase-random-{index}",
        )
        name = f"uppercase_random_{index + 1}"
        conditions.append((name, SymbolAlphabet(name, symbols), None))

    digits = ALPHABETS["arabic_digits"]
    permuted_digits = deterministic_permutation(
        digits.symbols,
        seed=config.master_seed,
        namespace="permuted-digits",
    )
    number_words = SymbolAlphabet(
        "number_words",
        ("ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"),
    )
    conflicting_words = SymbolAlphabet(
        "conflicting_number_words",
        deterministic_permutation(
            number_words.symbols,
            seed=config.master_seed,
            namespace="conflicting-number-words",
        ),
    )
    conditions.extend(
        (
            ("digits_ordinary", digits, "arabic_digits"),
            ("digits_permuted", SymbolAlphabet("permuted_digits", permuted_digits), None),
            ("number_words_ordinary", number_words, None),
            ("number_words_conflicting", conflicting_words, None),
            ("nonce_neutral", ALPHABETS["nonce_labels"], "nonce_labels"),
        )
    )

    all_requests = []
    inference_requests = []
    reused_conditions = []
    for record in puzzles:
        for condition, alphabet, main_condition in conditions:
            request = sudoku_request(
                "exp8",
                condition,
                model,
                record,
                alphabet,
                metadata={"reused_from_step": "exp4"} if main_condition else None,
            )
            all_requests.append(request)
            if main_condition:
                reused_conditions.append((request, main_condition))
            else:
                inference_requests.append(request)

    main_results = index_results(
        (config.output_directory / config.run_id / model.name / "exp4").glob("shard-*.jsonl")
    )
    reused_results = {}
    for request, source_condition in reused_conditions:
        try:
            reused_results[request.request_id] = main_results[(request.puzzle_id, source_condition)]
        except KeyError as error:
            raise SystemExit(f"missing main result for {request.puzzle_id} {source_condition}") from error

    summary = execute_requests(
        config,
        model,
        "exp8",
        all_requests,
        inference_requests=inference_requests,
        reused_results=reused_results,
        manifest_notes={
            "conditions": len(conditions),
            "new_calls_per_puzzle": 8,
            "reused_conditions": ["uppercase_standard", "digits_ordinary", "nonce_neutral"],
        },
    )
    print(json.dumps(asdict(summary), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
