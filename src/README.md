# Sudoku representation experiments

This project tests whether a language model can solve the same 9x9 Sudoku when the values are renamed with different symbols.

All commands assume the repository is `/scratch/kudhru/arnavbharti/src`. Every numbered script is safe to run again: completed requests are reused and active Slurm jobs are not submitted twice.

## Models and sample sizes

| Script name | Model | Execution |
|---|---|---|
| `mistral-small-4-local` | Mistral Small 4 119B A6B | 2 H200 GPUs |
| `nemotron-local` | Llama-3.3-Nemotron-Super-49B-v1.5 FP8 | 1 H100 GPU |
| `gpt-5.6-terra-openrouter` | GPT | OpenRouter |
| `claude-sonnet-5-openrouter` | Claude | OpenRouter |

- Calibration: 5 easy + 5 medium + 5 hard Arabic puzzles.
- Pilot: 5 + 5 + 5 puzzles in four representations.
- Main benchmark: 20 + 20 + 20 puzzles in nine representations.
- Mechanism experiments: 5 puzzles per difficulty.
- Exploratory ablations: 3 puzzles per difficulty.

The main benchmark makes `60 x 9 x 4 = 2,160` calls. The complete workflow makes approximately 4,418 to 4,526 calls before retries.

Run GPU jobs one at a time. Wait for each job before submitting the next. Never run the full benchmark for a model that fails calibration.

## Repeat after every login

Paste this on the login node:

```bash
export ARNAVSCRATCH="/scratch/kudhru/arnavbharti"
export PIP_CACHE_DIR="/scratch/kudhru/arnavbharti/cache/pip"
export HF_HOME="/scratch/kudhru/arnavbharti/huggingface"
cd "/scratch/kudhru/arnavbharti/src"
git pull origin main --ff-only
spack unload --all
spack load anaconda3/lddgbyw
source .venv/bin/activate
python -c "import sqlite3, sys; assert sys.version_info >= (3, 10); print(sys.version); print('SQLite', sqlite3.sqlite_version)"
```

Define this helper after each login. It submits one job, waits for that exact job ID, and prints the final Slurm state:

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
    squeue --noheader --jobs "$job_id" --format='%i %T %M/%l %R'
    sleep 60
  done
  sacct -j "$job_id" --format=JobID,JobName,State,Elapsed,ExitCode
}
```

Commands written as `run_and_wait python ...` can safely be pasted as one complete block. The next command starts only after the previous job leaves the queue.

Before an OpenRouter job, also run:

```bash
export OPENROUTER_API_KEY="replace-with-your-key"
```

## One-time Python setup

On the login node:

```bash
export ARNAVSCRATCH="/scratch/kudhru/arnavbharti"
cd "/scratch/kudhru/arnavbharti/src"
git pull origin main --ff-only
srun --partition=compute --nodes=1 --ntasks=1 --cpus-per-task=8 --mem=32G --time=02:00:00 --pty bash -l
```

On the compute node:

```bash
export ARNAVSCRATCH="/scratch/kudhru/arnavbharti"
export PIP_CACHE_DIR="/scratch/kudhru/arnavbharti/cache/pip"
export HF_HOME="/scratch/kudhru/arnavbharti/huggingface"
cd "/scratch/kudhru/arnavbharti/src"
spack unload --all
spack load anaconda3/lddgbyw
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[local]"
python -m unittest discover -s tests -v
```

If `.venv` already works, do not recreate it. Run only:

```bash
source .venv/bin/activate
python -m pip install -e ".[local]"
python -m unittest discover -s tests -v
```

## Delete old downloaded weights

Old result files are useful development evidence. Do not delete `experiment_outputs/`.

First inspect the exact old cache directories:

```bash
du -sh \
  /scratch/kudhru/arnavbharti/huggingface/hub/models--Qwen--Qwen3.8-27B \
  /scratch/kudhru/arnavbharti/huggingface/hub/models--zai-org--GLM-4.7-Flash \
  /scratch/kudhru/arnavbharti/huggingface/hub/models--moonshotai--Kimi-Linear-48B-A3B-Instruct
```

If those paths are correct, delete exactly those recoverable downloads:

```bash
rm -rf -- \
  /scratch/kudhru/arnavbharti/huggingface/hub/models--Qwen--Qwen3.8-27B \
  /scratch/kudhru/arnavbharti/huggingface/hub/models--zai-org--GLM-4.7-Flash \
  /scratch/kudhru/arnavbharti/huggingface/hub/models--moonshotai--Kimi-Linear-48B-A3B-Instruct
