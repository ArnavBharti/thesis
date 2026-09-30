# Experiment-by-experiment writing guide: methodology, results, and discussion

This is the self-contained experiment-centered route through the dossier. Each block includes the applicable exact procedures, sample identities, settings, saved prompts or label inventories, complete available results, interpretation, alternatives, limitations, and local verification steps. You do not need to consult the separate Methodology, Results, or Discussion sections to write an experiment account. Those original sections and all twelve discussion lenses remain preserved for another reading route. The repeated material here is deliberate. No missing experiment result is inferred from a submission or a different experiment.

**Evidence boundary.** Main and mechanism numbers below come from the verified `2026-09-30-report` snapshot. GPT-OSS Step 13 subsequently completed in job `373562`, with a separate verified local backup. Qwen Steps 8--12 and dependent Step 13 were subsequently queued. Their submission is not a result: this guide contains no completed Qwen follow-up outcomes. “Not available” below means unavailable in the verified evidence used here, not a fresh claim about the live queue. Refresh and audit those outputs before replacing these entries. Do not pool new follow-ups into main accuracy.

## A. Dataset construction and difficulty certification

### Methodology, rationale, alternatives, and limitations

Explain the data source before the model experiments. Generate complete Sudoku grids with seeded randomized search, remove clues while retaining exactly one solution, and accept candidates only when their deterministic difficulty certificate matches the requested tier. Retain 100 puzzles per tier. Store seed, clue mask, exact solution, uniqueness and difficulty certificates, and hashes. Re-execute certification locally rather than accepting a file count as validation.

The reason for unique solutions is that an exact reference comparison must not reject another legitimate completion. The reason for procedural tiers is to distinguish puzzles handled by singles, puzzles requiring the implemented intermediate techniques, and puzzles on which that technique procedure stalls. The reason for seeded generation is reproducibility, not a guarantee of a representative sample of all Sudoku.

Why not define difficulty only by clue count? Different logical structures can occur at similar clue counts. Why not claim human difficulty? No human study was performed. Why not say every hard puzzle universally requires backtracking? Search is needed relative to the implemented technique set, not necessarily every stronger logical solver. Exact-grid deduplication also does not exclude symmetry-equivalent puzzles.

Selection produces a disjoint 15-puzzle pilot and 60-puzzle main sample. Mechanism and ablation subsets contain 15 and nine puzzles nested in the main sample. These nested sets enable baseline reuse but are not new held-out test sets. The main and follow-up answers therefore have a shared evidential origin.

### GPT-OSS and Qwen evidence

Both models use the same certified dataset and the same 60 main puzzle IDs. All 300 records pass the local dataset audit. Actual clue ranges and medians are easy 40--46, median 43; medium 24--28, median 26; hard 23--27, median 25. These are dataset properties, not model scores. All accepted easy puzzles are solved by naked singles in the registered analyzer.

### Discussion and writing decision

This construction makes within-puzzle relabeling a strong control for the abstract task. It does not make easy-versus-hard comparisons randomized interventions on one difficulty variable. Discuss this under **Lens 2: difficulty interaction** and **Lens 12: reproducibility and evaluation design**. Place certification and sample construction in Methodology, summarize the audit briefly, and avoid presenting dataset validation as evidence of model reasoning.

## B. Timing diagnostics, qualification, and pilot

### Methodology, rationale, alternatives, and limitations

Distinguish three operations. Timing diagnostics estimate feasibility on one puzzle per difficulty. Qualification checks five easy puzzles assigned five representations. The pilot evaluates 15 different puzzles, five per tier, in four alphabets: Arabic digits, Greek letters, uppercase Latin, and emoji. It produces 60 requests per model.

The purpose is to identify workable local configurations and estimate runtime before freezing the main benchmark. GPT-OSS qualification required 5/5 with zero operational failures. Qwen's approved threshold was 3/5 with zero operational failures. Both actually achieved 5/5. Do not rewrite the qualification rule after observing their perfect scores, or say perfect easy performance was a general scientific inclusion requirement.

The pilot is not the main benchmark. Do not combine its requests with main requests to increase the denominator. Do not treat its representation ranking as a basis for selectively omitting an inconvenient main alphabet. The observed qualification IDs are disjoint from pilot/main IDs, but this is a verified property of these runs rather than an unconditional property of every historical screening procedure.

