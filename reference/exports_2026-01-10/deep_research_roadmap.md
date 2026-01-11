# deep_research_roadmap (completeness-checked)

Export date: 2026-01-10

This roadmap is designed so Deep Research (Deep Search) produces **maximally reusable** results with **minimal rework**.

## 1) Definition of completeness (4 layers)

### layer A — structural completeness (must always pass)
- required exports exist (guide, csv, jsonl, audit, coverage_matrix)
- schemas validate (CSV columns, JSONL required fields)
- registry exists (research/index.yml) and is append-only

### layer B — coverage completeness (module-level)
For each module code:
- ≥1 Standard OR explicit note "no primary standard exists"
- ≥1 Spec or Protocol defining internal criteria
- ≥1 Lesson (if user-facing)
- ≥1 Assessment linked to each lesson

High-risk modules additionally require:
- stop conditions + referral triggers
- allowed/disallowed equipment notes
- “claims we do/do not make” block

### layer C — evidence completeness (claim-level)
For each non-trivial claim in user-facing docs:
- labeled EVIDENCE / INFERENCE / HYPOTHESIS
- EVIDENCE claims cite a Source Register entry (SRC-####)
- INFERENCE explains reasoning briefly
- HYPOTHESIS states what would confirm/falsify

### layer D — freshness completeness (drift control)
For anything likely to change (laws, rulebooks, policies):
- include last_checked and next_review_date
- add a drift_watch section (what would trigger update)

## 2) Deep Research run plan (optimized waves)

### wave 0 — setup (1 day)
- verify templates exist (vault/00_system/templates)
- confirm research/index.yml registry is current
- confirm coverage_matrix.csv lists all modules

### wave 1 — safety + legality (Tier 1)
Run tasks: S1–S5
Outputs must populate:
- standards/legal/* (ADA, HUD, EEOC, schools)
- specs/safety_boundaries, protocols/behavior_triage
- service_task_library taxonomy + refer-out policy

Gate to pass:
- Behavior_Triage exists as SOP + assessment
- Policy pages include “may ask/may not ask” checklists
- Service task library includes safety boundaries

### wave 2 — health + development (Tier 2)
Run tasks: T1–T5
Outputs must populate:
- standards/health references (vet org guidance)
- protocols for first aid, conditioning progression, rehab triggers
Gate:
- Health_FirstAid has emergency action plan template
- Development modules include stage modifications + risk periods

### wave 3 — sports breadth (Tier 3)
Run tasks: U1–U5
Outputs must populate:
- standards/rulebooks/* with rulebook extracts
- adapters mapping sport exercises → Skill Atoms → service cross-training
Gate:
- each sport has: progression lesson + safety notes + assessment

### wave 4 — cue devices + ethics education-only (Tier 4)
Run tasks: V1–V3
Outputs must populate:
- standards/position_statements/*
- evidence_synthesis notes summarizing the state of evidence
Gate:
- clear policy: education-only; not first-line; refer-out
- no “how to use” instructions for aversive devices

### wave 5 — facilities/environment (Tier 5)
Run tasks: W1–W2
Outputs must populate:
- facilities setups + hazard checklists (hazards-by-category (evergreen))
Gate:
- environment progression template exists and links into public access training

### wave 6 — ops + QA (Tier 6)
Run tasks: X1–X3
Outputs must populate:
- contributor workflows, reviewer rubric, accessibility standards
Gate:
- PR checklist + reviewer rubric + versioning policy are present and approved

## 3) Verification: “have we covered all bases?”

Use this 6-part audit repeatedly:

1. **module audit**
   - coverage_matrix.csv: each module meets minimum counts
2. **risk audit**
   - all high-risk notes have stop/referral triggers
3. **standards audit**
   - each external-facing claim points to a Standard or is marked INFERENCE/HYPOTHESIS
4. **assessment audit**
   - each lesson has at least one linked assessment item
5. **drift audit**
   - standards have next_review_date where appropriate
6. **user-reality audit**
   - include constraints: low-cost gear, shelter pipeline, adult dogs, real schedules, accessibility

## 4) What would “v1 complete” look like?

Minimum viable v1:
- Spine1_Foundations + Spine2_CGC + Spine3_Reliability each have lessons + assessments + scoring overlay
- Policy_Housing / Policy_Employment / Policy_Schools have checklists + scripts
- Behavior_Triage exists and is mandatory reading before advanced modules
- Service task library exists with explicit safety boundaries
- At least 2 sports tracks (Rally + Nosework) fully cross-mapped into service reliability



---

## v6: verification-first research cycle (for completeness)

### wave 0 — verify primaries (convert INFERENCE → EVIDENCE)
- HUD FHEO-2020-01 + associated FAQs
- ADA service animal requirements + FAQ updates
- askJAN/adata.org as secondary practical framing
Deliverable: replace summaries with direct verbatim extracts where legal wording matters.

### wave 1 — instantiate 3 end-to-end “spines”
Each spine must include: standard + spec + protocol + lesson + assessment.
1) CGC spine
2) Public access spine
3) Behavior triage spine (already mostly scaffolded)

### wave 2 — rulebook library build-out
Choose 1 venue per sport and extract novice rules + allowed/disallowed gear.

### wave 3 — drift + governance
Add `next_review_date`, changelog sections, and PR checklists tied to module risk.

### wave 4 — evidence deepening
Systematic reviews (training methods, e-collar/vibration cue devices, welfare, stress physiology) with neutral synthesis and explicit boundaries.

See also: `exports/2026-01-10/completeness_definition.md`.
