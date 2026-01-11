#!/usr/bin/env python3
"""ODA size audit.

- Shows total size under a root folder
- Lists top-N largest files
- Aggregates by extension

Where to run:
  From the repo root:
    python3 scripts/size_audit.py .
"""

from __future__ import annotations

import os
import sys
from collections import defaultdict

TOP_N = 25
SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules"}


def walk_files(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            try:
                st = os.stat(p)
            except OSError:
                continue
            yield p, st.st_size


def human(n: int) -> str:
    x = float(n)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if x < 1024 or unit == "TB":
            if unit == "B":
                return f"{int(x)}{unit}"
            return f"{x:.1f}{unit}"
        x /= 1024
    return f"{x:.1f}TB"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/size_audit.py /path/to/folder")
        return 2

    root = os.path.abspath(sys.argv[1])
    files = list(walk_files(root))
    total = sum(sz for _, sz in files)

    by_ext: dict[str, int] = defaultdict(int)
    for p, sz in files:
        _, ext = os.path.splitext(p.lower())
        by_ext[ext or "(noext)"] += sz

    print(f"Root:  {root}")
    print(f"Total: {human(total)}")
    print()

    print("Top files:")
    for p, sz in sorted(files, key=lambda x: x[1], reverse=True)[:TOP_N]:
        rel = os.path.relpath(p, root)
        print(f"  {human(sz):>8}  {rel}")

    print("\nBy extension (top 20):")
    for ext, sz in sorted(by_ext.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {human(sz):>8}  {ext}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
