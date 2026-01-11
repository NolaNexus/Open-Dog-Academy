#!/usr/bin/env python3
"""verify_chat_chunks.py

Verify a folder produced by scripts/chunk_for_chat.py.

Problem
-------
Some chat interfaces silently truncate long copy/paste. The chunker therefore
writes per-part SHA-256 hashes (computed over the *body only*) plus explicit
markers.

This verifier checks:
- each part contains ODA_CHUNK_BEGIN_BODY / ODA_CHUNK_END_BODY marker lines
- each part's body SHA-256 matches manifest.json
- each part contains the expected END_OF_PART marker

Optional:
- reconstruct the full document by concatenating bodies
- compare the reconstructed output to an original source file

Usage
-----
  python3 scripts/verify_chat_chunks.py docs/reference/exports_YYYY-MM-DD/chat_chunks/<doc_stem>
  python3 scripts/verify_chat_chunks.py <out_dir> --rebuild rebuilt.md
  python3 scripts/verify_chat_chunks.py <out_dir> --compare-original docs/manuals/manual-socialization.md

Exit codes
----------
0: all good
1: verification failed
2: usage/input error
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

BEGIN = "<!-- ODA_CHUNK_BEGIN_BODY -->"
END_BODY = "<!-- ODA_CHUNK_END_BODY -->"

RE_BEGIN = re.compile(rf"^{re.escape(BEGIN)}$", flags=re.MULTILINE)
RE_END = re.compile(rf"^{re.escape(END_BODY)}$", flags=re.MULTILINE)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def extract_body(part_text: str) -> str:
    mb = RE_BEGIN.search(part_text)
    if not mb:
        raise ValueError("Missing ODA_CHUNK_BEGIN_BODY marker line")
    me = RE_END.search(part_text)
    if not me:
        raise ValueError("Missing ODA_CHUNK_END_BODY marker line")
    if me.start() < mb.end():
        raise ValueError("Markers out of order")

    # Body starts on the next line after the BEGIN marker line.
    body_start = part_text.find("\n", mb.end())
    if body_start < 0:
        raise ValueError("Malformed BEGIN marker line")
    body_start += 1

    # Body ends right before the END marker line.
    body_end = part_text.rfind("\n", 0, me.start())
    if body_end < 0:
        # No preceding newline; treat as empty body
        return ""
    return part_text[body_start:body_end + 1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir", help="Folder containing manifest.json and part-XX.md files")
    ap.add_argument("--rebuild", default=None, help="Write reconstructed body to this path")
    ap.add_argument("--compare-original", default=None, help="Compare reconstructed output to an original Markdown file")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    if not out_dir.exists() or not out_dir.is_dir():
        print(f"Not a folder: {out_dir}")
        return 2

    manifest_path = out_dir / "manifest.json"
    if not manifest_path.exists():
        print(f"Missing manifest.json in {out_dir}")
        return 2

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    parts = manifest.get("parts", [])
    if not parts:
        print("manifest.json has no parts")
        return 2

    ok = True
    bodies: list[str] = []

    for p in parts:
        part_name = p["part"]
        expected_sha = p["sha256"]
        expected_end = p.get("end_marker", "")

        part_path = out_dir / part_name
        if not part_path.exists():
            print(f"MISSING: {part_name}")
            ok = False
            continue

        text = part_path.read_text(encoding="utf-8", errors="replace")
        try:
            body = extract_body(text)
        except Exception as e:
            print(f"BAD MARKERS: {part_name}: {e}")
            ok = False
            continue

        actual_sha = sha256_text(body)
        if actual_sha != expected_sha:
            print(f"SHA MISMATCH: {part_name}\n  expected {expected_sha}\n  actual   {actual_sha}")
            ok = False

        if expected_end and expected_end not in text:
            print(f"MISSING END MARKER: {part_name} (expected '{expected_end}')")
            ok = False

        bodies.append(body)

    rebuilt = "".join(bodies)

    if args.rebuild:
        out_path = Path(args.rebuild)
        out_path.write_text(rebuilt, encoding="utf-8")
        print(f"Wrote rebuilt file: {out_path}")

    if args.compare_original:
        orig_path = Path(args.compare_original)
        if not orig_path.exists():
            print(f"Original not found: {orig_path}")
            return 2
        orig_text = orig_path.read_text(encoding="utf-8", errors="replace")
        if sha256_text(orig_text) != sha256_text(rebuilt):
            print("COMPARE FAILED: rebuilt output does not match original (SHA-256 differs)")
            print(f"  original: {sha256_text(orig_text)}")
            print(f"  rebuilt:  {sha256_text(rebuilt)}")
            ok = False
        else:
            print("COMPARE OK: rebuilt output matches original")

    if ok:
        print("OK: all parts verified")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
