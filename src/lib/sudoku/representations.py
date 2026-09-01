"""Bijective symbol alphabets and exact Unicode-safe grid transformation."""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass

from .grid import CELL_COUNT, Grid


@dataclass(frozen=True, slots=True)
class SymbolAlphabet:
    name: str
    symbols: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(self.symbols) != 9 or len(set(self.symbols)) != 9:
            raise ValueError(f"alphabet {self.name!r} must contain nine distinct symbols")
        for symbol in self.symbols:
            if not symbol or any(character.isspace() for character in symbol):
                raise ValueError(f"alphabet {self.name!r} contains an empty or whitespace symbol")
            if symbol == ".":
                raise ValueError("the default empty marker cannot be a value symbol")
            if unicodedata.normalize("NFC", symbol) != symbol:
                raise ValueError(f"symbol {symbol!r} is not stored in NFC form")

    def symbol_for(self, value: int) -> str:
        if value not in range(1, 10):
            raise ValueError(f"abstract value must be in 1..9, got {value}")
        return self.symbols[value - 1]

    def value_for(self, symbol: str) -> int:
        try:
            return self.symbols.index(symbol) + 1
        except ValueError as error:
            raise ValueError(f"invalid symbol {symbol!r} for alphabet {self.name!r}") from error


ALPHABETS: dict[str, SymbolAlphabet] = {
    alphabet.name: alphabet
    for alphabet in (
        SymbolAlphabet("arabic_digits", tuple("123456789")),
        SymbolAlphabet("devanagari_numerals", tuple("१२३४५६७८९")),
        SymbolAlphabet("bengali_numerals", tuple("১২৩৪৫৬৭৮৯")),
        SymbolAlphabet("uppercase_latin", tuple("ABCDEFGHI")),
        SymbolAlphabet("lowercase_latin", tuple("abcdefghi")),
        SymbolAlphabet("greek_letters", tuple("αβγδεζηθι")),
        SymbolAlphabet("abstract_symbols", ("△", "□", "○", "☆", "×", "†", "‡", "§", "¶")),
        SymbolAlphabet("emoji", ("🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "⚪")),
        SymbolAlphabet("nonce_labels", ("KAV", "MIP", "ZOT", "RUL", "BEK", "DAX", "PEV", "NUG", "WIF")),
    )
}


def encode_grid(grid: Grid, alphabet: SymbolAlphabet, *, empty_marker: str = ".") -> str:
    if not empty_marker or any(character.isspace() for character in empty_marker):
        raise ValueError("empty marker must be one non-whitespace token")
    rows: list[str] = []
    for row in grid.rows():
        rows.append(
            " ".join(alphabet.symbol_for(value) if value else empty_marker for value in row)
        )
    encoded = "\n".join(rows)
    encoded.encode("utf-8", errors="strict")
    return encoded


def decode_grid(text: str, alphabet: SymbolAlphabet, *, empty_marker: str = ".") -> Grid:
    text.encode("utf-8", errors="strict").decode("utf-8", errors="strict")
    if unicodedata.normalize("NFC", text) != text:
        raise UnicodeError("grid is not encoded in NFC-normalized Unicode")
    rows = text.splitlines()
    if len(rows) != 9:
        raise ValueError(f"expected 9 rows, got {len(rows)}")
    values: list[int] = []
    for number, row in enumerate(rows, start=1):
        tokens = row.split(" ")
        if len(tokens) != 9 or any(not token for token in tokens):
            raise ValueError(f"row {number} is not exactly 9 single-space-separated symbols")
        for token in tokens:
            values.append(0 if token == empty_marker else alphabet.value_for(token))
    if len(values) != CELL_COUNT:  # defensive: row validation above already guarantees this
        raise ValueError(f"expected 81 cells, got {len(values)}")
    return Grid(tuple(values))


def verify_round_trip(grid: Grid, alphabet: SymbolAlphabet) -> None:
    encoded = encode_grid(grid, alphabet)
    decoded = decode_grid(encoded, alphabet)
    if decoded != grid:
        raise ValueError(f"Unicode round-trip invariant failed for {alphabet.name}")
