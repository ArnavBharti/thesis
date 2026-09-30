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

The study now has two selected local models. GPT-OSS 120B has completed its
benchmark and mechanism experiments:

- Profile: `gpt-oss-120b-local`
- Model: `openai/gpt-oss-120b`
- Revision: `b5c939de8f754692c1647ca79fbf85e8c1e70f8a`
- Reasoning: hidden Harmony reasoning; only the final answer is scored
- Partition: `gpu_h100_4`
- GPUs: 1 H100
- CPUs: 12
- Memory: 192 GB for the frozen main profile; 96 GB for later mechanism jobs
- Normal main-part wall-time: 8 hours

The 2026-09-30 evidence audit corrected an earlier handoff error: the frozen
GPT-OSS main profile and main job scripts request 192 GB host RAM. Later
mechanism scripts request 96 GB. Verify the exact saved script and scheduler
record rather than assuming one allocation for every stage. These are host
memory requests, not GPU VRAM.

Reasoning must not appear in the final response, but hidden reasoning tokens may be used internally. The earlier error was treating reasoning as a small output-token budget rather than bounding execution by time.

Qwen3.8-27B-FP8 is the second study model and is isolated from the frozen
GPT-OSS configuration. The first screen used `config/qwen-27b.json`; the
larger-context screen and pilot use `config/qwen-27b-v2.json`:

- Config: `config/qwen-27b-v2.json`
- Profile: `qwen-3.8-27b-local`
- Model: `Qwen/Qwen3.8-27B-FP8`
- Revision: `017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`
- Reasoning: thinking enabled at `xhigh`; thinking tags removed before scoring
- Context and output ceilings: 131,072 tokens each, matching GPT-OSS
- Effective sampling: temperature 1, top-p 1, matching GPT-OSS
- Partition: `gpu_h100_4`
- GPUs: 1 H100
- CPUs: 12
- Memory: 96 GB
- Diagnostic and qualification wall-time: 2 hours

The current Qwen profile has run ID `qwen-3.8-27b-v2`. Do not add it to or
otherwise change `config/local-models.json`, because that configuration is part
of the frozen GPT-OSS protocol. The qualification threshold for this Qwen
screen is 3/5 easy puzzles with zero operational failures; the default 5/5 rule
remains unchanged for other runs. The user has chosen Qwen as the second model.
Its pilot has completed and supports a full main benchmark. The Qwen protocol
was frozen after the pilot, using the same 60 main puzzles and nine alphabets
as GPT-OSS. The isolated Qwen configuration sets 12 main hash shards. Each job
requests a 12-hour wall-time, one H100, 12 CPUs, and 96 GB RAM. All 12 parts
have been submitted; see exact IDs below.

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

## Completed mechanism evidence

The input/output-cross experiment (Step 8, job `361279`) completed 135/135
conditions with zero operational failures. Overall accuracy was 120/135. The
four 15-puzzle Sudoku conditions scored 12/15 for Arabic-to-Arabic, 12/15 for
Greek-to-Greek, 10/15 for Greek-to-Arabic, and 11/15 for Arabic-to-Greek. All
75 no-Sudoku controls were correct. Across the four Sudoku conditions, easy,
medium, and hard accuracy was 19/20, 18/20, and 8/20. Two hard requests
truncated. These findings do not support a simple Greek-output penalty; the
cross-mapping conditions were weaker, but the small sample does not isolate a
single causal mechanism.

The token-length experiment (Step 9, job `361280`) completed 45/45 conditions
with zero operational failures. One-, two-, and three-token labels scored 9/15,
13/15, and 10/15. Difficulty accuracy was 15/15 easy, 13/15 medium, and 4/15
hard, with five truncations. The preregistered multivariable fit had a singular
information matrix because token, byte, code-point, and prompt-length measures
co-varied in the construction. Report the descriptive non-monotonic result; do
not claim an independently identified token-length effect.

