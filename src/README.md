# Sudoku representation experiments

This project tests whether language models can still solve the same Sudoku when digits are replaced by other symbols.

On Sharanga, the repository should be located at `/scratch/kudhru/arnavbharti`. Run all experiment commands from `/scratch/kudhru/arnavbharti/src`. The numbered Python files contain the experiment steps. Shared model, Sudoku, evaluation, storage, and Slurm code is in `lib/`.

The shell prompt tells you where you are:

- `[kudhru@hpc01 ...]` is the login node.
- `[kudhru@node... ...]` is an interactive compute job.

Steps 1, 2, 3, and 6 run directly and must be run on an interactive compute node. Steps 4, 5, and 7 through 13 submit their own Slurm jobs and should be started from the login node.

## Models

| Script name | Execution |
|---|---|
| `qwen-local` | Qwen3.8-27B on 1 H100 |
| `glm-flash-local` | GLM-4.7-Flash on 2 H100s |
| `kimi-linear-local` | Kimi-Linear-48B-A3B on 2 H200s |
| `gpt-5.6-terra-openrouter` | OpenAI through OpenRouter |
| `claude-sonnet-5-openrouter` | Anthropic through OpenRouter |

GLM-4.7-Flash and Kimi-Linear are smaller replacements for the GLM-5.2 and Kimi-K3 models named in the original outline. Report their exact names in the paper.

## One-time setup on Sharanga

### A. Paste on the login node

Define the scratch location and start an interactive compute shell:

```bash
export ARNAVSCRATCH="/scratch/kudhru/arnavbharti"
cd "$ARNAVSCRATCH/src"
srun --partition=compute \
  --nodes=1 \
  --ntasks=1 \
  --cpus-per-task=8 \
  --mem=32G \
  --time=02:00:00 \
  --pty bash -l
```

Wait for the prompt to change from `hpc01` to `node...`.

### B. Paste on the compute node

Create the Python environment:

```bash
export ARNAVSCRATCH="/scratch/kudhru/arnavbharti"
export PIP_CACHE_DIR="$ARNAVSCRATCH/cache/pip"
export HF_HOME="$ARNAVSCRATCH/huggingface"
mkdir -p "$PIP_CACHE_DIR" "$HF_HOME"
cd "$ARNAVSCRATCH/src"
spack unload --all
spack load anaconda3/lddgbyw
python3 -c "import sqlite3, sys; assert sys.version_info >= (3, 10); print(sys.version); print('SQLite', sqlite3.sqlite_version)"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[local]"
```

The check must print Python 3.10 or newer and an SQLite version. Sharanga's standalone Python 3.10 build has no `_sqlite3` module, so do not use `spack load python/wikzev7` for this project.

If `.venv` was created with Python 3.6 or with `python/wikzev7`, replace it before installing packages:

```bash
deactivate
mv .venv .venv-without-sqlite
spack unload --all
spack load anaconda3/lddgbyw
python3 -c "import sqlite3, sys; assert sys.version_info >= (3, 10); print(sys.version); print('SQLite', sqlite3.sqlite_version)"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[local]"
```

The moved `.venv-without-sqlite` directory is only a backup. You can delete it after the new environment works. The model downloads under `$HF_HOME` are separate and do not need to be downloaded again. Stay in the compute shell and continue with Steps 1, 2, and 3 below.

## Repeat after every login

Paste this block on the login node whenever you log in again. It prepares the shell for commands that submit experiment jobs:

```bash
export ARNAVSCRATCH="/scratch/kudhru/arnavbharti"
export PIP_CACHE_DIR="$ARNAVSCRATCH/cache/pip"
export HF_HOME="$ARNAVSCRATCH/huggingface"
cd "$ARNAVSCRATCH/src"
spack unload --all
spack load anaconda3/lddgbyw
source .venv/bin/activate
python -c "import sqlite3, sys; assert sys.version_info >= (3, 10); print(sys.version); print('SQLite', sqlite3.sqlite_version)"
```

The last command must print Python 3.10 or newer and an SQLite version, and the prompt should begin with `(.venv)`. Do not run a numbered script from the login node until all checks are true.

Before submitting a GPT or Claude job in that shell, also run:

```bash
export OPENROUTER_API_KEY="replace-with-your-key"
```

You do not need the OpenRouter key for Qwen, GLM, or Kimi. Slurm receives the environment values that are set when you submit the job.

## Start an interactive compute shell again

Steps 1, 2, 3, and 6 require an interactive compute shell. If your prompt says `hpc01`, paste:

```bash
srun --partition=compute \
  --nodes=1 \
  --ntasks=1 \
  --cpus-per-task=8 \
  --mem=32G \
  --time=02:00:00 \
  --pty bash -l
```

After the prompt changes to `node...`, paste:

