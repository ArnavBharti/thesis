"""Shared code for the reproducible Sudoku experiments."""

import sys

if sys.version_info < (3, 10):
    raise RuntimeError(
        "Python 3.10 or newer is required. On Sharanga, run "
        "'spack load anaconda3/lddgbyw' and 'source .venv/bin/activate' first."
    )

try:
    import sqlite3 as _sqlite3
except ImportError as error:
    raise RuntimeError(
        "This Python installation has no SQLite support, which vLLM requires. "
        "On Sharanga, recreate .venv using 'spack load anaconda3/lddgbyw'."
    ) from error

__version__ = "0.1.0"
