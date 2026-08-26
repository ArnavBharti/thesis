# Sudoku symbol-substitution experiments

This directory contains the complete reproducible pipeline for the thesis: the certified 300-puzzle corpus, all experiment case generators, local and OpenRouter inference backends, strict evaluation, resumable result storage, analysis, pinned model downloads, and Sharanga Slurm submission.

## Final model cohort

Only the two closed models use OpenRouter. The other three are downloaded from Hugging Face and run locally.

| Experiment name | Execution | Checkpoint | Sharanga request |
|---|---|---|---|
| `qwen-local` | local vLLM | `Qwen/Qwen3.8-27B` | 1 H100 80 GB |
| `glm-flash-local` | local vLLM | `zai-org/GLM-4.7-Flash` | 2 H100 80 GB |
| `kimi-linear-local` | local vLLM | `moonshotai/Kimi-Linear-48B-A3B-Instruct` | 2 H200 141 GB |
| `gpt-5.6-terra-openrouter` | OpenRouter, OpenAI route pinned | `openai/gpt-5.6-terra` | CPU job |
| `claude-sonnet-5-openrouter` | OpenRouter, Anthropic route pinned | `anthropic/claude-sonnet-5` | CPU job |

The exact GLM-5.2 and Kimi-K3 models named in the outline are not locally deployable on Sharanga: their published checkpoint files are approximately 1.5 TB each, exceeding even the aggregate 1.128 TB VRAM of an eight-H200 node before inference overhead. Kimi-K3 is a 2.8-trillion-parameter model. The configuration therefore uses official, feasible GLM- and Kimi-family replacements. This substitution is embedded in each frozen protocol manifest and must be disclosed in the thesis; results must not be labelled as GLM-5.2 or Kimi-K3 results.

The three snapshots are pinned by immutable Hugging Face commit SHA in [`config/experiments.json`](config/experiments.json). The local snapshots currently occupy approximately 55.6 GB, 62.4 GB, and 98.3 GB respectively.

## One-time Sharanga setup

