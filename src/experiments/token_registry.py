"""Unicode/token diagnostics and tokenizer-specific neutral alphabet construction."""

from __future__ import annotations

import itertools
import random
import unicodedata
from dataclasses import dataclass
from typing import Any, Iterable

from sudoku.representations import ALPHABETS, SymbolAlphabet
from sudoku.schema import PuzzleRecord, grid_from_compact

from .backends import TokenizerAdapter
from .prompts import solve_prompt
from .selection import derived_seed


@dataclass(frozen=True, slots=True)
class TokenAlphabetPlan:
    alphabets: tuple[SymbolAlphabet, ...]
    registry: tuple[dict[str, Any], ...]
    missing_token_lengths: tuple[int, ...]


def unicode_registry() -> tuple[dict[str, Any], ...]:
    rows: list[dict[str, Any]] = []
    for alphabet in ALPHABETS.values():
        for position, symbol in enumerate(alphabet.symbols, start=1):
            rows.append(
                {
                    "alphabet": alphabet.name,
                    "abstract_value": position,
                    "symbol": symbol,
                    "unicode_code_points": [f"U+{ord(character):04X}" for character in symbol],
                    "utf8_bytes": len(symbol.encode("utf-8")),
                    "code_point_count": len(symbol),
                    "grapheme_count": _grapheme_count(symbol),
                    "tokens_isolation": None,
                    "token_ids_isolation": None,
                    "tokens_after_whitespace": None,
                    "token_ids_after_whitespace": None,
                    "tokens_inside_row_total": None,
                    "tokenizer": None,
                }
            )
    return tuple(rows)


def symbol_diagnostics(symbol: str, tokenizer: TokenizerAdapter) -> dict[str, Any]:
    return {
        "symbol": symbol,
        "unicode_code_points": [f"U+{ord(character):04X}" for character in symbol],
        "utf8_bytes": len(symbol.encode("utf-8")),
        "code_point_count": len(symbol),
        "grapheme_count": _grapheme_count(symbol),
        "tokens_isolation": len(tokenizer.encode(symbol)),
        "token_ids_isolation": tokenizer.encode(symbol),
        "tokens_after_whitespace": len(tokenizer.encode(" " + symbol)),
        "token_ids_after_whitespace": tokenizer.encode(" " + symbol),
    }


def representation_registry(tokenizer: TokenizerAdapter) -> tuple[dict[str, Any], ...]:
    rows: list[dict[str, Any]] = []
    for alphabet in ALPHABETS.values():
        row_text = " ".join(alphabet.symbols)
        for position, symbol in enumerate(alphabet.symbols, start=1):
            value = symbol_diagnostics(symbol, tokenizer)
            value.update(
                {
                    "alphabet": alphabet.name,
                    "abstract_value": position,
                    "tokens_inside_row_total": len(tokenizer.encode(row_text)),
                    "tokenizer": tokenizer.identity,
                }
            )
            rows.append(value)
    return tuple(rows)


def prompt_token_registry(
    records: Iterable[PuzzleRecord],
    tokenizer: TokenizerAdapter,
) -> tuple[dict[str, Any], ...]:
    rows: list[dict[str, Any]] = []
    for record in records:
        puzzle = grid_from_compact(record.puzzle)
        for alphabet in ALPHABETS.values():
            visible = [alphabet.symbol_for(value) for value in puzzle.cells if value]
            clue_tokens = sum(len(tokenizer.encode(symbol)) for symbol in visible)
            prompt = solve_prompt(puzzle, alphabet)
            rows.append(
                {
                    "kind": "prompt",
                    "puzzle_id": record.puzzle_id,
                    "difficulty": record.difficulty,
                    "alphabet": alphabet.name,
                    "clue_count": len(visible),
                    "visible_clue_tokens": clue_tokens,
                    "mean_clue_tokens": clue_tokens / len(visible),
                    "total_prompt_tokens": len(tokenizer.encode(prompt)),
                    "tokenizer": tokenizer.identity,
                }
            )
    return tuple(rows)


def construct_token_alphabets(
    tokenizer: TokenizerAdapter,
    *,
    seed: int,
    search_limit: int = 100_000,
) -> TokenAlphabetPlan:
    rng = random.Random(derived_seed(seed, f"token-alphabets:{tokenizer.identity}"))
    candidates = list(_nonce_candidates())
    rng.shuffle(candidates)
    bins: dict[int, list[str]] = {1: [], 2: [], 3: []}
    registry: list[dict[str, Any]] = []

    for candidate in candidates[:search_limit]:
        isolation = len(tokenizer.encode(candidate))
        after_whitespace = len(tokenizer.encode(" " + candidate))
        if isolation == after_whitespace and isolation in bins and candidate not in bins[isolation]:
            bins[isolation].append(candidate)
            registry.append(symbol_diagnostics(candidate, tokenizer))
            if all(len(values) >= 9 for values in bins.values()):
                break

    alphabets = tuple(
        SymbolAlphabet(f"neutral_{length}_token_{tokenizer.identity}", tuple(bins[length][:9]))
        for length in (1, 2, 3)
        if len(bins[length]) >= 9
    )
    missing = tuple(length for length in (1, 2, 3) if len(bins[length]) < 9)
    return TokenAlphabetPlan(alphabets, tuple(registry), missing)


def _nonce_candidates() -> Iterable[str]:
    consonants = "BCDFGHJKLMNPQRSTVWXYZ"
    vowels = "AEIOU"
    for length in range(1, 13):
        if length <= 4:
            for characters in itertools.product("ABCDEFGHIJKLMNOPQRSTUVWXYZ", repeat=length):
                yield "".join(characters)
        else:
            for index in range(20_000):
                pieces = [
                    consonants[(index + offset * 7) % len(consonants)]
                    if offset % 2 == 0
                    else vowels[(index // (offset + 1) + offset) % len(vowels)]
                    for offset in range(length)
                ]
                yield "".join(pieces) + str(index % 97)


def _grapheme_count(value: str) -> int:
    count = 0
    joined = False
    for character in value:
        category = unicodedata.category(character)
        if character == "\u200d":
            joined = True
            continue
        if category.startswith("M") or character in {"\ufe0e", "\ufe0f"}:
            continue
        if joined:
            joined = False
            continue
        count += 1
    return count
