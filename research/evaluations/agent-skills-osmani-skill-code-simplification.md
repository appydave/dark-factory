---
artifact_id: agent-skills-osmani:skill:code-simplification
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [refactor]
phase_fit: [4]
evaluated_at: 2026-05-17
---

# Eval: code-simplification

**Intent**: Reduces code complexity while preserving exact behavior, targeting readability and comprehension speed over line-count reduction.

## Scores
- **quality_score**: 5 — Five named principles, Chesterton's Fence as the anchor concept, language-specific examples (TS/JS/Python/React), the Rule of 500 for automation thresholds, and an anti-rationalization table. Near-complete reference for this domain.
- **adoption_fit_final**: strong — Every project in David's stack benefits from this; the `simplify` skill already exists in the personal skills, so this is the upstream mechanism reference and upgrade candidate.
- **inspiration_value**: high
- **uniqueness_refined**: uncommon — The Chesterton's Fence framing for refactoring and the explicit "comprehension speed not line count" standard are not common in refactoring literature.
- **composability**: called-by-others — The `code-simplify` command delegates to this; intended to be invoked after feature work or code review.
- **description_craft_refined**: trigger — "Use when refactoring… Use when code works but is harder to read… Use when reviewing code that has accumulated unnecessary complexity" — three distinct trigger conditions.

## Mineable phrasing
> "Simplification that breaks project consistency is not simplification — it's churn."

## Notes
The "DAMP over DRY in tests" distinction (borrowed from TDD section) shows well-considered cross-skill coherence. The Rule of 500 for automation is a practical threshold rarely articulated anywhere. David's existing `simplify` skill likely overlaps significantly — this would be the winner mechanism for a unified refactoring skill with the Rule of 500 and Chesterton's Fence folded in.
