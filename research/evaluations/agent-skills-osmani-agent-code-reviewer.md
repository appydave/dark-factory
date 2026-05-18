---
artifact_id: agent-skills-osmani:agent:code-reviewer
repo: agent-skills-osmani
artifact_type: agent
cluster_facet: [code-review]
phase_fit: [6]
evaluated_at: 2026-05-17
---

# Eval: code-reviewer (agent persona)

**Intent**: Staff-Engineer-level persona that conducts thorough five-axis code review and returns categorized, actionable feedback — designed to be dispatched as a subagent by `/review` or `/ship` fan-out.

## Scores
- **quality_score**: 4 — Well-structured persona with clear output template (Review Summary, Critical/Important/Suggestions, What's Done Well, Verification Story), explicit dispatch rules (invoked via `/review` or `/ship`, never from another persona), and a composition constraint that enforces clean orchestration boundaries ("do not invoke from another persona — orchestration belongs to slash commands, not personas"). Slightly thinner than the skill counterpart since it delegates depth to the skill.
- **adoption_fit_final**: mid — David's stack has `review-code-quality` and similar skills. The value here is the orchestration-boundary rule (personas don't cross-call; only commands/skills orchestrate) and the structured output template with mandatory "What's Done Well" section. The persona form factor itself is familiar.
- **inspiration_value**: mid — The "What's Done Well — always include at least one" rule is a concrete quality norm worth borrowing. The composition constraint ("if you find yourself wanting to delegate to security-auditor, surface it as a recommendation instead — orchestration belongs to slash commands") is an excellent boundary enforcement pattern.
- **uniqueness_refined**: uncommon — The explicit orchestration boundary rule ("do not invoke from another persona") is an unusual and high-value design constraint that prevents cascading context explosion in multi-agent systems.
- **composability**: called-by-others — Explicitly designed to be called by `/review` command and `/ship` fan-out. The agent definition enforces this boundary explicitly.
- **description_craft_refined**: trigger — "Use for thorough code review before merge." Minimal but clear. The composition section is where the dispatch semantics actually live.

## Mineable phrasing
> "If you find yourself wanting to delegate to security-auditor or test-engineer, surface that as a recommendation in your report instead — orchestration belongs to slash commands, not personas."

## Notes
The most valuable element of this artifact is the orchestration boundary constraint, not the review framework itself (which duplicates the skill). The rule that personas never dispatch other personas — and that all orchestration must flow through commands/skills — is a clean architectural principle for multi-agent systems. This is mechanism-distinct from the skill even though their review content overlaps: the skill is a knowledge framework, the agent is a dispatch-safe persona. At distillation time, keep both as distinct mechanisms.
