#!/usr/bin/env python3
"""Convenience wrapper for ``python -m experiments.cli``."""

from experiments.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
