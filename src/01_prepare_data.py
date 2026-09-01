#!/usr/bin/env python3
"""Step 1: test, create when needed, and audit the 300-puzzle dataset."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from lib.sudoku.dataset import (
    DatasetConfig,
    TIERS,
    audit_directory,
    generate_dataset,
    write_dataset,
)
from lib.sudoku.generator import GENERATOR_VERSION

ROOT = Path(__file__).resolve().parent
DATA_DIRECTORY = ROOT / "data"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--master-seed", type=int, default=20260826)
    parser.add_argument("--puzzles-per-tier", type=int, default=100)
    parser.add_argument("--force", action="store_true", help="regenerate even when data are valid")
    parser.add_argument("--status", action="store_true", help="only inspect existing data")
    arguments = parser.parse_args()

    expected_counts = {tier: arguments.puzzles_per_tier for tier in TIERS}
    try:
        audit = audit_directory(DATA_DIRECTORY)
        manifest = json.loads((DATA_DIRECTORY / "manifest.json").read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        audit = {"valid": False, "record_count": 0, "difficulty_counts": {}, "errors": []}
        manifest = {}
    ready = (
        audit["valid"]
        and audit["record_count"] == arguments.puzzles_per_tier * len(TIERS)
        and audit["difficulty_counts"] == expected_counts
        and manifest.get("master_seed") == arguments.master_seed
        and manifest.get("generator_version") == GENERATOR_VERSION
    )

    if arguments.status:
        print("READY" if ready else "NOT READY")
        print(f"Puzzles: {audit['record_count']}")
        for error in audit.get("errors", []):
            print(f"  {error}")
        return 0 if ready else 1

    print("Running automated tests...")
    subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=ROOT,
        check=True,
    )

    if ready and not arguments.force:
        print("SKIP generation: the existing 300-puzzle dataset is valid")
    else:
        print("Generating the certified Sudoku dataset...")
        result = generate_dataset(
            DatasetConfig(
                master_seed=arguments.master_seed,
                puzzles_per_tier=arguments.puzzles_per_tier,
            )
        )
        write_dataset(result, DATA_DIRECTORY)

    final_audit = audit_directory(DATA_DIRECTORY)
    if not final_audit["valid"]:
        raise SystemExit("dataset audit failed: " + "; ".join(final_audit["errors"]))
    print(f"DONE: {final_audit['record_count']} certified puzzles are ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
