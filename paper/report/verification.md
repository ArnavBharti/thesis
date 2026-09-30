# Final report verification

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
