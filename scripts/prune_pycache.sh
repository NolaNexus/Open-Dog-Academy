#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

# Deletes transient Python cache artifacts.
# Safe for packaging and CI; not intended for use inside a running virtualenv.

echo "Pruning Python cache artifacts under: ${ROOT}"

find "${ROOT}" -type d -name "__pycache__" -prune -exec rm -rf {} +
find "${ROOT}" -type f -name "*.pyc" -delete

echo "Done."
