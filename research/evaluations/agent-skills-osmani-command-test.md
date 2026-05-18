---
artifact_id: agent-skills-osmani:command:test
repo: agent-skills-osmani
artifact_type: command
cluster_facet: [test-authoring]
phase_fit: [4]
evaluated_at: 2026-05-17
---

# Eval: test (command)

**Intent**: Orchestration entry point that invokes `test-driven-development` for new features and the Prove-It pattern for bugs, with a browser-testing addendum for UI issues.

## Scores
- **quality_score**: 3 — Minimal dispatch file; value is entirely in delegation. Clean separation of feature-TDD vs bug-Prove-It as command variants. Browser addendum is the only novel content.
- **adoption_fit_final**: mid — Useful as a slot-in command pattern; David's stack uses slash commands. However, the mechanism lives in `test-driven-development` — this command is thin glue.
- **inspiration_value**: low
- **uniqueness_refined**: commodity — Nearly identical command dispatch pattern appears across multiple repos.
- **composability**: calls-others — Delegates to `test-driven-development` and `browser-testing-with-devtools`.
- **description_craft_refined**: summary — Description is a brief action statement rather than a trigger phrase list.

## Mineable phrasing
`none`

## Notes
The command's value is its branching logic (new features vs bug fixes) rather than unique content. In distillation, this would fold into the command wrapper layer of a unified TDD skill rather than become its own skill. The browser-testing addendum for UI issues is the only non-redundant contribution vs the skill it dispatches to.