```bash
export ARNAVSCRATCH="/scratch/kudhru/arnavbharti"
export PIP_CACHE_DIR="$ARNAVSCRATCH/cache/pip"
export HF_HOME="$ARNAVSCRATCH/huggingface"
cd "$ARNAVSCRATCH/src"
spack unload --all
spack load anaconda3/lddgbyw
source .venv/bin/activate
python -c "import sqlite3, sys; assert sys.version_info >= (3, 10); print(sys.version); print('SQLite', sqlite3.sqlite_version)"
```

The last command must print Python 3.10 or newer and an SQLite version.

## Repeat after every submitted job

Each experiment command submits one job and then returns to the terminal. Check the queue:

```bash
squeue -u "$USER"
```

Wait until the submitted group is no longer listed. Then check what completed and which command comes next:

```bash
python status.py
```

Do not start the next step, or the next Step 7 part, until the current group has finished.

## Which jobs can run together

The commands in one allowed group may be pasted together. Each command still creates a separate Slurm job.

| Step | Commands that may be submitted together |
|---|---|
| 1 | One direct command on an interactive compute node. |
| 2 | One direct command; it downloads all three local models. |
| 3 | One direct command on an interactive compute node. |
| 4 | All five model qualification jobs. |
| 5 | All five model pilot jobs, after every model has passed Step 4. |
| 6 | One direct command, after all five pilot jobs finish. |
| 7 | One part per model at a time: submit the five Part 1 jobs together, wait, then Part 2, and so on. |
| 8 | All five model jobs, after Step 7 is complete. |
| 9 | All three local-model jobs. |
| 10 | All five model jobs. |
| 11 | All five model jobs. |
| 12 | All five model jobs. |
| 13 | All five analysis jobs, after the required experiments finish. |

Do not submit different numbered steps together. For OpenRouter jobs, your account must have enough credit and rate-limit capacity for GPT and Claude to run at the same time.

## Step 1: prepare and check the Sudoku data

Run this on the interactive compute node. If your prompt says `hpc01`, first use the two copy-and-paste blocks under **Start an interactive compute shell again**.

```bash
python 01_prepare_data.py
```

The command runs the tests, keeps the existing dataset when it is valid, and independently checks all 300 puzzles. It is safe to run again.

Check without changing anything:

```bash
python 01_prepare_data.py --status
```

## Step 2: download the local models

Stay on the interactive compute node and run:

```bash
python 02_download_models.py
```

Existing downloaded files are reused. If the interactive allocation ends during a download, start another interactive compute shell and run the same command again. Verify the downloads later without downloading:

```bash
python 02_download_models.py --verify-only
```

## Step 3: check the complete setup

Stay on the interactive compute node and run:

```bash
python 03_check_setup.py
```

Every item should print `READY`.

Return to the login node:

```bash
exit
```

After the prompt changes back to `hpc01`, paste the block under **Repeat after every login** before continuing with Step 4.

## Step 4: qualify every model

All five commands are independent. Paste all five together:

```bash
python 04_qualify_model.py qwen-local
python 04_qualify_model.py glm-flash-local
python 04_qualify_model.py kimi-linear-local
python 04_qualify_model.py gpt-5.6-terra-openrouter
python 04_qualify_model.py claude-sonnet-5-openrouter
```

Each model must solve all five qualification puzzles. A failed model is not silently replaced.

## Step 5: run the pilot

After all five models pass Step 4, paste all five commands together:

```bash
python 05_run_pilot.py qwen-local
python 05_run_pilot.py glm-flash-local
python 05_run_pilot.py kimi-linear-local
python 05_run_pilot.py gpt-5.6-terra-openrouter
python 05_run_pilot.py claude-sonnet-5-openrouter
```

The pilot uses 60 puzzles and four representations. Pilot puzzles are not used in the confirmatory main sample.

## Step 6: freeze the reduced protocol

Run this only after all five pilot jobs are complete. From `hpc01`, use the two blocks under **Start an interactive compute shell again**. Then run this on the compute node:

```bash
python 06_freeze_protocol.py
```

Return to the login node when it finishes:

```bash
exit
```

This freezes these deterministic samples:

- Pilot: 20 puzzles per difficulty, 60 total.
- Main benchmark: 50 different puzzles per difficulty, 150 total.
- Mechanism experiments: 10 main puzzles per difficulty, 30 total.
- Ablation and revision experiments: 5 main puzzles per difficulty, 15 total.

The command also writes and prints the Arabic pilot accuracy for each model. A warning means a difficulty tier is outside the planned calibration range. Keep the warning and report the observed floor or ceiling in the paper; do not silently replace puzzles after seeing confirmatory results.

Do not change prompts, samples, models, or inference settings after this step. If a real protocol change is necessary, use a new `run_id` in `config/experiments.json`.

