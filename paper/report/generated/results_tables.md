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

## Qwen exp6

Evidence path: `qwen-3.8-27b-v2/qwen-3.8-27b-local/exp6`. Saved 135 of 135. Complete: True.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All | 120/135 | 88.9 | 9 | 6 | 0 | 0 | 257.18 |
| easy | 44/45 | 97.8 | 1 | 0 | 0 | 0 | 52.43 |
| medium | 43/45 | 95.6 | 2 | 0 | 0 | 0 | 246.05 |
| hard | 33/45 | 73.3 | 6 | 6 | 0 | 0 | 473.07 |

Parseable Sudoku grids: 54/60. Clues preserved among parseable grids: 48/54. Valid Sudoku units together: 51/54. Median record latency: 9.65 seconds. Reused outcome rows: 30.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A_arabic_to_arabic | 13/15 | 86.7 | 0 | 2 | 0 | 0 | 538.91 |
| B_greek_to_greek | 11/15 | 73.3 | 3 | 1 | 0 | 0 | 584.72 |
| C_greek_to_arabic | 11/15 | 73.3 | 4 | 0 | 0 | 0 | 531.30 |
| D_arabic_to_greek | 10/15 | 66.7 | 2 | 3 | 0 | 0 | 642.79 |
| control_coordinate_retrieval | 15/15 | 100.0 | 0 | 0 | 0 | 0 | 1.60 |
| control_copy | 15/15 | 100.0 | 0 | 0 | 0 | 0 | 1.63 |
| control_grid_conversion | 15/15 | 100.0 | 0 | 0 | 0 | 0 | 9.09 |
| control_mapping_translation | 15/15 | 100.0 | 0 | 0 | 0 | 0 | 1.41 |
| control_occurrence_count | 15/15 | 100.0 | 0 | 0 | 0 | 0 | 3.18 |

### Condition by difficulty

| Condition | Easy | Medium | Hard |
| --- | --- | --- | --- |
| A_arabic_to_arabic | 5/5 | 5/5 | 3/5 |
| B_greek_to_greek | 5/5 | 5/5 | 1/5 |
| C_greek_to_arabic | 5/5 | 4/5 | 2/5 |
| D_arabic_to_greek | 4/5 | 4/5 | 2/5 |
| control_coordinate_retrieval | 5/5 | 5/5 | 5/5 |
| control_copy | 5/5 | 5/5 | 5/5 |
| control_grid_conversion | 5/5 | 5/5 | 5/5 |
| control_mapping_translation | 5/5 | 5/5 | 5/5 |
| control_occurrence_count | 5/5 | 5/5 | 5/5 |

## Qwen exp7

Evidence path: `qwen-3.8-27b-v2/qwen-3.8-27b-local/exp7`. Saved 45 of 45. Complete: True.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All | 37/45 | 82.2 | 3 | 2 | 3 | 0 | 570.43 |
| easy | 14/15 | 93.3 | 0 | 0 | 1 | 0 | 142.82 |
| medium | 15/15 | 100.0 | 0 | 0 | 0 | 0 | 627.87 |
| hard | 8/15 | 53.3 | 3 | 2 | 2 | 0 | 940.61 |

Parseable Sudoku grids: 40/45. Clues preserved among parseable grids: 38/40. Valid Sudoku units together: 39/40. Median record latency: 440.05 seconds. Reused outcome rows: 0.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| neutral_1_tokens | 12/15 | 80.0 | 2 | 1 | 0 | 0 | 608.61 |
| neutral_2_tokens | 11/15 | 73.3 | 0 | 1 | 3 | 0 | 563.30 |
| neutral_3_tokens | 14/15 | 93.3 | 1 | 0 | 0 | 0 | 539.39 |

### Condition by difficulty

| Condition | Easy | Medium | Hard |
| --- | --- | --- | --- |
| neutral_1_tokens | 5/5 | 5/5 | 2/5 |
| neutral_2_tokens | 4/5 | 5/5 | 2/5 |
| neutral_3_tokens | 5/5 | 5/5 | 4/5 |

## Qwen exp8

