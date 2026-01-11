---
title: "Open Dog Academy — Personal Reference Guide + AI Handoff"
scope: "Compilation of planning + research-scaffolding produced in this chat/project (tasklists, taxonomy, file structures, and improvement framework). NOTE: No external sources were fetched/validated in-chat; this package is primarily an internal design + research plan."
created: "2026-01-10"
updated: "2026-01-10"
status: draft
tags:
  - open_dog_academy
  - dog_training
  - service_dogs
  - working_dogs
  - curriculum_design
  - open_source
  - research_ops
  - obsidian
---

Project Name: **Open Dog Academy**  
Corpus Name: **Open Dog Academy Personal Reference Guide + AI Handoff**  
Export Date: **2026-01-10**

# Table of Contents
1. Research Map
2. Topic Briefs (RCH-0001 to RCH-0012)
3. Glossary
4. Roadmap to Maintain and Extend This Corpus

# Research Map
This corpus is a design + research-scaffolding package for building Open Dog Academy as an open-source, course-like resource that:
- teaches fundamentals → advanced fundamentals → reliability,
- supports service-first goals while using sports for precision and proofing,
- spans working dog roles (service, detection, SAR, etc.),
- includes safety boundaries, ethics, and referral triggers,
- uses a “Deep Search” workflow to pull authoritative sources later and convert them into reusable artifacts,
- supports maintainability via GitHub (index registry) and Obsidian (type-first architecture).

Major theme areas covered:
- Knowledge architecture (repo + Obsidian vault patterns)
- Research task design (Deep Search prompts + output contract)
- Taxonomy (domains, modules, tags, risk levels)
- Certifications ecosystem (CGC baseline + broader targets)
- Reliability overlay (scoring + generalization + re-tests)
- Safety policies (behavior triage, referral triggers, devices/aversives education-only)
- Working dogs + sports breadth
- Gear/DIY/rope skills
- Experimental sport design (pentest-inspired)

# Topic Briefs

## RCH-0001 — Corpus Architecture (Type-first Knowledge System)
Summary: Type-first architecture: standards/specs/curriculum/protocols/assessments/reference/ops/projects.
Key takeaways:
- Type-first reduces churn as new domains are added.
- Specs centralize definitions to reduce drift.
Decision rules:
- Prefer small notes + linking.
Claims:
- INFERENCE (high): Type-first reduces structural churn. Sources: SRC-0001.

## RCH-0002 — Deep Search Output Standard + Artifact Contract
Summary: A strict extraction template for each source plus an “improvement layer”.
Claims:
- INFERENCE (high): Strict templates improve reuse. Sources: SRC-0001.

## RCH-0003 — Domain + Module Taxonomy
Summary: Multi-axis tagging: domain/audience/use/risk/modules.
Claims:
- INFERENCE (high): Multi-axis tagging supports multiple curriculum views. Sources: SRC-0001.

## RCH-0004 — Improvement Pack v3 (What to Research Next)
Summary: Tiered research plan (policy/triage/tasks → health → sports → devices → facilities → ops).
Claims:
- INFERENCE (high): Prioritizing policy + triage reduces harm. Sources: SRC-0001.

## RCH-0005 — Certification Ecosystem + Crosswalk (“Compile Down”)
Summary: Treat certifications as targets; map to Skill Atoms and modules; add ODA overlay beyond pass/fail.
Claims:
- INFERENCE (high): Crosswalk reduces duplication. Sources: SRC-0001.

## RCH-0006 — Reliability Overlay + Assessment Bank
Summary: Scoring semantics, generalization matrices, re-tests, assessor calibration.
Claims:
- INFERENCE (high): Consistent scoring reduces ambiguity. Sources: SRC-0001.

## RCH-0007 — Safety Boundaries + Behavior Triage + Refer-out Policy
Summary: Green/yellow/red triage + stop-and-refer triggers; high-risk boundaries.
Claims:
- INFERENCE (high): Referral triggers reduce harm. Sources: SRC-0001.

## RCH-0008 — Working Dogs Umbrella (Service as specialization)
Summary: Service under working dogs; shared foundations reused across roles.
Claims:
- INFERENCE (high): Service-under-working reduces duplication. Sources: SRC-0001.

