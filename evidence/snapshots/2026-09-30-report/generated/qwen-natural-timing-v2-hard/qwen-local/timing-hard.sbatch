#!/bin/bash
#SBATCH --partition=gpu_h200_8
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=192G
#SBATCH --time=0-01:00
#SBATCH --job-name=sdk-qwen-local-timing-hard
#SBATCH --output=/scratch/kudhru/arnavbharti/src/slurm/generated/qwen-natural-timing-v2-hard/qwen-local/logs/sdk-qwen-local-timing-hard-%j.out
#SBATCH --error=/scratch/kudhru/arnavbharti/src/slurm/generated/qwen-natural-timing-v2-hard/qwen-local/logs/sdk-qwen-local-timing-hard-%j.err
#SBATCH --gres=gpu:1

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
srun python3 diagnose_timing.py hard --config /scratch/kudhru/arnavbharti/src/config/stronger-model-diagnostic.json --execute