The binding experiment (Step 10, job `361281`) completed 165/165 records with
zero request-level operational failures. Overall accuracy was 124/165, with
seven truncations. Easy, medium, and hard accuracy was 55/55, 50/55, and 19/55.
Ordinary digits, ordinary number words, and neutral nonce labels each scored
12/15; permuted digits and conflicting number words each scored 10/15. Six
mappings over the same uppercase tokens ranged from 10/15 to 13/15. The paired
differences point toward binding and semantic interference but are not
conclusive with 15 puzzles per condition.

The prompt/output ablation experiment (Step 11, job `361282`) wrote all 171/171
records and a valid completion marker before Slurm killed backend teardown at
the 15-hour wall-time. The records contain zero request-level operational
failures, 103/171 correct outcomes, and 12 truncations. A digit mapping scored
8/9, while no rule or output-format variant was uniformly better. Four
conditions that generated identical default prompts independently scored 5/9,
6/9, 5/9, and 7/9, demonstrating generation variability despite the recorded
fixed sampling seed. The evidence does not isolate numerical/runtime
nondeterminism from stochastic effects. Do not
treat small ablation differences as grounds to change the frozen protocol.

The self-revision experiment (Step 12, job `361283`) completed 108/108 records
with a valid completion marker and zero request-level operational failures.
Correct counts were 18/27 for one pass, 19/27 for one self-revision, 23/27 for
two self-revisions, and 22/27 for checker-guided revision. These 27-request
condition results are exploratory and do not establish a universal revision
benefit. Step 12 raw evidence is now backed up in the dated report snapshot
and included in its offline tables and stage-cost analysis.

Qwen's first 32,768-token timing screen completed: easy was correct in 80.48
inference seconds; medium and hard were incorrect after 32,425 and 32,426
generated tokens respectively. In both failures, prompt plus generation filled
the entire 32,768-token context, so they are not clean Sudoku-accuracy tests.

Qwen's 131,072-token medium timing rerun, job `363803`, completed correctly in
387.20 inference seconds with exit `0:0`. Qualification job `363811` completed
5/5 correct with zero operational failures and exit `0:0`.

Qwen's 60-request pilot, job `363814`, completed in 7:38:08 with exit `0:0`,
60/60 saved records, and a valid completion marker. It solved 54/60 with zero
operational failures and two truncations. Easy, medium, and hard accuracy was
20/20, 16/20, and 18/20. Arabic digits, emoji, and Greek letters each scored
13/15; uppercase Latin scored 15/15. Mean latency was 452.30 seconds. Tier
means were 122.37 seconds for easy, 654.35 for medium, and 580.18 for hard.
The Qwen main plan has the same 60 puzzle IDs as the frozen GPT-OSS plan.
Twelve shards have 36 to 56 requests each, with pilot-weighted estimates of
4.4 to 7.2 inference hours. The 12-hour wall-time leaves room for slower main
requests; interrupted parts can resume from saved request IDs.

The complete GPT-OSS main benchmark, qualification, pilot, and Steps 8--12
evidence is backed up under `evidence/snapshots/2026-09-30-report/`, alongside
historical diagnostics and the captured Qwen outputs. JSONL and job logs are
losslessly gzip-compressed. `snapshot-manifest.json` records stored-file and
raw-content SHA-256 checksums. Model weights, environments, and credentials
are excluded.

## Follow-up submissions (2026-09-30 21:57 IST)

The user explicitly authorized all remaining experiments after receiving the
complete report. Five independent Qwen mechanism jobs were submitted with no
dependencies. Each uses the unchanged `config/qwen-27b-v2.json`, one H100 in
`gpu_h100_4`, 12 CPUs, and 96 GB host RAM. Wall-times are submission overrides,
not changes to the frozen configuration or generation settings.

| Step | Job ID | Expected job name | Wall-time |
|---|---:|---|---|
| 8 | 373543 | `sdk-qwen-3-8-27b-local-exp6-input-output` | 12 hours |
| 9 | 373544 | `sdk-qwen-3-8-27b-local-exp7-token-length` | 12 hours |
| 10 | 373545 | `sdk-qwen-3-8-27b-local-exp8-binding` | 24 hours |
| 11 | 373546 | `sdk-qwen-3-8-27b-local-exp9-ablations` | 36 hours |
| 12 | 373547 | `sdk-qwen-3-8-27b-local-exp10-revisions` | 18 hours |
| 13 | 373551 | `sdk-qwen-3-8-27b-local-final-analysis` | 2 hours |

