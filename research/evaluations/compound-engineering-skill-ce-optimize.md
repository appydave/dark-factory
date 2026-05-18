---
artifact_id: compound-engineering:skill:ce-optimize
repo: compound-engineering-plugin
artifact_type: skill
cluster_facet: [compound-engineering, optimization-loop, metric-driven, llm-as-judge]
phase_fit: [stage-10]
evaluated_at: 2026-05-17
---

# Eval: ce-optimize

**Intent**: Runs a multi-phase metric-driven optimization loop (hard metrics or LLM-as-judge) with crash-safe disk persistence and parallel git worktree experiments.

## Scores
- **quality_score**: 5 — Exceptionally complete: 4-phase structure, 6 mandatory disk checkpoints, crash recovery, parallelism probe, LLM-judge stratification, runner-up cherry-pick logic, budget caps
- **adoption_fit_final**: strong — Mechanism is fully portable (worktree + measurement command); not locked to any stack
- **inspiration_value**: high — Disk-first persistence discipline ("conversation is NOT durable storage") and hard/judge metric split are directly teachable patterns
- **uniqueness_refined**: rare — No other artifact in this catalog combines iterative experiment loops with judge-as-primary-metric and verifiable write-then-read checkpoints
- **composability**: calls-others — Dispatches `ce-learnings-researcher`, `ce-repo-research-analyst`, experiment subagents, and judge subagents
- **description_craft_refined**: trigger — Description is long but precise; includes concrete optimization targets (clustering, search, build)

## Mineable phrasing
> "The conversation context is NOT durable storage. Results that exist only in the conversation WILL be lost."

## Notes
The persistence discipline section alone is worth extracting as a standalone dark-factory pattern: write-then-verify before presenting results, per-experiment crash-recovery markers, and re-read from disk at every phase boundary. The hard/judge metric decision tree (quantitative vs qualitative) is also a high-value teachable heuristic. Standout artifact in this batch.