Hidden reasoning is permitted, separated from the scored final response, and still consumes generation/context capacity. A job wall-time is not a measured per-puzzle thinking deadline. A single timing success cannot establish tier-wide accuracy. Initial short-budget Qwen screens are not directly comparable to the later configuration because sampling settings also changed.

### GPT-OSS results

The one-puzzle timing diagnostic is correct at all three difficulties: 36.12 seconds easy, 254.59 medium, and 227.35 hard. Qualification is 5/5. Pilot correctness is 47/60: easy 20/20, medium 13/20, hard 14/20. Alphabet counts are Arabic 14/15, emoji 13/15, Greek 10/15, uppercase Latin 10/15. Mean latency is 252.48 seconds. There are two truncations and no request-level operational failures.

### Qwen results

The initial 32,768-context screen solves easy in 80.48 seconds, while medium and hard fill the available context and fail. The larger-context medium rerun is correct in 387.20 seconds. Qualification is 5/5. Pilot correctness is 54/60: easy 20/20, medium 16/20, hard 18/20. Arabic, Greek, and emoji each score 13/15; uppercase Latin scores 15/15. Mean latency is 452.30 seconds. There are two truncations and no operational failures.

### Discussion and writing decision

Both selected configurations are operationally feasible and proceed to the frozen main benchmark. Qwen's pilot is more accurate and slower, but the main paired experiment is the appropriate source for the paper's model comparison. The early context-limited failures motivate separating resource exhaustion from wrong completed grids. They do not prove more tokens always rescue failure. Use **Lenses 5, 11, and 12**. Screening histories belong mainly in the execution appendix because they use unequal settings and create model-selection limitations.

## C. Main symbolic-representation benchmark and paired retention

### Methodology, rationale, alternatives, and limitations

Evaluate the same 60 puzzles, 20 per tier, under nine bijective alphabets for each model. Relabel all clues and the reference solution consistently, without changing cell positions or abstract constraints. This yields 540 requests per model and 1,080 matched-model observations, but only 60 underlying main puzzles. There is one sampled completion per puzzle/alphabet/model cell, not repeated-seed estimation of each prompt's success probability.

Use pinned model revisions, native reasoning/final-answer conventions, effective temperature 1 and top-p 1, and 131,072-token context/output ceilings. GPT-OSS uses `high` and Qwen `xhigh` reasoning controls. Those controls are not calibrated equal-compute treatments. Main generation is not regex-constrained. Evaluate only the extracted final grid under strict formatting, alphabet, clue, row, column, box, and unique-solution checks.

Why pairing? It prevents differences in the underlying Sudoku from explaining within-puzzle alphabet comparisons. Why preserve output errors in the denominator? The final-answer contract is part of deployed success. Why not rank only parsed grids? That selects a different denominator and can conceal practical failures. Why not compare all 540 cells as independent samples? Nine conditions share one puzzle.

Report mutually exclusive outcomes alongside overlapping diagnostic labels. Compute Arabic-baseline conditional retention and paired discordances, not accuracy alone. The registered retention analysis uses exact McNemar comparisons. The report adds exploratory Holm adjustment over eight alphabet contrasts per model and a 10,000-replicate stratified puzzle-cluster bootstrap for the paired model difference. Do not describe these additions as amendments made before data collection.

### GPT-OSS results

Correctness is 372/540 (68.9%): easy 171/180, medium 121/180, hard 80/180. Exclusive failures comprise 96 nontruncated incorrect grids, 24 truncations, and 48 other output errors, with zero operational errors. Of 468 parseable grids, 454 preserve every clue and 377 satisfy all Sudoku units. Five unit-valid grids are nevertheless wrong for the supplied clues.

Alphabet scores are Arabic 45/60, uppercase Latin 45/60, lowercase Latin 44/60, Bengali 43/60, nonce 43/60, Devanagari 39/60, abstract symbols 38/60, emoji 38/60, and Greek 37/60. Arabic and uppercase Latin have equal aggregate scores but nine Arabic-only and nine uppercase-only successes. Equal accuracy therefore does not establish puzzle-level invariance. No Arabic-baseline contrast survives the report's Holm adjustment.

