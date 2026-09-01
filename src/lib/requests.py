"""Small request builders shared by the visible numbered experiment scripts."""

from __future__ import annotations

from .config import ModelConfig
from .prompts import PromptOptions, solve_prompt
from .records import ExperimentRequest, Message
from .sudoku.representations import SymbolAlphabet
from .sudoku.schema import PuzzleRecord, grid_from_compact


def sudoku_request(
    experiment: str,
    condition: str,
    model: ModelConfig,
    record: PuzzleRecord,
    input_alphabet: SymbolAlphabet,
    output_alphabet: SymbolAlphabet | None = None,
    *,
    options: PromptOptions = PromptOptions(),
    metadata: dict[str, object] | None = None,
) -> ExperimentRequest:
    """Build one Sudoku request without deciding which experiments should use it."""

    output_alphabet = output_alphabet or input_alphabet
    request_metadata: dict[str, object] = {
        "difficulty": record.difficulty,
        "input_symbols": list(input_alphabet.symbols),
        "output_symbols": list(output_alphabet.symbols),
        "output_format": options.output_format,
        "empty_marker": options.empty_marker,
        "evaluation_kind": "sudoku",
    }
    if metadata:
        request_metadata.update(metadata)
    puzzle = grid_from_compact(record.puzzle)
    return ExperimentRequest(
        experiment=experiment,
        condition=condition,
        model=model.name,
        messages=(
            Message(
                "user",
                solve_prompt(
                    puzzle,
                    input_alphabet,
                    output_alphabet,
                    options=options,
                ),
            ),
        ),
        puzzle_id=record.puzzle_id,
        input_alphabet=input_alphabet.name,
        output_alphabet=output_alphabet.name,
        expected_solution=record.solution,
        puzzle=record.puzzle,
        metadata=request_metadata,
    )
