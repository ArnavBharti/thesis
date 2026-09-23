# Thesis repository agent guide

This file is the durable handoff for agents working in this repository. Read it before changing code, running experiments, or operating Sharanga.

## Scope and research objective

This first-degree thesis measures how LLM Sudoku performance changes under symbolic representation changes and related experimental conditions. Only the final Sudoku grid is scored; visible reasoning traces are not an analysis target.

The required answer is exactly nine lines of nine space-separated symbols, with no prose or Markdown. All clues must be preserved, and every row, column, and 3x3 box must be valid.

The dataset contains 300 unique-solution puzzles: 100 easy, 100 medium, and 100 hard. The frozen main sample contains 20 puzzles at each difficulty. Do not modify the dataset, frozen sample plan, or benchmark protocol without first discussing the evidence with the user.

## Repositories and synchronization

- Local repository: `/Users/arnavbharti/Developer/arnavbharti/thesis`
- Local source directory: `/Users/arnavbharti/Developer/arnavbharti/thesis/src`
- SSH alias: `thesis`
- Server repository: `/scratch/kudhru/arnavbharti/src`
- Permitted server write tree: `/scratch/kudhru/arnavbharti`

Always synchronize the server repository with:

```bash
ssh thesis
cd /scratch/kudhru/arnavbharti/src
git pull origin main --ff-only
```

Never edit tracked source independently on the server. Test, commit, and push local changes to `origin/main` before pulling them on Sharanga.

If SSH connects only as far as the login banner or otherwise stalls, stop immediately and ask the user to unlock SSH. Do not repeatedly troubleshoot the connection.

## Sharanga safety rules

The `kudhru` HPC account is shared by multiple people.

- Never cancel, modify, hold, reprioritize, or otherwise interfere with a job unless it was submitted by this thesis workflow in the current conversation or its recorded continuation.
- Before cancelling, verify both the exact job ID and expected thesis job name with `squeue` or `sacct`.
- Inspecting files, logs, and scheduler state is allowed.
- Run inference only through numbered Python scripts submitted to Slurm.
- Never run inference, model loading, package installation, compilation, or other heavy work on the login node.
- Do not download models unless the user explicitly authorizes that specific download. Downloads must use `02_download_models.py` inside an interactive CPU compute allocation, never on the login node.
- Independent thesis GPU jobs may run concurrently. Use Slurm dependencies only when an actual data or protocol dependency exists; do not serialize unrelated experiments.
- Before every GPU submission, tell the user the model, partition/GPU type, GPU count, CPU count, memory, and wall-time.
- Never run OpenRouter models unless the user explicitly requests it.
- Do not touch unrelated jobs, even if they block this workflow through shared-account QOS or fair-share limits.

Read-only status pattern:

```bash
ssh thesis 'squeue --noheader -j JOB_ID -o "%i|%j|%T|%M|%l|%E|%R"; sacct -j JOB_ID -X -n -P -o JobID,JobName,State,Elapsed,ExitCode'
```

Use `squeue --start -j JOB_ID` only as an estimate; it may change. Ordinary users cannot legitimately raise priority. Accurate, shorter wall-times may improve backfill. Higher-priority QOS or reservations require HPC administrator approval. Do not use unauthorized QOS, partition, nice, or priority changes.

## Current models and resources

The paper is currently being completed with GPT-OSS 120B:

- Profile: `gpt-oss-120b-local`
- Model: `openai/gpt-oss-120b`
- Revision: `b5c939de8f754692c1647ca79fbf85e8c1e70f8a`
- Reasoning: hidden Harmony reasoning; only the final answer is scored
- Partition: `gpu_h100_4`
- GPUs: 1 H100
- CPUs: 12
- Memory: 96 GB
- Normal main-part wall-time: 8 hours

Do not describe 192 GB as the GPT-OSS allocation; the committed profile requests 96 GB.

Reasoning must not appear in the final response, but hidden reasoning tokens may be used internally. The earlier error was treating reasoning as a small output-token budget rather than bounding execution by time.

Qwen3.8-27B-FP8 is the candidate replication model and is isolated from the frozen GPT-OSS configuration:

