"""Seed-fixed stratified selection and deterministic permutations."""

from __future__ import annotations

import hashlib
import random
from collections import defaultdict
from typing import Iterable, TypeVar

from sudoku.schema import PuzzleRecord

T = TypeVar("T")


def select_stratified(
    records: Iterable[PuzzleRecord],
    per_tier: int,
    *,
    seed: int,
    namespace: str,
) -> tuple[PuzzleRecord, ...]:
    if per_tier < 1:
        raise ValueError("per_tier must be positive")
    groups: dict[str, list[PuzzleRecord]] = defaultdict(list)
    for record in records:
        groups[record.difficulty].append(record)
    selected: list[PuzzleRecord] = []
    for tier in ("easy", "medium", "hard"):
        available = groups[tier]
        if len(available) < per_tier:
            raise ValueError(f"requested {per_tier} {tier} puzzles but only {len(available)} exist")
        ranked = sorted(
            available,
            key=lambda record: _rank(seed, namespace, tier, record.puzzle_id),
        )
        selected.extend(ranked[:per_tier])
    return tuple(selected)


def deterministic_permutation(values: Iterable[T], *, seed: int, namespace: str) -> tuple[T, ...]:
    result = list(values)
    rng = random.Random(_seed(seed, namespace))
    rng.shuffle(result)
    return tuple(result)


def derived_seed(seed: int, namespace: str) -> int:
    return _seed(seed, namespace)


def _rank(seed: int, namespace: str, *parts: str) -> bytes:
    text = ":".join((str(seed), namespace, *parts))
    return hashlib.sha256(text.encode("utf-8")).digest()


def _seed(seed: int, namespace: str) -> int:
    return int.from_bytes(_rank(seed, namespace)[:8], "big")