## Step 7: run the main benchmark

The main benchmark has six parts per model. Submit one part for all five models together. Wait for those five jobs to finish before submitting the next part.

Part 1:

```bash
python 07_run_main_benchmark.py qwen-local --part 1
python 07_run_main_benchmark.py glm-flash-local --part 1
python 07_run_main_benchmark.py kimi-linear-local --part 1
python 07_run_main_benchmark.py gpt-5.6-terra-openrouter --part 1
python 07_run_main_benchmark.py claude-sonnet-5-openrouter --part 1
```

Part 2, after all Part 1 jobs finish:

```bash
python 07_run_main_benchmark.py qwen-local --part 2
python 07_run_main_benchmark.py glm-flash-local --part 2
python 07_run_main_benchmark.py kimi-linear-local --part 2
python 07_run_main_benchmark.py gpt-5.6-terra-openrouter --part 2
python 07_run_main_benchmark.py claude-sonnet-5-openrouter --part 2
```

Part 3, after all Part 2 jobs finish:

```bash
python 07_run_main_benchmark.py qwen-local --part 3
python 07_run_main_benchmark.py glm-flash-local --part 3
python 07_run_main_benchmark.py kimi-linear-local --part 3
python 07_run_main_benchmark.py gpt-5.6-terra-openrouter --part 3
python 07_run_main_benchmark.py claude-sonnet-5-openrouter --part 3
```

Part 4, after all Part 3 jobs finish:

```bash
python 07_run_main_benchmark.py qwen-local --part 4
python 07_run_main_benchmark.py glm-flash-local --part 4
python 07_run_main_benchmark.py kimi-linear-local --part 4
python 07_run_main_benchmark.py gpt-5.6-terra-openrouter --part 4
python 07_run_main_benchmark.py claude-sonnet-5-openrouter --part 4
```

Part 5, after all Part 4 jobs finish:

```bash
python 07_run_main_benchmark.py qwen-local --part 5
python 07_run_main_benchmark.py glm-flash-local --part 5
python 07_run_main_benchmark.py kimi-linear-local --part 5
python 07_run_main_benchmark.py gpt-5.6-terra-openrouter --part 5
python 07_run_main_benchmark.py claude-sonnet-5-openrouter --part 5
```

Part 6, after all Part 5 jobs finish:

```bash
python 07_run_main_benchmark.py qwen-local --part 6
python 07_run_main_benchmark.py glm-flash-local --part 6
python 07_run_main_benchmark.py kimi-linear-local --part 6
python 07_run_main_benchmark.py gpt-5.6-terra-openrouter --part 6
python 07_run_main_benchmark.py claude-sonnet-5-openrouter --part 6
```

## Step 8: run the input/output experiment

After all Step 7 jobs finish, paste all five commands together:

```bash
python 08_run_input_output_cross.py qwen-local
python 08_run_input_output_cross.py glm-flash-local
python 08_run_input_output_cross.py kimi-linear-local
python 08_run_input_output_cross.py gpt-5.6-terra-openrouter
python 08_run_input_output_cross.py claude-sonnet-5-openrouter
```

Matching Arabic and Greek baseline answers are reused from Step 7, so they do not make duplicate model calls.

## Step 9: run the token-length experiment

This step requires exact token IDs and therefore runs only for local models. Paste all three commands together:

```bash
python 09_run_token_length.py qwen-local
python 09_run_token_length.py glm-flash-local
python 09_run_token_length.py kimi-linear-local
```

## Step 10: run the binding experiment

Paste all five commands together:

```bash
python 10_run_binding.py qwen-local
python 10_run_binding.py glm-flash-local
python 10_run_binding.py kimi-linear-local
python 10_run_binding.py gpt-5.6-terra-openrouter
python 10_run_binding.py claude-sonnet-5-openrouter
```

Three exact baseline conditions are reused from Step 7.

## Step 11: run the prompt ablations

Paste all five commands together:

```bash
python 11_run_ablations.py qwen-local
python 11_run_ablations.py glm-flash-local
python 11_run_ablations.py kimi-linear-local
python 11_run_ablations.py gpt-5.6-terra-openrouter
python 11_run_ablations.py claude-sonnet-5-openrouter
```

These 15-puzzle analyses are exploratory and should be described that way in the paper.

## Step 12: run the revision experiment

Paste all five commands together:

```bash
python 12_run_revisions.py qwen-local
python 12_run_revisions.py glm-flash-local
python 12_run_revisions.py kimi-linear-local
python 12_run_revisions.py gpt-5.6-terra-openrouter
python 12_run_revisions.py claude-sonnet-5-openrouter
```

Each revision condition starts from the same saved Step 7 answer. The revision branches are separate, so feedback from one branch cannot enter another branch.

## Step 13: analyze each model

