"""End-to-end dataset generation, serialization, and independent auditing."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .certificate import certify
from .difficulty import analyze_difficulty
from .generator import GENERATOR_VERSION, generate_candidate
from .schema import Difficulty, DifficultyCertificate, PuzzleRecord, grid_from_compact
from .solver import count_solutions, solve

SCHEMA_VERSION = "1.0.0"
TIERS: tuple[Difficulty, ...] = ("easy", "medium", "hard")
TIER_PREFIX: dict[Difficulty, str] = {"easy": "E", "medium": "M", "hard": "H"}
TIER_SEED_OFFSETS: dict[Difficulty, int] = {
    "easy": 0,
    "medium": 1_000_000_000,
    "hard": 2_000_000_000,
}


@dataclass(frozen=True, slots=True)
class DatasetConfig:
    master_seed: int = 20260826
    puzzles_per_tier: int = 100

    def __post_init__(self) -> None:
        if self.master_seed < 0:
            raise ValueError("master seed must be non-negative")
        if self.puzzles_per_tier < 1:
            raise ValueError("puzzles per tier must be positive")


@dataclass(frozen=True, slots=True)
class GenerationResult:
    records: tuple[PuzzleRecord, ...]
    report: dict[str, Any]


def generate_dataset(config: DatasetConfig = DatasetConfig()) -> GenerationResult:
    records: list[PuzzleRecord] = []
    seen_hashes: set[str] = set()
    report_tiers: dict[str, Any] = {}

    for tier in TIERS:
        next_seed = config.master_seed + TIER_SEED_OFFSETS[tier]
        examined = 0
        rejected_difficulty: Counter[str] = Counter()
        duplicate_count = 0
        tier_records: list[PuzzleRecord] = []

        while len(tier_records) < config.puzzles_per_tier:
            candidate = generate_candidate(next_seed, tier)
            next_seed += 1
            examined += 1
            if candidate.analysis.difficulty != tier:
                rejected_difficulty[candidate.analysis.difficulty] += 1
                continue

            puzzle_id = f"{TIER_PREFIX[tier]}{len(tier_records) + 1:03d}"
            record = certify(candidate, puzzle_id, tier)
            if record.puzzle_sha256 in seen_hashes:
                duplicate_count += 1
                continue
            seen_hashes.add(record.puzzle_sha256)
            tier_records.append(record)

        records.extend(tier_records)
        report_tiers[tier] = {
            "accepted": len(tier_records),
            "candidates_examined": examined,
            "duplicate_puzzles_rejected": duplicate_count,
            "difficulty_rejections": dict(sorted(rejected_difficulty.items())),
            "first_seed": tier_records[0].seed,
            "last_seed": tier_records[-1].seed,
        }

    report = {
        "schema_version": SCHEMA_VERSION,
        "generator_version": GENERATOR_VERSION,
        "master_seed": config.master_seed,
        "puzzles_per_tier": config.puzzles_per_tier,
        "total_puzzles": len(records),
        "tiers": report_tiers,
    }
    return GenerationResult(tuple(records), report)


def write_dataset(result: GenerationResult, output_directory: Path) -> dict[str, Any]:
    output_directory.mkdir(parents=True, exist_ok=True)
    dataset_path = output_directory / "puzzles.jsonl"
    report_path = output_directory / "generation-report.json"
    manifest_path = output_directory / "manifest.json"

    dataset_text = "".join(_json_line(record.to_dict()) for record in result.records)
    report_text = _pretty_json(result.report)
    dataset_path.write_text(dataset_text, encoding="utf-8", newline="\n")
    report_path.write_text(report_text, encoding="utf-8", newline="\n")

    counts = Counter(record.difficulty for record in result.records)
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "generator_version": GENERATOR_VERSION,
        "master_seed": result.report["master_seed"],
        "record_count": len(result.records),
        "difficulty_counts": {tier: counts[tier] for tier in TIERS},
        "files": {
            dataset_path.name: _sha256_text(dataset_text),
            report_path.name: _sha256_text(report_text),
        },
    }
    manifest_path.write_text(_pretty_json(manifest), encoding="utf-8", newline="\n")
    return manifest


def read_records(dataset_path: Path) -> tuple[PuzzleRecord, ...]:
    records: list[PuzzleRecord] = []
    with dataset_path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
                certificate = DifficultyCertificate(
                    deduction_steps=value["difficulty_certificate"]["deduction_steps"],
                    techniques=tuple(value["difficulty_certificate"]["techniques"]),
                    backtracking_required=value["difficulty_certificate"]["backtracking_required"],
                    maximum_search_depth=value["difficulty_certificate"]["maximum_search_depth"],
                    search_nodes=value["difficulty_certificate"]["search_nodes"],
                )
                records.append(
                    PuzzleRecord(
                        puzzle_id=value["puzzle_id"],
                        difficulty=value["difficulty"],
                        puzzle=value["puzzle"],
                        solution=value["solution"],
                        clue_mask=value["clue_mask"],
                        clue_count=value["clue_count"],
                        seed=value["seed"],
                        generator_version=value["generator_version"],
                        solver_certificate=value["solver_certificate"],
                        difficulty_certificate=certificate,
                        puzzle_sha256=value["puzzle_sha256"],
                    )
                )
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
                raise ValueError(f"invalid record on line {line_number}: {error}") from error
    return tuple(records)


def audit_records(records: Iterable[PuzzleRecord]) -> dict[str, Any]:
    records = tuple(records)
    errors: list[str] = []
    counts: Counter[str] = Counter()
    ids: set[str] = set()
    hashes: set[str] = set()

    for record in records:
        counts[record.difficulty] += 1
        if record.puzzle_id in ids:
            errors.append(f"{record.puzzle_id}: duplicate puzzle ID")
        ids.add(record.puzzle_id)
        if record.puzzle_sha256 in hashes:
            errors.append(f"{record.puzzle_id}: duplicate puzzle hash")
        hashes.add(record.puzzle_sha256)

        try:
            record.validate()
            puzzle = grid_from_compact(record.puzzle)
            stored_solution = grid_from_compact(record.solution)
            expected_hash = hashlib.sha256(record.puzzle.encode("ascii")).hexdigest()
            if expected_hash != record.puzzle_sha256:
                errors.append(f"{record.puzzle_id}: puzzle hash mismatch")
            if count_solutions(puzzle, limit=2) != 1:
                errors.append(f"{record.puzzle_id}: puzzle is not uniquely solvable")
            if solve(puzzle) != stored_solution:
                errors.append(f"{record.puzzle_id}: independently solved grid does not match")
            analysis = analyze_difficulty(puzzle)
            if analysis.difficulty != record.difficulty:
                errors.append(
                    f"{record.puzzle_id}: difficulty is {analysis.difficulty}, "
                    f"not {record.difficulty}"
                )
            if analysis.certificate != record.difficulty_certificate:
                errors.append(f"{record.puzzle_id}: difficulty certificate mismatch")
        except ValueError as error:
            errors.append(f"{record.puzzle_id}: {error}")

    return {
        "valid": not errors,
        "record_count": len(records),
        "difficulty_counts": {tier: counts[tier] for tier in TIERS},
        "errors": errors,
    }


def audit_directory(output_directory: Path) -> dict[str, Any]:
    dataset_path = output_directory / "puzzles.jsonl"
    report_path = output_directory / "generation-report.json"
    manifest_path = output_directory / "manifest.json"
    records = read_records(dataset_path)
    audit = audit_records(records)

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        expected_dataset_hash = _sha256_text(dataset_path.read_text(encoding="utf-8"))
        expected_report_hash = _sha256_text(report_path.read_text(encoding="utf-8"))
        if manifest["files"][dataset_path.name] != expected_dataset_hash:
            audit["errors"].append("manifest hash mismatch for puzzles.jsonl")
        if manifest["files"][report_path.name] != expected_report_hash:
            audit["errors"].append("manifest hash mismatch for generation-report.json")
        if manifest["record_count"] != len(records):
            audit["errors"].append("manifest record count mismatch")
    except (FileNotFoundError, KeyError, TypeError, json.JSONDecodeError) as error:
        audit["errors"].append(f"invalid manifest: {error}")
    audit["valid"] = not audit["errors"]
    return audit


def _json_line(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def _pretty_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
