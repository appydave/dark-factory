---
artifact_id: appydave-plugins:skill:ralphy
repo: appydave-plugins
artifact_type: skill
cluster_facet: [orchestration, planning, spec-writing]
phase_fit: [1, 2, 9]
evaluated_at: 2026-05-17
---

# Eval: ralphy

**Intent**: Run autonomous batch development campaigns on existing projects using a directive coordinator loop with four modes (Requirements, Plan, Build, Extend) and three campaign profiles (Development, Analysis, Content).

## Scores
- **quality_score**: 5 — The most complete autonomous-campaign orchestrator in the corpus. Hard-gate architecture (A/B/C), per-task two-stage review (spec compliance before code quality), deliberate subagent context exclusion, efficiency observer, and KDD auto-promotion all reflect sustained production use. At ~860 lines it is the largest skill in the corpus and justifiably so.
- **adoption_fit_final**: strong — David's primary execution loop. No adoption required; it already runs campaigns. The profile system (Development/Analysis/Content) and Project Heal retroactive backlog builder are particularly mature.
- **inspiration_value**: high — Multiple mineable patterns: hard-gate state machine, subagent context exclusion rules, AGENTS.md inheritance (never rebuild from scratch), campaign lifecycle artifacts (BACKLOG.md, assessment.md, next-round-brief.md), and the efficiency observer's three-dimension model.
- **uniqueness_refined**: rare — The combination of profile-scoped AGENTS.md, hard gates with anti-rationalization tables, and loop meta-learning capture is not found as a complete system anywhere else in the evaluated corpus.
- **composability**: calls-others — Invokes delivery-review, architectural-review, code-quality-audit, and other skills as sub-systems at named lifecycle gates.
- **description_craft_refined**: trigger — Description covers four modes, three profiles, and twelve trigger phrases; the "Be directive" orientation statement distinguishes it from passive skills.

## Mineable phrasing
> "Subagents are defined by what they DON'T receive — task agents get task text + AGENTS.md only."

## Notes
The "deliberate context exclusion" principle (agents receive only task scope + AGENTS.md; no plan, no sibling results, no prior wave outcomes) is the single most transferable architectural insight in the stage 2 batch. It solves a real multi-agent integration failure mode: agents compensating for each other when they can see sibling work. The hard-gate state machine with three non-bypassable checkpoints and explicit anti-rationalization tables is a governance pattern that deserves its own distillation. The `#18` principle ("Never decline lifecycle tracking — even a 1-work-unit campaign with proper tracking is better than a quick fix") is a strong philosophical statement about compounding system value.
