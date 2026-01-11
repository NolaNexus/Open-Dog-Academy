#!/usr/bin/env python3
"""Minimal repo checks (expand later)."""
from __future__ import annotations
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
GEN = ROOT / "docs" / "_generated" / "atoms" / "index.md"

def main() -> int:
    if not GEN.exists():
        subprocess.check_call([sys.executable, str(ROOT/"scripts"/"generate_cards.py")])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