Evidence path: `qwen-3.8-27b-v2/qwen-3.8-27b-local/exp8`. Saved 165 of 165. Complete: True.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All | 147/165 | 89.1 | 9 | 8 | 1 | 0 | 477.57 |
| easy | 50/55 | 90.9 | 5 | 0 | 0 | 0 | 112.43 |
| medium | 51/55 | 92.7 | 1 | 2 | 1 | 0 | 484.95 |
| hard | 46/55 | 83.6 | 3 | 6 | 0 | 0 | 835.32 |

Parseable Sudoku grids: 156/165. Clues preserved among parseable grids: 151/156. Valid Sudoku units together: 149/156. Median record latency: 353.93 seconds. Reused outcome rows: 45.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| digits_ordinary | 13/15 | 86.7 | 0 | 2 | 0 | 0 | 538.91 |
| digits_permuted | 15/15 | 100.0 | 0 | 0 | 0 | 0 | 425.90 |
| nonce_neutral | 14/15 | 93.3 | 1 | 0 | 0 | 0 | 523.15 |
| number_words_conflicting | 9/15 | 60.0 | 4 | 2 | 0 | 0 | 509.01 |
| number_words_ordinary | 12/15 | 80.0 | 0 | 2 | 1 | 0 | 624.82 |
| uppercase_random_1 | 12/15 | 80.0 | 2 | 1 | 0 | 0 | 440.48 |
| uppercase_random_2 | 15/15 | 100.0 | 0 | 0 | 0 | 0 | 331.69 |
| uppercase_random_3 | 13/15 | 86.7 | 1 | 1 | 0 | 0 | 611.53 |
| uppercase_random_4 | 15/15 | 100.0 | 0 | 0 | 0 | 0 | 356.10 |
| uppercase_random_5 | 15/15 | 100.0 | 0 | 0 | 0 | 0 | 489.27 |
| uppercase_standard | 14/15 | 93.3 | 1 | 0 | 0 | 0 | 402.41 |

### Condition by difficulty

| Condition | Easy | Medium | Hard |
| --- | --- | --- | --- |
| digits_ordinary | 5/5 | 5/5 | 3/5 |
| digits_permuted | 5/5 | 5/5 | 5/5 |
| nonce_neutral | 4/5 | 5/5 | 5/5 |
| number_words_conflicting | 2/5 | 4/5 | 3/5 |
| number_words_ordinary | 5/5 | 4/5 | 3/5 |
| uppercase_random_1 | 5/5 | 4/5 | 3/5 |
| uppercase_random_2 | 5/5 | 5/5 | 5/5 |
| uppercase_random_3 | 5/5 | 4/5 | 4/5 |
| uppercase_random_4 | 5/5 | 5/5 | 5/5 |
| uppercase_random_5 | 5/5 | 5/5 | 5/5 |
| uppercase_standard | 4/5 | 5/5 | 5/5 |

## Qwen exp9

Evidence path: `qwen-3.8-27b-v2/qwen-3.8-27b-local/exp9`. Saved 171 of 171. Complete: True.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All | 130/171 | 76.0 | 25 | 4 | 12 | 0 | 558.25 |
| easy | 51/57 | 89.5 | 3 | 0 | 3 | 0 | 210.69 |
| medium | 43/57 | 75.4 | 7 | 0 | 7 | 0 | 606.72 |
| hard | 36/57 | 63.2 | 15 | 4 | 2 | 0 | 857.33 |

