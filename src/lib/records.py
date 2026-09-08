"""Stable request and response records used by the resumable runner."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any, Literal

Role = Literal["system", "user", "assistant"]


@dataclass(frozen=True, slots=True)
class Message:
    role: Role
    content: str

    def to_dict(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass(frozen=True, slots=True)
class ExperimentRequest:
    experiment: str
    condition: str
    model: str
    messages: tuple[Message, ...]
    puzzle_id: str | None = None
    input_alphabet: str | None = None
    output_alphabet: str | None = None
    expected_solution: str | None = None
    puzzle: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def request_id(self) -> str:
        payload = self.to_dict(include_request_id=False)
        digest = hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()[:20]
        parts = [self.experiment, self.model, self.puzzle_id or "control", digest]
        return ":".join(parts)

    def to_dict(self, *, include_request_id: bool = True) -> dict[str, Any]:
        value = asdict(self)
        value["messages"] = [message.to_dict() for message in self.messages]
        if include_request_id:
            value["request_id"] = self.request_id
        return value


@dataclass(frozen=True, slots=True)
class Generation:
    text: str
    finish_reason: str | None
    prompt_tokens: int | None
    completion_tokens: int | None
    latency_seconds: float
    provider_metadata: dict[str, Any] = field(default_factory=dict)
    raw_text: str | None = None


@dataclass(frozen=True, slots=True)
class ExperimentResult:
    request: ExperimentRequest
    status: Literal["OK", "API_ERROR", "TIMEOUT"]
    generation: Generation | None
    evaluation: dict[str, Any] | None
    attempts: int
    error: str | None
    started_at: str
    completed_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "request": self.request.to_dict(),
            "status": self.status,
            "generation": asdict(self.generation) if self.generation else None,
            "evaluation": self.evaluation,
            "attempts": self.attempts,
            "error": self.error,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }


def shard_for(request_id: str, shard_count: int) -> int:
    if shard_count < 1:
        raise ValueError("shard_count must be positive")
    digest = hashlib.sha256(request_id.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") % shard_count


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
