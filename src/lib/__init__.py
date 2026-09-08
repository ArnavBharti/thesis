"""Shared code for the reproducible Sudoku experiments."""

import sys

if sys.version_info < (3, 10):
    raise RuntimeError(
        "Python 3.10 or newer is required. On Sharanga, run "
        "'spack load python/wikzev7' and 'source .venv/bin/activate' first."
    )

__version__ = "0.1.0"
