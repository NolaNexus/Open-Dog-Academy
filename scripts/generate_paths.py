#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate curated learning path pages from YAML configs.

Why:
  - Keeps "paths" pages from drifting when files move.
  - Makes the recommended curriculum editable in one small YAML file.

Usage:
  python3 scripts/generate_paths.py
  python3 scripts/generate_paths.py --check
"""

from __future__ import annotations

import argparse
from pathlib import Path

from _lib.fs import write_text

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS = REPO_ROOT / "docs"
CONFIG = DOCS / "paths" / "_config" / "level-0-to-2.yml"
OUT = DOCS / "paths" / "level-0-to-2.md"


def find_skill_doc(skill_id: str) -> Path | None:
    hits = list((DOCS / "skills").rglob(f"{skill_id}.md"))
    if not hits:
        return None
    hits.sort(key=lambda p: len(str(p)))
    return hits[0]


def md_link(title: str, rel_path_from_paths: Path) -> str:
    return f"[{title}]({rel_path_from_paths.as_posix()})"


def build() -> str:
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    title = str(cfg["title"]).strip()
    status = str(cfg.get("status", "draft")).strip()
    goal = str(cfg.get("goal", "")).strip()

    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"Status: {status}")
    if goal:
        lines.append("")
        lines.append(f"Goal: {goal}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## How to use this path")
    lines.append("")
    for item in cfg.get("how_to_use", []):
        lines.append(f"- {item}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for lvl in cfg.get("levels", []):
        n = int(lvl["level"])
        name = str(lvl["name"])
        lines.append(f"## Level {n} — {name}")
        lines.append("")

        ig = lvl.get("instructor_guide")
        if ig:
            rel = Path("..") / str(ig)
            lines.append("### Group script")
            display_name = f"Level {n} — {name.split(' (')[0]}"
            lines.append(f"- Instructor guide: {md_link(display_name, rel)}")
            lines.append("")

        skills = lvl.get("skills", [])
        if skills:
            lines.append("### Core skills")
            for sid in skills:
                sid = str(sid)
                p = find_skill_doc(sid)
                if not p:
                    lines.append(f"- `{sid}` (MISSING FILE)")
                    continue
                rel = Path("..") / p.relative_to(DOCS)
                lines.append(f"- {md_link(sid, rel)}")
            lines.append("")

        atoms = lvl.get("atoms", [])
        if atoms:
            lines.append("### Atoms you will reuse constantly")
            for a in atoms:
                rel = Path("..") / str(a["path"])
                lines.append(f"- {md_link(str(a['title']), rel)}")
            lines.append("")

        notes = lvl.get("notes", [])
        if notes:
            lines.append("### Notes")
            for note in notes:
                lines.append(f"- {note}")
            lines.append("")

        lines.append("---")
        lines.append("")

    branches = cfg.get("branches", [])
    if branches:
        lines.append("## When to branch")
        lines.append("")
        for b in branches:
            when = str(b["when"])
            title2 = str(b["title"])
            rel = Path("..") / str(b["go_to"])
            lines.append(f"- {when}: {md_link(title2, rel)}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="Exit nonzero if output is stale.")
    args = ap.parse_args()

    content = build()

    if args.check:
        if not OUT.exists():
            print(f"ERROR: missing generated file: {OUT.relative_to(REPO_ROOT)}")
            return 2
        current = OUT.read_text(encoding="utf-8")
        if current != content:
            print("ERROR: learning path page is stale. Run: python3 scripts/generate_paths.py")
            return 2
        return 0

    write_text(OUT, content, mode=0o644)
    print(f"Wrote: {OUT.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
