# Open Dog Academy (ODA)

This repository is a modular dog-training knowledge base designed for **MkDocs + GitHub Pages**.

## Website (MkDocs)
- Source docs live in `docs/`
- Config lives in `mkdocs.yml`

## Key rules
- Skills are atomic: **one file per `SKILL_ID`** in `docs/skills/`
- Standards are the **single source of truth** in `docs/standards/`
- No PDFs as primary storage (see `docs/format-policy.md`)

## Catalog (SQLite)

This repo includes a canonical, integrity-checked SQLite catalog used for handoffs and for generating a human-readable index page.

- Canonical DB: `artifacts/oda_catalog.sqlite`
- Hash manifest: `artifacts/manifest.sha256`
- Generated page: `docs/reference/catalog.md`

Commands:

```bash
make catalog
make verify-catalog
make catalog-rebuild
python3 scripts/update_artifact_manifest.py
```

## Local preview
```bash
python3 -m pip install -r requirements.txt
mkdocs serve
```

Then open the local URL MkDocs prints.

## Local checks (same as CI)

```bash
python3 scripts/run_checks.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Fast checks (skip MkDocs build):

```bash
python3 scripts/run_checks.py --fast
```

## Helper CLI

```bash
python3 scripts/oda.py check
python3 scripts/oda.py new atom --folder protocols --type protocol --slug leash-handling
```

## Start
- See `docs/start-here.md`

## Branding (placeholder)

Placeholder branding is optimized for **small repo size** and **fast page loads**:

- Logo (WebP): `docs/assets/branding/logo.webp`
- Favicon: `docs/assets/branding/favicon.png`
- Apple touch icon: `docs/assets/branding/apple-touch-icon.png`

See `docs/branding.md` for the replacement policy (keep filenames stable).

## Even faster: wrappers


If you’re on Linux/macOS and prefer a short command:

```bash
./oda check --fast
./oda new skill OB_PLACE
```

If you have `make`:

```bash
make fast
make report-core10
```

Windows PowerShell wrapper:

```powershell
./oda.ps1 check --fast
```
