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
