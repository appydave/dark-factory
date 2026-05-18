---
artifact_id: agent-skills-osmani:command:spec
repo: agent-skills-osmani
artifact_type: command
cluster_facet: [spec-writing, entry-point, command-dispatch]
phase_fit: [1]
evaluated_at: 2026-05-17
---

# Eval: spec (command)

**Intent**: Thin entry-point command that invokes spec-driven-development skill, guides four clarifying questions, generates a six-section spec, and saves as SPEC.md.

## Scores

- **quality_score**: 3. Does exactly what a command should do — invoke a skill with a concrete task and output location. Brief and correct. Low score because there's minimal craft here; value lives in the skill it dispatches.
- **adoption_fit_final**: `mid`. The command-as-entry-point-to-skill pattern is broadly applicable; this specific command is a wrapper.
- **inspiration_value**: `low`. No novel mechanism — just the dispatch pattern.
- **uniqueness_refined**: `commodity`. Command that invokes a skill is the standard pattern in agent-skills-osmani.
- **composability**: `calls-others`. Entirely a dispatcher; value is the skill it routes to.
- **description_craft_refined**: `summary`. Description summarizes what it does rather than routing triggers.

## Mineable phrasing

none

## Notes

The command correctly specifies the output location (SPEC.md in project root) and the confirm-before-proceeding step — these are useful conventions for commands that produce persistent artifacts. The four clarifying questions listed in the command body mirror the spec skill's Phase 1 without duplication, which is good layering. Evaluated primarily for completeness; the skill is where evaluation weight should sit.
