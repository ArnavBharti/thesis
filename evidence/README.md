# Experiment evidence backup

This directory is the repository-backed copy of irreplaceable evidence produced on
Sharanga. Raw JSONL files and completed Slurm text logs are gzip-compressed without
modification. Protocol files, sample plans, provenance, request manifests,
completion markers, summaries, and Slurm submission files retain their original
relative layout.

The complete capture is `snapshots/2026-10-03-complete/`: 599 files with
stored-file and raw-content SHA-256 checksums. It includes both models'
qualification, pilot, main, input/output cross, token length, binding, ablations,
revision, final analyses, tokenizer registries, and relevant job metadata. Its
offline audit checks 2,650 selected/historical outcome records without errors.
Earlier snapshots remain unchanged. GPT-OSS's ablation marker was written before
the teardown timeout; Qwen's follow-up jobs all completed with exit `0:0`.

The following scratch-only material is intentionally excluded because it is
reproducible or secret: model weights, Hugging Face and package caches, virtual
environments, compiled files, and `.env` credentials.

To verify this capture locally without inference:

```bash
python3 paper/report/prepare_snapshot.py tmp/research-report/unused \
  evidence/snapshots/2026-10-03-complete --verify
python3 paper/report/analyze_evidence.py \
  --snapshot evidence/snapshots/2026-10-03-complete \
  --output tmp/research-report/recheck
```
