#!/usr/bin/env python3
"""Show completed work and the next command for each model."""

from __future__ import annotations

import argparse
from pathlib import Path

from lib.config import load_config
from lib.samples import sample_plan_path
from lib.workflow import workflow_status

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "config" / "experiments.json"

SCRIPT_FOR_EXPERIMENT = {
    "exp2": "05_run_pilot.py",
    "exp4": "07_run_main_benchmark.py",
    "exp6": "08_run_input_output_cross.py",
    "exp7": "09_run_token_length.py",
    "exp8": "10_run_binding.py",
    "exp9": "11_run_ablations.py",
    "exp10": "12_run_revisions.py",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--model", action="append", help="show only this model; repeat if needed")
    arguments = parser.parse_args()

    config = load_config(arguments.config)
    models = config.enabled_models
    if arguments.model:
        requested = set(arguments.model)
        unknown = requested - {model.name for model in models}
        if unknown:
            raise SystemExit("unknown models: " + ", ".join(sorted(unknown)))
        models = tuple(model for model in models if model.name in requested)

    protocol_frozen = sample_plan_path(config).exists()
    for model in models:
        status = workflow_status(config, model)
        print(f"\n{model.name}")
        print(f"  qualification: {_word(status.qualification_complete)}")
        for experiment, parts in status.experiments.items():
            print(f"  {experiment}: {sum(parts)}/{len(parts)} parts complete")
        print(f"  analysis: {_word(status.finalization_complete)}")
        print(f"  next: {_next_command(model.name, status, protocol_frozen)}")
    return 0


def _word(value: bool) -> str:
    return "complete" if value else "not complete"


def _next_command(model_name: str, status, protocol_frozen: bool) -> str:
    if not status.qualification_complete:
        return f"python 04_qualify_model.py {model_name}"
    pilot = status.experiments["exp2"]
    if not all(pilot):
        return f"python 05_run_pilot.py {model_name}"
    if not protocol_frozen:
        return "python 06_freeze_protocol.py  # after every model pilot is complete"
    for experiment, parts in status.experiments.items():
        if experiment == "exp2":
            continue
        for part, complete in enumerate(parts, start=1):
            if not complete:
                command = f"python {SCRIPT_FOR_EXPERIMENT[experiment]} {model_name}"
                return f"{command} --part {part}" if len(parts) > 1 else command
    if not status.finalization_complete:
        return f"python 13_analyze_results.py {model_name}"
    return "all work is complete"


if __name__ == "__main__":
    raise SystemExit(main())
