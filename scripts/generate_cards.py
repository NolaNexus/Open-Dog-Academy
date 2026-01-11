#!/usr/bin/env python3
"""Generate card index pages from atoms + skills.

Outputs:
- docs/_generated/atoms/index.md
- docs/_generated/skills/index.md

Design goals:
- deterministic output
- minimal dependencies
- metadata-driven cards using Material's grid layout
"""

from __future__ import annotations

from pathlib import Path
import re
import yaml

RE_FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)\Z", re.S)

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

ATOMS_DIR = DOCS / "_atoms"
SKILLS_DIR = DOCS / "skills"

OUT_ATOMS = DOCS / "_generated" / "atoms" / "index.md"
OUT_SKILLS = DOCS / "_generated" / "skills" / "index.md"


def parse_front_matter(text: str) -> dict:
    m = RE_FM.match(text)
    if not m:
        return {}
    return yaml.safe_load(m.group(1)) or {}


def link_from_generated(target_doc_rel: Path, generated_section: str) -> str:
    # from docs/_generated/<generated_section>/ to docs/<target>
    # e.g. skills index lives in docs/_generated/skills/index.md
    # so link to docs/skills/foo.md is "../skills/foo.md"
    return "../" + str(target_doc_rel).replace("\\", "/")


def write_cards_index(out_path: Path, title: str, grouped: dict[str, list[tuple[str, str, str]]]) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append(f"# {title}\n")
    lines.append("This page is generated. Do not edit by hand.\n")

    for group in sorted(grouped.keys()):
        lines.append(f"## {group}\n")
        lines.append('<div class="grid cards" markdown>\n')
        for item_title, href, subtitle in grouped[group]:
            lines.append(f"-   **[{item_title}]({href})**\n\n    {subtitle}\n")
        lines.append("</div>\n")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    # --- Atoms ---
    atom_items: list[tuple[str, str, str, str]] = []
    for path in sorted(ATOMS_DIR.rglob("*.md")):
        if path.name == "README.md":
            continue
        fm = parse_front_matter(path.read_text(encoding="utf-8"))
        atom_type = fm.get("type") or "atom"
        title = fm.get("title") or path.stem
        atom_id = fm.get("id") or ""
        rel_doc = path.relative_to(DOCS)
        href = link_from_generated(rel_doc, "atoms")
        atom_items.append((atom_type, title, href, atom_id))

    atoms_grouped: dict[str, list[tuple[str, str, str]]] = {}
    for atom_type, title, href, atom_id in atom_items:
        subtitle = f"`{atom_id}`" if atom_id else ""
        atoms_grouped.setdefault(atom_type, []).append((title, href, subtitle))

    write_cards_index(OUT_ATOMS, "Atoms", atoms_grouped)

    # --- Skills ---
    skill_items: list[tuple[str, str, str, int]] = []
    for path in sorted(SKILLS_DIR.rglob("*.md")):
        if path.name == "index.md":
            continue
        fm = parse_front_matter(path.read_text(encoding="utf-8"))
        level = fm.get("level")
        try:
            level_int = int(level) if level is not None else 0
        except Exception:
            level_int = 0

        title = fm.get("title") or path.stem
        skill_id = fm.get("id") or ""
        rel_doc = path.relative_to(DOCS)
        href = link_from_generated(rel_doc, "skills")
        skill_items.append(("Level " + str(level_int), title, href, skill_id, level_int))

    skills_grouped: dict[str, list[tuple[str, str, str]]] = {}
    for group, title, href, skill_id, _lvl in skill_items:
        subtitle = f"`{skill_id}`" if skill_id else ""
        skills_grouped.setdefault(group, []).append((title, href, subtitle))

    write_cards_index(OUT_SKILLS, "Skills", skills_grouped)

    print(f"Wrote {OUT_ATOMS}")
    print(f"Wrote {OUT_SKILLS}")


if __name__ == "__main__":
    main()
