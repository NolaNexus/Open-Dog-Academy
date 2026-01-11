#!/usr/bin/env python3
"""Repo checks run locally and in CI."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "generate_cards.py")])
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "validate_front_matter.py")])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