At submission verification, all GPU jobs were pending for Resources/Priority.
CPU analysis `373551` was pending with `afterok` dependencies on all five GPU
IDs. It uses `compute`, zero GPUs, 4 CPUs, and 16 GB RAM. The partition's
default `cpulimit` QOS currently requires at least 4 CPUs; the generated
2-CPU default was rejected before submission. No QOS override was used.
The CPU job file was generated with the existing `write_python_job` helper
for `13_analyze_results.py`; only execution, after dependencies finish, performs
the experiment-completion checks and analysis. Submission IDs are also saved
in their `.submitted.json` files under the Qwen generated-job directory.

GPT-OSS Step 13 initially refused the current tree. The normalized comparison
confirmed that only `source_sha256` differs: the earlier report of `models`
and `sample_plan` differences was a Python tuple-versus-JSON-list comparison
error. The exact changes are a new isolated timing script, qualification
threshold support, and qualification-summary threshold support. Step 13 and
the remaining analysis implementation are unchanged. A 1,229-record local
comparison produced identical old/new analysis outputs apart from the new
`min_correct: 5` qualification field. The exact frozen commit is `2cdbc1f`;
its 82-test suite and the full archived global-protocol comparison pass.
The user authorized safe execution after this review. The source archive,
CPU submission script, and review are under
`evidence/submissions/2026-09-30-gptoss-final-analysis/`. Run its numbered
Step 13 from that separate historical export, keeping the original guard
enabled. Do not edit frozen artifacts or overwrite the active Qwen source.
CPU job `373562`, expected name
`sdk-gpt-oss-120b-local-final-analysis-frozen`, was subsequently submitted
from tested/pushed script commit `b234f3c`. It requests `compute`, 4 CPUs,
16 GB RAM, zero GPUs, and two hours, with no dependency. It started on
`node22` and completed in 3:44 with exit `0:0` and an empty error log.
The numbered script wrote 2,781 registry rows and analyzed 1,229 saved records.
The additional local backup is
`evidence/snapshots/2026-09-30-gptoss-step13/`; the earlier report snapshot
remains unchanged. GPT-OSS Step 13 is now complete.
The report and dated snapshot remain an immutable capture preceding these
new runs. Update them only from verified completed follow-up evidence.

## Recorded main job state (2026-09-30 19:31 IST)

The Qwen v2 timing, qualification, and pilot jobs have completed:

- Medium timing rerun: `363803`, expected name `sdk-qwen-3-8-27b-local-timing-medium`, completed in 17:41 with exit `0:0`.
- Qualification: `363811`, expected name `sdk-qwen-3-8-27b-local-qualification`, completed in 10:15 with exit `0:0`.
- 60-request pilot: `363814`, expected name `sdk-qwen-3-8-27b-local-exp2-pilot`, completed in 7:38:08 with exit `0:0` and a valid completion marker.

Each requests one H100 in `gpu_h100_4`, 12 CPUs, and 96 GB RAM. The older Qwen
jobs `361306`, `361307`, and `361308` have completed; do not cancel them.

The dependency fields for independent jobs were deliberately cleared after the
user authorized concurrent work. Qwen timing, qualification, and pilot had
actual data dependencies. Never assume the recorded states remain current;
query Slurm first.

Qwen's separate sample plan and protocol were frozen by CPU job `366208`,
expected name `sdk-qwen-3-8-27b-local-freeze`, which completed with exit `0:0`.
The main benchmark consists of 540 requests in 12 independent hash shards.
Exact part-to-job mappings are:

