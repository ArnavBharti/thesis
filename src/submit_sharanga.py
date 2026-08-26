#!/usr/bin/env python3
"""Generate, inspect, or submit resumable Sharanga Slurm experiment jobs."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from experiments.config import ExperimentConfig, ModelConfig, SlurmResources, load_config
from experiments.storage import iter_result_values

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "config" / "experiments.json"
MAIN_EXPERIMENTS = "exp2,exp4,exp6,exp7,exp8,exp9,exp10"


@dataclass(frozen=True, slots=True)
class CompletionState:
    qualification: bool
    main: bool
    finalize: bool
    actual_counts: dict[str, int]
    expected_counts: dict[str, int | None]

    @property
    def complete(self) -> bool:
        return self.qualification and self.main and self.finalize


@dataclass(frozen=True, slots=True)
class JobFiles:
    qualification: Path
    main: Path
    finalize: Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--action", choices=("generate", "status", "test", "submit"), default="generate")
    parser.add_argument("--model", action="append", help="model name; repeat to select several")
    parser.add_argument("--jobs-dir", type=Path, help="generated scripts and logs directory")
    parser.add_argument("--venv", type=Path, default=Path(".venv"), help="virtual environment relative to src")
    parser.add_argument("--python", default="python3", help="Python executable after environment activation")
    parser.add_argument("--force", action="store_true", help="submit phases even when completion markers exist")
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    config = load_config(arguments.config)
    models = _selected_models(config, arguments.model)
    jobs_directory = (arguments.jobs_dir or ROOT / "slurm" / "generated" / config.run_id).resolve()
    jobs_directory.mkdir(parents=True, exist_ok=True)
    (jobs_directory / "logs").mkdir(exist_ok=True)

    failed = False
    for model in models:
        state = completion_state(config, model)
        if arguments.action == "status":
            print(_status_json(model, state))
            failed |= not state.complete
            continue
        files = write_job_files(
            config,
            model,
            jobs_directory,
            venv=arguments.venv,
            python=arguments.python,
            config_path=arguments.config.resolve(),
        )
        if arguments.action == "generate":
            print(json.dumps({"model": model.name, "status": "generated", "jobs": _job_paths(files)}, sort_keys=True))
        elif arguments.action == "test":
            for phase, path in _job_items(files):
                _sbatch(path, test_only=True)
                print(json.dumps({"model": model.name, "phase": phase, "status": "accepted_by_slurm"}, sort_keys=True))
        else:
            _submit_model(model, files, state, force=arguments.force)
    return 1 if failed else 0


def completion_state(config: ExperimentConfig, model: ModelConfig) -> CompletionState:
    directory = config.output_directory / config.run_id / model.name
    qualification = _qualification_passed(directory)
    expected = _expected_counts(directory)
    actual = _actual_counts(directory)
    required = ("exp2", "exp4", "exp6", "exp7", "exp8", "exp9", "exp10")
    main = qualification and bool(expected) and all(
        _experiment_complete(name, expected.get(name), actual.get(name, 0), directory)
        for name in required
    )
    finalize = main and (directory / "exp3" / "representation-registry.jsonl").exists() and (
        directory / "analysis" / "summary.json"
    ).exists()
    return CompletionState(qualification, main, finalize, actual, expected)


def write_job_files(
    config: ExperimentConfig,
    model: ModelConfig,
    jobs_directory: Path,
    *,
    venv: Path,
    python: str,
    config_path: Path = DEFAULT_CONFIG,
) -> JobFiles:
    prefix = _safe_name(model.name)
    files = JobFiles(
        qualification=jobs_directory / f"{prefix}-qualification.sbatch",
        main=jobs_directory / f"{prefix}-main.sbatch",
        finalize=jobs_directory / f"{prefix}-finalize.sbatch",
    )
    common = ["--config", str(config_path), "--model", model.name]
    _write_script(
        files.qualification,
        resources=model.slurm,
        job_name=f"sdk-{prefix}-qual",
        command=[python, "run_experiments.py", *common, "--experiments", "qualification"],
        venv=venv,
    )
    shards = model.slurm.shards or config.slurm_shards
    array = f"0-{shards - 1}"
    if model.slurm.max_concurrent:
        array += f"%{model.slurm.max_concurrent}"
    _write_script(
        files.main,
        resources=model.slurm,
        job_name=f"sdk-{prefix}-main",
        command=[
            python,
            "run_experiments.py",
            *common,
            "--experiments",
            MAIN_EXPERIMENTS,
            "--shard-index",
            "${SLURM_ARRAY_TASK_ID}",
            "--shard-count",
            str(shards),
        ],
        venv=venv,
        array=array,
    )
    finalize_resources = SlurmResources(
        partition="compute",
        gpus=0,
        cpus=2,
        memory="16G",
        time_limit="0-02:00",
    )
    finalize_commands = [
        [python, "run_experiments.py", *common, "--action", "token-registry"],
        [python, "run_experiments.py", *common, "--action", "analyze"],
    ]
    _write_script(
        files.finalize,
        resources=finalize_resources,
        job_name=f"sdk-{prefix}-final",
        command=finalize_commands,
        venv=venv,
    )
    return files


def _write_script(
    path: Path,
    *,
    resources: SlurmResources,
    job_name: str,
    command: list[str] | list[list[str]],
    venv: Path,
    array: str | None = None,
) -> None:
    log_suffix = "%A_%a" if array else "%j"
    lines = [
        "#!/bin/bash",
        f"#SBATCH --partition={resources.partition}",
        "#SBATCH --nodes=1",
        "#SBATCH --ntasks=1",
        f"#SBATCH --cpus-per-task={resources.cpus}",
        f"#SBATCH --mem={resources.memory}",
        f"#SBATCH --time={resources.time_limit}",
        f"#SBATCH --job-name={job_name}",
        f"#SBATCH --output={path.parent / 'logs' / (job_name + '-' + log_suffix + '.out')}",
        f"#SBATCH --error={path.parent / 'logs' / (job_name + '-' + log_suffix + '.err')}",
    ]
    if resources.gpus:
        lines.append(f"#SBATCH --gres=gpu:{resources.gpus}")
    if resources.nodelist:
        lines.append(f"#SBATCH --nodelist={resources.nodelist}")
    if array:
        lines.append(f"#SBATCH --array={array}")
    lines.extend(["", "set -euo pipefail", f"cd {shlex.quote(str(ROOT))}"])
    activate = venv if venv.is_absolute() else ROOT / venv
    lines.extend(
        [
            f"if [[ ! -f {shlex.quote(str(activate / 'bin' / 'activate'))} ]]; then",
            f"  echo {shlex.quote('missing virtual environment: ' + str(activate))} >&2",
            "  exit 2",
            "fi",
            f"source {shlex.quote(str(activate / 'bin' / 'activate'))}",
            "export TOKENIZERS_PARALLELISM=false",
        ]
    )
    for module in resources.modules:
        lines.append(f"module load {shlex.quote(module)}")
    commands = command if command and isinstance(command[0], list) else [command]
    for value in commands:
        lines.append("srun " + _shell_join(value))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def _shell_join(arguments: Iterable[str]) -> str:
    return " ".join(value if value == "${SLURM_ARRAY_TASK_ID}" else shlex.quote(value) for value in arguments)


def _submit_model(model: ModelConfig, files: JobFiles, state: CompletionState, *, force: bool) -> None:
    if state.complete and not force:
        print(json.dumps({"model": model.name, "status": "already_complete"}, sort_keys=True))
        return
    qualification_job: str | None = None
    main_job: str | None = None
    if not state.qualification or force:
        qualification_job = _sbatch(files.qualification)
        print(json.dumps({"model": model.name, "phase": "qualification", "job_id": qualification_job}, sort_keys=True))
    if not state.main or force:
        main_job = _sbatch(files.main, dependency=qualification_job)
        print(json.dumps({"model": model.name, "phase": "main", "job_id": main_job}, sort_keys=True))
    if not state.finalize or force:
        finalize_job = _sbatch(files.finalize, dependency=main_job)
        print(json.dumps({"model": model.name, "phase": "finalize", "job_id": finalize_job}, sort_keys=True))


def _sbatch(path: Path, *, dependency: str | None = None, test_only: bool = False) -> str:
    command = ["sbatch"]
    if test_only:
        command.append("--test-only")
    else:
        command.append("--parsable")
    if dependency:
        command.extend(["--dependency", f"afterok:{dependency}"])
    command.append(str(path))
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except FileNotFoundError as error:
        raise SystemExit("sbatch is unavailable; generate jobs locally and submit them on Sharanga") from error
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or error.stdout).strip()
        raise SystemExit(f"sbatch rejected {path}: {detail}") from error
    return result.stdout.strip().split(";", 1)[0]


def _qualification_passed(directory: Path) -> bool:
    path = directory / "qualification-status.json"
    try:
        return bool(json.loads(path.read_text(encoding="utf-8")).get("passed"))
    except (OSError, json.JSONDecodeError, AttributeError):
        return False


def _expected_counts(directory: Path) -> dict[str, int | None]:
    path = directory / "protocol-manifest.json"
    try:
        experiments = json.loads(path.read_text(encoding="utf-8"))["experiments"]
        return {name: value.get("request_count") for name, value in experiments.items()}
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        return {}


def _actual_counts(directory: Path) -> dict[str, int]:
    paths = tuple(directory.glob("*/shard-*.jsonl"))
    counts: dict[str, int] = {}
    seen: set[str] = set()
    for value in iter_result_values(paths):
        request = value["request"]
        request_id = request["request_id"]
        if request_id in seen:
            raise ValueError(f"duplicate request ID across result shards: {request_id}")
        seen.add(request_id)
        experiment = request["experiment"]
        counts[experiment] = counts.get(experiment, 0) + 1
    return counts


def _experiment_complete(name: str, expected: int | None, actual: int, directory: Path) -> bool:
    if expected is None:
        return name == "exp7" and (directory / "exp7" / "status.json").exists()
    return actual == expected


def _selected_models(config: ExperimentConfig, names: list[str] | None) -> tuple[ModelConfig, ...]:
    if not names:
        return config.enabled_models
    try:
        return tuple(config.model(name) for name in names)
    except KeyError as error:
        raise SystemExit(str(error)) from error


def _safe_name(value: str) -> str:
    return "".join(character if character.isalnum() else "-" for character in value).strip("-")[:48]


def _status_json(model: ModelConfig, state: CompletionState) -> str:
    return json.dumps(
        {
            "model": model.name,
            "complete": state.complete,
            "qualification_complete": state.qualification,
            "main_complete": state.main,
            "finalize_complete": state.finalize,
            "actual_counts": state.actual_counts,
            "expected_counts": state.expected_counts,
        },
        sort_keys=True,
    )


def _job_items(files: JobFiles) -> tuple[tuple[str, Path], ...]:
    return (("qualification", files.qualification), ("main", files.main), ("finalize", files.finalize))


def _job_paths(files: JobFiles) -> dict[str, str]:
    return {name: str(path) for name, path in _job_items(files)}


if __name__ == "__main__":
    raise SystemExit(main())
