---
title: "Symbolic Representation and LLM Sudoku Performance"
subtitle: "Evidence dossier and section-by-section research-paper writing guide"
author: "Prepared for Arnav Bharti"
date: "30 September 2026"
---

# Purpose, scope, and how to use this report

This is a writing dossier, not a replacement manuscript. You will write the paper yourself. It supplies the facts, definitions, experimental steps, source literature, numerical tables, interpretation boundaries, and verification procedures needed to do that. The attached *Research @ BITS Pilani* guidance determines the writing structure. Recorded requests and results determine the scientific content. Where an older draft, README, handoff, or model-selection note conflicts with the saved evidence, use the evidence.

Read this narrative together with `generated/results_tables.md`. The latter contains every selected-model condition, its difficulty breakdown, error categories, latency, and completion checks. `generated/audit.json` is the machine-readable audit. `generated/observations.csv` contains one row per saved result and can be opened in a spreadsheet. Historical diagnostics are included separately. Do not combine them into one model accuracy figure.

The raw backup is under `evidence/snapshots/2026-09-30-report/`. JSONL results and job logs are losslessly gzip-compressed. A snapshot manifest records both compressed-file and uncompressed-content SHA-256 checksums. The transfer includes result records, frozen protocols, sample plans, provenance, generated Slurm scripts, and logs. It excludes model weights, virtual environments, and credentials. The uncompressed working copy is under the ignored `tmp/research-report/snapshot/` directory.

## Evidence status and the central writing decision

Both selected models have complete qualification, pilot, and main evidence. Each main benchmark contains 540/540 saved records with its exact frozen request digest and all valid completion markers. GPT-OSS also has complete outcome records for Steps 8 through 12. Qwen's final part, job 366222, completed at 19:29:44 IST on 30 September 2026 in 8:18:28 with exit code `0:0`. The final read-only capture followed at 19:31 IST. The local audit covers 2,026 records across the selected and historical runs. It finds no request-content hash, shard, scoring, independent-grid, or dataset-identity disagreement. The generated audit states the status of every included run. Historical incomplete diagnostic trials remain incomplete and must not be described as completed merely because the selected main benchmarks are complete.

No Qwen mechanism experiment is represented in this snapshot. Code exists for those experiments, but implemented code is not completed evidence. Do not write that input/output cross, token length, binding, ablations, or revision replicated across both models. Do not write that the whole project is finished merely because GPT-OSS inference is finished.

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

**Method, one or two sentences.** Mention three technique-defined difficulty tiers, nine alphabets, the same 60 main puzzles across representations, and final-grid-only scoring. Name GPT-OSS-120B and Qwen3.8-27B-FP8. Their complete main evidence is verified. Distinguish the paired main benchmark from smaller GPT-OSS diagnostic experiments.

**Results, one or two sentences.** Select the strongest complete findings. GPT-OSS solved 372/540 requests, or 68.9%, and Qwen solved 472/540, or 87.4%. The paired difference is 18.5 percentage points, with an exploratory stratified puzzle-bootstrap 95% interval of 13.7 to 23.5 points. Both models decline with difficulty. Alphabet accuracies range from 61.7% to 75.0% for GPT-OSS and 80.0% to 93.3% for Qwen, but neither model's eight Arabic-baseline comparisons survives Holm adjustment at 0.05. Do not pack all of these numbers into the abstract. A compact option is the two overall accuracies, a qualitative difficulty trend, and a bounded statement that numerical representation variation was not statistically resolved by these baseline comparisons.

**Implication, one sentence.** State that equivalent symbolic formulations can yield different realized outcomes and that evaluation should distinguish invalid grids, output errors, and resource truncation. Do not claim a proven tokenizer mechanism or a universal inability to reason.

## Decisions to make before writing the abstract

- Decide whether the main message is representation sensitivity, the model comparison, or the separation of failure types. Give one of these priority.
- If the abstract mentions revision, note that the result is a small GPT-OSS subset. Do not let a 27-cell arm dominate the 540-request main study.
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

The dataset has 300 puzzles, 100 per tier. The frozen main sample has 20 per tier. Each model receives 540 main requests. The pilot uses different underlying puzzles. GPT-OSS mechanisms use nested 15-puzzle and nine-puzzle subsets of the main set. Hidden reasoning is permitted, but only the extracted final answer is scored.

Name the two selected checkpoints and state that the experiments run locally on Sharanga H100 compute nodes. “Local” means locally hosted open-weight inference on the university cluster, not inference on your laptop. Do not introduce Nemotron and Mistral as main-study models.

## Paragraph 6: major findings with at most two or three numbers

Choose a small number of complete findings. The two-model version can state 68.9% versus 87.4% overall main accuracy, the 18.5-point paired difference and its exploratory uncertainty, and the descriptive decline with difficulty. If representation ranges are central, state them alongside the absence of Holm-significant Arabic-baseline contrasts, not as established causal penalties.

You may state that correct formatting did not guarantee correctness in historical constrained-decoding diagnostics, but keep the detailed failed-model chronology in an appendix. Do not use these different configurations as a controlled leaderboard against the selected models.

## Paragraph 7: three or four contributions

Candidate contributions, stated in full sentences, are as follows.

1. A reproducible paired evaluation of the same unique-solution Sudoku puzzles under nine symbolic alphabets and three solver-defined difficulty tiers.
2. A final-answer evaluation procedure that separates logical errors, clue changes, output-format failures, and truncation from operational failures.
3. A comparison of the selected open-weight reasoning models under matched puzzle sets, sampling settings, and context ceilings, with model-specific reasoning interfaces disclosed.
4. Targeted GPT-OSS experiments testing input/output remapping, token-length constructions, label assignments, prompt/output choices, and final-answer revision.

Do not describe the dataset as the largest Sudoku benchmark or the models as the strongest possible models. Do not present small mechanism differences as causal discoveries. The distinctive contribution is the controlled combination and auditability, not a claim that every component is new.

## Suggested research questions

RQ1 asks whether realized final-grid accuracy differs across equivalent symbolic alphabets on the same puzzles. RQ2 asks how that pattern changes with solver-defined difficulty and model. RQ3 asks how much failure is attributable to invalid grids versus output errors and truncation. RQ4 asks whether simple Greek-symbol handling or cross-mapping alone explains failures. RQ5 asks what the token-length, binding, and prompt experiments establish or fail to establish. RQ6 asks whether revising a shared initial answer improves correctness, and at what additional cost.

Keep the paper's RQs limited enough that each has a substantive answer. RQ4 through RQ6 currently have GPT-OSS evidence only. The report's discussion later gives alternative organizations if you want a shorter paper.

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

Total records are (15(4+5)=135). Thirty Sudoku baselines are reused, 30 Sudoku cross calls are new, and 75 controls are new. All 75 control outcomes are correct. Some controls repeat a fixed answer such as `9` or `5 3 7`. They are limited checks, not exhaustive proofs of arbitrary Greek understanding or general grid manipulation.

**Purpose.** Separate simple symbol handling from integrated constraint solving and cross-representation output. A successful control excludes some narrow explanations under that prompt, but not every possible parsing, memory, reasoning, or binding problem in the full task.

## 12. Step 9: token-length experiment

Use the selected model's exact tokenizer to search deterministic candidate labels. Bin labels with one, two, or three tokens in isolation. Require the same token count after a leading space. Choose nine distinct labels per bin. Use each constructed alphabet on the same 15 mechanism puzzles, yielding 45 new requests.

Record nominal token length, mean clue tokens, mean symbol UTF-8 bytes, mean code-point count, and prompt tokens. Full-row and contextual tokenization can differ from isolation, so do not describe a label's isolated length as the whole prompt cost.

The registered logistic fit predicts correctness using prompt tokens, mean clue tokens, mean bytes, and mean code points. It returned a singular information matrix. These predictors co-vary in the available construction. There is no independently identified coefficient to interpret. Do not omit this failure and present a clean token-length explanation.

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

All 135 records are saved with a valid marker. The four Sudoku conditions solve 12/15, 12/15, 10/15, and 11/15 for Arabic-to-Arabic, Greek-to-Greek, Greek-to-Arabic, and Arabic-to-Greek. The Sudoku-only total is 45/60. The 75 controls all pass. The combined 120/135 figure mixes solving with simpler controls and should not be presented as the model's Sudoku accuracy.

Sudoku-only easy, medium, and hard correctness is 19/20, 18/20, and 8/20. All four Sudoku conditions score 2/5 on hard. Two hard responses truncate. There are zero request-level operational failures.

The baseline equality of Arabic-to-Arabic and Greek-to-Greek, plus perfect simple controls, does not support a simple universal Greek-output penalty. The cross conditions are lower in aggregate, but their extra instructions and mapping burden confound pure input/output attribution. They also have only 15 puzzles per condition.

## Step 9: token-length construction

All 45 requests are complete. One-token labels solve 9/15, two-token labels 13/15, and three-token labels 10/15. Easy is 15/15, medium 13/15, and hard 4/15 across the three conditions. There are five truncations, four other output errors, four incorrect grids, and zero operational failures.

The best observed condition is the two-token alphabet. Hard correctness is 0/5, 3/5, and 1/5 across the bins. This is non-monotonic. The registered regression reports a singular information matrix for 45 observations. Report the construction and descriptive result without assigning an independently estimated token-length effect.

## Step 10: binding conditions

All 165 records are complete. Overall correctness is 124/165. Easy, medium, and hard counts are 55/55, 50/55, and 19/55. Seven outputs truncate, two have other output errors, and 32 are nontruncated incorrect grids. There are no request-level operational failures.

Ordinary digits, ordinary number words, and nonce labels each solve 12/15. Permuted digits and permuted number words each solve 10/15. Six uppercase assignments range from 10/15 to 13/15. The complete condition table supplies exact results and latency.

Possible interpretation is sensitivity to assignment or familiar-label semantics. However, the smaller permutations are not established causal effects. Five fixed uppercase permutations also vary by up to three outcomes, showing that assignment choice can interact with the selected puzzle sample and sampled generation. Do not state that “semantic conflict causes a 13.3-point loss” as an identified general mechanism.

## Step 11: ablation outcomes and generation variability

All 171 outcome records and a valid completion marker exist. Slurm job 361282 timed out at 15 hours after the result artifact was complete. The saved request records contain no operational errors. Preserve this distinction in the execution appendix. Do not delete the complete data because the scheduler state says `TIMEOUT`.

The overall result is 103/171. Difficulty counts are 55/57 easy, 37/57 medium, and 11/57 hard. Twelve outputs truncate. Mapping to digits and uppercase nonce labels each score 8/9. Compact rows and an 81-symbol string each score 3/9. All 19 conditions and their tier results appear in the companion table.

The four identical-default-prompt conditions score 5/9, 6/9, 5/9, and 7/9. This demonstrates that a two-answer difference can arise without changing the prompt. Consequently an observed 8/9 condition is a candidate for further evaluation, not sufficient evidence to replace the frozen benchmark prompt.

The alternate formats are evaluated under their own parsing rules. A low score can include substantive grid errors as well as formatting failures. Do not claim their entire performance change is an output-format compliance effect without the category breakdown.

## Step 12: revision results and costs

All 108 records are complete. Aggregate final correctness by branch is 18/27 one pass, 19/27 one self-revision, 23/27 two self-revisions, and 22/27 checker-guided revision. The one-pass baseline is exactly shared, so these are paired branches, not four independent 27-request samples.

One self-revision fixes one wrong answer, two self-revisions fix five, and checker-guided revision fixes four. No initially correct answer regresses in these observed arms. Absence of a regression in 18 initially correct cells does not prove revision is safe on all problems. The checker arm cannot regress the initial successes because it does not revise them.

New-call counts are zero, 27, 54, and nine. Additional generation time totals are 0, 4,599.26, 8,057.65, and 4,439.46 seconds. Mean end-to-end generation time per branch cell, including the reused initial answer, is 312.25, 482.60, 610.69, and 476.68 seconds. These are observed generation-time estimates, not scheduler elapsed time or GPU energy.

The table's final-record truncation count is three across the four branches, while all-stage counts are larger because shared initial truncated answers appear in each arm and revisions can truncate. Do not sum shared initial stages and report them as independent truncation events. Use unique source request IDs or explicitly state branch-stage accounting.

The strongest bounded statement is that two generic revisions and one conditional checker revision improve realized final correctness on this nine-puzzle, three-representation subset. Extra compute, branch selection, and feedback are not independently isolated. Qwen revision behavior is not measured in this snapshot.

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

# Experiment-by-experiment writing guide: methodology, results, and discussion

This section adds an experiment-centered route through the dossier. It does not replace the separate Methodology, Results, Discussion, or Conclusion sections, the twelve discussion lenses, or the verification instructions. Use the existing sections for exact prompts, label inventories, scoring definitions, source references, and complete tables. Use the sequence below to write a coherent account of each experiment: question, implementation, rationale, alternatives, limitations, model-specific results, and interpretation.

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

The frozen source passes 82 historical tests. The current repository passes 95 tests. Old and current statistical outputs on the same records are identical apart from the added qualification field `min_correct: 5`. None of these engineering checks adds new model accuracy observations.

### Qwen results and artifacts

Job `373551` was queued for CPU finalization after successful completion of all five follow-up jobs. No completed Qwen Step 13 artifact is used here. Do not substitute the already completed offline main comparison for evidence that every Qwen mechanism prerequisite has finished.

### Discussion and writing decision

Use **Lens 12** to distinguish preserved evidence, exact analysis reproduction, and repeat inference. Report the historical source resolution in a reproducibility appendix rather than allowing an execution detail to dominate the scientific findings. Completion markers establish artifact completeness, not answer correctness. Tests establish the checks they implement, not human-level reasoning or causal identification.

