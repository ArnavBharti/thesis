#!/usr/bin/env python3
"""Step 8: separate transformed input decoding from transformed output generation."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from lib.prompts import PromptOptions, format_solution
from lib.protocol import verify_global_protocol
from lib.records import ExperimentRequest, Message
from lib.requests import sudoku_request
from lib.results import index_results
from lib.samples import load_sample_plan
from lib.slurm import finish_submission, write_python_job
from lib.steps import execute_requests, load_enabled_model
from lib.sudoku.dataset import read_records
from lib.sudoku.representations import ALPHABETS, SymbolAlphabet, encode_grid
from lib.sudoku.schema import PuzzleRecord, grid_from_compact
from lib.workflow import experiment_complete, experiment_part_complete

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "config" / "experiments.json"


def control_requests(
    model_name: str,
    record: PuzzleRecord,
    greek: SymbolAlphabet,
    arabic: SymbolAlphabet,
) -> tuple[ExperimentRequest, ...]:
    solution = grid_from_compact(record.solution)
    greek_solution = encode_grid(solution, greek)
    arabic_solution = format_solution(solution, arabic, "spaced")
    row = greek_solution.splitlines()[0]
    controls = (
        ("control_copy", f"Copy the following row exactly. Return only the copied row.\n\n{row}", row),
        (
            "control_mapping_translation",
            "Using α=1, β=2, γ=3, δ=4, ε=5, ζ=6, η=7, θ=8, ι=9, translate this sequence. Return only the translated space-separated sequence.\n\nε γ η",
            "5 3 7",
        ),
        (
            "control_coordinate_retrieval",
            f"Grid:\n{greek_solution}\n\nWhich symbol is in row 1, column 5? Return only that symbol.",
            greek.symbol_for(solution.cells[4]),
        ),
        (
            "control_occurrence_count",
            f"Count occurrences of {greek.symbol_for(1)} in this completed grid. Return only the integer.\n\n{greek_solution}",
            "9",
        ),
        (
            "control_grid_conversion",
            "Convert the supplied completed Greek grid to Arabic digits using α=1 through ι=9. Return only 9 lines of 9 space-separated digits.\n\n"
            + greek_solution,
            arabic_solution,
        ),
    )
    return tuple(
        ExperimentRequest(
            experiment="exp6",
            condition=condition,
            model=model_name,
            messages=(Message("user", prompt),),
            puzzle_id=record.puzzle_id,
            metadata={
                "difficulty": record.difficulty,
                "evaluation_kind": "exact_text",
                "expected_text": expected,
            },
        )
        for condition, prompt, expected in controls
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--test-only", action="store_true")
    parser.add_argument("--execute", action="store_true", help=argparse.SUPPRESS)
    arguments = parser.parse_args()

    config, model = load_enabled_model(arguments.config, arguments.model)
    verify_global_protocol(config, load_sample_plan(config))
    if not experiment_complete(config, model, "exp4"):
        raise SystemExit(f"finish all Step 7 parts for {model.name} first")
    if experiment_part_complete(config, model, "exp6", 1):
        print(f"SKIP: input/output experiment is complete for {model.name}")
        return 0
    if not arguments.execute:
        path = write_python_job(
            config,
            model,
            Path(__file__),
            "exp6-input-output",
            (model.name, "--config", str(arguments.config.resolve())),
        )
        return finish_submission(path, dry_run=arguments.dry_run, test_only=arguments.test_only)

    records = read_records(config.dataset_path)
    puzzles = load_sample_plan(config).records("mechanism", records)
    arabic = ALPHABETS["arabic_digits"]
    greek = ALPHABETS["greek_letters"]
    all_requests: list[ExperimentRequest] = []
    inference_requests: list[ExperimentRequest] = []
    reused_conditions: list[tuple[ExperimentRequest, str]] = []

    for record in puzzles:
        conditions = (
            ("A_arabic_to_arabic", arabic, arabic),
            ("B_greek_to_greek", greek, greek),
            ("C_greek_to_arabic", greek, arabic),
            ("D_arabic_to_greek", arabic, greek),
        )
        for condition, input_alphabet, output_alphabet in conditions:
            request = sudoku_request(
                "exp6",
                condition,
                model,
                record,
                input_alphabet,
                output_alphabet,
                options=PromptOptions(
                    mapping_style="to_digits" if input_alphabet != output_alphabet else "alphabet_only"
                ),
                metadata={"reused_from_step": "exp4"} if condition.startswith(("A_", "B_")) else None,
            )
            all_requests.append(request)
            if condition == "A_arabic_to_arabic":
                reused_conditions.append((request, "arabic_digits"))
            elif condition == "B_greek_to_greek":
                reused_conditions.append((request, "greek_letters"))
            else:
                inference_requests.append(request)
        controls = control_requests(model.name, record, greek, arabic)
        all_requests.extend(controls)
        inference_requests.extend(controls)

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
        "exp6",
        all_requests,
        inference_requests=inference_requests,
        reused_results=reused_results,
        manifest_notes={"new_calls_per_puzzle": 7, "reused_conditions": ["A", "B"]},
    )
    print(json.dumps(asdict(summary), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
