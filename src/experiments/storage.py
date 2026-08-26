"""Append-only, shard-local result storage with corruption detection and resume support."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterable

from .records import ExperimentResult


class ResultStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._completed = self._load_completed()

    @property
    def completed_request_ids(self) -> frozenset[str]:
        return frozenset(self._completed)

    def contains(self, request_id: str) -> bool:
        return request_id in self._completed

    def append(self, result: ExperimentResult) -> None:
        request_id = result.request.request_id
        if request_id in self._completed:
            raise ValueError(f"request {request_id} is already stored in {self.path}")
        line = json.dumps(
            result.to_dict(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ) + "\n"
        with self.path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(line)
            stream.flush()
            os.fsync(stream.fileno())
        self._completed.add(request_id)

    def _load_completed(self) -> set[str]:
        if not self.path.exists():
            return set()
        completed: set[str] = set()
        with self.path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, start=1):
                try:
                    value = json.loads(line)
                    request_id = value["request"]["request_id"]
                except (json.JSONDecodeError, KeyError, TypeError) as error:
                    raise ValueError(f"corrupt result line {line_number} in {self.path}: {error}") from error
                if request_id in completed:
                    raise ValueError(f"duplicate request {request_id} in {self.path}")
                completed.add(request_id)
        return completed


def iter_result_values(paths: Iterable[Path]) -> Iterable[dict[str, Any]]:
    for path in sorted(paths):
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, start=1):
                try:
                    yield json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(f"corrupt result line {line_number} in {path}: {error}") from error
