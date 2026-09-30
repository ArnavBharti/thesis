# GPT-OSS Step 13 source review

Compared all files covered by `source_digest()` between frozen commit
`2cdbc1f` and the current source on 30 September 2026. Exactly three files
differ:

1. `03_run_timing_diagnostic.py` was added for isolated Qwen timing reruns.
   Step 13 neither imports nor executes it.
2. `04_qualify_model.py` gained `--min-correct`, range validation, forwarding
   into the submitted qualification job, and forwarding into qualification
   status generation. The default remains five. Step 13 does not execute it.
3. `lib/statistics.py` reads the recorded qualification threshold, accepts a
   `min_correct` argument, adds that field to qualification summaries, and
   checks `correct >= min_correct` rather than exactly five. Its default
   remains five. Main accuracy, retention tests, regression, revision
   summaries, observations, and their implementations are unchanged.

`13_analyze_results.py`, model inference, prompts, evaluation, token registry,
dataset handling, and sample selection are byte-identical to the frozen
version. GPT-OSS model configuration and the saved sample plan are identical
after JSON normalization. The previous comparison incorrectly reported
model/sample-plan differences because it compared Python tuples to JSON lists.

The frozen source digest is
`3a0be67794c976e26dd4b7b70fbc8b4ac57155e796d7d87d9ce4ad38cb0b7de7`.
Current source is
`505a323f5c29503d44e996a6d207a9a8c3a32f5d7a8bf11ffc2aba9cc6af63ec`.
Local reconstruction using the frozen source and original server dataset path
matches the entire archived global protocol, not just its source hash.

The frozen source's full local suite passes 82 tests. Running both historical
and current statistical implementations locally on the same 1,229 saved
GPT-OSS records produces identical summaries apart from the current version's
added `min_correct: 5` qualification field.

## Execution decision

The changes do not require rerunning GPT-OSS inference. To retain the exact
registered implementation, Step 13 runs from a separate export of `src/` at
`2cdbc1f`, packaged locally with `git archive`. The original source-hash and
configuration check remains enabled. It reads the original saved results and
writes only the normal token registry and analysis artifacts. It never
rewrites raw inference results or the frozen protocol.

The CPU Slurm job requests `compute`, 4 CPUs, 16 GB RAM, zero GPUs, and two
hours. It unpacks into the personal permitted scratch tree, uses the existing
virtual environment, and forces offline tokenizer access. No installation,
model download, inference, or login-node analysis is involved. The active
Qwen source and its five queued mechanism jobs are not modified.
