---
artifact_id: agent-skills-osmani:skill:deprecation-and-migration
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [refactor, delivery-readiness]
phase_fit: [4, 6]
evaluated_at: 2026-05-17
---

# Eval: deprecation-and-migration

**Intent**: Manages safe removal of old systems and migration of users from deprecated to new implementations with structured decision criteria.

## Scores
- **quality_score**: 4 — Strong conceptual framing (Hyrum's Law, Zombie Code, Churn Rule), structured decision checklist, three migration patterns (Strangler, Adapter, Feature Flag). Slightly less applicable to solo/small-team work where most deprecations are internal.
- **adoption_fit_final**: mid — Valuable for FliVideo (Ruby → Node migrations, API versioning) and kybernesis (SaaS versioning), but David's solo/small team context means the "announce and document" ceremony overhead is lighter. Core patterns (strangler, feature flag) are universally useful.
- **inspiration_value**: mid
- **uniqueness_refined**: uncommon — The "Zombie Code" section and the Churn Rule ("if you own the infrastructure, you are responsible for migrating your users") are genuinely sharp articulations.
- **composability**: standalone — Can be used independently; no required companion skill.
- **description_craft_refined**: trigger — Three "Use when" trigger lines.

## Mineable phrasing
> "Code is a liability, not an asset. Every line of code has ongoing maintenance cost."

## Notes
The Hyrum's Law reference grounds the "why migration is hard" case precisely. The compulsory vs advisory deprecation distinction is valuable and rarely explicit. Zombie code definition (no owner but active consumers, failing tests nobody fixes) is a useful checklist for David's brain maintenance work as well as codebase hygiene.
