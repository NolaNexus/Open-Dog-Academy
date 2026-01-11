# Open Dog Academy (Template Skeleton)

This repository is a **clean-room rebuild** template for Open Dog Academy-style documentation:
- MkDocs (Material) site
- Atomic content blocks ("atoms") + assembled skills/classes
- Deterministic catalog generation (JSON + SQLite-ready pipeline stub)
- GitHub Pages deploy via GitHub Actions (artifact → deploy)

## Quick start (local)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdocs serve
```

## Repo conventions
- Authoritative standards live in `docs/standards/`
- Reusable blocks live in `docs/_atoms/`
- Pages that list many things are generated into `docs/_generated/` (do not hand-edit)
