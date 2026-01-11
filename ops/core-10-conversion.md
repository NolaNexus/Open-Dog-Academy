# Core-10 skills conversion tracker

Status: draft

This tracker exists to keep the “Core 10” assembly refactor honest:
- reduce duplication
- move reusable truth into `_atoms/`
- keep each skill page short and skimmable

---

## Core 10 (current)

This list is the current working set used by `docs/paths/_config/core10.yml`.

1. `OB_NAME` — name response
2. `OB_PLACE` — stationing / mat
3. `IND_SETTLE_SOLO` — settle without micromanagement
4. `OB_LOOSE_LEASH` — loose leash walking
5. `OB_LEAVE_IT` — leave it
6. `OB_DROP` — drop
7. `IND_CRATE` — crate comfort
8. `OB_RECALL` — recall foundations
9. `CC_NAILS` — cooperative care starter
10. `OB_TOUCH` — hand target

---

## Conversion checklist (done means “assembly-shaped”)

A skill is “converted” when:
- [ ] Header is complete: Type / Status / Last updated
- [ ] Repeated protocol content is replaced with atoms (`--8<-- ...`)
- [ ] Pass criteria is measurable (latency / distance / duration / distraction)
- [ ] Troubleshooting links to atoms (instead of reinventing)
- [ ] Doc stays under caps (or is split cleanly)

---

## Tracker

| Skill | Current status | Assembly refactor | Notes |
|---|---:|---:|---|
| OB_NAME | draft | ☐ | Candidate: convert to recall-style assembly (marker timing + proofing ladder + pass criteria template). |
| OB_PLACE | draft | ☐ | |
| IND_SETTLE_SOLO | draft | ☐ | |
| OB_LOOSE_LEASH | draft | ☐ | |
| OB_LEAVE_IT | draft | ✅ | Converted to assembly (includes protocols/rubrics + measurable pass criteria). |
| OB_DROP | draft | ☐ | |
| IND_CRATE | draft | ✅ | Converted to assembly (includes distress signals + measurable pass criteria). |
| OB_RECALL | draft | ✅ | Already refactored as a demo. |
| CC_NAILS | draft | ☐ | |
| OB_TOUCH | draft | ☐ | |

---

## How to refactor one skill (repeatable workflow)

1. Find duplicated blocks (setup, proofing, criteria, troubleshooting).
2. Move each block into `docs/_atoms/...`.
3. Replace in-skill content with snippet includes:

```md
--8<-- "_atoms/templates/logging-template-001.md"
```

4. Run checks:

```bash
python3 scripts/run_checks.py --fast
python3 scripts/update_artifact_manifest.py
python3 scripts/verify_catalog_sqlite.py
```
