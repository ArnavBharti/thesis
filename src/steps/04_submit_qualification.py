#!/usr/bin/env python3
"""Step 4: submit one five-puzzle qualification job for one model."""

from __future__ import annotations

import argparse

from _shared import add_submit_arguments, finish_job, load_model
from experiments.slurm import qualification_job
from experiments.workflow import qualification_result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", help="model name from config/experiments.json")
    add_submit_arguments(parser)
    arguments = parser.parse_args()
    config, model = load_model(arguments.config, arguments.model)

    result = qualification_result(config, model)
    if result is True:
        print(f"SKIP: {model.name} already passed qualification")
        return 0
    if result is False:
        raise SystemExit(
            f"{model.name} failed qualification. Inspect its output before using a new run_id."
        )

    path = qualification_job(arguments.config, config, model)
    return finish_job(path, dry_run=arguments.dry_run, test_only=arguments.test_only)


if __name__ == "__main__":
    raise SystemExit(main())
