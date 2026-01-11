# completeness_definition (measurable)

Updated: 2026-01-10

Completeness is **not** “we wrote a lot.” It is the intersection of:

1) **Coverage** — every module has the minimum required artifacts.
2) **Traceability** — every non-trivial claim links to a source_id in the source register (or is explicitly marked inference/hypothesis).
3) **Safety readiness** — every medium/high risk topic has:
   - safety boundaries
   - stop/referral triggers
   - “do-not-DIY” policies where appropriate
4) **Testability** — every skill/module has:
   - a rubric/checklist
   - a way to self-assess
   - criteria for progression
5) **Drift control** — policy/standards modules have review cadence and change logs.

## measurable indicators

### module completeness score (0–100)
For modules with numeric expectations, compute:

- artifacts_present = sum(min(present_i, expected_i)) / sum(expected_i)
- score = artifacts_present × 100

(ODA can extend this later with weights for risk, evidence, and freshness.)

### evidence coverage (target ratios)
- EVIDENCE claims ≥ 60% for **law/standards/rulebooks**
- EVIDENCE claims ≥ 40% for **health** (with referral triggers)
- INFERENCE allowed for internal design, but must be labeled

### safety coverage
- 100% of modules with Risk = high must have:
  - safety boundary doc
  - referral trigger list
  - “not medical advice / not legal advice” disclaimers when relevant

### freshness / drift
- legal sources: review every 6–12 months
- venue rulebooks: review every 12 months (or on major revision)
- medical/first-aid: review every 6–12 months

## verification loop

1. **Index audit**: every file path registered in `research/index.yml`.
2. **Coverage audit**: `exports/2026-01-10/coverage_matrix.csv` shows completeness score.
3. **Source audit**: every doc front matter `sources:` ids exist in source register.
4. **Claim audit**: `ai_handoff_corpus.jsonl` chunks reference only registered sources.
5. **Drift watch**: update `70_ops/dash_drift_watch.md` with next_review_date for high-change domains.
