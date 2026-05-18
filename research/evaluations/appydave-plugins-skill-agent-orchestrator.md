---
artifact_id: appydave-plugins:skill:agent-orchestrator
repo: appydave-plugins
artifact_type: skill
cluster_facet: [documentation, orchestration, workflow-architecture]
phase_fit: [2, 6, 7, 9]
evaluated_at: 2026-05-17
---

# Eval: agent-orchestrator

**Intent**: Design advisor that elicits multi-agent workflow requirements from the user and produces infrastructure start block, paste-ready orchestrator command sequence, gate definitions, diagnostic contracts, and agent prompt additions — for Claude Code teammate mode.

## Scores
- **quality_score**: 4 — Well-structured design advisor with a five-step elicitation process, clear gate taxonomy (Human required / Auto-proceed with condition / Conditional loop), diagnostic reporting contract concept, and orchestrator system prompt template. The reference-file architecture (infrastructure.md, diagnostic-contract.md, orchestrator-system-prompt.md) shows mature separation of concerns. Slightly weaker on runtime mechanism specifics — delegates to reference files that weren't read.
- **adoption_fit_final**: strong — This is David's own skill in his current stack. The evaluation question is whether Osmani's `/ship` or other orchestration mechanisms would upgrade or replace elements of it. The gate taxonomy and diagnostic contract pattern are the distinctive elements worth preserving at distillation.
- **inspiration_value**: mid — The diagnostic contract concept (each agent has a defined "reporting back" format that the orchestrator depends on) is a useful abstraction. The gate taxonomy (three types with explicit trigger conditions) is cleaner than most workflow descriptions.
- **uniqueness_refined**: uncommon — The diagnostic contract pattern (per-agent structured report format defined before orchestration begins) is not common in the corpus. Most orchestration artifacts describe dispatch but not the return contract.
- **composability**: standalone — This is a design advisor, not a runtime executor. Produces artifacts for human review and implementation, doesn't call other skills.
- **description_craft_refined**: trigger — Description has 9 explicit trigger phrases ("design a multi-agent workflow", "set up agent orchestration", etc.) covering the full vocabulary space. Strong trigger coverage, possibly over-specified.

## Mineable phrasing
> `none` — The key mechanism (diagnostic contract) lives in reference files not read; no quotable phrasing surfaced from SKILL.md alone.

## Notes
This is David's existing skill, so the evaluation is about its standing relative to the Osmani cluster. The diagnostic contract concept (structured return format per agent, defined at design time) is the most distinctive mechanism and worth preserving in any unified orchestration skill. The gate taxonomy (human / auto / conditional loop) maps cleanly to the phase-fit across stages 2, 6, 7, 9. At distillation, compare this directly with `/ship`'s three-phase fan-out: they solve different levels of the orchestration problem — this is design-time advisor, `/ship` is runtime executor.
