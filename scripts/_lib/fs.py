"""Tiny filesystem helpers for ODA scripts.

Mantra for scripts
  - Deterministic output
  - One command to run
  - No surprises (permissions, newlines, encoding)

Notes
  - Git only tracks the executable bit, but *local* permissions still matter
    for workflow (especially on Linux/macOS). We set sane defaults at write time.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path


def is_windows() -> bool:
    return os.name == "nt"


def write_text(
    path: Path,
    content: str,
    *,
    mode: int = 0o644,
    ensure_trailing_newline: bool = True,
) -> None:
    """Write UTF-8 text atomically with consistent newlines + predictable perms."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if ensure_trailing_newline and content and not content.endswith("\n"):
        content += "\n"

    # Write to a temp file in the same directory then replace atomically.
    # This avoids partial writes if interrupted.
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        delete=False,
        dir=str(path.parent),
        prefix=path.name + ".tmp.",
    ) as tf:
        tf.write(content)
        tmp_path = Path(tf.name)

    tmp_path.replace(path)

    # Best-effort chmod. On Windows this is mostly meaningless, so skip.
    if not is_windows():
        try:
            os.chmod(path, mode)
        except PermissionError:
            # Don’t crash generation because of chmod edge cases (e.g. strange mounts).
            pass
