---
name: thesis-paper-report
description: Prepare or use Arnav Bharti's Sudoku-thesis paper-writing dossier, verify experimental claims, refresh result summaries, and apply the supplied BITS Pilani research-writing guidance. Use for this thesis's abstract, introduction, related work, methodology, results, discussion, conclusion, or evidence-backed manuscript review.
---

# Thesis paper report

Support the user writing their own research paper. Do not replace their manuscript or rewrite `paper/draft.tex` unless asked. The maintained dossier is in `/Users/arnavbharti/Developer/arnavbharti/thesis/paper/report/`.

## Read the relevant evidence first

Read the repository's `AGENTS.md` for current authorization and server rules. Read `paper/report/writing_report.md` for the section being written and the methodological corrections. Use `paper/report/generated/results_tables.md`, `detailed_appendix.md`, and `audit.json` for exact numbers and completion status. The lossless raw snapshot is under `evidence/snapshots/2026-09-30-report/`; its manifest contains compressed and raw-content checksums. Do not treat this dated snapshot as live scheduler state.

For writing structure and submission checks, read [references/writing-guidance.md](references/writing-guidance.md). For report refresh, use the offline scripts documented below. For literature, use the dossier's canonical links, recheck changed publication metadata, and verify authors/title/year/venue before final citation. Do not call the report an exhaustive systematic review.

## Claim boundaries that change decisions

- Main observations are the same 60 underlying puzzles times nine alphabets per model, not 540 independent puzzles. Pilot uses 15 other puzzles times four alphabets.
- Distinguish incomplete shards from completed wrong answers. A completion claim needs marker/count agreement and the exact request-ID digest. Do not put partial Qwen main accuracy into final manuscript prose.
- Main GPT-OSS and Qwen prompts use ordinary generation with strict final-grid scoring, not regex-constrained decoding or the old internal-verification paragraph. Check saved messages rather than historical prompt summaries.
- Hidden reasoning is unscored but consumes generation tokens and context. There is no demonstrated local 600-second per-request timeout. Effective temperature/top-p are 1/1 after overrides.
- GPT-OSS frozen main profile uses 192 GB host RAM. Its recorded later mechanism jobs use 96 GB. Qwen uses 96 GB. Read exact `.sbatch` and scheduler evidence before stating resources.
- Error labels overlap. Use exclusive outcome categories for stacked tables and plots. Evaluate clue preservation only when the final grid can be parsed. Valid Sudoku units do not imply original clues were preserved.
- Reused mechanism baselines and shared revision initials are not fresh independent calls. Revision cost includes the initial generation plus every new stage, not just the final stage latency.
- Difficulty is relative to the registered technique procedure, not human validation or a proof that all methods require search.
- Token-length results are non-monotonic and the registered regression is singular. Small binding/ablation differences do not establish causality. Identical ablation prompts yielded different sampled scores.
- Do not claim Qwen mechanism replication without completed corresponding evidence. Do not infer a universal model reasoning limitation from historical budget-limited screens.
- Only the extracted final Sudoku grid is scored. Do not analyze or quote reasoning traces to explain cognition.

## Offline verification and refresh

From the repository root, run:

```bash
python3 paper/report/prepare_snapshot.py tmp/research-report/snapshot \
  evidence/snapshots/2026-09-30-report --verify
python3 paper/report/analyze_evidence.py \
  --snapshot evidence/snapshots/2026-09-30-report \
  --output tmp/research-report/recheck
```

The audit must show a valid dataset and no evaluation/independent-grid disagreements. For an authorized fresh report, first copy only experiment outputs and relevant Slurm metadata to a new local capture. Never load models, install packages, or run audits on the login node. Ask for SSH unlock if authentication/banner stalls. Do not refresh a dated snapshot silently or replace an immutable frozen source artifact.

Create a new dated evidence snapshot with `prepare_snapshot.py`, then regenerate tables with `analyze_evidence.py` and figures/appendices with `build_assets.py`. These helpers do not run inference. Use `paper/report/build_report.py` to assemble and render the report after reviewing its dependencies and the PDF skill if available. Update narrative claims to the verified capture and visually inspect the rendered PDF. Keep pending/not-run status in the dossier, but write completed findings in standard final-draft technical English without the label “preliminary.”

## Scope and handoff

Skill invocation does not authorize new jobs, downloads, installation, API models, cancellation, or frozen-protocol changes. A writing request authorizes local analysis and evidence-backed artifact creation. Do not spawn agents unless separately authorized. Preserve unrelated work. Test relevant local changes and the full repository suite before committing and pushing, as required by `AGENTS.md`.

Deliver the requested section guidance or updated report, the exact evidence location, and important completion/interpretation limits. Let the user remain the paper's author.
