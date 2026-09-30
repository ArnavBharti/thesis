# Qwen follow-up submissions

Submitted on Sharanga on 30 September 2026, approximately 21:55--21:57 IST,
after the user authorized all remaining experiments. The copied `.sbatch`
files are generated scripts, not changes to frozen source. Slurm command-line
overrides below supersede their default resource directives.

| Script | Job ID | Expected job name | Time override |
|---|---:|---|---|
| `08_run_input_output_cross.py` | 373543 | `sdk-qwen-3-8-27b-local-exp6-input-output` | `0-12:00` |
| `09_run_token_length.py` | 373544 | `sdk-qwen-3-8-27b-local-exp7-token-length` | `0-12:00` |
| `10_run_binding.py` | 373545 | `sdk-qwen-3-8-27b-local-exp8-binding` | `1-00:00` |
| `11_run_ablations.py` | 373546 | `sdk-qwen-3-8-27b-local-exp9-ablations` | `1-12:00` |
| `12_run_revisions.py` | 373547 | `sdk-qwen-3-8-27b-local-exp10-revisions` | `0-18:00` |
| `13_analyze_results.py` | 373551 | `sdk-qwen-3-8-27b-local-final-analysis` | default `0-02:00` |

All five inference jobs use `qwen-3.8-27b-local` with
`config/qwen-27b-v2.json`, `gpu_h100_4`, one H100, 12 CPUs, and 96 GB RAM.
They have no dependencies and may run concurrently. All five resource
requests passed `sbatch --test-only` before submission. Test-only IDs are
not actual queued jobs.

The CPU analysis uses `compute`, 4 CPUs (command-line override), 16 GB RAM,
no GPU, and `afterok:373543:373544:373545:373546:373547`. The initial 2-CPU
request was rejected by `cpulimit`'s minimum of 4 CPUs; no QOS change was used.
The corrected request passed its test-only check before submission.

At the final check all inference jobs were pending. The scheduler estimated
Step 8 at 1 October 10:48:34 IST and Step 9 at 1 October 14:45:23 IST;
the other GPU jobs had no estimate. These are changeable scheduling
estimates, not promises. The CPU job was pending for its dependencies.

GPT-OSS Step 13 was not submitted. The numbered entry point refused its
current environment because `models`, `sample_plan`, and `source_sha256`
differ from its frozen global protocol. No guard or frozen artifact was
changed. The report's completed offline analysis is unaffected.

These files document submissions only, not successful completion. Verify
exact IDs/names, saved request counts, digests, and completion markers before
including follow-up outcomes in the paper. If a GPU job times out, resume
its checkpointed experiment and update the analysis dependency to the exact
authorized replacement job before relying on automatic finalization.
