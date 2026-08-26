#!/usr/bin/env python3
"""Run the reproducible Sudoku build, skipping unchanged successful steps.

Examples:
    python3 run_pipeline.py
    python3 run_pipeline.py --status
    python3 run_pipeline.py --force
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

from sudoku.dataset import TIERS
from sudoku.generator import GENERATOR_VERSION

ROOT = Path(__file__).resolve().parent
DATA_DIRECTORY = ROOT / "data"
STATE_PATH = DATA_DIRECTORY / "pipeline-state.json"
STATE_VERSION = 1
STEPS = ("tests", "generate", "audit")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Test, generate, and audit the thesis Sudoku corpus idempotently."
    )
    parser.add_argument("--master-seed", type=int, default=20260826)
    parser.add_argument("--puzzles-per-tier", type=int, default=100)
    parser.add_argument("--force", action="store_true", help="rerun every step")
    parser.add_argument("--status", action="store_true", help="show step state without running")
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    if arguments.master_seed < 0:
        raise SystemExit("--master-seed must be non-negative")
    if arguments.puzzles_per_tier < 1:
        raise SystemExit("--puzzles-per-tier must be positive")

    state = _read_state()
    fingerprints = _fingerprints(arguments.master_seed, arguments.puzzles_per_tier)
    if arguments.status:
        _print_status(state, fingerprints, arguments)
        return 0

    commands = {
        "tests": [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        "generate": [
            sys.executable,
            "-m",
            "sudoku.cli",
            "generate",
            "--master-seed",
            str(arguments.master_seed),
            "--puzzles-per-tier",
            str(arguments.puzzles_per_tier),
            "--output",
            str(DATA_DIRECTORY),
        ],
        "audit": [
            sys.executable,
            "-m",
            "sudoku.cli",
            "audit",
            "--input",
            str(DATA_DIRECTORY),
        ],
    }

    for step in STEPS:
        fingerprints = _fingerprints(arguments.master_seed, arguments.puzzles_per_tier)
        fingerprint = fingerprints[step]
        completed = state["steps"].get(step, {})
        unchanged = completed.get("fingerprint") == fingerprint
        artifacts_valid = step not in {"generate", "audit"} or _artifacts_match_manifest(
            arguments.master_seed, arguments.puzzles_per_tier
        )

        if not arguments.force and unchanged and artifacts_valid:
            print(f"SKIP {step}: unchanged and previously successful", flush=True)
            continue

        if (
            step == "generate"
            and not arguments.force
            and not completed
            and _artifacts_match_manifest(arguments.master_seed, arguments.puzzles_per_tier)
        ):
            print("ADOPT generate: existing corpus and manifest are valid", flush=True)
        else:
            print(f"RUN  {step}", flush=True)
            _run(commands[step])

        final_fingerprints = _fingerprints(arguments.master_seed, arguments.puzzles_per_tier)
        state["steps"][step] = {
            "fingerprint": final_fingerprints[step],
            "completed_at": datetime.now(UTC).isoformat(),
        }
        _write_state(state)

    print("DONE pipeline is complete", flush=True)
    return 0


def _run(command: list[str]) -> None:
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(ROOT)
    subprocess.run(command, cwd=ROOT, env=environment, check=True)


def _read_state() -> dict[str, Any]:
    try:
        value = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        if value.get("state_version") != STATE_VERSION or not isinstance(value.get("steps"), dict):
            raise ValueError("unsupported pipeline state")
        return value
    except (FileNotFoundError, json.JSONDecodeError, TypeError, ValueError):
        return {"state_version": STATE_VERSION, "steps": {}}


def _write_state(state: dict[str, Any]) -> None:
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)
    temporary_path = DATA_DIRECTORY / ".pipeline-state.tmp"
    temporary_path.write_text(
        json.dumps(state, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary_path.replace(STATE_PATH)


def _fingerprints(master_seed: int, puzzles_per_tier: int) -> dict[str, str]:
    source_files = sorted((ROOT / "sudoku").glob("*.py"))
    test_files = sorted((ROOT / "tests").glob("*.py"))
    configuration = json.dumps(
        {
            "master_seed": master_seed,
            "puzzles_per_tier": puzzles_per_tier,
            "generator_version": GENERATOR_VERSION,
        },
        sort_keys=True,
    ).encode("utf-8")
    source_digest = _digest_files(source_files + [ROOT / "pyproject.toml", Path(__file__)])
    tests_digest = _digest_files(source_files + test_files + [ROOT / "pyproject.toml", Path(__file__)])
    artifacts = [
        DATA_DIRECTORY / "puzzles.jsonl",
        DATA_DIRECTORY / "generation-report.json",
        DATA_DIRECTORY / "manifest.json",
    ]
    return {
        "tests": _digest_parts([tests_digest.encode("ascii")]),
        "generate": _digest_parts([source_digest.encode("ascii"), configuration]),
        "audit": _digest_parts(
            [source_digest.encode("ascii"), configuration, _digest_files(artifacts).encode("ascii")]
        ),
    }


def _digest_files(paths: Iterable[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: str(item)):
        relative = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        digest.update(str(relative).encode("utf-8"))
        digest.update(b"\0")
        if path.is_file():
            digest.update(path.read_bytes())
        else:
            digest.update(b"<missing>")
        digest.update(b"\0")
    return digest.hexdigest()


def _digest_parts(parts: Iterable[bytes]) -> str:
    digest = hashlib.sha256()
    for part in parts:
        digest.update(part)
        digest.update(b"\0")
    return digest.hexdigest()


def _artifacts_match_manifest(master_seed: int, puzzles_per_tier: int) -> bool:
    dataset_path = DATA_DIRECTORY / "puzzles.jsonl"
    report_path = DATA_DIRECTORY / "generation-report.json"
    manifest_path = DATA_DIRECTORY / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        expected_counts = {tier: puzzles_per_tier for tier in TIERS}
        return (
            manifest["generator_version"] == GENERATOR_VERSION
            and manifest["master_seed"] == master_seed
            and manifest["record_count"] == puzzles_per_tier * len(TIERS)
            and manifest["difficulty_counts"] == expected_counts
            and manifest["files"][dataset_path.name] == _sha256_file(dataset_path)
            and manifest["files"][report_path.name] == _sha256_file(report_path)
        )
    except (FileNotFoundError, KeyError, TypeError, json.JSONDecodeError):
        return False


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _print_status(state: dict[str, Any], fingerprints: dict[str, str], arguments: Any) -> None:
    print(
        f"configuration: master_seed={arguments.master_seed}, "
        f"puzzles_per_tier={arguments.puzzles_per_tier}"
    )
    artifacts_valid = _artifacts_match_manifest(arguments.master_seed, arguments.puzzles_per_tier)
    for step in STEPS:
        completed = state["steps"].get(step, {})
        if completed.get("fingerprint") != fingerprints[step]:
            status = "pending"
        elif step in {"generate", "audit"} and not artifacts_valid:
            status = "invalidated"
        else:
            status = "complete"
        print(f"{step}: {status}")


if __name__ == "__main__":
    raise SystemExit(main())
