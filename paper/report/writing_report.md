---
title: "Symbolic Representation and LLM Sudoku Performance"
subtitle: "Evidence dossier and section-by-section research-paper writing guide"
author: "Prepared for Arnav Bharti"
date: "3 October 2026"
---

# Purpose, scope, and how to use this report

This is a writing dossier, not a replacement manuscript. You will write the paper yourself. It supplies the facts, definitions, experimental steps, source literature, numerical tables, interpretation boundaries, and verification procedures needed to do that. The attached *Research @ BITS Pilani* guidance determines the writing structure. Recorded requests and results determine the scientific content. Where an older draft, README, handoff, or model-selection note conflicts with the saved evidence, use the evidence.

Read this narrative together with `generated/results_tables.md`. The latter contains every selected-model condition, its difficulty breakdown, error categories, latency, and completion checks. `generated/audit.json` is the machine-readable audit. `generated/observations.csv` contains one row per saved result and can be opened in a spreadsheet. Historical diagnostics are included separately. Do not combine them into one model accuracy figure.

The complete raw backup is under `evidence/snapshots/2026-10-03-complete/`. Its 599 files occupy 69,814,796 stored bytes, excluding the manifest. JSONL results and job logs are losslessly gzip-compressed. The manifest records stored-file and raw-content SHA-256 checksums. The transfer includes outcomes, frozen protocols, sample plans, provenance, generated Slurm scripts, logs, both final analyses and token registries, and a fresh exact-ID scheduler capture. It excludes weights, environments, and credentials. The uncompressed working copy is under ignored `tmp/research-report/2026-10-03-capture/`. Both September snapshots remain unchanged.

## Evidence status and the central writing decision

Both selected models have complete qualification, pilot, main, Steps 8--12, and final-analysis evidence. Each main contains 540/540 saved records with matching frozen request digests and valid markers. Qwen follow-ups contain 135, 45, 165, 171, and 108 records, all complete with matching digests. Jobs 373543--373547 and CPU analysis 373551 completed with exit `0:0`; final analysis ended at 13:04:25 IST on 3 October. The fresh read-only capture followed that evening. The local audit covers 2,650 outcome records across selected and historical runs with no content-hash, shard, re-scoring, independent-grid, or dataset-identity disagreement. Historical partial diagnostics remain partial.

Both models now have completed corresponding follow-up evidence, but their patterns are not identical. Both pass 75/75 simple controls and have singular token-length regressions. Permuted number words score lower in both, while permuted digits decrease GPT-OSS's score and increase Qwen's. Two revisions improve GPT-OSS's score but produce no net Qwen gain, with two Qwen regressions. Describe this as a completed two-model comparison, not universal replication of every effect. Step 13 analyzes 1,229 outcome rows and writes 2,781 token-diagnostic rows per model; neither count represents fresh independent solves.

This dossier does not label completed manuscript results as “preliminary.” It distinguishes completed evidence, incomplete evidence, and untested explanations for your use as the author. Only completed, verified evidence belongs in final-paper results prose.

## The most important corrections to carry into the paper

1. The main experiment uses an explicit Sudoku prompt and a strict scorer. It does **not** use a regex-constrained decoder. Regex decoding appeared in earlier Nemotron and Mistral diagnostics.
2. The main prompt does **not** contain the earlier four-step “Before answering” verification paragraph. The saved main messages show `verify_before_answer=False`. Some timing diagnostics do contain that paragraph.
3. Reasoning is excluded from scoring, not from generation accounting. Hidden reasoning consumes generated tokens and context. A short final grid can still be preceded by enough reasoning to exhaust the available context.
4. Local vLLM requests are not interrupted by a demonstrated 600-second per-puzzle timer. The retry configuration's HTTP timeout is not an enforced local `LLM.generate` deadline. The verified bounds are context/output ceilings and the Slurm job wall-time.
5. Effective sampling is temperature 1 and top-p 1 for both selected-model main protocols. GPT-OSS's root inference JSON also contains 0.6 and 0.95, but model-specific sampling overrides replace them. Cite effective settings, not just the root fields.
6. GPT-OSS's frozen main profile and verified main job 359393 request 192 GB host RAM. Its later mechanism jobs request 96 GB in their saved Slurm scripts. Qwen requests 96 GB. GPU memory is a separate resource, one H100 80 GB per job. An earlier handoff claiming all GPT-OSS allocations were 96 GB is incorrect.
7. The pilot contains 15 underlying puzzles, not 60 different puzzles. Four representations of each puzzle produce 60 requests. The main experiment contains 60 underlying puzzles and 540 requests per model.
8. Technique-defined difficulty is not a human difficulty rating. “Hard” means the registered technique solver stalled and the reference procedure used search. It does not prove that every possible human technique must backtrack.
9. The old GLM, Kimi, and early unquantized Qwen calibration files actually contain five easy and ten hard requests, not five at each tier. Read their recorded metadata. Do not retroactively impose the current selection rule.
10. A valid-format answer, an answer preserving clues, a valid completed Sudoku, and the correct solution are different observations. Report their denominators separately.
11. Mechanism baselines are sometimes reused from the main experiment. These are not fresh independent trials. Revision branches share exactly the same initial answer.
12. The study has one sampled answer per main puzzle/representation/model cell. It measures realized performance under the frozen configuration, not an exact per-cell success probability.

# Applying the BITS Pilani writing guidance

The guidance requires you to manually verify every sentence, numerical claim, reference, table, and figure before submission. This dossier reduces that work but does not replace it. You should compare every selected manuscript number against the generated tables and its raw request IDs.

Use complete academic sentences in manuscript prose. Prefer active voice, simple words, and short sentences. Define technical terms when first used. Avoid em dashes, en dashes, and semicolons as prose connectors. This report uses lists as an author checklist, not as a recommendation to write the entire paper in fragments. Avoid unsupported promotional language such as “groundbreaking,” “state of the art,” or “proved genuine reasoning.”

The abstract and introduction should be accessible to a reader with beginner-level knowledge of machine learning. Explain the task as solving the same Sudoku with different visible labels. Introduce specialized quantities, such as conditional retention, later. Organize related work into two or three coherent themes. Each theme needs a survey paragraph and a short differentiation paragraph. A list of paper summaries is not enough.

Organize results by research questions. For each figure or table, identify one main takeaway and one or two secondary observations. The paper usually needs no more than two explanatory paragraphs per visual. The dossier is intentionally much longer than the manuscript should be. Put detailed historical screenings, exact prompts, complete condition tables, and audit commands in appendices or supplementary material.

Use the authentic template for your chosen venue. The supplied guidance mentions venue-specific procedures, but it does not establish that this thesis is being submitted to any particular conference. Check that venue's current instructions independently. Do not infer a page limit, anonymity requirement, deadline, or mandatory declaration from a different venue's example.

# Abstract: all points to cover

## The six required moves

**Background, one sentence.** State that mathematical constraint-solving should depend on the puzzle's relations, not the particular symbols used to write it. Sudoku is useful because relabeling preserves the problem while correctness is exactly checkable.

**Gap, one sentence.** State that high accuracy on a familiar representation does not establish unchanged performance on equivalent representations. Existing work studies Sudoku variants, arithmetic remapping, prompt sensitivity, or specialized symmetry-aware networks. Your experiment focuses on paired text-only label changes in off-the-shelf open-weight reasoning models.

**Contribution, one or two sentences.** Say you evaluate a controlled symbolic-representation benchmark with unique-solution Sudoku puzzles and deterministic answer checks. Identify the study as evaluation and diagnosis, not a new training algorithm, tokenizer, neural architecture, or Sudoku solver.

**Method, one or two sentences.** Mention three technique-defined difficulty tiers, nine alphabets, the same 60 main puzzles across representations, and final-grid-only scoring. Name GPT-OSS-120B and Qwen3.8-27B-FP8. Distinguish the paired main benchmark from the smaller completed diagnostics for both models.

**Results, one or two sentences.** Select the strongest complete findings. GPT-OSS solved 372/540 requests, or 68.9%, and Qwen solved 472/540, or 87.4%. The paired difference is 18.5 percentage points, with an exploratory stratified puzzle-bootstrap 95% interval of 13.7 to 23.5 points. Both models decline with difficulty. Alphabet accuracies range from 61.7% to 75.0% for GPT-OSS and 80.0% to 93.3% for Qwen, but neither model's eight Arabic-baseline comparisons survives Holm adjustment at 0.05. Do not pack all of these numbers into the abstract. A compact option is the two overall accuracies, a qualitative difficulty trend, and a bounded statement that numerical representation variation was not statistically resolved by these baseline comparisons.

**Implication, one sentence.** State that equivalent symbolic formulations can yield different realized outcomes and that evaluation should distinguish invalid grids, output errors, and resource truncation. Do not claim a proven tokenizer mechanism or a universal inability to reason.

## Decisions to make before writing the abstract

- Decide whether the main message is representation sensitivity, the model comparison, or the separation of failure types. Give one of these priority.
- If the abstract mentions revision, state its small shared-initial subset and model-dependent result: two revisions help GPT-OSS but give no net Qwen improvement. Do not let a 27-cell arm dominate the main study.
- Use “percentage points” for accuracy differences. A change from 75.0% to 61.7% is 13.3 percentage points, not a 13.3% relative reduction.
- Do not call the main input set “540 puzzles.” State 60 puzzles represented nine ways.
- Avoid putting raw Slurm job IDs, framework versions, historical rejected models, or context-ceiling details in the abstract.
- Do not say “all representation differences were significant.” None of GPT-OSS's eight Arabic-baseline comparisons survives Holm adjustment at 0.05 in the all-tier analysis.
- Do not say the tokenizer experiment proved shorter labels are better. The descriptive pattern is non-monotonic and the registered multivariable fit is singular.
- Do not say hidden reasoning eliminates output truncation. The observed records contradict that claim.

## Abstract self-check

After drafting, underline each claimed finding and identify its exact evidence table. Check that the problem is understandable without equations. Check that every model named has the completed evidence the sentence implies. Remove causal explanations that are only hypotheses. Ensure the last sentence states a bounded implication rather than a slogan about intelligence.

# Introduction: paragraph-level content and reasoning

## Paragraph 1: broad motivation without an inflated opening

Start with the reliability of language models on structured tasks. A model can produce fluent text while failing a checkable constraint. You do not need a broad claim about transforming every industry. Introduce the importance of separating success on a familiar notation from success on the same logical task written differently.

Define symbolic representation in plain language. Here it means the visible tokens used to denote Sudoku values. Digits, letters, geometric symbols, and color emoji can all name the same nine abstract values. They are not new Sudoku rules.

## Paragraph 2: why Sudoku and why paired relabeling

Explain that standard 9-by-9 Sudoku requires each of nine labels once in each row, column, and 3-by-3 box, while preserving clues. Arithmetic is not required. A consistent bijection on labels leaves solution structure unchanged. The same underlying puzzle can therefore be presented in several forms without changing its abstract constraints or solution uniqueness.

This controls an important source of confounding. Comparing unrelated digit and Greek puzzles would mix representation with puzzle difficulty. Your design presents the same puzzle under all nine alphabets. Difficulty tiers add another axis, but the pairing within a puzzle remains the core control.

## Paragraph 3: closest prior work and the precise gap

Mention Sudoku-Bench as an evaluation of Sudoku variants. Mention symbolic remapping work in arithmetic. Acknowledge the 2026 symbol-equivariant recurrent reasoning work explicitly. That work already studies Sudoku symbol symmetry, so the thesis cannot claim to introduce the concept or to be the first symmetry test in Sudoku.

Position this study as an empirical comparison of off-the-shelf reasoning language models, using a matched text-only final-grid protocol and a decomposed failure taxonomy. It also provides targeted behavioral diagnostics without analyzing visible reasoning traces. The distinction is from variant-rule puzzles, arithmetic tasks, task-trained architectures, and internal activation interventions, not from all prior reasoning evaluation.

## Paragraph 4: the study design at a high level

Describe the pipeline in three short stages. First, generate and certify unique-solution puzzles with fixed difficulty procedures. Second, substitute labels while keeping cell positions and clues fixed. Third, collect the final answer and validate format, clue preservation, Sudoku units, and equality to the reference solution.