Run these commands from `src` on a Sharanga login node. Python 3.10 or later is required.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[local]"
```

Use scratch storage for model weights because the three snapshots total more than 200 GB and Sharanga home storage is limited. Scratch files are temporary and may be purged after 15 days, so verify the cache before a run.

```bash
export HF_HOME="$SCRATCH/thesis-huggingface"
python download_models.py --cache-dir "$HF_HOME"
python download_models.py --cache-dir "$HF_HOME" --verify-only
```

`download_models.py` is idempotent. Hugging Face resumes partial downloads and reuses complete pinned snapshots. To inspect the plan without downloading:

```bash
python download_models.py --dry-run
```

Set the OpenRouter secret only in the shell; it is inherited by Slurm and never written to a generated job file.

```bash
export OPENROUTER_API_KEY="..."
```

Run the corpus pipeline once after transferring the repository. It fingerprints every step and reruns only stale or missing steps.

```bash
python run_pipeline.py
```

## Inspect and submit the experiments

First confirm request counts and locally cached checkpoints:

```bash
python run_experiments.py --action plan
python run_experiments.py --action probe
```

Generate the Slurm files, ask Slurm to validate their resource requests, then submit:

```bash
python submit_sharanga.py --action generate
python submit_sharanga.py --action test
python submit_sharanga.py --action submit
```

The submission command creates a dependency chain for each model:

```text
5-case qualification -> 24-way inference array -> token registry and analysis
```

Qualification must pass before the main array starts. The local models use the hardware-specific `gpu_h100_4` and `gpu_h200_8` partitions; OpenRouter calls use `compute`. GPU jobs request `--gres=gpu:N`, every payload is launched with `srun`, and all time limits are below Sharanga's 24-hour maximum.

The command is safe to run again. Existing JSONL results are append-only and identified by stable request IDs. `submit_sharanga.py` reads the frozen protocol and outputs, skips completed phases, and submits only unfinished phases. Check progress with:

```bash
python submit_sharanga.py --action status
```

That command exits with status 1 until all selected models are finished. To target one model, repeat `--model` as needed:

```bash
python submit_sharanga.py --action submit --model qwen-local
```

Do not use `--force` during a normal resume: it intentionally resubmits completed phases.

## Running without Slurm

If a model is already usable in the current process environment, run qualification and then the entire protocol with the same entry point:

```bash
python run_experiments.py --model qwen-local --experiments qualification
python run_experiments.py --model qwen-local --experiments all
```

The second command resumes qualification rather than repeating its calls. For explicit parallel execution, provide `--shard-index` and `--shard-count`; never run two processes with the same model, experiment, and shard index.

## Experiment coverage

| Outline step | Implementation |
|---|---|
| Experiment 1 | Certified corpus, uniqueness audit, difficulty certificates |
| Experiment 2 | Pilot subsets and difficulty calibration summary |
| Experiment 3 | Unicode and exact local-tokenizer representation registry |
| Experiment 4 | Full 300 × 9 symbol-condition main experiment |
| Experiment 5 | Paired retention, failure rates, and exact McNemar analysis |
| Experiment 6 | Input/output symbol crosses and non-Sudoku controls |
| Experiment 7 | Token-length-matched symbols and logistic regression |
| Experiment 8 | Explicit mappings and semantic-conflict conditions |
| Experiment 9 | Formatting and prompt ablations |
| Experiment 10 | Self-revision and checker-guided revision trajectories |

Exact tokenizer access is required to construct Experiment 7. It runs for all three local models. OpenRouter does not expose the exact GPT/Claude tokenizer, so those model/experiment cells are explicitly recorded as `NOT_RUN_NO_EXACT_TOKENIZER_ACCESS`; they are not silently approximated.

## Outputs and invariants

Runtime outputs are written below `experiment_outputs/<run_id>/<model>/` and ignored by Git. Each model directory contains:

- `protocol-manifest.json`: dataset hash, model revision, request counts/digests, inference settings, and substitutions; immutable once created.
- `provenance.json`: Git, Python, package, host, and accelerator metadata.
- `qualification-status.json`: the five-case gate.
- `exp*/shard-*.jsonl`: append-only requests, raw generations, provider metadata, evaluations, and retry status.
- `analysis/summary.json` and `analysis/observations.jsonl`: derived results.

Changing the dataset, prompts, model config, tokenizer, or inference settings after a protocol has frozen raises an error. Make intentional protocol changes under a new `run_id`.

## Useful local validation

```bash
python -m unittest discover -s tests -v
python -m compileall -q experiments sudoku *.py
git status --short
```

References: [Sharanga hardware configuration](https://sharanga.hpc.bits-hyderabad.ac.in/docs/misc_docs/configuration/), [Sharanga GPU job rules](https://sharanga.hpc.bits-hyderabad.ac.in/docs/faq/jobs/gpu/), [Sharanga CUDA partitions](https://sharanga.hpc.bits-hyderabad.ac.in/docs/faq/software/cuda/), [Sharanga storage policy](https://sharanga.hpc.bits-hyderabad.ac.in/docs/faq/storage/), [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B), [GLM-4.7-Flash](https://huggingface.co/zai-org/GLM-4.7-Flash), [Kimi-Linear-48B-A3B-Instruct](https://huggingface.co/moonshotai/Kimi-Linear-48B-A3B-Instruct), [GLM-5.2](https://huggingface.co/zai-org/GLM-5.2), [Kimi-K3](https://openrouter.ai/moonshotai/kimi-k3), [GPT-5.6 Terra on OpenRouter](https://openrouter.ai/openai/gpt-5.6-terra), and [Claude Sonnet 5 on OpenRouter](https://openrouter.ai/anthropic/claude-sonnet-5).
