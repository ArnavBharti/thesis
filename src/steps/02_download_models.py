#!/usr/bin/env python3
"""Step 2: download or verify the three local model snapshots."""

from __future__ import annotations

import sys

import _shared  # Makes the src modules available when this file is run directly.
from download_models import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
