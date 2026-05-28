---
distillation_id: orchestration-agent-lifecycle-coordinator
stage: orchestration
intent: "Spawn, monitor, balance load across, and safely terminate agents — runtime management of a live agent pool"
created: 2026-05-16
status: draft
source_artifacts:
  - ruflo:skill:agent-coordination
  - ruflo:agent:autopilot-coordinator
  - ruflo:command:autopilot
  - ruflo:agent:loop-worker-coordinator
  - gbrain:skill:minion-orchestrator
  - everything-claude-code:skill:claude-devfleet
  - everything-claude-code:agent:loop-operator
  - ruflo:skill:agent-load-balancer
  - ruflo:skill:agent-resource-allocator
  - ruflo:skill:agent-sandbox
  - ruflo:skill:agent-scout-explorer
  - ruflo:skill:agent-orchestrator-task
  - ruflo:skill:agent-topology-optimizer
  - ruflo:skill:agent-worker-specialist
  - ruflo:skill:worker-integration
winner_mechanism: gbrain:skill:minion-orchestrator
---

# Unified Skill: agent-lifecycle-coordinator

**Purpose**: Spawn, assign work to, monitor, and safely terminate agents — the runtime management layer for a live agent pool, distinct from topology design (which agent to use) or review (what agents produce).

**For Agents**: Use when David asks about "spawning agents", "monitoring running agents", "stopping a runaway agent", "assigning tasks to workers", "autopilot", or managing an active swarm at runtime.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

## Intent

Manage a pool of agents at runtime: spawn workers for deterministic shell jobs OR LLM subagents for reasoning tasks, monitor health, rebalance load, handle failures, and terminate cleanly.

## Winner's Mechanism

`gbrain:skill:minion-orchestrator` wins for the cleanest dual-mode design: it handles **deterministic shell jobs** (cron, bash scripts) and **LLM subagents** (reasoning tasks) through the same orchestrator interface. This is the real gap in David's stack — he has review orchestrators (fan-out) and pipeline runners (autonomous execution) but no explicit **worker pool manager**. Minion's dual-mode design is the right abstraction.

`ruflo:agent:loop-worker-coordinator` adds health monitoring + dispatch across loop and cron execution modes — the "keep-alive" layer that detects stalled workers.

## Non-overlapping ideas folded in

- From `ruflo:agent:loop-worker-coordinator`: **Health monitoring + stall detection** — worker heartbeat, auto-restart on stall, report on slow workers. Minion doesn't have this; it's the production-grade addition.
- From `everything-claude-code:skill:claude-devfleet`: **Isolated worktree per agent** — each agent works in its own git worktree, preventing file conflicts in parallel execution. Critical for code-writing agents.
- From `ruflo:skill:agent-load-balancer`: **Task queue + load balancing** — route tasks to least-loaded worker, not just next-available. Useful when worker pool is heterogeneous.
- From `ruflo:skill:agent-sandbox`: **Sandboxed agent** for untrusted task execution — run risky operations in isolation before committing results to main context.
- From `ruflo:agent:autopilot-coordinator`: **Autopilot mode** — enable/disable autonomous task completion; safety layer for hands-off campaigns.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| gbrain:minion-orchestrator | Dual-mode (shell + LLM) worker dispatch | GBrain-specific persistence (Supabase) |
| ruflo:loop-worker-coordinator | Health monitoring, stall detection, restart | Ruflo daemon dependency |
| claude-devfleet | Isolated worktree per parallel agent | ECC-specific DevFleet platform |
| ruflo:agent-load-balancer | Load-balanced task routing | Ruflo worker registry |
| ruflo:agent-sandbox | Sandboxed execution for risky tasks | Ruflo-specific sandbox env |
| ruflo:autopilot-coordinator | Autopilot enable/disable safety layer | /loop MCP tool dependency |
| ruflo:agent-topology-optimizer | Topology evolution at runtime | Ruflo-specific optimizer |

## Draft SKILL.md frontmatter

```yaml
name: agent-lifecycle-coordinator
description: >
  Manage a live agent pool at runtime — spawn workers (shell jobs or LLM subagents),
  monitor health, detect stalls, rebalance load, isolate risky tasks in sandbox,
  and terminate cleanly. Separate from topology design (what structure) and review
  (what agents produce).
  Use when: "spawn agents", "monitor running agents", "worker pool", "autopilot",
  "stop runaway agent", "assign tasks to workers", "health check agents",
  "stalled agent", "agent crashed".
```

## Open questions for David

- Is there a gap here? David has `ralphy` for campaigns and `remote-machines` for cross-machine work — but no explicit **local worker pool manager**. Is this the missing piece between "I have a plan" and "I have running agents"?
- Ruflo's lifecycle coordinator requires the Ruflo daemon — should David's version use Claude Code's native worktree + subagent model instead?
- Does "autopilot" belong here or is it better placed in `autonomous-pipeline-runner`? (It's a safety toggle, not a spawning mechanism.)
