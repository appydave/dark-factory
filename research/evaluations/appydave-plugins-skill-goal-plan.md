---
artifact_id: appydave-plugins:skill:goal-plan
repo: appydave-plugins
artifact_type: skill
cluster_facet: [planning, spec-writing, test-authoring]
phase_fit: [1, 2, 4]
evaluated_at: 2026-05-17
---

# Eval: goal-plan

**Intent**: Walk the user through a structured 6-section interview to produce both a plan markdown document and a paste-ready `/goal` condition for Claude Code's autonomous executor feature.

## Scores
- **quality_score**: 5 — Tightly scoped, non-overlapping artifacts (plan.md + goal.txt), mode-switching interview pattern, explicit "does NOT execute" boundary, and absolute-path discipline are all production-craft signals.
- **adoption_fit_final**: strong — Already David's own skill; no stack friction. Directly feeds Ralphy's Mode 2 / 3 handoff chain and the `/goal` autonomous loop.
- **inspiration_value**: high — The idea of producing two artefacts from one interview (human-readable plan + machine-readable /goal condition) is a compound output pattern worth mining.
- **uniqueness_refined**: rare — Combining structured spec interview with /goal condition generation in a single skill is found nowhere else in the corpus; this is a named harness-version-specific pattern (v2.1.139+).
- **composability**: calls-others — References mode-specific question files and a plan template; designed to hand off to `/goal` as downstream executor.
- **description_craft_refined**: trigger — Description lists nine distinct trigger phrases and four modes up front; correctly uses "Use when..." phrasing throughout.

## Mineable phrasing
> "Does NOT execute the plan; produces the inputs that /goal then runs."

## Notes
The explicit "boundary statement" (what the skill deliberately does NOT do) is a mature craft pattern — it prevents scope creep and clarifies the handoff contract. The two-artifact output (plan.md + goal.txt) is a reusable compound-output pattern applicable across any planning skill. The per-mode reference files (code/content/research/freeform) show progressive-disclosure done correctly — heavy content deferred to referenced files, keeping SKILL.md scannable.
