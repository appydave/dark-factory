---
artifact_id: agent-skills-osmani:command:build
repo: agent-skills
artifact_type: command
cluster_facet: [agent-skills-osmani, tdd-workflow, incremental-build]
phase_fit: [stage-3]
evaluated_at: 2026-05-17
---

# Eval: build (command)

**Intent**: Implements one pending task using TDD red-green-refactor loop, then commits and marks it done.

## Scores
- **quality_score**: 3 — Thin orchestrator that delegates to two other skills; value is in the composition, not the command itself
- **adoption_fit_final**: mid — Assumes `agent-skills` plugin ecosystem is installed; discipline is portable but invocation is stack-locked
- **inspiration_value**: mid — TDD-per-task cadence is the interesting pattern; the command itself is boilerplate
- **uniqueness_refined**: uncommon — Most harnesses lack an explicit per-task TDD commit loop as a named command
- **composability**: calls-others — Invokes `incremental-implementation` + `test-driven-development` skills; delegates error recovery too
- **description_craft_refined**: trigger — "Implement the next task incrementally — build, test, verify, commit" is clean and activatable

## Mineable phrasing
> "Pick the next pending task from the plan."

## Notes
The real value is the RED-GREEN-commit granularity enforced at each task boundary, not the command wrapper. Phrasing "Pick the next pending task" is a reusable micro-pattern for any plan-driven agent loop. Weak standalone — only meaningful when the full agent-skills ecosystem is present.
