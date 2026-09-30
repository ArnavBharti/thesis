#!/bin/bash
#SBATCH --partition=gpu_h100_4
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=256G
#SBATCH --time=0-23:30
#SBATCH --job-name=sdk-glm-flash-local-qualification
#SBATCH --output=/scratch/kudhru/arnavbharti/src/slurm/generated/thesis-confirmatory-lean-v5/glm-flash-local/logs/sdk-glm-flash-local-qualification-%j.out
#SBATCH --error=/scratch/kudhru/arnavbharti/src/slurm/generated/thesis-confirmatory-lean-v5/glm-flash-local/logs/sdk-glm-flash-local-qualification-%j.err
#SBATCH --gres=gpu:2

set -euo pipefail
cd /scratch/kudhru/arnavbharti/src
source /scratch/kudhru/arnavbharti/src/.venv/bin/activate
export HF_HOME=/scratch/kudhru/arnavbharti/huggingface
export XDG_CACHE_HOME=/scratch/kudhru/arnavbharti/cache
export VLLM_CACHE_ROOT=/scratch/kudhru/arnavbharti/cache/vllm
export TORCHINDUCTOR_CACHE_DIR=/scratch/kudhru/arnavbharti/cache/torchinductor
export TRITON_CACHE_DIR=/scratch/kudhru/arnavbharti/cache/triton
export FLASHINFER_WORKSPACE_BASE=/scratch/kudhru/arnavbharti/cache
mkdir -p "$HF_HOME" "$VLLM_CACHE_ROOT" "$TORCHINDUCTOR_CACHE_DIR" "$TRITON_CACHE_DIR"
FLASHINFER_FD_EXCHANGE="$(find "$VIRTUAL_ENV/lib" -path '*/site-packages/flashinfer/comm/fd_exchange.py' -print -quit)"
if [[ -n "$FLASHINFER_FD_EXCHANGE" ]] && ! grep -q "^from __future__ import annotations$" "$FLASHINFER_FD_EXCHANGE"; then
    sed -i '1i from __future__ import annotations' "$FLASHINFER_FD_EXCHANGE"
fi
NVCC_PATH="$(find "$VIRTUAL_ENV/lib" -path '*/site-packages/nvidia/cu*/bin/nvcc' -type f -perm -u+x -print -quit)"
if [[ -n "$NVCC_PATH" ]]; then
    export PATH="$(dirname "$NVCC_PATH"):$PATH"
    export CUDA_HOME="$(dirname "$(dirname "$NVCC_PATH")")"
    export CUDACXX="$NVCC_PATH"
fi
export VLLM_USE_FLASHINFER_SAMPLER=0
export TOKENIZERS_PARALLELISM=false
srun python3 04_qualify_model.py glm-flash-local --config /scratch/kudhru/arnavbharti/src/config/experiments.json --execute
