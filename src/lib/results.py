"""Append-only result storage with corruption detection and resume support."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterable

from .records import ExperimentRequest, ExperimentResult, Generation


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


def index_results(
    paths: Iterable[Path],
) -> dict[tuple[str, str], dict[str, Any]]:
    """Index results by puzzle ID and condition, rejecting duplicates."""

    indexed: dict[tuple[str, str], dict[str, Any]] = {}
    for value in iter_result_values(paths):
        request = value["request"]
        key = (request.get("puzzle_id"), request["condition"])
        if key in indexed:
            raise ValueError(f"duplicate result key: {key}")
        indexed[key] = value
    return indexed


def store_reused_result(
    store: ResultStore,
    request: ExperimentRequest,
    source: dict[str, Any],
) -> bool:
    """Store a transparent derived result without making another model call."""

    if store.contains(request.request_id):
        return False
    if source["request"]["messages"] != [message.to_dict() for message in request.messages]:
        raise ValueError("cannot reuse a result produced from a different prompt")
    generation_value = source.get("generation")
    generation = (
        Generation(
            text=generation_value["text"],
            finish_reason=generation_value.get("finish_reason"),
            prompt_tokens=generation_value.get("prompt_tokens"),
            completion_tokens=generation_value.get("completion_tokens"),
            latency_seconds=float(generation_value.get("latency_seconds") or 0.0),
            raw_text=generation_value.get("raw_text"),
            provider_metadata={
                **dict(generation_value.get("provider_metadata") or {}),
                "reused_from_request_id": source["request"]["request_id"],
            },
        )
        if generation_value is not None
        else None
    )
    store.append(
        ExperimentResult(
            request=request,
            status=source["status"],
            generation=generation,
            evaluation=source.get("evaluation"),
            attempts=0,
            error=source.get("error"),
            started_at=source["started_at"],
            completed_at=source["completed_at"],
        )
    )
    return True
