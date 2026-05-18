---
artifact_id: agent-skills-osmani:skill:incremental-implementation
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [code-implementation]
phase_fit: [3, 4]
evaluated_at: 2026-05-17
---

# Eval: incremental-implementation

**Intent**: Enforce thin vertical-slice delivery — implement one complete piece, test it, verify it, commit it — never writing more than ~100 lines before testing.

## Scores
- **quality_score**: 5 — Vertical/contract-first/risk-first slicing strategies, five named implementation rules (simplicity first, scope discipline, one thing at a time, compilable invariant, feature flags), and an agent-specific "Be explicit about what's NOT in scope" prompt template are all high-craft. The red flag list ("Running the same build/test command twice in a row without code change" as a waste signal) is unusually precise.
- **adoption_fit_final**: strong — Language/stack agnostic. The "Noticed but not touching" note pattern is directly adoptable. Aligns precisely with Ralphy's Build mode (Mode 3) and the per-task work unit discipline.
- **inspiration_value**: high — "Rule 0.5: Scope Discipline" (do not clean up adjacent code, refactor imports, or modernise syntax in files you're only reading) is a named, scoped anti-pattern category for agents that is not found elsewhere. The "NOTICED BUT NOT TOUCHING" annotation pattern converts implicit restraint into explicit verifiable output.
- **uniqueness_refined**: uncommon — Scope discipline as a named rule with explicit "do NOT" list, plus the "Re-running same command is waste" red flag, are not found in other incremental implementation guidance.
- **composability**: calls-others — References git-workflow-and-versioning for commit guidance; referenced by the `build` command.
- **description_craft_refined**: trigger — Description names both trigger ("any feature or change that touches more than one file") and explicit non-trigger ("When NOT to use: single-file, single-function changes").

## Mineable phrasing
> "If you notice something worth improving outside your task scope, note it — don't fix it."

## Notes
Rule 0 (simplicity first) and Rule 0.5 (scope discipline) together form a two-layer defence against the most common AI agent failure modes: over-engineering and scope creep. The simplicity check table (EventBus vs simple function call; abstract factory vs two components; config-driven form builder vs three forms) is a concrete diagnostic tool rather than a vague quality directive. The red flag "Touching files outside the task scope 'while I'm here'" directly names the scope-creep failure pattern that Ralphy's subagent context exclusion rule also targets — these two skills are complementary at different levels of the stack.
