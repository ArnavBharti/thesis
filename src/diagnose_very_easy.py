#!/usr/bin/env python3
"""Run one fixed, unique 57-clue Sudoku diagnostic on one local model."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, replace
from pathlib import Path

from lib.calibration import apply_calibration_profile
from lib.config import load_config
from lib.prompts import PromptOptions, solve_prompt
from lib.records import ExperimentRequest, Message
from lib.results import iter_result_values
from lib.slurm import finish_submission, write_python_job
from lib.steps import execute_requests
from lib.sudoku.grid import preserves_clues
from lib.sudoku.representations import ALPHABETS
from lib.sudoku.schema import grid_from_compact
from lib.sudoku.solver import count_solutions
from lib.workflow import model_directory

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "config" / "experiments.json"
PUZZLE = "8.3..142...5932.862618473957526948...481.36.2136258.49..4.859.33174...68.8.316.7."
SOLUTION = "893561427475932186261847395752694831948173652136258749624785913317429568589316274"
PROFILE_BY_MODEL = {
    "nemotron-local": "nemotron-verified-constrained",
    "mistral-small-4-local": "mistral-verified-constrained",
}


def diagnostic_request(model) -> ExperimentRequest:
    puzzle = grid_from_compact(PUZZLE)
    solution = grid_from_compact(SOLUTION)
    if puzzle.clue_count != 57 or count_solutions(puzzle, limit=2) != 1:
        raise RuntimeError("very-easy diagnostic must have 57 clues and one solution")
    if not preserves_clues(puzzle, solution):
        raise RuntimeError("very-easy diagnostic solution changes a clue")

    alphabet = ALPHABETS["arabic_digits"]
    messages: list[Message] = []
    system_prompt = model.extra.get("system_prompt")
    if system_prompt is not None:
        messages.append(Message("system", system_prompt))
    messages.append(
        Message(
            "user",
            solve_prompt(
                puzzle,
                alphabet,
                options=PromptOptions(verify_before_answer=True),
            ),
        )
    )
    return ExperimentRequest(
        experiment="very-easy-diagnostic",
        condition="arabic_digits",
        model=model.name,
        messages=tuple(messages),
        puzzle_id="VE001",
        input_alphabet="arabic_digits",
        output_alphabet="arabic_digits",
        expected_solution=SOLUTION,
        puzzle=PUZZLE,
        metadata={
            "diagnostic": "very_easy_57_clues",
            "difficulty": "very_easy",
            "input_symbols": list(alphabet.symbols),
            "output_symbols": list(alphabet.symbols),
            "output_format": "spaced",
            "empty_marker": ".",
            "evaluation_kind": "sudoku",
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", choices=sorted(PROFILE_BY_MODEL))
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--test-only", action="store_true")
    parser.add_argument("--execute", action="store_true", help=argparse.SUPPRESS)
    arguments = parser.parse_args()

    base_config = load_config(arguments.config)
    config, model = apply_calibration_profile(base_config, PROFILE_BY_MODEL[arguments.model])
    config = replace(config, run_id=f"configuration-diagnostic-v1-very-easy-{model.name}")
    request = diagnostic_request(model)

    if not arguments.execute:
        path = write_python_job(
            config,
            model,
            Path(__file__),
            "very-easy-diagnostic",
            (arguments.model, "--config", str(arguments.config.resolve())),
        )
        return finish_submission(path, dry_run=arguments.dry_run, test_only=arguments.test_only)

    summary = execute_requests(config, model, "diagnostic", (request,))
    path = model_directory(config, model) / "diagnostic" / "shard-000-of-001.jsonl"
    result = tuple(iter_result_values((path,)))
    if len(result) != 1:
        raise RuntimeError("very-easy diagnostic did not produce exactly one result")
    print(json.dumps({"summary": asdict(summary), "result": result[0]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
