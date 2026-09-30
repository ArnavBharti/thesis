#!/usr/bin/env python3
"""Losslessly archive copied experiment artifacts with compressed/raw checksums."""

import argparse
import gzip
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        manifest = json.loads((args.destination / "snapshot-manifest.json").read_text())
        for entry in manifest["files"]:
            data = (args.destination / entry["path"]).read_bytes()
            raw = gzip.decompress(data) if entry["compressed"] else data
            if digest(data) != entry["stored_sha256"] or digest(raw) != entry["raw_sha256"]:
                raise SystemExit(f"checksum mismatch: {entry['path']}")
        print(f"Verified {len(manifest['files'])} stored and raw checksums")
        return
    entries = []
    for path in sorted(args.source.rglob("*")):
        if not path.is_file() or path.name.startswith(".env"):
            continue
        if path.suffix not in {".jsonl", ".json", ".out", ".err", ".sbatch", ".tsv", ".txt"}:
            continue
        relative = path.relative_to(args.source)
        if relative.parts[0] not in {"experiment_outputs", "generated", "scheduler"}:
            continue
        raw = path.read_bytes()
        compressed = path.suffix in {".jsonl", ".out", ".err"}
        stored = gzip.compress(raw, compresslevel=9, mtime=0) if compressed else raw
        target = args.destination / (str(relative) + (".gz" if compressed else ""))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(stored)
        entries.append({"path": str(target.relative_to(args.destination)), "compressed": compressed,
                        "raw_bytes": len(raw), "stored_bytes": len(stored),
                        "raw_sha256": digest(raw), "stored_sha256": digest(stored)})
    manifest = {"schema_version": 1, "archived_at_utc": datetime.now(timezone.utc).isoformat(),
                "source": "Read-only rsync of Sharanga experiment_outputs and slurm/generated",
                "capture_note": "Qwen active shard status must be checked against its completion marker and request digest.",
                "files": entries}
    args.destination.mkdir(parents=True, exist_ok=True)
    (args.destination / "snapshot-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Archived {len(entries)} files, {sum(e['stored_bytes'] for e in entries)} stored bytes")


if __name__ == "__main__":
    main()
