#!/usr/bin/env python3
"""Derive paper diagnostics from checksum-verified saved evidence, without inference."""
import gzip
import hashlib
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'evidence/snapshots/2026-10-03-complete'
ALPHABETS = {
    'arabic_digits': 'Arabic', 'devanagari_numerals': 'Devanagari',
    'bengali_numerals': 'Bengali', 'uppercase_latin': 'Uppercase Latin',
    'lowercase_latin': 'Lowercase Latin', 'greek_letters': 'Greek',
    'abstract_symbols': 'Abstract', 'emoji': 'Emoji', 'nonce_labels': 'Nonce',
}


def read_rows(path):
    with gzip.open(path, 'rt', encoding='utf-8') as stream:
        return [json.loads(line) for line in stream if line.strip()]


def verify(snapshot):
    for entry in json.loads((snapshot / 'snapshot-manifest.json').read_text())['files']:
        stored = (snapshot / entry['path']).read_bytes()
        raw = gzip.decompress(stored) if entry['compressed'] else stored
        assert hashlib.sha256(stored).hexdigest() == entry['stored_sha256']
        assert hashlib.sha256(raw).hexdigest() == entry['raw_sha256']


def token_range(rows, key):
    values = [r[key] for r in rows]
    return str(min(values)) if min(values) == max(values) else f'{min(values)}--{max(values)}'


def main():
    verify(SNAPSHOT)
    models = {
        'GPT-OSS': 'local-models-v1/gpt-oss-120b-local',
        'Qwen': 'qwen-3.8-27b-v2/qwen-3.8-27b-local',
    }
    summaries = {}
    tokenizer_rows = []
    runtime_rows = []
    for model, directory in models.items():
        registry = read_rows(SNAPSHOT / 'experiment_outputs' / directory / 'exp3/representation-registry.jsonl.gz')
        assert len(registry) == 2781
        rows = [r for path in sorted((SNAPSHOT / 'experiment_outputs' / directory / 'exp4').glob('shard-*.jsonl.gz')) for r in read_rows(path)]
        assert len(rows) == 540
        assert len({r['request']['request_id'] for r in rows}) == 540
        summaries[model] = {}
        for alphabet, label in ALPHABETS.items():
            group = [r for r in rows if r['request']['input_alphabet'] == alphabet]
            assert len(group) == 60
            parsed = sum(len(r['generation']['text'].splitlines()) == 9 and all(len(line.split(' ')) == 9 and all(token in r['request']['metadata']['output_symbols'] for token in line.split(' ')) for line in r['generation']['text'].splitlines()) for r in group)
            summary = {
                'correct': sum(r['evaluation']['outcome'] == 'CORRECT' for r in group),
                'unparseable': 60 - parsed,
                'length_stopped_incorrect': sum(r['evaluation']['outcome'] != 'CORRECT' and r['generation']['finish_reason'] == 'length' for r in group),
                'mean_prompt_tokens': statistics.mean(r['generation']['prompt_tokens'] for r in group),
                'mean_generation_tokens': statistics.mean(r['generation']['completion_tokens'] for r in group),
            }
            summaries[model][alphabet] = summary
            runtime_rows.append(f"{model} & {label} & {summary['mean_prompt_tokens']:.1f} & {summary['mean_generation_tokens']:.0f} & {summary['unparseable']}/60 & {summary['length_stopped_incorrect']}/60 " + r'\\')
            if registry:
                symbols = [r for r in registry if r['kind'] == 'symbol' and r['alphabet'] == alphabet]
                assert len(symbols) == 9
                assert all(r['token_ids_isolation'] and r['token_ids_after_whitespace'] for r in symbols)
                prompt_rows = [r for r in registry if r['kind'] == 'prompt' and r['alphabet'] == alphabet and r['puzzle_id'] in {g['request']['puzzle_id'] for g in group}]
                assert len(prompt_rows) == 60
                summaries[model][alphabet]['tokenizer'] = {
                    'isolation_range': token_range(symbols, 'tokens_isolation'),
                    'leading_space_range': token_range(symbols, 'tokens_after_whitespace'),
                    'alphabet_row_tokens': symbols[0]['tokens_inside_row_total'],
                    'mean_user_prompt_tokens': statistics.mean(r['total_prompt_tokens'] for r in prompt_rows),
                }
                d = summaries[model][alphabet]['tokenizer']
                tokenizer_rows.append(f"{model} & {label} & {d['isolation_range']} & {d['leading_space_range']} & {d['alphabet_row_tokens']} & {summary['mean_prompt_tokens']:.1f} & {summary['correct']}/60 " + r'\\')
    target = Path(__file__).resolve().parent / 'generated'
    target.mkdir(exist_ok=True)
    (target / 'tokenizer_rows.tex').write_text('\n'.join(tokenizer_rows) + '\n')
    (target / 'runtime_rows.tex').write_text('\n'.join(runtime_rows) + '\n')
    (target / 'tokenizer_table.tex').write_text(
        r'\begin{tabular}{llrrrrr}' + '\n' + r'\toprule' + '\n'
        + r'Model & Alphabet & Isolated & Leading space & Alphabet row & Mean input & Correct\\' + '\n'
        + r'\midrule' + '\n' + '\n'.join(tokenizer_rows) + '\n'
        + r'\bottomrule' + '\n' + r'\end{tabular}' + '\n')
    (target / 'runtime_table.tex').write_text(
        r'\begin{tabular}{llrrrr}' + '\n' + r'\toprule' + '\n'
        + r'Model & Alphabet & Mean input tokens & Mean generated tokens & Unparseable & Truncated\\' + '\n'
        + r'\midrule' + '\n' + '\n'.join(runtime_rows) + '\n'
        + r'\bottomrule' + '\n' + r'\end{tabular}' + '\n')
    (target / 'diagnostics.json').write_text(json.dumps(summaries, indent=2) + '\n')
    print(json.dumps(summaries, indent=2))


if __name__ == '__main__':
    main()