| Part | Job ID | Expected job name |
|---|---:|---|
| 1 | 366211 | `sdk-qwen-3-8-27b-local-exp4-part-001-of-012` |
| 2 | 366212 | `sdk-qwen-3-8-27b-local-exp4-part-002-of-012` |
| 3 | 366213 | `sdk-qwen-3-8-27b-local-exp4-part-003-of-012` |
| 4 | 366214 | `sdk-qwen-3-8-27b-local-exp4-part-004-of-012` |
| 5 | 366215 | `sdk-qwen-3-8-27b-local-exp4-part-005-of-012` |
| 6 | 366216 | `sdk-qwen-3-8-27b-local-exp4-part-006-of-012` |
| 7 | 366217 | `sdk-qwen-3-8-27b-local-exp4-part-007-of-012` |
| 8 | 366218 | `sdk-qwen-3-8-27b-local-exp4-part-008-of-012` |
| 9 | 366219 | `sdk-qwen-3-8-27b-local-exp4-part-009-of-012` |
| 10 | 366220 | `sdk-qwen-3-8-27b-local-exp4-part-010-of-012` |
| 11 | 366221 | `sdk-qwen-3-8-27b-local-exp4-part-011-of-012` |
| 12 | 366222 | `sdk-qwen-3-8-27b-local-exp4-part-012-of-012` |

All twelve Qwen main parts completed with valid markers and exit `0:0`.
Final part job `366222` completed on `gpunode5` at 19:29:44 IST in 8:18:28.
The final copied snapshot has 540/540 records and the matching frozen request
digest: 472 correct (87.4%), 33 nontruncated incorrect grids, 24 truncations,
11 other output errors, and zero request-level operational errors. Easy is
174/180, medium 160/180, and hard 138/180. Mean generation latency is 531.25
seconds and median 422.78. There are 505 parseable grids, 488 preserving all
clues and 487 satisfying all Sudoku units. Seventeen grids modify givens.
The GPT-OSS main result is 372/540 (68.9%), with mean latency 290.81 seconds.
The paired matrix has 338 both correct, 34 GPT-OSS only, 134 Qwen only, and
34 neither. The exploratory stratified puzzle bootstrap gives a Qwen-minus-
GPT-OSS difference of 18.52 points, 95% interval 13.70--23.52. Neither model's
eight Arabic-baseline comparisons survives Holm adjustment at 0.05.
Qwen mechanism experiments are not represented by completed outputs; do not
claim a two-model mechanism replication or submit those jobs from a report
request alone. Query current state for any later authorized submissions.
Qwen result files and markers are under
`experiment_outputs/qwen-3.8-27b-v2/qwen-3.8-27b-local/exp4/`.
Part `N` uses `shard-(N-1)-of-012.jsonl` and `part-N-of-012.complete.json`,
with three-digit indices. Verify counts and markers before treating a part as
complete. If a part times out, resume only that part with the numbered script;
saved request IDs are skipped.

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

The GPT-OSS main benchmark and Steps 8--12 are complete. The paper includes
their results. The report snapshot now includes Step 12 raw evidence and its
offline table generator. Qwen results should enter the paper only after their corresponding
experiments complete. Do not present partial pilot counts as final model
accuracy. Keep raw copied server evidence under the ignored `tmp/` tree unless
the repository explicitly requires otherwise. The user requested a detailed
paper-writing dossier rather than a manuscript rewrite. Its maintained source
is `paper/report/writing_report.md`; the assembled report is
`paper/report/complete_report.md`, and the PDF is
`output/pdf/thesis-paper-writing-report.pdf`. Do not replace `paper/draft.tex`
unless asked. The reusable skill is `$thesis-paper-report`, versioned under
`skills/thesis-paper-report/` and installed in the local Codex skill directory.

Offline verification is documented in the report and `src/README.md`. Run
`paper/report/prepare_snapshot.py ... --verify` for backup checksums and
`paper/report/analyze_evidence.py --snapshot ...` for re-scoring, independent
clue/unit checks, request content hashes, shard/marker integrity, and tables.
These scripts run locally without model loading. The added Holm comparisons
and puzzle-cluster bootstrap are exploratory report analyses, not frozen
preregistration amendments. No saved completed server Step 13 analysis or
Qwen mechanism outputs were found in this capture; do not infer execution
from the existence of their scripts. The report's local analysis reproduces
the implemented retention and token-length procedures and adds explicitly
exploratory paired analyses.

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
