---
artifact_id: agent-skills-osmani:command:review
repo: agent-skills-osmani
artifact_type: command
cluster_facet: [code-review]
phase_fit: [6]
evaluated_at: 2026-05-17
---

# Eval: /review (command)

**Intent**: Thin orchestration entry point that invokes the `code-review-and-quality` skill to evaluate staged or recent changes across five quality axes — user-typed command form of the review workflow.

## Scores
- **quality_score**: 2 — Deliberately minimal: 7 lines, no new mechanism, pure delegation to the skill. Quality as a standalone artifact is low — it only has value in its role as the user-typed entry point that routes to the richer skill. No independent innovation.
- **adoption_fit_final**: mid — The command form factor (user types `/review`) is useful as a quick-invoke shortcut distinct from the skill's auto-trigger behavior. David's existing `review-code-quality` skill handles the same intent. This adds the explicit command-type entry point but minimal new substance.
- **inspiration_value**: low — No novel mechanism or phrasing. Value is entirely structural (demonstrates the command-as-thin-orchestrator pattern).
- **uniqueness_refined**: commodity — A thin forwarding command that delegates to a skill is a standard pattern. The mechanism is identical to dozens of similar slash commands.
- **composability**: calls-others — Delegates entirely to the `code-review-and-quality` skill. The command's only job is routing.
- **description_craft_refined**: summary — "Conduct a five-axis code review — correctness, readability, architecture, security, performance." Describes what it does rather than when to invoke it.

## Mineable phrasing
> `none`

## Notes
This artifact's value is architectural rather than content-based: it demonstrates the command-as-thin-orchestrator pattern where the command handles user invocation and the skill handles the knowledge. This separation (commands for recall-based invocation, skills for capability) matches the agentic-capability design advisor's decision framework. At distillation time, this should be noted as the command-layer entry point but not treated as a mechanism winner — the skill is the mechanism.
