#!/usr/bin/env python3
"""Validate ODA atoms (single-source-of-truth building blocks).

Rules
- Atoms live in docs/_atoms/
- Each atom must include header fields:
  - ID:
  - Type:
  - Status:
  - Path:
- Filenames should end with -NNN.md (e.g., session-structure-001.md)

Usage
  python3 scripts/validate_atoms.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ATOMS_DIR = Path("docs/_atoms")
FILENAME_RE = re.compile(r"^[a-z0-9-]+-\d{3}\.md$")


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    sys.exit(1)


def main() -> int:
    if not ATOMS_DIR.exists():
        fail(f"Missing atoms directory: {ATOMS_DIR}")

    atom_files = sorted(ATOMS_DIR.rglob("*.md"))
    if not atom_files:
        fail("No atom files found under docs/_atoms/")

    problems: list[str] = []

    for f in atom_files:
        rel = f.as_posix()
        if f.name != "index.md" and not FILENAME_RE.match(f.name):
            problems.append(f"Bad atom filename: {rel} (expected *-NNN.md)")
            continue


        # Index is allowed to be a normal page without atom headers
        if f.name == "index.md":
            continue

        text = f.read_text(encoding="utf-8", errors="replace")
        head = "\n".join(text.splitlines()[:40])

        required = ["ID:", "Type:", "Status:", "Path:"]
        for key in required:
            if key not in head:
                problems.append(f"Missing '{key}' in header: {rel}")

        # Validate Path matches actual file path (best-effort)
        m = re.search(r"^Path:\s*`([^`]+)`\s*$", head, flags=re.MULTILINE)
        if m:
            declared = m.group(1).strip()
            expected = f"docs/_atoms/{f.relative_to(ATOMS_DIR).as_posix()}"
            if declared != expected:
                problems.append(
                    f"Path mismatch in {rel}: declared '{declared}' expected '{expected}'"
                )

        # Basic size sanity: atoms should stay small-ish
        # (hard caps are enforced by validate_doc_limits.py)
        if len(text) > 15000:
            problems.append(f"Atom too large (>15k chars): {rel} (split into smaller atoms)")

    if problems:
        print("Atom validation failed:\n")
        for p in problems:
            print(f"- {p}")
        return 1

    print(f"Atoms OK: {len(atom_files)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
