"""Create and freeze deterministic, non-overlapping study samples."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import ExperimentConfig
from .selection import select_stratified
from .sudoku.schema import PuzzleRecord


@dataclass(frozen=True, slots=True)
class SamplePlan:
    dataset_sha256: str
    master_seed: int
    pilot_ids: tuple[str, ...]
    main_ids: tuple[str, ...]
    mechanism_ids: tuple[str, ...]
    ablation_ids: tuple[str, ...]

    def records(self, name: str, all_records: tuple[PuzzleRecord, ...]) -> tuple[PuzzleRecord, ...]:
        ids = set(getattr(self, f"{name}_ids"))
        selected = tuple(record for record in all_records if record.puzzle_id in ids)
        if len(selected) != len(ids):
            raise ValueError(f"sample {name!r} refers to missing puzzle IDs")
        return selected


def sample_plan_path(config: ExperimentConfig) -> Path:
    return config.output_directory / config.run_id / "sample-plan.json"


def build_sample_plan(
    config: ExperimentConfig,
    records: tuple[PuzzleRecord, ...],
) -> SamplePlan:
    pilot = select_stratified(
        records,
        config.pilot_per_tier,
        seed=config.master_seed,
        namespace="pilot",
    )
    pilot_ids = {record.puzzle_id for record in pilot}
    remaining = tuple(record for record in records if record.puzzle_id not in pilot_ids)
    main = select_stratified(
        remaining,
        config.main_per_tier,
        seed=config.master_seed,
        namespace="confirmatory-main",
    )
    mechanism = select_stratified(
        main,
        config.mechanism_per_tier,
        seed=config.master_seed,
        namespace="confirmatory-mechanism",
    )
    ablation = select_stratified(
        mechanism,
        config.ablation_per_tier,
        seed=config.master_seed,
        namespace="confirmatory-ablation",
    )
    return SamplePlan(
        dataset_sha256=_sha256_file(config.dataset_path),
        master_seed=config.master_seed,
        pilot_ids=tuple(record.puzzle_id for record in pilot),
        main_ids=tuple(record.puzzle_id for record in main),
        mechanism_ids=tuple(record.puzzle_id for record in mechanism),
        ablation_ids=tuple(record.puzzle_id for record in ablation),
    )


def freeze_sample_plan(config: ExperimentConfig, plan: SamplePlan) -> Path:
    path = sample_plan_path(config)
    text = json.dumps(asdict(plan), indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_text(encoding="utf-8") != text:
            raise ValueError(f"sample plan differs from the frozen plan at {path}; use a new run_id")
        return path
    temporary = path.with_suffix(".tmp")
    temporary.write_text(text, encoding="utf-8", newline="\n")
    temporary.replace(path)
    return path


def load_sample_plan(config: ExperimentConfig) -> SamplePlan:
    path = sample_plan_path(config)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        plan = SamplePlan(
            dataset_sha256=value["dataset_sha256"],
            master_seed=value["master_seed"],
            pilot_ids=tuple(value["pilot_ids"]),
            main_ids=tuple(value["main_ids"]),
            mechanism_ids=tuple(value["mechanism_ids"]),
            ablation_ids=tuple(value["ablation_ids"]),
        )
    except FileNotFoundError as error:
        raise SystemExit("sample plan is missing; run 06_freeze_protocol.py first") from error
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid sample plan: {path}") from error
    expected = build_sample_plan(config, _read_records(config))
    if plan != expected:
        raise ValueError(f"sample plan no longer matches the configuration: {path}")
    return plan


def _read_records(config: ExperimentConfig) -> tuple[PuzzleRecord, ...]:
    from .sudoku.dataset import read_records

    return read_records(config.dataset_path)


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
