#!/bin/bash
#SBATCH --partition=gpu_h100_4
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=192G
#SBATCH --time=0-23:30
#SBATCH --job-name=sdk-qwen-local-qualification
#SBATCH --output=/Users/arnavbharti/Developer/arnavbharti/thesis/src/slurm/generated/test-step-scripts/qwen-local/logs/sdk-qwen-local-qualification-%j.out
#SBATCH --error=/Users/arnavbharti/Developer/arnavbharti/thesis/src/slurm/generated/test-step-scripts/qwen-local/logs/sdk-qwen-local-qualification-%j.err
#SBATCH --gres=gpu:1

set -euo pipefail
cd /Users/arnavbharti/Developer/arnavbharti/thesis/src
source /Users/arnavbharti/Developer/arnavbharti/thesis/src/.venv/bin/activate
export TOKENIZERS_PARALLELISM=false
srun python3 run_experiments.py --config /private/var/folders/6r/_p6my8514875g6pwhnc56tww0000gn/T/tmp3j3qmz2s/experiments.json --model qwen-local --experiments qualification
