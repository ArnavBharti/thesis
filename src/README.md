# Sudoku representation experiments

This project tests whether a language model can solve the same 9x9 Sudoku when the
values are renamed with different symbols. Only the final grid is scored. Hidden
reasoning is stored separately and is never part of the scored answer.

All server commands assume the repository is:

```text
/scratch/kudhru/arnavbharti/src
```

The numbered scripts are idempotent: completed requests are reused, active jobs are
not submitted twice, and interrupted runs resume from saved results.

## Models and sample sizes

The workflow uses exactly two open-weight local models:

| Script name | Pinned model | Hidden reasoning | Sharanga request |
|---|---|---|---|
| `gpt-oss-120b-local` | `openai/gpt-oss-120b` | Harmony analysis/final channels | 1 H100, 12 CPUs, 192 GB RAM |
| `qwen-3.5-122b-local` | `Qwen/Qwen3.5-122B-A10B-FP8` | thinking tags removed before scoring | 2 H200, 8 CPUs, 256 GB RAM |

Qwen uses vLLM's Triton linear and GDN-prefill backends because the automatic
FlashInfer FP8 kernel fails during initialization on Sharanga's H200 software stack.

The choices are supported by primary documentation:

- [OpenAI GPT-OSS release](https://openai.com/index/introducing-gpt-oss/) documents
  high/medium/low reasoning and single-80-GB-GPU operation.
- [OpenAI GPT-OSS-120B documentation](https://developers.openai.com/api/docs/models/gpt-oss-120b)
  identifies it as OpenAI's most capable open-weight model.
- [Qwen3.5-122B-A10B-FP8](https://huggingface.co/Qwen/Qwen3.5-122B-A10B-FP8)
  is the official 125B MoE FP8 checkpoint with configurable thinking.
- [vLLM's GPT-OSS recipe](https://docs.vllm.ai/projects/recipes/en/latest/OpenAI/GPT-OSS.html)
  documents structured reasoning and final output channels.

Sample sizes:

- Model screen: one held-out easy, medium, and hard puzzle per model.
- Qualification: five held-out puzzles in five representations per model.
- Pilot: 5 easy + 5 medium + 5 hard puzzles in four representations.
- Main benchmark: 20 easy + 20 medium + 20 hard puzzles in nine representations.
- Mechanism experiments: five puzzles per difficulty.
- Exploratory ablations: three puzzles per difficulty.

The main benchmark makes `60 x 9 x 2 = 1,080` calls.

## Safety rules

- The HPC account is shared. Never change or cancel another user's job.
- Identify a thesis job by both exact job ID and expected job name before cancelling.
- Write only under `/scratch/kudhru/arnavbharti`.
- Synchronize the server only with `git pull origin main --ff-only`.
- Run GPU inference jobs one at a time.
- Do not run hosted API models.
- Do not install packages on the login node.
- Download model weights manually after login; do not submit download jobs.
- Before every GPU submission, record the model, partition/GPU type, GPU count,
  CPUs, RAM, and wall-time.

## Repeat after every login

Copy and paste on the login node:

```bash
export ARNAVSCRATCH="/scratch/kudhru/arnavbharti"
export PIP_CACHE_DIR="/scratch/kudhru/arnavbharti/cache/pip"
export HF_HOME="/scratch/kudhru/arnavbharti/huggingface"
export HF_HUB_CACHE="/scratch/kudhru/arnavbharti/huggingface/hub"
cd "/scratch/kudhru/arnavbharti/src"
git pull origin main --ff-only
spack unload --all
spack load anaconda3/lddgbyw
source .venv/bin/activate
python -c "import sqlite3, sys; assert sys.version_info >= (3, 10); print(sys.version); print('SQLite', sqlite3.sqlite_version)"
```

Define this helper after each login. It submits one inference job, waits for that
exact job ID, and prints the final Slurm state:

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

## Verify Sharanga limits

These read-only commands show the current GPU partitions and QOS limits:

```bash
sinfo -o "%P|%G|%D|%C|%l"
scontrol show partition gpu_h100_4
scontrol show partition gpu_h200_8
sacctmgr -n -P show qos format=Name,MaxTRESPerUser,MaxJobsPerUser,MaxWall,GrpTRES   | grep -E '^qos_gpu_h(100|200)\|'
```

At the last verified check, `qos_gpu_h200` allowed at most three H200 GPUs, eight
CPUs, and 300 GB RAM per user. Every configured request stays below those limits.
Generated jobs load GCC 13.2 and its runtime library, expose the wheel-bundled CUDA
runtime libraries to the JIT linker, and disable optional vLLM usage telemetry. All
generated shims and caches remain under thesis scratch.

## One-time Python setup

Only use this section if `.venv` is missing or broken. Start an interactive CPU
compute allocation from the login node:

```bash
export ARNAVSCRATCH="/scratch/kudhru/arnavbharti"
cd "/scratch/kudhru/arnavbharti/src"
git pull origin main --ff-only
srun --partition=compute --nodes=1 --ntasks=1 --cpus-per-task=8 --mem=32G --time=02:00:00 --pty bash -l
```

Install only after the prompt changes to the allocated compute node:

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
python -m unittest discover -s tests -q
exit
```

If the environment already works, do not recreate or reinstall it.

## Inspect model storage

These commands are read-only:

```bash
du -sh   /scratch/kudhru/arnavbharti/huggingface/hub/models--openai--gpt-oss-120b   /scratch/kudhru/arnavbharti/huggingface/hub/models--Qwen--Qwen3.5-122B-A10B-FP8   2>/dev/null
df -h /scratch/kudhru/arnavbharti
```

Do not delete a snapshot while an inference job may be using it. Result files under
`experiment_outputs/` are evidence and must not be deleted.

## Step 1: prepare the dataset

Run from the activated login environment:

```bash
python 01_prepare_data.py
```

## Step 2: download local models

Download manually after login, one at a time. These pinned downloads are idempotent
and resume interrupted shards:

```bash
python 02_download_models.py   --config config/local-models.json   --model gpt-oss-120b-local

python 02_download_models.py   --config config/local-models.json   --verify-only   --model gpt-oss-120b-local

python 02_download_models.py   --config config/local-models.json   --model qwen-3.5-122b-local

python 02_download_models.py   --config config/local-models.json   --verify-only   --model qwen-3.5-122b-local
```

Verify both together:

```bash
python 02_download_models.py   --config config/local-models.json   --verify-only   --model gpt-oss-120b-local   --model qwen-3.5-122b-local
```

## Step 3: check the setup

```bash
python 03_check_setup.py --config config/local-models.json --model gpt-oss-120b-local
python 03_check_setup.py --config config/local-models.json --model qwen-3.5-122b-local
```

## Step 4: screen the two models

The screen uses the same reproducibly selected easy, medium, and hard puzzle for
each model. The 131,072-token ceiling prevents unbounded generation; the one-hour
Slurm limit is the actual time limit. Only the separated final grid is scored.

Run the entire block. The helper guarantees sequential GPU use:

```bash
run_and_wait python diagnose_timing.py gpt-oss-120b-local easy
run_and_wait python diagnose_timing.py gpt-oss-120b-local medium
run_and_wait python diagnose_timing.py gpt-oss-120b-local hard

run_and_wait python diagnose_timing.py qwen-3.5-122b-local easy
run_and_wait python diagnose_timing.py qwen-3.5-122b-local medium
run_and_wait python diagnose_timing.py qwen-3.5-122b-local hard
```

This is a diagnostic, not a requirement to solve every puzzle. Performance such as
3/5 or 4/5 easy, 1/5 medium, and 0/5 hard can be acceptable at calibration. Do not
alter the dataset or frozen benchmark protocol from a single diagnostic result.

## Step 4B: qualify each model

Run only after reviewing the three-puzzle screen:

```bash
run_and_wait python 04_qualify_model.py gpt-oss-120b-local --config config/local-models.json
run_and_wait python 04_qualify_model.py qwen-3.5-122b-local --config config/local-models.json
```

An exit code of 1 can represent a missed accuracy threshold rather than a CUDA,
Python, vLLM, or memory failure. Inspect the exact job log before classifying it.

## Step 5: run the pilot

Run one model at a time:

```bash
run_and_wait python 05_run_pilot.py gpt-oss-120b-local --config config/local-models.json
run_and_wait python 05_run_pilot.py qwen-3.5-122b-local --config config/local-models.json
```

## Step 6: freeze the protocol

Only freeze after all required pilots are complete:

```bash
python 06_freeze_protocol.py --config config/local-models.json
```

This freezes 15 pilot puzzles, 60 different main puzzles, 15 mechanism puzzles, and
nine ablation puzzles. Do not change the frozen protocol without documenting the
evidence and decision.

## Step 7: run the main benchmark

Run parts 1 through 6 in order for each model. The helper waits after every line:

```bash
for model in   gpt-oss-120b-local   qwen-3.5-122b-local
do
  for part in 1 2 3 4 5 6
  do
    run_and_wait python 07_run_main_benchmark.py "$model"       --part "$part"       --config config/local-models.json
  done
done
```

## Steps 8 to 12: mechanism experiments

Run each complete block sequentially.

Step 8, input/output cross:

```bash
for model in gpt-oss-120b-local qwen-3.5-122b-local
do
  run_and_wait python 08_run_input_output_cross.py "$model" --config config/local-models.json
done
```

Step 9, token length:

```bash
for model in gpt-oss-120b-local qwen-3.5-122b-local
do
  run_and_wait python 09_run_token_length.py "$model" --config config/local-models.json
done
```

Step 10, arbitrary binding:

```bash
for model in gpt-oss-120b-local qwen-3.5-122b-local
do
  run_and_wait python 10_run_binding.py "$model" --config config/local-models.json
done
```

Step 11, prompt and output ablations:

```bash
for model in gpt-oss-120b-local qwen-3.5-122b-local
do
  run_and_wait python 11_run_ablations.py "$model" --config config/local-models.json
done
```

Step 12, revisions:

```bash
for model in gpt-oss-120b-local qwen-3.5-122b-local
do
  run_and_wait python 12_run_revisions.py "$model" --config config/local-models.json
done
```

## Step 13: analyze results

```bash
for model in gpt-oss-120b-local qwen-3.5-122b-local
do
  run_and_wait python 13_analyze_results.py "$model" --config config/local-models.json
done
```

## Check status and logs

Show workflow status:

```bash
python status.py --config config/local-models.json
python status.py --config config/local-models.json --model gpt-oss-120b-local
python status.py --config config/local-models.json --model qwen-3.5-122b-local
```

Inspect one exact job:

```bash
squeue -j JOB_ID -o "%i|%j|%T|%M|%l|%R"
sacct -j JOB_ID -X --format=JobID,JobName,State,Elapsed,ExitCode
```

Follow its logs:

```bash
tail -f slurm/generated/RUN_ID/MODEL_NAME/logs/*-JOB_ID.out
tail -f slurm/generated/RUN_ID/MODEL_NAME/logs/*-JOB_ID.err
```

Press `Ctrl+C` to stop following a log. This does not cancel the job.

## Safe reruns

- Completed request IDs are skipped.
- An active thesis job is not submitted twice.
- An interrupted job continues from saved results.
- Results are append-only.
- Frozen manifests reject changed settings.
- Never manually edit files under `experiment_outputs/`.

## Local verification before committing

```bash
cd "/Users/arnavbharti/Developer/arnavbharti/thesis/src"
python3 -m unittest discover -s tests -q
cd "/Users/arnavbharti/Developer/arnavbharti/thesis"
git status --short
git diff --check
git add <only-relevant-files>
git commit -m "<clear-message>"
git push origin main
```

Update Sharanga only after the push:

```bash
ssh thesis
cd "/scratch/kudhru/arnavbharti/src"
git pull origin main --ff-only
```
