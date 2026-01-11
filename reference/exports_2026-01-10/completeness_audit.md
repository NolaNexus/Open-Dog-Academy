# completeness_audit (2026-01-10)

## v7 updates (2026-01-10)
- Added ADA service animal standard + public access standard/protocol/lesson/assessment.
- Added raw source PDFs from recent Deep Research wave.
- Updated source register with new legal + public access sources.


This audit checks **structural completeness** of the package (files, schemas, and coverage stubs).  
It does **not** guarantee external factual correctness (sources must still be verified at publication time).

## measurable definition
See: `exports/2026-01-10/completeness_definition.md`

## module coverage snapshot (selected high-ROI areas)

| module              |   expected_standard |   expected_spec |   expected_protocol |   expected_lesson |   expected_assessment |   present_standard_count |   present_spec_count |   present_protocol_count |   present_lesson_count |   present_assessment_count |   completeness_score |
|:--------------------|--------------------:|----------------:|--------------------:|------------------:|----------------------:|-------------------------:|---------------------:|-------------------------:|-----------------------:|---------------------------:|---------------------:|
| Health_FirstAid     |                   1 |               0 |                   1 |                 1 |                     1 |                        1 |                    0 |                        1 |                      1 |                          1 |                  100 |
| Health_Nutrition    |                   1 |               0 |                   1 |                 1 |                     1 |                        1 |                    0 |                        1 |                      1 |                          1 |                  100 |
| Ops_Accessibility   |                   1 |               0 |                   1 |                 1 |                     1 |                        1 |                    0 |                        1 |                      1 |                          1 |                  100 |
| Policy_Employment   |                   1 |               0 |                   1 |                 1 |                     1 |                        1 |                    0 |                        1 |                      1 |                          1 |                  100 |
| Policy_Housing      |                   1 |               0 |                   1 |                 1 |                     1 |                        1 |                    0 |                        1 |                      1 |                          1 |                  100 |
| Policy_Schools      |                   1 |               0 |                   1 |                 1 |                     1 |                        1 |                    0 |                        1 |                      1 |                          1 |                  100 |
| Service_TaskLibrary |                   1 |               1 |                   1 |                 1 |                     1 |                        1 |                    1 |                        1 |                      1 |                          1 |                  100 |

## gaps (still incomplete modules with numeric expectations)
| module   | completeness_score   |
|----------|----------------------|

## major missing areas (by design)
These remain **stub-only** or not yet instantiated as full standards/specs/protocols/lessons/assessments:

- Public access test comparisons (ADI/IAADP PAT rubrics)
- CGC/CGCA/CGCU + evaluator notes (verbatim rule items)
- Sports rulebooks (rally/obedience/nosework/agility/etc.)
- Working dog specialties (detection/SAR/protection safety policy)
- Health deep dives (rehab, injury epidemiology by sport/job)
- Open-source contributor QA (review rubrics beyond skeleton)

## immediate next actions to improve completeness
1. Run Deep Research “primary sources verification pass” for legal modules (HUD/ADA/EEOC/adata.org) and replace INFERENCE with EVIDENCE where appropriate.
2. Instantiate rulebook extraction modules (CGC + one sport) end-to-end (standard → protocol → lesson → assessment).
3. Add drift-watch `next_review_date` fields to all legal/standards notes.
