"""Write and submit one readable Sharanga Slurm job at a time."""

from __future__ import annotations

import json
import shlex
import subprocess
from pathlib import Path
from typing import Iterable

from .config import ExperimentConfig, ModelConfig, SlurmResources

ROOT = Path(__file__).resolve().parents[1]


def write_python_job(
    config: ExperimentConfig,
    model: ModelConfig,
    script: Path,
    step_name: str,
    arguments: Iterable[str],
    *,
    resources: SlurmResources | None = None,
) -> Path:
    """Create one job that executes the same numbered Python script."""

    selected_resources = resources or model.slurm
    directory = ROOT / "slurm" / "generated" / config.run_id / model.name
    logs = directory / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    path = directory / f"{step_name}.sbatch"
    job_name = _safe_name(f"sdk-{model.name}-{step_name}")
    command = ["python3", script.name, *arguments, "--execute"]

    lines = [
        "#!/bin/bash",
        f"#SBATCH --partition={selected_resources.partition}",
        "#SBATCH --nodes=1",
        "#SBATCH --ntasks=1",
        f"#SBATCH --cpus-per-task={selected_resources.cpus}",
        f"#SBATCH --mem={selected_resources.memory}",
        f"#SBATCH --time={selected_resources.time_limit}",
        f"#SBATCH --job-name={job_name}",
        f"#SBATCH --output={logs / (job_name + '-%j.out')}",
        f"#SBATCH --error={logs / (job_name + '-%j.err')}",
    ]
    if selected_resources.gpus:
        lines.append(f"#SBATCH --gres=gpu:{selected_resources.gpus}")
    if selected_resources.nodelist:
        lines.append(f"#SBATCH --nodelist={selected_resources.nodelist}")

    lines.extend(("", "set -euo pipefail"))
    for module in selected_resources.modules:
        lines.append(f"module load {shlex.quote(module)}")
    lines.extend(
        (
            f"cd {shlex.quote(str(ROOT))}",
            f"source {shlex.quote(str(ROOT / '.venv' / 'bin' / 'activate'))}",
            f"export HF_HOME={shlex.quote(str(ROOT.parent / 'huggingface'))}",
            f"export XDG_CACHE_HOME={shlex.quote(str(ROOT.parent / 'cache'))}",
            f"export VLLM_CACHE_ROOT={shlex.quote(str(ROOT.parent / 'cache' / 'vllm'))}",
            f"export TORCHINDUCTOR_CACHE_DIR={shlex.quote(str(ROOT.parent / 'cache' / 'torchinductor'))}",
            f"export TRITON_CACHE_DIR={shlex.quote(str(ROOT.parent / 'cache' / 'triton'))}",
            f"export FLASHINFER_WORKSPACE_BASE={shlex.quote(str(ROOT.parent / 'cache'))}",
            'mkdir -p "$HF_HOME" "$VLLM_CACHE_ROOT" "$TORCHINDUCTOR_CACHE_DIR" "$TRITON_CACHE_DIR"',
            'FLASHINFER_FD_EXCHANGE="$(find "$VIRTUAL_ENV/lib" '
            "-path '*/site-packages/flashinfer/comm/fd_exchange.py' -print -quit)\"",
            'if [[ -n "$FLASHINFER_FD_EXCHANGE" ]] && '
            '! grep -q "^from __future__ import annotations$" "$FLASHINFER_FD_EXCHANGE"; then',
            "    sed -i '1i from __future__ import annotations' \"$FLASHINFER_FD_EXCHANGE\"",
            "fi",
            'NVCC_PATH="$(find "$VIRTUAL_ENV/lib" -path \'*/site-packages/nvidia/cu*/bin/nvcc\' '
            '-type f -perm -u+x -print -quit)"',
            'if [[ -n "$NVCC_PATH" ]]; then',
            '    export PATH="$(dirname "$NVCC_PATH"):$PATH"',
            '    export CUDA_HOME="$(dirname "$(dirname "$NVCC_PATH")")"',
            '    export CUDACXX="$NVCC_PATH"',
            "fi",
            "export VLLM_USE_FLASHINFER_SAMPLER=0",
            "export TOKENIZERS_PARALLELISM=false",
            "srun " + _shell_join(command),
        )
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return path


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


def finish_submission(path: Path, *, dry_run: bool, test_only: bool) -> int:
    print(f"Job file: {path}")
    if dry_run:
        print("DRY RUN: the job was not submitted")
        return 0
    if test_only:
        submit_job(path, test_only=True)
        print("Slurm accepted the resources. The job was not submitted.")
        return 0
    previous_job = _previous_job_id(path)
    if previous_job and _job_is_active(previous_job):
        print(f"SKIP: Slurm job {previous_job} is already queued or running")
        return 0
    job_id = submit_job(path)
    _write_submission(path, job_id)
    print(f"Submitted one job: {job_id}")
    return 0


def cpu_resources(*, time_limit: str = "0-02:00") -> SlurmResources:
    return SlurmResources(
        partition="compute",
        gpus=0,
        cpus=2,
        memory="16G",
        time_limit=time_limit,
    )


def _shell_join(arguments: Iterable[str]) -> str:
    return " ".join(shlex.quote(value) for value in arguments)


def _safe_name(value: str) -> str:
    clean = "".join(character if character.isalnum() else "-" for character in value)
    return clean.strip("-")[:100]


def _submission_path(job_path: Path) -> Path:
    return job_path.with_suffix(".submitted.json")


def _previous_job_id(job_path: Path) -> str | None:
    try:
        value = json.loads(_submission_path(job_path).read_text(encoding="utf-8"))
        return str(value["job_id"])
    except (FileNotFoundError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None


def _job_is_active(job_id: str) -> bool:
    try:
        result = subprocess.run(
            ["squeue", "--noheader", "--jobs", job_id, "--format", "%i"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False
    return any(line.strip() == job_id for line in result.stdout.splitlines())


def _write_submission(job_path: Path, job_id: str) -> None:
    path = _submission_path(job_path)
    text = json.dumps({"job_id": job_id}, indent=2, sort_keys=True) + "\n"
    temporary = path.with_suffix(".tmp")
    temporary.write_text(text, encoding="utf-8", newline="\n")
    temporary.replace(path)