## RCH-0009 — Sports as Improvement Engine
Summary: Sports provide structured drills; map exercises to Skill Atoms; enforce safety.
Claims:
- INFERENCE (medium): Sports can increase reliability when mapped properly. Sources: SRC-0001.

## RCH-0010 — Gear Ecosystem (Low-cost, DIY, maintenance)
Summary: Gear matrices, DIY safety, inspection/retirement, loaner library concept.
Claims:
- INFERENCE (high): Gear matrix reduces confusion. Sources: SRC-0001.

## RCH-0011 — Rope Skills for Trainers (Safety-first)
Summary: Quick-release knots, long-line handling, strict no-unattended-tie-out stance.
Claims:
- INFERENCE (medium): Standard rope SOP reduces accidents. Sources: SRC-0001.

## RCH-0012 — New Sport Design (Pentest-inspired Arena Sport)
Summary: Safe legal arena puzzle sport; welfare-first judging; rulebook skeleton early.
Claims:
- INFERENCE (medium): Mechanics layer makes new sports easier to design safely. Sources: SRC-0001.

# Glossary
- standards: external authorities (laws, rulebooks, tests).
- specs: internal canonical definitions (interfaces).
- protocols: SOPs.
- assessments: rubrics + score sheets (test harnesses).
- skill_atoms: smallest reusable behavior primitives.

# Roadmap to Maintain and Extend This Corpus
Workflow: intake → triage → capture → synthesize → review → publish → handoff.
Quality checklist:
- claims labeled EVIDENCE/INFERENCE/HYPOTHESIS
- high-risk includes stop/referral triggers
- IDs are append-only
Versioning: v0.x early; v1.0 stable IDs.


## Package Additions (Completeness Upgrades)
- research/deep_search_tasklist_master.md
- research/tasks_v3/ (task stubs S1–X3)
- research/facets/ (gap stubs)
- research/index.yml (pre-registered paths)
- exports/2026-01-10/completeness_audit.md
- exports/2026-01-10/coverage_matrix.csv

## Housing access (FHA/HUD assistance animals)

**Doc ID:** RCH-0101

### Summary
Internal synthesis capturing how housing providers should handle assistance animal accommodation requests under the Fair Housing Act, anchored to HUD guidance. Focus: what providers may ask, what fees are disallowed, and when denial/removal is permitted.

### Key takeaways
- Assistance animals are not treated as pets in the accommodation context.
- Pet fees/deposits are generally not allowed for assistance animals (damages are separate).
- Documentation may be requested when disability/need is not obvious, within limits.
- Direct threat/behavior issues can justify denial/removal with a documented rationale.

### Decision rules / heuristics
- Default to allowing the animal; denial is the exception case (undue burden / direct threat).
- Never require “registration/certification” as a condition of accommodation.
- Write everything down: request, documentation, decision, escalation path.

### Details
#### what to build next
- Housing request intake form template.
- “What landlords may ask / may not ask” one-pager.
- Dispute script + referral instructions for HUD/FHEO complaints.

### Risks / failure modes
- **Guidance drift:** HUD guidance documents can be withdrawn/updated. Treat FHEO-2020-01 as historical and confirm current HUD guidance before publishing hard rules.
- Over-collection of medical info (privacy breach).
- Illegal fees or blanket breed bans applied to assistance animals.
- Failure to address dangerous behavior with a safety plan.

### Open questions
- Confirm current HUD notice wording at time of publication.
- Integrate Montana-specific law once collected.

### Claims list
- **INFERENCE** (medium) — Housing providers must generally treat assistance animals as a reasonable accommodation unless undue burden or direct threat applies.  
  sources: SRC-0006, SRC-0007, SRC-0008, SRC-0049, SRC-0050, SRC-0002
- **INFERENCE** (medium) — Pet fees/deposits are not permitted for assistance animals; damage liability remains separate.  
  sources: SRC-0007, SRC-0008, SRC-0002
- **INFERENCE** (medium) — If disability/need is not obvious, providers may request reliable documentation limited to disability-related need.  
  sources: SRC-0007, SRC-0002

