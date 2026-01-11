#!/usr/bin/env python3
"""Generate a human-friendly catalog page from artifacts/oda_catalog.sqlite.

Outputs:
- docs/reference/catalog.md (index)
- docs/reference/catalog/<kind>.md (per-kind tables)

Design goals:
- deterministic output (stable ordering)
- small, readable markdown
- no third-party deps

Run:
  python3 scripts/sqlite_to_catalog_md.py
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from collections import Counter, defaultdict
import re

REPO_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = REPO_ROOT / "artifacts" / "oda_catalog.sqlite"
OUT_PATH = REPO_ROOT / "docs" / "reference" / "catalog.md"
OUT_DIR = REPO_ROOT / "docs" / "reference" / "catalog"


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or "kind"


def q(conn: sqlite3.Connection, sql: str, params: tuple = ()):
    cur = conn.execute(sql, params)
    return cur.fetchall()


def main() -> int:
    if not DB_PATH.exists():
        raise SystemExit(f"Missing DB: {DB_PATH}")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))
    rows = q(
        conn,
        "SELECT path, title, kind, status, dtype, size_chars, sha256 FROM docs ORDER BY kind, dtype, status, path",
    )

    total = len(rows)
    kind_c = Counter(r[2] for r in rows)
    status_c = Counter(r[3] for r in rows)
    dtype_c = Counter(r[4] for r in rows)

    # Group by kind for readable sections
    by_kind: dict[str, list[tuple]] = defaultdict(list)
    for r in rows:
        by_kind[r[2]].append(r)

    lines: list[str] = []
    lines.append("# Catalog (SQLite-backed)")
    lines.append("")
    lines.append("This page is generated from the canonical SQLite catalog:")
    lines.append("")
    lines.append(f"- **Database:** `{DB_PATH.as_posix()}`")
    lines.append("- **Integrity:** `artifacts/manifest.sha256` (SHA-256)")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total docs indexed: **{total}**")

    def bullets(title: str, counter: Counter):
        lines.append(f"- {title}:")
        for k, v in sorted(counter.items(), key=lambda kv: (-kv[1], str(kv[0]))):
            lines.append(f"  - `{k}`: **{v}**")

    bullets("By kind", kind_c)
    bullets("By status", status_c)
    bullets("By dtype", dtype_c)

    lines.append("")
    lines.append("## Index (split by kind)")
    lines.append("")
    lines.append("This index links to smaller, per-kind tables to avoid doc truncation limits.")
    lines.append("")

    # Create stable slugs (with collision handling)
    kind_to_slug: dict[str, str] = {}
    used: Counter = Counter()
    for kind in sorted(by_kind.keys()):
        base = slugify(kind)
        used[base] += 1
        slug = base if used[base] == 1 else f"{base}-{used[base]}"
        kind_to_slug[kind] = slug

    for kind in sorted(by_kind.keys()):
        slug = kind_to_slug[kind]
        rel = f"catalog/{slug}.md"
        lines.append(f"- [{kind}]({rel})")

    # Write per-kind pages (tables)
    for kind in sorted(by_kind.keys()):
        slug = kind_to_slug[kind]
        p = OUT_DIR / f"{slug}.md"
        k_lines: list[str] = []
        k_lines.append(f"# Catalog — {kind}")
        k_lines.append("")
        k_lines.append("Generated from the canonical SQLite catalog:")
        k_lines.append("")
        k_lines.append(f"- **Database:** `{DB_PATH.as_posix()}`")
        k_lines.append("")
        k_lines.append("| Title | Type | Status | Size (chars) | Hash | Path |")
        k_lines.append("|---|---|---|---:|---|---|")
        for path, title, _kind, status, dtype, size_chars, sha256 in by_kind[kind]:
            md_path = path
            short_hash = sha256[:12]
            k_lines.append(
                f"| {title} | `{dtype}` | `{status}` | {size_chars} | `{short_hash}…` | [{md_path}]({md_path}) |"
            )
        k_lines.append("")
        p.write_text("\n".join(k_lines) + "\n", encoding="utf-8")

    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
