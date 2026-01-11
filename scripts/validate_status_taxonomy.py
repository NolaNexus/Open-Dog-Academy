#!/usr/bin/env python3
"""Validate doc Status taxonomy across ODA.

ODA uses a *docs-as-code* approach: docs are versioned, reviewed, and validated
in CI the same way code is. A small, strict Status taxonomy makes it possible
to:

- filter what's ready to teach vs still being built
- enforce consistency across doc types
- enable automation (indexes, release bundles, curriculum paths)

Status taxonomy (strict)
- stub   : placeholder/skeleton, may be incomplete or missing prerequisites
- draft  : usable for trials, but may still change significantly
- stable : ready for general use; edits are incremental not structural

Validated zones
- docs/_atoms/** (expects atom headers incl. Status)
- docs/skills/** (expects **Type**, **Status**, **Last updated**)
- docs/classes/**, docs/instructor-guides/**, docs/manuals/**, docs/lab/**,
  docs/ops/**, docs/standards/** (expects Status near top)

Non-goals
- This script does not enforce Type taxonomies (yet).
- docs/reference/** is excluded (often raw/source material).

Usage
  python3 scripts/validate_status_taxonomy.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ALLOWED = {"stub", "draft", "stable"}

RE_STATUS_ANY = re.compile(r"^(?:\*\*Status:\*\*|Status:)\s*(.+?)\s*$", re.MULTILINE)
RE_SKILL_TYPE = re.compile(r"^\*\*Type:\*\*\s+.+?\s*$", re.MULTILINE)
RE_SKILL_STATUS = re.compile(r"^\*\*Status:\*\*\s*(.+?)\s*$", re.MULTILINE)
RE_SKILL_LAST = re.compile(r"^\*\*Last updated:\*\*\s*(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)


def _read_head(path: Path, n_lines: int = 60) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    return "\n".join(text.splitlines()[:n_lines])


def _extract_status(head: str) -> str | None:
    m = RE_STATUS_ANY.search(head)
    if not m:
        return None
    return m.group(1).strip()


def _normalize_for_compare(status: str) -> str:
    # No clever parsing: status must be exact.
    return status.strip().lower()


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    docs = repo_root / "docs"

    zones = [
        (docs / "_atoms", "atom"),
        (docs / "skills", "skill"),
        (docs / "classes", "generic"),
        (docs / "instructor-guides", "generic"),
        (docs / "manuals", "generic"),
        (docs / "lab", "generic"),
        (docs / "ops", "generic"),
        (docs / "standards", "generic"),
    ]

    problems: list[str] = []

    for folder, kind in zones:
        if not folder.exists():
            continue

        for f in sorted(folder.rglob("*.md")):
            rel = f.relative_to(repo_root).as_posix()

            # Exempt known generated/indexy pages.
            if rel.startswith("docs/indexes/"):
                continue
            if rel.startswith("docs/_atoms/") and f.name == "index.md":
                continue
            if rel.startswith("docs/lab/") and f.name == "index.md":
                # still validate lab/index.md (it's a real landing page)
                pass

            head = _read_head(f)

            if kind == "skill":
                if not RE_SKILL_TYPE.search(head):
                    problems.append(f"Missing **Type:** header in skill: {rel}")
                ms = RE_SKILL_STATUS.search(head)
                if not ms:
                    problems.append(f"Missing **Status:** header in skill: {rel}")
                else:
                    raw = ms.group(1).strip()
                    norm = _normalize_for_compare(raw)
                    if norm not in ALLOWED:
                        problems.append(
                            f"Invalid Status in skill {rel}: '{raw}' (allowed: {', '.join(sorted(ALLOWED))})"
                        )

                if not RE_SKILL_LAST.search(head):
                    problems.append(
                        f"Missing or malformed **Last updated:** (YYYY-MM-DD) in skill: {rel}"
                    )
                continue

            # generic + atom
            status = _extract_status(head)
            if status is None:
                problems.append(f"Missing Status in {rel}")
                continue
            norm = _normalize_for_compare(status)
            if norm not in ALLOWED:
                problems.append(
                    f"Invalid Status in {rel}: '{status}' (allowed: {', '.join(sorted(ALLOWED))})"
                )

    if problems:
        print("Status taxonomy validation failed:\n")
        for p in problems:
            print(f"- {p}")
        print("\nFix guidance:")
        print("- Use exactly one of: stub | draft | stable")
        print("- For skills, ensure headers include: **Type:**, **Status:**, **Last updated:**")
        return 1

    print("OK: status taxonomy")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
