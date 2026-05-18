---
artifact_id: appydave-plugins:skill:doc-review-crossref
repo: appydave-plugins
artifact_type: skill
cluster_facet: [code-review, documentation, knowledge-capture]
phase_fit: [6, 7, 8]
evaluated_at: 2026-05-17
---

# Eval: doc-review-crossref

**Intent**: Verify cross-reference integrity — confirm that referenced content still says what the referencing document thinks it says, beyond just whether links resolve.

## Scores
- **quality_score**: 4 — The distinction from GL ("not whether links work — whether the referenced content still says what the referencing doc thinks it says") is the key insight and it's crisp. The staleness threshold table with domain-velocity override (Claude Code = shorter thresholds than BMAD) is a practical calibration mechanism. Provenance chain verification (brain → source → upstream) aligns directly with David's knowledge management system.
- **adoption_fit_final**: strong — Directly applies to David's brains system, which has explicit provenance requirements.
- **inspiration_value**: mid — The "domain velocity" concept for staleness thresholds is the most portable idea. A high-churn domain needs shorter staleness windows than a stable one.
- **uniqueness_refined**: uncommon — Content-accuracy-of-references (as opposed to link resolution) is underrepresented in review tools.
- **composability**: called-by-others — Background agent in doc-review orchestrator.
- **description_craft_refined**: trigger — "Provenance chain", "examples accurate", "index sync" are precise trigger vocabulary.

## Mineable phrasing
> "Not whether links *work* (GL handles dead links) — whether the referenced content **still says what the referencing doc thinks it says**" / domain velocity staleness thresholds

## Notes
The staleness threshold table (< 1 month = no flag, > 12 months = critical) combined with domain-velocity override is a reusable calibration pattern for any time-sensitive document corpus. The provenance chain dimension (brain references upstream source, skill references brain) aligns exactly with David's knowledge system layering. "New in..." or "Since v3..." language that is no longer newsworthy is a common real-world noise pattern that this dimension specifically catches.
