#!/usr/bin/env python3
"""
Validate that every SKILL_ID referenced in docs/classes (and optionally instructor guides)
has a corresponding file in docs/skills/<namespace>/<SKILL_ID>.md.

Usage:
  python3 scripts/validate_skill_links.py

Exit codes:
  0 = OK
  1 = Missing skill files found
"""

from __future__ import annotations

import pathlib
import re
import sys
from typing import Dict, Iterable, List, Set, Tuple

SKILL_PATTERN = re.compile(r"\b[A-Z]{2,6}_[A-Z0-9]{2,}\b")

PREFIX_DIR_MAP: Dict[str, str] = {
    "AG_": "skills/ag",
    "ARC_": "skills/arc",
    "CC_": "skills/cc",
    "IND_": "skills/ind",
    "LS_": "skills/ls",
    "NW_": "skills/nw",
    "OB_": "skills/ob",
    "OL_": "skills/ol",
    "RALLY_": "skills/rally",
    "RCD_": "skills/rcd",
    "REG_": "skills/reg",
    "RET_": "skills/ret",
    "SHAPE_": "skills/shape",
    "TASK_": "skills/task",
    "PLAY_": "skills/play",
}

def iter_md_files(folder: pathlib.Path) -> Iterable[pathlib.Path]:
    if not folder.exists():
        return []
    return folder.rglob("*.md")

def parse_skill_ids(text: str) -> Set[str]:
    return set(SKILL_PATTERN.findall(text))

def folder_for(skill_id: str, docs_root: pathlib.Path) -> pathlib.Path:
    for pref, rel in PREFIX_DIR_MAP.items():
        if skill_id.startswith(pref):
            return docs_root / rel
    return docs_root / "skills"

def main() -> int:
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    docs = repo_root / "docs"

    class_dir = docs / "classes"
    instructor_dir = docs / "instructor-guides"

    files: List[pathlib.Path] = []
    files += list(iter_md_files(class_dir))
    files += list(iter_md_files(instructor_dir))

    referenced: Set[str] = set()
    for f in files:
        try:
            txt = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            txt = f.read_text(encoding="utf-8", errors="ignore")
        referenced |= parse_skill_ids(txt)

    missing: List[Tuple[str, pathlib.Path]] = []
    for sid in sorted(referenced):
        folder = folder_for(sid, docs)
        expected = folder / f"{sid}.md"
        if not expected.exists():
            missing.append((sid, expected))

    if missing:
        print("ERROR: missing skill files:")
        for sid, path in missing:
            rel = path.relative_to(repo_root) if path.is_absolute() else path
            print(f"  - {sid}: expected {rel}")
        return 1

    print("OK: all referenced SKILL_IDs exist.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
