#!/usr/bin/env python3
"""chunk_for_chat.py

Chunk a Markdown document into chat-safe parts to mitigate interface truncation.

Why this exists
---------------
Even if the repo enforces document size limits, chat interfaces can truncate long outputs.
This tool creates small, numbered parts with explicit end markers, suitable for copy/paste
or incremental sending.

Features
--------
- Optional expansion of pymdownx.snippets include syntax:
    --8<-- "_atoms/templates/logging-template-001.md"
- Split primarily on H2 boundaries ("## "), then paragraphs if needed.
- Writes an index.md plus part-XX.md files to an export folder.

Reliability trick
-----------------
Each part includes a SHA-256 digest of its *body* and an explicit end marker.
If an interface truncates a copy/paste, the digest will not match.

Usage
-----
  python3 scripts/chunk_for_chat.py docs/manuals/manual-socialization.md --expand-includes
  python3 scripts/chunk_for_chat.py <path> --max-chars 6000 --out docs/reference/exports_YYYY-MM-DD/chat_chunks

Exit codes
----------
0 success
2 input error
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
from pathlib import Path
from typing import List, Tuple


INCLUDE_RE = re.compile(r'^\s*--8<--\s+"([^"]+)"\s*$')


def _safe_read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def expand_includes(text: str, docs_root: Path, max_depth: int = 10) -> str:
    """Expand snippet includes recursively."""
    def _expand_lines(lines: List[str], stack: Tuple[Path, ...], depth: int) -> List[str]:
        if depth > max_depth:
            raise ValueError(f"Include expansion exceeded max depth ({max_depth}). Stack: {stack}")
        out: List[str] = []
        for line in lines:
            m = INCLUDE_RE.match(line)
            if not m:
                out.append(line)
                continue

            rel = m.group(1).strip()
            inc_path = (docs_root / rel).resolve()

            # Safety: include must stay within docs_root
            if docs_root.resolve() not in inc_path.parents and inc_path != docs_root.resolve():
                raise ValueError(f"Unsafe include path '{rel}' resolves outside docs/: {inc_path}")

            if not inc_path.exists():
                raise FileNotFoundError(f"Missing include '{rel}' (resolved: {inc_path})")

            if inc_path in stack:
                raise ValueError(f"Include cycle detected: {' -> '.join(p.as_posix() for p in stack + (inc_path,))}")

            inc_text = _safe_read_text(inc_path)
            inc_lines = inc_text.splitlines(keepends=True)
            out.extend(_expand_lines(inc_lines, stack + (inc_path,), depth + 1))
        return out

    return "".join(_expand_lines(text.splitlines(keepends=True), stack=tuple(), depth=0))


def split_on_h2(text: str) -> List[str]:
    """Split text into blocks that start with an H2 (## ). Keeps the preamble as block 0."""
    lines = text.splitlines(keepends=True)
    blocks: List[List[str]] = [[]]
    for ln in lines:
        if ln.startswith("## "):
            blocks.append([ln])
        else:
            blocks[-1].append(ln)
    return ["".join(b).rstrip() + "\n" for b in blocks if "".join(b).strip()]


def split_paragraphs(block: str) -> List[str]:
    """Fallback splitting for oversized blocks: split on blank lines."""
    parts: List[str] = []
    buf: List[str] = []
    for ln in block.splitlines(keepends=True):
        buf.append(ln)
        if ln.strip() == "":
            parts.append("".join(buf))
            buf = []
    if buf:
        parts.append("".join(buf))
    return [p for p in parts if p.strip()]


def chunk_blocks(blocks: List[str], max_chars: int) -> List[str]:
    """Pack blocks into chunks under max_chars. Oversized blocks are further split."""
    chunks: List[str] = []
    cur: List[str] = []
    cur_len = 0

    def flush():
        nonlocal cur, cur_len
        if cur:
            chunks.append("".join(cur).rstrip() + "\n")
            cur, cur_len = [], 0

    for b in blocks:
        b_len = len(b)
        if b_len > max_chars:
            # flush current chunk, then split this block further
            flush()
            for p in split_paragraphs(b):
                if len(p) > max_chars:
                    # hard fallback: slice
                    for i in range(0, len(p), max_chars):
                        chunks.append(p[i:i + max_chars].rstrip() + "\n")
                else:
                    chunks.append(p.rstrip() + "\n")
            continue

        if cur_len + b_len > max_chars and cur:
            flush()

        cur.append(b)
        cur_len += b_len

    flush()
    return chunks


def default_out_dir(docs_root: Path, input_path: Path) -> Path:
    stamp = _dt.date.today().isoformat()
    base = input_path.stem
    return docs_root / "reference" / f"exports_{stamp}" / "chat_chunks" / base


def write_chunks(out_dir: Path, source_rel: str, chunks: List[str], digest_lines: int = 5) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    n = len(chunks)

    manifest = {
        "source": source_rel,
        "generated": _dt.datetime.now().isoformat(timespec="seconds"),
        "parts": [],
    }

    # Write parts
    part_paths: List[Path] = []
    for i, body in enumerate(chunks, start=1):
        part = out_dir / f"part-{i:02d}.md"

        body_bytes = body.encode("utf-8", errors="replace")
        sha = hashlib.sha256(body_bytes).hexdigest()
        words = len(re.findall(r"\S+", body))
        lines = body.count("\n") + 1

        # Head/tail snippets help humans confirm continuity across parts.
        # Keep these short: they are not the data, they are a fingerprint.
        dl = max(0, int(digest_lines))
        head_lines = "".join(body.splitlines(keepends=True)[:dl]).rstrip() if dl else ""
        tail_lines = "".join(body.splitlines(keepends=True)[-dl:]).rstrip() if dl else ""

        header = (
            f"# {out_dir.name} — Part {i}/{n}\n\n"
            f"- Source: `{source_rel}`\n"
            f"- Characters (body): {len(body)}\n"
            f"- Words (body): {words}\n"
            f"- Lines (body): {lines}\n"
            f"- SHA-256 (body): `{sha}`\n\n"
            f"## Head (first ~{dl} lines)\n\n"
            f"```\n{head_lines}\n```\n\n"
            f"## Tail (last ~{dl} lines)\n\n"
            f"```\n{tail_lines}\n```\n\n"
        )
        body_wrap_start = "<!-- ODA_CHUNK_BEGIN_BODY -->\n"
        # Important: do NOT prefix with a newline. We want the bytes between
        # BEGIN_BODY and END_BODY to be *exactly* the body that was hashed.
        body_wrap_end = "<!-- ODA_CHUNK_END_BODY -->\n"
        end = f"<!-- END_OF_PART {i}/{n} -->\n"

        part.write_text(header + body_wrap_start + body + body_wrap_end + end, encoding="utf-8")
        part_paths.append(part)

        manifest["parts"].append(
            {
                "part": f"part-{i:02d}.md",
                "chars": len(body),
                "words": words,
                "lines": lines,
                "sha256": sha,
                "begin_marker": "ODA_CHUNK_BEGIN_BODY",
                "end_body_marker": "ODA_CHUNK_END_BODY",
                "end_marker": f"END_OF_PART {i}/{n}",
            }
        )

    # Write index
    links = "\n".join([f"- [Part {i:02d}](part-{i:02d}.md)" for i in range(1, n + 1)])
    index = (
        f"# Chat chunks: `{source_rel}`\n\n"
        f"Generated to avoid interface truncation. Each part ends with `<!-- END_OF_PART n/N -->`.\n\n"
        f"Integrity: each part includes a SHA-256 digest of its body.\n\n"
        f"## Parts\n\n{links}\n"
    )
    (out_dir / "index.md").write_text(index, encoding="utf-8")

    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="Path to a Markdown file (usually under docs/).")
    ap.add_argument("--max-chars", type=int, default=6000, help="Maximum characters per output part.")
    ap.add_argument("--out", default=None, help="Output directory. Defaults to docs/reference/exports_DATE/chat_chunks/<file_stem>/")
    ap.add_argument("--expand-includes", action="store_true", help="Expand pymdownx.snippets includes before chunking.")
    ap.add_argument("--digest-lines", type=int, default=5, help="Number of head/tail lines to show as a human fingerprint.")
    ap.add_argument("--docs-root", default="docs", help="Docs root (default: docs).")
    args = ap.parse_args()

    in_path = Path(args.path)
    if not in_path.exists() or not in_path.is_file():
        print(f"Input not found: {in_path}")
        return 2

    docs_root = Path(args.docs_root)
    if not docs_root.exists():
        print(f"Docs root not found: {docs_root}")
        return 2

    text = _safe_read_text(in_path)

    # Compute source rel for metadata
    try:
        source_rel = in_path.relative_to(docs_root).as_posix()
    except Exception:
        source_rel = in_path.as_posix()

    if args.expand_includes:
        text = expand_includes(text, docs_root=docs_root)

    blocks = split_on_h2(text)
    chunks = chunk_blocks(blocks, max_chars=args.max_chars)

    out_dir = Path(args.out) if args.out else default_out_dir(docs_root, in_path)
    write_chunks(out_dir, source_rel=source_rel, chunks=chunks, digest_lines=args.digest_lines)

    print(f"Wrote {len(chunks)} part(s) to {out_dir.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