Mean generation latency is 290.81 seconds. Total recorded generation time is 43.62 hours and total completion tokens are 29,568,276. These exclude checkpoint loading and queue waiting and are not energy or monetary costs.

### Qwen results

Correctness is 472/540 (87.4%): easy 174/180, medium 160/180, hard 138/180. Exclusive failures comprise 33 nontruncated incorrect grids, 24 truncations, and 11 other output errors, with zero operational errors. Of 505 parseable grids, 488 preserve all clues and 487 satisfy all units. Fifteen unit-valid grids are wrong for the supplied clues.

Alphabet scores are Devanagari 56/60, uppercase Latin 55/60, emoji 54/60, Arabic 53/60, Bengali 53/60, abstract symbols 51/60, Greek 51/60, lowercase Latin 51/60, and nonce 48/60. No Arabic-baseline contrast survives Holm adjustment. Mean generation latency is 531.25 seconds, total recorded generation time is 79.69 hours, and completion tokens total 21,910,495.

### Discussion and writing decision

Use the complete paired comparison: 338 cells correct for both models, 34 GPT-OSS only, 134 Qwen only, and 34 neither. Qwen's observed advantage is 18.52 percentage points, with exploratory puzzle-cluster bootstrap interval 13.70--23.52. Its net advantage is three easy, 39 medium, and 58 hard answers. This supports an accuracy-latency trade-off between the recorded configurations, not universal Qwen dominance, a parameter-count scaling law, or an equal-compute comparison.

The alphabet rankings differ numerically, but neither model has a Holm-significant Arabic contrast. Do not turn this into proof that representation never matters. Conversely, observed pair disagreements cannot be attributed wholly to notation without repeat-prompt controls at main scale. The union of saved correct answers is 506/540, but no ensemble-selection system was evaluated.

Use **Lenses 1--6, 11, and 12**, especially the separation of format, valid units, and clue preservation. The main experiment should anchor the paper. Use the heatmap, exclusive error plot, paired counts, and latency table to introduce the narrower questions tested below.

## D. Input/output cross and simple controls: Step 8, experiment exp6

### Methodology, rationale, alternatives, and limitations

On the 15 nested mechanism puzzles, compare Arabic-to-Arabic, Greek-to-Greek, Greek-to-Arabic, and Arabic-to-Greek. Reuse 30 matching main baselines, make 30 cross-Sudoku calls, and add 75 no-solving controls. The controls test copying, fixed mapping translation, coordinate retrieval, occurrence counting, and conversion of a supplied completed grid. There are 135 saved outcomes but only 105 new calls.

The rationale is to test narrow alternatives to a constraint-solving failure: inability to copy Greek symbols, apply a fixed mapping, or manipulate a supplied grid. Why not interpret perfect controls as perfect input understanding? They remove the solving burden and sometimes have fixed answers. Why not call the cross comparison a pure output-alphabet intervention? The cross prompts also add explicit mapping instructions and conversion requirements. These differences are part of the treatment.

Use Sudoku-only and control-only denominators. The same-alphabet baselines are reused responses, not independent replications. The 15 puzzles are nested in main, and five per tier limit each difficulty-specific inference.

### GPT-OSS results

All 135 records are complete. Same-alphabet Sudoku conditions score 12/15 each; Greek-to-Arabic scores 10/15 and Arabic-to-Greek 11/15. Sudoku-only total is 45/60, with easy 19/20, medium 18/20, hard 8/20. Each Sudoku condition scores 2/5 hard. All 75 controls pass. Two responses truncate, with zero operational failures. The mixed 120/135 total is not a Sudoku-only accuracy measure.

### Qwen results

No completed Step 8 evidence is included here. Job `373543` was submitted for the same design with model-specific baseline reuse. Do not fill its cells from Qwen's main Greek/Arabic aggregate scores: the cross prompts require new calls and the mechanism subset has different denominators.

### Discussion and writing decision

Basic control success narrows simple symbol-handling explanations, while full solving still fails. Baseline equality on this subset does not support a deterministic universal Greek-output penalty. Lower cross scores are consistent with extra mapping burden but do not isolate its cause. Use **Lens 8**, with **Lenses 2, 3, and 7** as alternatives. Once verified Qwen outcomes exist, compare condition patterns, not just mixed totals, before claiming replication.