After all required experiment jobs finish, paste all five commands together:

```bash
python 13_analyze_results.py qwen-local
python 13_analyze_results.py glm-flash-local
python 13_analyze_results.py kimi-linear-local
python 13_analyze_results.py gpt-5.6-terra-openrouter
python 13_analyze_results.py claude-sonnet-5-openrouter
```

These are small CPU jobs.

## Check progress

Run this at any time:

```bash
python status.py
```

For one model:

```bash
python status.py --model qwen-local
```

The script prints the next command to run.

Check the Slurm queue:

```bash
squeue -u "$USER"
```

## Safe reruns

Every numbered script can be run again:

- A completed step prints `SKIP`.
- A job that is already queued or running is not submitted again.
- An interrupted job can be submitted again with the same command.
- Existing request IDs in append-only result files are skipped.
- A step is marked complete only after every expected request is stored.
- Frozen manifests prevent changed code or settings from being mixed into the same run.

Preview a job without submitting it:

```bash
python 07_run_main_benchmark.py qwen-local --part 1 --dry-run
```

Ask Slurm to validate the resources without submitting:

```bash
python 07_run_main_benchmark.py qwen-local --part 1 --test-only
```

## Reduced study size

The design uses approximately 12,595 to 12,820 model calls before retries. The exact Experiment 10 count depends on whether checker-guided revision is needed. The original design required approximately 27,265 to 27,715 calls.

The full workflow uses 68 one-at-a-time Slurm jobs:

- 5 qualification jobs.
- 5 pilot jobs.
- 30 main-benchmark jobs.
- 5 input/output jobs.
- 3 token-length jobs.
- 5 binding jobs.
- 5 ablation jobs.
- 5 revision jobs.
- 5 analysis jobs.

## If vLLM reports a CUDA compiler error

The generated GPU jobs automatically find the CUDA compiler installed inside
`.venv` and put it on `PATH`. They also store vLLM, TorchInductor, and Triton
compilation caches under `$ARNAVSCRATCH/cache`, not under your small home quota.
The local dependency list pins the compiler to the same CUDA 13.0 release used
by PyTorch.

If the log says that the CUDA compiler and toolkit headers are incompatible,
update the environment in an interactive compute shell. Start on the login
node:

```bash
export ARNAVSCRATCH="/scratch/kudhru/arnavbharti"
cd "$ARNAVSCRATCH/src"
git pull --ff-only
srun --partition=compute \
  --nodes=1 \
  --ntasks=1 \
  --cpus-per-task=8 \
  --mem=32G \
  --time=02:00:00 \
  --pty bash -l
```

After the prompt changes to `node...`, repair and verify the environment:

```bash
export ARNAVSCRATCH="/scratch/kudhru/arnavbharti"
export PIP_CACHE_DIR="$ARNAVSCRATCH/cache/pip"
export HF_HOME="$ARNAVSCRATCH/huggingface"
cd "$ARNAVSCRATCH/src"
spack unload --all
spack load anaconda3/lddgbyw
source .venv/bin/activate
python -m pip install -e ".[local]"
python 03_check_setup.py --model qwen-local
exit
```

`CUDA compiler` must print `READY`. Back on the login node, load the environment
and submit the failed qualification job again:

```bash
export ARNAVSCRATCH="/scratch/kudhru/arnavbharti"
export HF_HOME="$ARNAVSCRATCH/huggingface"
cd "$ARNAVSCRATCH/src"
spack unload --all
spack load anaconda3/lddgbyw
source .venv/bin/activate
python 04_qualify_model.py qwen-local
```

The last command replaces the generated `.sbatch` file and submits a new job.
It does not repeat any completed requests.

## Results

Results are stored under:

```text
experiment_outputs/thesis-confirmatory-lean-v1/
```

Important files include:

- `sample-plan.json`: frozen pilot, main, mechanism, and ablation puzzle IDs.
- `protocol.json`: frozen global design.
- `<model>/provenance.json`: model, software, Git, host, and GPU information.
- `<model>/<experiment>/request-manifest.json`: exact request count and digest.
- `<model>/<experiment>/shard-*.jsonl`: append-only raw responses and evaluations.
- `<model>/analysis/summary.json`: final statistical summary.
- `<model>/analysis/observations.jsonl`: analysis-ready request-level records.

Do not manually edit result files.

## Run tests manually

```bash
python -m unittest discover -s tests -v
```

## Sharanga documentation

- [GPU jobs](https://sharanga.hpc.bits-hyderabad.ac.in/docs/faq/jobs/gpu/)
- [GPU configuration](https://sharanga.hpc.bits-hyderabad.ac.in/docs/misc_docs/configuration/)
- [Scratch storage](https://sharanga.hpc.bits-hyderabad.ac.in/docs/faq/storage/)
