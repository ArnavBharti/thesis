#!/bin/bash
#SBATCH --partition=gpu_h200_8
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=256G
#SBATCH --time=0-00:30
#SBATCH --job-name=sdk-mistral-small-4-local-very-easy-diagnostic
#SBATCH --output=/scratch/kudhru/arnavbharti/src/slurm/generated/configuration-diagnostic-v1-very-easy-mistral-small-4-local/mistral-small-4-local/logs/sdk-mistral-small-4-local-very-easy-diagnostic-%j.out
#SBATCH --error=/scratch/kudhru/arnavbharti/src/slurm/generated/configuration-diagnostic-v1-very-easy-mistral-small-4-local/mistral-small-4-local/logs/sdk-mistral-small-4-local-very-easy-diagnostic-%j.err
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
NVCC_PATH="$(find "$VIRTUAL_ENV/lib" -path '*/site-packages/nvidia/cu*/bin/nvcc' -type f -perm -u+x -print -quit)"
if [[ -n "$NVCC_PATH" ]]; then
    export PATH="$(dirname "$NVCC_PATH"):$PATH"
    export CUDA_HOME="$(dirname "$(dirname "$NVCC_PATH")")"
    export CUDACXX="$NVCC_PATH"
fi
export VLLM_USE_FLASHINFER_SAMPLER=0
export TOKENIZERS_PARALLELISM=false
srun python3 diagnose_very_easy.py mistral-small-4-local --config /scratch/kudhru/arnavbharti/src/config/experiments.json --execute
