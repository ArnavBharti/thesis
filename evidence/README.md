# Experiment evidence backup

This directory is the repository-backed copy of irreplaceable evidence produced on
Sharanga. Raw JSONL files and completed Slurm text logs are gzip-compressed without
modification. Protocol files, sample plans, provenance, request manifests,
completion markers, summaries, and Slurm submission files retain their original
relative layout.

The backup currently contains the completed GPT-OSS qualification, pilot, all six
main-benchmark shards, input/output cross, token length, binding, and prompt/output
ablations. Add each later experiment only after its completion marker and Slurm
terminal state have been verified. The ablation results and completion marker were
written before Slurm terminated the job during backend teardown at its wall-time.

The following scratch-only material is intentionally excluded because it is
reproducible or secret: model weights, Hugging Face and package caches, virtual
environments, compiled files, and `.env` credentials.

To read a compressed result file without extracting it:

```bash
gzip -cd evidence/experiment_outputs/local-models-v1/gpt-oss-120b-local/exp4/shard-000-of-006.jsonl.gz | head
```
