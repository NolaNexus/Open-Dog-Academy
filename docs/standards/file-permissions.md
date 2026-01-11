# File permissions policy

**Status:** stable


This repo uses docs-as-code: deterministic generation + CI gates + low-friction local checks.

Permissions are a workflow detail, but they can create noisy diffs or broken tooling if they drift.
Also note: Git only tracks one permission bit — whether a file is executable.

## Policy

### Executable bit

- `docs/**` is **never executable**.
- Common config/content files are **never executable** (`*.md`, `*.yml`, `*.yaml`, `*.json`, etc.).
- `scripts/*.py` files with a **shebang** (`#!...`) should be executable.

### Defaults for generated files

All generator scripts write output files with:

- UTF-8 encoding
- LF newlines
- Trailing newline
- Non-executable mode (`0644`) on Linux/macOS

## Tools

### Check permissions

```bash
python3 scripts/fix_permissions.py --check
```

### Fix permissions

```bash
python3 scripts/fix_permissions.py --apply
```

### Run everything (recommended)

```bash
python3 scripts/oda.py check --fast
```

## Notes on umask

Your OS applies a process-wide creation mask (**umask**) when new files are created.
If you see odd default permissions, check your shell profile (`~/.profile`, `~/.zshrc`, etc.).

For local development, a common default is `022` (files `644`, dirs `755`).
For stricter privacy on multi-user machines, `077` is common.
