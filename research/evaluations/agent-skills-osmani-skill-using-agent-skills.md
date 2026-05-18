---
artifact_id: agent-skills-osmani:skill:using-agent-skills
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [discovery-routing, skill-authoring]
phase_fit: [9]
evaluated_at: 2026-05-17
---

# Eval: using-agent-skills

**Intent**: Meta-skill injected at session start that provides a decision tree for skill discovery across the full SDLC and enforces six non-negotiable operating behaviors for the agent.

## Scores

- **quality_score**: 4 — The skill does two genuinely distinct things well: (1) a clean ASCII decision tree that routes task type to the right skill at session start, and (2) a strong behavioral constitution (surface assumptions, manage confusion, push back, enforce simplicity, scope discipline, verify). The behavioral section is unusually honest about failure modes like sycophancy and overcomplication. Quality drops slightly because the lifecycle sequence table and quick-reference table are partially redundant with the decision tree.
- **adoption_fit_final**: mid — The skill is tightly coupled to the agent-skills-osmani skill set by name (it routes to skills like `interview-me`, `spec-driven-development`, `context-engineering` etc. that only exist in that collection). The design pattern (meta-skill + behavioral constitution) is directly portable to David's stack, but the routing table must be rebuilt around his actual skills. The behavioral principles section is copy-paste-worthy as-is.
- **inspiration_value**: high — The behavioral constitution section is among the most directly usable material in the whole catalog. "Sycophancy is a failure mode" and the ten failure modes list are the kind of crisp framing that elevates a skill collection from a menu to an opinionated system.
- **uniqueness_refined**: uncommon — Meta-skill + behavioral constitution combo is not common. Most skill collections lack a governing skill that enforces cross-cutting discipline.
- **composability**: called-by-others — This skill is designed to be injected at session start; it is the harness root for the whole collection.
- **description_craft_refined**: trigger — Description correctly identifies both the discovery function and the session-start trigger. Well-formed.

## Mineable phrasing

> "Sycophancy is a failure mode. 'Of course!' followed by implementing a bad idea helps no one. Honest technical disagreement is more valuable than false agreement."

## Notes

The session-start routing tree is the harness-orchestration shape that stage 9 is about. The behavioral constitution is independently valuable — it functions as a "operating principles" inject regardless of which skill handles the task. The failure-modes list (10 items) is a concrete anti-pattern register that David could adapt into a `clauding-lab` or agent-os constitution document. The skill has a Ruflo-free design: no runtime dependency, just load-at-start behavior.
