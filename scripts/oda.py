#!/usr/bin/env python3
"""ODA helper CLI.

This is intentionally dependency-free. It's a convenience wrapper around the
existing scripts, plus a couple of safe scaffolds.

Examples
  python3 scripts/oda.py check
  python3 scripts/oda.py check --fast
  python3 scripts/oda.py index
  python3 scripts/oda.py status normalize
  python3 scripts/oda.py new skill OB_PLACE
  python3 scripts/oda.py new atom --folder protocols --type protocol --slug leash-handling
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from _lib.fs import write_text


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = REPO_ROOT / "docs"


def run(cmd: list[str]) -> int:
    print(f"==> {' '.join(cmd)}")
    p = subprocess.run(cmd, cwd=REPO_ROOT)
    return int(p.returncode)


def title_from_id(skill_id: str) -> str:
    return skill_id.replace("_", " ").title()


@dataclass
class AtomSpec:
    folder: str
    type: str
    slug: str
    status: str


ATOM_TEMPLATE = """ID: `{atom_id}`
Type: {atom_type}
Status: {status}
Path: `{path}`

---

## {title}

TODO
"""


SKILL_TEMPLATE = """# {skill_id} — {title}

**Type:** skill reference  
**Status:** stub  
**Last updated:** {today}

---

## Definition
TODO

## Setup
TODO

## Steps
TODO

## Pass criteria
TODO

## Common pitfalls + fixes
TODO

