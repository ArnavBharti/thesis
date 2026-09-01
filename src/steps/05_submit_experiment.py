#!/usr/bin/env python3
"""Step 5: submit one experiment part for one qualified model."""

from __future__ import annotations

import argparse

from _shared import add_submit_arguments, finish_job, load_model
from experiments.slurm import experiment_job
from experiments.workflow import (
    INFERENCE_EXPERIMENTS,
    experiment_part_complete,
    experiments_for,
    qualification_complete,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", help="model name from config/experiments.json")
    parser.add_argument("experiment", choices=INFERENCE_EXPERIMENTS)
    parser.add_argument("--part", type=int, default=1, help="part number, starting at 1")
    add_submit_arguments(parser)
    arguments = parser.parse_args()
    config, model = load_model(arguments.config, arguments.model)

    if not qualification_complete(config, model):
        raise SystemExit(f"{model.name} has not passed qualification")
    if arguments.experiment not in experiments_for(model):
        print(f"SKIP: {arguments.experiment} needs an exact tokenizer and is not run for {model.name}")
        return 0

    parts = config.shard_count(arguments.experiment)
    if not 1 <= arguments.part <= parts:
        raise SystemExit(f"--part must be between 1 and {parts}")
    if experiment_part_complete(config, model, arguments.experiment, arguments.part):
        print(
            f"SKIP: {model.name} {arguments.experiment} "
            f"part {arguments.part}/{parts} is already complete"
        )
        return 0

    path = experiment_job(
        arguments.config,
        config,
        model,
        arguments.experiment,
        arguments.part,
    )
    return finish_job(path, dry_run=arguments.dry_run, test_only=arguments.test_only)


if __name__ == "__main__":
    raise SystemExit(main())
