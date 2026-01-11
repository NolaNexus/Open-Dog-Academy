#!/usr/bin/env python3
"""Suggest how to split a long Markdown doc into smaller modules.

This is a *planning tool* to support the repo's modularity theme and avoid truncation issues.
It does NOT modify files by default.

How it works
- Looks up the doc's configured limits from `doc-limits.yml`
- Finds H2 sections (lines starting with '## ')
- Proposes module boundaries so each part stays comfortably under a target ratio of the caps

Usage:
  python3 scripts/suggest_doc_split.py docs/manuals/some_doc.md
  python3 scripts/suggest_doc_split.py docs/manuals/some_doc.md --target-ratio 0.70

Notes:
- Best practice: split at H2 boundaries and create an index page that links the parts.
- If the doc is mostly raw sources, prefer moving content into `docs/reference/extracts/` or `docs/reference/exports_YYYY-MM-DD/`.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

import yaml


DOC_LIMITS_FILE = Path(__file__).resolve().parents[1] / "doc-limits.yml"


@dataclass
class Limits:
    max_chars: int
    max_lines: int


def load_limits_config() -> dict:
    if not DOC_LIMITS_FILE.exists():
        raise SystemExit(f"Missing limits config: {DOC_LIMITS_FILE}")
    return yaml.safe_load(DOC_LIMITS_FILE.read_text(encoding="utf-8"))


def match_limits(doc_path: Path, cfg: dict) -> Limits:
    defaults = cfg.get("defaults", {})
    default_limits = Limits(
        max_chars=int(defaults.get("max_chars", 20000)),
        max_lines=int(defaults.get("max_lines", 650)),
    )

    rel = doc_path.as_posix()
    rules = cfg.get("rules", [])

    def glob_match(globs: List[str]) -> bool:
        for g in globs:
            # Path.match is anchored; we want repo-relative matching
            if Path(rel).match(g.replace("**/", "")) or Path(rel).match(g):
                return True
        return False

    for rule in rules:
        globs = rule.get("globs", [])
        if globs and glob_match(globs):
            return Limits(
                max_chars=int(rule.get("max_chars", default_limits.max_chars)),
                max_lines=int(rule.get("max_lines", default_limits.max_lines)),
            )

    return default_limits


def find_h2_sections(lines: List[str]) -> List[Tuple[int, str]]:
    sections: List[Tuple[int, str]] = []
    for i, line in enumerate(lines):
        if re.match(r"^##\s+", line):
            title = re.sub(r"^##\s+", "", line).strip()
            sections.append((i, title))
    return sections


def propose_chunks(lines: List[str], section_starts: List[Tuple[int, str]], char_cap: int, line_cap: int) -> List[Tuple[int, int, str]]:
    """Return [(start_line, end_line_exclusive, label)]"""
    if not section_starts:
        return [(0, len(lines), "part-01")]

    # Create boundaries including EOF
    starts = [s for s, _ in section_starts]
    titles = [t for _, t in section_starts]
    starts.append(len(lines))
    titles.append("")

    chunks: List[Tuple[int, int, str]] = []
    chunk_start = 0
    part = 1

    def within_caps(s: int, e: int) -> bool:
        seg_lines = lines[s:e]
        seg_line_count = len(seg_lines)
        seg_char_count = sum(len(x) for x in seg_lines)
        return seg_line_count <= line_cap and seg_char_count <= char_cap

    # Build chunks by adding one H2 section at a time
    for idx in range(len(section_starts)):
        next_start = starts[idx + 1]

        # If adding this section would exceed, cut before it (but only if chunk isn't empty)
        if not within_caps(chunk_start, next_start) and chunk_start != starts[idx]:
            label = f"part-{part:02d}"
            chunks.append((chunk_start, starts[idx], label))
            part += 1
            chunk_start = starts[idx]

    # Remainder
    label = f"part-{part:02d}"
    chunks.append((chunk_start, len(lines), label))
    return chunks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("doc", type=str, help="Path to a Markdown file under docs/")
    ap.add_argument("--target-ratio", type=float, default=0.70, help="Aim to keep each part under this fraction of caps (default: 0.70)")
    args = ap.parse_args()

    doc_path = Path(args.doc)
    if not doc_path.exists():
        print(f"File not found: {doc_path}")
        return 2

    cfg = load_limits_config()
    limits = match_limits(doc_path, cfg)

    lines = doc_path.read_text(encoding="utf-8").splitlines(keepends=True)
    total_chars = sum(len(x) for x in lines)
    total_lines = len(lines)

    target_char_cap = int(limits.max_chars * args.target_ratio)
    target_line_cap = int(limits.max_lines * args.target_ratio)

    h2s = find_h2_sections(lines)
    chunks = propose_chunks(lines, h2s, target_char_cap, target_line_cap)

    print(f"Doc: {doc_path}")
    print(f"Current: {total_chars} chars / {total_lines} lines")
    print(f"Limits:  {limits.max_chars} chars / {limits.max_lines} lines")
    print(f"Target per part (~{int(args.target_ratio*100)}%): {target_char_cap} chars / {target_line_cap} lines\n")

    if not h2s:
        print("No H2 sections found (##). Recommendation: add H2 headings, then split.")
        return 0

    # Report chunk stats
    for (s, e, label) in chunks:
        seg = lines[s:e]
        seg_chars = sum(len(x) for x in seg)
        seg_lines = len(seg)
        # try to label from first H2 title in the chunk
        first_title = None
        for i, title in h2s:
            if s <= i < e:
                first_title = title
                break
        human = first_title or label
        print(f"- {label}: lines {s+1}-{e} | {seg_chars} chars | {seg_lines} lines | starts: {human}")

    print("\nRecommended split pattern:")
    print("1) Create a folder next to the doc (same stem).\n2) Move each part into that folder as 01-*, 02-* files.\n3) Turn the original file into an index that links the parts.\n4) Prefer atoms for any content repeated across 2+ docs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
