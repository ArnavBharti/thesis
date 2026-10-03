# Main thesis paper

`paper.tex` is the main manuscript, using the supplied ACL style and the author details already present in this folder. Build from this directory with `make`. The compiled paper is written to `../output/pdf/thesis-main-paper.pdf`; temporary LaTeX files stay under `../tmp/main-paper/build/`.

The thesis outline supplies the research questions. `LLM_Course_Project_Paper_Template.pdf` guides the structure, experiment commentary, limitations, disclosure, and appendices. The verified `evidence/snapshots/2026-10-03-complete/` capture supplies both models' main and complete follow-up evidence, final analyses, and tokenizer registries. The central narrative is symbol-set performance and tests of candidate explanations. Cross-model ranking and its bootstrap interval remain secondary appendix context.

`generate_diagnostics.py` verifies all 599 snapshot files and generates both models' tokenizer and main length/parseability tables. `generate_followups.py` requires complete audited outcomes and generates all condition/tier tables, exclusive failure tables, and shared-initial revision transitions/costs. Both run locally without model loading. Generated tokens include hidden reasoning; only final grids are scored. Both token-length regressions are singular. Qwen's two-revision branch includes two initial-to-final regressions, so the paper does not claim a universal benefit from more revision.

`references.bib` holds manuscript references. `acl_latex.tex` is the compatible template entry point and loads `paper.tex`. Compile either entry point on Overleaf, with `paper.tex` selected by default. The style files are unchanged. The document uses ACL preprint mode for named authors and page numbers; this is a thesis manuscript, not a claim of acceptance or compliance with a specific venue's page limit.

The paper states the actual AI drafting assistance. Author review remains necessary before submission, including affiliation and authorship details, the acknowledgement, final venue rules, and publication metadata for preprints. No experiment settings, datasets, frozen plans, or earlier manuscript sources under `paper/` are changed.
