#!/usr/bin/env python3
"""Create a ChatGPT-friendly handoff export bundle.

Design
------
- Markdown is source-of-truth.
- Export pack is derived and text-first.
- Include a JSONL catalog so an LLM can 'search' by reading.

Outputs
-------
- artifacts/handoff_pack_<YYYY-MM-DD>.zip
- artifacts/handoff_manifest_<YYYY-MM-DD>.md
- artifacts/handoff_prompt_<YYYY-MM-DD>.md

Exit codes
----------
0 success
2 input error
"""

from __future__ import annotations

import argparse
import datetime as _dt
import subprocess
import zipfile
from pathlib import Path
from typing import List, Tuple


def run(cmd: List[str]) -> None:
    subprocess.run(cmd, check=True)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def collect_existing(paths: List[Path]) -> List[Path]:
    return [p for p in paths if p.exists() and p.is_file()]


def zip_files(zip_path: Path, base_dir: Path, files: List[Path]) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for p in files:
            arc = p.relative_to(base_dir).as_posix()
            zf.write(p, arcname=arc)


def build_pack(repo_root: Path, include_chunks: bool) -> Tuple[Path, Path, Path]:
    date = _dt.date.today().isoformat()
    artifacts = repo_root / 'artifacts'
    docs_root = repo_root / 'docs'

    # 1) Ensure generated content is current
    run(['python3', str(repo_root / 'scripts' / 'generate_indexes.py')])
    run(['python3', str(repo_root / 'scripts' / 'generate_paths.py')])
    run(['python3', str(repo_root / 'scripts' / 'core10_report.py'), '--write'])
    run(['python3', str(repo_root / 'scripts' / 'build_catalog_db.py')])

    # 2) Optional: chunk ROADMAP for chat interfaces
    chunk_dir: Path | None = None
    if include_chunks:
        roadmap = repo_root / 'ROADMAP.md'
        if roadmap.exists():
            chunk_dir = docs_root / 'reference' / f'exports_{date}' / 'chat_chunks' / 'ROADMAP'
            run([
                'python3', str(repo_root / 'scripts' / 'chunk_for_chat.py'),
                str(roadmap),
                '--docs-root', str(repo_root),  # allow non-docs path; tool uses rel fallback
                '--out', str(chunk_dir),
                '--max-chars', '5500'
            ])

    # 3) Compose manifest + prompt
    manifest_path = artifacts / f'handoff_manifest_{date}.md'
    prompt_path = artifacts / f'handoff_prompt_{date}.md'
    zip_path = artifacts / f'handoff_pack_{date}.zip'

    files: List[Path] = []

    # Core repo docs
    files += collect_existing([
        repo_root / 'README.md',
        repo_root / 'ROADMAP.md',
        repo_root / 'FORMAT_POLICY.md',
        repo_root / 'mkdocs.yml',
        repo_root / 'doc-limits.yml',
    ])

    # Standards + indexes + paths + reports
    if docs_root.exists():
        files += collect_existing(list((docs_root / 'standards').rglob('*.md')))
        files += collect_existing(list((docs_root / 'indexes').rglob('*.md')))
        files += collect_existing(list((docs_root / 'paths').rglob('*.md')))
        files += collect_existing(list((docs_root / 'reference' / 'reports').rglob('*.md')))

    # DB/JSONL artifacts
    files += collect_existing([
        artifacts / 'oda_catalog.jsonl',
        artifacts / 'oda_catalog.sqlite',
        artifacts / 'manifest.sha256',
    ])

    # Optional chunked roadmap files
    if chunk_dir and chunk_dir.exists():
        files += collect_existing(list(chunk_dir.rglob('*.md')))

    # Deterministic sort
    files = sorted(set(files), key=lambda p: p.as_posix())

    manifest_lines = [
        f"# ODA handoff manifest ({date})",
        "",
        "This pack is **derived** from the repository. Markdown in the repo is the source of truth.",
        "",
        "## Included files",
        "",
    ]
    for p in files:
        manifest_lines.append(f"- `{p.relative_to(repo_root).as_posix()}`")

    write_text(manifest_path, "\n".join(manifest_lines) + "\n")

    prompt = f"""# Open Dog Academy — Handoff Prompt ({date})

You are continuing work on the **Open Dog Academy** docs-as-code repository.

## Mantra
- **Markdown is truth.**
- Generated artifacts must be deterministic and enforced via CI.

## Your job
1) Read `ROADMAP.md` and the current reports in `docs/reference/reports/`.
2) Use `artifacts/oda_catalog.jsonl` as your search/index surface.
3) Propose the next smallest set of changes that move the roadmap forward.
4) When you change docs, also update the roadmap (or add a roadmap fragment, if policy exists).

## Constraints
- Keep scripts dependency-light.
- Prefer validators + generators with `--check` modes.
- Avoid hand-edited indexes; generate them.
"""
    write_text(prompt_path, prompt)

    # Ensure manifest and prompt are included in the zip
    files += [manifest_path, prompt_path]
    files = sorted(set(files), key=lambda p: p.as_posix())

    zip_files(zip_path, base_dir=repo_root, files=files)

    return zip_path, manifest_path, prompt_path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo-root', default='.', help='Repo root (default: .).')
    ap.add_argument('--include-chunks', action='store_true', help='Include chat-chunked ROADMAP parts.')
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    if not (repo_root / 'docs').exists():
        print(f"Repo root does not look right (missing docs/): {repo_root}")
        return 2

    zip_path, manifest_path, prompt_path = build_pack(repo_root, include_chunks=args.include_chunks)
    print(f"Wrote: {zip_path}")
    print(f"Manifest: {manifest_path}")
    print(f"Prompt: {prompt_path}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
