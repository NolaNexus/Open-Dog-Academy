#!/usr/bin/env python3
"""Verify docs/ content against artifacts/oda_catalog.sqlite.

Checks:
- every catalog row has a corresponding docs/<path> file
- sha256 matches file bytes
- size_chars matches len(text)

Run:
  python3 scripts/verify_catalog_sqlite.py

Exit codes:
- 0: OK
- 2: mismatches found
"""

from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = REPO_ROOT / "artifacts" / "oda_catalog.sqlite"
DOCS_ROOT = REPO_ROOT / "docs"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    if not DB_PATH.exists():
        print(f"Missing DB: {DB_PATH}")
        return 2

    conn = sqlite3.connect(str(DB_PATH))
    rows = conn.execute(
        "SELECT path, size_chars, sha256 FROM docs ORDER BY path"
    ).fetchall()

    missing = []
    hash_mismatch = []
    size_mismatch = []

    for rel_path, size_chars, expected_hash in rows:
        p = DOCS_ROOT / rel_path
        if not p.exists():
            missing.append(rel_path)
            continue
        b = p.read_bytes()
        actual_hash = sha256_bytes(b)
        if actual_hash != expected_hash:
            hash_mismatch.append((rel_path, expected_hash, actual_hash))

        # size_chars is stored as character count of the UTF-8 decoded text
        try:
            text = b.decode("utf-8")
        except UnicodeDecodeError:
            # fall back: treat bytes length as size
            text = ""
        actual_size = len(text)
        if actual_size != int(size_chars):
            size_mismatch.append((rel_path, int(size_chars), actual_size))

    ok = not (missing or hash_mismatch or size_mismatch)

    if ok:
        print(f"OK: {len(rows)} docs verified against SQLite catalog")
        return 0

    print("CATALOG VERIFY FAILED")
    if missing:
        print(f"- Missing files: {len(missing)}")
        for x in missing[:25]:
            print(f"  - {x}")
        if len(missing) > 25:
            print(f"  ... ({len(missing)-25} more)")

    if hash_mismatch:
        print(f"- Hash mismatches: {len(hash_mismatch)}")
        for rel, exp, act in hash_mismatch[:10]:
            print(f"  - {rel}: expected {exp[:12]}… got {act[:12]}…")
        if len(hash_mismatch) > 10:
            print(f"  ... ({len(hash_mismatch)-10} more)")

    if size_mismatch:
        print(f"- Size mismatches: {len(size_mismatch)}")
        for rel, exp, act in size_mismatch[:10]:
            print(f"  - {rel}: expected {exp} chars got {act}")
        if len(size_mismatch) > 10:
            print(f"  ... ({len(size_mismatch)-10} more)")

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
