"""Deterministic request generation for qualification and Experiments 2 through 10."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterable, Iterator, Sequence

from sudoku.representations import ALPHABETS, SymbolAlphabet, encode_grid
from sudoku.schema import PuzzleRecord, grid_from_compact

from .backends import TokenizerAdapter
from .config import ExperimentConfig, ModelConfig
from .prompts import PromptOptions, format_solution, solve_prompt
from .records import ExperimentRequest, Message
from .selection import deterministic_permutation, select_stratified
from .token_registry import construct_token_alphabets

INFERENCE_EXPERIMENTS = (
    "qualification",
    "exp2",
    "exp4",
    "exp6",
    "exp7",
    "exp8",
    "exp9",
    "exp10",
)
DERIVED_EXPERIMENTS = ("exp1", "exp3", "exp5")


@dataclass(frozen=True, slots=True)
class CaseFactory:
    config: ExperimentConfig
    records: tuple[PuzzleRecord, ...]

    def requests(
        self,
        experiment: str,
        model: ModelConfig,
        *,
        tokenizer: TokenizerAdapter | None = None,
    ) -> Iterator[ExperimentRequest]:
        builders = {
            "qualification": self._qualification,
            "exp2": self._exp2,
            "exp4": self._exp4,
            "exp6": self._exp6,
            "exp7": self._exp7,
            "exp8": self._exp8,
            "exp9": self._exp9,
            "exp10": self._exp10,
        }
        try:
            builder = builders[experiment]
        except KeyError as error:
            raise ValueError(f"{experiment!r} does not generate inference requests") from error
        if experiment == "exp7":
            if tokenizer is None:
                raise ValueError("Experiment 7 requires the model tokenizer")
            yield from builder(model, tokenizer)  # type: ignore[call-arg]
        else:
            yield from builder(model)  # type: ignore[call-arg]

    def _qualification(self, model: ModelConfig) -> Iterator[ExperimentRequest]:
        alphabets = (
            ALPHABETS["arabic_digits"],
            ALPHABETS["greek_letters"],
            ALPHABETS["emoji"],
            ALPHABETS["nonce_labels"],
            ALPHABETS["devanagari_numerals"],
        )
        puzzles = select_stratified(
            self.records, 2, seed=self.config.master_seed, namespace="qualification"
        )[:5]
        for record, alphabet in zip(puzzles, alphabets, strict=True):
            yield self._solve_request("qualification", alphabet.name, model, record, alphabet)

    def _exp2(self, model: ModelConfig) -> Iterator[ExperimentRequest]:
        subset = select_stratified(
            self.records,
            self.config.pilot_per_tier,
            seed=self.config.master_seed,
            namespace="pilot",
        )
        for record in subset:
            for name in ("arabic_digits", "uppercase_latin", "greek_letters", "emoji"):
                alphabet = ALPHABETS[name]
                yield self._solve_request("exp2", name, model, record, alphabet)

    def _exp4(self, model: ModelConfig) -> Iterator[ExperimentRequest]:
        for record in self.records:
            for alphabet in ALPHABETS.values():
                yield self._solve_request("exp4", alphabet.name, model, record, alphabet)

    def _exp6(self, model: ModelConfig) -> Iterator[ExperimentRequest]:
        subset = select_stratified(
            self.records,
            self.config.mechanism_per_tier,
            seed=self.config.master_seed,
            namespace="mechanism",
        )
        arabic = ALPHABETS["arabic_digits"]
        greek = ALPHABETS["greek_letters"]
        for record in subset:
            for condition, input_alphabet, output_alphabet in (
                ("A_arabic_to_arabic", arabic, arabic),
                ("B_greek_to_greek", greek, greek),
                ("C_greek_to_arabic", greek, arabic),
                ("D_arabic_to_greek", arabic, greek),
            ):
                yield self._solve_request(
                    "exp6",
                    condition,
                    model,
                    record,
                    input_alphabet,
                    output_alphabet,
                    options=PromptOptions(mapping_style="to_digits" if input_alphabet != output_alphabet else "alphabet_only"),
                )
            yield from self._exp6_controls(model, record, greek, arabic)

    def _exp6_controls(
        self,
        model: ModelConfig,
        record: PuzzleRecord,
        greek: SymbolAlphabet,
        arabic: SymbolAlphabet,
    ) -> Iterator[ExperimentRequest]:
        solution = grid_from_compact(record.solution)
        greek_solution = encode_grid(solution, greek)
        arabic_solution = encode_grid(solution, arabic)
        row = greek_solution.splitlines()[0]
        controls = (
            (
                "control_copy",
                f"Copy the following row exactly. Return only the copied row.\n\n{row}",
                row,
            ),
            (
                "control_mapping_translation",
                "Using α=1, β=2, γ=3, δ=4, ε=5, ζ=6, η=7, θ=8, ι=9, translate this sequence. Return only the translated space-separated sequence.\n\nε γ η",
                "5 3 7",
            ),
            (
                "control_coordinate_retrieval",
                f"Grid:\n{greek_solution}\n\nWhich symbol is in row 1, column 5? Return only that symbol.",
                greek.symbol_for(solution.cells[4]),
            ),
            (
                "control_occurrence_count",
                f"Count occurrences of {greek.symbol_for(1)} in this completed grid. Return only the integer.\n\n{greek_solution}",
                "9",
            ),
            (
                "control_grid_conversion",
                "Convert the supplied completed Greek grid to Arabic digits using α=1 through ι=9. Return only 9 lines of 9 space-separated digits.\n\n"
                + greek_solution,
                arabic_solution,
            ),
        )
        for condition, prompt, expected in controls:
            yield ExperimentRequest(
                experiment="exp6",
                condition=condition,
                model=model.name,
                messages=(Message("user", prompt),),
                puzzle_id=record.puzzle_id,
                metadata={"evaluation_kind": "exact_text", "expected_text": expected},
            )

    def _exp7(
        self,
        model: ModelConfig,
        tokenizer: TokenizerAdapter,
    ) -> Iterator[ExperimentRequest]:
        plan = construct_token_alphabets(tokenizer, seed=self.config.master_seed)
        if plan.missing_token_lengths:
            missing = ", ".join(map(str, plan.missing_token_lengths))
            raise ValueError(
                f"could not construct nine neutral labels for token lengths {missing}; "
                "inspect the Experiment 3 token registry before running Experiment 7"
            )
        subset = select_stratified(
            self.records,
            self.config.mechanism_per_tier,
            seed=self.config.master_seed,
            namespace="token-length",
        )
        for record in subset:
            for alphabet in plan.alphabets:
                token_length = len(tokenizer.encode(alphabet.symbols[0]))
                yield self._solve_request(
                    "exp7",
                    f"neutral_{token_length}_tokens",
                    model,
                    record,
                    alphabet,
                    extra_metadata={"token_length": token_length},
                )

    def _exp8(self, model: ModelConfig) -> Iterator[ExperimentRequest]:
        subset = select_stratified(
            self.records,
            self.config.mechanism_per_tier,
            seed=self.config.master_seed,
            namespace="binding",
        )
        uppercase = ALPHABETS["uppercase_latin"]
        alphabets: list[tuple[str, SymbolAlphabet]] = [("uppercase_standard", uppercase)]
        for index in range(5):
            symbols = deterministic_permutation(
                uppercase.symbols,
                seed=self.config.master_seed,
                namespace=f"uppercase-random-{index}",
            )
            alphabets.append((f"uppercase_random_{index + 1}", SymbolAlphabet(f"uppercase_random_{index + 1}", symbols)))

        digits = ALPHABETS["arabic_digits"]
        permuted_digits = deterministic_permutation(
            digits.symbols, seed=self.config.master_seed, namespace="permuted-digits"
        )
        number_words = SymbolAlphabet(
            "number_words", ("ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE")
        )
        conflicting_words = SymbolAlphabet(
            "conflicting_number_words",
            deterministic_permutation(
                number_words.symbols,
                seed=self.config.master_seed,
                namespace="conflicting-number-words",
            ),
        )
        alphabets.extend(
            (
                ("digits_ordinary", digits),
                ("digits_permuted", SymbolAlphabet("permuted_digits", permuted_digits)),
                ("number_words_ordinary", number_words),
                ("number_words_conflicting", conflicting_words),
                ("nonce_neutral", ALPHABETS["nonce_labels"]),
            )
        )
        for record in subset:
            for condition, alphabet in alphabets:
                yield self._solve_request("exp8", condition, model, record, alphabet)

    def _exp9(self, model: ModelConfig) -> Iterator[ExperimentRequest]:
        subset = select_stratified(
            self.records,
            self.config.ablation_per_tier,
            seed=self.config.master_seed,
            namespace="ablation",
        )
        greek = ALPHABETS["greek_letters"]
        variants: list[tuple[str, SymbolAlphabet, PromptOptions]] = []
        for style in ("minimal", "explicit_constraints", "constraints_alphabet", "fully_explicit"):
            variants.append((f"rules_{style}", greek, PromptOptions(rule_style=style)))
        for style in ("alphabet_only", "to_digits", "to_abstract"):
            variants.append((f"mapping_{style}", greek, PromptOptions(mapping_style=style)))
        for output_format in ("spaced", "compact", "string81", "json"):
            variants.append((f"output_{output_format}", greek, PromptOptions(output_format=output_format)))
        for name, marker in (("dot", "."), ("zero", "0"), ("underscore", "_"), ("word", "EMPTY")):
            variants.append((f"empty_{name}", greek, PromptOptions(empty_marker=marker)))
        variants.extend(
            (
                ("latin_uppercase", ALPHABETS["uppercase_latin"], PromptOptions()),
                ("latin_lowercase", ALPHABETS["lowercase_latin"], PromptOptions()),
                ("nonce_uppercase", ALPHABETS["nonce_labels"], PromptOptions()),
                (
                    "nonce_lowercase",
                    SymbolAlphabet("nonce_lowercase", tuple(symbol.lower() for symbol in ALPHABETS["nonce_labels"].symbols)),
                    PromptOptions(),
                ),
            )
        )
        for record in subset:
            for condition, alphabet, options in variants:
                yield self._solve_request("exp9", condition, model, record, alphabet, options=options)

    def _exp10(self, model: ModelConfig) -> Iterator[ExperimentRequest]:
        subset = select_stratified(
            self.records,
            self.config.ablation_per_tier,
            seed=self.config.master_seed,
            namespace="revision",
        )
        for record in subset:
            for alphabet_name in ("arabic_digits", "greek_letters", "emoji"):
                alphabet = ALPHABETS[alphabet_name]
                for condition in (
                    "one_pass",
                    "one_self_revision",
                    "two_self_revisions",
                    "checker_guided_revision",
                ):
                    yield self._solve_request(
                        "exp10",
                        f"{alphabet_name}:{condition}",
                        model,
                        record,
                        alphabet,
                        extra_metadata={"revision_condition": condition},
                    )

    def _solve_request(
        self,
        experiment: str,
        condition: str,
        model: ModelConfig,
        record: PuzzleRecord,
        input_alphabet: SymbolAlphabet,
        output_alphabet: SymbolAlphabet | None = None,
        *,
        options: PromptOptions = PromptOptions(),
        extra_metadata: dict[str, object] | None = None,
    ) -> ExperimentRequest:
        output_alphabet = output_alphabet or input_alphabet
        puzzle = grid_from_compact(record.puzzle)
        metadata: dict[str, object] = {
            "difficulty": record.difficulty,
            "input_symbols": list(input_alphabet.symbols),
            "output_symbols": list(output_alphabet.symbols),
            "output_format": options.output_format,
            "empty_marker": options.empty_marker,
            "evaluation_kind": "sudoku",
        }
        if extra_metadata:
            metadata.update(extra_metadata)
        return ExperimentRequest(
            experiment=experiment,
            condition=condition,
            model=model.name,
            messages=(Message("user", solve_prompt(puzzle, input_alphabet, output_alphabet, options=options)),),
            puzzle_id=record.puzzle_id,
            input_alphabet=input_alphabet.name,
            output_alphabet=output_alphabet.name,
            expected_solution=record.solution,
            puzzle=record.puzzle,
            metadata=metadata,
        )