Parseable Sudoku grids: 155/171. Clues preserved among parseable grids: 137/155. Valid Sudoku units together: 147/155. Median record latency: 517.43 seconds. Reused outcome rows: 0.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| empty_dot | 7/9 | 77.8 | 2 | 0 | 0 | 0 | 549.77 |
| empty_underscore | 7/9 | 77.8 | 2 | 0 | 0 | 0 | 502.99 |
| empty_word | 8/9 | 88.9 | 1 | 0 | 0 | 0 | 478.71 |
| empty_zero | 6/9 | 66.7 | 3 | 0 | 0 | 0 | 410.06 |
| latin_lowercase | 7/9 | 77.8 | 1 | 1 | 0 | 0 | 644.03 |
| latin_uppercase | 8/9 | 88.9 | 1 | 0 | 0 | 0 | 415.45 |
| mapping_alphabet_only | 7/9 | 77.8 | 2 | 0 | 0 | 0 | 548.86 |
| mapping_to_abstract | 4/9 | 44.4 | 3 | 0 | 2 | 0 | 635.56 |
| mapping_to_digits | 9/9 | 100.0 | 0 | 0 | 0 | 0 | 487.84 |
| nonce_lowercase | 8/9 | 88.9 | 1 | 0 | 0 | 0 | 580.09 |
| nonce_uppercase | 9/9 | 100.0 | 0 | 0 | 0 | 0 | 589.55 |
| output_compact | 2/9 | 22.2 | 0 | 1 | 6 | 0 | 773.64 |
| output_json | 7/9 | 77.8 | 1 | 1 | 0 | 0 | 643.48 |
| output_spaced | 7/9 | 77.8 | 2 | 0 | 0 | 0 | 548.80 |
| output_string81 | 4/9 | 44.4 | 1 | 1 | 3 | 0 | 839.71 |
| rules_constraints_alphabet | 7/9 | 77.8 | 1 | 0 | 1 | 0 | 573.50 |
| rules_explicit_constraints | 7/9 | 77.8 | 2 | 0 | 0 | 0 | 424.07 |
| rules_fully_explicit | 7/9 | 77.8 | 2 | 0 | 0 | 0 | 552.24 |
| rules_minimal | 9/9 | 100.0 | 0 | 0 | 0 | 0 | 408.32 |

### Condition by difficulty

| Condition | Easy | Medium | Hard |
| --- | --- | --- | --- |
| empty_dot | 3/3 | 3/3 | 1/3 |
| empty_underscore | 3/3 | 2/3 | 2/3 |
| empty_word | 3/3 | 2/3 | 3/3 |
| empty_zero | 3/3 | 2/3 | 1/3 |
| latin_lowercase | 3/3 | 2/3 | 2/3 |
| latin_uppercase | 2/3 | 3/3 | 3/3 |
| mapping_alphabet_only | 3/3 | 3/3 | 1/3 |
| mapping_to_abstract | 3/3 | 0/3 | 1/3 |
| mapping_to_digits | 3/3 | 3/3 | 3/3 |
| nonce_lowercase | 3/3 | 2/3 | 3/3 |
| nonce_uppercase | 3/3 | 3/3 | 3/3 |
| output_compact | 1/3 | 0/3 | 1/3 |
| output_json | 3/3 | 3/3 | 1/3 |
| output_spaced | 3/3 | 3/3 | 1/3 |
| output_string81 | 1/3 | 2/3 | 1/3 |
| rules_constraints_alphabet | 2/3 | 2/3 | 3/3 |
| rules_explicit_constraints | 3/3 | 2/3 | 2/3 |
| rules_fully_explicit | 3/3 | 3/3 | 1/3 |
| rules_minimal | 3/3 | 3/3 | 3/3 |

## Qwen exp10

Evidence path: `qwen-3.8-27b-v2/qwen-3.8-27b-local/exp10`. Saved 108 of 108. Complete: True.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All | 98/108 | 90.7 | 7 | 3 | 0 | 0 | 323.74 |
| easy | 36/36 | 100.0 | 0 | 0 | 0 | 0 | 87.06 |
| medium | 35/36 | 97.2 | 1 | 0 | 0 | 0 | 260.44 |
| hard | 27/36 | 75.0 | 6 | 3 | 0 | 0 | 623.71 |

Parseable Sudoku grids: 105/108. Clues preserved among parseable grids: 101/105. Valid Sudoku units together: 102/105. Median record latency: 104.28 seconds. Reused outcome rows: 0.

