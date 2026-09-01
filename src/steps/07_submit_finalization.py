#!/usr/bin/env python3
"""Step 7: submit token-registry and analysis work for one finished model."""

from __future__ import annotations

import argparse

from _shared import add_submit_arguments, finish_job, load_model
from experiments.slurm import finalization_job
from experiments.workflow import workflow_status


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", help="model name from config/experiments.json")
    add_submit_arguments(parser)
    arguments = parser.parse_args()
    config, model = load_model(arguments.config, arguments.model)
    status = workflow_status(config, model)

    if status.finalization_complete:
        print(f"SKIP: {model.name} is already finalized")
        return 0
    if not status.inference_complete:
        missing = sum(not complete for parts in status.experiments.values() for complete in parts)
        raise SystemExit(
            f"{model.name} still has {missing} unfinished experiment job(s). "
            "Run steps/06_show_status.py for details."
        )

    path = finalization_job(arguments.config, config, model)
    return finish_job(path, dry_run=arguments.dry_run, test_only=arguments.test_only)


if __name__ == "__main__":
    raise SystemExit(main())
