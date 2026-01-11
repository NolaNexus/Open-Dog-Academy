#!/usr/bin/env python3
"""Validate atom/skill front matter against the content contract.

Fail conditions:
- missing required keys
- duplicate IDs
"""

from __future__ import annotations

from pathlib import Path
import re
import sys
import yaml

RE_FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)\Z", re.S)

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ATOMS_DIR = DOCS / "_atoms"
SKILLS_DIR = DOCS / "skills"

ATOM_REQUIRED = {"id", "title", "type", "tags"}
SKILL_REQUIRED = {"id", "title", "level", "tags", "uses_atoms"}


def parse_front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = RE_FM.match(text)
    if not m:
        return {}
    return yaml.safe_load(m.group(1)) or {}


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    raise SystemExit(1)


def main() -> int:
    ids: set[str] = set()

    # Atoms
    for path in ATOMS_DIR.rglob("*.md"):
        if path.name == "README.md":
            continue
        fm = parse_front_matter(path)
        missing = ATOM_REQUIRED - set(fm.keys())
        if missing:
            fail(f"{path}: missing atom keys: {sorted(missing)}")
        _id = str(fm["id"]).strip()
        if not _id:
            fail(f"{path}: empty id")
        if _id in ids:
            fail(f"duplicate id: {_id}")
        ids.add(_id)

    # Skills
    for path in SKILLS_DIR.rglob("*.md"):
        if path.name == "index.md":
            continue
        fm = parse_front_matter(path)
        missing = SKILL_REQUIRED - set(fm.keys())
        if missing:
            fail(f"{path}: missing skill keys: {sorted(missing)}")
        _id = str(fm["id"]).strip()
        if not _id:
            fail(f"{path}: empty id")
        if _id in ids:
            fail(f"duplicate id: {_id}")
        ids.add(_id)

    print("Front matter validated OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
