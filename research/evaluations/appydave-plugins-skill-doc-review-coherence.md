---
artifact_id: appydave-plugins:skill:doc-review-coherence
repo: appydave-plugins
artifact_type: skill
cluster_facet: [code-review, documentation]
phase_fit: [6, 7]
evaluated_at: 2026-05-17
---

# Eval: doc-review-coherence

**Intent**: Find contradictions, drift, tonal shifts, and implicit conflicts across a documentation corpus — things that are present but disagree.

## Scores
- **quality_score**: 4 — The four-category taxonomy (contradictions / drift / tonal shifts / implicit conflicts) is precise and non-overlapping. The concept-map build step (key terms → which files define or reference them) is the right methodology for cross-doc consistency checking. The distinction from doc-review-gaps ("not broken links or missing files — CH finds things that are present but disagree") is crisp. Loses one point for being a leaf skill with limited standalone value — it's most useful as part of the orchestrated suite.
- **adoption_fit_final**: strong — Part of David's doc-review suite; already in use.
- **inspiration_value**: mid — The "implicit conflicts" category (no direct contradiction, but reading both creates confusion) is the most nuanced and underappreciated finding type. Worth mining.
- **uniqueness_refined**: uncommon — The concept-map methodology for cross-document consistency is differentiated.
- **composability**: called-by-others — Designed to be launched as a background agent by doc-review orchestrator. Can run standalone.
- **description_craft_refined**: trigger — Description clearly distinguishes CH from GL. Trigger phrases are precise.

## Mineable phrasing
> "CH finds things that are *present* but *disagree*" / "Implicit conflicts — No direct contradiction, but reading Doc A then Doc B creates confusion"

## Notes
The "implicit conflicts" category is the hardest to find and the most valuable — it captures documentation that is technically correct in isolation but misleading in combination. The drift category (especially "We plan to..." language for things that already happened or never did) is a common real-world issue that most review tools miss. The concept-map build step is a practical methodology that prevents false-negative coherence checks.
