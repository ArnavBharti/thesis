#!/usr/bin/env python3
"""Step 2: download or verify the two pinned local model snapshots."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from lib.config import load_config
from lib.downloads import ensure_snapshot, local_models

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "config" / "experiments.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--model", action="append", help="local model name; repeat if needed")
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()

    config = load_config(arguments.config)
    models = local_models(config.models)
    if arguments.model:
        requested = set(arguments.model)
        unknown = requested - {model.name for model in models}
        if unknown:
            raise SystemExit("unknown local models: " + ", ".join(sorted(unknown)))
        models = tuple(model for model in models if model.name in requested)

    for model in models:
        plan = {
            "model": model.name,
            "repo_id": model.resolved_model_id,
            "revision": model.revision,
            "HF_HOME": os.environ.get("HF_HOME", "Hugging Face default"),
        }
        if arguments.dry_run:
            print(json.dumps({**plan, "status": "planned"}, sort_keys=True))
            continue
        snapshot = ensure_snapshot(model, None, verify_only=arguments.verify_only)
        status = "verified" if arguments.verify_only else "ready"
        print(json.dumps({**plan, "status": status, "snapshot_path": str(snapshot)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
