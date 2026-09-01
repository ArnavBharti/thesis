"""Create and submit one readable Sharanga job script at a time."""

from __future__ import annotations

import shlex
import subprocess
from pathlib import Path
from typing import Iterable

from .config import ExperimentConfig, ModelConfig, SlurmResources

ROOT = Path(__file__).resolve().parents[1]


def qualification_job(
    config_path: Path,
    config: ExperimentConfig,
    model: ModelConfig,
) -> Path:
    command = _runner(config_path, model, "--experiments", "qualification")
    return _write_job(config, model, "qualification", model.slurm, [command])


def experiment_job(
    config_path: Path,
    config: ExperimentConfig,
    model: ModelConfig,
    experiment: str,
    part: int,
) -> Path:
    parts = config.shard_count(experiment)
    if not 1 <= part <= parts:
        raise ValueError(f"part must be between 1 and {parts}")
    command = _runner(
        config_path,
        model,
        "--experiments",
        experiment,
        "--shard-index",
        str(part - 1),
        "--shard-count",
        str(parts),
    )
    name = f"{experiment}-part-{part:03d}-of-{parts:03d}"
    return _write_job(config, model, name, model.slurm, [command])


def finalization_job(
    config_path: Path,
    config: ExperimentConfig,
    model: ModelConfig,
) -> Path:
    resources = SlurmResources(
        partition="compute",
        gpus=0,
        cpus=2,
        memory="16G",
        time_limit="0-02:00",
    )
    commands = [
        _runner(config_path, model, "--action", "token-registry"),
        _runner(config_path, model, "--action", "analyze"),
    ]
    return _write_job(config, model, "finalize", resources, commands)


def submit_job(path: Path, *, test_only: bool = False) -> str:
    command = ["sbatch", "--test-only" if test_only else "--parsable", str(path)]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    except FileNotFoundError as error:
        raise SystemExit("sbatch is not available. Run this command on Sharanga.") from error
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or error.stdout).strip()
        raise SystemExit(f"Slurm rejected the job: {detail}") from error
    return result.stdout.strip().split(";", 1)[0]


def _runner(config_path: Path, model: ModelConfig, *arguments: str) -> list[str]:
    return [
        "python3",
        "run_experiments.py",
        "--config",
        str(config_path.resolve()),
        "--model",
        model.name,
        *arguments,
    ]


def _write_job(
    config: ExperimentConfig,
    model: ModelConfig,
    step_name: str,
    resources: SlurmResources,
    commands: list[list[str]],
) -> Path:
    directory = ROOT / "slurm" / "generated" / config.run_id / model.name
    logs = directory / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    path = directory / f"{step_name}.sbatch"
    job_name = _safe_name(f"sdk-{model.name}-{step_name}")

    lines = [
        "#!/bin/bash",
        f"#SBATCH --partition={resources.partition}",
        "#SBATCH --nodes=1",
        "#SBATCH --ntasks=1",
        f"#SBATCH --cpus-per-task={resources.cpus}",
        f"#SBATCH --mem={resources.memory}",
        f"#SBATCH --time={resources.time_limit}",
        f"#SBATCH --job-name={job_name}",
        f"#SBATCH --output={logs / (job_name + '-%j.out')}",
        f"#SBATCH --error={logs / (job_name + '-%j.err')}",
    ]
    if resources.gpus:
        lines.append(f"#SBATCH --gres=gpu:{resources.gpus}")
    if resources.nodelist:
        lines.append(f"#SBATCH --nodelist={resources.nodelist}")

    lines.extend(["", "set -euo pipefail"])
    for module in resources.modules:
        lines.append(f"module load {shlex.quote(module)}")
    activate = ROOT / ".venv" / "bin" / "activate"
    lines.extend(
        [
            f"cd {shlex.quote(str(ROOT))}",
            f"source {shlex.quote(str(activate))}",
            "export TOKENIZERS_PARALLELISM=false",
        ]
    )
    lines.extend("srun " + _shell_join(command) for command in commands)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return path


def _shell_join(arguments: Iterable[str]) -> str:
    return " ".join(shlex.quote(value) for value in arguments)


def _safe_name(value: str) -> str:
    clean = "".join(character if character.isalnum() else "-" for character in value)
    return clean.strip("-")[:100]
