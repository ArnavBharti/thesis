"""Command-line interface for generating and auditing the thesis Sudoku corpus."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .dataset import DatasetConfig, audit_directory, generate_dataset, write_dataset

DEFAULT_DATA_DIRECTORY = Path(__file__).resolve().parents[1] / "data"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="thesis-sudoku")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="generate the certified puzzle corpus")
    generate.add_argument("--master-seed", type=int, default=20260826)
    generate.add_argument("--puzzles-per-tier", type=int, default=100)
    generate.add_argument("--output", type=Path, default=DEFAULT_DATA_DIRECTORY)

    audit = subparsers.add_parser("audit", help="independently audit a generated corpus")
    audit.add_argument("--input", type=Path, default=DEFAULT_DATA_DIRECTORY)
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    if arguments.command == "generate":
        result = generate_dataset(
            DatasetConfig(
                master_seed=arguments.master_seed,
                puzzles_per_tier=arguments.puzzles_per_tier,
            )
        )
        manifest = write_dataset(result, arguments.output)
        print(json.dumps(manifest, indent=2, sort_keys=True))
        return 0

    audit = audit_directory(arguments.input)
    print(json.dumps(audit, indent=2, sort_keys=True))
    return 0 if audit["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
