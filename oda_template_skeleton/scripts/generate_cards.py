#!/usr/bin/env python3
"""Generate docs/_generated/atoms/index.md from docs/_atoms/*.

Where to run:
- repo root: `python scripts/generate_cards.py`
"""

from __future__ import annotations
from pathlib import Path
import re
import yaml

RE_FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)\Z", re.S)

ROOT = Path(__file__).resolve().parents[1]
ATOMS_DIR = ROOT / "docs" / "_atoms"
OUT = ROOT / "docs" / "_generated" / "atoms" / "index.md"

def parse_front_matter(text: str) -> dict:
    m = RE_FM.match(text)
    if not m:
        return {}
    return yaml.safe_load(m.group(1)) or {}

def main() -> None:
    items = []
    for path in sorted(ATOMS_DIR.rglob("*.md")):
        if path.name == "README.md":
            continue
        fm = parse_front_matter(path.read_text(encoding="utf-8"))
        title = fm.get("title") or path.stem
        atom_id = fm.get("id") or ""
        atom_type = fm.get("type") or "atom"
        rel_doc = path.relative_to(ROOT / "docs")
        href = "../" + str(rel_doc).replace("\\", "/")
        items.append((atom_type, title, href, atom_id))

    by_type = {}
    for t, title, href, atom_id in items:
        by_type.setdefault(t, []).append((title, href, atom_id))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append("# Atoms\n")
    lines.append("This page is generated. Do not edit by hand.\n")
    for t in sorted(by_type.keys()):
        lines.append(f"## {t}\n")
        lines.append("<div class=\"grid cards\" markdown>\n")
        for title, href, atom_id in by_type[t]:
            subtitle = f"`{atom_id}`" if atom_id else ""
            lines.append(f"-   **[{title}]({href})**\n\n    {subtitle}\n")
        lines.append("</div>\n")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
