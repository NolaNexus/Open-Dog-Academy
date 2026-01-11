# Open Dog Academy — Handoff Prompt (2026-01-11)

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
