---
artifact_id: appydave-plugins:skill:codebase-audit
repo: appydave-plugins
artifact_type: skill
cluster_facet: [code-review, orchestration, test-authoring]
phase_fit: [4, 6, 9]
evaluated_at: 2026-05-17
---

# Eval: codebase-audit

**Intent**: Three-lens codebase audit orchestrator — spawns code quality, test quality, and architectural review as parallel subagents and synthesises into a combined readiness verdict.

## Scores

- **quality_score**: 4 — The orchestration pattern is sound: three independent subagents (each with a full context window), explicit prompts for each subagent embedded in the skill, synthesis that cross-references findings across lenses (cross-lens issues rank higher), and a compound readiness verdict. The subagent prompts are complete enough that they can run without reading additional files. The "For partial audits, use individual skills directly — this orchestrator is for full three-lens reviews only" scope note prevents scope confusion. Deduction: the architectural review subagent prompt is slightly weaker than the code quality and test quality prompts (less dimensional specificity).
- **adoption_fit_final**: strong — Already in David's stack. The three-lens parallel-subagent orchestration pattern with synthesis is directly usable for any multi-perspective audit.
- **inspiration_value**: mid — The cross-lens synthesis step (issues appearing in 2+ lenses rank highest) is a useful compounding heuristic. The "any D or BLOCKER → NOT READY" compound verdict rule is clean.
- **uniqueness_refined**: uncommon — The combination of parallel subagents + cross-lens deduplication + compound verdict is not common in audit skills. Most multi-audit skills either run sequentially or just concatenate outputs.
- **composability**: calls-others — Spawns three subagents via the Agent tool. Acts as a root orchestrator.
- **description_craft_refined**: trigger — Effective disambiguation of when to use this vs individual audit skills. Clear.

## Mineable phrasing

`none`

## Notes

The skill is a direct application of the orchestration-topology prompt pattern: spawn parallel subagents for independent concerns, synthesise in main thread. The embedded subagent prompts (not references to external files) make this skill fully self-contained — a subagent can run without cross-skill path dependencies. The cross-lens ranking heuristic (2+ lenses = higher priority) is a simple but effective synthesis rule. No Ruflo dependency.