State that the study uses pinned model revisions and frozen sample plans. Do not imply that reproducibility means stochastic results must be bitwise identical across GPU software versions. The saved records and request manifests enable exact re-analysis even when a fresh inference run differs.

## Paragraph 5: experimental setup in one paragraph

The dataset has 300 puzzles, 100 per tier. The frozen main sample has 20 per tier. Each model receives 540 main requests. The pilot uses different underlying puzzles. Both models' mechanisms use the same nested 15-puzzle and nine-puzzle subsets. Hidden reasoning is permitted, but only the extracted final answer is scored.

Name the two selected checkpoints and state that the experiments run locally on Sharanga H100 compute nodes. “Local” means locally hosted open-weight inference on the university cluster, not inference on your laptop. Do not introduce Nemotron and Mistral as main-study models.

## Paragraph 6: major findings with at most two or three numbers

Choose a small number of complete findings. The two-model version can state 68.9% versus 87.4% overall main accuracy, the 18.5-point paired difference and its exploratory uncertainty, and the descriptive decline with difficulty. If representation ranges are central, state them alongside the absence of Holm-significant Arabic-baseline contrasts, not as established causal penalties.

You may state that correct formatting did not guarantee correctness in historical constrained-decoding diagnostics, but keep the detailed failed-model chronology in an appendix. Do not use these different configurations as a controlled leaderboard against the selected models.

## Paragraph 7: three or four contributions

Candidate contributions, stated in full sentences, are as follows.

1. A reproducible paired evaluation of the same unique-solution Sudoku puzzles under nine symbolic alphabets and three solver-defined difficulty tiers.
2. A final-answer evaluation procedure that separates logical errors, clue changes, output-format failures, and truncation from operational failures.
3. A comparison of the selected open-weight reasoning models under matched puzzle sets, sampling settings, and context ceilings, with model-specific reasoning interfaces disclosed.
4. Corresponding experiments for both models testing input/output remapping, model-specific token-length constructions, label assignments, prompt/output choices, and final-answer revision.

Do not describe the dataset as the largest Sudoku benchmark or the models as the strongest possible models. Do not present small mechanism differences as causal discoveries. The distinctive contribution is the controlled combination and auditability, not a claim that every component is new.

## Suggested research questions

RQ1 asks whether realized final-grid accuracy differs across equivalent symbolic alphabets on the same puzzles. RQ2 asks how that pattern changes with solver-defined difficulty and model. RQ3 asks how much failure is attributable to invalid grids versus output errors and truncation. RQ4 asks whether simple Greek-symbol handling or cross-mapping alone explains failures. RQ5 asks what the token-length, binding, and prompt experiments establish or fail to establish. RQ6 asks whether revising a shared initial answer improves correctness, and at what additional cost.

Keep the paper's RQs limited enough that each has a substantive answer. All six now have completed evidence for both models. Shared and differing patterns must both appear. The later discussion offers shorter-paper organizations.

# Background and related work

## Definitions to establish before the methodology

A constraint-satisfaction problem specifies variables, their possible values, and rules restricting combinations. Sudoku has 81 cell variables with nine values. Its 27 all-different units are nine rows, nine columns, and nine boxes. Given clues fix some variables. A solution is a complete assignment satisfying every rule and clue.

A bijection is a one-to-one mapping between two label sets. Applying it consistently to a puzzle and solution preserves equality and inequality relations. Sudoku's mathematical solution does not depend on whether a value is displayed as `1`, `A`, or another token. This does not mean a learned language model's probability distribution must be invariant to the spelling.

An equivariant solver would transform its output consistently when the input labels are permuted. An invariant accuracy score would not change under equivalent label transformations. These are different statements. Equal aggregate accuracy can conceal different individual successes. Your experiment therefore examines paired successes and failures, not just mean accuracy.

A tokenizer converts text into model input units. A visible label can occupy one or several tokens, bytes, or Unicode code points. These quantities are not interchangeable. The experiment's token-length construction controls isolated and leading-space token counts for its chosen labels, but does not independently randomize every correlated property.

Binding means consistently connecting a visible label to its role or abstract value across a problem. Here the term describes a behavioral challenge. The evaluator's `GLOBAL_BINDING_ERROR` is a specific pattern in the final grid. It is not proof about a model's internal representations or an identified neural circuit.

Hidden reasoning means internal generation separated from the scored final response by the model's output convention. It does not mean zero compute, zero tokens, or a symbolic solver. In this study it is not inspected to explain model cognition. The backend extracts the final answer and retains generation metadata for audit.

## Related-work structure: three coherent clusters

### Cluster 1: Sudoku reasoning, difficulty, and symbol symmetry

Survey work on certified Sudoku difficulty, evaluation with variant constraints, and task-trained neural solvers. Distinguish a fixed standard Sudoku problem from a novel-rule variant. Explain why solver-defined tiers are reproducible but not human difficulty ratings. Include symbol-equivariant architectures because they directly address the same mathematical symmetry.

Your differentiation paragraph should say that this thesis tests label changes in off-the-shelf text-generating reasoning models without training a Sudoku architecture. The underlying standard puzzle is held fixed across representations. It checks the final grid rather than analyzing model traces or learned activation circuits.

### Cluster 2: representation sensitivity, tokenization, and binding

Survey arithmetic remapping, semantics-preserving problem variants, arbitrary symbol mappings, prompt-format sensitivity, and tokenizer differences. These works motivate testing whether surface notation changes realized success. They do not by themselves identify why a particular Sudoku condition fails.

Your differentiation paragraph should emphasize matched puzzles, unchanged constraints, and multiple label families rather than translated natural-language prompts. The study also separates final-grid failures from formatting and resource truncation. Acknowledge that labels differ in familiarity, spelling, tokenization, and Unicode properties, so the main alphabet comparison is not a single-factor causal tokenizer experiment.

### Cluster 3: self-revision, external feedback, and constrained output

Survey work on self-feedback, intrinsic correction limits, locating errors, and grammar-constrained decoding. The literature does not support a blanket statement that self-revision always helps or never helps. External feedback supplies information that an unassisted second pass may lack.

Your differentiation paragraph should focus on four branches from the same initial grid, a deterministic Sudoku checker, recorded stage-level costs, and exact final-grid scoring. Explain that syntax constraints differ from semantic Sudoku constraints. The historical regex only constrains nine rows of valid digits. It does not ensure clues or all-different units.

## Annotated primary-source reading list

The entries below are deliberately concise paraphrases. Links lead to canonical proceedings, author pages, or the paper's primary preprint record. Read the full relevant papers before making stronger comparisons. Publication status is stated where verified. An accepted-paper claim on an author page is not a reason to invent proceedings volume or page numbers.

### Sudoku and symbol symmetry

**Radek Pelánek, 2014. *Difficulty Rating of Sudoku Puzzles: An Overview and Evaluation*.** This overview discusses difficulty measures in relation to human solving data. It supports considering the complexity of steps and their dependencies rather than relying only on clue count. It does not validate this thesis's labels as human difficulty ratings. The primary record is a preprint. [Paper record](https://arxiv.org/abs/1403.7373).

