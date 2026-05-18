---
artifact_id: appydave-plugins:skill:architectural-review
repo: appydave-plugins
artifact_type: skill
cluster_facet: [code-review, documentation, planning]
phase_fit: [1, 2, 6, 7]
evaluated_at: 2026-05-17
---

# Eval: architectural-review

**Intent**: Predictive structural review of a codebase anchored to the next planned feature — not what's wrong now, but what structural traps will hurt next.

## Scores
- **quality_score**: 5 — Exceptional framing. The upfront question ("What is the next major feature?") anchors the entire review to a concrete future state — this is the differentiator that makes it predictive rather than reactive. The reactive/predictive distinction is crisp. A-D grading + top-5 concerns + readiness verdict is a complete and actionable output contract.
- **adoption_fit_final**: strong — Sits alongside code-quality-audit and test-quality-audit as the third lens; David already has both sisters. Clean integration story.
- **inspiration_value**: high — The feature-anchored review framing is the highest-signal idea in this stage. "What happens to this structure when the next feature arrives?" is a transferable evaluation principle.
- **uniqueness_refined**: uncommon — Agent Skills Osmani has an architectural review skill but does not anchor to next feature explicitly. This framing is genuinely differentiated.
- **composability**: called-by-others — Designed to be run alongside code-quality-audit and test-quality-audit as part of a three-skill review set.
- **description_craft_refined**: trigger — Description has strong trigger vocabulary (God class, responsibility review, before adding a major feature). The "does NOT replace" clarification is excellent.

## Mineable phrasing
> "code quality is reactive (what's wrong now). Architectural review is predictive (where is complexity heading, what structural traps will hurt when the next feature arrives)."

## Notes
The principle of anchoring a structural review to a concrete future scenario rather than current state is the highest-quality idea in stages 7+8. The A–D grade + top-5 structural concerns + readiness verdict pattern is directly portable to any review skill. The references/ architecture (criteria.md, output-template.md) keeps the SKILL.md clean without losing depth.
