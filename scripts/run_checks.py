#!/usr/bin/env python3
"""Run the ODA quality gates locally.

Why this exists
  - CI is the final judge, but local feedback should be fast.
  - This script groups the checks into one predictable command.

Usage
  python3 scripts/run_checks.py          # fast checks + mkdocs build
  python3 scripts/run_checks.py --fast   # skip mkdocs build
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> int:
    print(f"\n==> {' '.join(cmd)}")
    try:
        p = subprocess.run(cmd, cwd=REPO_ROOT)
        return int(p.returncode)
    except FileNotFoundError:
        exe = cmd[0]
        print(f"ERROR: command not found: {exe}")
        if exe == "mkdocs":
            print("Hint: install docs tooling with: python3 -m pip install -r requirements.txt")
        return 127


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--fast",
        action="store_true",
        help="Skip mkdocs build (useful for pre-commit and quick iterations).",
    )
    args = ap.parse_args()

    checks: list[list[str]] = [
        ["python3", "scripts/check_sizes.py"],
        ["python3", "scripts/validate_yaml.py"],
        ["python3", "scripts/validate_doc_limits.py"],
        ["python3", "scripts/validate_atoms.py"],
        ["python3", "scripts/validate_includes.py"],
        ["python3", "scripts/validate_skill_links.py"],
        ["python3", "scripts/generate_indexes.py", "--check"],
        ["python3", "scripts/generate_paths.py", "--check"],
        ["python3", "scripts/validate_status_taxonomy.py"],
        ["python3", "scripts/fix_permissions.py", "--check"],
        # Derived catalog (SQLite + JSONL) for search/reporting/AI handoff.
        # Markdown remains the source of truth.
        ["python3", "scripts/build_catalog_db.py"],
    ]

    for c in checks:
        rc = run(c)
        if rc != 0:
            return rc

    if not args.fast:
        # Strict build catches broken nav and missing files.
        rc = run(["mkdocs", "build", "--strict"])
        if rc != 0:
            return rc

    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