## Related skills
- TODO
"""


def atom_next_number(folder_path: Path, slug: str) -> int:
    # Finds the next available NNN for slug-NNN.md within a folder.
    pat = re.compile(rf"^{re.escape(slug)}-(\d{{3}})\.md$")
    nums = []
    for f in folder_path.glob(f"{slug}-*.md"):
        m = pat.match(f.name)
        if m:
            nums.append(int(m.group(1)))
    return (max(nums) + 1) if nums else 1


def cmd_check(args: argparse.Namespace) -> int:
    return run(["python3", "scripts/run_checks.py"] + (["--fast"] if args.fast else []))


def cmd_index(_: argparse.Namespace) -> int:
    return run(["python3", "scripts/generate_indexes.py"])


def cmd_status_normalize(_: argparse.Namespace) -> int:
    return run(["python3", "scripts/normalize_status_taxonomy.py"])


def cmd_perms_check(_: argparse.Namespace) -> int:
    return run(["python3", "scripts/fix_permissions.py", "--check"])


def cmd_perms_fix(_: argparse.Namespace) -> int:
    return run(["python3", "scripts/fix_permissions.py", "--apply"])


def cmd_new_skill(args: argparse.Namespace) -> int:
    import datetime as _dt

    sid = args.skill_id.strip()
    if not re.match(r"^[A-Z]{2,6}_[A-Z0-9]{2,}$", sid):
        print("ERROR: skill_id should look like OB_RECALL or PLAY_START")
        return 2

    # Reuse the mapping from generate_skill_files.py by importing it.
    sys.path.insert(0, str(REPO_ROOT))
    from scripts.generate_skill_files import folder_for  # type: ignore

    out_dir = folder_for(sid, DOCS_ROOT)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{sid}.md"

    if out_file.exists() and not args.force:
        print(f"Exists: {out_file.relative_to(REPO_ROOT)} (use --force to overwrite)")
        return 0

    today = _dt.date.today().isoformat()
    write_text(out_file, SKILL_TEMPLATE.format(skill_id=sid, title=title_from_id(sid), today=today), mode=0o644)
    print(f"Wrote: {out_file.relative_to(REPO_ROOT)}")
    return 0


def cmd_new_atom(args: argparse.Namespace) -> int:
    spec = AtomSpec(
        folder=args.folder.strip("/"),
        type=args.type.strip(),
        slug=args.slug.strip(),
        status=args.status.strip(),
    )
    if not re.match(r"^[a-z0-9-]+$", spec.slug):
        print("ERROR: --slug must be kebab-case, e.g., leash-handling")
        return 2
    if not re.match(r"^[a-z0-9-]+$", spec.folder):
        print("ERROR: --folder must be a simple folder name, e.g., protocols")
        return 2

    atom_dir = DOCS_ROOT / "_atoms" / spec.folder
    atom_dir.mkdir(parents=True, exist_ok=True)

    n = atom_next_number(atom_dir, spec.slug)
    fname = f"{spec.slug}-{n:03d}.md"
    path = atom_dir / fname

    atom_id = f"{spec.type}-{spec.slug}-{n:03d}"
    rel_path = f"docs/_atoms/{spec.folder}/{fname}"
    title = spec.slug.replace("-", " ").title()

    if path.exists() and not args.force:
        print(f"Exists: {path.relative_to(REPO_ROOT)} (use --force to overwrite)")
        return 0

    write_text(path, ATOM_TEMPLATE.format(atom_id=atom_id, atom_type=spec.type, status=spec.status, path=rel_path, title=title), mode=0o644)
    print(f"Wrote: {path.relative_to(REPO_ROOT)}")
    return 0



def cmd_path_build(_: argparse.Namespace) -> int:
    return run(["python3", "scripts/generate_paths.py"])


def cmd_report_core10(args: argparse.Namespace) -> int:
    cmd = ["python3", "scripts/core10_report.py"]
    if args.write:
        cmd.append("--write")
    return run(cmd)


def cmd_catalog_build(_: argparse.Namespace) -> int:
    return run(["python3", "scripts/build_catalog_db.py"])


def cmd_handoff(args: argparse.Namespace) -> int:
    cmd = ["python3", "scripts/handoff_pack.py"]
    if args.include_chunks:
        cmd.append("--include-chunks")
    return run(cmd)

def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="oda")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("check", help="Run validators (and mkdocs build unless --fast).")
    p.add_argument("--fast", action="store_true", help="Skip mkdocs build.")
    p.set_defaults(fn=cmd_check)

    p = sub.add_parser("index", help="Regenerate doc indexes (skills/classes/instructors).")
    p.set_defaults(fn=cmd_index)

    p = sub.add_parser("path", help="Generate curated learning path pages from YAML configs.")
    p.set_defaults(fn=cmd_path_build)

    p = sub.add_parser("report", help="Progress reports.")
    sub2 = p.add_subparsers(dest="report_cmd", required=True)
    p2 = sub2.add_parser("core10", help="Report progress converting the core 10 skills into assemblies.")
    p2.add_argument("--write", action="store_true", help="Write docs/reference/reports/core10-report.md")
    p2.set_defaults(fn=cmd_report_core10)

    p = sub.add_parser("perms", help="Permissions helpers (exec bits).")
    sub2 = p.add_subparsers(dest="perms_cmd", required=True)
    p2 = sub2.add_parser("check", help="Check exec-bit permissions policy.")
    p2.set_defaults(fn=cmd_perms_check)
    p2 = sub2.add_parser("fix", help="Apply exec-bit permissions policy.")
    p2.set_defaults(fn=cmd_perms_fix)

    p = sub.add_parser("status", help="Status taxonomy helpers.")
    sub2 = p.add_subparsers(dest="status_cmd", required=True)
    p2 = sub2.add_parser("normalize", help="Normalize legacy status strings across docs.")
    p2.set_defaults(fn=cmd_status_normalize)

    p = sub.add_parser("new", help="Create new docs from templates.")
    sub2 = p.add_subparsers(dest="new_cmd", required=True)

    ps = sub2.add_parser("skill", help="Create a new skill page (stub).")
    ps.add_argument("skill_id", help="Example: OB_RECALL")
    ps.add_argument("--force", action="store_true", help="Overwrite if the file exists.")
    ps.set_defaults(fn=cmd_new_skill)

    pa = sub2.add_parser("atom", help="Create a new atom file under docs/_atoms.")
    pa.add_argument("--folder", required=True, help="Atom category folder (e.g., protocols).")
    pa.add_argument("--type", required=True, help="Atom type (e.g., protocol, rubric).")
    pa.add_argument("--slug", required=True, help="kebab-case name (e.g., leash-handling).")
    pa.add_argument(
        "--status",
        default="draft",
        choices=["stub", "draft", "stable"],
        help="Status taxonomy value.",
    )
    pa.add_argument("--force", action="store_true", help="Overwrite if the file exists.")
    pa.set_defaults(fn=cmd_new_atom)

    p = sub.add_parser("catalog", help="Build derived catalog artifacts (SQLite + JSONL).")
    sub2 = p.add_subparsers(dest="catalog_cmd", required=True)
    p2 = sub2.add_parser("build", help="Scan docs and write artifacts/oda_catalog.sqlite + .jsonl")
    p2.set_defaults(fn=cmd_catalog_build)

    p = sub.add_parser("handoff", help="Build a ChatGPT-friendly handoff export bundle.")
    p.add_argument("--include-chunks", action="store_true", help="Also include chunked ROADMAP parts.")
    p.set_defaults(fn=cmd_handoff)

    return ap


def main() -> int:
    ap = build_parser()
    args = ap.parse_args()
    return int(args.fn(args))


if __name__ == "__main__":
    raise SystemExit(main())