```

If the obsolete Python backup exists and the current `.venv` passes tests:

```bash
du -sh /scratch/kudhru/arnavbharti/src/.venv-without-sqlite
rm -rf -- /scratch/kudhru/arnavbharti/src/.venv-without-sqlite
```

## Step 1: prepare the dataset

Run on the interactive compute node:

```bash
python 01_prepare_data.py
```

## Step 2: download local models

Stay on the interactive compute node. Download one at a time:

```bash
python 02_download_models.py --model nemotron-local
```

```bash
python 02_download_models.py --model mistral-small-4-local
```

Verify the downloads:

```bash
python 02_download_models.py --verify-only --model nemotron-local
python 02_download_models.py --verify-only --model mistral-small-4-local
```

## Step 3: check the setup

```bash
python 03_check_setup.py --model nemotron-local
python 03_check_setup.py --model mistral-small-4-local
exit
```

Back on the login node, paste **Repeat after every login** again.

## Step 4A: calibrate local models

Calibration uses 15 held-out Arabic puzzles. Passing requires at least 4/5 easy, 2/5 medium, 1/5 hard, and no operational failure.

Submit Nemotron, then wait:

```bash
run_and_wait python 04_calibrate_model.py nemotron-answer-only
```

After it finishes, submit Mistral:

```bash
run_and_wait python 04_calibrate_model.py mistral-small-4-bounded
```

For every submitted job, replace `JOB_ID` below with the printed ID:

```bash
squeue -j JOB_ID
sacct -j JOB_ID --format=JobID,JobName,State,Elapsed,ExitCode
```

Code 1 can mean that the accuracy threshold was missed. Read the log before treating it as an operational error.

## Step 4B: qualify all models

Run one command, wait for it to finish, then run the next:

```bash
run_and_wait python 04_qualify_model.py nemotron-local
```

```bash
run_and_wait python 04_qualify_model.py mistral-small-4-local
```

```bash
export OPENROUTER_API_KEY="replace-with-your-key"
run_and_wait python 04_qualify_model.py gpt-5.6-terra-openrouter
```

```bash
run_and_wait python 04_qualify_model.py claude-sonnet-5-openrouter
```

## Step 5: run the pilot

Run one at a time and wait after each:

```bash
run_and_wait python 05_run_pilot.py nemotron-local
run_and_wait python 05_run_pilot.py mistral-small-4-local
run_and_wait python 05_run_pilot.py gpt-5.6-terra-openrouter
run_and_wait python 05_run_pilot.py claude-sonnet-5-openrouter
```

## Step 6: freeze the protocol

From the login node:

```bash
srun --partition=compute --nodes=1 --ntasks=1 --cpus-per-task=8 --mem=32G --time=02:00:00 --pty bash -l
```

On the compute node:

```bash
export ARNAVSCRATCH="/scratch/kudhru/arnavbharti"
export HF_HOME="/scratch/kudhru/arnavbharti/huggingface"
cd "/scratch/kudhru/arnavbharti/src"
spack unload --all
spack load anaconda3/lddgbyw
source .venv/bin/activate
python 06_freeze_protocol.py
exit
```

This freezes 15 pilot puzzles, 60 different main puzzles, 15 mechanism puzzles, and 9 ablation puzzles.

## Step 7: main benchmark

Paste **Repeat after every login** first. For each model, run Parts 1 through 6 in order. Wait after every line.

```bash
run_and_wait python 07_run_main_benchmark.py nemotron-local --part 1
run_and_wait python 07_run_main_benchmark.py nemotron-local --part 2
run_and_wait python 07_run_main_benchmark.py nemotron-local --part 3
run_and_wait python 07_run_main_benchmark.py nemotron-local --part 4
run_and_wait python 07_run_main_benchmark.py nemotron-local --part 5
run_and_wait python 07_run_main_benchmark.py nemotron-local --part 6
```

```bash
run_and_wait python 07_run_main_benchmark.py mistral-small-4-local --part 1
run_and_wait python 07_run_main_benchmark.py mistral-small-4-local --part 2
run_and_wait python 07_run_main_benchmark.py mistral-small-4-local --part 3
run_and_wait python 07_run_main_benchmark.py mistral-small-4-local --part 4
run_and_wait python 07_run_main_benchmark.py mistral-small-4-local --part 5
run_and_wait python 07_run_main_benchmark.py mistral-small-4-local --part 6
```

```bash
run_and_wait python 07_run_main_benchmark.py gpt-5.6-terra-openrouter --part 1
run_and_wait python 07_run_main_benchmark.py gpt-5.6-terra-openrouter --part 2
run_and_wait python 07_run_main_benchmark.py gpt-5.6-terra-openrouter --part 3
run_and_wait python 07_run_main_benchmark.py gpt-5.6-terra-openrouter --part 4
run_and_wait python 07_run_main_benchmark.py gpt-5.6-terra-openrouter --part 5
run_and_wait python 07_run_main_benchmark.py gpt-5.6-terra-openrouter --part 6
```

```bash
run_and_wait python 07_run_main_benchmark.py claude-sonnet-5-openrouter --part 1
run_and_wait python 07_run_main_benchmark.py claude-sonnet-5-openrouter --part 2
run_and_wait python 07_run_main_benchmark.py claude-sonnet-5-openrouter --part 3
run_and_wait python 07_run_main_benchmark.py claude-sonnet-5-openrouter --part 4
run_and_wait python 07_run_main_benchmark.py claude-sonnet-5-openrouter --part 5
run_and_wait python 07_run_main_benchmark.py claude-sonnet-5-openrouter --part 6
```

## Steps 8 to 12: mechanism experiments

Run one line at a time and wait after each submitted job.

Step 8, input/output cross:

```bash
run_and_wait python 08_run_input_output_cross.py nemotron-local
run_and_wait python 08_run_input_output_cross.py mistral-small-4-local
run_and_wait python 08_run_input_output_cross.py gpt-5.6-terra-openrouter
run_and_wait python 08_run_input_output_cross.py claude-sonnet-5-openrouter
```

Step 9, token length for local models:

```bash
run_and_wait python 09_run_token_length.py nemotron-local
run_and_wait python 09_run_token_length.py mistral-small-4-local
```

Step 10, arbitrary binding:

```bash
run_and_wait python 10_run_binding.py nemotron-local
run_and_wait python 10_run_binding.py mistral-small-4-local
run_and_wait python 10_run_binding.py gpt-5.6-terra-openrouter
run_and_wait python 10_run_binding.py claude-sonnet-5-openrouter
```

Step 11, prompt and output ablations:

```bash
run_and_wait python 11_run_ablations.py nemotron-local
run_and_wait python 11_run_ablations.py mistral-small-4-local
run_and_wait python 11_run_ablations.py gpt-5.6-terra-openrouter
run_and_wait python 11_run_ablations.py claude-sonnet-5-openrouter
```

Step 12, revisions:

```bash
run_and_wait python 12_run_revisions.py nemotron-local
run_and_wait python 12_run_revisions.py mistral-small-4-local
run_and_wait python 12_run_revisions.py gpt-5.6-terra-openrouter
run_and_wait python 12_run_revisions.py claude-sonnet-5-openrouter
```

## Step 13: analyze results

```bash
run_and_wait python 13_analyze_results.py nemotron-local
run_and_wait python 13_analyze_results.py mistral-small-4-local
run_and_wait python 13_analyze_results.py gpt-5.6-terra-openrouter
run_and_wait python 13_analyze_results.py claude-sonnet-5-openrouter
```

## Check status and logs

```bash
squeue -u "$USER"
python status.py
python status.py --model nemotron-local
```

For one job:

```bash
sacct -j JOB_ID --format=JobID,JobName,State,Elapsed,ExitCode
```

Follow its logs:

```bash
tail -f slurm/generated/thesis-confirmatory-compact-v1/MODEL_NAME/logs/*-JOB_ID.out
tail -f slurm/generated/thesis-confirmatory-compact-v1/MODEL_NAME/logs/*-JOB_ID.err
```

Press `Ctrl+C` to stop following a log. It does not cancel the job.

## Safe reruns

- Completed request IDs are skipped.
- An active job is not submitted twice.
- An interrupted job continues from saved results.
- Results are append-only.
- Frozen manifests reject changed settings.

Do not manually edit anything under `experiment_outputs/`.
