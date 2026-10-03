.PHONY: all clean
all:
	mkdir -p ../tmp/main-paper
	python3 generate_diagnostics.py > ../tmp/main-paper/diagnostics-build.txt
	python3 generate_followups.py
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../tmp/main-paper/build paper.tex
	mkdir -p ../output/pdf
	cp ../tmp/main-paper/build/paper.pdf ../output/pdf/thesis-main-paper.pdf
clean:
	latexmk -C -outdir=../tmp/main-paper/build paper.tex
