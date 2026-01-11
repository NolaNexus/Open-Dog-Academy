#!/usr/bin/env python3
"""Rebuild artifacts/oda_catalog.sqlite from the current docs/ tree.

This is the "authoritative index" generator. It is intentionally conservative:
- reads only local files
- generates deterministic output
- stores sha256 + size_chars for integrity checks

Run:
  python3 scripts/rebuild_catalog_sqlite.py

Then:
  make catalog
  make verify-catalog

NOTE: If you treat the SQLite DB as canonical for handoffs, rebuild it whenever docs change.
"""

from __future__ import annotations

import hashlib
import os
import re
import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = REPO_ROOT / "docs"
DB_PATH = REPO_ROOT / "artifacts" / "oda_catalog.sqlite"

INCLUDE_RE = re.compile(r"--8<--\s+[\"']([^\"']+)[\"']")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def clean_value(s: str) -> str:
    s = s.strip()
    # strip common markdown wrappers
    s = s.strip("` ")
    s = s.strip("*")
    s = s.replace("**", "").strip()
    return s


def infer_kind(rel_path: str) -> str:
    # rel_path is relative to docs/
    parts = rel_path.split("/")
    if not parts:
        return "doc"
    head = parts[0]
    if head == "_atoms":
        return "atom"
    if head == "skills":
        return "skill"
    if head == "classes":
        return "class"
    if head == "instructor-guides":
        return "instructor-guide"
    if head == "manuals":
        return "manual"
    if head == "standards":
        return "standard"
    if head == "ops":
        return "ops"
    if head == "research":
        return "research"
    if head == "lab":
        return "lab"
    if head == "reference":
        return "reference"
    if head == "indexes":
        return "index"
    if head == "paths":
        return "path"
    return "doc"


def extract_title(rel_path: str, text: str, kind: str) -> str:
    stem = Path(rel_path).stem
    if kind == "atom":
        return stem
    # first Markdown H1
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return stem


def extract_meta(text: str) -> tuple[str, str]:
    """Return (dtype, status). Defaults to ('unknown','unknown').

    Supports:
    - `Type: ...` / `Status: ...`
    - `**Type:** ...` / `**Status:** ...`
    """
    head = "\n".join(text.splitlines()[:80])

    dtype = "unknown"
    status = "unknown"

    # Try plain
    m = re.search(r"^Type:\s*(.+)$", head, flags=re.MULTILINE)
    if m:
        dtype = clean_value(m.group(1))
    m = re.search(r"^Status:\s*(.+)$", head, flags=re.MULTILINE)
    if m:
        status = clean_value(m.group(1))

    # Try bold markdown
    m = re.search(r"^\*\*Type:\*\*\s*(.+)$", head, flags=re.MULTILINE)
    if m:
        dtype = clean_value(m.group(1))
    m = re.search(r"^\*\*Status:\*\*\s*(.+)$", head, flags=re.MULTILINE)
    if m:
        status = clean_value(m.group(1))

    return dtype, status


def iter_md_files() -> list[Path]:
    files: list[Path] = []
    for p in DOCS_ROOT.rglob("*.md"):
        rel = p.relative_to(DOCS_ROOT).as_posix()
        # ignore generated catalog page (it is derived from the DB)
        if rel == "reference/catalog.md":
            continue
        # ignore exports/chunks
        if rel.startswith("reference/exports_"):
            continue
        if rel.startswith("reference/extracts/"):
            # extracts can be large; keep them out of the canonical catalog by default
            continue
        files.append(p)
    return sorted(files, key=lambda x: x.relative_to(DOCS_ROOT).as_posix())


def main() -> int:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    tmp = DB_PATH.with_suffix(".sqlite.tmp")
    if tmp.exists():
        tmp.unlink()

    conn = sqlite3.connect(str(tmp))
    conn.execute("PRAGMA journal_mode=DELETE")
    conn.execute(
        """
        CREATE TABLE docs (
          path TEXT PRIMARY KEY,
          title TEXT NOT NULL,
          kind TEXT NOT NULL,
          status TEXT NOT NULL,
          dtype TEXT NOT NULL,
          size_chars INTEGER NOT NULL,
          sha256 TEXT NOT NULL
        );
        """
    )
    conn.execute(
        """
        CREATE TABLE includes (
          from_path TEXT NOT NULL,
          include_path TEXT NOT NULL,
          PRIMARY KEY (from_path, include_path)
        );
        """
    )

    md_files = iter_md_files()

    docs_rows = []
    inc_rows = []

    for p in md_files:
        rel = p.relative_to(DOCS_ROOT).as_posix()
        b = p.read_bytes()
        sha = sha256_bytes(b)
        try:
            text = b.decode("utf-8")
        except UnicodeDecodeError:
            # ODA policy: markdown should be UTF-8
            text = b.decode("utf-8", errors="replace")
        size_chars = len(text)

        kind = infer_kind(rel)
        dtype, status = extract_meta(text)
        title = extract_title(rel, text, kind)

        docs_rows.append((rel, title, kind, status, dtype, size_chars, sha))

        # includes via pymdownx.snippets syntax
        for m in INCLUDE_RE.finditer(text):
            inc_path = m.group(1).strip()
            inc_rows.append((rel, inc_path))

    conn.executemany(
        "INSERT INTO docs(path,title,kind,status,dtype,size_chars,sha256) VALUES(?,?,?,?,?,?,?)",
        docs_rows,
    )
    conn.executemany(
        "INSERT OR IGNORE INTO includes(from_path,include_path) VALUES(?,?)",
        inc_rows,
    )
    conn.commit()
    conn.close()

    os.replace(tmp, DB_PATH)
    print(f"Rebuilt {DB_PATH} ({len(docs_rows)} docs, {len(set(inc_rows))} includes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
