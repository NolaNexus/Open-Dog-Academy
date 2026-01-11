#!/usr/bin/env python3
"""Validate that all YAML/YML files in the repository parse.

Why this exists:
- YAML is easy to break with indentation/punctuation.
- A single malformed file can silently rot registries and CI.

Behavior:
- Walk the repo from the git root.
- Attempt yaml.safe_load() for each *.yml/*.yaml.
- Fail with a clear, file-specific error message.

Usage:
  python3 scripts/validate_yaml.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml


EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "site",  # mkdocs output
    "__pycache__",
    ".pytest_cache",
    "node_modules",
}


def iter_yaml_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        # prune excluded directories
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]

        for fn in filenames:
            if fn.endswith((".yml", ".yaml")):
                files.append(Path(dirpath) / fn)
    return sorted(files)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    yaml_files = iter_yaml_files(repo_root)
    if not yaml_files:
        print("No YAML files found.")
        return 0

    errors: list[str] = []
    for fp in yaml_files:
        rel = fp.relative_to(repo_root)
        try:
            text = fp.read_text(encoding="utf-8")
            # safe_load handles empty docs (returns None)
            yaml.safe_load(text)
        except Exception as e:  # noqa: BLE001 - want full capture for CI output
            errors.append(f"- {rel}: {type(e).__name__}: {e}")

    if errors:
        print("YAML validation FAILED:\n" + "\n".join(errors))
        return 1

    print(f"YAML validation OK ({len(yaml_files)} file(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
