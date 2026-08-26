"""Frozen prompt templates and output-format instructions for all experiments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from sudoku.grid import Grid
from sudoku.representations import SymbolAlphabet, encode_grid

RuleStyle = Literal["minimal", "explicit_constraints", "constraints_alphabet", "fully_explicit"]
MappingStyle = Literal["alphabet_only", "to_digits", "to_abstract"]
OutputFormat = Literal["spaced", "compact", "string81", "json"]


@dataclass(frozen=True, slots=True)
class PromptOptions:
    rule_style: RuleStyle = "fully_explicit"
    mapping_style: MappingStyle = "alphabet_only"
    output_format: OutputFormat = "spaced"
    empty_marker: str = "."


def solve_prompt(
    puzzle: Grid,
    input_alphabet: SymbolAlphabet,
    output_alphabet: SymbolAlphabet | None = None,
    *,
    options: PromptOptions = PromptOptions(),
) -> str:
    output_alphabet = output_alphabet or input_alphabet
    parts = ["Solve the following 9x9 Sudoku."]

    if options.rule_style in {"constraints_alphabet", "fully_explicit"}:
        parts.append("Valid input symbols:\n" + " ".join(input_alphabet.symbols))
    if output_alphabet != input_alphabet:
        parts.append("Valid output symbols:\n" + " ".join(output_alphabet.symbols))

    if options.mapping_style == "to_digits":
        parts.append(
            "Symbol mapping:\n"
            + " ".join(
                f"{input_alphabet.symbol_for(value)}={value}" for value in range(1, 10)
            )
        )
    elif options.mapping_style == "to_abstract":
        parts.append(
            "Abstract-value mapping:\n"
            + " ".join(
                f"{input_alphabet.symbol_for(value)}=V{value}" for value in range(1, 10)
            )
        )

    if output_alphabet != input_alphabet:
        parts.append(
            "Input-to-output mapping:\n"
            + " ".join(
                f"{input_alphabet.symbol_for(value)}={output_alphabet.symbol_for(value)}"
                for value in range(1, 10)
            )
        )

    if options.rule_style == "minimal":
        parts.append("Use standard Sudoku rules and do not change the given cells.")
    else:
        rules = [
            "Every row must contain each valid value exactly once.",
            "Every column must contain each valid value exactly once.",
            "Every 3x3 box must contain each valid value exactly once.",
            "Do not change the given cells.",
        ]
        if options.rule_style == "fully_explicit":
            rules.append("The visible symbols are labels; apply the same symbol-value mapping everywhere.")
        parts.append("Rules:\n- " + "\n- ".join(rules))

    parts.append(
        "Puzzle:\n"
        + encode_grid(puzzle, input_alphabet, empty_marker=options.empty_marker)
    )
    parts.append(_output_instruction(options.output_format, output_alphabet))
    return "\n\n".join(parts)


def revision_prompt(*, checker_feedback: str | None = None) -> str:
    if checker_feedback:
        return (
            "The automatic checker found the following errors:\n"
            f"{checker_feedback}\n\n"
            "Correct the answer. Return only 9 lines of 9 space-separated symbols."
        )
    return (
        "Check your answer and return a revised answer. Verify that it has exactly 81 cells, "
        "keeps every given clue unchanged, and satisfies every row, column, and 3x3 box. "
        "Return only 9 lines of 9 space-separated symbols."
    )


def format_solution(grid: Grid, alphabet: SymbolAlphabet, output_format: OutputFormat) -> str:
    spaced = encode_grid(grid, alphabet)
    if output_format == "spaced":
        return spaced
    if output_format == "compact":
        return "\n".join(line.replace(" ", "") for line in spaced.splitlines())
    if output_format == "string81":
        return "".join(line.replace(" ", "") for line in spaced.splitlines())
    if output_format == "json":
        import json

        return json.dumps([line.split(" ") for line in spaced.splitlines()], ensure_ascii=False)
    raise ValueError(f"unsupported output format {output_format!r}")


def _output_instruction(output_format: OutputFormat, alphabet: SymbolAlphabet) -> str:
    if output_format == "spaced":
        return "Return only 9 lines of 9 space-separated output symbols."
    if output_format == "compact":
        if any(len(symbol) != 1 for symbol in alphabet.symbols):
            raise ValueError("compact rows require single-code-point symbols")
        return "Return only 9 lines, each containing exactly 9 output symbols with no separators."
    if output_format == "string81":
        if any(len(symbol) != 1 for symbol in alphabet.symbols):
            raise ValueError("the 81-symbol format requires single-code-point symbols")
        return "Return only one string of exactly 81 output symbols with no spaces or line breaks."
    if output_format == "json":
        return "Return only a JSON array containing 9 arrays of 9 output-symbol strings."
    raise ValueError(f"unsupported output format {output_format!r}")
