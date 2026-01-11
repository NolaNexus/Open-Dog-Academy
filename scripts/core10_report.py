#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Report progress on the "core 10" skills conversion milestone.

Reads docs/paths/_config/core10.yml and reports:
  - status
  - include count (proxy for assembly-ness)
  - pass criteria section present
  - safety gating include present

Usage:
  python3 scripts/core10_report.py
  python3 scripts/core10_report.py --write
  python3 scripts/core10_report.py --check   # optional gating
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from _lib.fs import write_text

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS = REPO_ROOT / "docs"
CONFIG = DOCS / "paths" / "_config" / "core10.yml"
OUT = DOCS / "reference" / "reports" / "core10-report.md"

INCLUDE_RE = re.compile(r"^--8<--\s+\".+\"$", re.M)
STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(.+?)\s*$", re.M)
PASS_RE = re.compile(r"^##\s+Pass criteria\b", re.M)
SAFETY_INCLUDE_RE = re.compile(r"_atoms/safety/safety-gating-", re.M)


@dataclass
class Row:
    skill_id: str
    file_rel: str
    status: str
    includes: int
    has_pass: bool
    has_safety: bool


def find_skill(skill_id: str) -> Path | None:
    hits = list((DOCS / "skills").rglob(f"{skill_id}.md"))
    if not hits:
        return None
    hits.sort(key=lambda p: len(str(p)))
    return hits[0]


def parse_skill(path: Path) -> tuple[str, int, bool, bool]:
    txt = path.read_text(encoding="utf-8")
    status = "unknown"
    m = STATUS_RE.search(txt)
    if m:
        status = m.group(1).strip()
    includes = len(INCLUDE_RE.findall(txt))
    has_pass = bool(PASS_RE.search(txt))
    has_safety = bool(SAFETY_INCLUDE_RE.search(txt))
    return status, includes, has_pass, has_safety


def make_table(rows: list[Row]) -> str:
    lines = []
    lines.append("| Skill | Status | Assembly includes | Pass criteria | Safety gating | File |")
    lines.append("|---|---|---:|---|---|---|")
    for r in rows:
        pc = "✅" if r.has_pass else "❌"
        sg = "✅" if r.has_safety else "❌"
        lines.append(f"| `{r.skill_id}` | {r.status} | {r.includes} | {pc} | {sg} | `{r.file_rel}` |")
    return "\n".join(lines)


def build_report(rows: list[Row]) -> str:
    total = len(rows)
    assemblies = sum(1 for r in rows if r.includes >= 3)  # heuristic
    ready = sum(1 for r in rows if (r.includes >= 3 and r.has_pass and r.has_safety))
    missing = [r.skill_id for r in rows if r.file_rel == "MISSING"]

    lines = []
    lines.append("# Core 10 conversion report")
    lines.append("")
    lines.append("Status: draft")
    lines.append("")
    lines.append("This report tracks the M2 deliverable: converting the **core 10** skills into atom-powered assemblies.")
    lines.append("")
    lines.append(f"- Total: **{total}**")
    lines.append(f"- Assembly-ish (≥3 includes): **{assemblies}**")
    lines.append(f"- Assembly + pass criteria + safety gating: **{ready}**")
    if missing:
        lines.append(f"- Missing files: {', '.join(f'`{m}`' for m in missing)}")
    lines.append("")
    lines.append(make_table(rows))
    lines.append("")
    lines.append("## Suggested next conversions")
    lines.append("")
    todo = sorted(rows, key=lambda r: (r.includes, r.status, r.skill_id))
    for r in todo[:5]:
        if r.file_rel == "MISSING":
            continue
        lines.append(f"- `{r.skill_id}`: includes={r.includes}, pass={r.has_pass}, safety={r.has_safety}")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="Write docs/reference/reports/core10-report.md")
    ap.add_argument("--check", action="store_true", help="Exit nonzero if any core skill is missing pass criteria or safety gating.")
    args = ap.parse_args()

    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    core = cfg.get("core10", [])
    rows: list[Row] = []

    for item in core:
        sid = item.get("id") if isinstance(item, dict) else str(item)
        sid = str(sid)
        p = find_skill(sid)
        if not p:
            rows.append(Row(skill_id=sid, file_rel="MISSING", status="missing", includes=0, has_pass=False, has_safety=False))
            continue
        status, includes, has_pass, has_safety = parse_skill(p)
        rows.append(Row(
            skill_id=sid,
            file_rel=str(p.relative_to(DOCS)),
            status=status,
            includes=includes,
            has_pass=has_pass,
            has_safety=has_safety,
        ))

    report = build_report(rows)
    print(report)

    if args.write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        write_text(OUT, report, mode=0o644)
        print(f"Wrote: {OUT.relative_to(REPO_ROOT)}")

    if args.check:
        bad = [r for r in rows if not (r.has_pass and r.has_safety)]
        if bad:
            print("\nERROR: some core skills are missing pass criteria and/or safety gating.")
            for r in bad:
                print(f"- {r.skill_id}: pass={r.has_pass} safety={r.has_safety} file={r.file_rel}")
            return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
