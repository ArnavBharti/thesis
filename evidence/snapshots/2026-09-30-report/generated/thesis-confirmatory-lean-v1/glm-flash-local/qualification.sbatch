#!/bin/bash
#SBATCH --partition=gpu_h100_4
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=256G
#SBATCH --time=0-23:30
#SBATCH --job-name=sdk-glm-flash-local-qualification
#SBATCH --output=/scratch/kudhru/arnavbharti/src/slurm/generated/thesis-confirmatory-lean-v1/glm-flash-local/logs/sdk-glm-flash-local-qualification-%j.out
#SBATCH --error=/scratch/kudhru/arnavbharti/src/slurm/generated/thesis-confirmatory-lean-v1/glm-flash-local/logs/sdk-glm-flash-local-qualification-%j.err
#SBATCH --gres=gpu:2

set -euo pipefail
cd /scratch/kudhru/arnavbharti/src
source /scratch/kudhru/arnavbharti/src/.venv/bin/activate
export TOKENIZERS_PARALLELISM=false
srun python3 04_qualify_model.py glm-flash-local --config /scratch/kudhru/arnavbharti/src/config/experiments.json --execute
