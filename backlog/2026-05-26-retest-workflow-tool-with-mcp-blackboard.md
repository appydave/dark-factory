# Retest Workflow Tool performance with MCP blackboard

## Context

The 284s measurement in `experiments/ylo/README.md` (probe #2 comparison) was made against the **bash blackboard** (no MCP). The 5× regression was caused by the Workflow VM having no filesystem access — every store write was a full agent round-trip.

Since then, R11/R12 confirmed that Workflow Tool subagents CAN call MCP tools directly (verified 2026-05-25 via `hello-blackboard` workflow — 29s, 2 agents). The root cause of the performance gap is now removable.

## What needs to happen

1. Rebuild probe #2 (title-gen) using Workflow Tool + MCP blackboard (not bash)
2. Measure wall-clock, agent count, token count against the same b65 scenario
3. Compare to original bash blackboard (~56s, 2 agents)
4. Update `experiments/ylo/README.md` with the new numbers
5. Re-evaluate the Hybrid recommendation — it may no longer hold

## Why this matters

The Hybrid recommendation (WT for fan-out, Blackboard for sequential) was grounded in the 284s number. If MCP blackboard eliminates the regression, the picture changes. We may not need the Hybrid at all.

## Status

Open — not started
