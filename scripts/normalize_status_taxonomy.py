#!/usr/bin/env python3
"""Normalize ODA Status values to the strict taxonomy.

This is a *one-shot maintenance* script that:
- rewrites known legacy Status variants (e.g., "draft (modular refactor)")
  to their canonical value (e.g., "draft")
- upgrades legacy PLAY_* skill stubs to the standard skill header format
- inserts missing Status lines in a handful of older docs (default: draft)

Usage
  python3 scripts/normalize_status_taxonomy.py

Note
  This script edits files in-place. Review the diff before committing.
"""

from __future__ import annotations

import re
from pathlib import Path

from _lib.fs import write_text


RE_STATUS_LINE = re.compile(r"^(\*\*Status:\*\*|Status:)\s*(.+?)\s*$", re.MULTILINE)


STATUS_REWRITES: dict[str, str] = {
    "draft (modular refactor)": "draft",
    "detailed draft (modular refactor)": "draft",
    "detailed draft (atoms-first)": "draft",
}


def rewrite_status_values(text: str) -> tuple[str, bool]:
    changed = False

    def _sub(m: re.Match) -> str:
        nonlocal changed
        prefix = m.group(1)
        raw = m.group(2).strip()
        replacement = STATUS_REWRITES.get(raw, raw)
        if replacement != raw:
            changed = True
        return f"{prefix} {replacement}"

    new = RE_STATUS_LINE.sub(_sub, text)
    return new, changed


def upgrade_legacy_play_skill(path: Path, text: str) -> tuple[str, bool]:
    """Convert legacy PLAY_* header into standard skill header.

    Legacy form:
      # PLAY_START
      Path: docs/skills/play/PLAY_START.md
      Status: stub
      Updated: 2026-01-10
    """
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        return text, False
    if len(lines) < 4:
        return text, False
    if not lines[1].startswith("Path: docs/skills/play/"):
        return text, False
    if not lines[2].startswith("Status:"):
        return text, False
    if not lines[3].startswith("Updated:"):
        return text, False

    title = lines[0].strip()
    status = lines[2].split(":", 1)[1].strip() or "stub"
    updated = lines[3].split(":", 1)[1].strip() or "2026-01-10"

    body = "\n".join(lines[4:]).lstrip("\n")
    new = (
        f"{title}\n\n"
        f"**Type:** skill reference\n"
        f"**Status:** {status}\n"
        f"**Last updated:** {updated}\n\n"
        f"---\n\n{body}\n"
    )
    return new, True


def insert_status_after_h1(text: str, status: str = "draft") -> tuple[str, bool]:
    lines = text.splitlines()
    if not lines:
        return text, False
    if not lines[0].startswith("# "):
        return text, False
    head = "\n".join(lines[:60])
    if RE_STATUS_LINE.search(head):
        return text, False

    # Insert right after the H1 line.
    new_lines = [lines[0], f"Status: {status}"] + lines[1:]
    return "\n".join(new_lines) + "\n", True


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    docs = repo_root / "docs"

    # (1) Normalize Status values wherever they appear.
    changed_files: list[str] = []
    for f in sorted(docs.rglob("*.md")):
        rel = f.relative_to(repo_root).as_posix()
        if rel.startswith("docs/indexes/"):
            continue
        if rel.startswith("docs/reference/"):
            continue

        text = f.read_text(encoding="utf-8", errors="replace")
        new = text
        changed = False

        # Upgrade legacy PLAY_* skill stubs
        if rel.startswith("docs/skills/play/PLAY_"):
            new, did = upgrade_legacy_play_skill(f, new)
            changed = changed or did

        # Rewrite known legacy status variants
        new, did = rewrite_status_values(new)
        changed = changed or did

        # Insert missing Status lines in older docs (default: draft)
        if any(
            rel.startswith(p)
            for p in (
                "docs/classes/",
                "docs/instructor-guides/",
                "docs/manuals/",
                "docs/lab/",
                "docs/ops/",
                "docs/standards/",
            )
        ):
            new2, did2 = insert_status_after_h1(new, status="draft")
            new = new2
            changed = changed or did2

        if changed and new != text:
            write_text(f, new, mode=0o644)
            changed_files.append(rel)

    print(f"Normalized status taxonomy. Updated {len(changed_files)} files.")
    for r in changed_files[:25]:
        print(f"- {r}")
    if len(changed_files) > 25:
        print(f"... and {len(changed_files) - 25} more")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
