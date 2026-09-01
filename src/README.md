# Sudoku experiments

This project tests how language models solve Sudoku when the digits are replaced by other symbols.

Run the numbered Python scripts in `steps/`. Each submission script sends only one Slurm job. It never submits an array or a chain of jobs.

## Project layout

```text
src/
├── steps/          Commands that you run, in order
├── sudoku/         Shared Sudoku generation and checking code
├── experiments/    Shared model, prompt, evaluation, Slurm, and analysis code
├── config/         Model and experiment settings
├── data/           The certified 300-puzzle dataset
└── tests/          Automated tests
```

The files in `steps/` are small wrappers. The shared code is grouped by purpose in `sudoku/` and `experiments/`. This avoids duplicate code and keeps each file focused.

Run every command below from the `src` directory.

## Models

| Name used by the scripts | How it runs |
|---|---|
| `qwen-local` | Local Qwen3.8-27B on 1 H100 |
| `glm-flash-local` | Local GLM-4.7-Flash on 2 H100s |
| `kimi-linear-local` | Local Kimi-Linear-48B-A3B on 2 H200s |
| `gpt-5.6-terra-openrouter` | OpenRouter with the OpenAI provider fixed |
| `claude-sonnet-5-openrouter` | OpenRouter with the Anthropic provider fixed |

The research outline named GLM-5.2 and Kimi-K3. Their published model files are too large for a normal Sharanga job. This project uses smaller official models from the same families. The replacement is recorded in the experiment manifest. Do not report their results as GLM-5.2 or Kimi-K3 results.

## One-time setup

Create a Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[local]"
```

Store model files in Sharanga scratch space. The three local models need more than 200 GB.

```bash
export HF_HOME="$SCRATCH/thesis-huggingface"
```

Set the OpenRouter key before submitting GPT or Claude jobs:

```bash
export OPENROUTER_API_KEY="your-key"
```

Slurm inherits these environment variables when you submit a job. Set them again after a new login.

## Step 1: prepare the Sudoku data

```bash
python steps/01_prepare_data.py
```

This runs the tests, creates 300 puzzles, and audits the dataset. It skips work that is already complete and unchanged.

Check its status without running anything:

```bash
python steps/01_prepare_data.py --status
```

## Step 2: download the local models

```bash
python steps/02_download_models.py --cache-dir "$HF_HOME"
```

The download can be run again. Existing files are reused. Verify the files without downloading:

```bash
python steps/02_download_models.py --cache-dir "$HF_HOME" --verify-only
```

## Step 3: check the setup

```bash
python steps/03_check_setup.py
```

It checks the dataset, local model cache, and `OPENROUTER_API_KEY`. A missing item is printed as `MISSING`.

## Step 4: qualify one model

Submit one small qualification job:

```bash
python steps/04_submit_qualification.py qwen-local
```

Replace `qwen-local` with another model name when you are ready to test that model. The main experiments cannot run until its five qualification puzzles are correct.

To inspect the generated job without submitting it:

```bash
python steps/04_submit_qualification.py qwen-local --dry-run
```

To ask Slurm to validate the job without submitting it:

```bash
python steps/04_submit_qualification.py qwen-local --test-only
```

## Step 5: submit one experiment job

Most experiments use one job:

```bash
python steps/05_submit_experiment.py qwen-local exp2
python steps/05_submit_experiment.py qwen-local exp6
python steps/05_submit_experiment.py qwen-local exp7
python steps/05_submit_experiment.py qwen-local exp8
python steps/05_submit_experiment.py qwen-local exp9
python steps/05_submit_experiment.py qwen-local exp10
```

Experiment 4 has 2,700 requests. It is divided into 24 parts so each job can stay below Sharanga's 24-hour limit. Submit one part, wait for it to finish, and then submit the next part:

```bash
python steps/05_submit_experiment.py qwen-local exp4 --part 1
python steps/05_submit_experiment.py qwen-local exp4 --part 2
```

Continue through `--part 24`.

Experiment 7 needs the exact model tokenizer. It runs for the three local models. It is skipped for GPT and Claude because their exact tokenizers are not available through OpenRouter.

Every completed part has a small completion file. If you run the same command again, the script prints `SKIP`. If a job stops early, run the same command again. Completed requests are not repeated.

## Step 6: check what to run next

You can run the status script at any time:

```bash
python steps/06_show_status.py
```

For one model:

```bash
python steps/06_show_status.py --model qwen-local
```

It prints completed parts and the exact next command.

## Step 7: finalize one model

After every required experiment job for a model is complete, run:

```bash
python steps/07_submit_finalization.py qwen-local
```

This submits one CPU job. It creates the token registry and final analysis files. Experiment 5 is calculated from the paired Experiment 4 results during this step.

## Number of jobs

The complete five-model study uses 158 jobs when Experiment 4 has 24 parts:

- 96 jobs for the three local models.
- 62 jobs for GPT and Claude.

You submit these jobs one at a time. You do not need to submit every model or experiment in one session.

## Output files

Results are stored in:

```text
experiment_outputs/thesis-confirmatory-v1/<model-name>/
```

Important files are:

- `protocol-manifest.json`: frozen dataset, model, prompt, and request information.
- `provenance.json`: Git, Python, package, host, and GPU information.
- `qualification-status.json`: qualification result.
- `exp*/shard-*.jsonl`: raw responses and evaluations.
- `analysis/summary.json`: final summary.

Result files are append-only. Request IDs are stable. Do not manually edit the result files.

If you intentionally change the dataset, models, prompts, or inference settings, change `run_id` in `config/experiments.json`. This keeps the old and new studies separate.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Sharanga references

- [GPU job instructions](https://sharanga.hpc.bits-hyderabad.ac.in/docs/faq/jobs/gpu/)
- [GPU and node configuration](https://sharanga.hpc.bits-hyderabad.ac.in/docs/misc_docs/configuration/)
- [GPU partition names](https://sharanga.hpc.bits-hyderabad.ac.in/docs/faq/software/cuda/)
- [Scratch storage policy](https://sharanga.hpc.bits-hyderabad.ac.in/docs/faq/storage/)
