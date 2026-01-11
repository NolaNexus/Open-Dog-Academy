# Dev workflow (helper scripts + automation)

Status: draft

This repo is set up "docs-as-code" style: small pages, reusable atoms, and **CI gates**.

---

## Install local tooling (recommended)

### Python
- Use Python 3.11+.

### MkDocs

```bash
python3 -m pip install -r requirements.txt
```

Dev extras (optional):

```bash
python3 -m pip install -r requirements-dev.txt
```

---

## One-command checks

Run the same validators as CI:

```bash
python3 scripts/run_checks.py
```

Fast mode (skip MkDocs build):

```bash
python3 scripts/run_checks.py --fast
```

---

## Helper CLI

The `oda` helper wraps common tasks:

```bash
python3 scripts/oda.py check
python3 scripts/oda.py index
python3 scripts/oda.py status normalize
python3 scripts/oda.py new skill OB_PLACE
python3 scripts/oda.py new atom --folder protocols --type protocol --slug leash-handling
```

---

## Pre-commit hooks (optional, but very nice)

Pre-commit runs lightweight checks before each commit.

```bash
python3 -m pip install pre-commit
pre-commit install
```

Now `git commit` will automatically run:
- basic markdown + yaml hygiene
- `scripts/run_checks.py --fast`
- unit tests

---

## Atomization accelerators

### Suggest a standard include pack for a skill

Default: prints a pasteable snippet (safe):

```bash
python3 scripts/skill_pack_apply.py docs/skills/ob/OB_RECALL.md --pack foundations
```

Apply mode (appends missing includes at the end):

```bash
python3 scripts/skill_pack_apply.py docs/skills/ob/OB_RECALL.md --pack foundations --write
```

---

## When CI fails

Run locally:

```bash
python3 scripts/run_checks.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Most failures are one of:
- a doc exceeded its length cap
- an atom header is missing `ID/Type/Status/Path`
- an `--8<--` include points to a missing file
- indexes are stale
- a status value isn't one of `stub/draft/stable`
