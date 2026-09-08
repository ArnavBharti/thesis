"""Resumable request execution, retry handling, and revision workflows."""

from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping, Sequence

from .models import BackendError, BackendTimeout, InferenceBackend
from .config import RetryConfig
from .evaluation import checker_feedback, evaluate_generation
from .prompts import revision_prompt
from .records import ExperimentRequest, ExperimentResult, Generation, Message, shard_for
from .results import ResultStore


@dataclass(frozen=True, slots=True)
class ExecutionSummary:
    eligible: int
    completed_before_run: int
    executed: int
    correct: int
    incorrect: int
    not_evaluated: int


class ExperimentExecutor:
    def __init__(
        self,
        backend: InferenceBackend,
        store: ResultStore,
        retry: RetryConfig,
        *,
        shard_index: int = 0,
        shard_count: int = 1,
    ) -> None:
        if not 0 <= shard_index < shard_count:
            raise ValueError("shard_index must be in [0, shard_count)")
        self.backend = backend
        self.store = store
        self.retry = retry
        self.shard_index = shard_index
        self.shard_count = shard_count

    def run(
        self,
        requests: Iterable[ExperimentRequest],
        *,
        maximum_requests: int | None = None,
        initial_results: Mapping[str, dict[str, Any]] | None = None,
    ) -> ExecutionSummary:
        eligible = completed = executed = correct = incorrect = not_evaluated = 0
        for request in requests:
            if shard_for(request.request_id, self.shard_count) != self.shard_index:
                continue
            eligible += 1
            if self.store.contains(request.request_id):
                completed += 1
                continue
            if maximum_requests is not None and executed >= maximum_requests:
                continue
            initial = (initial_results or {}).get(request.request_id)
            result = self._execute(request, initial)
            self.store.append(result)
            executed += 1
            outcome = (result.evaluation or {}).get("outcome")
            if outcome == "CORRECT":
                correct += 1
            elif outcome == "NOT_EVALUATED":
                not_evaluated += 1
            else:
                incorrect += 1
        return ExecutionSummary(eligible, completed, executed, correct, incorrect, not_evaluated)

    def _execute(
        self,
        request: ExperimentRequest,
        initial_result: dict[str, Any] | None = None,
    ) -> ExperimentResult:
        started = datetime.now(timezone.utc).isoformat()
        if request.experiment == "exp10":
            return self._execute_revision(request, started, initial_result)
        if initial_result is not None:
            raise ValueError("reused initial results are only valid for Experiment 10")
        generation, status, attempts, error = self._generate(request.messages)
        evaluation = evaluate_generation(
            request,
            generation,
            operational_result=status if status != "OK" else None,
        )
        return ExperimentResult(
            request=request,
            status=status,
            generation=generation,
            evaluation=evaluation,
            attempts=attempts,
            error=error,
            started_at=started,
            completed_at=datetime.now(timezone.utc).isoformat(),
        )

    def _execute_revision(
        self,
        request: ExperimentRequest,
        started: str,
        initial_result: dict[str, Any] | None,
    ) -> ExperimentResult:
        condition = str(request.metadata["revision_condition"])
        messages = list(request.messages)
        stages: list[dict[str, object]] = []
        total_attempts = 0

        if initial_result is None:
            generation, status, attempts, error = self._generate(messages)
            total_attempts += attempts
            evaluation = evaluate_generation(
                request,
                generation,
                operational_result=status if status != "OK" else None,
            )
            initial_called = True
        else:
            source_messages = initial_result["request"]["messages"]
            if source_messages != [message.to_dict() for message in request.messages]:
                raise ValueError("reused Experiment 10 baseline has a different prompt")
            generation = _generation_from_value(initial_result.get("generation"))
            status = str(initial_result["status"])
            error = initial_result.get("error")
            evaluation = dict(initial_result.get("evaluation") or {})
            initial_called = False
        stages.append(
            {
                "stage": "initial",
                "model_called": initial_called,
                "generation": _generation_dict(generation),
                "evaluation": evaluation,
            }
        )

        revisions = 0
        checker_guided = condition == "checker_guided_revision"
        if condition == "one_self_revision":
            revisions = 1
        elif condition == "two_self_revisions":
            revisions = 2
        elif checker_guided and evaluation["outcome"] != "CORRECT":
            revisions = 1

        for revision_index in range(revisions):
            if generation is None or status != "OK":
                break
            feedback = checker_feedback(evaluation) if checker_guided else None
            messages.extend(
                (
                    Message("assistant", generation.text),
                    Message("user", revision_prompt(checker_feedback=feedback)),
                )
            )
            generation, status, attempts, error = self._generate(messages)
            total_attempts += attempts
            evaluation = evaluate_generation(
                request,
                generation,
                operational_result=status if status != "OK" else None,
            )
            stages.append(
                {
                    "stage": f"revision_{revision_index + 1}",
                    "model_called": True,
                    "generation": _generation_dict(generation),
                    "evaluation": evaluation,
                }
            )

        evaluation = dict(evaluation)
        evaluation["stages"] = stages
        return ExperimentResult(
            request=request,
            status=status,
            generation=generation,
            evaluation=evaluation,
            attempts=total_attempts,
            error=error,
            started_at=started,
            completed_at=datetime.now(timezone.utc).isoformat(),
        )

    def _generate(
        self,
        messages: Sequence[Message],
    ) -> tuple[Generation | None, str, int, str | None]:
        delay = self.retry.initial_delay_seconds
        last_error: str | None = None
        last_status = "API_ERROR"
        for attempt in range(1, self.retry.attempts + 1):
            try:
                return self.backend.generate(messages), "OK", attempt, None
            except BackendTimeout as error:
                last_status = "TIMEOUT"
                last_error = str(error)
            except BackendError as error:
                last_status = "API_ERROR"
                last_error = str(error)
            if attempt < self.retry.attempts and delay:
                time.sleep(delay)
                delay = min(delay * 2, self.retry.maximum_delay_seconds)
        return None, last_status, self.retry.attempts, last_error


def _generation_dict(generation: Generation | None) -> dict[str, object] | None:
    if generation is None:
        return None
    return {
        "text": generation.text,
        "finish_reason": generation.finish_reason,
        "prompt_tokens": generation.prompt_tokens,
        "completion_tokens": generation.completion_tokens,
        "latency_seconds": generation.latency_seconds,
        "provider_metadata": generation.provider_metadata,
    }


def _generation_from_value(value: dict[str, Any] | None) -> Generation | None:
    if value is None:
        return None
    return Generation(
        text=value["text"],
        finish_reason=value.get("finish_reason"),
        prompt_tokens=value.get("prompt_tokens"),
        completion_tokens=value.get("completion_tokens"),
        latency_seconds=float(value.get("latency_seconds") or 0.0),
        provider_metadata=dict(value.get("provider_metadata") or {}),
    )
