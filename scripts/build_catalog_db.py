#!/usr/bin/env python3
"""Build a derived catalog (SQLite + JSONL) from docs/**/*.md.

Mantra
------
Markdown is truth.
The database is a *derived index* to power search, QA, and AI handoff exports.

This script intentionally has no third‑party dependencies.

Outputs
-------
- artifacts/oda_catalog.sqlite
- artifacts/oda_catalog.jsonl

Exit codes
----------
0 success
2 input error
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

INCLUDE_RE = re.compile(r'^\s*--8<--\s+"([^"]+)"\s*$')
H1_RE = re.compile(r'^#\s+(.+?)\s*$')
# Matches: **Status:** draft  OR  Status: draft
KV_RE = re.compile(r'^(?:\*\*)?(Status|Type)(?:\*\*)?:\s*(.+?)\s*$')


@dataclass(frozen=True)
class DocRow:
    path: str
    title: str
    kind: str
    status: str
    dtype: str
    size_chars: int
    sha256: str


def sha256_text(text: str) -> str:
    h = hashlib.sha256()
    h.update(text.encode('utf-8', errors='replace'))
    return h.hexdigest()


def guess_kind(rel_path: str) -> str:
    # Keep this conservative; it's a report label, not truth.
    p = rel_path.replace('\\', '/')
    if p.startswith('skills/'):
        return 'skill'
    if p.startswith('_atoms/'):
        return 'atom'
    if p.startswith('class-guides/'):
        return 'class_guide'
    if p.startswith('instructor-guides/'):
        return 'instructor_guide'
    if p.startswith('standards/'):
        return 'standard'
    if p.startswith('paths/'):
        return 'path'
    if p.startswith('manuals/'):
        return 'manual'
    if p.startswith('reference/'):
        return 'reference'
    return 'doc'


def parse_doc(text: str, rel_path: str) -> Tuple[str, str, str, List[str]]:
    """Return (title, status, dtype, includes)."""
    title = ''
    status = ''
    dtype = ''
    includes: List[str] = []

    # Title: first H1
    for line in text.splitlines():
        if not title:
            m = H1_RE.match(line)
            if m:
                title = m.group(1).strip()
        m2 = INCLUDE_RE.match(line)
        if m2:
            includes.append(m2.group(1).strip())

    # Metadata: scan first 60 lines only (fast + avoids false positives)
    for line in text.splitlines()[:60]:
        m = KV_RE.match(line.strip())
        if not m:
            continue
        k = m.group(1).lower()
        v = m.group(2).strip()
        if k == 'status' and not status:
            status = v
        elif k == 'type' and not dtype:
            dtype = v

    # Defaults
    if not title:
        title = Path(rel_path).stem
    if not status:
        status = 'unknown'
    if not dtype:
        dtype = 'unknown'

    return title, status, dtype, includes


def ensure_sqlite_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA journal_mode=WAL;
        PRAGMA synchronous=NORMAL;

        CREATE TABLE IF NOT EXISTS docs (
          path TEXT PRIMARY KEY,
          title TEXT NOT NULL,
          kind TEXT NOT NULL,
          status TEXT NOT NULL,
          dtype TEXT NOT NULL,
          size_chars INTEGER NOT NULL,
          sha256 TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS includes (
          from_path TEXT NOT NULL,
          include_path TEXT NOT NULL,
          PRIMARY KEY (from_path, include_path),
          FOREIGN KEY (from_path) REFERENCES docs(path) ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS idx_docs_kind ON docs(kind);
        CREATE INDEX IF NOT EXISTS idx_docs_status ON docs(status);
        CREATE INDEX IF NOT EXISTS idx_docs_dtype ON docs(dtype);
        """
    )


def iter_markdown_files(docs_root: Path) -> Iterable[Path]:
    for p in docs_root.rglob('*.md'):
        if p.is_file():
            yield p


def build_catalog(docs_root: Path, artifacts_dir: Path) -> Tuple[Path, Path]:
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    sqlite_path = artifacts_dir / 'oda_catalog.sqlite'
    jsonl_path = artifacts_dir / 'oda_catalog.jsonl'

    conn = sqlite3.connect(sqlite_path)
    try:
        ensure_sqlite_schema(conn)

        # Clear derived content (rebuild)
        conn.execute('DELETE FROM includes')
        conn.execute('DELETE FROM docs')

        jsonl_fp = jsonl_path.open('w', encoding='utf-8')
        try:
            for md in sorted(iter_markdown_files(docs_root)):
                rel = md.relative_to(docs_root).as_posix()
                text = md.read_text(encoding='utf-8', errors='replace')
                title, status, dtype, includes = parse_doc(text, rel)

                row = DocRow(
                    path=rel,
                    title=title,
                    kind=guess_kind(rel),
                    status=status,
                    dtype=dtype,
                    size_chars=len(text),
                    sha256=sha256_text(text),
                )

                conn.execute(
                    'INSERT INTO docs(path,title,kind,status,dtype,size_chars,sha256) VALUES (?,?,?,?,?,?,?)',
                    (row.path, row.title, row.kind, row.status, row.dtype, row.size_chars, row.sha256),
                )

                for inc in includes:
                    conn.execute(
                        'INSERT OR IGNORE INTO includes(from_path, include_path) VALUES (?,?)',
                        (row.path, inc),
                    )

                jsonl_fp.write(json.dumps({
                    'path': row.path,
                    'title': row.title,
                    'kind': row.kind,
                    'status': row.status,
                    'type': row.dtype,
                    'size_chars': row.size_chars,
                    'sha256': row.sha256,
                    'includes': includes,
                }, ensure_ascii=False) + '\n')

            conn.commit()
        finally:
            jsonl_fp.close()

    finally:
        conn.close()

    return sqlite_path, jsonl_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--docs-root', default='docs', help='Docs root (default: docs).')
    ap.add_argument('--artifacts', default='artifacts', help='Artifacts output dir (default: artifacts).')
    args = ap.parse_args()

    docs_root = Path(args.docs_root)
    if not docs_root.exists():
        print(f"Docs root not found: {docs_root}")
        return 2

    sqlite_path, jsonl_path = build_catalog(docs_root, Path(args.artifacts))
    print(f"Wrote SQLite: {sqlite_path}")
    print(f"Wrote JSONL : {jsonl_path}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
