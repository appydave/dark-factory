---
artifact_id: agent-skills-osmani:skill:performance-optimization
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [code-implementation, verification-validation]
phase_fit: [3, 4, 5, 6]
evaluated_at: 2026-05-17
---

# Eval: performance-optimization

**Intent**: Enforce measure-before-optimise discipline — establish baseline, identify specific bottleneck, fix it, re-measure, guard against regression — never optimising without profiling evidence.

## Scores
- **quality_score**: 5 — Core Web Vitals targets table with thresholds, symptom-to-measurement decision tree (first page load / sluggish interaction / post-navigation / backend API), anti-pattern fix catalogue (N+1, unbounded fetching, missing image optimisation with correct LCP/below-fold picture/img element examples, unnecessary re-renders, large bundles), and performance budget with CI enforcement commands are all production-grade.
- **adoption_fit_final**: strong — Language-agnostic measurement discipline; React/TypeScript examples but the measure→identify→fix→verify→guard workflow and the symptom-tree are universally applicable. Not stack-locked.
- **inspiration_value**: mid — The "where to start measuring" symptom-to-measurement decision tree is the most practical performance triage aid in the corpus. The image optimisation example (art direction + resolution switching + fetchpriority for LCP, loading=lazy for below-fold) is unusually complete.
- **uniqueness_refined**: uncommon — The structured symptom decision tree (what is slow → where to measure first) and the complete picture/img LCP pattern (art direction × resolution switching) are not seen elsewhere at this depth.
- **composability**: standalone — Operates as a set of constraints and measurement procedures; no direct agent sub-invocations.
- **description_craft_refined**: trigger — Description gives four distinct trigger conditions (performance requirements in spec, user reports, Core Web Vitals below thresholds, profiling reveals bottlenecks) plus an explicit "When NOT to use" guard (don't optimise before evidence).

## Mineable phrasing
> "Performance work without measurement is guessing — and guessing leads to premature optimization that adds complexity without improving what matters."

## Notes
The measure-first discipline expressed as "profiling reveals bottlenecks" (not "I suspect a bottleneck") is the key invariant for preventing premature optimisation. The React.memo/useMemo red flag ("overusing is as bad as underusing") is a rare balanced statement in a field where most guidance only warns against one direction. The performance budget section (specific KB targets + CI enforcement commands) converts the general principle into an actionable artefact — this is the distillable pattern: every quality standard should have a CI-enforceable budget.
