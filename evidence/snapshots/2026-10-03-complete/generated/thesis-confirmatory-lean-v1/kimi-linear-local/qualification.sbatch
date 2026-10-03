#!/bin/bash
#SBATCH --partition=gpu_h200_8
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=256G
#SBATCH --time=0-23:30
#SBATCH --job-name=sdk-kimi-linear-local-qualification
#SBATCH --output=/scratch/kudhru/arnavbharti/src/slurm/generated/thesis-confirmatory-lean-v1/kimi-linear-local/logs/sdk-kimi-linear-local-qualification-%j.out
#SBATCH --error=/scratch/kudhru/arnavbharti/src/slurm/generated/thesis-confirmatory-lean-v1/kimi-linear-local/logs/sdk-kimi-linear-local-qualification-%j.err
#SBATCH --gres=gpu:2

set -euo pipefail
cd /scratch/kudhru/arnavbharti/src
source /scratch/kudhru/arnavbharti/src/.venv/bin/activate
export TOKENIZERS_PARALLELISM=false
srun python3 04_qualify_model.py kimi-linear-local --config /scratch/kudhru/arnavbharti/src/config/experiments.json --execute