- Config: `config/qwen-27b.json`
- Profile: `qwen-3.8-27b-local`
- Model: `Qwen/Qwen3.8-27B-FP8`
- Revision: `017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`
- Reasoning: thinking enabled at `xhigh`; thinking tags removed before scoring
- Partition: `gpu_h100_4`
- GPUs: 1 H100
- CPUs: 12
- Memory: 96 GB
- Diagnostic wall-time: 1 hour

The Qwen profile has its own run ID, `qwen-3.8-27b-v1`. Do not add it to or otherwise change `config/local-models.json`, because that configuration is part of the frozen GPT-OSS protocol. Screen Qwen with one easy, medium, and hard timing puzzle, then qualification and the 60-request pilot. Do not run a Qwen main benchmark unless those results justify the additional inference.

The authorized token file is local at `src/.env`. It is ignored by Git and must remain mode `0600`. When explicitly authorized, copy it only to `/scratch/kudhru/arnavbharti/src/.env`, set the server copy to mode `0600`, source it without printing it, and never include its contents in logs or tool output.

## Completed experimental evidence

GPT-OSS timing diagnostic, one puzzle per difficulty, was fully correct:

- Easy: 36.12 seconds, 7,247 tokens
- Medium: 254.59 seconds, 49,220 tokens
- Hard: 227.35 seconds, 44,435 tokens

Qualification job `347048` completed 5/5 with zero operational failures.

Pilot completed 60/60 requests with 47 correct (78.3%) and zero operational failures:

- Easy: 20/20
- Medium: 13/20
- Hard: 14/20
- Arabic: 14/15
- Emoji: 13/15
- Greek: 10/15
- Uppercase Latin: 10/15
- Mean latency: 252.48 seconds
- Median latency: 194.85 seconds
- Truncations: 2

The GPT-OSS protocol was frozen with `06_freeze_protocol.py --model gpt-oss-120b-local`. The main benchmark contains 540 requests in six deterministic hash shards. Exact shard sizes are:

- Part 1: 101
- Part 2: 89
- Part 3: 77
- Part 4: 108
- Part 5: 86
- Part 6: 79

Completed main parts:

- Part 1: 101/101, completion marker present. Initial job `351374` timed out after 82 results; resume job `352226` completed.
- Part 2: 89/89, completion marker present. Job `352227` completed in 6:37:44 with exit `0:0`.
- Part 3: 77/77, completion marker present. Job `353501` completed in 6:31:39 with exit `0:0`.
- Part 4: 108/108, completion marker present. Initial job `353504` timed out after 97 results; resume job `356757` completed the remaining requests.
- Part 5: 86/86, completion marker present. The successful replacement run completed with exit `0:0`.
- Part 6: 79/79, completion marker present. Job `359393` completed in 7:16:03 with exit `0:0`.

The complete main benchmark contains 540/540 saved requests and valid completion markers for all six parts. Part 4 job `353504` timed out after 8:00:08 with 97/108 results saved; this was wall-time exhaustion, not a model, CUDA, Python, vLLM, or memory failure. The resume reused those checkpointed results.

## Active queue state (recorded 2026-09-23 23:28 IST)

The remaining GPT-OSS mechanism experiments are independently queued with no dependencies. Each requests one H100, 12 CPUs, and 96 GB RAM:

- Input/output cross: job `361279`, expected name `sdk-gpt-oss-120b-local-exp6-input-output`, 5-hour wall-time, pending for resources.
- Token length: job `361280`, expected name `sdk-gpt-oss-120b-local-exp7-token-length`, 6-hour wall-time, pending for priority.
- Binding: job `361281`, expected name `sdk-gpt-oss-120b-local-exp8-binding`, 11-hour wall-time, pending for priority.
- Prompt/output ablations: job `361282`, expected name `sdk-gpt-oss-120b-local-exp9-ablations`, 15-hour wall-time, pending for priority.
- Revisions: job `361283`, expected name `sdk-gpt-oss-120b-local-exp10-revisions`, 10-hour wall-time, pending for priority.

