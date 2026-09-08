#!/usr/bin/env python3
"""Step 3: check the dataset, model files, and OpenRouter key."""

from __future__ import annotations

import argparse
import importlib
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

from lib.config import load_config
from lib.models import probe_model
from lib.sudoku.dataset import audit_records, read_records

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "config" / "experiments.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--model", action="append", help="check only this model; repeat if needed")
    arguments = parser.parse_args()

    config = load_config(arguments.config)
    audit = audit_records(read_records(config.dataset_path))
    print(f"Dataset: {'READY' if audit['valid'] else 'FAILED'} ({audit['record_count']} puzzles)")
    if not audit["valid"]:
        for error in audit["errors"]:
            print(f"  {error}")
        return 1

    models = config.enabled_models
    if arguments.model:
        requested = set(arguments.model)
        unknown = requested - {model.name for model in models}
        if unknown:
            raise SystemExit("unknown or disabled models: " + ", ".join(sorted(unknown)))
        models = tuple(model for model in models if model.name in requested)

    failed = False
    print(
        f"Python runtime: READY ({sys.version.split()[0]}, SQLite {sqlite3.sqlite_version})"
    )
    if any(model.backend == "vllm" for model in models):
        try:
            getattr(importlib.import_module("vllm"), "LLM")
        except Exception as error:
            print("vLLM import: FAILED")
            print(f"  {type(error).__name__}: {error}")
            failed = True
        else:
            print("vLLM import: READY")
        cuda_ready, cuda_detail = check_cuda_versions()
        print(f"CUDA compiler: {'READY' if cuda_ready else 'FAILED'}")
        print(f"  {cuda_detail}")
        failed |= not cuda_ready
    for model in models:
        ready, detail = probe_model(model)
        print(f"{model.name}: {'READY' if ready else 'MISSING'}")
        print(f"  {detail}")
        failed |= not ready
    return 1 if failed else 0


def check_cuda_versions() -> tuple[bool, str]:
    """Confirm that the bundled compiler matches PyTorch's CUDA headers."""

    try:
        torch = importlib.import_module("torch")
    except Exception as error:
        return False, f"cannot import torch: {error}"

    runtime_version = getattr(torch.version, "cuda", None)
    if not runtime_version:
        return False, "the installed PyTorch build has no CUDA runtime"

    candidates = sorted(
        Path(sys.prefix).glob("lib/python*/site-packages/nvidia/cu*/bin/nvcc")
    )
    if not candidates:
        return False, "bundled nvcc is missing; reinstall the local dependencies"

    compiler = candidates[0]
    try:
        result = subprocess.run(
            [str(compiler), "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        return False, f"cannot run {compiler}: {error}"

    match = re.search(r"release\s+(\d+\.\d+)", result.stdout)
    if not match:
        return False, f"could not read the CUDA version from {compiler}"
    compiler_version = match.group(1)
    runtime_major_minor = ".".join(runtime_version.split(".")[:2])
    if compiler_version != runtime_major_minor:
        return (
            False,
            f"nvcc {compiler_version} does not match PyTorch CUDA {runtime_major_minor}; "
            'run python -m pip install -e ".[local]" again',
        )
    return True, f"nvcc {compiler_version} matches PyTorch CUDA {runtime_major_minor}"


if __name__ == "__main__":
    raise SystemExit(main())
