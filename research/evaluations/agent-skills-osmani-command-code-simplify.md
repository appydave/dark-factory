---
artifact_id: agent-skills-osmani:command:code-simplify
repo: agent-skills-osmani
artifact_type: command
cluster_facet: [refactor]
phase_fit: [4]
evaluated_at: 2026-05-17
---

# Eval: code-simplify (command)

**Intent**: Orchestration entry point that invokes `code-simplification` to reduce complexity while preserving exact behavior, with a six-step incremental procedure.

## Scores
- **quality_score**: 3 — Clean six-step procedure that adds slightly more orchestration detail than the pure skill delegation model. "Run tests after each change" embedded in the step sequence is helpful. Ends with a `code-review-and-quality` call which creates a quality chain.
- **adoption_fit_final**: mid — Useful command pattern but the mechanism is in the skill. David's existing `simplify` skill is the local equivalent.
- **inspiration_value**: low
- **uniqueness_refined**: commodity — Command dispatch pattern; the six steps are a condensed restatement of the skill's procedure.
- **composability**: calls-others — Delegates to `code-simplification`; chains to `code-review-and-quality` for result validation.
- **description_craft_refined**: summary — "Reduce complexity without changing behavior" is a summary statement.

## Mineable phrasing
`none`

## Notes
The `code-review-and-quality` tail call (verify the result after simplifying) is a useful composition model — simplify then review forms a quality chain. This is the main non-redundant idea vs the underlying skill. In distillation this folds into the command wrapper layer.
