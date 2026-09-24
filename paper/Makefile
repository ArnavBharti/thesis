EVIDENCE ?= ../evidence/experiment_outputs

.PHONY: all clean refresh-results

all: draft.pdf

refresh-results:
	python3 generate_results.py --evidence "$(EVIDENCE)" --output generated

draft.pdf: draft.tex references.bib generated/results.tex \
	generated/pilot_difficulty.dat generated/pilot_representation.dat \
	generated/pilot_difficulty_rows.tex generated/pilot_representation_rows.tex \
	generated/main_difficulty_rows.tex generated/main_representation_rows.tex \
	generated/main_representation.dat generated/main_retention_rows.tex \
	generated/input_output_rows.tex generated/token_length_rows.tex
	latexmk -xelatex -interaction=nonstopmode -halt-on-error draft.tex

clean:
	latexmk -C draft.tex