## E. Token-length labels: Step 9, experiment exp7

### Methodology, rationale, alternatives, and limitations

Use each model's pinned tokenizer to construct nine labels with one token, nine with two, and nine with three. Require equal isolated and leading-space token length. Apply the three alphabets to the same 15 mechanism puzzles, making 45 new calls. Record prompt tokens, mean clue tokens, UTF-8 bytes, and code points.

The motivation is to probe a tokenization-related explanation raised by the main alphabets. Why not infer token-length effects directly from Greek versus Arabic? Their spelling, familiarity, and Unicode properties also differ. Why not call the constructed bins a clean causal manipulation? Bin assignment also changes label identity, and only one alphabet per bin is evaluated. Whole-row tokenization can differ from isolated-label tokenization.

The registered regression includes prompt tokens and the three clue/symbol measures. Its identifiability must be checked before interpreting coefficients. Qwen and GPT-OSS use different tokenizers, so their bins need not contain the same labels. A comparison concerns model-specific token-length constructions, not necessarily identical visible prompts.

### GPT-OSS results

One-, two-, and three-token conditions score 9/15, 13/15, and 10/15. Difficulty totals are easy 15/15, medium 13/15, hard 4/15. Hard-bin scores are 0/5, 3/5, and 1/5. There are five truncations, four other output errors, four incorrect grids, and zero operational failures. The registered 45-observation regression has a singular information matrix.

### Qwen results

No completed Step 9 evidence is included. Job `373544` was submitted. Verify its constructed label inventory, tokenizer identity, 45-request completion, and fit status before adding a comparison. Do not assume its fitted regression will be identifiable merely because Qwen's main accuracy is higher.

### Discussion and writing decision

GPT-OSS's pattern is non-monotonic and does not identify an independent token-length coefficient. State both facts, rather than hiding the failed fit or claiming two tokens are inherently optimal. Specific labels and correlated prompt properties remain explanations. Use **Lens 6**, supported by **Lenses 5 and 12**. Multiple alphabets per bin and matched repeated sampling would strengthen a future design, but were not performed here.

## F. Binding and label assignment: Step 10, experiment exp8

### Methodology, rationale, alternatives, and limitations

Evaluate 11 conditions on the same 15 mechanism puzzles: standard uppercase and five fixed seeded uppercase permutations, ordinary and permuted digits, ordinary and permuted English number words, and nonce labels. Reuse standard-uppercase, ordinary-digit, and nonce main outcomes. This yields 165 records, 45 reused baselines, and 120 new calls.

The same uppercase vocabulary across permutations helps distinguish assignment sensitivity from changing the vocabulary itself. Ordinary/permuted number words probe a possible familiar-association explanation. However, the prompt does not explicitly define a conflicting arithmetic relation such as `ONE=7`. The labels render abstract values, and Sudoku constraints depend on consistent equality. Describe the perturbation accurately rather than claiming explicit arithmetic disobedience.

Five fixed permutations are not an exhaustive or independently resampled distribution over assignments. Ordering, specific puzzle structure, and generation variability remain alternatives. Reused baselines also share dependence with the main experiment. Report condition counts and paired disagreements rather than converting a two-answer difference into a general causal percentage effect.

### GPT-OSS results

All 165 records are complete, with 124 correct. Easy is 55/55, medium 50/55, hard 19/55. Ordinary digits, ordinary number words, and nonce labels each score 12/15. Permuted digits and permuted number words each score 10/15. Uppercase assignments range from 10/15 to 13/15. There are seven truncations, two other output errors, 32 nontruncated incorrect grids, and no operational failures.

### Qwen results

No completed Step 10 evidence is included. Job `373545` was submitted. Its reused baseline cells must match the saved Qwen main answers. Its new permutations and number-word conditions must be evaluated before any statement about cross-model semantic interference.

### Discussion and writing decision

