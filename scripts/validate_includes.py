#!/usr/bin/env python3
"""Validate snippet includes (atoms-as-truth composition).

We use pymdownx.snippets with include syntax:

  --8<-- "_atoms/templates/logging-template-001.md"

This script scans docs/**/*.md and verifies every referenced include file exists.

Usage
  python3 scripts/validate_includes.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS_DIR = Path("docs")

# Matches:
# --8<-- "path"
# --8<-- 'path'
INCLUDE_RE = re.compile(r"--8<--\s*([\"\'])(.+?)\1")


def main() -> int:
    missing: list[str] = []
    checked = 0

    for md in sorted(DOCS_DIR.rglob("*.md")):
        text = md.read_text(encoding="utf-8", errors="replace")
        for m in INCLUDE_RE.finditer(text):
            inc_path = m.group(2).strip()
            # Disallow absolute paths or traversal outside docs
            if inc_path.startswith("/") or inc_path.startswith("..") or "://" in inc_path:
                missing.append(f"{md.as_posix()}: unsafe include path '{inc_path}'")
                continue
            target = DOCS_DIR / inc_path
            checked += 1
            if not target.exists():
                missing.append(f"{md.as_posix()}: missing include '{inc_path}'")

    if missing:
        print("Include validation failed:\n")
        for line in missing:
            print(f"- {line}")
        return 1

    print(f"Includes OK: {checked} include(s) checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
