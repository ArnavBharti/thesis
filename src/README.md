# Sudoku representation experiments

This repository measures whether changing Sudoku symbols changes language-model
accuracy. Only the final 9x9 grid is scored; reasoning is retained separately and is
never treated as part of the answer.

## Selected local models

The active stronger-model screen uses three open-weight models:

| Script name | Pinned model | Why it is included | Sharanga request |
|---|---|---|---|
| `gpt-oss-120b-local` | `openai/gpt-oss-120b` | Configurable effort, Harmony reasoning/final channels, and official single-H100 operation | 1 H100, 12 CPUs, 192 GB, 1 hour |
| `qwen-3.5-122b-local` | `Qwen/Qwen3.5-122B-A10B-FP8` | 125B-parameter MoE with about 10B active parameters and explicit thinking support | 2 H200, 8 CPUs, 256 GB, 1 hour |
| `mistral-medium-3.5-local` | `mistralai/Mistral-Medium-3.5-128B` | Dense 128B model with native high reasoning and separate reasoning/content output | 2 H200, 8 CPUs, 256 GB, 1 hour |

Qwen3.8-27B remains in the diagnostic configuration only to reproduce earlier timing
evidence. It is disabled for the new screen. It correctly solved the selected easy
and hard puzzles, while the selected medium run did not return a final grid.

Primary references:

- [OpenAI: introducing GPT-OSS](https://openai.com/index/introducing-gpt-oss/)
- [OpenAI: GPT-OSS-120B model](https://developers.openai.com/api/docs/models/gpt-oss-120b)
- [Qwen3.5-122B-A10B-FP8 model card](https://huggingface.co/Qwen/Qwen3.5-122B-A10B-FP8)
- [Mistral Medium 3.5 model card](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B)
- [vLLM GPT-OSS recipe](https://docs.vllm.ai/projects/recipes/en/latest/OpenAI/GPT-OSS.html)

## Sharanga limits

The live `qos_gpu_h200` policy allows at most 3 H200 GPUs, 8 CPUs, and 300 GB RAM per
user. The H100 policy allows this workflow's 1-H100, 12-CPU, 192-GB request. Verify
the current policy without changing anything:

```bash
scontrol show partition gpu_h200_8
sacctmgr -n -P show qos format=Name,MaxTRESPerUser,MaxJobsPerUser,MaxWall,GrpTRES \
  | grep -E '^qos_gpu_h(100|200)\|'
```

Never interfere with another user's jobs. Run thesis GPU jobs one at a time.

## Login setup

Copy and paste after every login:

```bash
export ARNAVSCRATCH="/scratch/kudhru/arnavbharti"
export HF_HOME="/scratch/kudhru/arnavbharti/huggingface"
export HF_HUB_CACHE="/scratch/kudhru/arnavbharti/huggingface/hub"
export PIP_CACHE_DIR="/scratch/kudhru/arnavbharti/cache/pip"
cd "/scratch/kudhru/arnavbharti/src"
git pull origin main --ff-only
spack unload --all
spack load anaconda3/lddgbyw
source .venv/bin/activate
python -c "import sqlite3, sys; print(sys.version); print('SQLite', sqlite3.sqlite_version)"
```

Do not install packages on the login node. If the existing environment ever needs
repair, request an interactive CPU compute allocation before installing anything.
Model downloads below are manual login-session commands, not Slurm jobs.

## Download the three models

The commands are idempotent and pinned by `config/stronger-model-diagnostic.json`.
Interrupted downloads resume when the same command is run again. Download one model
at a time:

```bash
python 02_download_models.py \
  --config config/stronger-model-diagnostic.json \
  --model gpt-oss-120b-local

python 02_download_models.py \
  --config config/stronger-model-diagnostic.json \
  --verify-only \
  --model gpt-oss-120b-local

python 02_download_models.py \
  --config config/stronger-model-diagnostic.json \
  --model qwen-3.5-122b-local

python 02_download_models.py \
  --config config/stronger-model-diagnostic.json \
  --verify-only \
  --model qwen-3.5-122b-local

python 02_download_models.py \
  --config config/stronger-model-diagnostic.json \
  --model mistral-medium-3.5-local

python 02_download_models.py \
  --config config/stronger-model-diagnostic.json \
  --verify-only \
  --model mistral-medium-3.5-local
```

Verify all snapshots together:

```bash
python 02_download_models.py \
  --config config/stronger-model-diagnostic.json \
  --verify-only \
  --model gpt-oss-120b-local \
  --model qwen-3.5-122b-local \
  --model mistral-medium-3.5-local
```

## Sequential inference helper

Define this helper on the login node. It waits for the exact job returned by the
numbered script before allowing the next command to submit:

```bash
run_and_wait() {
  output=$("$@" 2>&1)
  command_status=$?
  printf '%s\n' "$output"
  job_id=$(printf '%s\n' "$output" | awk '/Submitted one job:/ {print $NF}' | tail -n 1)
  if [ -z "$job_id" ]; then
    return "$command_status"
  fi
  while squeue --noheader --jobs "$job_id" | grep -q .; do
    squeue --noheader --jobs "$job_id" --format='%i|%j|%T|%M|%l|%R'
    sleep 60
  done
  sacct -j "$job_id" -X --format=JobID,JobName,State,Elapsed,ExitCode
}
```

## Three-puzzle model screen

Each model receives the same reproducibly selected easy, medium, and hard puzzle.
Reasoning may consume the available time and token context, but only the separated
final grid is scored. Run the complete block; it remains sequential:

```bash
run_and_wait python diagnose_timing.py gpt-oss-120b-local easy
run_and_wait python diagnose_timing.py gpt-oss-120b-local medium
run_and_wait python diagnose_timing.py gpt-oss-120b-local hard

run_and_wait python diagnose_timing.py qwen-3.5-122b-local easy
run_and_wait python diagnose_timing.py qwen-3.5-122b-local medium
run_and_wait python diagnose_timing.py qwen-3.5-122b-local hard

run_and_wait python diagnose_timing.py mistral-medium-3.5-local easy
run_and_wait python diagnose_timing.py mistral-medium-3.5-local medium
run_and_wait python diagnose_timing.py mistral-medium-3.5-local hard
```

The diagnostic is exploratory. Completing every easy puzzle is not required. Results
such as 3/5 or 4/5 easy, 1/5 medium, and 0/5 hard can still justify retaining a model
for calibration. Do not change the main dataset or frozen benchmark protocol based on
one diagnostic puzzle.

## Local verification before source changes

Run locally before every commit:

```bash
cd "/Users/arnavbharti/Developer/arnavbharti/thesis/src"
python3 -m unittest discover -s tests -q
cd "/Users/arnavbharti/Developer/arnavbharti/thesis"
git status --short
git diff --check
```
