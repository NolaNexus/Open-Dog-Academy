#!/usr/bin/env python3
"""Update artifacts/manifest.sha256 for tracked canonical artifacts.

By design, this manifest is small and boring. It supports:
- tamper detection in handoffs
- quick integrity verification in CI

Currently tracked:
- artifacts/oda_catalog.sqlite

Run:
  python3 scripts/update_artifact_manifest.py
"""

from __future__ import annotations

import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = [
    REPO_ROOT / "artifacts" / "oda_catalog.sqlite",
]
OUT = REPO_ROOT / "artifacts" / "manifest.sha256"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    missing = [str(p) for p in ARTIFACTS if not p.exists()]
    if missing:
        raise SystemExit(f"Missing artifacts: {missing}")

    lines = []
    for p in ARTIFACTS:
        rel = p.relative_to(REPO_ROOT).as_posix()
        lines.append(f"{sha256_file(p)}  {rel}")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
