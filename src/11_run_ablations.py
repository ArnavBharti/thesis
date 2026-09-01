#!/usr/bin/env python3
"""Step 11: test prompt wording, mapping, formatting, and empty markers."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from lib.prompts import PromptOptions
from lib.protocol import verify_global_protocol
from lib.requests import sudoku_request
from lib.samples import load_sample_plan
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
    verify_global_protocol(config, load_sample_plan(config))
    if not experiment_complete(config, model, "exp4"):
        raise SystemExit(f"finish all Step 7 parts for {model.name} first")
    if experiment_part_complete(config, model, "exp9", 1):
        print(f"SKIP: ablation experiment is complete for {model.name}")
        return 0
    if not arguments.execute:
        path = write_python_job(
            config,
            model,
            Path(__file__),
            "exp9-ablations",
            (model.name, "--config", str(arguments.config.resolve())),
        )
        return finish_submission(path, dry_run=arguments.dry_run, test_only=arguments.test_only)

    records = read_records(config.dataset_path)
    puzzles = load_sample_plan(config).records("ablation", records)
    greek = ALPHABETS["greek_letters"]
    variants: list[tuple[str, SymbolAlphabet, PromptOptions]] = []

    for style in ("minimal", "explicit_constraints", "constraints_alphabet", "fully_explicit"):
        variants.append((f"rules_{style}", greek, PromptOptions(rule_style=style)))
    for style in ("alphabet_only", "to_digits", "to_abstract"):
        variants.append((f"mapping_{style}", greek, PromptOptions(mapping_style=style)))
    for output_format in ("spaced", "compact", "string81", "json"):
        variants.append((f"output_{output_format}", greek, PromptOptions(output_format=output_format)))
    for name, marker in (("dot", "."), ("zero", "0"), ("underscore", "_"), ("word", "EMPTY")):
        variants.append((f"empty_{name}", greek, PromptOptions(empty_marker=marker)))
    variants.extend(
        (
            ("latin_uppercase", ALPHABETS["uppercase_latin"], PromptOptions()),
            ("latin_lowercase", ALPHABETS["lowercase_latin"], PromptOptions()),
            ("nonce_uppercase", ALPHABETS["nonce_labels"], PromptOptions()),
            (
                "nonce_lowercase",
                SymbolAlphabet(
                    "nonce_lowercase",
                    tuple(symbol.lower() for symbol in ALPHABETS["nonce_labels"].symbols),
                ),
                PromptOptions(),
            ),
        )
    )

    requests = tuple(
        sudoku_request("exp9", condition, model, record, alphabet, options=options)
        for record in puzzles
        for condition, alphabet, options in variants
    )
    summary = execute_requests(
        config,
        model,
        "exp9",
        requests,
        manifest_notes={"puzzles": len(puzzles), "conditions": len(variants), "exploratory": True},
    )
    print(json.dumps(asdict(summary), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