- **INFERENCE** (low) — HUD withdrew certain older guidance documents in September 2025; this can change how older HUD notices should be treated (historical vs current). Confirm on HUD before relying on withdrawn documents for “must/shall” claims.
  sources: SRC-0050, SRC-0049

### Sources used
SRC-0006, SRC-0007, SRC-0008, SRC-0049, SRC-0050, SRC-0002


## Employment access (ADA Title I workplace accommodation)

**Doc ID:** RCH-0102

### Summary
Internal synthesis describing service animals as workplace accommodations via the ADA Title I interactive process. Emphasis: documentation boundaries, trial-period evaluation, and balancing coworker allergies/phobias without default denial.

### Key takeaways
- Workplace access is handled via the interactive process, not the public-access two-question script.
- Denial/removal requires undue hardship or direct threat basis.
- Trial periods plus rubrics reduce arbitrary decisions.

### Decision rules / heuristics
- Treat the request like any assistive device accommodation: document, evaluate, iterate.
- If behavior creates a direct threat, remove the animal and pursue alternate accommodations.

### Details
#### what to build next
- HR checklist + meeting agenda.
- Trial-period behavior rubric.
- Coworker accommodation balancing worksheet.

### Risks / failure modes
- Confusing Title I with public-access rules and mishandling documentation.
- Ad hoc denials driven by prejudice rather than hardship analysis.

### Open questions
- Verify most current EEOC/ADA guidance language before publishing templates.

### Claims list
- **INFERENCE** (medium) — Allowing a service animal can be a reasonable accommodation under ADA Title I and should be handled through the interactive process.  
  sources: SRC-0011, SRC-0009, SRC-0002
- **INFERENCE** (medium) — Employers may deny/remove only where undue hardship or direct threat applies, with documentation.  
  sources: SRC-0011, SRC-0009, SRC-0002

### Sources used
SRC-0011, SRC-0009, SRC-0002


## School access (ADA/Section 504; K–12 and higher ed)

**Doc ID:** RCH-0103

### Summary
Internal synthesis summarizing school access: K–12 service dog access under ADA Title II/Section 504, and higher ed under ADA plus FHA for dorm housing (including ESAs in housing-only contexts).

### Key takeaways
- K–12 and college policies differ, but both require accommodation of service dogs.
- Schools should train staff on working-dog interaction and incident response.
- Campus housing can fall under FHA assistance animal accommodations.

### Decision rules / heuristics
- Plan operations: relief breaks, handler responsibility, staff response to misbehavior.
- Keep the school from ‘becoming the trainer’; focus on access + integration.

### Details
#### what to build next
- Staff training one-pager.
- Classroom layout + relief schedule template.
- Incident response SOP aligned to ADA removal conditions.

### Risks / failure modes
- Unsafe environments if staff/peers distract the dog.
- Misapplied ESA rules causing conflict in classrooms.

### Open questions
- Need primary-source verification for current school-specific guidance language.

### Claims list
- **INFERENCE** (medium) — Schools must generally permit service dogs; policies should align to ADA question/removal boundaries.  
  sources: SRC-0010, SRC-0005, SRC-0002
- **INFERENCE** (medium) — Campus housing can trigger FHA accommodation for assistance animals (including ESAs) within housing areas.  
  sources: SRC-0006, SRC-0010, SRC-0002

### Sources used
SRC-0010, SRC-0005, SRC-0006, SRC-0002


## Behavior triage for working-dog pathways

**Doc ID:** RCH-0104

### Summary
Internal synthesis establishing a green/yellow/red triage framework for candidate dogs, with explicit stop/referral triggers to protect public safety and prevent escalation.

### Key takeaways
- Public-access work demands exceptional stability; aggression is a hard stop without professional remediation.
- Yellow-flag stress signals should trigger plan changes early.
- Referral pathways must be explicit and easy to activate.

### Decision rules / heuristics
- When in doubt, increase distance and reduce exposure; safety beats ego.
- Re-evaluate after major changes (health, environment, routine).

### Details
#### what to build next
- Triage decision flowchart.
- Trigger log + distance plan template.
- Post-incident review SOP.

### Risks / failure modes
- Handler overconfidence leading to unsafe exposures.
- Suppression masquerading as progress (shutdown).

### Open questions
- Need guidance on which assessments are appropriate and how to interpret them.

