---
artifact_id: agent-skills-osmani:skill:planning-and-task-breakdown
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [task-planning, vertical-slicing, spec-requirements]
phase_fit: [1]
evaluated_at: 2026-05-17
---

# Eval: planning-and-task-breakdown

**Intent**: Decomposes validated specs into verifiable tasks using dependency-graph ordering and vertical slicing (one complete feature path per task), with explicit sizing guidelines and human-review checkpoints.

## Scores

- **quality_score**: 4. Dependency graph diagram, vertical vs. horizontal slicing contrast, XS/S/M/L/XL size table, break-down triggers ("and" in title = two tasks). Solid. Docked one point: slightly generic compared to interview-me and idea-refine in this batch.
- **adoption_fit_final**: `strong`. Fully process-based, stack-agnostic; the vertical slicing principle applies universally.
- **inspiration_value**: `mid`. The "if you write 'and' in the task title, it's two tasks" heuristic is a clean, memorable rule.
- **uniqueness_refined**: `commodity`. Vertical slicing and dependency graphs are well-established planning practices; the skill packages them well but introduces little new mechanism.
- **composability**: `called-by-others`. Spec-driven-development calls this as Phase 3; the /plan command invokes it directly.
- **description_craft_refined**: `trigger`. Four concrete trigger scenarios, including the useful negative ("when NOT to use").

## Mineable phrasing

> "If you find yourself writing 'and' in the task title — that's a sign it is two tasks."

## Notes

The distinction between "safe to parallelize" vs. "must be sequential" vs. "needs coordination" in the parallelization section is a useful three-category framework for multi-agent task assignment. The checkpoint-every-2-3-tasks structure is enforced as a template element, not just recommended — that makes it structural rather than advisory.
