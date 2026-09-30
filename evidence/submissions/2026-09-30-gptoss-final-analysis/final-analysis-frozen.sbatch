#!/bin/bash
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=0-02:00
#SBATCH --job-name=sdk-gpt-oss-120b-local-final-analysis-frozen
#SBATCH --output=/scratch/kudhru/arnavbharti/src/slurm/generated/local-models-v1/gpt-oss-120b-local/logs/sdk-gpt-oss-120b-local-final-analysis-frozen-%j.out
#SBATCH --error=/scratch/kudhru/arnavbharti/src/slurm/generated/local-models-v1/gpt-oss-120b-local/logs/sdk-gpt-oss-120b-local-final-analysis-frozen-%j.err

set -euo pipefail
spack load gcc@13.2.0
GCC_LIBRARY_DIR="$(dirname "$(g++ -print-file-name=libstdc++.so.6)")"
export LD_LIBRARY_PATH="$GCC_LIBRARY_DIR${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
cd /scratch/kudhru/arnavbharti/src
source .venv/bin/activate
export HF_HOME=/scratch/kudhru/arnavbharti/huggingface
export XDG_CACHE_HOME=/scratch/kudhru/arnavbharti/cache
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export TOKENIZERS_PARALLELISM=false
export PYTHONDONTWRITEBYTECODE=1

# Unpack the locally tested historical source, not the active Qwen tree.
THESIS_FROZEN_ROOT=/scratch/kudhru/arnavbharti/reproducibility/gpt-oss-2cdbc1f
mkdir -p "$THESIS_FROZEN_ROOT"
tar -xzf ../evidence/submissions/2026-09-30-gptoss-final-analysis/frozen-source.tar.gz \
  -C "$THESIS_FROZEN_ROOT"
srun python3 "$THESIS_FROZEN_ROOT/src/13_analyze_results.py" \
  gpt-oss-120b-local \
  --config /scratch/kudhru/arnavbharti/src/config/local-models.json \
  --execute