## J. Turning these blocks into manuscript sections

Keep the separate manuscript sections if required by the venue. In Methodology, use the experiment blocks to define each question, treatment, sample, baseline reuse, scoring rule, and limitation. In Results, follow the same experiment order and give the GPT-OSS and Qwen findings together wherever both have verified evidence. In Discussion, revisit each question with its relevant existing lenses and alternatives. This aligns the reader's route without removing section boundaries.

Alternatively, if the venue permits experiment-centered subsections, give each a Methods, Results, and Discussion sequence, then retain a common dataset/scoring section and a cross-experiment limitations section. Avoid repeating the same global settings in every block. State shared settings once and describe only actual deviations.

The main comparison is the anchor. Cross controls test basic handling alternatives; token length examines segmentation-related hypotheses; binding changes assignments; ablations examine interfaces and prompt variability; revision evaluates correction routes and added compute. This logical chain is stronger than presenting unrelated mini-studies. Every explanatory claim must remain bounded by the controls actually performed. Keep the existing twelve lenses as a cross-experiment synthesis, not a list of causal conclusions.


# How to verify every result yourself

## Verification level 1: reproduce the report's local analysis

Run these commands on your machine. They do not use SSH, load a model, install packages, or submit jobs.

```bash
cd /Users/arnavbharti/Developer/arnavbharti/thesis
python3 paper/report/prepare_snapshot.py \
  tmp/research-report/snapshot \
  evidence/snapshots/2026-09-30-report --verify
python3 paper/report/analyze_evidence.py \
  --snapshot evidence/snapshots/2026-09-30-report \
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
root = Path('evidence/snapshots/2026-09-30-report/experiment_outputs')
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
root = Path('evidence/snapshots/2026-09-30-report/experiment_outputs')
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

The two-token condition may benefit from its specific labels, stochastic variation, or other correlated prompt properties. There is only one constructed alphabet per bin. A stronger experiment would use multiple matched label sets and independent repeats, but that has not been completed. Do not present such a design as part of the existing method.

## Lens 7: binding and semantics

The ordinary versus permuted conditions suggest an assignment-related difference on the selected sample. Sudoku needs consistent equality relationships, so natural numeric meanings are unnecessary. A model could nevertheless rely on familiar templates or label associations. This is a plausible behavioral explanation.

But the observed two-answer differences also fit sampling variation at this scale. The prompt does not explicitly impose a conflicting word-to-number definition. Internal activation evidence is absent. Use “consistent with” or “suggests a candidate explanation,” not “proves a binding mechanism” or “isolates semantic interference.”

## Lens 8: input/output asymmetry

All simple controls succeed, while full Sudoku solving fails. This narrows explanations involving basic symbol copying or the fixed translation task. It does not prove all input processing is flawless during long solving. Cross-mapping adds instructions and an additional conversion requirement, so a weaker cross condition can reflect combined burden rather than output script alone.

The two same-alphabet baselines both score 12/15 on the mechanism subset. That result is incompatible with a deterministic universal Greek penalty. It is compatible with sample-specific difficulty, prompt interactions, and stochastic variability. Do not generalize a mechanism-subset equality to the full main sample.

## Lens 9: prompt sensitivity and variance

The ablation has genuine prompt changes and identical-prompt repeats. The latter demonstrate outcome variation without an instruction change, despite the recorded fixed sampling seed. They do not identify its numerical or stochastic source, or provide a stable estimate of variance from independent seeds. The highest condition score cannot automatically be explained by its wording. A larger repeated paired experiment is needed to estimate a prompt's expected improvement.

Some ablations change output contract and parsing, while others change symbol identity or empty markers. This is not a clean factorial decomposition of all factors. It can generate practical hypotheses. It cannot estimate every interaction or establish a universally best prompt.

## Lens 10: revision as extra computation and information

Two revisions improve the observed count from 18/27 to 23/27. Checker-guided revision reaches 22/27 while calling the model on only nine initially wrong cells. This is a useful practical comparison. Its additional compute and selective intervention differ from generic revision.

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
- It does not provide completed Qwen mechanism evidence in the current snapshot.

## Limitations paragraph checklist

Include the single generated dataset family, 60 main underlying puzzles, one sampled completion per condition, two selected configurations, nested small mechanism subsets, provider-specific reasoning controls, different architecture/quantization, context-bound generation, selection after screening, missing independently varied tokenizer factors, sampling variability, and once-per-run provenance. State that the exact verifier assesses final solutions, not the process by which they were generated.

Both main benchmarks are complete in this checksum-verified snapshot. Qwen mechanisms remain unrun in the captured evidence. Do not conceal that a historical or GPT-OSS job timeout happened, but do not misclassify checkpointed or completed outcome data as operational request errors. If later experiments are added, update the evidence capture and analysis before adding their findings.

# Conclusion: points to include and what to leave out

The conclusion should be one or two paragraphs. Restate the question and the controlled paired design in past tense. Summarize two or three completed findings. End with the bounded implication for evaluating equivalent symbolic tasks and validating final outputs.

Include that standard Sudoku label substitutions preserve the abstract problem, that the study evaluated pinned local reasoning models without scoring traces, and that outcomes must distinguish correct solutions, grid errors, output failures, and truncation. Include the principal complete main result or final two-model comparison. Mention difficulty dependence and the limited explanatory power of smaller mechanisms if central to your argument.

Do not introduce new numerical analyses in the conclusion. Do not promise unrun experiments as completed work. Do not claim tokenization caused the differences. Do not claim the study proves all current models lack reasoning. Do not write that syntax-only constraints solve correctness.

Future work can name repeated sampling, broader datasets, additional models, tokenizer-matched label sets, equal-time/equal-compute comparisons, Qwen mechanism replication, and conditional reruns with a larger context. These are proposals, not accomplishments. No such inference was submitted while preparing this report.

## Two defensible paper narratives

**Evaluation-centered narrative.** Lead with paired symbolic representation and difficulty. Use the complete two-model main benchmark, with bounded within-model representation findings and the paired configuration comparison. Use error decomposition as a second contribution. Put most mechanism details and failed-model screening in appendices. This is the clearest route if the paper's main value is a carefully audited empirical benchmark.

**Diagnosis-centered narrative.** Lead with why an apparently equivalent task can fail at the final-output interface. Present GPT-OSS main results, simple-symbol controls, non-monotonic token-length evidence, and revision results. Keep explanations explicitly bounded. Do not market the diagnostic experiments as a causal mechanistic discovery.

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
- Missing Qwen mechanisms or analysis stages remain explicitly unclaimed.

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


# Evidence figures

These figures are generated from the same audit JSON as the tables. They display realized outcomes, not causal effects or independent request-level confidence intervals.

![The design hierarchy distinguishes disjoint pilot/main puzzles from nested diagnostic sets and reused evidence.](generated/design_hierarchy.png)

![Main accuracy by alphabet and difficulty. Every cell includes its correct count and saved denominator.](generated/accuracy_heatmap.png)

![Exclusive final-outcome categories by difficulty. Counts sum to each saved denominator. Length-stopped incorrect answers take precedence over other output errors.](generated/failure_decomposition.png)

![Revision accuracy against mean cumulative generation time. All branches share the same initial answers. The checker intervenes only on initially incorrect outputs.](generated/revision_cost.png)

# Verified results tables

Generated locally from the backed-up result records. These tables are the numeric companion to the writing report.

## GPT-OSS qualification

Evidence path: `local-models-v1/gpt-oss-120b-local/qualification`. Saved 5 of 5. Complete: True.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All | 5/5 | 100.0 | 0 | 0 | 0 | 0 | 44.61 |
| easy | 5/5 | 100.0 | 0 | 0 | 0 | 0 | 44.61 |

Parseable Sudoku grids: 5/5. Clues preserved among parseable grids: 5/5. Valid Sudoku units together: 5/5. Median record latency: 45.16 seconds. Reused outcome rows: 0.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| arabic_digits | 1/1 | 100.0 | 0 | 0 | 0 | 0 | 30.19 |
| devanagari_numerals | 1/1 | 100.0 | 0 | 0 | 0 | 0 | 25.46 |
| emoji | 1/1 | 100.0 | 0 | 0 | 0 | 0 | 60.58 |
| greek_letters | 1/1 | 100.0 | 0 | 0 | 0 | 0 | 45.16 |
| nonce_labels | 1/1 | 100.0 | 0 | 0 | 0 | 0 | 61.64 |

### Condition by difficulty

| Condition | Easy | Medium | Hard |
| --- | --- | --- | --- |
| arabic_digits | 1/1 | 0/0 | 0/0 |
| devanagari_numerals | 1/1 | 0/0 | 0/0 |
| emoji | 1/1 | 0/0 | 0/0 |
| greek_letters | 1/1 | 0/0 | 0/0 |
| nonce_labels | 1/1 | 0/0 | 0/0 |

## GPT-OSS exp2

Evidence path: `local-models-v1/gpt-oss-120b-local/exp2`. Saved 60 of 60. Complete: True.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All | 47/60 | 78.3 | 8 | 2 | 3 | 0 | 252.48 |
| easy | 20/20 | 100.0 | 0 | 0 | 0 | 0 | 48.96 |
| medium | 13/20 | 65.0 | 4 | 2 | 1 | 0 | 397.82 |
| hard | 14/20 | 70.0 | 4 | 0 | 2 | 0 | 310.64 |

Parseable Sudoku grids: 55/60. Clues preserved among parseable grids: 53/55. Valid Sudoku units together: 47/55. Median record latency: 194.85 seconds. Reused outcome rows: 0.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| arabic_digits | 14/15 | 93.3 | 0 | 1 | 0 | 0 | 245.76 |
| emoji | 13/15 | 86.7 | 0 | 1 | 1 | 0 | 233.41 |
| greek_letters | 10/15 | 66.7 | 3 | 0 | 2 | 0 | 301.58 |
| uppercase_latin | 10/15 | 66.7 | 5 | 0 | 0 | 0 | 229.15 |

### Condition by difficulty

| Condition | Easy | Medium | Hard |
| --- | --- | --- | --- |
| arabic_digits | 5/5 | 4/5 | 5/5 |
| emoji | 5/5 | 4/5 | 4/5 |
| greek_letters | 5/5 | 3/5 | 2/5 |
| uppercase_latin | 5/5 | 2/5 | 3/5 |

## GPT-OSS exp4

Evidence path: `local-models-v1/gpt-oss-120b-local/exp4`. Saved 540 of 540. Complete: True.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All | 372/540 | 68.9 | 96 | 24 | 48 | 0 | 290.81 |
| easy | 171/180 | 95.0 | 1 | 0 | 8 | 0 | 53.48 |
| medium | 121/180 | 67.2 | 35 | 8 | 16 | 0 | 372.49 |
| hard | 80/180 | 44.4 | 60 | 16 | 24 | 0 | 446.45 |

Parseable Sudoku grids: 468/540. Clues preserved among parseable grids: 454/468. Valid Sudoku units together: 377/468. Median record latency: 240.46 seconds. Reused outcome rows: 0.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| abstract_symbols | 38/60 | 63.3 | 6 | 7 | 9 | 0 | 360.32 |
| arabic_digits | 45/60 | 75.0 | 14 | 1 | 0 | 0 | 265.80 |
| bengali_numerals | 43/60 | 71.7 | 8 | 2 | 7 | 0 | 274.01 |
| devanagari_numerals | 39/60 | 65.0 | 13 | 1 | 7 | 0 | 237.15 |
| emoji | 38/60 | 63.3 | 9 | 3 | 10 | 0 | 322.34 |
| greek_letters | 37/60 | 61.7 | 15 | 3 | 5 | 0 | 304.23 |
| lowercase_latin | 44/60 | 73.3 | 11 | 2 | 3 | 0 | 261.15 |
| nonce_labels | 43/60 | 71.7 | 8 | 3 | 6 | 0 | 331.12 |
| uppercase_latin | 45/60 | 75.0 | 12 | 2 | 1 | 0 | 261.14 |

### Condition by difficulty

| Condition | Easy | Medium | Hard |
| --- | --- | --- | --- |
| abstract_symbols | 18/20 | 10/20 | 10/20 |
| arabic_digits | 20/20 | 14/20 | 11/20 |
| bengali_numerals | 17/20 | 15/20 | 11/20 |
| devanagari_numerals | 18/20 | 12/20 | 9/20 |
| emoji | 18/20 | 13/20 | 7/20 |
| greek_letters | 20/20 | 11/20 | 6/20 |
| lowercase_latin | 20/20 | 15/20 | 9/20 |
| nonce_labels | 20/20 | 16/20 | 7/20 |
| uppercase_latin | 20/20 | 15/20 | 10/20 |

### Paired comparisons against Arabic digits

| Alphabet | Paired | Retained / Arabic correct | Arabic only | Alphabet only | Exact p | Holm p |
| --- | --- | --- | --- | --- | --- | --- |
| abstract_symbols | 60 | 31/45 | 14 | 7 | 0.1892 | 1.0000 |
| bengali_numerals | 60 | 36/45 | 9 | 7 | 0.8036 | 1.0000 |
| devanagari_numerals | 60 | 36/45 | 9 | 3 | 0.1460 | 1.0000 |
| emoji | 60 | 32/45 | 13 | 6 | 0.1671 | 1.0000 |
| greek_letters | 60 | 36/45 | 9 | 1 | 0.0215 | 0.1719 |
| lowercase_latin | 60 | 37/45 | 8 | 7 | 1.0000 | 1.0000 |
| nonce_labels | 60 | 36/45 | 9 | 7 | 0.8036 | 1.0000 |
| uppercase_latin | 60 | 36/45 | 9 | 9 | 1.0000 | 1.0000 |

### Difficulty-specific paired retention

These use the registered retention procedure. The p-values below are unadjusted exploratory tier comparisons, not independent confirmation tests. The eight-comparison Holm family above covers the all-tier alphabet comparisons only.

| Alphabet | Tier | Retained / Arabic correct | Arabic only | Alphabet only | Exact p |
| --- | --- | --- | --- | --- | --- |
| abstract_symbols | easy | 18/20 | 2 | 0 | 0.5000 |
| abstract_symbols | medium | 8/14 | 6 | 2 | 0.2891 |
| abstract_symbols | hard | 5/11 | 6 | 5 | 1.0000 |
| bengali_numerals | easy | 17/20 | 3 | 0 | 0.2500 |
| bengali_numerals | medium | 13/14 | 1 | 2 | 1.0000 |
| bengali_numerals | hard | 6/11 | 5 | 5 | 1.0000 |
| devanagari_numerals | easy | 18/20 | 2 | 0 | 0.5000 |
| devanagari_numerals | medium | 11/14 | 3 | 1 | 0.6250 |
| devanagari_numerals | hard | 7/11 | 4 | 2 | 0.6875 |
| emoji | easy | 18/20 | 2 | 0 | 0.5000 |
| emoji | medium | 8/14 | 6 | 5 | 1.0000 |
| emoji | hard | 6/11 | 5 | 1 | 0.2188 |
| greek_letters | easy | 20/20 | 0 | 0 | 1.0000 |
| greek_letters | medium | 11/14 | 3 | 0 | 0.2500 |
| greek_letters | hard | 5/11 | 6 | 1 | 0.1250 |
| lowercase_latin | easy | 20/20 | 0 | 0 | 1.0000 |
| lowercase_latin | medium | 12/14 | 2 | 3 | 1.0000 |
| lowercase_latin | hard | 5/11 | 6 | 4 | 0.7539 |
| nonce_labels | easy | 20/20 | 0 | 0 | 1.0000 |
| nonce_labels | medium | 12/14 | 2 | 4 | 0.6875 |
| nonce_labels | hard | 4/11 | 7 | 3 | 0.3438 |
| uppercase_latin | easy | 20/20 | 0 | 0 | 1.0000 |
| uppercase_latin | medium | 10/14 | 4 | 5 | 1.0000 |
| uppercase_latin | hard | 6/11 | 5 | 4 | 1.0000 |

## GPT-OSS exp6

Evidence path: `local-models-v1/gpt-oss-120b-local/exp6`. Saved 135 of 135. Complete: True.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All | 120/135 | 88.9 | 9 | 2 | 4 | 0 | 120.43 |
| easy | 44/45 | 97.8 | 1 | 0 | 0 | 0 | 34.91 |
| medium | 43/45 | 95.6 | 2 | 0 | 0 | 0 | 103.51 |
| hard | 33/45 | 73.3 | 6 | 2 | 4 | 0 | 222.89 |

Parseable Sudoku grids: 54/60. Clues preserved among parseable grids: 50/54. Valid Sudoku units together: 47/54. Median record latency: 8.51 seconds. Reused outcome rows: 30.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A_arabic_to_arabic | 12/15 | 80.0 | 2 | 1 | 0 | 0 | 257.30 |
| B_greek_to_greek | 12/15 | 80.0 | 2 | 0 | 1 | 0 | 265.74 |
| C_greek_to_arabic | 10/15 | 66.7 | 3 | 1 | 1 | 0 | 295.16 |
| D_arabic_to_greek | 11/15 | 73.3 | 2 | 0 | 2 | 0 | 250.25 |
| control_coordinate_retrieval | 15/15 | 100.0 | 0 | 0 | 0 | 0 | 2.20 |
| control_copy | 15/15 | 100.0 | 0 | 0 | 0 | 0 | 0.98 |
| control_grid_conversion | 15/15 | 100.0 | 0 | 0 | 0 | 0 | 8.26 |
| control_mapping_translation | 15/15 | 100.0 | 0 | 0 | 0 | 0 | 0.85 |
| control_occurrence_count | 15/15 | 100.0 | 0 | 0 | 0 | 0 | 3.16 |

### Condition by difficulty

| Condition | Easy | Medium | Hard |
| --- | --- | --- | --- |
| A_arabic_to_arabic | 5/5 | 5/5 | 2/5 |
| B_greek_to_greek | 5/5 | 5/5 | 2/5 |
| C_greek_to_arabic | 4/5 | 4/5 | 2/5 |
| D_arabic_to_greek | 5/5 | 4/5 | 2/5 |
| control_coordinate_retrieval | 5/5 | 5/5 | 5/5 |
| control_copy | 5/5 | 5/5 | 5/5 |
| control_grid_conversion | 5/5 | 5/5 | 5/5 |
| control_mapping_translation | 5/5 | 5/5 | 5/5 |
| control_occurrence_count | 5/5 | 5/5 | 5/5 |

## GPT-OSS exp7

Evidence path: `local-models-v1/gpt-oss-120b-local/exp7`. Saved 45 of 45. Complete: True.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All | 32/45 | 71.1 | 4 | 5 | 4 | 0 | 319.74 |
| easy | 15/15 | 100.0 | 0 | 0 | 0 | 0 | 78.96 |
| medium | 13/15 | 86.7 | 0 | 1 | 1 | 0 | 320.83 |
| hard | 4/15 | 26.7 | 4 | 4 | 3 | 0 | 559.44 |

Parseable Sudoku grids: 36/45. Clues preserved among parseable grids: 35/36. Valid Sudoku units together: 33/36. Median record latency: 240.75 seconds. Reused outcome rows: 0.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| neutral_1_tokens | 9/15 | 60.0 | 1 | 2 | 3 | 0 | 345.30 |
| neutral_2_tokens | 13/15 | 86.7 | 2 | 0 | 0 | 0 | 287.10 |
| neutral_3_tokens | 10/15 | 66.7 | 1 | 3 | 1 | 0 | 326.83 |

### Condition by difficulty

| Condition | Easy | Medium | Hard |
| --- | --- | --- | --- |
| neutral_1_tokens | 5/5 | 4/5 | 0/5 |
| neutral_2_tokens | 5/5 | 5/5 | 3/5 |
| neutral_3_tokens | 5/5 | 4/5 | 1/5 |

## GPT-OSS exp8

Evidence path: `local-models-v1/gpt-oss-120b-local/exp8`. Saved 165 of 165. Complete: True.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All | 124/165 | 75.2 | 32 | 7 | 2 | 0 | 272.25 |
| easy | 55/55 | 100.0 | 0 | 0 | 0 | 0 | 51.62 |
| medium | 50/55 | 90.9 | 3 | 2 | 0 | 0 | 282.08 |
| hard | 19/55 | 34.5 | 29 | 5 | 2 | 0 | 483.04 |

Parseable Sudoku grids: 156/165. Clues preserved among parseable grids: 155/156. Valid Sudoku units together: 125/156. Median record latency: 203.68 seconds. Reused outcome rows: 45.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| digits_ordinary | 12/15 | 80.0 | 2 | 1 | 0 | 0 | 257.30 |
| digits_permuted | 10/15 | 66.7 | 4 | 1 | 0 | 0 | 295.63 |
| nonce_neutral | 12/15 | 80.0 | 2 | 1 | 0 | 0 | 296.92 |
| number_words_conflicting | 10/15 | 66.7 | 4 | 1 | 0 | 0 | 313.16 |
| number_words_ordinary | 12/15 | 80.0 | 3 | 0 | 0 | 0 | 258.97 |
| uppercase_random_1 | 11/15 | 73.3 | 3 | 1 | 0 | 0 | 258.11 |
| uppercase_random_2 | 11/15 | 73.3 | 3 | 1 | 0 | 0 | 274.32 |
| uppercase_random_3 | 13/15 | 86.7 | 2 | 0 | 0 | 0 | 247.60 |
| uppercase_random_4 | 12/15 | 80.0 | 2 | 0 | 1 | 0 | 218.08 |
| uppercase_random_5 | 10/15 | 66.7 | 4 | 0 | 1 | 0 | 273.44 |
| uppercase_standard | 11/15 | 73.3 | 3 | 1 | 0 | 0 | 301.17 |

### Condition by difficulty

| Condition | Easy | Medium | Hard |
| --- | --- | --- | --- |
| digits_ordinary | 5/5 | 5/5 | 2/5 |
| digits_permuted | 5/5 | 4/5 | 1/5 |
| nonce_neutral | 5/5 | 5/5 | 2/5 |
| number_words_conflicting | 5/5 | 4/5 | 1/5 |
| number_words_ordinary | 5/5 | 4/5 | 3/5 |
| uppercase_random_1 | 5/5 | 5/5 | 1/5 |
| uppercase_random_2 | 5/5 | 5/5 | 1/5 |
| uppercase_random_3 | 5/5 | 5/5 | 3/5 |
| uppercase_random_4 | 5/5 | 5/5 | 2/5 |
| uppercase_random_5 | 5/5 | 4/5 | 1/5 |
| uppercase_standard | 5/5 | 4/5 | 2/5 |

## GPT-OSS exp9

Evidence path: `local-models-v1/gpt-oss-120b-local/exp9`. Saved 171 of 171. Complete: True.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All | 103/171 | 60.2 | 42 | 12 | 14 | 0 | 311.03 |
| easy | 55/57 | 96.5 | 1 | 0 | 1 | 0 | 78.20 |
| medium | 37/57 | 64.9 | 11 | 2 | 7 | 0 | 351.60 |
| hard | 11/57 | 19.3 | 30 | 10 | 6 | 0 | 503.29 |

Parseable Sudoku grids: 145/171. Clues preserved among parseable grids: 140/145. Valid Sudoku units together: 104/145. Median record latency: 242.87 seconds. Reused outcome rows: 0.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| empty_dot | 7/9 | 77.8 | 1 | 1 | 0 | 0 | 254.11 |
| empty_underscore | 4/9 | 44.4 | 2 | 2 | 1 | 0 | 380.01 |
| empty_word | 6/9 | 66.7 | 2 | 0 | 1 | 0 | 336.26 |
| empty_zero | 6/9 | 66.7 | 2 | 1 | 0 | 0 | 247.09 |
| latin_lowercase | 7/9 | 77.8 | 1 | 1 | 0 | 0 | 271.58 |
| latin_uppercase | 5/9 | 55.6 | 4 | 0 | 0 | 0 | 291.01 |
| mapping_alphabet_only | 6/9 | 66.7 | 2 | 0 | 1 | 0 | 332.66 |
| mapping_to_abstract | 5/9 | 55.6 | 3 | 1 | 0 | 0 | 328.28 |
| mapping_to_digits | 8/9 | 88.9 | 1 | 0 | 0 | 0 | 221.84 |
| nonce_lowercase | 4/9 | 44.4 | 2 | 2 | 1 | 0 | 329.19 |
| nonce_uppercase | 8/9 | 88.9 | 1 | 0 | 0 | 0 | 307.07 |
| output_compact | 3/9 | 33.3 | 4 | 0 | 2 | 0 | 297.93 |
| output_json | 5/9 | 55.6 | 2 | 0 | 2 | 0 | 342.12 |
| output_spaced | 5/9 | 55.6 | 3 | 0 | 1 | 0 | 356.57 |
| output_string81 | 3/9 | 33.3 | 4 | 0 | 2 | 0 | 271.33 |
| rules_constraints_alphabet | 5/9 | 55.6 | 1 | 3 | 0 | 0 | 387.82 |
| rules_explicit_constraints | 6/9 | 66.7 | 2 | 1 | 0 | 0 | 333.62 |
| rules_fully_explicit | 5/9 | 55.6 | 3 | 0 | 1 | 0 | 322.96 |
| rules_minimal | 5/9 | 55.6 | 2 | 0 | 2 | 0 | 298.12 |

### Condition by difficulty

| Condition | Easy | Medium | Hard |
| --- | --- | --- | --- |
| empty_dot | 3/3 | 3/3 | 1/3 |
| empty_underscore | 3/3 | 1/3 | 0/3 |
| empty_word | 3/3 | 3/3 | 0/3 |
| empty_zero | 3/3 | 3/3 | 0/3 |
| latin_lowercase | 3/3 | 3/3 | 1/3 |
| latin_uppercase | 3/3 | 2/3 | 0/3 |
| mapping_alphabet_only | 3/3 | 2/3 | 1/3 |
| mapping_to_abstract | 3/3 | 2/3 | 0/3 |
| mapping_to_digits | 3/3 | 3/3 | 2/3 |
| nonce_lowercase | 3/3 | 1/3 | 0/3 |
| nonce_uppercase | 3/3 | 3/3 | 2/3 |
| output_compact | 2/3 | 1/3 | 0/3 |
| output_json | 3/3 | 1/3 | 1/3 |
| output_spaced | 3/3 | 1/3 | 1/3 |
| output_string81 | 2/3 | 1/3 | 0/3 |
| rules_constraints_alphabet | 3/3 | 2/3 | 0/3 |
| rules_explicit_constraints | 3/3 | 2/3 | 1/3 |
| rules_fully_explicit | 3/3 | 1/3 | 1/3 |
| rules_minimal | 3/3 | 2/3 | 0/3 |

## GPT-OSS exp10

Evidence path: `local-models-v1/gpt-oss-120b-local/exp10`. Saved 108 of 108. Complete: True.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All | 82/108 | 75.9 | 17 | 3 | 6 | 0 | 218.14 |
| easy | 36/36 | 100.0 | 0 | 0 | 0 | 0 | 49.51 |
| medium | 35/36 | 97.2 | 0 | 0 | 1 | 0 | 146.96 |
| hard | 11/36 | 30.6 | 17 | 3 | 5 | 0 | 457.96 |

Parseable Sudoku grids: 99/108. Clues preserved among parseable grids: 94/99. Valid Sudoku units together: 85/99. Median record latency: 94.84 seconds. Reused outcome rows: 0.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| arabic_digits:checker_guided_revision | 8/9 | 88.9 | 1 | 0 | 0 | 0 | 208.05 |
| arabic_digits:one_pass | 7/9 | 77.8 | 1 | 1 | 0 | 0 | 293.91 |
| arabic_digits:one_self_revision | 7/9 | 77.8 | 2 | 0 | 0 | 0 | 65.22 |
| arabic_digits:two_self_revisions | 8/9 | 88.9 | 1 | 0 | 0 | 0 | 14.23 |
| emoji:checker_guided_revision | 7/9 | 77.8 | 1 | 1 | 0 | 0 | 295.83 |
| emoji:one_pass | 5/9 | 55.6 | 1 | 0 | 3 | 0 | 331.79 |
| emoji:one_self_revision | 6/9 | 66.7 | 2 | 0 | 1 | 0 | 220.78 |
| emoji:two_self_revisions | 8/9 | 88.9 | 1 | 0 | 0 | 0 | 104.58 |
| greek_letters:checker_guided_revision | 7/9 | 77.8 | 1 | 1 | 0 | 0 | 331.56 |
| greek_letters:one_pass | 6/9 | 66.7 | 2 | 0 | 1 | 0 | 311.06 |
| greek_letters:one_self_revision | 6/9 | 66.7 | 3 | 0 | 0 | 0 | 225.02 |
| greek_letters:two_self_revisions | 7/9 | 77.8 | 1 | 0 | 1 | 0 | 215.69 |

### Condition by difficulty

| Condition | Easy | Medium | Hard |
| --- | --- | --- | --- |
| arabic_digits:checker_guided_revision | 3/3 | 3/3 | 2/3 |
| arabic_digits:one_pass | 3/3 | 3/3 | 1/3 |
| arabic_digits:one_self_revision | 3/3 | 3/3 | 1/3 |
| arabic_digits:two_self_revisions | 3/3 | 3/3 | 2/3 |
| emoji:checker_guided_revision | 3/3 | 3/3 | 1/3 |
| emoji:one_pass | 3/3 | 2/3 | 0/3 |
| emoji:one_self_revision | 3/3 | 3/3 | 0/3 |
| emoji:two_self_revisions | 3/3 | 3/3 | 2/3 |
| greek_letters:checker_guided_revision | 3/3 | 3/3 | 1/3 |
| greek_letters:one_pass | 3/3 | 3/3 | 0/3 |
| greek_letters:one_self_revision | 3/3 | 3/3 | 0/3 |
| greek_letters:two_self_revisions | 3/3 | 3/3 | 1/3 |

### Shared-initial revision transitions and compute

| Arm | Correct | Fixed | Regressed | New calls | Extra seconds | Mean end-to-end seconds | All-stage truncations |
| --- | --- | --- | --- | --- | --- | --- | --- |
| checker_guided_revision | 22 | 4 | 0 | 9 | 4439.46 | 476.68 | 3 |
| one_pass | 18 | 0 | 0 | 0 | 0.00 | 312.25 | 1 |
| one_self_revision | 19 | 1 | 0 | 27 | 4599.26 | 482.60 | 1 |
| two_self_revisions | 23 | 5 | 0 | 54 | 8057.65 | 610.69 | 1 |

## Qwen qualification

Evidence path: `qwen-3.8-27b-v2/qwen-3.8-27b-local/qualification`. Saved 5 of 5. Complete: True.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All | 5/5 | 100.0 | 0 | 0 | 0 | 0 | 98.69 |
| easy | 5/5 | 100.0 | 0 | 0 | 0 | 0 | 98.69 |

Parseable Sudoku grids: 5/5. Clues preserved among parseable grids: 5/5. Valid Sudoku units together: 5/5. Median record latency: 75.62 seconds. Reused outcome rows: 0.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| arabic_digits | 1/1 | 100.0 | 0 | 0 | 0 | 0 | 51.00 |
| devanagari_numerals | 1/1 | 100.0 | 0 | 0 | 0 | 0 | 56.05 |
| emoji | 1/1 | 100.0 | 0 | 0 | 0 | 0 | 86.52 |
| greek_letters | 1/1 | 100.0 | 0 | 0 | 0 | 0 | 224.27 |
| nonce_labels | 1/1 | 100.0 | 0 | 0 | 0 | 0 | 75.62 |

### Condition by difficulty

| Condition | Easy | Medium | Hard |
| --- | --- | --- | --- |
| arabic_digits | 1/1 | 0/0 | 0/0 |
| devanagari_numerals | 1/1 | 0/0 | 0/0 |
| emoji | 1/1 | 0/0 | 0/0 |
| greek_letters | 1/1 | 0/0 | 0/0 |
| nonce_labels | 1/1 | 0/0 | 0/0 |

## Qwen exp2

Evidence path: `qwen-3.8-27b-v2/qwen-3.8-27b-local/exp2`. Saved 60 of 60. Complete: True.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All | 54/60 | 90.0 | 3 | 2 | 1 | 0 | 452.30 |
| easy | 20/20 | 100.0 | 0 | 0 | 0 | 0 | 122.37 |
| medium | 16/20 | 80.0 | 2 | 1 | 1 | 0 | 654.35 |
| hard | 18/20 | 90.0 | 1 | 1 | 0 | 0 | 580.18 |

Parseable Sudoku grids: 57/60. Clues preserved among parseable grids: 56/57. Valid Sudoku units together: 55/57. Median record latency: 395.60 seconds. Reused outcome rows: 0.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| arabic_digits | 13/15 | 86.7 | 2 | 0 | 0 | 0 | 361.94 |
| emoji | 13/15 | 86.7 | 0 | 1 | 1 | 0 | 517.06 |
| greek_letters | 13/15 | 86.7 | 1 | 1 | 0 | 0 | 561.78 |
| uppercase_latin | 15/15 | 100.0 | 0 | 0 | 0 | 0 | 368.43 |

### Condition by difficulty

| Condition | Easy | Medium | Hard |
| --- | --- | --- | --- |
| arabic_digits | 5/5 | 4/5 | 4/5 |
| emoji | 5/5 | 4/5 | 4/5 |
| greek_letters | 5/5 | 3/5 | 5/5 |
| uppercase_latin | 5/5 | 5/5 | 5/5 |

## Qwen exp4

Evidence path: `qwen-3.8-27b-v2/qwen-3.8-27b-local/exp4`. Saved 540 of 540. Complete: True.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All | 472/540 | 87.4 | 33 | 24 | 11 | 0 | 531.25 |
| easy | 174/180 | 96.7 | 5 | 0 | 1 | 0 | 110.10 |
| medium | 160/180 | 88.9 | 15 | 2 | 3 | 0 | 605.11 |
| hard | 138/180 | 76.7 | 13 | 22 | 7 | 0 | 878.53 |

Parseable Sudoku grids: 505/540. Clues preserved among parseable grids: 488/505. Valid Sudoku units together: 487/505. Median record latency: 422.78 seconds. Reused outcome rows: 0.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| abstract_symbols | 51/60 | 85.0 | 4 | 0 | 5 | 0 | 532.99 |
| arabic_digits | 53/60 | 88.3 | 3 | 4 | 0 | 0 | 495.67 |
| bengali_numerals | 53/60 | 88.3 | 2 | 4 | 1 | 0 | 540.67 |
| devanagari_numerals | 56/60 | 93.3 | 1 | 2 | 1 | 0 | 438.53 |
| emoji | 54/60 | 90.0 | 2 | 2 | 2 | 0 | 533.41 |
| greek_letters | 51/60 | 85.0 | 8 | 1 | 0 | 0 | 533.51 |
| lowercase_latin | 51/60 | 85.0 | 6 | 2 | 1 | 0 | 560.07 |
| nonce_labels | 48/60 | 80.0 | 4 | 7 | 1 | 0 | 657.13 |
| uppercase_latin | 55/60 | 91.7 | 3 | 2 | 0 | 0 | 489.22 |

### Condition by difficulty

| Condition | Easy | Medium | Hard |
| --- | --- | --- | --- |
| abstract_symbols | 19/20 | 17/20 | 15/20 |
| arabic_digits | 20/20 | 19/20 | 14/20 |
| bengali_numerals | 19/20 | 19/20 | 15/20 |
| devanagari_numerals | 20/20 | 19/20 | 17/20 |
| emoji | 19/20 | 20/20 | 15/20 |
| greek_letters | 20/20 | 17/20 | 14/20 |
| lowercase_latin | 19/20 | 15/20 | 17/20 |
| nonce_labels | 19/20 | 16/20 | 13/20 |
| uppercase_latin | 19/20 | 18/20 | 18/20 |

### Paired comparisons against Arabic digits

| Alphabet | Paired | Retained / Arabic correct | Arabic only | Alphabet only | Exact p | Holm p |
| --- | --- | --- | --- | --- | --- | --- |
| abstract_symbols | 60 | 44/53 | 9 | 7 | 0.8036 | 1.0000 |
| bengali_numerals | 60 | 48/53 | 5 | 5 | 1.0000 | 1.0000 |
| devanagari_numerals | 60 | 51/53 | 2 | 5 | 0.4531 | 1.0000 |
| emoji | 60 | 48/53 | 5 | 6 | 1.0000 | 1.0000 |
| greek_letters | 60 | 46/53 | 7 | 5 | 0.7744 | 1.0000 |
| lowercase_latin | 60 | 46/53 | 7 | 5 | 0.7744 | 1.0000 |
| nonce_labels | 60 | 43/53 | 10 | 5 | 0.3018 | 1.0000 |
| uppercase_latin | 60 | 49/53 | 4 | 6 | 0.7539 | 1.0000 |

### Difficulty-specific paired retention

These use the registered retention procedure. The p-values below are unadjusted exploratory tier comparisons, not independent confirmation tests. The eight-comparison Holm family above covers the all-tier alphabet comparisons only.

| Alphabet | Tier | Retained / Arabic correct | Arabic only | Alphabet only | Exact p |
| --- | --- | --- | --- | --- | --- |
| abstract_symbols | easy | 19/20 | 1 | 0 | 1.0000 |
| abstract_symbols | medium | 16/19 | 3 | 1 | 0.6250 |
| abstract_symbols | hard | 9/14 | 5 | 6 | 1.0000 |
| bengali_numerals | easy | 19/20 | 1 | 0 | 1.0000 |
| bengali_numerals | medium | 18/19 | 1 | 1 | 1.0000 |
| bengali_numerals | hard | 11/14 | 3 | 4 | 1.0000 |
| devanagari_numerals | easy | 20/20 | 0 | 0 | 1.0000 |
| devanagari_numerals | medium | 18/19 | 1 | 1 | 1.0000 |
| devanagari_numerals | hard | 13/14 | 1 | 4 | 0.3750 |
| emoji | easy | 19/20 | 1 | 0 | 1.0000 |
| emoji | medium | 19/19 | 0 | 1 | 1.0000 |
| emoji | hard | 10/14 | 4 | 5 | 1.0000 |
| greek_letters | easy | 20/20 | 0 | 0 | 1.0000 |
| greek_letters | medium | 17/19 | 2 | 0 | 0.5000 |
| greek_letters | hard | 9/14 | 5 | 5 | 1.0000 |
| lowercase_latin | easy | 19/20 | 1 | 0 | 1.0000 |
| lowercase_latin | medium | 14/19 | 5 | 1 | 0.2188 |
| lowercase_latin | hard | 13/14 | 1 | 4 | 0.3750 |
| nonce_labels | easy | 19/20 | 1 | 0 | 1.0000 |
| nonce_labels | medium | 15/19 | 4 | 1 | 0.3750 |
| nonce_labels | hard | 9/14 | 5 | 4 | 1.0000 |
| uppercase_latin | easy | 19/20 | 1 | 0 | 1.0000 |
| uppercase_latin | medium | 17/19 | 2 | 1 | 1.0000 |
| uppercase_latin | hard | 13/14 | 1 | 5 | 0.2188 |

## Historical diagnostics and all available outputs

These are inventory counts, not a combined accuracy estimate. A missing marker or incomplete request digest prevents a completion claim.

| Evidence step | Saved / expected | Correct | Truncated | Operational | Complete |
| --- | --- | --- | --- | --- | --- |
| configuration-calibration-v1-glm-bounded-final/glm-flash-local/calibration | 15/15 | 0 | 14 | 0 | True |
| configuration-calibration-v1-kimi-bounded-final/kimi-linear-local/calibration | 15/15 | 0 | 11 | 0 | True |
| configuration-calibration-v1-nemotron-answer-only/nemotron-local/calibration | 11/15 | 0 | 11 | 0 | False |
| configuration-calibration-v1-nemotron-answer-only-sampled/nemotron-local/calibration | 15/15 | 0 | 2 | 0 | True |
| configuration-calibration-v1-nemotron-bounded/nemotron-local/calibration | 10/15 | 0 | 8 | 0 | False |
| configuration-calibration-v1-nemotron-constrained-greedy/nemotron-local/calibration | 15/15 | 0 | 0 | 0 | True |
| configuration-calibration-v1-nemotron-verified-constrained/nemotron-local/calibration | 15/15 | 0 | 0 | 0 | True |
| configuration-calibration-v1-qwen-bounded-final/qwen-local/calibration | 15/15 | 4 | 2 | 0 | True |
| configuration-calibration-v1-qwen-official-thinking/qwen-local/calibration | 15/15 | 4 | 11 | 0 | True |
| configuration-calibration-v2-mistral-verified-constrained/mistral-small-4-local/calibration | 15/15 | 0 | 0 | 0 | True |
| configuration-diagnostic-v1-very-easy-mistral-small-4-local/mistral-small-4-local/diagnostic | 1/1 | 0 | 0 | 0 | True |
| configuration-diagnostic-v1-very-easy-nemotron-local/nemotron-local/diagnostic | 1/1 | 0 | 0 | 0 | True |
| configuration-diagnostic-v2-very-easy-mistral-small-4-local/mistral-small-4-local/diagnostic | 1/1 | 0 | 0 | 0 | True |
| configuration-diagnostic-v3-very-easy-mistral-small-4-local/mistral-small-4-local/diagnostic | 1/1 | 0 | 0 | 0 | True |
| gpt-oss-120b-local-natural-timing-v1-easy/gpt-oss-120b-local/timing-diagnostic | 1/1 | 1 | 0 | 0 | True |
| gpt-oss-120b-local-natural-timing-v1-hard/gpt-oss-120b-local/timing-diagnostic | 1/1 | 1 | 0 | 0 | True |
| gpt-oss-120b-local-natural-timing-v1-medium/gpt-oss-120b-local/timing-diagnostic | 1/1 | 1 | 0 | 0 | True |
| local-models-v1/gpt-oss-120b-local/exp10 | 108/108 | 82 | 3 | 0 | True |
| local-models-v1/gpt-oss-120b-local/exp2 | 60/60 | 47 | 2 | 0 | True |
| local-models-v1/gpt-oss-120b-local/exp4 | 540/540 | 372 | 24 | 0 | True |
| local-models-v1/gpt-oss-120b-local/exp6 | 135/135 | 120 | 2 | 0 | True |
| local-models-v1/gpt-oss-120b-local/exp7 | 45/45 | 32 | 5 | 0 | True |
| local-models-v1/gpt-oss-120b-local/exp8 | 165/165 | 124 | 7 | 0 | True |
| local-models-v1/gpt-oss-120b-local/exp9 | 171/171 | 103 | 12 | 0 | True |
| local-models-v1/gpt-oss-120b-local/qualification | 5/5 | 5 | 0 | 0 | True |
| qwen-3.5-122b-local-natural-timing-v2-easy/qwen-3.5-122b-local/timing-diagnostic | 1/1 | 1 | 0 | 0 | True |
| qwen-3.5-122b-local-natural-timing-v2-medium/qwen-3.5-122b-local/timing-diagnostic | 1/1 | 0 | 1 | 0 | True |
| qwen-3.8-27b-local-natural-timing-v2-easy/qwen-3.8-27b-local/timing-diagnostic | 1/1 | 1 | 0 | 0 | True |
| qwen-3.8-27b-local-natural-timing-v2-hard/qwen-3.8-27b-local/timing-diagnostic | 1/1 | 0 | 1 | 0 | True |
| qwen-3.8-27b-local-natural-timing-v2-medium/qwen-3.8-27b-local/timing-diagnostic | 1/1 | 0 | 1 | 0 | True |
| qwen-3.8-27b-v2/qwen-3.8-27b-local/exp2 | 60/60 | 54 | 2 | 0 | True |
| qwen-3.8-27b-v2/qwen-3.8-27b-local/exp4 | 540/540 | 472 | 24 | 0 | True |
| qwen-3.8-27b-v2/qwen-3.8-27b-local/qualification | 5/5 | 5 | 0 | 0 | True |
| qwen-3.8-27b-v2-natural-timing-v3-medium/qwen-3.8-27b-local/timing-diagnostic | 1/1 | 1 | 0 | 0 | True |
| qwen-natural-timing-v1-easy/qwen-local/timing-diagnostic | 1/1 | 1 | 0 | 0 | True |
| qwen-natural-timing-v1-hard/qwen-local/timing-diagnostic | 1/1 | 0 | 1 | 0 | True |
| qwen-natural-timing-v1-medium/qwen-local/timing-diagnostic | 1/1 | 0 | 1 | 0 | True |
| qwen-natural-timing-v2-hard/qwen-local/timing-diagnostic | 1/1 | 1 | 0 | 0 | True |
| qwen-natural-timing-v2-medium/qwen-local/timing-diagnostic | 1/1 | 0 | 0 | 0 | True |
| thesis-confirmatory-lean-v1/qwen-local/qualification | 5/5 | 0 | 5 | 0 | True |
| thesis-confirmatory-lean-v2/qwen-local/qualification | 5/5 | 1 | 4 | 0 | True |
| thesis-confirmatory-lean-v3/qwen-local/qualification | 5/5 | 2 | 3 | 0 | True |
| thesis-confirmatory-lean-v4/qwen-local/qualification | 2/5 | 1 | 1 | 0 | False |
| thesis-confirmatory-lean-v5/glm-flash-local/qualification | 1/5 | 0 | 1 | 0 | False |
| thesis-confirmatory-lean-v5/qwen-local/qualification | 5/5 | 4 | 0 | 0 | True |
| thesis-confirmatory-lean-v6/glm-flash-local/qualification | 5/5 | 0 | 0 | 0 | True |
| thesis-confirmatory-lean-v6/kimi-linear-local/qualification | 5/5 | 0 | 4 | 0 | True |

## Cross-model paired outcomes

```json
{
  "paired_requests": 540,
  "both_correct": 338,
  "gpt_only": 34,
  "qwen_only": 134,
  "neither_correct": 34,
  "qwen_minus_gpt_pp": 18.51851851851852,
  "stratified_puzzle_bootstrap_95_pp": [
    13.703703703703704,
    23.518518518518515
  ],
  "bootstrap_seed": 20260930,
  "bootstrap_replicates": 10000
}
```

### Paired model outcomes by difficulty

| Difficulty | Paired | Both correct | GPT-OSS only | Qwen only | Neither correct |
| --- | --- | --- | --- | --- | --- |
| easy | 180 | 165 | 6 | 9 | 0 |
| medium | 180 | 108 | 13 | 52 | 7 |
| hard | 180 | 65 | 15 | 73 | 27 |

### Paired model outcomes by alphabet

| Alphabet | Paired | Both correct | GPT-OSS only | Qwen only | Neither correct |
| --- | --- | --- | --- | --- | --- |
| abstract_symbols | 60 | 35 | 3 | 16 | 6 |
| arabic_digits | 60 | 40 | 5 | 13 | 2 |
| bengali_numerals | 60 | 39 | 4 | 14 | 3 |
| devanagari_numerals | 60 | 39 | 0 | 17 | 4 |
| emoji | 60 | 35 | 3 | 19 | 3 |
| greek_letters | 60 | 34 | 3 | 17 | 6 |
| lowercase_latin | 60 | 38 | 6 | 13 | 3 |
| nonce_labels | 60 | 37 | 6 | 11 | 6 |
| uppercase_latin | 60 | 41 | 4 | 14 | 1 |

## Local integrity audit

```json
{
  "dataset": {
    "valid": true,
    "record_count": 300,
    "difficulty_counts": {
      "easy": 100,
      "medium": 100,
      "hard": 100
    },
    "errors": [],
    "clues": {
      "easy": {
        "n": 100,
        "min": 40,
        "max": 46,
        "median": 43.0
      },
      "medium": {
        "n": 100,
        "min": 24,
        "max": 28,
        "median": 26.0
      },
      "hard": {
        "n": 100,
        "min": 23,
        "max": 27,
        "median": 25.0
      }
    },
    "technique_puzzle_counts": {
      "easy": {
        "naked_single": 100
      },
      "medium": {
        "naked_single": 100,
        "hidden_single": 100,
        "naked_pair": 83,
        "hidden_pair": 37,
        "pointing_pair": 32,
        "box_line": 3
      },
      "hard": {
        "hidden_single": 100,
        "naked_pair": 71,
        "pointing_pair": 74,
        "naked_single": 91,
        "hidden_pair": 32,
        "box_line": 25
      }
    }
  },
  "audit_errors": []
}
```


# Detailed evidence and representative outputs

This appendix expands the numerical tables with settings, sample checks, failure incidences, and final-only output examples.

## Frozen samples

Main IDs identical across selected models: True.

### GPT-OSS

Dataset SHA-256: `43a1ef3a4dfe22fa6cd8939021a80ef3cc812c5916ab62ef6b11501b45b58cc2`.

Pilot (15 puzzles): E002, E036, E064, E061, E062, M013, M019, M072, M096, M099, H043, H027, H093, H085, H009.

Main (60 puzzles): E084, E046, E012, E003, E032, E087, E016, E035, E027, E079, E030, E007, E021, E033, E082, E014, E049, E066, E037, E051, M018, M035, M059, M034, M048, M078, M052, M021, M063, M003, M037, M064, M061, M087, M085, M053, M032, M033, M047, M044, H092, H050, H060, H018, H023, H032, H017, H074, H005, H030, H026, H028, H051, H029, H049, H034, H020, H048, H008, H079.

Mechanism (15 puzzles): E030, E087, E021, E007, E012, M087, M064, M053, M078, M085, H079, H028, H018, H060, H050.

Ablation (9 puzzles): E012, E087, E021, M087, M085, M078, H028, H050, H060.

Qualification IDs: E073, E039, E081, E034, E056. Observed qualification/main overlap: []. Observed qualification/pilot overlap: [].

### Qwen

Dataset SHA-256: `43a1ef3a4dfe22fa6cd8939021a80ef3cc812c5916ab62ef6b11501b45b58cc2`.

Pilot (15 puzzles): E002, E036, E064, E061, E062, M013, M019, M072, M096, M099, H043, H027, H093, H085, H009.

Main (60 puzzles): E084, E046, E012, E003, E032, E087, E016, E035, E027, E079, E030, E007, E021, E033, E082, E014, E049, E066, E037, E051, M018, M035, M059, M034, M048, M078, M052, M021, M063, M003, M037, M064, M061, M087, M085, M053, M032, M033, M047, M044, H092, H050, H060, H018, H023, H032, H017, H074, H005, H030, H026, H028, H051, H029, H049, H034, H020, H048, H008, H079.

Mechanism (15 puzzles): E030, E087, E021, E007, E012, M087, M064, M053, M078, M085, H079, H028, H018, H060, H050.

Ablation (9 puzzles): E012, E087, E021, M087, M085, M078, H028, H050, H060.

Qualification IDs: E073, E039, E081, E034, E056. Observed qualification/main overlap: []. Observed qualification/pilot overlap: [].

## GPT-OSS main failure-label incidences

Each count is requests containing the label. Counts overlap and must not be summed.

| Label | Requests |
| --- | --- |
| BOX_CONSTRAINT_ERROR | 87 |
| COLUMN_CONSTRAINT_ERROR | 29 |
| CORRECT | 372 |
| FORMAT_ERROR | 25 |
| GIVEN_MODIFIED | 14 |
| INVALID_SYMBOL | 42 |
| LOCAL_MAPPING_ERROR | 96 |
| NO_FINAL_ANSWER | 24 |
| REFUSAL | 4 |
| ROW_CONSTRAINT_ERROR | 17 |
| TRUNCATED_OUTPUT | 24 |
| WRONG_CELL_COUNT | 25 |
| WRONG_ROW_COUNT | 22 |

### Parsing, clues, and Sudoku validity by alphabet

| Alphabet | Saved | Parsed | Clues preserved / parsed | Valid units / parsed | Changed clue cells |
| --- | --- | --- | --- | --- | --- |
| abstract_symbols | 60 | 44 | 41/44 | 40/44 | 27 |
| arabic_digits | 60 | 59 | 57/59 | 46/59 | 2 |
| bengali_numerals | 60 | 51 | 49/51 | 43/51 | 3 |
| devanagari_numerals | 60 | 52 | 51/52 | 39/52 | 1 |
| emoji | 60 | 47 | 45/47 | 38/47 | 17 |
| greek_letters | 60 | 52 | 52/52 | 37/52 | 0 |
| lowercase_latin | 60 | 55 | 54/55 | 44/55 | 3 |
| nonce_labels | 60 | 51 | 50/51 | 44/51 | 1 |
| uppercase_latin | 60 | 57 | 55/57 | 46/57 | 13 |

### Representative final-only outputs

Examples are deterministic first matches in sorted shard order. They illustrate categories, not prevalence. No reasoning trace is reproduced.

#### Correct: E007 / arabic_digits

Request ID: `exp4:gpt-oss-120b-local:E007:31bf2b61ba4101a6c1fb`. Finish: `stop`. Latency: 31.38 seconds. Generation tokens: 6426. Labels: CORRECT.

```text
8 2 9 1 3 4 7 5 6
3 6 4 7 9 5 1 2 8
5 7 1 2 8 6 9 3 4
7 1 8 4 2 9 3 6 5
2 9 3 6 5 1 4 8 7
4 5 6 3 7 8 2 1 9
6 4 2 8 1 7 5 9 3
9 3 7 5 6 2 8 4 1
1 8 5 9 4 3 6 7 2
```

Independent grid audit: `{"parseable": true, "clues_preserved": true, "changed_clues": 0, "changed_cells": [], "rows_valid": true, "columns_valid": true, "boxes_valid": true, "sudoku_valid": true, "solution_equal": true}`.

#### Incorrect Grid: H049 / arabic_digits

Request ID: `exp4:gpt-oss-120b-local:H049:33418cc546709ae21aaf`. Finish: `stop`. Latency: 616.98 seconds. Generation tokens: 110179. Labels: BOX_CONSTRAINT_ERROR, LOCAL_MAPPING_ERROR.

```text
2 8 5 1 7 9 6 3 4
9 3 7 8 6 2 1 4 5
6 1 8 5 4 3 9 2 7
4 7 1 9 2 8 3 5 6
3 9 2 6 5 4 7 1 8
8 5 6 7 3 1 4 9 2
7 6 3 4 9 5 2 8 1
1 4 9 2 8 7 5 6 3
5 2 4 3 1 6 8 7 9
```

Independent grid audit: `{"parseable": true, "clues_preserved": true, "changed_clues": 0, "changed_cells": [], "rows_valid": true, "columns_valid": true, "boxes_valid": false, "sudoku_valid": false, "solution_equal": false}`.

#### Truncated: H028 / arabic_digits

Request ID: `exp4:gpt-oss-120b-local:H028:4a81df38a8451442cd7e`. Finish: `length`. Latency: 714.92 seconds. Generation tokens: 130791. Labels: NO_FINAL_ANSWER, TRUNCATED_OUTPUT.

```text
[No extracted final answer]
```

Independent grid audit: `{"parseable": false}`.

#### Other Output Error: E007 / abstract_symbols

Request ID: `exp4:gpt-oss-120b-local:E007:3ec231d832b1f703487a`. Finish: `stop`. Latency: 48.72 seconds. Generation tokens: 9934. Labels: FORMAT_ERROR, INVALID_SYMBOL, WRONG_CELL_COUNT.

```text
§ □ ¶ △ ○ ☆ ‡ × †
○ † ☆ ‡ ¶ × △ □ §
× ‡ △ □ § † ¶ ○ ☆
‡ △ § ☆ □ ¶ ○ † ×
□ ¶ ☆ † × △ ○ § ‡
☆ × † ○ ‡ § □ △ ¶
† ☆ □ § △ ‡ × ¶ ○
¶ ○ ‡ × † □ § ☆ △
△ § × ¶ ☆ ○ †   ‡ □
```

Independent grid audit: `{"parseable": false}`.

## Qwen main failure-label incidences

Each count is requests containing the label. Counts overlap and must not be summed.

| Label | Requests |
| --- | --- |
| BOX_CONSTRAINT_ERROR | 13 |
| COLUMN_CONSTRAINT_ERROR | 9 |
| CORRECT | 472 |
| FORMAT_ERROR | 11 |
| GIVEN_MODIFIED | 17 |
| INVALID_SYMBOL | 7 |
| LOCAL_MAPPING_ERROR | 33 |
| NO_FINAL_ANSWER | 24 |
| ROW_CONSTRAINT_ERROR | 1 |
| TRUNCATED_OUTPUT | 24 |
| WRONG_CELL_COUNT | 11 |
| WRONG_ROW_COUNT | 9 |

### Parsing, clues, and Sudoku validity by alphabet

| Alphabet | Saved | Parsed | Clues preserved / parsed | Valid units / parsed | Changed clue cells |
| --- | --- | --- | --- | --- | --- |
| abstract_symbols | 60 | 55 | 52/55 | 53/55 | 4 |
| arabic_digits | 60 | 56 | 55/56 | 54/56 | 1 |
| bengali_numerals | 60 | 55 | 54/55 | 54/55 | 2 |
| devanagari_numerals | 60 | 57 | 57/57 | 56/57 | 0 |
| emoji | 60 | 56 | 54/56 | 56/56 | 3 |
| greek_letters | 60 | 59 | 54/59 | 56/59 | 6 |
| lowercase_latin | 60 | 57 | 55/57 | 53/57 | 2 |
| nonce_labels | 60 | 52 | 50/52 | 49/52 | 28 |
| uppercase_latin | 60 | 58 | 57/58 | 56/58 | 1 |

### Representative final-only outputs

Examples are deterministic first matches in sorted shard order. They illustrate categories, not prevalence. No reasoning trace is reproduced.

#### Correct: E014 / arabic_digits

Request ID: `exp4:qwen-3.8-27b-local:E014:b9ff585a04774ca273d8`. Finish: `stop`. Latency: 81.27 seconds. Generation tokens: 6647. Labels: CORRECT.

```text
7 9 4 1 2 3 5 8 6
1 8 3 4 5 6 2 7 9
5 2 6 9 7 8 1 4 3
6 7 2 5 8 4 3 9 1
4 1 5 2 3 9 8 6 7
9 3 8 7 6 1 4 2 5
8 4 9 6 1 5 7 3 2
2 6 1 3 4 7 9 5 8
3 5 7 8 9 2 6 1 4
```

Independent grid audit: `{"parseable": true, "clues_preserved": true, "changed_clues": 0, "changed_cells": [], "rows_valid": true, "columns_valid": true, "boxes_valid": true, "sudoku_valid": true, "solution_equal": true}`.

#### Incorrect Grid: M047 / arabic_digits

Request ID: `exp4:qwen-3.8-27b-local:M047:cd2605260c0150dd4b9c`. Finish: `stop`. Latency: 770.11 seconds. Generation tokens: 59558. Labels: BOX_CONSTRAINT_ERROR, COLUMN_CONSTRAINT_ERROR, LOCAL_MAPPING_ERROR, ROW_CONSTRAINT_ERROR.

```text
7 6 5 8 2 1 4 9 3
1 3 6 9 4 5 8 7 2
2 4 9 3 7 6 5 8 1
9 7 8 5 1 4 2 3 6
6 1 3 2 8 7 9 5 4
5 2 4 6 3 9 1 8 7
4 5 7 1 6 8 3 2 9
3 8 1 7 9 2 6 4 5
8 9 2 4 5 3 7 6 8
```

Independent grid audit: `{"parseable": true, "clues_preserved": true, "changed_clues": 0, "changed_cells": [], "rows_valid": false, "columns_valid": false, "boxes_valid": false, "sudoku_valid": false, "solution_equal": false}`.

#### Truncated: H050 / arabic_digits

Request ID: `exp4:qwen-3.8-27b-local:H050:b5a20f94de2a2820aab7`. Finish: `length`. Latency: 1773.65 seconds. Generation tokens: 130787. Labels: NO_FINAL_ANSWER, TRUNCATED_OUTPUT.

```text
[No extracted final answer]
```

Independent grid audit: `{"parseable": false}`.

#### Other Output Error: H008 / abstract_symbols

Request ID: `exp4:qwen-3.8-27b-local:H008:1829dd5e1f5686c24d03`. Finish: `stop`. Latency: 1271.13 seconds. Generation tokens: 95005. Labels: FORMAT_ERROR, WRONG_CELL_COUNT, WRONG_ROW_COUNT.

```text
△ □ ○ ☆ × † ‡ § ¶

