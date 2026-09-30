#!/usr/bin/env python3
"""Assemble the writing dossier and render its PDF with existing local tools."""

import argparse
import subprocess
from pathlib import Path

from build_experiment_guide import build_guide

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, default=ROOT / "output/pdf/thesis-paper-writing-report.pdf")
    args = parser.parse_args()
    for name in ("accuracy_heatmap", "failure_decomposition", "revision_cost", "design_hierarchy"):
        subprocess.run(["rsvg-convert", "-w", "1920", "-o", str(HERE / "generated" / (name + ".png")), str(HERE / "generated" / (name + ".svg"))], check=True)
    narrative = (HERE / "writing_report.md").read_text(encoding="utf-8")
    experiment_guide = build_guide()
    (HERE / "experiment_guide.md").write_text(experiment_guide, encoding="utf-8")
    verification_heading = "# How to verify every result yourself"
    if narrative.count(verification_heading) != 1:
        raise ValueError("expected exactly one verification section")
    narrative = narrative.replace(verification_heading, experiment_guide + "\n\n" + verification_heading)
    figures = """\n\n# Evidence figures\n\nThese figures are generated from the same audit JSON as the tables. They display realized outcomes, not causal effects or independent request-level confidence intervals.\n\n![The design hierarchy distinguishes disjoint pilot/main puzzles from nested diagnostic sets and reused evidence.](generated/design_hierarchy.png)\n\n![Main accuracy by alphabet and difficulty. Every cell includes its correct count and saved denominator.](generated/accuracy_heatmap.png)\n\n![Exclusive final-outcome categories by difficulty. Counts sum to each saved denominator. Length-stopped incorrect answers take precedence over other output errors.](generated/failure_decomposition.png)\n\n![Revision accuracy against mean cumulative generation time. All branches share the same initial answers. The checker intervenes only on initially incorrect outputs.](generated/revision_cost.png)\n\n"""
    tables = (HERE / "generated/results_tables.md").read_text(encoding="utf-8")
    appendix = (HERE / "generated/detailed_appendix.md").read_text(encoding="utf-8")
    assembled = narrative + figures + tables + "\n\n" + appendix
    (HERE / "complete_report.md").write_text(assembled, encoding="utf-8")
    args.pdf.parent.mkdir(parents=True, exist_ok=True)
    # Emoji are spelled out in the PDF to avoid unsupported color-font glyphs.
    # Markdown and raw evidence retain exact original Unicode output symbols.
    emoji_names = {"🔴":"U+1F534(red)", "🟠":"U+1F7E0(orange)", "🟡":"U+1F7E1(yellow)", "🟢":"U+1F7E2(green)", "🔵":"U+1F535(blue)", "🟣":"U+1F7E3(purple)", "🟤":"U+1F7E4(brown)", "⚫":"U+26AB(black)", "⚪":"U+26AA(white)"}
    pdf_text = assembled
    for symbol, name in emoji_names.items():
        pdf_text = pdf_text.replace(symbol, name)
    pdf_text = pdf_text.replace("# Purpose, scope, and how to use this report", "# Purpose, scope, and how to use this report\n\nPDF notation note. Emoji symbols are written as Unicode code points and color names in this PDF. The Markdown edition and raw result records preserve the exact original symbols.")
    intermediate = ROOT / "tmp/pdfs/report-input.md"
    intermediate.parent.mkdir(parents=True, exist_ok=True)
    intermediate.write_text(pdf_text, encoding="utf-8")
    command = ["pandoc", str(intermediate), "--from", "markdown+tex_math_single_backslash", "--pdf-engine=xelatex", "--toc", "--toc-depth=2", "--resource-path", str(HERE), "--syntax-highlighting=tango", "--lua-filter", str(HERE / "pdf_filter.lua"), "--include-in-header", str(HERE / "pdf_header.tex"), "-V", "mainfont=Arial", "-V", "monofont=Menlo", "-V", "fontsize=10pt", "-V", "geometry:margin=20mm", "-V", "colorlinks=true", "-V", "linkcolor=blue", "-o", str(args.pdf)]
    subprocess.run(command, check=True)
    print(args.pdf)


if __name__ == "__main__":
    main()
