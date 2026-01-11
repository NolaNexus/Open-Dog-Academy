#!/usr/bin/env python3
"""
Check repository file sizes against ODA hard caps.

Usage:
  python3 scripts/check_sizes.py

This script is designed to be CI-friendly.
Exit codes:
  0 = OK
  1 = One or more files exceed caps
"""

from __future__ import annotations

import pathlib
import sys
from typing import Dict, List, Tuple

# Hard caps in bytes
MB = 1024 * 1024

HARD_CAPS_BY_EXT: Dict[str, int] = {
    ".md": 1 * MB,
    ".yml": 1 * MB,
    ".yaml": 1 * MB,
    ".csv": 5 * MB,
    ".json": 5 * MB,
    ".jsonl": 5 * MB,
    ".svg": 1 * MB,
    ".webp": 1 * MB,
    ".jpg": 1 * MB,
    ".jpeg": 1 * MB,
    ".png": 2 * MB,
    ".opus": 5 * MB,
    ".ogg": 5 * MB,
    ".m4a": 5 * MB,
    ".mp3": 5 * MB,
    ".mp4": 50 * MB,
    ".zip": 25 * MB,
    ".pdf": 0,  # PDFs are disallowed by default in this repo
}

EXCLUDE_DIRS = {
    ".git",
    ".github",
    "site",  # mkdocs build output
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
}

def human_bytes(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n/1024:.1f} KB"
    return f"{n/(1024*1024):.2f} MB"

def main() -> int:
    repo_root = pathlib.Path(__file__).resolve().parents[1]

    offenders: List[Tuple[pathlib.Path, int, int]] = []

    for p in repo_root.rglob("*"):
        if not p.is_file():
            continue

        rel_parts = p.relative_to(repo_root).parts
        if any(part in EXCLUDE_DIRS for part in rel_parts):
            continue

        ext = p.suffix.lower()
        if ext in HARD_CAPS_BY_EXT:
            cap = HARD_CAPS_BY_EXT[ext]
            size = p.stat().st_size

            # Special rule: PDFs are disallowed unless cap > 0
            if ext == ".pdf" and cap == 0:
                offenders.append((p, size, cap))
                continue

            if cap > 0 and size > cap:
                offenders.append((p, size, cap))

    if offenders:
        print("ERROR: file size policy violations:")
        for p, size, cap in sorted(offenders, key=lambda x: x[1], reverse=True):
            rel = p.relative_to(repo_root)
            if cap == 0 and p.suffix.lower() == ".pdf":
                print(f"  - {rel}: {human_bytes(size)} (PDFs disallowed by policy)")
            else:
                print(f"  - {rel}: {human_bytes(size)} > cap {human_bytes(cap)}")
        print("\nTip: see docs/format-policy.md for caps and allowed formats.")
        return 1

    print("OK: all files within size caps (and no PDFs present).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