□ ☆ † § ‡ △ ¶ ○ ×
○ × △ □ ☆ ¶ § † ‡
¶ § ‡ × ○ † ☆ □ △
× † ○ △ § □ ‡ ☆ ¶
‡ △ ☆ ¶ × ○ □ § †
§ ¶ □ ‡ † ☆ × △ ○
☆ □ ¶ ○ △ ‡ † × §
△ ‡ § † □ × ○ ¶ ☆
† ○ × ☆ ¶ § △ ‡ □
```

Independent grid audit: `{"parseable": false}`.

## Historical diagnostics: exact settings and tier counts

Historical configurations changed. Their names are identifiers, not proof of equivalently controlled conditions.

### Historical run 1: glm-flash-local

Evidence path: `configuration-calibration-v1-glm-bounded-final/glm-flash-local/calibration`.

Checkpoint: `zai-org/GLM-4.7-Flash`. Revision: `7dd20894a642a0aa287e9827cb1a1f7f91386b67`. Saved/expected: 15/15. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 16384, "seed": 20260826, "temperature": 1.0, "top_p": 0.95}`.

Model controls: `{"bounded_final": {"final_tokens": 1024, "mode": "close_think", "reasoning_tokens": 15360}, "chat_template": {"enable_thinking": true}, "reasoning_output": "think_tags", "sampling": {}, "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 32768}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 0/5 | 1 | 4 | 0 | 0 | 89.32 |
| hard | 0/10 | 0 | 10 | 0 | 0 | 89.69 |

Parseable Sudoku grids 1/15. Clues preserved 0/1 parseable grids.

### Historical run 2: kimi-linear-local

Evidence path: `configuration-calibration-v1-kimi-bounded-final/kimi-linear-local/calibration`.

Checkpoint: `moonshotai/Kimi-Linear-48B-A3B-Instruct`. Revision: `e1df551a447157d4658b573f9a695d57658590e9`. Saved/expected: 15/15. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 8192, "repetition_penalty": 1.05, "seed": 20260826, "temperature": 0.7, "top_k": 20, "top_p": 0.9}`.