| Group | Correct / total | Accuracy % | Invalid grid | Truncated | Other output error | Operational | Mean seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| arabic_digits:checker_guided_revision | 9/9 | 100.0 | 0 | 0 | 0 | 0 | 421.80 |
| arabic_digits:one_pass | 7/9 | 77.8 | 0 | 2 | 0 | 0 | 719.65 |
| arabic_digits:one_self_revision | 9/9 | 100.0 | 0 | 0 | 0 | 0 | 236.80 |
| arabic_digits:two_self_revisions | 9/9 | 100.0 | 0 | 0 | 0 | 0 | 33.47 |
| emoji:checker_guided_revision | 9/9 | 100.0 | 0 | 0 | 0 | 0 | 405.79 |
| emoji:one_pass | 9/9 | 100.0 | 0 | 0 | 0 | 0 | 405.79 |
| emoji:one_self_revision | 9/9 | 100.0 | 0 | 0 | 0 | 0 | 70.66 |
| emoji:two_self_revisions | 7/9 | 77.8 | 2 | 0 | 0 | 0 | 92.31 |
| greek_letters:checker_guided_revision | 8/9 | 88.9 | 0 | 1 | 0 | 0 | 692.37 |
| greek_letters:one_pass | 7/9 | 77.8 | 2 | 0 | 0 | 0 | 558.38 |
| greek_letters:one_self_revision | 8/9 | 88.9 | 1 | 0 | 0 | 0 | 185.92 |
| greek_letters:two_self_revisions | 7/9 | 77.8 | 2 | 0 | 0 | 0 | 61.93 |

### Condition by difficulty

| Condition | Easy | Medium | Hard |
| --- | --- | --- | --- |
| arabic_digits:checker_guided_revision | 3/3 | 3/3 | 3/3 |
| arabic_digits:one_pass | 3/3 | 3/3 | 1/3 |
| arabic_digits:one_self_revision | 3/3 | 3/3 | 3/3 |
| arabic_digits:two_self_revisions | 3/3 | 3/3 | 3/3 |
| emoji:checker_guided_revision | 3/3 | 3/3 | 3/3 |
| emoji:one_pass | 3/3 | 3/3 | 3/3 |
| emoji:one_self_revision | 3/3 | 3/3 | 3/3 |
| emoji:two_self_revisions | 3/3 | 2/3 | 2/3 |
| greek_letters:checker_guided_revision | 3/3 | 3/3 | 2/3 |
| greek_letters:one_pass | 3/3 | 3/3 | 1/3 |
| greek_letters:one_self_revision | 3/3 | 3/3 | 2/3 |
| greek_letters:two_self_revisions | 3/3 | 3/3 | 1/3 |

### Shared-initial revision transitions and compute

| Arm | Correct | Fixed | Regressed | New calls | Extra seconds | Mean end-to-end seconds | All-stage truncations |
| --- | --- | --- | --- | --- | --- | --- | --- |
| checker_guided_revision | 26 | 3 | 0 | 4 | 4252.98 | 718.79 | 3 |
| one_pass | 23 | 0 | 0 | 0 | 0.00 | 561.28 | 2 |
| one_self_revision | 26 | 3 | 0 | 27 | 4440.47 | 725.74 | 2 |
| two_self_revisions | 23 | 2 | 2 | 54 | 6123.53 | 788.07 | 2 |

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
| qwen-3.8-27b-v2/qwen-3.8-27b-local/exp10 | 108/108 | 98 | 3 | 0 | True |
| qwen-3.8-27b-v2/qwen-3.8-27b-local/exp2 | 60/60 | 54 | 2 | 0 | True |
| qwen-3.8-27b-v2/qwen-3.8-27b-local/exp4 | 540/540 | 472 | 24 | 0 | True |
| qwen-3.8-27b-v2/qwen-3.8-27b-local/exp6 | 135/135 | 120 | 6 | 0 | True |
| qwen-3.8-27b-v2/qwen-3.8-27b-local/exp7 | 45/45 | 37 | 2 | 0 | True |
| qwen-3.8-27b-v2/qwen-3.8-27b-local/exp8 | 165/165 | 147 | 8 | 0 | True |
| qwen-3.8-27b-v2/qwen-3.8-27b-local/exp9 | 171/171 | 130 | 4 | 0 | True |
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
