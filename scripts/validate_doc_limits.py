#!/usr/bin/env python3
"""Validate markdown document length limits to avoid 'turncated' (truncated) copy/paste issues.

What it does
- Enforces max characters and max lines per doc category (skills/manuals/etc.)
- Emits warnings when docs approach the cap (modularity nudge)
- Categories are defined in doc-limits.yml at repo root

Usage
  python3 scripts/validate_doc_limits.py
  python3 scripts/validate_doc_limits.py --report
  python3 scripts/validate_doc_limits.py --fail-on-warn
"""

from __future__ import annotations

import argparse
import fnmatch
import os
from pathlib import Path
from typing import List, Optional, Tuple

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "doc-limits.yml"


def read_text_safe(path: Path) -> str:
    # Enforce UTF-8; replace errors so the validator can't crash on a weird byte.
    return path.read_text(encoding="utf-8", errors="replace")


def glob_match_any(rel_path: str, patterns: List[str]) -> bool:
    return any(fnmatch.fnmatch(rel_path, pat) for pat in patterns)


def pick_rule(rel_path: str, rules: List[dict]) -> Optional[dict]:
    for rule in rules:
        globs = rule.get("globs", [])
        if any(fnmatch.fnmatch(rel_path, pat) for pat in globs):
            return rule
    return None


def iter_markdown_files() -> List[Path]:
    docs_dir = REPO_ROOT / "docs"
    if not docs_dir.exists():
        return []
    return [p for p in docs_dir.rglob("*.md") if p.is_file()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", action="store_true", help="Print top 20 largest docs even if passing.")
    parser.add_argument(
        "--fail-on-warn",
        action="store_true",
        help="Exit non-zero if any doc crosses the warn_ratio threshold.",
    )
    args = parser.parse_args()

    if not CONFIG_PATH.exists():
        raise SystemExit(f"Missing config: {CONFIG_PATH}")

    cfg = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}
    defaults = cfg.get("defaults", {})
    default_max_chars = int(defaults.get("max_chars", 20000))
    default_max_lines = int(defaults.get("max_lines", 650))
    default_warn_ratio = float(defaults.get("warn_ratio", 0.85))

    rules = cfg.get("rules", [])
    overrides = cfg.get("overrides", [])
    exclude_globs = cfg.get("exclude_globs", [])

    violations: List[str] = []
    warnings: List[str] = []
    sizes: List[Tuple[int, int, str]] = []  # chars, lines, rel_path

    for path in iter_markdown_files():
        rel_path = str(path.relative_to(REPO_ROOT)).replace(os.sep, "/")

        if glob_match_any(rel_path, exclude_globs):
            continue

        text = read_text_safe(path)
        chars = len(text)
        lines = text.count("\n") + 1
        sizes.append((chars, lines, rel_path))

        # Per-file overrides (exact path match) beat category rules.
        ov = next((o for o in overrides if o.get("path") == rel_path), None)
        if ov:
            rule_name = f"override:{ov.get('name','custom')}"
            max_chars = int(ov.get("max_chars", default_max_chars))
            max_lines = int(ov.get("max_lines", default_max_lines))
            warn_ratio = float(ov.get("warn_ratio", default_warn_ratio))
        else:
            rule = pick_rule(rel_path, rules)
            rule_name = (rule or {}).get("name", "default")
            max_chars = int((rule or {}).get("max_chars", default_max_chars))
            max_lines = int((rule or {}).get("max_lines", default_max_lines))
            warn_ratio = float((rule or {}).get("warn_ratio", default_warn_ratio))

        # Hard violations
        too_chars = chars > max_chars
        too_lines = lines > max_lines
        if too_chars or too_lines:
            msg_parts = [f"[{rule_name}] {rel_path}:"]
            if too_chars:
                msg_parts.append(f"chars {chars:,} > {max_chars:,}")
            if too_lines:
                msg_parts.append(f"lines {lines:,} > {max_lines:,}")
            msg_parts.append("Fix: split into smaller docs (recommended: split at H2 '##' headings).")
            msg_parts.append("If it's raw source material, move it under docs/reference/extracts/ or exports.")
            violations.append(" ".join(msg_parts))
            continue

        # Soft warnings (modularity nudge)
        if max_chars > 0 and max_lines > 0:
            char_ratio = chars / max_chars
            line_ratio = lines / max_lines
            ratio = max(char_ratio, line_ratio)
            if ratio >= warn_ratio:
                warnings.append(
                    f"[{rule_name}] {rel_path}: {chars:,}/{max_chars:,} chars, {lines:,}/{max_lines:,} lines "
                    f"(>= {warn_ratio:.2f} cap). Consider splitting into modules."
                )

    if args.report or warnings or violations:
        sizes_sorted = sorted(sizes, reverse=True)[:20]
        print("\nTop docs by length (chars):")
        for chars, lines, rel in sizes_sorted:
            print(f"  {chars:>7,} chars | {lines:>5,} lines | {rel}")
        print("")

    if warnings:
        print("DOC LIMIT WARNINGS (modularity nudge):")
        for w in warnings:
            print(f"  - {w}")
        print("")

    if violations:
        print("DOC LIMIT VIOLATIONS:")
        for v in violations:
            print(f"  - {v}")
        print("\nConfig: doc-limits.yml")
        return 1

    if warnings and args.fail_on_warn:
        return 2

    print("Doc limits: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
