#!/usr/bin/env python3
"""Step 6: freeze the reduced sample plan after every pilot is complete."""

from __future__ import annotations

import argparse
from pathlib import Path

from lib.config import load_config
from lib.protocol import freeze_json, global_protocol
from lib.samples import build_sample_plan, freeze_sample_plan
from lib.sudoku.dataset import audit_records, read_records
from lib.workflow import experiment_part_complete, qualification_complete

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "config" / "experiments.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    arguments = parser.parse_args()

    config = load_config(arguments.config)
    records = read_records(config.dataset_path)
    audit = audit_records(records)
    if not audit["valid"]:
        raise SystemExit("dataset audit failed: " + "; ".join(audit["errors"]))

    for model in config.enabled_models:
        if not qualification_complete(config, model):
            raise SystemExit(f"{model.name} has not passed qualification")
        if not experiment_part_complete(config, model, "exp2", 1):
            raise SystemExit(f"{model.name} has not completed the pilot")

    plan = build_sample_plan(config, records)
    sample_path = freeze_sample_plan(config, plan)
    protocol_path = freeze_json(
        config.output_directory / config.run_id / "protocol.json",
        global_protocol(config, plan),
    )
    print(f"Sample plan: {sample_path}")
    print(f"Protocol: {protocol_path}")
    print("DONE: confirmatory samples and settings are frozen")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
