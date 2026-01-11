#!/usr/bin/env python3
"""Enforce predictable file permissions.

Why this exists
  - Git tracks only the executable bit, but accidental exec bits on docs are common
    and noisy.
  - Generator scripts should create files with sane defaults (0644), but we also
    want a repo-wide guardrail.

Policy (Linux/macOS)
  - docs/** and config files are NON-executable
  - Python scripts in scripts/** that have a shebang are executable

Windows note
  - chmod is mostly meaningless on Windows; this script becomes a no-op.

Usage
  python3 scripts/fix_permissions.py --check
  python3 scripts/fix_permissions.py --apply
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def is_windows() -> bool:
    return os.name == "nt"


def has_exec_bit(p: Path) -> bool:
    try:
        return bool(p.stat().st_mode & 0o111)
    except FileNotFoundError:
        return False


def has_shebang(p: Path) -> bool:
    try:
        with p.open("r", encoding="utf-8") as f:
            first = f.readline()
        return first.startswith("#!")
    except (FileNotFoundError, UnicodeDecodeError):
        return False


def iter_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for p in root.rglob("*"):
        if p.is_file() and ".git" not in p.parts:
            files.append(p)
    return files


def desired_exec_state(p: Path) -> bool | None:
    """Return True/False if we care about exec bit, None otherwise."""

    rel = p.relative_to(REPO_ROOT)

    # Never executable: docs and common config/content.
    if rel.parts and rel.parts[0] == "docs":
        return False

    if rel.name in {"mkdocs.yml", "doc-limits.yml", "ROADMAP.md", "README.md", "FORMAT_POLICY.md"}:
        return False

    if rel.suffix.lower() in {".md", ".yml", ".yaml", ".json", ".txt"}:
        return False

    # scripts: if it looks like a script you run directly, make it executable.
    if rel.parts and rel.parts[0] == "scripts" and rel.suffix == ".py":
        return True if has_shebang(p) else None

    return None


def apply_exec_state(p: Path, want_exec: bool) -> None:
    st = p.stat().st_mode
    if want_exec:
        new_mode = st | 0o111
    else:
        new_mode = st & ~0o111

    if new_mode != st:
        os.chmod(p, new_mode)


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true")
    g.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    if is_windows():
        print("Windows detected: permission bits are not enforced here.")
        return 0

    offenders: list[tuple[Path, bool, bool]] = []

    for p in iter_files(REPO_ROOT):
        want = desired_exec_state(p)
        if want is None:
            continue
        have = has_exec_bit(p)
        if have != want:
            offenders.append((p, have, want))

    if not offenders:
        if args.check:
            print("Permissions OK.")
        return 0

    if args.check:
        print("Permission drift found (exec bit):")
        for p, have, want in offenders:
            rel = p.relative_to(REPO_ROOT)
            print(f" - {rel}: have exec={have}, want exec={want}")
        print("\nFix with: python3 scripts/fix_permissions.py --apply")
        return 2

    # apply
    for p, _, want in offenders:
        apply_exec_state(p, want)
        print(f"Fixed: {p.relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
