# Final report verification

## Complete two-model refresh (3 October 2026)

This section supersedes the completion status below. Earlier verification
entries are preserved as dated history, not current queue claims.

- A fresh read-only SSH transfer captured all Qwen follow-up outputs, markers,
  registries, final summaries, generated job scripts, and logs. Exact-ID
  accounting confirms jobs 373543--373547 and 373551 completed with exit `0:0`.
- `evidence/snapshots/2026-10-03-complete/` contains 599 evidence files plus
  its manifest, with 69,814,796 stored bytes. All stored/raw SHA-256 pairs pass.
  Both older snapshots remain unchanged. Credentials, weights, and environments
  are excluded; no Hugging Face/API token or private-key patterns were found.
- The local audit validates 300 puzzles and 2,650 selected/historical outcomes,
  with no request/dataset mismatch, re-scoring disagreement, independent-grid
  disagreement, content-hash error, shard error, or completion/digest error.
  Both models' main benchmarks and Steps 8--12 are complete.
- Local registered re-analysis exactly matches both server summaries, apart
  from the documented added GPT-OSS `min_correct: 5` field. Each analysis
  summarizes 1,229 rows and each registry contains 81 symbols and 2,700 prompts.
  All 75 reused cross/binding generations per model match their original main
  generations. Qwen's four identical-default-prompt binary success sets match.
- The full suite passes 104 tests, including new registered-summary, reuse,
  registry-scope, and prompt-agreement checks. The skill's installed and versioned
  instruction files match. Ruby's YAML parser validates their metadata.
  The bundled validator remains unavailable because PyYAML is not installed;
  no package installation was performed.
- The 195-page writing report preserves separate sections and all twelve
  lenses, and embeds complete methods, model-specific saved prompts/labels,
  condition/tier/error tables, transitions, cost, interpretation, and verification
  per experiment. The main paper is updated in `Soduku/paper.tex`, not the older
  `paper/draft.tex`, and its compiled PDF has 17 pages.
- All PDF pages were rendered and reviewed in contact sheets, with full-size
  checks of tokenizer, prompt-inventory, revision, and complete condition tables.
  Both builds have no LaTeX warnings, unresolved references, or missing glyphs.
  Extracted text has no replacement characters. Emoji remain explicit code-point
  notation in the PDF and exact Unicode in the Markdown/raw evidence.
- Frozen experiment code, configurations, datasets, and source artifacts are
  unchanged. No inference, download, install, job submission, or cancellation
  occurred during this update. All analysis and PDF compilation ran on the Mac.

Current reproduction commands, from the repository root:

```bash
python3 paper/report/prepare_snapshot.py tmp/research-report/unused \
  evidence/snapshots/2026-10-03-complete --verify
python3 paper/report/analyze_evidence.py \
  --snapshot evidence/snapshots/2026-10-03-complete \
  --output tmp/research-report/recheck
diff paper/report/generated/results_tables.md \
  tmp/research-report/recheck/results_tables.md
make -C Soduku
cd src
python3 -m unittest discover -s tests -q
```

## Historical verification (30 September 2026)

Verified locally on 30 September 2026. The final read-only Sharanga capture
was taken at 19:31 IST, after Qwen job `366222` completed at 19:29:44 IST
with its expected thesis job name and exit `0:0`.

## Evidence and analysis

- The dated snapshot contains 551 archived evidence files plus its manifest.
  Stored and decompressed SHA-256 checksums pass for every archived file.
- The backup excludes credentials, model weights, and environments. A scan
  found no token/private-key patterns. The largest stored file is 7,507,866 bytes.
- The offline audit reads 2,026 saved records across current and historical
  experiments. All 300 dataset puzzles pass their certificate checks.
- Request content hashes, shard assignment, expected request digests,
  duplicate checks, and completion markers establish both complete 540-request
  main benchmarks. Saved outcomes agree with rescoring and the independent
  final-grid checks. The audit reports no errors.
- Reanalysis directly from the lossless compressed backup produces the same
  results tables as the working capture.
- GPT-OSS scores 372/540; Qwen scores 472/540. Qwen mechanism experiments
  have not been completed and are not claimed in the report.

## Code, presentation, and reusable skill

- The full local unit suite passes: 95 tests, including 12 new report tests.
- The 63-page PDF was rendered page by page. All pages were reviewed in
  contact sheets, with full-size checks of figures, Unicode symbols, and
  detailed results tables. Extracted PDF text has no replacement characters.
- Emoji in the PDF edition are represented by explicit Unicode codes/color
  names; the editable report and raw evidence retain the exact symbols.
- The installed `$thesis-paper-report` skill matches its versioned copy and
  is discoverable in the available-skills catalog. Its YAML metadata,
  naming, required fields, invocation, and references passed equivalent
  checks using Ruby's existing YAML parser. The bundled Python validator
  could not run because PyYAML is unavailable; it is not claimed as passed.
- The manuscript, bibliography, dataset, numbered experiment entry points,
  and frozen library source remain unchanged. README and AGENTS contain
  the corrected evidence status and offline reproduction instructions.

## Reproduce locally

From the repository root:

```bash
python3 paper/report/prepare_snapshot.py tmp/research-report/snapshot \
  evidence/snapshots/2026-09-30-report --verify
python3 paper/report/analyze_evidence.py \
  --snapshot evidence/snapshots/2026-09-30-report \
  --output tmp/research-report/recheck
diff paper/report/generated/results_tables.md \
  tmp/research-report/recheck/results_tables.md
cd src
python3 -m unittest discover -s tests -q
```

The snapshot verification command uses only the destination when `--verify`
is supplied; the ignored working capture is not required to verify the backup.
No command above loads a model or submits a job.

## Experiment-centered guide addition

The updated assembled report has 71 pages and adds the approximately
4,000-word `experiment_guide.md` section before the verification instructions.
Removing that one insertion from the assembled Markdown reproduces the
previous assembled report exactly. The original narrative source, separate
sections, twelve discussion lenses, figures, and result tables are unchanged.

The new section incorporates the separately verified completed GPT-OSS
Step 13 artifact and distinguishes submitted Qwen follow-ups from completed
results. It makes no fresh live-queue claim. The rebuilt PDF has no extracted
replacement characters. All 71 pages were visually reviewed, including a
full-size check of the new methodology/results/discussion blocks. The full
95-test unit suite passes after the builder change.

## Self-contained experiment guide expansion (1 October 2026)

The rebuilt PDF has 162 pages. The experiment-centered addition spans pages
23--121 and contains approximately 50,000 words. Every block carries its own
procedures, settings, samples, complete available results, error and grid-check
tables, interpretations, alternatives, limitations and local verification.
The cross/control and ablation blocks reproduce saved request messages. The
binding and token-length blocks include exact ordered label inventories.
The main and revision plots also appear inside their experiment blocks.

The guide is generated by `build_experiment_guide.py` from
`experiment_guide_notes.md`, the unchanged original narrative, verified tables,
audit JSON and immutable request evidence. This avoids maintaining duplicate
numeric tables by hand. Qwen follow-ups remain explicitly unavailable in the
dated capture; no fresh scheduler claim is made. Step 13 includes the separately
backed-up GPT-OSS registry and distinguishes tokenized prompts from inference.

All 162 rendered pages were inspected in contact sheets, with full-size checks
of prompt inventories and cost/token tables. No clipped tables or replacement
characters were found. Both backup manifests pass all checksums (551 and five
stored evidence files). The full suite passes 99 tests, including four guide
coverage tests. Original narrative sections, twelve lenses, manuscript sources,
frozen experiment source and evidence artifacts are unchanged.
