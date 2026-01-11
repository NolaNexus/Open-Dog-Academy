#!/usr/bin/env python3
"""
Scan docs/classes and docs/instructor-guides for SKILL_IDs and ensure a skill file exists
for each one. Missing files are created from a minimal template.

Usage:
  python3 scripts/generate_skill_files.py
"""

from __future__ import annotations

import pathlib
import re
from typing import Dict, Iterable, Set

from _lib.fs import write_text

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

TEMPLATE = """# {skill_id} — {title}

**Type:** skill reference  
**Status:** stub  
**Last updated:** {today}

---

## Definition
TODO

## Setup
TODO

## Steps
TODO

## Pass criteria
TODO

## Common pitfalls + fixes
TODO

## Related skills
- TODO
"""

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

def title_from_id(skill_id: str) -> str:
    return skill_id.replace("_", " ").title()

def main() -> int:
    repo_root = pathlib.Path(__file__).resolve().parents[1]
    docs = repo_root / "docs"

    class_dir = docs / "classes"
    instructor_dir = docs / "instructor-guides"

    referenced: Set[str] = set()
    for f in list(iter_md_files(class_dir)) + list(iter_md_files(instructor_dir)):
        try:
            txt = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            txt = f.read_text(encoding="utf-8", errors="ignore")
        referenced |= parse_skill_ids(txt)

    import datetime as _dt
    today = _dt.date.today().isoformat()

    created = 0
    for sid in sorted(referenced):
        folder = folder_for(sid, docs)
        folder.mkdir(parents=True, exist_ok=True)
        out = folder / f"{sid}.md"
        if not out.exists():
            write_text(out, TEMPLATE.format(skill_id=sid, title=title_from_id(sid), today=today), mode=0o644)
            created += 1

    print(f"Done. Created {created} new skill file(s).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
