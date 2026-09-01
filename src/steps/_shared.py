"""Shared command-line helpers for the numbered workflow scripts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.config import ExperimentConfig, ModelConfig, load_config  # noqa: E402
from experiments.slurm import submit_job  # noqa: E402

DEFAULT_CONFIG = ROOT / "config" / "experiments.json"


def add_config_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)


def add_submit_arguments(parser: argparse.ArgumentParser) -> None:
    add_config_argument(parser)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="write the job file but do not submit it")
    mode.add_argument("--test-only", action="store_true", help="ask Slurm to validate the job without submitting it")


def load_model(config_path: Path, model_name: str) -> tuple[ExperimentConfig, ModelConfig]:
    config = load_config(config_path)
    try:
        model = config.model(model_name)
    except KeyError as error:
        choices = ", ".join(model.name for model in config.enabled_models)
        raise SystemExit(f"Unknown model {model_name!r}. Choose one of: {choices}") from error
    if not model.enabled:
        raise SystemExit(f"Model {model_name!r} is disabled in the configuration")
    return config, model


def finish_job(path: Path, *, dry_run: bool, test_only: bool) -> int:
    print(f"Job file: {path}")
    if dry_run:
        print("DRY RUN: the job was not submitted")
        return 0
    if test_only:
        submit_job(path, test_only=True)
        print("Slurm accepted the resource request. The job was not submitted.")
        return 0
    job_id = submit_job(path)
    print(f"Submitted one job: {job_id}")
    return 0
