#!/bin/bash
#SBATCH --partition=gpu_h100_4
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=192G
#SBATCH --time=0-01:00
#SBATCH --job-name=sdk-gpt-oss-120b-local-exp6-input-output
#SBATCH --output=/scratch/kudhru/arnavbharti/src/slurm/generated/local-models-v1/gpt-oss-120b-local/logs/sdk-gpt-oss-120b-local-exp6-input-output-%j.out
#SBATCH --error=/scratch/kudhru/arnavbharti/src/slurm/generated/local-models-v1/gpt-oss-120b-local/logs/sdk-gpt-oss-120b-local-exp6-input-output-%j.err
#SBATCH --gres=gpu:1

set -euo pipefail
spack load gcc@13.2.0
GCC_LIBRARY_DIR="$(dirname "$(g++ -print-file-name=libstdc++.so.6)")"
export LD_LIBRARY_PATH="$GCC_LIBRARY_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
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
    CUDA_LINK_DIR="$VLLM_CACHE_ROOT/cuda-link"
    mkdir -p "$CUDA_LINK_DIR"
    ln -sfn "$CUDA_HOME/lib/libcudart.so.13" "$CUDA_LINK_DIR/libcudart.so"
    ln -sfn "$CUDA_HOME/lib/libnvrtc.so.13" "$CUDA_LINK_DIR/libnvrtc.so"
    export LIBRARY_PATH="$CUDA_LINK_DIR${LIBRARY_PATH:+:$LIBRARY_PATH}"
    export LD_LIBRARY_PATH="$CUDA_HOME/lib:$LD_LIBRARY_PATH"
fi
export VLLM_USE_FLASHINFER_SAMPLER=0
export VLLM_NO_USAGE_STATS=1
export TOKENIZERS_PARALLELISM=false
srun python3 08_run_input_output_cross.py gpt-oss-120b-local --config /scratch/kudhru/arnavbharti/src/config/local-models.json --execute