The dependency fields were deliberately cleared after the user authorized concurrent independent jobs. Never assume the recorded states remain current; query Slurm first.

Superseded pending jobs `356607`, `356608`, and `356609` were safely cancelled after exact name verification. Earlier blocked jobs `353505` and `353506` were also safely cancelled. Do not operate on these completed/cancelled IDs.

Main result files and markers are under:

```text
/scratch/kudhru/arnavbharti/src/experiment_outputs/local-models-v1/gpt-oss-120b-local/exp4/
```

Part `N` uses `shard-(N-1)-of-006.jsonl` with a three-digit shard index, and marker `part-N-of-006.complete.json` with a three-digit part number. A Slurm exit of `0:0` plus a valid completion marker establishes successful completion. A JSONL count alone does not.

## Running or resuming a main part

The numbered entry point is:

```bash
cd /scratch/kudhru/arnavbharti/src
source .venv/bin/activate
python 07_run_main_benchmark.py gpt-oss-120b-local \
  --part PART \
  --config config/local-models.json \
  --wall-time 0-08:00
```

Execution is idempotent: existing request IDs in the shard JSONL are skipped. If a part times out, determine the exact eligible count and saved count before choosing a resume wall-time. Do not delete partial results.

When jobs truly depend on one another, generate the `.sbatch` file with `--dry-run`, submit with `sbatch --parsable --dependency=afterok:JOB_ID`, record every returned ID, and verify names, resources, and dependencies with `squeue`. Independent experiments should be submitted without dependencies and may run concurrently.

## Local development requirements

Keep code and README instructions simple, readable, correct, idempotent, and copy-paste friendly. Preserve unrelated user changes in a dirty worktree.

Use `apply_patch` for manual file edits. Before committing local changes, run:

```bash
cd /Users/arnavbharti/Developer/arnavbharti/thesis/src
python3 -m unittest discover -s tests -q

cd /Users/arnavbharti/Developer/arnavbharti/thesis
git status --short
git diff --check
git add <only-relevant-files>
git commit -m "<clear message>"
git push origin main
```

Never use destructive Git commands to discard user work.

## Paper draft

The paper sources are local under `paper/`:

- `paper/draft.tex`
- `paper/references.bib`
- `paper/generate_results.py`
- `paper/Makefile`

Commit `0ff0d34` introduced the initial paper draft and generated tables. It contains only evidence available at that time (pilot and completed main part 1). Update results only from completed, verified experiment evidence. Do not label results as “preliminary”; write final-draft technical English while leaving unavailable results unwritten. Do not invent findings.

The main benchmark is complete. Copy or synchronize its verified result evidence locally, regenerate tables and plots for all six parts, compile the PDF, and visually inspect every page. Keep raw copied server evidence under the ignored `tmp/` tree unless the repository explicitly requires otherwise.

## Historical model evidence

Nemotron diagnostics established that formatting constraints alone did not create Sudoku competence:

- Reasoning-enabled bounded run: 0/5 easy and 0/5 medium, with contradictory visible reasoning.
- Reasoning-off greedy: 0/5 easy before cancellation, frequent prose/token exhaustion.
- Reasoning-off sampled: 0/15.
- Reasoning-off constrained greedy: 0/15; correct format but invalid grids and changed clues.

These results are useful methodological context, but the completed main benchmark and active mechanism experiments use GPT-OSS. Do not restart Nemotron, Mistral, or OpenRouter work without explicit user direction. Qwen3.8-27B-FP8 screening is now explicitly authorized under its isolated configuration. Older Qwen job `347025` was previously cancelled safely while pending.

## Interpretation rules

- Perfect easy accuracy is not a qualification requirement. Performance such as 3/5 or 4/5 easy can be acceptable; 1/5 medium and 0/5 hard can still be informative.
- Separate operational failures from incorrect Sudoku answers and from the calibration script's intentional exit code `1` when acceptance criteria are missed.
- Report format compliance, clue preservation, Sudoku validity, correctness by difficulty and representation, latency, truncation, and operational errors separately.
- Never infer success from clean formatting alone.
