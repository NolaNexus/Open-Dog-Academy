# Doc length limits (anti-truncation)
Status: draft

Goal: keep individual docs small enough to **copy/paste into chat tools** without getting truncated, while still being readable on the website.

## What is enforced
- All Markdown under `docs/` is checked in CI.
- Limits are defined in the repo root file: `doc-limits.yml`.
- The validator is: `scripts/validate_doc_limits.py`.

## Why this exists
Long pages are harder to:
- paste into AI tools for “handoff”
- review in PRs
- navigate on a static site

## Per-file overrides (rare)
If a doc *must* be longer (e.g., a reference export), add an entry to `doc-limits.yml`:

```yml
overrides:
  - name: long_export
    path: docs/reference/exports_YYYY-MM-DD/some_file.md
    max_chars: 60000
    max_lines: 2500
```

## How to fix a failure
When a doc exceeds the cap, use the standard split pattern:

1) Make a folder next to the doc:
   - `docs/manuals/manual-foo.md` → `docs/manuals/manual-foo/`
2) Split into parts at `##` (H2) boundaries:
   - `docs/manuals/manual-foo/part-01.md`
   - `docs/manuals/manual-foo/part-02.md`
3) Turn the original file into an index:
   - short overview
   - link list to the parts
4) For raw/quoted source material:
   - put your *summary* in `docs/reference/extracts/`
   - put large exports in `docs/reference/exports_YYYY-MM-DD/`

## Run locally
```bash
python3 scripts/validate_doc_limits.py --report
```



## When you get a warning (before a failure)
The validator emits **warnings** when a doc hits ~85% of its configured cap. Treat this as a “refactor now” signal.

Recommended response:
1) Run a split plan:
   - `python3 scripts/suggest_doc_split.py <your_doc.md>`
2) Split at `##` boundaries into small modules.
3) Promote repeated content into `docs/_atoms/` and include it from assemblies.

This keeps docs portable (AI handoff), reviewable (PRs), and readable (web).


## Interface-safe delivery

If the interface truncates long AI outputs, use `scripts/chunk_for_chat.py` to export any repo doc into chat-safe parts (with end markers).