### Claims list
- **INFERENCE** (medium) — Aggression or uncontrolled public behavior is incompatible with public-access working standards and should trigger cessation + professional evaluation.  
  sources: SRC-0024, SRC-0005, SRC-0013, SRC-0002, SRC-0003

### Sources used
SRC-0024, SRC-0005, SRC-0013, SRC-0002, SRC-0003


## Service task taxonomy and claims boundaries

**Doc ID:** RCH-0105

### Summary
Internal synthesis mapping tasks into families and setting policy boundaries: tasks must be observable, trainable, and disability-related; avoid medical promises; mobility tasks require extra safety review.

### Key takeaways
- Task = disability-related work/behavior, not comfort.
- Taxonomy improves reuse: training patterns, assessments, proofing plans.
- Mobility and medical-claim areas need strict boundaries and refer-out rules.

### Decision rules / heuristics
- Write tasks as behavior specs with pass/fail criteria and proofing matrices.
- Use neutral language in docs: assist/mitigate/respond; never ‘cure.’

### Details
#### what to build next
- Task spec schema with examples.
- Suitability matrix.
- Claims policy for medical alert tasks.

### Risks / failure modes
- Over-claiming medical alert accuracy without validation.
- Biomechanical injury from inappropriate mobility task training.

### Open questions
- Need evidence review on medical alert reliability and validation methods.

### Claims list
- **INFERENCE** (medium) — Service tasks must be disability-related work/tasks; comfort alone is not sufficient.  
  sources: SRC-0005, SRC-0022, SRC-0002
- **INFERENCE** (low) — ADI standards describe program expectations that can inform curriculum benchmarks; verify exact requirement wording before publishing as mandatory for owner-trainers.  
  sources: SRC-0024, SRC-0002

### Sources used
SRC-0005, SRC-0022, SRC-0024, SRC-0002
## Public access (ADA) — standards, assessment, and training progression

**Doc ID:** RCH-0106

### Summary
This brief anchors “public access” training to what actually matters:
- ADA public-access baseline (control + housebreaking; limited removal conditions)
- an ODA trainer-observable checklist that can be audited in real spaces
- a progressive training ladder + abort criteria + logging so reliability scales

It also makes a clean distinction between **law** (minimums) and **industry rubrics** (useful, not mandatory).

### Key takeaways
- ADA baseline is simple: the dog must be **under control** and **housebroken**; otherwise removal can be required.  
- “Perfect obedience” is not the legal standard; **effective control under distraction** is.
- Treat public access as a skill system: criteria → drills → proofing matrix → assessment.

### Decision rules / heuristics
- Gate outings behind an at-home obedience baseline.
- Increase distraction one variable at a time (environment *or* distance *or* duration).
- Any repeat “out of control” patterns → stop outings and route to behavior triage.

### Details
- Standard: [[public_access_standard]]
- Protocol: [[sop_public_access_training]]
- Assessment: [[assessment_public_access]]
- Lesson: [[public_access_lesson]]

### Risks / failure modes
- Over-facing (too much, too soon) → reactivity/avoidance.
- Handler inconsistency (leash + reinforcement timing) → “random dog” behavior.
- Mistaking IAADP/other rubrics as legal requirements.

### Open questions
- Add primary Title III eCFR section on control/removal as a direct citation.
- Build a comparative table of PAT rubrics (IAADP vs ADI vs program tests).

### Claims list
- **EVIDENCE** (high) — ADA guidance allows removal if the dog is out of control and the handler cannot/will not regain control, or if the dog is not housebroken.  
  sources: SRC-0041, SRC-0044
- **EVIDENCE** (high) — Staff in public accommodations may ask the “two questions” when the disability/task is not obvious, and may not require documentation.  
  sources: SRC-0005, SRC-0041
- **EVIDENCE** (medium) — IAADP publishes a minimum training standard for public access that includes behavioral neutrality and structured public exposure expectations.  
  sources: SRC-0045
- **INFERENCE** (medium) — A trainer-observable checklist (loose leash, neutral passing, settle, toileting reliability) is a practical translation of “under control/housebroken.”  
  sources: SRC-0041, SRC-0045

### Sources used
SRC-0005, SRC-0041, SRC-0044, SRC-0045