Model controls: `{"bounded_final": {"final_tokens": 1024, "mode": "followup", "reasoning_tokens": 7168}, "sampling": {"repetition_penalty": 1.05, "top_k": 20}, "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 32768}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 0/5 | 4 | 1 | 0 | 0 | 28.58 |
| hard | 0/10 | 0 | 10 | 0 | 0 | 30.23 |

Parseable Sudoku grids 4/15. Clues preserved 1/4 parseable grids.

### Historical run 3: nemotron-local

Evidence path: `configuration-calibration-v1-nemotron-answer-only/nemotron-local/calibration`.

Checkpoint: `nvidia/Llama-3_3-Nemotron-Super-49B-v1_5-FP8`. Revision: `04822723e77e036ddf2d24e83c6d469d3b009252`. Saved/expected: 11/15. Marker and digest completion: False.

Effective recorded inference and overrides: `{"max_new_tokens": 256, "seed": 20260826, "temperature": 0.0, "top_p": 1.0}`.

Model controls: `{"bounded_final": null, "reasoning_output": null, "system_prompt": "/no_think", "vllm": {"enforce_eager": true, "gpu_memory_utilization": 0.9, "max_model_len": 32768, "quantization": "modelopt"}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 0/5 | 0 | 5 | 0 | 0 | 7.74 |
| medium | 0/5 | 0 | 5 | 0 | 0 | 7.70 |
| hard | 0/1 | 0 | 1 | 0 | 0 | 7.73 |

Parseable Sudoku grids 0/11. Clues preserved 0/0 parseable grids.

### Historical run 4: nemotron-local

Evidence path: `configuration-calibration-v1-nemotron-answer-only-sampled/nemotron-local/calibration`.

Checkpoint: `nvidia/Llama-3_3-Nemotron-Super-49B-v1_5-FP8`. Revision: `04822723e77e036ddf2d24e83c6d469d3b009252`. Saved/expected: 15/15. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 1024, "seed": 20260826, "temperature": 0.6, "top_p": 0.95}`.

Model controls: `{"bounded_final": null, "reasoning_output": null, "system_prompt": "/no_think", "vllm": {"enforce_eager": true, "gpu_memory_utilization": 0.9, "max_model_len": 32768, "quantization": "modelopt"}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 0/5 | 0 | 0 | 5 | 0 | 18.68 |
| medium | 0/5 | 1 | 2 | 2 | 0 | 16.43 |
| hard | 0/5 | 0 | 0 | 5 | 0 | 15.86 |

Parseable Sudoku grids 1/15. Clues preserved 0/1 parseable grids.

### Historical run 5: nemotron-local

Evidence path: `configuration-calibration-v1-nemotron-bounded/nemotron-local/calibration`.

Checkpoint: `nvidia/Llama-3_3-Nemotron-Super-49B-v1_5-FP8`. Revision: `04822723e77e036ddf2d24e83c6d469d3b009252`. Saved/expected: 10/15. Marker and digest completion: False.

Effective recorded inference and overrides: `{"max_new_tokens": 16384, "seed": 20260826, "temperature": 0.6, "top_p": 0.95}`.

Model controls: `{"bounded_final": {"final_tokens": 1024, "mode": "close_think", "reasoning_tokens": 15360}, "reasoning_output": "think_tags", "vllm": {"enforce_eager": true, "gpu_memory_utilization": 0.9, "max_model_len": 32768, "quantization": "modelopt"}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 0/5 | 0 | 4 | 1 | 0 | 497.24 |
| medium | 0/5 | 0 | 4 | 1 | 0 | 500.26 |

Parseable Sudoku grids 0/10. Clues preserved 0/0 parseable grids.

### Historical run 6: nemotron-local

Evidence path: `configuration-calibration-v1-nemotron-constrained-greedy/nemotron-local/calibration`.

Checkpoint: `nvidia/Llama-3_3-Nemotron-Super-49B-v1_5-FP8`. Revision: `04822723e77e036ddf2d24e83c6d469d3b009252`. Saved/expected: 15/15. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 256, "seed": 20260826, "temperature": 0.0, "top_p": 1.0}`.

Model controls: `{"bounded_final": null, "reasoning_output": null, "structured_regex": "[1-9]( [1-9]){8}(\\n[1-9]( [1-9]){8}){8}", "system_prompt": "/no_think", "vllm": {"enforce_eager": true, "gpu_memory_utilization": 0.9, "max_model_len": 32768, "quantization": "modelopt"}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 0/5 | 5 | 0 | 0 | 0 | 5.10 |
| medium | 0/5 | 5 | 0 | 0 | 0 | 4.94 |
| hard | 0/5 | 5 | 0 | 0 | 0 | 4.93 |

Parseable Sudoku grids 15/15. Clues preserved 0/15 parseable grids.

### Historical run 7: nemotron-local

Evidence path: `configuration-calibration-v1-nemotron-verified-constrained/nemotron-local/calibration`.

Checkpoint: `nvidia/Llama-3_3-Nemotron-Super-49B-v1_5-FP8`. Revision: `04822723e77e036ddf2d24e83c6d469d3b009252`. Saved/expected: 15/15. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 256, "seed": 20260826, "temperature": 0.0, "top_p": 1.0}`.

Model controls: `{"bounded_final": null, "reasoning_output": null, "structured_regex": "[1-9]( [1-9]){8}(\\n[1-9]( [1-9]){8}){8}", "system_prompt": "/no_think", "vllm": {"enforce_eager": true, "gpu_memory_utilization": 0.9, "max_model_len": 32768, "quantization": "modelopt"}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 0/5 | 5 | 0 | 0 | 0 | 5.23 |
| medium | 0/5 | 5 | 0 | 0 | 0 | 4.96 |
| hard | 0/5 | 5 | 0 | 0 | 0 | 4.96 |

Parseable Sudoku grids 15/15. Clues preserved 1/15 parseable grids.

### Historical run 8: qwen-local

Evidence path: `configuration-calibration-v1-qwen-bounded-final/qwen-local/calibration`.

Checkpoint: `Qwen/Qwen3.8-27B`. Revision: `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`. Saved/expected: 15/15. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 16384, "min_p": 0.0, "presence_penalty": 0.0, "repetition_penalty": 1.0, "seed": 20260826, "temperature": 1.0, "top_k": 20, "top_p": 0.95}`.

Model controls: `{"bounded_final": {"final_tokens": 1024, "mode": "close_think", "reasoning_tokens": 15360}, "chat_template": {"enable_thinking": true, "preserve_thinking": false, "reasoning_effort": "medium"}, "reasoning_output": "think_tags", "sampling": {"min_p": 0.0, "presence_penalty": 0.0, "repetition_penalty": 1.0, "top_k": 20}, "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 32768}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 4/5 | 0 | 0 | 1 | 0 | 177.23 |
| hard | 0/10 | 2 | 2 | 6 | 0 | 325.33 |

Parseable Sudoku grids 6/15. Clues preserved 6/6 parseable grids.

### Historical run 9: qwen-local

Evidence path: `configuration-calibration-v1-qwen-official-thinking/qwen-local/calibration`.

Checkpoint: `Qwen/Qwen3.8-27B`. Revision: `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`. Saved/expected: 15/15. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 16384, "min_p": 0.0, "presence_penalty": 0.0, "repetition_penalty": 1.0, "seed": 20260826, "temperature": 1.0, "top_k": 20, "top_p": 0.95}`.

Model controls: `{"chat_template": {"enable_thinking": true, "preserve_thinking": false, "reasoning_effort": "medium"}, "reasoning_output": "think_tags", "sampling": {"min_p": 0.0, "presence_penalty": 0.0, "repetition_penalty": 1.0, "top_k": 20}, "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 32768}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 4/5 | 0 | 1 | 0 | 0 | 180.55 |
| hard | 0/10 | 0 | 10 | 0 | 0 | 334.10 |

Parseable Sudoku grids 4/15. Clues preserved 4/4 parseable grids.

### Historical run 10: mistral-small-4-local

Evidence path: `configuration-calibration-v2-mistral-verified-constrained/mistral-small-4-local/calibration`.

Checkpoint: `mistralai/Mistral-Small-4-119B-2603`. Revision: `a11f36bebf709121056b1dbcc943d1c6afbe494d`. Saved/expected: 15/15. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 256, "seed": 20260826, "temperature": 0.1, "top_p": 1.0}`.

Model controls: `{"bounded_final": null, "chat_template": {"reasoning_effort": "none"}, "reasoning_output": null, "structured_regex": "[1-9]( [1-9]){8}(\\n[1-9]( [1-9]){8}){8}", "vllm": {"attention_backend": "FLASH_ATTN_MLA", "gpu_memory_utilization": 0.8, "max_model_len": 32768, "moe_backend": "triton"}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 0/5 | 5 | 0 | 0 | 0 | 1.36 |
| medium | 0/5 | 5 | 0 | 0 | 0 | 0.91 |
| hard | 0/5 | 5 | 0 | 0 | 0 | 0.76 |

Parseable Sudoku grids 15/15. Clues preserved 5/15 parseable grids.

### Historical run 11: mistral-small-4-local

Evidence path: `configuration-diagnostic-v1-very-easy-mistral-small-4-local/mistral-small-4-local/diagnostic`.

Checkpoint: `mistralai/Mistral-Small-4-119B-2603`. Revision: `a11f36bebf709121056b1dbcc943d1c6afbe494d`. Saved/expected: 1/1. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 256, "seed": 20260826, "temperature": 0.1, "top_p": 1.0}`.

Model controls: `{"bounded_final": null, "chat_template": {"reasoning_effort": "none"}, "reasoning_output": null, "structured_regex": "[1-9]( [1-9]){8}(\\n[1-9]( [1-9]){8}){8}", "vllm": {"attention_backend": "FLASH_ATTN_MLA", "gpu_memory_utilization": 0.8, "max_model_len": 32768, "moe_backend": "triton"}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |

Parseable Sudoku grids 1/1. Clues preserved 0/1 parseable grids.

### Historical run 12: nemotron-local

Evidence path: `configuration-diagnostic-v1-very-easy-nemotron-local/nemotron-local/diagnostic`.

Checkpoint: `nvidia/Llama-3_3-Nemotron-Super-49B-v1_5-FP8`. Revision: `04822723e77e036ddf2d24e83c6d469d3b009252`. Saved/expected: 1/1. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 256, "seed": 20260826, "temperature": 0.0, "top_p": 1.0}`.

Model controls: `{"bounded_final": null, "reasoning_output": null, "structured_regex": "[1-9]( [1-9]){8}(\\n[1-9]( [1-9]){8}){8}", "system_prompt": "/no_think", "vllm": {"enforce_eager": true, "gpu_memory_utilization": 0.9, "max_model_len": 32768, "quantization": "modelopt"}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |

Parseable Sudoku grids 1/1. Clues preserved 0/1 parseable grids.

### Historical run 13: mistral-small-4-local

Evidence path: `configuration-diagnostic-v2-very-easy-mistral-small-4-local/mistral-small-4-local/diagnostic`.

Checkpoint: `mistralai/Mistral-Small-4-119B-2603`. Revision: `a11f36bebf709121056b1dbcc943d1c6afbe494d`. Saved/expected: 1/1. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 8448, "seed": 20260826, "temperature": 0.6, "top_p": 0.95}`.

Model controls: `{"bounded_final": {"final_tokens": 256, "mode": "followup", "reasoning_tokens": 8192}, "chat_template": {"reasoning_effort": "high"}, "final_structured_regex": "8 [1-9] 3 [1-9] [1-9] 1 4 2 [1-9]\\n[1-9] [1-9] 5 9 3 2 [1-9] 8 6\\n2 6 1 8 4 7 3 9 5\\n7 5 2 6 9 4 8 [1-9] [1-9]\\n[1-9] 4 8 1 [1-9] 3 6 [1-9] 2\\n1 3 6 2 5 8 [1-9] 4 9\\n[1-9] [1-9] 4 [1-9] 8 5 9 [1-9] 3\\n3 1 7 4 [1-9] [1-9] [1-9] 6 8\\n[1-9] 8 [1-9] 3 1 6 [1-9] 7 [1-9]", "reasoning_output": "mistral_think_tags", "structured_regex": null, "vllm": {"attention_backend": "FLASH_ATTN_MLA", "gpu_memory_utilization": 0.8, "max_model_len": 32768, "moe_backend": "triton"}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |

Parseable Sudoku grids 1/1. Clues preserved 1/1 parseable grids.

### Historical run 14: mistral-small-4-local

Evidence path: `configuration-diagnostic-v3-very-easy-mistral-small-4-local/mistral-small-4-local/diagnostic`.

Checkpoint: `mistralai/Mistral-Small-4-119B-2603`. Revision: `a11f36bebf709121056b1dbcc943d1c6afbe494d`. Saved/expected: 1/1. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 8448, "seed": 20260826, "temperature": 0.6, "top_p": 0.95}`.

Model controls: `{"bounded_final": {"final_tokens": 256, "mode": "followup", "reasoning_tokens": 8192}, "chat_template": {"reasoning_effort": "high"}, "chat_template_file": "chat_template.jinja", "final_structured_regex": "8 [1-9] 3 [1-9] [1-9] 1 4 2 [1-9]\\n[1-9] [1-9] 5 9 3 2 [1-9] 8 6\\n2 6 1 8 4 7 3 9 5\\n7 5 2 6 9 4 8 [1-9] [1-9]\\n[1-9] 4 8 1 [1-9] 3 6 [1-9] 2\\n1 3 6 2 5 8 [1-9] 4 9\\n[1-9] [1-9] 4 [1-9] 8 5 9 [1-9] 3\\n3 1 7 4 [1-9] [1-9] [1-9] 6 8\\n[1-9] 8 [1-9] 3 1 6 [1-9] 7 [1-9]", "reasoning_output": "mistral_think_tags", "structured_regex": null, "vllm": {"attention_backend": "FLASH_ATTN_MLA", "gpu_memory_utilization": 0.8, "max_model_len": 32768, "moe_backend": "triton"}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |

Parseable Sudoku grids 1/1. Clues preserved 1/1 parseable grids.

### Historical run 15: gpt-oss-120b-local

Evidence path: `gpt-oss-120b-local-natural-timing-v1-easy/gpt-oss-120b-local/timing-diagnostic`.

Checkpoint: `openai/gpt-oss-120b`. Revision: `b5c939de8f754692c1647ca79fbf85e8c1e70f8a`. Saved/expected: 1/1. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 131072, "seed": 20260826, "skip_special_tokens": false, "temperature": 1, "top_p": 1}`.

Model controls: `{"chat_template": {"reasoning_effort": "high"}, "reasoning_output": "harmony_channels", "sampling": {"skip_special_tokens": false, "temperature": 1, "top_p": 1}, "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 131072}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 1/1 | 0 | 0 | 0 | 0 | 36.12 |

Parseable Sudoku grids 1/1. Clues preserved 1/1 parseable grids.

### Historical run 16: gpt-oss-120b-local

Evidence path: `gpt-oss-120b-local-natural-timing-v1-hard/gpt-oss-120b-local/timing-diagnostic`.

Checkpoint: `openai/gpt-oss-120b`. Revision: `b5c939de8f754692c1647ca79fbf85e8c1e70f8a`. Saved/expected: 1/1. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 131072, "seed": 20260826, "skip_special_tokens": false, "temperature": 1, "top_p": 1}`.

Model controls: `{"chat_template": {"reasoning_effort": "high"}, "reasoning_output": "harmony_channels", "sampling": {"skip_special_tokens": false, "temperature": 1, "top_p": 1}, "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 131072}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| hard | 1/1 | 0 | 0 | 0 | 0 | 227.35 |

Parseable Sudoku grids 1/1. Clues preserved 1/1 parseable grids.

### Historical run 17: gpt-oss-120b-local

Evidence path: `gpt-oss-120b-local-natural-timing-v1-medium/gpt-oss-120b-local/timing-diagnostic`.

Checkpoint: `openai/gpt-oss-120b`. Revision: `b5c939de8f754692c1647ca79fbf85e8c1e70f8a`. Saved/expected: 1/1. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 131072, "seed": 20260826, "skip_special_tokens": false, "temperature": 1, "top_p": 1}`.

Model controls: `{"chat_template": {"reasoning_effort": "high"}, "reasoning_output": "harmony_channels", "sampling": {"skip_special_tokens": false, "temperature": 1, "top_p": 1}, "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 131072}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| medium | 1/1 | 0 | 0 | 0 | 0 | 254.59 |

Parseable Sudoku grids 1/1. Clues preserved 1/1 parseable grids.

### Historical run 18: qwen-3.5-122b-local

Evidence path: `qwen-3.5-122b-local-natural-timing-v2-easy/qwen-3.5-122b-local/timing-diagnostic`.

Checkpoint: `Qwen/Qwen3.5-122B-A10B-FP8`. Revision: `a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9`. Saved/expected: 1/1. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 131072, "min_p": 0, "presence_penalty": 1.5, "repetition_penalty": 1, "seed": 20260826, "temperature": 1, "top_k": 20, "top_p": 0.95}`.

Model controls: `{"chat_template": {"enable_thinking": true, "preserve_thinking": false, "reasoning_effort": "high"}, "reasoning_output": "think_tags", "sampling": {"min_p": 0, "presence_penalty": 1.5, "repetition_penalty": 1, "temperature": 1, "top_k": 20, "top_p": 0.95}, "vllm": {"gdn_prefill_backend": "triton", "gpu_memory_utilization": 0.9, "language_model_only": true, "linear_backend": "triton", "max_model_len": 131072}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 1/1 | 0 | 0 | 0 | 0 | 194.07 |

Parseable Sudoku grids 1/1. Clues preserved 1/1 parseable grids.

### Historical run 19: qwen-3.5-122b-local

Evidence path: `qwen-3.5-122b-local-natural-timing-v2-medium/qwen-3.5-122b-local/timing-diagnostic`.

Checkpoint: `Qwen/Qwen3.5-122B-A10B-FP8`. Revision: `a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9`. Saved/expected: 1/1. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 131072, "min_p": 0, "presence_penalty": 1.5, "repetition_penalty": 1, "seed": 20260826, "temperature": 1, "top_k": 20, "top_p": 0.95}`.

Model controls: `{"chat_template": {"enable_thinking": true, "preserve_thinking": false, "reasoning_effort": "high"}, "reasoning_output": "think_tags", "sampling": {"min_p": 0, "presence_penalty": 1.5, "repetition_penalty": 1, "temperature": 1, "top_k": 20, "top_p": 0.95}, "vllm": {"gdn_prefill_backend": "triton", "gpu_memory_utilization": 0.9, "language_model_only": true, "linear_backend": "triton", "max_model_len": 131072}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| medium | 0/1 | 0 | 1 | 0 | 0 | 1392.24 |

Parseable Sudoku grids 0/1. Clues preserved 0/0 parseable grids.

### Historical run 20: qwen-3.8-27b-local

Evidence path: `qwen-3.8-27b-local-natural-timing-v2-easy/qwen-3.8-27b-local/timing-diagnostic`.

Checkpoint: `Qwen/Qwen3.8-27B-FP8`. Revision: `017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`. Saved/expected: 1/1. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 32768, "seed": 20260826, "temperature": 0.6, "top_p": 0.95}`.

Model controls: `{"chat_template": {"enable_thinking": true, "preserve_thinking": false, "reasoning_effort": "xhigh"}, "reasoning_output": "think_tags", "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 32768}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 1/1 | 0 | 0 | 0 | 0 | 80.48 |

Parseable Sudoku grids 1/1. Clues preserved 1/1 parseable grids.

### Historical run 21: qwen-3.8-27b-local

Evidence path: `qwen-3.8-27b-local-natural-timing-v2-hard/qwen-3.8-27b-local/timing-diagnostic`.

Checkpoint: `Qwen/Qwen3.8-27B-FP8`. Revision: `017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`. Saved/expected: 1/1. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 32768, "seed": 20260826, "temperature": 0.6, "top_p": 0.95}`.

Model controls: `{"chat_template": {"enable_thinking": true, "preserve_thinking": false, "reasoning_effort": "xhigh"}, "reasoning_output": "think_tags", "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 32768}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| hard | 0/1 | 0 | 1 | 0 | 0 | 422.77 |

Parseable Sudoku grids 0/1. Clues preserved 0/0 parseable grids.

### Historical run 22: qwen-3.8-27b-local

Evidence path: `qwen-3.8-27b-local-natural-timing-v2-medium/qwen-3.8-27b-local/timing-diagnostic`.

Checkpoint: `Qwen/Qwen3.8-27B-FP8`. Revision: `017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`. Saved/expected: 1/1. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 32768, "seed": 20260826, "temperature": 0.6, "top_p": 0.95}`.

Model controls: `{"chat_template": {"enable_thinking": true, "preserve_thinking": false, "reasoning_effort": "xhigh"}, "reasoning_output": "think_tags", "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 32768}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| medium | 0/1 | 0 | 1 | 0 | 0 | 412.04 |

Parseable Sudoku grids 0/1. Clues preserved 0/0 parseable grids.

### Historical run 23: qwen-3.8-27b-local

Evidence path: `qwen-3.8-27b-v2-natural-timing-v3-medium/qwen-3.8-27b-local/timing-diagnostic`.

Checkpoint: `Qwen/Qwen3.8-27B-FP8`. Revision: `017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`. Saved/expected: 1/1. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 131072, "seed": 20260826, "temperature": 1, "top_p": 1}`.

Model controls: `{"chat_template": {"enable_thinking": true, "preserve_thinking": false, "reasoning_effort": "xhigh"}, "reasoning_output": "think_tags", "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 131072}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| medium | 1/1 | 0 | 0 | 0 | 0 | 387.20 |

Parseable Sudoku grids 1/1. Clues preserved 1/1 parseable grids.

### Historical run 24: qwen-local

Evidence path: `qwen-natural-timing-v1-easy/qwen-local/timing-diagnostic`.

Checkpoint: `Qwen/Qwen3.8-27B`. Revision: `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`. Saved/expected: 1/1. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 32768, "min_p": 0.0, "presence_penalty": 0.0, "repetition_penalty": 1.0, "seed": 20260826, "temperature": 1.0, "top_k": 20, "top_p": 0.95}`.

Model controls: `{"bounded_final": null, "chat_template": {"enable_thinking": true, "preserve_thinking": false, "reasoning_effort": "medium"}, "reasoning_output": "think_tags", "sampling": {"min_p": 0.0, "presence_penalty": 0.0, "repetition_penalty": 1.0, "top_k": 20}, "structured_regex": null, "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 32768}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 1/1 | 0 | 0 | 0 | 0 | 184.71 |

Parseable Sudoku grids 1/1. Clues preserved 1/1 parseable grids.

### Historical run 25: qwen-local

Evidence path: `qwen-natural-timing-v1-hard/qwen-local/timing-diagnostic`.

Checkpoint: `Qwen/Qwen3.8-27B`. Revision: `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`. Saved/expected: 1/1. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 32768, "min_p": 0.0, "presence_penalty": 0.0, "repetition_penalty": 1.0, "seed": 20260826, "temperature": 1.0, "top_k": 20, "top_p": 0.95}`.

Model controls: `{"bounded_final": null, "chat_template": {"enable_thinking": true, "preserve_thinking": false, "reasoning_effort": "medium"}, "reasoning_output": "think_tags", "sampling": {"min_p": 0.0, "presence_penalty": 0.0, "repetition_penalty": 1.0, "top_k": 20}, "structured_regex": null, "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 32768}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| hard | 0/1 | 0 | 1 | 0 | 0 | 667.39 |

Parseable Sudoku grids 0/1. Clues preserved 0/0 parseable grids.

### Historical run 26: qwen-local

Evidence path: `qwen-natural-timing-v1-medium/qwen-local/timing-diagnostic`.

Checkpoint: `Qwen/Qwen3.8-27B`. Revision: `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`. Saved/expected: 1/1. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 32768, "min_p": 0.0, "presence_penalty": 0.0, "repetition_penalty": 1.0, "seed": 20260826, "temperature": 1.0, "top_k": 20, "top_p": 0.95}`.

Model controls: `{"bounded_final": null, "chat_template": {"enable_thinking": true, "preserve_thinking": false, "reasoning_effort": "medium"}, "reasoning_output": "think_tags", "sampling": {"min_p": 0.0, "presence_penalty": 0.0, "repetition_penalty": 1.0, "top_k": 20}, "structured_regex": null, "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 32768}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| medium | 0/1 | 0 | 1 | 0 | 0 | 666.77 |

Parseable Sudoku grids 0/1. Clues preserved 0/0 parseable grids.

### Historical run 27: qwen-local

Evidence path: `qwen-natural-timing-v2-hard/qwen-local/timing-diagnostic`.

Checkpoint: `Qwen/Qwen3.8-27B`. Revision: `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`. Saved/expected: 1/1. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 131072, "min_p": 0.0, "presence_penalty": 0.0, "repetition_penalty": 1.0, "seed": 20260826, "temperature": 1.0, "top_k": 20, "top_p": 0.95}`.

Model controls: `{"bounded_final": null, "chat_template": {"enable_thinking": true, "preserve_thinking": false, "reasoning_effort": "medium"}, "reasoning_output": "think_tags", "sampling": {"min_p": 0.0, "presence_penalty": 0.0, "repetition_penalty": 1.0, "top_k": 20}, "structured_regex": null, "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 131072}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| hard | 1/1 | 0 | 0 | 0 | 0 | 1388.72 |

Parseable Sudoku grids 1/1. Clues preserved 1/1 parseable grids.

### Historical run 28: qwen-local

Evidence path: `qwen-natural-timing-v2-medium/qwen-local/timing-diagnostic`.

Checkpoint: `Qwen/Qwen3.8-27B`. Revision: `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`. Saved/expected: 1/1. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 131072, "min_p": 0.0, "presence_penalty": 0.0, "repetition_penalty": 1.0, "seed": 20260826, "temperature": 1.0, "top_k": 20, "top_p": 0.95}`.

Model controls: `{"bounded_final": null, "chat_template": {"enable_thinking": true, "preserve_thinking": false, "reasoning_effort": "medium"}, "reasoning_output": "think_tags", "sampling": {"min_p": 0.0, "presence_penalty": 0.0, "repetition_penalty": 1.0, "top_k": 20}, "structured_regex": null, "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 131072}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| medium | 0/1 | 0 | 0 | 1 | 0 | 1103.20 |

Parseable Sudoku grids 0/1. Clues preserved 0/0 parseable grids.

### Historical run 29: qwen-local

Evidence path: `thesis-confirmatory-lean-v1/qwen-local/qualification`.

Checkpoint: `Qwen/Qwen3.8-27B`. Revision: `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`. Saved/expected: 5/5. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 2048, "seed": 20260826, "temperature": 0.0, "top_p": 1.0}`.

Model controls: `{"vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 32768}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 0/2 | 0 | 2 | 0 | 0 | 41.00 |
| medium | 0/2 | 0 | 2 | 0 | 0 | 40.78 |
| hard | 0/1 | 0 | 1 | 0 | 0 | 40.77 |

Parseable Sudoku grids 0/5. Clues preserved 0/0 parseable grids.

### Historical run 30: qwen-local

Evidence path: `thesis-confirmatory-lean-v2/qwen-local/qualification`.

Checkpoint: `Qwen/Qwen3.8-27B`. Revision: `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`. Saved/expected: 5/5. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 8192, "seed": 20260826, "temperature": 0.0, "top_p": 1.0}`.

Model controls: `{"chat_template": {"reasoning_effort": "medium"}, "reasoning_output": "think_tags", "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 32768}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 1/2 | 0 | 1 | 0 | 0 | 150.14 |
| medium | 0/2 | 0 | 2 | 0 | 0 | 163.48 |
| hard | 0/1 | 0 | 1 | 0 | 0 | 163.47 |

Parseable Sudoku grids 1/5. Clues preserved 1/1 parseable grids.

### Historical run 31: qwen-local

Evidence path: `thesis-confirmatory-lean-v3/qwen-local/qualification`.

Checkpoint: `Qwen/Qwen3.8-27B`. Revision: `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`. Saved/expected: 5/5. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 28672, "seed": 20260826, "temperature": 0.0, "top_p": 1.0}`.

Model controls: `{"chat_template": {"reasoning_effort": "medium"}, "reasoning_output": "think_tags", "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 32768}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 2/2 | 0 | 0 | 0 | 0 | 176.15 |
| medium | 0/2 | 0 | 2 | 0 | 0 | 581.16 |
| hard | 0/1 | 0 | 1 | 0 | 0 | 579.87 |

Parseable Sudoku grids 2/5. Clues preserved 2/2 parseable grids.

### Historical run 32: qwen-local

Evidence path: `thesis-confirmatory-lean-v4/qwen-local/qualification`.

Checkpoint: `Qwen/Qwen3.8-27B`. Revision: `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`. Saved/expected: 2/5. Marker and digest completion: False.

Effective recorded inference and overrides: `{"max_new_tokens": 28672, "seed": 20260826, "temperature": 0.0, "top_p": 1.0}`.

Model controls: `{"chat_template": {"reasoning_effort": "low"}, "reasoning_output": "think_tags", "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 32768}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 1/2 | 0 | 1 | 0 | 0 | 361.13 |

Parseable Sudoku grids 1/2. Clues preserved 1/1 parseable grids.

### Historical run 33: glm-flash-local

Evidence path: `thesis-confirmatory-lean-v5/glm-flash-local/qualification`.

Checkpoint: `zai-org/GLM-4.7-Flash`. Revision: `7dd20894a642a0aa287e9827cb1a1f7f91386b67`. Saved/expected: 1/5. Marker and digest completion: False.

Effective recorded inference and overrides: `{"max_new_tokens": 28672, "seed": 20260826, "temperature": 0.0, "top_p": 1.0}`.

Model controls: `{"reasoning_output": "think_tags", "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 32768}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 0/1 | 0 | 1 | 0 | 0 | 159.17 |

Parseable Sudoku grids 0/1. Clues preserved 0/0 parseable grids.

### Historical run 34: qwen-local

Evidence path: `thesis-confirmatory-lean-v5/qwen-local/qualification`.

Checkpoint: `Qwen/Qwen3.8-27B`. Revision: `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`. Saved/expected: 5/5. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 28672, "seed": 20260826, "temperature": 0.0, "top_p": 1.0}`.

Model controls: `{"chat_template": {"reasoning_effort": "medium"}, "reasoning_output": "think_tags", "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 32768}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 4/5 | 1 | 0 | 0 | 0 | 169.48 |

Parseable Sudoku grids 5/5. Clues preserved 5/5 parseable grids.

### Historical run 35: glm-flash-local

Evidence path: `thesis-confirmatory-lean-v6/glm-flash-local/qualification`.

Checkpoint: `zai-org/GLM-4.7-Flash`. Revision: `7dd20894a642a0aa287e9827cb1a1f7f91386b67`. Saved/expected: 5/5. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 28672, "seed": 20260826, "temperature": 0.0, "top_p": 1.0}`.

Model controls: `{"chat_template": {"enable_thinking": false}, "vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 32768}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 0/5 | 2 | 0 | 3 | 0 | 0.93 |

Parseable Sudoku grids 2/5. Clues preserved 1/2 parseable grids.

### Historical run 36: kimi-linear-local

Evidence path: `thesis-confirmatory-lean-v6/kimi-linear-local/qualification`.

Checkpoint: `moonshotai/Kimi-Linear-48B-A3B-Instruct`. Revision: `e1df551a447157d4658b573f9a695d57658590e9`. Saved/expected: 5/5. Marker and digest completion: True.

Effective recorded inference and overrides: `{"max_new_tokens": 28672, "seed": 20260826, "temperature": 0.0, "top_p": 1.0}`.

Model controls: `{"vllm": {"gpu_memory_utilization": 0.9, "max_model_len": 32768}}`.

| Tier | Correct / saved | Wrong grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- |
| easy | 0/5 | 0 | 4 | 1 | 0 | 96.51 |

Parseable Sudoku grids 0/5. Clues preserved 0/0 parseable grids.
