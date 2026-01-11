# Status taxonomy (stub → draft → stable)
Status: draft
Updated: 2026-01-10

ODA uses a strict 3-state maturity label on docs so the site can be both:

- **publishable** (you can safely point humans at it)
- **buildable** (we can iterate fast without pretending every page is finished)

This is classic docs-as-code: treat documentation like a first-class artifact and let automation catch drift.

---

## Allowed Status values

| Status | Meaning | What’s allowed | What’s required before promotion |
|---|---|---|---|
| `stub` | Placeholder / scaffold | incomplete sections, TODOs, missing prerequisites | Has a clear definition + links to needed atoms/skills |
| `draft` | Usable for trials | gaps ok, structure may change, content may be refactored | Pass criteria exists + safety notes where relevant |
| `stable` | Ready for general use | only incremental edits; avoid structural churn | Criteria tested in multiple contexts; failure modes documented |

---

## Where Status appears

- **Skills:** `**Status:** <value>` (with `**Type:**` and `**Last updated:**`)
- **Atoms:** `Status: <value>` in the atom header block
- **Other docs:** `Status: <value>` near the top

---

## Promotion checklist

### stub → draft
- Definition is one sentence and observable
- Minimum setup + session structure exists
- Safety gating included if there’s any risk (off-leash, equipment, handling)
- Logging / measurement fields are referenced (not reinvented)

### draft → stable
- Pass criteria is measurable and realistic
- Troubleshooting loop exists (common failure modes)
- Proofing ladder (distance/duration/distraction) is present or linked
- Dog welfare guardrails are explicit (no coercive pressure, avoid rehearsal of failure)

---

## Notes

- If you want extra nuance like “draft (modular refactor)”, put that nuance in the body, not in the Status field. The Status field stays machine-checkable.
- Consider using the Diátaxis doc-type split (tutorial / how-to / reference / explanation) when we later add a **Type taxonomy** across non-skill docs.