The GPT-OSS pattern is consistent with assignment-related sensitivity, but small differences and familiar-label contrasts do not identify an internal binding mechanism. Do not claim neutral nonce labels eliminate all semantics. Use **Lens 7**, with **Lenses 1, 6, and 9** for competing explanations. A useful two-model discussion would ask whether paired losses recur under matched assignments after both runs are verified, not assume the same mechanism from aggregate main accuracy.

## G. Prompt and output ablations: Step 11, experiment exp9

### Methodology, rationale, alternatives, and limitations

Use nine nested puzzles, three per tier, across 19 fresh conditions: four rule styles, three mapping styles, four output formats, four empty markers, and four case/alphabet variants. Most use Greek. Normalize compact rows, 81-symbol strings, and JSON under their registered contracts before checking Sudoku. This is an exploratory suite, not a complete factorial experiment.

The purpose is to explore whether practical instruction and interface choices might explain or alleviate failure. Why not select the best observed prompt immediately? Nine puzzles are a small development set and choosing its maximum incurs selection bias. Why not interpret every condition label as a different treatment? Four labels generate identical default prompts. They are useful variability checks, not four distinct prompt interventions.

Fixed recorded sampling seed does not establish deterministic outcome reproduction. Identical prompt scores can differ through generation/runtime behavior whose source these final-grid records do not isolate. Alternate output contracts also change parsing expectations, so separately report contract compliance and Sudoku correctness rather than evaluating every format against spaced rows.

### GPT-OSS results

All 171 records and the completion marker exist, despite the scheduler killing teardown at the 15-hour limit. The saved records have zero operational failures. Correctness is 103/171, with easy 55/57, medium 37/57, hard 11/57, and 12 truncations. Digit mapping and uppercase nonce each score 8/9. Compact rows and string81 each score 3/9. Identical-default-prompt conditions score 5/9, 6/9, 5/9, and 7/9.

### Qwen results

No completed Step 11 evidence is included. Job `373546` was submitted. Require all 171 request IDs and the marker, then inspect own-format compliance, tier counts, and identical-prompt outcomes. A scheduler timeout must be interpreted alongside saved artifact completeness, not automatically counted as 171 failed requests.

### Discussion and writing decision

The identical-prompt variation cautions against attributing a small difference to wording. No variant establishes a universally superior main prompt. A high score can motivate a separately documented repeat experiment, not a retrospective change to the frozen benchmark. Use **Lens 9**, with **Lenses 3 and 12**. Preserve the full condition table in an appendix to avoid highlighting only favorable variants.

## H. Shared-initial self-revision and checker feedback: Step 12, experiment exp10

### Methodology, rationale, alternatives, and limitations

Take nine puzzles under Arabic, Greek, and emoji, giving 27 saved main initial answers. Branch each into one pass, one self-revision, two self-revisions, and conditional checker-guided revision. The resulting 108 outcome records share 27 initial generations. Generic revisions run regardless of initial correctness; the checker arm runs only on initial failures and supplies constraint/format violations, not the full solution.

The shared initial answer makes branch differences easier to interpret than independently generated initial solves. The reason for counting fixes and regressions is that an unchanged aggregate score can conceal both. The reason for cumulative cost is that final-stage latency alone omits prior computation.

Why not infer pure self-correction ability? Additional computation and another sampled generation are confounded with revision. Why not call the checker and generic arms equal treatments? The checker provides extra information and selects only initial failures. Its stopping rule protects initial successes. No equal-compute resampling, best-of-n, or majority-vote baseline was evaluated.

Report initial plus new-stage generation time, new-call counts, and unique-source or clearly labeled stage-level truncations. Repeated copies of an initial truncated response are not separate inference failures. Twenty-seven branch cells remain clustered within nine puzzles.

### GPT-OSS results

Final counts are one pass 18/27, one self-revision 19/27, two self-revisions 23/27, and checker-guided revision 22/27. They fix zero, one, five, and four initial failures, with no observed regressions. New-call counts are zero, 27, 54, and nine. Mean cumulative generation time is 312.25, 482.60, 610.69, and 476.68 seconds respectively. The 108 final records contain three truncations and no operational failures; all-stage incidence uses a different accounting unit.

### Qwen results

No completed Step 12 evidence is included. Job `373547` was submitted. Calculate its own 27-cell initial-correct count before interpreting revisions. Do not reuse GPT-OSS's nine-failure checker denominator: Qwen's initial answers may have a different number of errors. Report ceilings for improvement and the number of errors actually eligible for repair.

