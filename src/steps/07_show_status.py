#!/usr/bin/env python3
"""Step 7: show completed work and the next job to submit."""

from __future__ import annotations

import argparse

from _shared import add_config_argument
from experiments.config import load_config
from experiments.workflow import ModelWorkflowStatus, workflow_status


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_config_argument(parser)
    parser.add_argument("--model", action="append", help="show only this model; repeat if needed")
    arguments = parser.parse_args()
    config = load_config(arguments.config)
    models = config.enabled_models
    if arguments.model:
        requested = set(arguments.model)
        models = tuple(model for model in models if model.name in requested)
        missing = requested - {model.name for model in models}
        if missing:
            raise SystemExit("Unknown or disabled models: " + ", ".join(sorted(missing)))

    for model in models:
        status = workflow_status(config, model)
        print(f"\n{model.name}")
        print(f"  qualification: {_word(status.qualification_complete)}")
        for experiment, parts in status.experiments.items():
            print(f"  {experiment}: {sum(parts)}/{len(parts)} parts complete")
        print(f"  finalization: {_word(status.finalization_complete)}")
        print(f"  next: {_next_command(model.name, status)}")
    return 0


def _word(complete: bool) -> str:
    return "complete" if complete else "not complete"


def _next_command(model_name: str, status: ModelWorkflowStatus) -> str:
    if not status.qualification_complete:
        return f"python steps/04_submit_qualification.py {model_name}"
    for experiment, parts in status.experiments.items():
        for index, complete in enumerate(parts, start=1):
            if not complete:
                command = f"python steps/05_submit_experiment.py {model_name} {experiment}"
                return command if len(parts) == 1 else f"{command} --part {index}"
    if not status.finalization_complete:
        return f"python steps/06_submit_finalization.py {model_name}"
    return "all work is complete"


if __name__ == "__main__":
    raise SystemExit(main())
