#!/usr/bin/env python3
"""Step 1: test, create, and audit the Sudoku dataset."""

from __future__ import annotations

import sys

import _shared  # Makes the src modules available when this file is run directly.
from run_pipeline import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