### Discussion and writing decision

Two generic revisions and conditional checker feedback improve realized GPT-OSS correctness on this subset. That supports a practical observed trade-off, not a universal revision benefit. One answer changes an arm by 3.7 percentage points. If Qwen starts nearer ceiling, fewer fixes may reflect fewer opportunities rather than inferior correction ability. Compare wrong-to-right and right-to-wrong transitions, denominators, and added time. Use **Lens 10**, supported by **Lenses 5, 11, and 12**.

## I. Final analysis and reproducibility: Step 13

### Methodology, rationale, alternatives, and limitations

Step 13 is CPU-only token diagnostics and saved-result analysis, not another inference experiment. It verifies prerequisites and the frozen protocol, loads the pinned local tokenizer, writes symbol/prompt diagnostics, and summarizes recorded outcomes, retention, token-length regression, and revisions. Do not count it as an additional set of model answers.

The broad source guard initially rejected GPT-OSS because later Qwen timing/qualification support changed three hashed files. A precise comparison showed that configuration and sample plan still matched after JSON normalization. Rather than relaxing the guard, execute the unchanged numbered script from the exact frozen commit `2cdbc1f` in an isolated directory with the original config and output paths. Keep Qwen's active tree unchanged.

Why this distinction matters: reproducing analysis with the registered source is different from repeating sampled inference. A source digest alone does not capture all software/hardware state, and a once-written provenance file with null Git commit must not be replaced by an invented per-job history. The report's exploratory bootstrap and Holm adjustments remain separate additions, not automatically part of the original Step 13 specification.

### GPT-OSS results and artifacts

Job `373562` completed in 3:44 with exit `0:0` and an empty error log. It produced 2,781 token-diagnostic rows and analyzed 1,229 saved records. These totals include pilot, qualification, main, and mechanism records, including reused outcome copies. They are not 1,229 independent Sudoku puzzles or fresh calls. The server summary exactly matches the separately executed local frozen-source analysis. Artifacts are backed up under `evidence/snapshots/2026-09-30-gptoss-step13/`.

The frozen source passed 82 historical tests. The earlier evidence audit passed 95 current-tree tests; the expanded guide now passes 99 tests. Old and current statistical outputs on the same records are identical apart from the added qualification field `min_correct: 5`. None of these engineering checks adds new model accuracy observations.

### Qwen results and artifacts

Job `373551` was queued for CPU finalization after successful completion of all five follow-up jobs. No completed Qwen Step 13 artifact is used here. Do not substitute the already completed offline main comparison for evidence that every Qwen mechanism prerequisite has finished.

### Discussion and writing decision

Use **Lens 12** to distinguish preserved evidence, exact analysis reproduction, and repeat inference. Report the historical source resolution in a reproducibility appendix rather than allowing an execution detail to dominate the scientific findings. Completion markers establish artifact completeness, not answer correctness. Tests establish the checks they implement, not human-level reasoning or causal identification.

## J. Turning these blocks into manuscript sections

Keep the separate manuscript sections if required by the venue. In Methodology, use the experiment blocks to define each question, treatment, sample, baseline reuse, scoring rule, and limitation. In Results, follow the same experiment order and give the GPT-OSS and Qwen findings together wherever both have verified evidence. In Discussion, revisit each question with its relevant existing lenses and alternatives. This aligns the reader's route without removing section boundaries.

Alternatively, if the venue permits experiment-centered subsections, give each a Methods, Results, and Discussion sequence, then retain a common dataset/scoring section and a cross-experiment limitations section. In the manuscript, state shared settings once and describe only actual deviations. This writing guide deliberately repeats settings inside each block so it can be used independently.

The main comparison is the anchor. Cross controls test basic handling alternatives; token length examines segmentation-related hypotheses; binding changes assignments; ablations examine interfaces and prompt variability; revision evaluates correction routes and added compute. This logical chain is stronger than presenting unrelated mini-studies. Every explanatory claim must remain bounded by the controls actually performed. Keep the existing twelve lenses as a cross-experiment synthesis, not a list of causal conclusions.
