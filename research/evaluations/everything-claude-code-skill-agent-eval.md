---
artifact_id: everything-claude-code:skill:agent-eval
repo: everything-claude-code
artifact_type: skill
cluster_facet: [everything-claude-code, agent-benchmarking, comparative-evaluation]
phase_fit: [stage-10]
evaluated_at: 2026-05-17
---

# Eval: agent-eval

**Intent**: CLI tool for head-to-head comparison of coding agents (Claude Code, Aider, Codex, etc.) on YAML-defined tasks, measuring pass rate, cost, time, and consistency via git worktree isolation.

## Scores
- **quality_score**: 4 — Clean YAML task schema, three judge types (deterministic/pattern/LLM), git worktree isolation without Docker, tabular reporting; points off for thin best-practices section and external repo dependency
- **adoption_fit_final**: strong — Stack-agnostic; works against any codebase; `commit: pin` reproducibility pattern applies universally
- **inspiration_value**: high — Frames agent selection as a data problem, not a vibes problem; the 3-trial consistency metric is an underused measurement idea
- **uniqueness_refined**: uncommon — Systematic multi-agent benchmarking on own codebase is rare; most teams use anecdote
- **composability**: standalone — Self-contained CLI; no upstream skill dependencies
- **description_craft_refined**: trigger — "Head-to-head comparison of coding agents" is clear; activation triggers are explicit in "When to Activate"

## Mineable phrasing
> "Every 'which coding agent is best?' comparison runs on vibes — this tool systematizes it."

## Notes
The worktree-per-run isolation pattern (no Docker, full reproducibility) is directly applicable to dark-factory evaluation pipelines. The instruction to track cost alongside pass rate ("95% agent at 10x cost") is a good prioritization heuristic. External repo dependency (github.com/joaquinhuigomez/agent-eval) means adoption requires vetting that repo first.
