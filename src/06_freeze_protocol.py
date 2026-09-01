#!/usr/bin/env python3
"""Step 6: freeze the reduced sample plan after every pilot is complete."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib.config import load_config
from lib.protocol import freeze_json, global_protocol
from lib.samples import build_sample_plan, freeze_sample_plan
from lib.results import iter_result_values
from lib.statistics import pilot_summary
from lib.sudoku.dataset import audit_records, read_records
from lib.workflow import experiment_part_complete, model_directory, qualification_complete

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
        summary = pilot_summary(
            iter_result_values((model_directory(config, model) / "exp2").glob("shard-*.jsonl"))
        )
        summary_path = model_directory(config, model) / "exp2" / "pilot-summary.json"
        summary_text = json.dumps(summary, indent=2, sort_keys=True) + "\n"
        if summary_path.exists() and summary_path.read_text(encoding="utf-8") != summary_text:
            raise ValueError(f"pilot summary changed at {summary_path}")
        summary_path.write_text(summary_text, encoding="utf-8", newline="\n")
        outside = [tier for tier, value in summary.items() if not value["within_target"]]
        result = ", ".join(
            f"{tier}={value['correct']}/{value['evaluated']}" for tier, value in summary.items()
        )
        print(f"{model.name} Arabic pilot: {result}")
        if outside:
            print("  WARNING: outside the planned range for " + ", ".join(outside))

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
