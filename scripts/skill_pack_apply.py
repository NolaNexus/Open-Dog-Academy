#!/usr/bin/env python3
"""Suggest (or apply) a standard atom include pack to a skill page.

This is a *helper*, not a dictator: the default mode prints a pasteable snippet
so you can place it where it makes sense.

Why
  - Roadmap "Now" = convert skills to atom-powered assemblies.
  - Repeating the same include set by hand is error-prone.

Usage
  # Print the suggested snippet
  python3 scripts/skill_pack_apply.py docs/skills/ob/OB_RECALL.md --pack foundations

  # Apply (append) the missing includes to the file
  python3 scripts/skill_pack_apply.py docs/skills/ob/OB_RECALL.md --pack foundations --write
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _lib.fs import write_text


PACKS: dict[str, list[tuple[str, str]]] = {
    # A default set that matches OB_RECALL's structure.
    "foundations": [
        ("Session start ritual", "_atoms/protocols/session-start-ritual-001.md"),
        ("Session structure", "_atoms/protocols/session-structure-001.md"),
        ("Marker timing", "_atoms/concepts/marker-timing-001.md"),
        ("Errorless learning", "_atoms/protocols/errorless-learning-001.md"),
        ("Reward tiering", "_atoms/protocols/reward-tiering-001.md"),
        ("Reinforcement schedule", "_atoms/protocols/reinforcement-schedule-001.md"),
        ("Proofing ladder", "_atoms/rubrics/proofing-ladder-001.md"),
        ("Distance rubric", "_atoms/rubrics/distance-rubric-001.md"),
        ("Duration rubric", "_atoms/rubrics/duration-rubric-001.md"),
        ("Distraction rubric", "_atoms/rubrics/distraction-rubric-001.md"),
        ("Latency rubric", "_atoms/rubrics/latency-rubric-001.md"),
        ("Generalization checklist", "_atoms/checklists/generalization-checklist-001.md"),
        ("Safety gating", "_atoms/safety/safety-gating-001.md"),
        ("Troubleshooting loop", "_atoms/troubleshooting/troubleshooting-loop-001.md"),
        ("Decompression menu", "_atoms/checklists/decompression-menu-001.md"),
        ("Pass criteria", "_atoms/rubrics/pass-criteria-template-001.md"),
        ("Logging", "_atoms/templates/logging-template-001.md"),
    ],
}


def snippet_for(pairs: list[tuple[str, str]]) -> str:
    out: list[str] = []
    for title, atom_rel in pairs:
        out.append(f"## {title}\n")
        out.append(f"--8<-- \"{atom_rel}\"\n")
        out.append("")
    return "\n".join(out).strip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("skill_file", help="Path to a skill markdown file")
    ap.add_argument("--pack", required=True, choices=sorted(PACKS.keys()))
    ap.add_argument(
        "--write",
        action="store_true",
        help="Append missing includes to the end of the file (default: print snippet).",
    )
    args = ap.parse_args()

    path = Path(args.skill_file)
    if not path.exists():
        print(f"ERROR: not found: {path}")
        return 2

    text = path.read_text(encoding="utf-8", errors="replace")
    pack = PACKS[args.pack]

    missing = [(t, a) for (t, a) in pack if f'--8<-- "{a}"' not in text]
    if not missing:
        print("No missing includes. You're already using the full pack.")
        return 0

    block = "\n\n---\n\n" + f"## Pack: {args.pack} (auto-added)\n\n" + snippet_for(missing)

    if not args.write:
        print("Pasteable snippet (missing only):\n")
        print(block.strip() + "\n")
        print(f"\nMissing includes: {len(missing)}")
        return 0

    write_text(path, text.rstrip() + block, mode=0o644)
    print(f"Updated: {path}")
    print(f"Added includes: {len(missing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
