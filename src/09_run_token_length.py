#!/usr/bin/env python3
"""Step 9: test one-, two-, and three-token neutral symbol alphabets."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from lib.models import load_huggingface_tokenizer
from lib.requests import sudoku_request
from lib.samples import load_sample_plan
from lib.slurm import finish_submission, write_python_job
from lib.steps import execute_requests, load_enabled_model, write_status
from lib.sudoku.dataset import read_records
from lib.sudoku.schema import grid_from_compact
from lib.token_registry import construct_token_alphabets
from lib.workflow import experiment_complete, experiment_part_complete, model_directory

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
    if model.backend == "openai_compatible" and not model.tokenizer_id:
        status_path = model_directory(config, model) / "exp7" / "status.json"
        write_status(status_path, {"status": "NOT_RUN", "reason": "NO_EXACT_TOKENIZER_ACCESS"})
        print(f"SKIP: {model.name} does not expose exact token IDs")
        return 0
    if not experiment_complete(config, model, "exp4"):
        raise SystemExit(f"finish all Step 7 parts for {model.name} first")
    if experiment_part_complete(config, model, "exp7", 1):
        print(f"SKIP: token-length experiment is complete for {model.name}")
        return 0
    if not arguments.execute:
        path = write_python_job(
            config,
            model,
            Path(__file__),
            "exp7-token-length",
            (model.name, "--config", str(arguments.config.resolve())),
        )
        return finish_submission(path, dry_run=arguments.dry_run, test_only=arguments.test_only)

    records = read_records(config.dataset_path)
    puzzles = load_sample_plan(config).records("mechanism", records)
    tokenizer = load_huggingface_tokenizer(model)
    token_plan = construct_token_alphabets(tokenizer, seed=config.master_seed)
    if token_plan.missing_token_lengths:
        missing = ", ".join(map(str, token_plan.missing_token_lengths))
        raise SystemExit(f"could not construct nine neutral labels for token lengths: {missing}")

    requests = []
    for record in puzzles:
        puzzle = grid_from_compact(record.puzzle)
        for alphabet in token_plan.alphabets:
            token_length = len(tokenizer.encode(alphabet.symbols[0]))
            visible_symbols = [alphabet.symbol_for(value) for value in puzzle.cells if value]
            clue_tokens = sum(len(tokenizer.encode(symbol)) for symbol in visible_symbols)
            requests.append(
                sudoku_request(
                    "exp7",
                    f"neutral_{token_length}_tokens",
                    model,
                    record,
                    alphabet,
                    metadata={
                        "token_length": token_length,
                        "mean_clue_tokens": clue_tokens / len(visible_symbols),
                        "mean_symbol_utf8_bytes": sum(len(symbol.encode("utf-8")) for symbol in alphabet.symbols) / 9,
                        "mean_symbol_code_points": sum(len(symbol) for symbol in alphabet.symbols) / 9,
                    },
                )
            )

    summary = execute_requests(
        config,
        model,
        "exp7",
        requests,
        manifest_notes={"tokenizer": tokenizer.identity, "token_lengths": [1, 2, 3]},
    )
    print(json.dumps(asdict(summary), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