**Radek Pelánek, 2011. *Difficulty Rating of Sudoku Puzzles by a Computational Model*. FLAIRS.** This published related work is useful when explaining why procedural solving difficulty can be meaningful. It concerns a computational model evaluated against human performance. This thesis uses a different fixed technique procedure and has no corresponding human validation. Cite it separately rather than changing the title/year of the 2014 overview. [Publisher PDF](https://cdn.aaai.org/ocs/2517/2517-11201-1-PB.pdf).

**Jeffrey Seely, Yuki Imajuku, Tianyu Zhao, Edoardo Cetin, and Llion Jones, 2025. *Sudoku-Bench: Evaluating Creative Reasoning with Sudoku Variants*.** This benchmark focuses on unconventional Sudoku constraints and challenging multi-step solving. It supplies relevant task motivation. Its difficulty, representations, and puzzles differ from this study, so its reported accuracy is not a directly comparable baseline. No equivalent archival proceedings entry was established in this review. [Primary paper](https://arxiv.org/abs/2505.16135), [project](https://pub.sakana.ai/sudoku/).

**Kulin Shah, Nishanth Dikkala, Xin Wang, and Rina Panigrahy, 2024. *Causal Language Modeling Can Elicit Search and Reasoning Capabilities on Logic Puzzles*. NeurIPS 37.** The authors study transformers trained on logical solving sequences for Sudoku and Zebra puzzles. This is evidence about task-specific training, not about the zero-shot competence of the checkpoints used here. Do not import its headline accuracy into a cross-model ranking on this dataset. [Proceedings](https://proceedings.neurips.cc/paper_files/paper/2024/hash/67b31ca159553d5593e62d7b998d63ea-Abstract-Conference.html).

**Richard Freinschlag, Timo Bertram, Erich Kobler, Andreas Mayr, and Günter Klambauer, 2026. *Symbol-Equivariant Recurrent Reasoning Models*.** This close prior work enforces symbol permutation equivariance through architecture and evaluates structured reasoning tasks including Sudoku. Its networks are not the off-the-shelf language models studied here. It makes a “first study of Sudoku symbol symmetry” claim untenable. The verified institutional listing describes a preprint, not an established conference publication. [Primary paper](https://arxiv.org/abs/2603.02193), [institutional metadata](https://research.jku.at/en/publications/symbol-equivariant-recurrent-reasoning-models/).

**Pedro Orvalho, Guillem Alenyà, and Felip Manyà, 2026. *MaxSAT-Based Feedback for Guiding Vision-Language Models in Sudoku*.** The authors use a symbolic consistency component to generate feedback for vision-language Sudoku solving. This is a relevant comparison for checker-guided refinement, but it uses a different modality and feedback algorithm. The author page states acceptance at EPIA 2026. Confirm the final proceedings citation before submission. [Author publication page](https://pmorvalho.github.io/publications/epia2026-2/).

### Representation, tokenization, and binding

**Iman Mirzadeh, Keivan Alizadeh-Vahid, Hooman Shahrokhi, Oncel Tuzel, Samy Bengio, and Mehrdad Farajtabar, 2025. *GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in Large Language Models*. ICLR.** Template-generated mathematical variants test sensitivity beyond original benchmark instances. Use this as motivation for controlled perturbations, not as proof that any observed change reveals lack of reasoning. Match the author names to the proceedings, which differ from the shortened older bibliography. [Proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/ec2e7a896f8250986b3907f57621ce94-Abstract-Conference.html).

**Dominika Agnieszka Długosz, Arlindo Oliveira, and Natalia Díaz-Rodríguez, 2026. *The Importance of Being Statistically Earnest: A Critical Re-evaluation of GSM-Symbolic*.** The primary record reports acceptance at EMNLP 2026 and revisits statistical and distributional assumptions in perturbation comparisons. It is especially relevant to clustered puzzle observations and model-specific explanations. Use it to motivate careful inference, not to assert that your own effects have already been validated by their analysis. Verify the final proceedings entry when available. [Primary paper, version 3](https://arxiv.org/abs/2605.28700v3).

**Yang Yan, Yu Lu, Renjun Xu, and Zhenzhong Lan, 2025. *Do Large Language Models Truly Grasp Addition? A Rule-Focused Diagnostic Using Two-Integer Arithmetic*. EMNLP, pages 13467-13483.** The diagnostics include symbolic remapping and representation invariance. This is a close conceptual predecessor, but addition uses numeric operations that Sudoku does not require. Avoid borrowing its interpretation as a conclusion about your two models. [Proceedings](https://aclanthology.org/2025.emnlp-main.681/).

**Jerry Wei, Le Hou, Andrew Lampinen, Xiangning Chen, Da Huang, Yi Tay, Xinyun Chen, Yifeng Lu, Denny Zhou, Tengyu Ma, and Quoc Le, 2023. *Symbol Tuning Improves In-Context Learning in Language Models*. EMNLP, pages 968-979.** The work studies training with arbitrary symbol mappings for in-context learning. It helps distinguish learning to follow arbitrary mappings from relying on label semantics. Your study does not symbol-tune the models and cannot attribute checkpoint differences to that training approach. [Proceedings](https://aclanthology.org/2023.emnlp-main.61/).

**Jiahai Feng and Jacob Steinhardt, 2024. *How Do Language Models Bind Entities in Context?* ICLR.** This work uses causal interventions on internal activations to study entity-attribute binding. Your final-grid behavioral tests do not reproduce those interventions or identify the same mechanism. Cite it for the binding concept and clearly distinguish behavioral evidence from neural explanation. [Proceedings PDF](https://proceedings.iclr.cc/paper_files/paper/2024/file/9d1b7fc578c0d2d6431fc26d736ecaf3-Paper-Conference.pdf), [primary preprint](https://arxiv.org/abs/2310.17191).

**Kaj Bostrom and Greg Durrett, 2020. *Byte Pair Encoding Is Suboptimal for Language Model Pretraining*. Findings of EMNLP, pages 4617-4624.** The work establishes that tokenizer design can affect model performance under its studied settings. It does not establish a monotonic law between isolated label token count and Sudoku correctness. [Proceedings](https://aclanthology.org/2020.findings-emnlp.414/).

**Phillip Rust, Jonas Pfeiffer, Ivan Vulić, Sebastian Ruder, and Iryna Gurevych, 2021. *How Good Is Your Tokenizer? On the Monolingual Performance of Multilingual Language Models*. ACL-IJCNLP, pages 3118-3135.** This study connects tokenization and multilingual model performance. It motivates recording script-specific token properties. Your inputs change value labels, not the natural language of the instructions, so do not describe this thesis as a multilingual task-comprehension study. [Proceedings](https://aclanthology.org/2021.acl-long.243/).

**Qintong Li, Leyang Cui, Xueliang Zhao, Lingpeng Kong, and Wei Bi, 2024. *GSM-Plus: A Comprehensive Benchmark for Evaluating the Robustness of LLMs as Mathematical Problem Solvers*. ACL, pages 2961-2984.** This paper evaluates mathematical robustness under multiple perturbation types. It supports an evaluation perspective that separates original accuracy from altered-form performance. The task and perturbations differ from bijective Sudoku relabeling. [Proceedings](https://aclanthology.org/2024.acl-long.163/).

**Melanie Sclar, Yejin Choi, Yulia Tsvetkov, and Alane Suhr, 2024. *Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I Learned to Start Worrying About Prompt Formatting*. ICLR.** This work examines meaning-preserving formatting changes and the distribution of results over formats. It motivates prompt disclosure and caution about one chosen wording. Your identical-prompt repetitions additionally show sampling variation, which must not be confused with a causal prompt-format effect. The primary record confirms the camera-ready venue. [Primary camera-ready record](https://arxiv.org/abs/2310.11324).

### Revision and constrained output

**Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh, and Peter Clark, 2023. *Self-Refine: Iterative Refinement with Self-Feedback*. NeurIPS 36.** Self-feedback and iterative refinement motivate additional final-answer passes. Its tasks and feedback procedure are not identical to this study's short grid-revision prompts. [Proceedings](https://proceedings.neurips.cc/paper_files/paper/2023/hash/91edff07232fb1b55a505a9e9f6c0ff3-Abstract-Conference.html).

**Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, and Denny Zhou, 2024. *Large Language Models Cannot Self-Correct Reasoning Yet*. ICLR.** The paper distinguishes intrinsic revision from correction using external feedback. Its findings are bounded by the models and tasks it evaluates. Neither its title nor this thesis's positive subset result supports a universal claim about all future models. [Conference record](https://openreview.net/forum?id=IkmD3fKBPQ), [primary paper](https://arxiv.org/abs/2310.01798).

**Kaya Stechly, Matthew Marquez, and Subbarao Kambhampati, 2023. *GPT-4 Doesn't Know It's Wrong: An Analysis of Iterative Prompting for Reasoning Problems*.** This is useful historical evidence on iterative prompting and the role of external verification. The workshop record is FMDM at NeurIPS, not a NeurIPS main-track paper. Verify the workshop citation rather than silently upgrading its venue. [Primary paper](https://arxiv.org/abs/2310.12397), [workshop record](https://openreview.net/forum?id=PMtZjDYB68).

**Gladys Tyen, Hassan Mansoor, Victor Carbune, Peter Chen, and Tony Mak, 2024. *LLMs Cannot Find Reasoning Errors, but Can Correct Them Given the Error Location*. Findings of ACL, pages 13894-13908.** The distinction between detecting an error and correcting a located error helps motivate the checker arm. Your checker reports grid and clue violations rather than reasoning-trace locations, and your study does not score reasoning traces. [Proceedings](https://aclanthology.org/2024.findings-acl.826/).

**Saibo Geng, Martin Josifoski, Maxime Peyrard, and Robert West, 2023. *Grammar-Constrained Decoding for Structured NLP Tasks without Finetuning*. EMNLP, pages 10932-10952.** Grammar constraints can improve adherence to specified output structures. A syntax grammar is not a Sudoku correctness oracle. Use this distinction when discussing the Nemotron regex diagnostics. [Proceedings](https://aclanthology.org/2023.emnlp-main.674/).

### Model documentation

The official GPT-OSS card documents Harmony formatting and configurable reasoning effort. The official Qwen checkpoint card documents FP8 weights, thinking control, and a dense 27B language model with a vision encoder. This study supplies text only. GPT-OSS is a mixture-of-experts model, so total parameter labels do not express equal active compute. Pin the exact checkpoint revision in methodology and supplement. Do not use unrelated vendor leaderboard scores as Sudoku evidence. [GPT-OSS checkpoint card](https://huggingface.co/openai/gpt-oss-120b), [OpenAI model card](https://openai.com/index/gpt-oss-model-card/), [Qwen checkpoint card](https://huggingface.co/Qwen/Qwen3.8-27B-FP8).

## Citation hygiene and bibliography corrections

Keep the existing `paper/references.bib` as a starting point, not an authority. The report does not overwrite your manuscript bibliography. Download proceedings BibTeX when preparing the final manuscript. Confirm complete names, exact title, year, venue, DOI, and pages against the paper itself. Preserve accents and hyphenated surnames.

Correct the older GSM-Symbolic author entry using the ICLR proceedings names. Distinguish Pelánek's 2011 published paper from his 2014 overview. Distinguish the FMDM workshop record from a NeurIPS main-track publication. Cite the final proceedings version of an accepted 2026 paper when its authoritative entry exists. For SE-RRM, the verified status is a preprint. For model cards, use an institutional author and an access date or pinned artifact revision appropriate to the venue.

Some OpenReview pages returned a browser-verification screen during this review. Primary arXiv or official proceedings copies provide alternative reading access. Do not cite inaccessible review text as if it were a verified paper conclusion. Two search candidates with inaccessible full metadata were not added to the reading list. This list is targeted background research, not a claimed exhaustive systematic literature review.

# Methodology: exact pipeline, implementation, and rationale

## 1. Research unit and experimental estimand

The underlying unit is a unique-solution Sudoku puzzle. A main observation is one puzzle, one alphabet, and one model under the frozen sampling and inference configuration. The outcome is binary correctness of the extracted final grid. The realized mean measures success on this selected sample and configuration. It is not pass@k, best-of-n, majority voting, a human rating, or performance with a solver tool.

For each puzzle $p$, model $m$, and alphabet $a$, define $Y_{pma}=1$ if the final answer exactly satisfies the registered evaluation, otherwise 0. The main accuracy is the sum of these outcomes divided by the number of requested cells. Operational errors are reported separately. The selected-model main runs have zero recorded request-level operational errors, so operational exclusion does not alter their present denominators.

The paired design holds the underlying puzzle fixed when comparing alphabets or models. Nine responses from one puzzle are dependent observations. Do not treat 540 requests as 540 independent puzzles when estimating uncertainty or testing a global model difference.

## 2. Dataset generation and certification

The generator uses master seed `20260826`, schema version `1.0.0`, and generator version `1.0.0`. Easy candidates start at the master seed. Medium and hard candidates use offsets of one billion and two billion. Within each tier, seeds advance until 100 accepted puzzles are collected.

For a candidate seed, the generator derives separate seeds for constructing a complete grid and carving clues. The exact solver fills an empty grid with seeded randomized choices. It then shuffles cell-removal order and tries removing clues. A removal is accepted only when exact solution counting, stopped at two solutions, reports one solution. Carving stops at the target or when the removal pass ends.

Target clue ranges are 40-46 for easy, 24-27 for medium, and 22-26 for hard. Actual accepted ranges are 40-46, 24-28, and 23-27. The difference is not a reporting error. Uniqueness-preserving removal may fail to reach the target. Report actual accepted puzzle statistics, not only carving targets. Medians are 43, 26, and 25.

The generator runs the fixed difficulty analyzer on each candidate. Candidates whose measured tier differs from the requested tier are rejected. Puzzle hashes prevent exact duplicate grids. This is exact-grid deduplication, not deduplication over all Sudoku symmetries or proof that no puzzle is isomorphic to another. IDs are `E001` through `E100`, `M001` through `M100`, and `H001` through `H100`.

Each stored record includes the compact puzzle, exact solution, clue mask/count, seed, generator version, uniqueness certificate, difficulty certificate, and puzzle SHA-256. The dataset manifest hashes `puzzles.jsonl` and the generation report. The dataset SHA-256 is `43a1ef3a4dfe22fa6cd8939021a80ef3cc812c5916ab62ef6b11501b45b58cc2`.

The local audit revalidated all 300 records. It checked record structure, duplicates, clue consistency, exact uniqueness, agreement with a fresh exact solution, difficulty labels, certificates, and manifest hashes. This is an independent re-execution of the registered checks, not an independently developed SAT solver. That distinction matters when describing verification strength.

**Why this approach.** Unique solutions eliminate ambiguity in reference comparison. Procedural generation avoids selecting puzzles based on model success. Seeds and certificates make generation and tier assignment inspectable. The exact solver is a data-generation and scoring reference, not an inference aid supplied to the main models.

## 3. Difficulty procedure

The analyzer applies techniques in a fixed priority order with deterministic tie-breaking. Singles include naked and hidden singles. Intermediate techniques include naked pairs, hidden pairs, pointing pairs, and box-line reductions. It restarts from the highest-priority technique after each successful step.

Easy puzzles are completed without an intermediate technique. Medium puzzles are completed with at least one intermediate technique. Hard puzzles cause this technique procedure to stall, after which the reference search solves the remaining grid. The certificate records deduction steps, techniques used, search nodes, and maximum search depth.

Every accepted easy puzzle in this dataset was solved using naked singles. Medium certificates include naked and hidden singles in all 100 puzzles, naked pairs in 83, hidden pairs in 37, pointing pairs in 32, and box-line reductions in three. Technique occurrence counts overlap because a puzzle can use several techniques. They must not be summed as a partition of the dataset.

**Interpretation limit.** Clue count alone does not define the tiers. Search depth includes recursive filling depth and is implementation-specific. “Backtracking required” is relative to the registered technique set. Avoid “objectively hard for humans” and avoid conflating generated standard Sudoku with Sudoku-Bench's specialized variants.

## 4. Sample construction and leakage checks

Selection is deterministic and stratified. Each tier ranks puzzle IDs using SHA-256 over the master seed, a selection namespace, tier, and puzzle ID. The lowest ranks are selected. This gives reproducible selection without relying on the accidental order of a JSONL file.

The pilot selects five puzzles per tier, 15 total, with namespace `pilot`. Main selection excludes these pilot IDs and selects 20 per tier with namespace `confirmatory-main`. The 15-puzzle mechanism set selects five per tier from the main sample using `confirmatory-mechanism`. The nine-puzzle ablation set selects three per tier from the mechanism set using `confirmatory-ablation`.

Pilot and main underlying puzzles are disjoint. Mechanism and ablation sets are nested, not held-out test sets. The same 60 main IDs occur in the frozen GPT-OSS and Qwen plans. Verify this equality directly rather than assuming that matching counts imply matching puzzles.

The current qualification script selects five easy puzzles and assigns a different representation to each. It builds a stratified selection and takes its first five entries, which are easy because the selection order is easy, medium, hard. It does not test five puzzles in each representation. Its sample is not explicitly reserved away from the main/pilot plans by the qualification script. Report any overlap found by the generated sample audit rather than claiming all screening examples were held out.

Historical calibration used a separate selection procedure and changed across old versions. Some old files have five easy and ten hard records. Those historical observations are not part of the main sample and should remain a diagnostic appendix.

**Why this approach.** A pilot estimates feasibility and latency without selecting the final main sample by outcome. Nested mechanism sets allow controlled paired follow-ups and reuse of exactly matching baselines. Nesting also limits generalization and creates dependencies that must be disclosed.

## 5. Symbolic transformations

The canonical puzzle uses values 1 through 9 and `.` for an empty cell. Each alphabet is an ordered tuple of nine distinct, nonempty, whitespace-free symbols. Position $v-1$ gives the visible symbol for abstract value $v$. Input and reference solution use the same mapping unless the input/output-cross condition explicitly specifies otherwise.

| Alphabet | Ordered labels for abstract values 1 through 9 |
| --- | --- |
| Arabic digits | `1 2 3 4 5 6 7 8 9` |
| Devanagari numerals | `१ २ ३ ४ ५ ६ ७ ८ ९` |
| Bengali numerals | `১ ২ ৩ ৪ ৫ ৬ ৭ ৮ ৯` |
| Uppercase Latin | `A B C D E F G H I` |
| Lowercase Latin | `a b c d e f g h i` |
| Greek letters | `α β γ δ ε ζ η θ ι` |
| Abstract symbols | `△ □ ○ ☆ × † ‡ § ¶` |
| Color emoji | `🔴 🟠 🟡 🟢 🔵 🟣 🟤 ⚫ ⚪` |
| Nonce labels | `KAV MIP ZOT RUL BEK DAX PEV NUG WIF` |

The main transformations preserve every cell position, empty position, clue relation, and solution value. Symbols are stored in Unicode NFC form. Encoding and decoding use exact single-space-separated rows. Round-trip checks ensure that transformed puzzle and solution decode back to the originals.

The name “Arabic digits” denotes the ASCII characters 1-9 in this repository. It does not mean Arabic-script text. The instructions remain English in all nine conditions. Nonce labels are arbitrary letter strings, not verified to have no meaning in every language or tokenizer vocabulary. Abstract symbols differ in visual shape, and emoji have color associations. Do not claim that any alphabet is semantically or perceptually neutral in all respects.

**Why this approach.** The bijective mapping changes notation without changing the abstract task. Differences still conflate several surface properties. The main study measures the combined effect of representation choice, not an independently isolated tokenization or cultural-familiarity effect.

## 6. Exact main prompt

The following is the saved Arabic prompt for main puzzle E003. Other main alphabets replace the listed labels and the puzzle values. The prompt contains no examples and no solver-generated hints.

```text
Solve the following 9x9 Sudoku.

Valid input symbols:
1 2 3 4 5 6 7 8 9

Rules:
- Every row must contain each valid value exactly once.
- Every column must contain each valid value exactly once.
- Every 3x3 box must contain each valid value exactly once.
- Do not change the given cells.
- The visible symbols are labels; apply the same symbol-value mapping everywhere.

Puzzle:
2 4 . . . 5 1 . 9
7 . . . . 6 . . 5
. 8 . 2 . . . . 7
3 5 2 4 . 7 . . 8
. . 1 . . 3 7 . 2
. 7 4 8 2 1 5 6 .
4 9 3 5 1 2 8 . .
5 . . 6 . . . 9 4
. 2 8 . 4 . . . .

Return only 9 lines of 9 space-separated output symbols.
```

The selected-model main prompt is a user message with the checkpoint's own chat template. There is no `/no_think` system message. That message belongs to historical Nemotron controls. There is no externally imposed regex or Sudoku-validity decoding constraint in the selected-model main study.

The strict answer contract is enforced by evaluation. The model is instructed to return only the final grid, and hidden reasoning is extracted away before scoring. A request is still incorrect if the extracted final answer contains prose or violates the exact row/symbol contract.

## 7. Selected models and effective inference settings

| Property | GPT-OSS | Qwen |
| --- | --- | --- |
| Profile | `gpt-oss-120b-local` | `qwen-3.8-27b-local` |
| Checkpoint | `openai/gpt-oss-120b` | `Qwen/Qwen3.8-27B-FP8` |
| Run ID | `local-models-v1` | `qwen-3.8-27b-v2` |
| Revision | `b5c939de8f754692c1647ca79fbf85e8c1e70f8a` | `017b9c7af6b5689d5dd426a76e0bc077eb5ca20a` |
| Backend | vLLM | vLLM |
| Chat reasoning setting | `reasoning_effort=high` | `enable_thinking=True`, `reasoning_effort=xhigh` |
| Prior reasoning retention | Final channel extracted | `preserve_thinking=False`, thinking tags extracted |
| Effective temperature / top-p | 1 / 1 | 1 / 1 |
| Configured output ceiling | 131,072 tokens | 131,072 tokens |
| Configured total context ceiling | 131,072 tokens | 131,072 tokens |
| Seed | 20260826 | 20260826 |
| Tensor parallelism | 1 | 1 |
| Maximum concurrent sequences per backend | 1 | 1 |
| GPU-memory utilization setting | 0.9 | 0.9 |
| Main compute | One H100, 12 CPUs | One H100, 12 CPUs |
| Main host RAM | 192 GB in frozen profile and verified main job | 96 GB |
| Main hash shards | 6 | 12 |

`high` and `xhigh` are provider-specific settings. They do not establish an equal number of reasoning steps or equal compute. The two models have different tokenizers, architectures, quantization formats, and throughput. Matched numeric sampling and context ceilings improve comparability but do not eliminate every difference.

For both models, vLLM's allowed generation is reduced to fit the prompt plus generated tokens within the context. Therefore the nominal 131,072 output ceiling cannot be fully used after a nonempty prompt. The final grid and hidden reasoning share that allowance. The main runs do not reserve a guaranteed 1,024-token final phase.

The first recorded provenance for both model runs reports Python 3.11.5, vLLM 0.28.0, Transformers 5.16.1, PyTorch 2.13.0, Accelerate 1.14.0, H100 80 GB HBM3, and driver 580.126.20. These files are written once at the model-run level. They do not establish a separately captured environment for every later shard. Their `git_commit` field is null. Do not invent a per-job commit hash. The frozen protocol records a source digest, and generated job artifacts provide additional execution evidence.

The official Qwen card recommends a top-p value different from the matched study setting. The study is not a claim that every checkpoint ran with its vendor-optimal defaults. Describe the matched effective settings and disclose checkpoint-specific reasoning controls. Model-card performance statements are not measurements made in this thesis.

**Why these models.** The selected checkpoints are locally deployable on Sharanga, expose separable reasoning/final-answer conventions, and passed the observed readiness/pilot workflow. This is a practical selection rationale, not proof that they are the two strongest open models for Sudoku. Screening creates selection bias toward feasible successful configurations, which belongs in limitations.

## 8. Runtime, Slurm, and checkpointing

Inference runs on GPU compute nodes through the numbered scripts, not on the login node. The login node is used for lightweight submission and read-only inspection. Model downloads and package preparation are separate setup activities on authorized compute allocations. No model was loaded or downloaded while producing this report.

Each request has a canonical hash-derived ID incorporating the exact request content and metadata. Main parts use a hash of this request ID modulo the shard count. These are scheduler partitions of the same 540-request experiment, not different scientific conditions. Parts have unequal counts. GPT-OSS sizes are 101, 89, 77, 108, 86, and 79. Qwen sizes are 41, 47, 40, 44, 51, 56, 50, 41, 36, 38, 44, and 52.

Results are append-only. Each completed record is flushed and fsynced. Existing request IDs are skipped on a rerun. Frozen manifests reject changed settings. Resuming a timed-out shard therefore reuses saved requests rather than making all calls again. Do not count the resumed job as a separate replicate.

The normal later GPT-OSS main submissions used eight-hour requests, with overrides visible in generated scripts. The original part 1 attempt requested six hours and timed out; part 6 requested ten hours. Part 5 needed two interrupted attempts, eight hours and one hour, followed by a successful three-hour-request resume. Qwen main parts request 12 hours. Job wall-time covers model initialization, request execution, and shutdown. Saved `latency_seconds` measures an individual generation call and excludes initial checkpoint loading. Scheduler waiting time is not inference latency.

Record-level operational failure is `API_ERROR` or `TIMEOUT` after retries. A Slurm job timeout is a different event. A job may time out with a partial shard that later resumes, or after all outcome records and a marker have been written. Conversely a clean Slurm exit alone is not proof of correct Sudoku answers.

The executor retries backend exceptions up to five times, with exponential delay capped at the configured maximum. It does not retry an incorrect Sudoku answer to improve accuracy. It stores the resulting final-answer evaluation. A process killed during an unsaved request leaves no result for that request, which must not be misclassified as a completed wrong answer.

## 9. Final-answer extraction and scoring

GPT-OSS uses Harmony channel markers. The backend extracts the final channel. Qwen uses thinking tags and the backend extracts the final-answer portion. The exact extraction implementation is in `src/lib/models.py`. Preserve both extracted text and raw generation for audit, but analyze only extracted text for Sudoku outcomes. Do not turn raw reasoning content into a result claim.

The scorer first distinguishes operational errors, missing generation, and exact-text controls. For Sudoku it detects registered refusal phrases, normalizes the requested output format, and performs strict parsing. The default format requires nine lines with nine valid symbols separated by one literal space. It does not accept arbitrary whitespace, headings, a code fence, or a tenth explanatory line. Alternate-format ablations are scored after their registered normalization, not against the default presentation contract.

Once parsed, each symbol is decoded to its abstract value. The checker tests all original clues. It then checks all nine rows, nine columns, and nine boxes. Finally it compares the candidate against the certified unique solution. Correctness requires no failed check. An apparently valid complete Sudoku that changes original clues is incorrect.

Final-grid failure labels include changed givens, row/column/box errors, and mapping mismatch. `GLOBAL_BINDING_ERROR` means the candidate differs by a consistent bijection of reference values. `LOCAL_MAPPING_ERROR` means the mismatch cannot be expressed by that consistent global substitution. These labels describe final outputs. They are not causal diagnoses.

One request can have many failure labels. For example it can change five clues and violate four columns. Report request incidence of each label or explicitly state that you are counting error instances. Never sum overlapping labels and call the total the number of failed requests.

The report's exclusive outcome categories use this order. Operational errors come first. Correct answers come next. Incorrect generations stopped by a length limit are truncations. Remaining failures with format, invalid-symbol, Unicode, missing-final-answer, or refusal labels are other output errors. The remaining failures are incorrect parseable grids. “Invalid grid” in the companion tables includes a valid Sudoku that fails the puzzle clues.

The independent local grid audit separately checks parseability, clues, rows, columns, boxes, and reference equality. It does not infer clue preservation when parsing fails. The denominator for clue preservation is parseable grids. This avoids the misleading shortcut of treating absence of `GIVEN_MODIFIED` as preserved clues when no grid was parsed.

## 10. Pilot and main experiment

Qualification is an operational/readiness screen, not the main evaluation. GPT-OSS's registered threshold was five correct out of five with zero operational failures. Qwen's approved threshold was at least three of five easy requests with zero operational failures. Both actually solved all five. Each observed qualification set consists of five easy puzzles in five representations. The saved qualification IDs are disjoint from that model's pilot and main IDs. This is a verified property of these captures, not a guarantee about every historical calibration selection procedure.

The pilot uses 15 puzzles, four representations, and 60 requests per model. It checks feasibility and estimates latency. It does not require perfect easy accuracy for inclusion. It is not interchangeable with the main experiment and should not be pooled into its accuracy.

After pilot review, each selected model's sample plan and protocol were frozen. The main experiment presents the same 60 main puzzles using nine alphabets. It contains 180 requests per difficulty, 60 per alphabet, and 20 in each alphabet-by-difficulty cell. There is one generation per cell, with no correctness-based resampling.

Step 5A's conditional retention analysis is an analysis of these main results, not another inference stage. For each non-Arabic alphabet, it asks what fraction of Arabic-correct puzzles remain correct under that alphabet. Report its conditional denominator. Also report successes unique to the transformed alphabet, because retention alone ignores those gains.

## 11. Step 8: input/output cross and controls

The 15 mechanism puzzles each have four Sudoku conditions. Arabic-to-Arabic and Greek-to-Greek reuse matching main outputs. Greek-to-Arabic and Arabic-to-Greek make new calls. Cross conditions explicitly include digit and input-to-output mappings, so they differ in instruction length and mapping burden as well as output alphabet. They are not a pure output-script intervention.

Each puzzle also has five controls. Copy a Greek row exactly. Translate the fixed sequence `ε γ η` to `5 3 7`. Retrieve the symbol at row 1, column 5 of a complete Greek grid. Count occurrences of one symbol in a complete grid. Convert a supplied complete Greek grid to Arabic digits. These tasks use a supplied completed solution and do not require solving Sudoku.

Total records are (15(4+5)=135) per model. Thirty Sudoku baselines are reused, 30 cross calls are new, and 75 controls are new. Both models pass all 75 controls. Some controls repeat a fixed answer such as `9` or `5 3 7`. These limited checks do not prove arbitrary Greek understanding or general grid manipulation.

**Purpose.** Separate simple symbol handling from integrated constraint solving and cross-representation output. A successful control excludes some narrow explanations under that prompt, but not every possible parsing, memory, reasoning, or binding problem in the full task.

## 12. Step 9: token-length experiment

Use the selected model's exact tokenizer to search deterministic candidate labels. Bin labels with one, two, or three tokens in isolation. Require the same token count after a leading space. Choose nine distinct labels per bin. Use each constructed alphabet on the same 15 mechanism puzzles, yielding 45 new requests.

Record nominal token length, mean clue tokens, mean symbol UTF-8 bytes, mean code-point count, and prompt tokens. Full-row and contextual tokenization can differ from isolation, so do not describe a label's isolated length as the whole prompt cost.

The registered logistic fit predicts correctness using prompt tokens, mean clue tokens, mean bytes, and mean code points. It returned a singular information matrix for both models. Predictors co-vary in each construction. No independent coefficient is identified. Do not omit these failures or present a clean token-length explanation.

**Purpose and limitation.** This is a diagnostic comparison of constructed label sets, not a randomized causal experiment isolating token count. Label identity also changes between bins. The non-monotonic descriptive results directly contradict a simple “fewer tokens always improves solving” summary on this sample.

## 13. Step 10: binding and label assignment

Each of 15 mechanism puzzles has 11 conditions. Six use the same uppercase token set with the standard assignment or five seeded permutations. Additional conditions use ordinary digits, permuted digits, ordinary English number words, permuted number words, and the neutral-nonce alphabet.

The default prompt lists the available symbols and instructs consistent use. It does not explicitly tell the model that `ONE` equals a conflicting digit. “Conflicting number words” means the experiment assigned word labels to abstract values in a seeded permutation when rendering the canonical puzzle. Since Sudoku depends on equality rather than numeric magnitude, describe this as a label-assignment perturbation. Do not present it as a direct proof that the model disobeyed an explicit arithmetic definition.

The standard-uppercase, ordinary-digit, and nonce outcomes reuse main results. That is 45 reused records and 120 new calls, 165 records total. Five permutations are fixed across puzzles for their respective conditions. They are not a random sample of all possible permutations on every request.

**Purpose.** Test whether label identity and assignment affect realized outcomes while leaving abstract constraints unchanged. A semantic-interference explanation is plausible, but stochastic variation, token identity, and instruction ordering remain alternatives.

## 14. Step 11: prompt, mapping, format, empty markers, and case

The nine ablation puzzles have 19 conditions, 171 fresh records. Four vary rule style from minimal to fully explicit. Three vary mapping instructions, alphabet-only, to digits, or to abstract names `V1` through `V9`. Four request spaced rows, compact rows, an 81-symbol string, or JSON. Four use `.`, `0`, `_`, or `EMPTY` as the empty-cell marker. Four compare uppercase/lowercase Latin and uppercase/lowercase nonce labels.

Most conditions use Greek labels. The case conditions intentionally change the alphabet. Alternate output formats are normalized according to the registered format before Sudoku evaluation. Report their own format-compliance rate, not whether they satisfy the default nine-spaced-row presentation.

Four condition names produce exactly the same default prompt per puzzle. They are `rules_fully_explicit`, `mapping_alphabet_only`, `output_spaced`, and `empty_dot`. Their independently generated results differ. This is direct evidence of generation variability on this nine-puzzle subset. The backend passes the recorded seed to vLLM's sampling parameters, so these are not documented independent-seed replicates. The records do not isolate random sampling from numerical or runtime nondeterminism. They are not four estimates of distinct prompt effects.

**Purpose.** Explore practical prompt/output choices and possible representation interactions. The experiment was marked exploratory. It has three puzzles per tier and no factorial combination of all variations. The highest-scoring condition is not automatically an optimized or validated replacement for the frozen prompt.

## 15. Step 12: shared-initial revision experiment

Use the nine ablation puzzles with Arabic digits, Greek letters, and emoji. This creates 27 puzzle/representation initial answers. All four branches start from the matching saved main answer. Branches are one pass, one self-revision, two self-revisions, and checker-guided revision. There are 108 outcome records, but not 108 independent initial solves.

One pass reuses the initial answer without a call. One self-revision always asks the model to check its answer and return a revised grid. Two self-revisions makes two such calls in sequence. Checker-guided revision makes one new call only if the initial answer is incorrect. It reports clue changes and row/column/box or format violations. It does not provide the complete reference solution or analyze the hidden reasoning.

Checker-guided revision's decision to revise uses deterministic correctness. It leaves correct initial answers untouched. Generic revision does not have that stopping rule. This gives the checker arm both information and a selection advantage. Do not attribute its entire gain solely to better feedback text.

Record each stage's generation, evaluation, and whether the model was called. Count wrong-to-right fixes and right-to-wrong regressions. Count new calls and all stage truncations. For cost, add the reused initial latency to all new-call latencies in each branch. The top-level latency is only the final stored generation's latency, so it is not a fair end-to-end revision cost.

**Purpose.** Compare practical routes to correcting a common initial answer. The experiment does not include equal-compute independent resampling, best-of-n, or a solver-assisted answer-generation baseline. A benefit may reflect extra compute, new sampling opportunities, explicit checking, or feedback information. The data alone do not separate these explanations.

## 16. Statistics and what each analysis can support

Report raw numerators and denominators alongside percentages. A 60-puzzle alphabet accuracy uses 60 observations, not 540. A difficulty-by-alphabet cell uses 20. An individual mechanism condition uses 15. An individual ablation condition uses nine. A revision arm has 27 cells clustered within nine puzzles.

For a specific Arabic-versus-alphabet comparison, construct paired binary outcomes on the same puzzles. Let $b$ count Arabic-only successes and $c$ count alphabet-only successes. The exact two-sided McNemar test uses the binomial distribution of the discordant pairs. The report supplies raw p-values and Holm-adjusted p-values over eight alphabet comparisons for each model. Holm adjustment was added during this report's analysis. Do not describe it as a preregistered rule unless an earlier frozen record establishes that.

Conditional retention equals the number correct in both conditions divided by the Arabic-correct count. It is a useful descriptive question, but it conditions on baseline success and omits transformed-only successes. An alphabet can have the same overall accuracy as Arabic and still lose and gain different individual puzzles.

For a global two-model main comparison, use the paired 60-puzzle matrix. The offline script computes a stratified puzzle-cluster bootstrap only when all 540 matched cells exist. It resamples 20 puzzle clusters within each difficulty tier, retains all nine representations in each cluster, uses seed `20260930`, and performs 10,000 replicates. It reports a percentile 95% interval for Qwen-minus-GPT-OSS accuracy in percentage points. This is a newly computed exploratory uncertainty summary, not a registered confirmation test or an estimate of within-prompt sampling variance.

Do not apply an unclustered significance test to all 540 request cells. Do not fit a saturated model with insufficient data and interpret unstable coefficients. A mixed-effects or cluster-robust analysis could be useful future statistical work, but no such completed fit is claimed here. The registered token-length fit's singularity must remain visible.

Within-tier representation effects and model interactions are worth inspecting descriptively. Testing every pair of alphabets, difficulty tier, model, and mechanism condition creates many comparisons. Distinguish prespecified questions from follow-up exploration and correct appropriately. Do not select only favorable p-values.

# Results: full evidence and how to write it

The companion tables appended to this report contain the full condition-level numerical results. This section gives the key claims, denominators, and writing choices. Verify every claim with those tables before transferring it into the manuscript.

## Readiness and pilot results

GPT-OSS's three timing diagnostics each solved one puzzle. Easy took 36.12 seconds and 7,247 generated tokens. Medium took 254.59 seconds and 49,220 tokens. Hard took 227.35 seconds and 44,435 tokens. These are individual examples, not mean tier latencies. The hard example finishing faster than the medium example does not imply hard puzzles are generally faster.

Both selected models solved all five qualification requests without operational failures. The qualification compares five easy puzzles in five representations, one each. It is a readiness check, not an accurate estimate of general success.

GPT-OSS's pilot solved 47/60 requests, or 78.3%. Easy, medium, and hard were 20/20, 13/20, and 14/20. Qwen solved 54/60, or 90.0%, with 20/20, 16/20, and 18/20. Each pilot had two truncations and zero operational failures. Mean call latency was 252.48 seconds for GPT-OSS and 452.30 for Qwen.

Pilot accuracy should not be pooled with main accuracy. Pilot and main use different underlying puzzles and different representation coverage. The pilot's tier order and alphabet rankings need not persist on the larger paired main sample. In particular, a 14/20 versus 13/20 difference does not establish hard puzzles are intrinsically easier than medium puzzles.

## GPT-OSS main accuracy and difficulty

The complete main result is 372/540, or 68.9%. Easy is 171/180, or 95.0%. Medium is 121/180, or 67.2%. Hard is 80/180, or 44.4%. Mean call latencies are 53.48, 372.49, and 446.45 seconds by tier. Overall mean latency is 290.81 seconds and median is 240.46 seconds.

The result supports a clear descriptive decline with the registered difficulty tiers under this configuration. It does not prove the models use the registered solver's techniques. The model never receives the technique certificate. Clue counts, puzzle structure, and the solver-defined tier are related, so attributing the trend to one of them alone is not justified.

Arabic digits and uppercase Latin each score 45/60. Lowercase Latin scores 44/60. Bengali numerals and nonce labels each score 43/60. Devanagari numerals score 39/60. Abstract symbols and emoji each score 38/60. Greek letters score 37/60. Thus the descriptive range is 61.7% to 75.0%, 13.3 percentage points.

Greek's lower aggregate performance is concentrated beyond easy. Arabic and Greek both solve 20/20 easy requests. Medium is 14/20 versus 11/20, and hard is 11/20 versus 6/20. Do not describe Greek symbols as unreadable. Simple Greek controls also all succeed.

The Arabic-versus-Greek paired comparison has nine Arabic-only successes and one Greek-only success. Its unadjusted exact p-value is 0.0215. Its Holm-adjusted value is 0.1719 across eight comparisons. Therefore the report does not claim a family-wise significant Greek penalty at 0.05. This does not prove no effect exists. It bounds what this sample and analysis establish.

Uppercase Latin and Arabic have identical aggregate accuracy, but nine Arabic-correct puzzles fail in uppercase and nine Arabic-failed puzzles succeed. Only 36 of 45 Arabic successes are retained. Equal averages do not imply identical puzzle-level behavior or empirical equivariance.

## GPT-OSS failure decomposition

Of 540 main records, 372 are correct, 96 are nontruncated incorrect grids, 24 are incorrect truncations, and 48 are other output errors. Zero are request-level operational failures. Thus 72 requests fail through truncation or other output errors, and 96 fail after producing a parseable nontruncated grid.

The independent checker parses 468/540 final answers, or 86.7%. Among these, 454/468 preserve all clues, or 97.0%. Fourteen parseable grids change at least one clue. All rows, columns, and boxes are valid together in 377/468 parsed grids. Only 372 parsed grids are the correct clue-preserving solution. The five additional valid Sudoku grids fail the original puzzle's clues.

Keep parseability distinct from nine-row shape alone. A nine-row answer containing an invalid output token can still fail parsing. Keep unit validity distinct from clue preservation. Do not infer either property for an unparseable output.

Twenty-four length-stopped outputs are only 4.4% of all requests, but 14.3% of the 168 incorrect requests. Even an unrealistically perfect repair of all 24 would raise observed accuracy only to 396/540, or 73.3%, not to 100%. This arithmetic bound is not a measured rerun result. It shows that truncation cannot explain all GPT-OSS main failures.

Among the 468 parseable outputs, correctness is 372/468, or 79.5%. You may show this conditional figure to diagnose format burden, but not replace the primary unconditional 68.9% accuracy. Conditioning on parseability selects easier or more successful outputs.

## Qwen main accuracy, errors, and paired model comparison

The complete Qwen result is 472/540, or 87.4%. Easy is 174/180 (96.7%), medium 160/180 (88.9%), and hard 138/180 (76.7%). Mean generation latencies are 110.10, 605.11, and 878.53 seconds by tier. Overall mean latency is 531.25 seconds and median latency is 422.78 seconds. The 68 failures consist of 33 nontruncated incorrect grids, 24 truncations, and 11 other output errors. There are zero recorded request-level operational failures.

Among 505 parseable grids, 488 preserve all clues and 487 satisfy all Sudoku units. The 17 clue-changing outputs modify 47 given cells. Fifteen outputs satisfy all units but fail original clues. Thus even this model's relatively frequent valid Sudoku outputs still require clue verification. Its parsing rate is 505/540 (93.5%), compared with GPT-OSS's 468/540 (86.7%). Clue preservation is 488/505 (96.6%) and 454/468 (97.0%) respectively among parseable outputs. Do not treat unparseable outputs as clue-preserving successes.

Devanagari is Qwen's highest observed alphabet at 56/60, followed by uppercase Latin 55/60 and emoji 54/60. Arabic digits and Bengali each score 53/60. Abstract symbols, Greek, and lowercase Latin each score 51/60. Nonce labels score 48/60. The descriptive range is 80.0% to 93.3%. All eight Holm-adjusted Arabic-baseline p-values equal 1.0. Therefore a claim that Devanagari reliably improves Qwen or nonce labels reliably harm it is not established by this sample. The alphabet ordering differs numerically from GPT-OSS's, but a statistically identified model-by-alphabet interaction was not fitted here.

Twenty-four truncations are 4.4% of all Qwen requests and 35.3% of its failures. An unrealistically perfect repair of all 24 would yield 496/540 (91.9%), not perfect accuracy. This is an arithmetic bound, not an observed higher-ceiling rerun. Both models have the same total number of truncations, but Qwen has fewer other failures, making truncation a larger share of its failure set.

On all 540 matched cells, 338 are correct for both, 34 only for GPT-OSS, 134 only for Qwen, and 34 for neither. The net difference of 100 correct answers is 18.52 percentage points. The stratified puzzle-cluster bootstrap gives a 95% percentile interval of 13.70 to 23.52 points, with seed `20260930` and 10,000 replicates. It retains all nine alphabets when resampling each puzzle and draws 20 puzzles within each tier. This post-capture exploratory interval reflects variation over these puzzle clusters, not independent sampling seeds or all possible model deployments.

The advantage is concentrated beyond easy. The net extra correct counts are three on easy, 39 on medium, and 58 on hard, corresponding to 1.67, 21.67, and 32.22 percentage points over 180 requests per tier. Both models are correct on 165 easy, 108 medium, and 65 hard cells. Both fail on zero easy, seven medium, and 27 hard cells. These tier comparisons are descriptive, not three independently confirmed inferential tests.

The 34 GPT-OSS-only successes show that the higher aggregate Qwen score does not imply individual-cell dominance. At least one model solves 506/540 cells (93.7%). That union quantifies complementarity of saved answers. It is not an evaluated two-model ensemble, an equal-cost baseline, or a claim that a deployment can choose a correct answer without a checking procedure.

Under the recorded deployed configurations, Qwen has higher realized accuracy and approximately 1.83 times the mean generation latency. Compare these configurations rather than inferring that parameter count alone explains the result. A dense 27B model and a 120B-labeled mixture-of-experts model do not have matching active compute.

## Step 8: input/output cross and controls

GPT-OSS saves all 135 records with a valid marker. Its four Sudoku conditions score 12/15, 12/15, 10/15, and 11/15 in Arabic-to-Arabic, Greek-to-Greek, Greek-to-Arabic, and Arabic-to-Greek order. Qwen scores 13/15, 11/15, 11/15, and 10/15. Each model solves 45/60 Sudoku outcomes and passes all 75 controls. Their equal mixed 120/135 totals conceal different condition outcomes and are not Sudoku-only accuracy.

Sudoku-only easy, medium, and hard correctness is 19/20, 18/20, and 8/20 for both models. GPT-OSS has two truncations, nine incorrect grids, and four other output errors. Qwen has six truncations and nine incorrect grids. Both have zero operational failures. Equal tier totals do not establish identical cells.

GPT-OSS's equal baselines do not support a universal Greek-output penalty. Qwen's Greek-to-Arabic score remains 11/15, equal to Greek-to-Greek, so Arabic output does not improve this aggregate. Cross prompts add instructions and mapping burden, confounding pure input/output attribution. Each condition has only 15 puzzles.

## Step 9: token-length construction

All 45 requests are complete. One-token labels solve 9/15, two-token labels 13/15, and three-token labels 10/15. Easy is 15/15, medium 13/15, and hard 4/15 across the three conditions. There are five truncations, four other output errors, four incorrect grids, and zero operational failures.

GPT-OSS's highest bin has two tokens, with hard counts 0/5, 3/5, and 1/5. Qwen solves 37/45: bins 12/15, 11/15, and 14/15; tiers 14/15 easy, 15/15 medium, and 8/15 hard. Its failures are three incorrect grids, two truncations, three other output errors, and zero operational failures. Both patterns are non-monotonic and both 45-observation fits are singular. Labels are model-specific. Report descriptive constructions, not an identified token-length effect.

## Step 10: binding conditions

All 165 records are complete. Overall correctness is 124/165. Easy, medium, and hard counts are 55/55, 50/55, and 19/55. Seven outputs truncate, two have other output errors, and 32 are nontruncated incorrect grids. There are no request-level operational failures.

Ordinary digits, ordinary number words, and nonce labels each solve 12/15. Permuted digits and permuted number words each solve 10/15. Six uppercase assignments range from 10/15 to 13/15. The complete condition table supplies exact results and latency.

Qwen solves 147/165: easy 50/55, medium 51/55, hard 46/55. Ordinary and permuted digits score 13/15 and 15/15; ordinary and permuted number words 12/15 and 9/15; nonce 14/15. Uppercase assignments span 12/15--15/15. Its failures are nine incorrect grids, eight truncations, one other output error, and zero operational failures.

Both models score lower on permuted words, but the digit direction differs. This rules out summarizing every permutation as harmful. Assignment sensitivity or familiar-label semantics are candidate explanations, not identified mechanisms. Fixed permutations and sampling remain alternatives. Do not state that semantic conflict causes a general percentage loss.

## Step 11: ablation outcomes and generation variability

All 171 outcome records and a valid completion marker exist. Slurm job 361282 timed out at 15 hours after the result artifact was complete. The saved request records contain no operational errors. Preserve this distinction in the execution appendix. Do not delete the complete data because the scheduler state says `TIMEOUT`.

The overall result is 103/171. Difficulty counts are 55/57 easy, 37/57 medium, and 11/57 hard. Twelve outputs truncate. Mapping to digits and uppercase nonce labels each score 8/9. Compact rows and an 81-symbol string each score 3/9. All 19 conditions and their tier results appear in the companion table.

The four identical-default-prompt conditions score 5/9, 6/9, 5/9, and 7/9. This demonstrates that a two-answer difference can arise without changing the prompt. Consequently an observed 8/9 condition is a candidate for further evaluation, not sufficient evidence to replace the frozen benchmark prompt.

Qwen completes all 171 records and marker, with job 373546 exiting `0:0` in 26:44:02. It solves 130/171: easy 51/57, medium 43/57, hard 36/57. Its failures are 25 incorrect grids, four truncations, and 12 other output errors, with zero operational failures. Digit mapping, uppercase nonce, and minimal rules score 9/9; compact rows 2/9 and string81 4/9. The four identical-default-prompt conditions have the same binary success set, 7/9. This verified agreement does not prove identical erroneous grids or deterministic future inference.

Alternate formats use their own parsing rules. A low score can include grid errors as well as formatting failures. Qwen has 18 clue-changing outputs among 155 parseable grids, despite 147 unit-valid grids. Do not claim every format difference is compliance alone or select the highest nine-puzzle score as a validated new protocol.

## Step 12: revision results and costs

All 108 records are complete. Aggregate final correctness by branch is 18/27 one pass, 19/27 one self-revision, 23/27 two self-revisions, and 22/27 checker-guided revision. The one-pass baseline is exactly shared, so these are paired branches, not four independent 27-request samples.

One self-revision fixes one wrong answer, two self-revisions fix five, and checker-guided revision fixes four. No initially correct answer regresses in these observed arms. Absence of a regression in 18 initially correct cells does not prove revision is safe on all problems. The checker arm cannot regress the initial successes because it does not revise them.

New-call counts are zero, 27, 54, and nine. Additional generation time totals are 0, 4,599.26, 8,057.65, and 4,439.46 seconds. Mean end-to-end generation time per branch cell, including the reused initial answer, is 312.25, 482.60, 610.69, and 476.68 seconds. These are observed generation-time estimates, not scheduler elapsed time or GPU energy.

The table's final-record truncation count is three across the four branches, while all-stage counts are larger because shared initial truncated answers appear in each arm and revisions can truncate. Do not sum shared initial stages and report them as independent truncation events. Use unique source request IDs or explicitly state branch-stage accounting.

Qwen's 108 records are complete. Its arms score 23/27, 26/27, 23/27, and 26/27 in one-pass, one-revision, two-revision, and checker order. One revision fixes three of four initial failures with no regression. Two revisions fix two initial failures and regress two initially correct answers. Checker feedback fixes three of four failures and makes four calls, not GPT-OSS's nine. Qwen's new-call counts are 0, 27, 54, and 4; added times 0, 4,440.47, 6,123.53, and 4,252.98 seconds; mean cumulative times 561.28, 725.74, 788.07, and 718.79 seconds. It has three final-row truncations and zero operational errors.

The bounded comparison is model-dependent. Two generic revisions help GPT-OSS but produce no net Qwen gain, including two regressions. Checker feedback improves both recorded subsets but uses selective intervention. Extra compute, selection, and feedback are not independently isolated. Do not generalize more revisions as consistently beneficial.

## Step 13: completed analysis and token registries

Both CPU analyses complete: GPT-OSS job 373562 in 3:44 and Qwen job 373551 in 7:40, exit `0:0`. Each analyzes 1,229 rows and produces 2,781 registry rows: 81 symbols and 2,700 user prompts across all 300 puzzles and nine alphabets. These are tokenizer measurements, not additional Sudoku solves. The experiment-centered block includes both full registry summaries and verification paths. The stored server retention, regression, and revision analyses must agree with their local registered re-analysis. Report-only Holm adjustment and the cluster bootstrap remain exploratory additions.

## Historical model-screening evidence

Include this material in an appendix if useful for explaining protocol development. Do not call it an equal-budget model comparison. These trials differ in reasoning controls, token/context limits, prompts, quantization, and samples.

Nemotron's bounded-reasoning trial saved ten of 15 requests, with 0/5 easy and 0/5 medium. Its greedy answer-only file saved 11/15, all incorrect and length-stopped. The initial handoff said cancellation occurred after easy became conclusive, but the saved file contains additional medium and hard records. Report the actual saved counts. The sampled answer-only trial completes 15/15 with zero correct. Constrained greedy completes 15/15 with zero correct and 15 parseable grids, none preserving all clues. Verified constrained also completes 15/15 with zero correct, 15 parseable grids, and only one preserving all clues.

Mistral's completed verified-constrained calibration is the v2 run. It solves 0/15 while all 15 outputs are parseable. Five preserve all clues, but no output is the correct solution. The v1 directory has no saved completed result shard in this snapshot. Its copied error log records a failed Ninja build and engine-core initialization failure, followed by a nonzero task exit. This is a backend startup failure, not 15 model-answer failures. Do not infer a specific underlying compiler or hardware cause from that message alone.

The separate nearly completed diagnostic puzzle is outside the main and pilot sets. One Nemotron and three Mistral diagnostic variants each produce one incorrect result. The first reasoning-off variants change clues. Later Mistral variants explicitly constrain the final answer to preserve clues and still fail Sudoku. Those later clue-preserving decoder conditions are materially different experiments, not repeated measurements of the same unconstrained setup.

Kimi-Linear-48B-A3B-Instruct and GLM-4.7-Flash each complete an old 15-request bounded-final calibration with zero correct. Kimi has 11 truncations, GLM 14. These files contain five easy and ten hard requests. They do not establish how the models would perform under the later natural-reasoning, larger-context protocol.

The old unquantized Qwen3.8-27B checkpoint has different revision `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0` from the selected FP8 checkpoint. Its bounded-final and official-thinking calibrations each solve four of 15 recorded requests, all four easy successes. Its early short-budget qualification variants produce 0/5, 1/5, 2/5, a partial 1/2, and later 4/5 under changing settings. Do not pool them or call them the current Qwen main model's results.

Qwen3.5-122B-A10B-FP8 has one complete easy diagnostic success in 194.07 seconds and one medium truncation in 1,392.24 seconds. The earlier failed/empty diagnostic directory is not a successful result. This small screen cannot establish a broad model ranking. Its settings also include different top-p, top-k, and presence penalty from the selected-model main protocol.

The selected FP8 Qwen's first 32,768-context screen solves easy in 80.48 seconds, then fills the available context on medium and hard. The generated lengths are 32,425 and 32,426 tokens. The 131,072-context medium rerun solves correctly in 387.20 seconds. This is evidence that the earlier screen was context-limited under its configuration. It is not a controlled one-factor rerun because the effective sampling configuration also changes in v2. It does not establish that increasing context will rescue every truncation.

The companion historical inventory lists all available runs and completion checks. The detailed appendix records model IDs, revisions, effective settings, and difficulty/error breakdowns. Models considered but never producing a saved inference result should be described as considered or setup-attempted, not evaluated.

# How to verify every result yourself

## Verification level 1: reproduce the report's local analysis

Run these commands on your machine. They do not use SSH, load a model, install packages, or submit jobs.

```bash
cd /Users/arnavbharti/Developer/arnavbharti/thesis
python3 paper/report/prepare_snapshot.py \
  tmp/research-report/snapshot \
  evidence/snapshots/2026-10-03-complete --verify
python3 paper/report/analyze_evidence.py \
  --snapshot evidence/snapshots/2026-10-03-complete \
  --output tmp/research-report/recheck
```

The checksum verifier must report all files verified. The analysis must report `dataset_valid: true` and an empty `audit_errors` list. It reads compressed shards directly. The original `source` argument is unused in checksum-verification mode, so loss of the ignored working directory does not prevent verification.

Compare `tmp/research-report/recheck/results_tables.md` with `paper/report/generated/results_tables.md`. Paths in the audit JSON differ according to where you read the snapshot, but results must agree. When comparing against a later refreshed snapshot, counts may legitimately increase. Never compare a newly refreshed incomplete set with an older complete-looking prose paragraph without checking capture status.

## Verification level 2: inspect one raw record without reading reasoning

This example prints only a request's final text and score, not its raw reasoning.

```bash
cd /Users/arnavbharti/Developer/arnavbharti/thesis
python3 - <<'PY'
import gzip
import json
from pathlib import Path
root = Path('evidence/snapshots/2026-10-03-complete/experiment_outputs')
directory = root / 'local-models-v1/gpt-oss-120b-local/exp4'
for path in sorted(directory.glob('shard-*.jsonl.gz')):
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        for line in stream:
            row = json.loads(line)
            request = row['request']
            if request['puzzle_id'] == 'E003' and request['condition'] == 'arabic_digits':
                print(request['request_id'])
                print(request['messages'][0]['content'])
                print((row.get('generation') or {}).get('text', 'NO GENERATION'))
                print(row['evaluation'])
PY
```

The correct E003 solution is shown in the representative-output appendix. Manually check the original clues and all 27 Sudoku units. For a non-Arabic record, use its recorded `output_symbols`, not a guessed Unicode order, to map back to digits.

## Verification level 3: count outcomes independently

```bash
cd /Users/arnavbharti/Developer/arnavbharti/thesis
python3 - <<'PY'
import gzip
import json
from collections import Counter
from pathlib import Path
root = Path('evidence/snapshots/2026-10-03-complete/experiment_outputs')
for relative in ('local-models-v1/gpt-oss-120b-local/exp4',
                 'qwen-3.8-27b-v2/qwen-3.8-27b-local/exp4'):
    rows = []
    for path in sorted((root / relative).glob('shard-*.jsonl.gz')):
        with gzip.open(path, 'rt', encoding='utf-8') as stream:
            rows.extend(json.loads(line) for line in stream if line.strip())
    print(relative, len(rows))
    print(Counter(row['evaluation']['outcome'] for row in rows))
    for tier in ('easy', 'medium', 'hard'):
        selected = [r for r in rows if r['request']['metadata']['difficulty'] == tier]
        correct = sum(r['evaluation']['outcome'] == 'CORRECT' for r in selected)
        print(tier, correct, len(selected))
PY
```

This confirms saved counts but not experiment completion. A final claim additionally needs the request-manifest digest, eligible counts, and completion markers. The audit script checks these. A line count without those checks is insufficient.

## Verification level 4: verify the frozen plans and prompts

Compare `sample-plan.json` in the GPT-OSS and Qwen run roots. Confirm identical main IDs and dataset hash. Confirm pilot/main disjointness and nested mechanism/ablation IDs. Read `protocol.json` and each step's `request-manifest.json`. Read model-specific sampling overrides. Check the exact prompt recorded in each result. Confirm no verification paragraph or structured regex is asserted for main inference unless the saved artifact actually contains it.

Request hashes use canonical JSON, sorted keys, and compact separators. The step manifest hashes newline-joined sorted request IDs. Hash-shard membership is deterministic. The offline audit checks shard assignment, duplicate IDs, marker counts, manifest digest, re-evaluation agreement, and independent grid correctness. It distinguishes a partial dataset from corrupt data.

## Verification level 5: scheduler and logs

The copied scheduler TSV and generated Slurm files establish exact names, requested resources, job states, and elapsed times for the recorded check. Scheduler status changes over time. A local TSV is historical evidence, not a live status query. For a live read-only check, use exact known thesis IDs only.

```bash
ssh thesis 'squeue --noheader -j 366222 -o "%i|%j|%T|%M|%l|%R"; sacct -j 366222 -X -n -P -o JobID,JobName%60,State,Elapsed,ExitCode'
```

If SSH stalls at authentication/banner, unlock it before trying again. Do not run model loading or the data audit on the login node. You can inspect the copied `.out.gz` and `.err.gz` files locally with `gzip -cd`. Search for the execution summary, completion message, CUDA traceback, backend exception, memory error, or Slurm time-limit message. Absence of a request error in saved records does not automatically prove the process never had a startup failure or interrupted unsaved request.

## Verification level 6: unit tests and analysis tests

```bash
cd /Users/arnavbharti/Developer/arnavbharti/thesis/src
python3 -m unittest discover -s tests -q
```

The report adds tests for exclusive error categories, strict clue/constraint diagnostics, paired outcomes, and backup checksums. Tests supplement re-analysis of actual records. They do not replace the full data audit or establish statistical significance.

## Audit a manuscript number before submission

For every table cell, record its run, experiment, condition, tier, numerator, denominator, and source-file checksum. For a latency mean, verify whether it is call-level, outcome-row-level, new-call-only, or end-to-end revision latency. For an error rate, verify category precedence and whether labels overlap. For a completion statement, verify manifest and markers. For a statistical conclusion, verify pairing, multiple-testing family, and clustering.

# Discussion: supported interpretations, alternatives, and limits

## Lens 1: surface representation versus abstract task

The task's mathematical symmetry is exact. The models' observed output behavior is not identical across label sets. This supports evaluating multiple equivalent representations. It does not require a claim that all representation differences are statistically established. A paired disagreement is an observed outcome even when an aggregate difference has broad uncertainty.

Equal aggregate performance is insufficient evidence of invariance. GPT-OSS's Arabic and uppercase conditions each solve 45/60, but exchange nine successes in each direction. Distinguish aggregate robustness from puzzle-level consistency. Stochastic decoding means even identical prompts can disagree, so the main experiment cannot cleanly separate representation-induced disagreement from ordinary repeat variability without additional repetitions.

## Lens 2: difficulty interaction

Easy performance is high for both selected configurations, and many representation differences appear on more difficult requests. One explanation is that representation changes add a burden that matters when constraint solving already strains the model. Another is that harder prompts generate longer trajectories, increasing opportunities for final-output failure. Neither explanation is directly identified by final-grid-only outcomes.

Clue density and procedural difficulty co-vary. A matched comparison within a puzzle controls underlying difficulty when comparing representations. Comparing easy to hard is not a randomized intervention on one difficulty factor. Avoid causal statements about a single logical technique or number of clues.

## Lens 3: representation errors versus solving errors

Separating output errors from incorrect grids makes the failure pattern more informative. GPT-OSS has 96 nontruncated incorrect grids and 72 truncation/other output failures. Formatting is a substantial issue, but it is not the only issue. Historical constrained-decoding failures reinforce that syntax alone does not establish Sudoku competence under those configurations.

A label set with many output errors may look worse under unconditional scoring even if its parsed outputs are often correct. That is part of the practical final-answer contract, not a reason to discard the errors. Show both unconditional accuracy and diagnostic conditional rates. Avoid ranking models only on successful parsing.

## Lens 4: clue preservation and mathematical validity

Changing clues is a failure to solve the stated puzzle even if the output is another valid Sudoku. The five GPT-OSS main grids that satisfy Sudoku units but are not correct solutions demonstrate this distinction. The clue-preservation checker is essential, not redundant with row/column validity.

Preserved clues do not imply correct completion. Historical Mistral clue-preserving decoder variants still fail units or the solution. A final-grid interface therefore needs several independent checks. This is an engineering lesson about validation, not an analysis of visible reasoning.

## Lens 5: hidden reasoning and resource exhaustion

Reasoning separation solves a scoring-interface problem, not a compute-budget problem. Hidden generation can use nearly the entire context before producing a final grid. The initial Qwen context screen and later successful rerun show why short output ceilings can make a model look less capable under a particular deployment.

However, truncation is not a clean measure of “needed more useful thinking.” It can reflect lengthy ineffective generation, repetition, delayed answer emission, or a problem the model cannot solve. Since the study does not analyze traces, do not choose among these explanations. A longer-limit rerun would measure a new configuration and require a separately documented experiment.

The same token ceiling does not imply the same time budget. Throughput and tokenization differ across models. A time-normalized comparison would be a different estimand. The current study compares the recorded configurations and reports latency separately.

## Lens 6: tokenizer explanations

The main alphabets differ in tokenizer segmentation as well as label identity, familiarity, and Unicode form. Their accuracy ranking does not isolate token count. The dedicated label-length experiment is non-monotonic, and its regression is singular. That evidence blocks a simple causal token-length story rather than confirming one.

GPT-OSS's two-token and Qwen's three-token conditions have the highest observed scores. Their different specific labels, sampling, and correlated properties remain explanations. There is one constructed alphabet per bin per model. Multiple matched label sets and independent repeats remain future work.

## Lens 7: binding and semantics

The ordinary versus permuted conditions suggest an assignment-related difference on the selected sample. Sudoku needs consistent equality relationships, so natural numeric meanings are unnecessary. A model could nevertheless rely on familiar templates or label associations. This is a plausible behavioral explanation.

Both models lose answers under permuted number words, but Qwen gains answers under permuted digits while GPT-OSS loses them. Small differences also fit sampling variation. The prompt does not impose a conflicting arithmetic definition. Internal evidence is absent. Use bounded candidate explanations, not a proven binding mechanism.

## Lens 8: input/output asymmetry

All simple controls succeed, while full Sudoku solving fails. This narrows explanations involving basic symbol copying or the fixed translation task. It does not prove all input processing is flawless during long solving. Cross-mapping adds instructions and an additional conversion requirement, so a weaker cross condition can reflect combined burden rather than output script alone.

GPT-OSS's same-alphabet baselines both score 12/15. Qwen's Arabic and Greek baselines score 13/15 and 11/15, while its Greek-to-Arabic cross remains 11/15. Neither pattern establishes a deterministic Greek-output cause. Sample-specific difficulty, extra mapping instructions, and variability remain alternatives.

## Lens 9: prompt sensitivity and variance

The ablation has genuine prompt changes and identical-prompt repeats. The latter demonstrate outcome variation without an instruction change, despite the recorded fixed sampling seed. They do not identify its numerical or stochastic source, or provide a stable estimate of variance from independent seeds. The highest condition score cannot automatically be explained by its wording. A larger repeated paired experiment is needed to estimate a prompt's expected improvement.

Some ablations change output contract and parsing, while others change symbol identity or empty markers. This is not a clean factorial decomposition of all factors. It can generate practical hypotheses. It cannot estimate every interaction or establish a universally best prompt.

## Lens 10: revision as extra computation and information

GPT-OSS improves from 18/27 to 23/27 after two revisions; checker feedback reaches 22/27 using nine calls. Qwen improves from 23/27 to 26/27 after one revision, but two revisions finish at 23/27 with two fixes and two regressions relative to the initial answer. Its checker reaches 26/27 with four calls. The benefit is not monotonic or universal. Compare eligible initial failures (nine versus four), protected successes, and cumulative generation costs.

The checker supplies constraint violations without a complete solution. That is less information than a solved grid but more information than an unassisted “check yourself” request. Its no-regression property follows partly from skipping initially correct outputs. The study lacks an equal-compute resampling baseline, so it cannot attribute gains exclusively to self-correction skill.

All observed gains are from a small subset dominated by difficult remaining errors. One more correct result changes an arm by 3.7 percentage points. Report counts and paired transitions, not an overprecise general percentage gain.

## Lens 11: model comparison and efficiency

The complete paired matrix supports an accuracy-latency trade-off: Qwen solves 100 more cells but takes longer on average. Its net advantage is largest on hard and medium, while both models are highly accurate on easy. Representation rankings differ numerically without a confirmed interaction. Thirty-four cells are solved only by GPT-OSS, so higher aggregate accuracy is not universal dominance. These distinctions allow a more informative discussion than a single leaderboard ranking.

A model with fewer total parameters can outperform a larger-labeled model on a selected task. That does not establish a scaling law. GPT-OSS uses a different active-compute structure from dense Qwen, and the checkpoints differ in training, quantization, tokenizer, and reasoning control. Avoid “27B is inherently stronger than 120B.”

Total recorded main generation time is 43.62 hours for GPT-OSS and 79.69 hours for Qwen. Dividing by correct outcomes gives 422.14 and 607.78 generation seconds per correct answer. These are offline ratios across successes and failures, not average latency conditional on success. They exclude loading, retries not separately timed, and queue waiting. They are not monetary cost or energy usage. A scheduler-level total should be reported separately and should not double-count reused mechanism baselines.

GPT-OSS generates 29,568,276 tokens in total, a mean of 54,756.07 per request. Qwen generates 21,910,495, a mean of 40,574.99. Despite fewer recorded generation tokens, Qwen takes longer. The aggregate ratios of generated tokens to recorded generation-call seconds are 188.29 and 76.38 tokens per second. These include call overhead and prompt processing within the measured interval, and are not a pure steady-state decode-throughput benchmark. Architecture, quantization, and runtime differ. Token counts do not directly measure useful reasoning, and this study does not inspect traces to explain the difference.

## Lens 12: reproducibility and evaluation design

Frozen plans, pinned revisions, immutable request manifests, and lossless backups make the evidence re-analyzable. They do not guarantee a fresh inference run exactly reproduces every sampled answer. A single fixed seed is not multiple independent seeds. GPU/software differences and call order can affect stochastic execution.

Hash shards are operational units. They do not create 12 independent scientific samples. A timeout and successful resume preserve the same experiment if saved IDs are reused. Independent jobs can run concurrently without changing the logical design, but resource contention may affect latency and must be kept distinct from score.

The provenance files have a null commit field and are captured once. Disclose that limitation rather than manufacturing a stronger reproducibility record. The frozen source digest still constrains code identity for registered experiments.

## What the study does not establish

- It does not prove or disprove that language models reason in a general philosophical sense.
- It does not analyze chain-of-thought faithfulness, reasoning strategies, or internal activations.
- It does not measure human difficulty, all Sudoku variants, larger board sizes, or all possible symbol permutations.
- It does not isolate tokenization from spelling and semantic familiarity in the main comparison.
- It does not establish a vendor-optimal setting for each checkpoint or equal active compute.
- It does not make a clean equal-budget ranking of every historically screened model.
- It does not establish a universal benefit from self-revision or checker feedback.
- It does not show that all length-limited responses would become correct with a higher ceiling.
- It does not prove exact novelty over all prior literature. Close symbol-symmetry work must be acknowledged.
- It does not establish that corresponding follow-ups share a single causal explanation across both models.

## Limitations paragraph checklist

Include the single generated dataset family, 60 main underlying puzzles, one sampled completion per condition, two selected configurations, nested small mechanism subsets, provider-specific reasoning controls, different architecture/quantization, context-bound generation, selection after screening, missing independently varied tokenizer factors, sampling variability, and once-per-run provenance. State that the exact verifier assesses final solutions, not the process by which they were generated.

Both main benchmarks, all selected-model follow-ups, and both final analyses are complete in this capture. GPT-OSS's completed ablation artifact survives a teardown timeout; Qwen's corresponding job completes normally. Preserve execution distinctions instead of misclassifying saved answers as request errors. Future additions require a new capture and audit.

# Conclusion: points to include and what to leave out

The conclusion should be one or two paragraphs. Restate the question and the controlled paired design in past tense. Summarize two or three completed findings. End with the bounded implication for evaluating equivalent symbolic tasks and validating final outputs.

Include that standard Sudoku label substitutions preserve the abstract problem, that the study evaluated pinned local reasoning models without scoring traces, and that outcomes must distinguish correct solutions, grid errors, output failures, and truncation. Include the principal complete main result or final two-model comparison. Mention difficulty dependence and the limited explanatory power of smaller mechanisms if central to your argument.

Do not introduce new numerical analyses in the conclusion. Do not promise unrun experiments as completed work. Do not claim tokenization caused the differences. Do not claim the study proves all current models lack reasoning. Do not write that syntax-only constraints solve correctness.

Future work can name repeated sampling, broader datasets, additional models, tokenizer-matched label sets, equal-time/equal-compute comparisons, and conditional larger-context reruns. Qwen's corresponding mechanisms are now completed, not future work. No new inference was submitted during this update.

## Two defensible paper narratives

**Evaluation-centered narrative.** Lead with paired symbolic representation and difficulty. Use the complete two-model main benchmark, with bounded within-model representation findings and the paired configuration comparison. Use error decomposition as a second contribution. Put most mechanism details and failed-model screening in appendices. This is the clearest route if the paper's main value is a carefully audited empirical benchmark.

**Diagnosis-centered narrative.** Lead with failures at the final-output interface. Use both models' main results, perfect simple controls, different non-monotonic token-length patterns, differing digit-permutation directions, and model-dependent revision. Keep causal claims bounded.

You may combine these, but avoid a paper with six unrelated mini-studies and no central claim. Use the main paired experiment as the anchor. Every mechanism section should answer a specific alternative explanation raised by the main data.

# Recommended figures, tables, and appendix contents

## Main-paper visuals

Figure 1 should show one canonical puzzle encoded in digits, letters, and another alphabet, all mapped back to the same values, followed by the four final-grid checks. It should illustrate the controlled transformation, not decorate the paper with an imagined reasoning trace.

Figure 2 should show the experiment hierarchy. The 300-puzzle dataset feeds disjoint pilot and main samples. Mechanism and ablation sets are nested inside main. The 60 main puzzles become nine representations per model. Indicate reused baselines and shared initial answers so the reader can see the dependencies.

Figure 3 can show alphabet-by-difficulty accuracy with counts or percentages for both completed models. A heatmap or grouped bars is appropriate. The report's generated version now uses the complete matrix, with all 20-request alphabet-by-tier denominators present. Numerical ranking differences should not be illustrated as independently confirmed causal effects.

Figure 4 can show stacked counts of correct, incorrect-grid, truncated, and other-output-error outcomes by tier. The categories must be exclusive and sum to the request count. Operational failures can be shown separately or in the legend as zero.

An optional revision figure should plot correctness against mean end-to-end generation time. It must use cumulative branch cost, not the last generation's latency. A point for checker-guided revision needs a note about conditional intervention.

## Main-paper tables

Table 1 can describe dataset counts, clue ranges, medians, and tier definitions. Table 2 can disclose selected models, revisions, reasoning interfaces, effective sampling, context ceiling, and H100 resources. Table 3 can give main model-by-tier accuracy and failure categories. Table 4 can give alphabet accuracy, baseline retention, and paired discordance counts. Table 5 can summarize the smaller experiments and the limitation on each interpretation.

Use full condition tables in the appendix rather than fitting every small experiment into the main text. Every figure and table must be cited at least once in manuscript prose. State what the reader should notice. Avoid repeating every cell in the surrounding paragraph.

## Appendix structure

Appendix A should contain exact dataset generation and certificate details. Appendix B should contain all alphabets and the full prompt. Appendix C should contain complete main condition-by-tier tables and error-label incidences. Appendix D should contain mechanism prompts and all outcomes. Appendix E should contain stage-level revision transitions and costs. Appendix F should contain historical screening and execution exceptions. Appendix G should contain reproducibility and audit commands.

The report's generated CSV and JSON can be supplementary artifacts. Before publication, review raw logs for credentials and irrelevant shared-account information. This backup intentionally excludes `.env`, and the public repository must never contain tokens. Raw model traces are preserved as generated artifacts but are not a research-analysis target.

# Final author checklist

## Scientific claims

- Each numerical claim has an exact completed evidence source.
- The model names, revisions, precision formats, and effective settings are correct.
- Puzzle counts are distinct from request counts and reused outcome rows.
- Main, pilot, diagnostic, and exploratory results are not pooled.
- Incorrect grids, output errors, and operational failures are separate.
- Parseability and clue preservation use stated denominators.
- Statistical tests respect pairing, clustering, and multiplicity.
- Causal explanations are not substituted for descriptive evidence.
- Both models' follow-up findings are grounded in matching completed artifacts, not inferred from submission or main scores.

## Writing and presentation

- The abstract hits background, gap, contribution, method, result, and implication.
- The introduction is understandable to a beginner-level ML reader.
- Related-work subsections each include specific differentiation.
- Methodology discloses the real prompt and generation bounds.
- Results are organized by questions, with one main takeaway per visual.
- Discussion states alternatives and limitations, not only preferred explanations.
- Conclusion contains no new or unfinished result.
- All references and venue metadata have been manually checked.
- Every visual is cited and every denominator is legible.
- Your final manuscript uses the chosen venue's authentic current template.

## Reproducibility handoff

Invoke `$thesis-paper-report` in a future session to retrieve and update this dossier. The skill routes to the maintained report, numerical audit, raw snapshot, and writing guidance. Invoking it does not authorize new inference, downloads, model installation, or frozen-protocol changes. A report refresh first needs a new read-only evidence capture and the local audit.
