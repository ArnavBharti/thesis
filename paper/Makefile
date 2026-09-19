EVIDENCE ?= ../tmp/paper-evidence

.PHONY: all clean refresh-results

all: draft.pdf

refresh-results:
	python3 generate_results.py --evidence "$(EVIDENCE)" --output generated

draft.pdf: draft.tex references.bib generated/results.tex \
	generated/pilot_difficulty.dat generated/pilot_representation.dat \
	generated/pilot_difficulty_rows.tex generated/pilot_representation_rows.tex \
	generated/main_part1_difficulty_rows.tex
	latexmk -xelatex -interaction=nonstopmode -halt-on-error draft.tex

clean:
	latexmk -C draft.tex
