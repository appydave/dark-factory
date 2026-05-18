---
distillation_id: workflow-architecture-agent-team-composer
stage: workflow-architecture
intent: "Compose the right agent team for a complex task — assign roles, define handoffs, choose execution topology (sequential vs parallel vs reviewer-separated)"
created: 2026-05-17
status: draft
source_artifacts:
  - appydave-plugins:skill:bmad-story-lifecycle
  - bmad-method:skill:bmad-agent-architect
  - compound-engineering:agent:ce-architecture-strategist
  - everything-claude-code:skill:agentic-os
  - everything-claude-code:skill:plan-orchestrate
  - everything-claude-code:command:multi-workflow
  - everything-claude-code:command:feature-dev
  - ruflo:agent:workflow-specialist
winner_mechanism: appydave-plugins:skill:bmad-story-lifecycle
---

# Unified Skill: agent-team-composer

**Purpose**: Design-time composition of a named agent team for a complex task — each agent gets a role, a trigger condition, a handoff contract, and an execution mode (sequential / parallel / reviewer-separated). Output is a paste-ready team setup block + execution sequence, not the execution itself.

**For Agents**: Use when David has a multi-role task and says "who should handle this", "design the agent team", "I need multiple agents for this", "what's the team for X", "set up the agents", or is starting a BMAD story / complex feature that needs explicit role assignment before running.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Before spinning up agents, decide: who does what, in what order, with what handoff, and with which topology check (reviewer never reads from implementer's session). Output a setup block David can paste to launch the team.

**Design-time vs runtime**: This skill designs the team. `orchestration-autonomous-pipeline-runner` (already distilled) executes it. These are adjacent but distinct — the design artifact (roles + topology + handoffs) is the input to the runtime.

**Overlap note**: This skill overlaps with `orchestration-workflow-design-advisor` (already distilled) at the broad "topology choice" level. The distinction: `workflow-design-advisor` answers "sequential or swarm?" (the structural question); `agent-team-composer` answers "given it's a swarm, which agents and what are their roles?" (the personnel question). They sequence: design-advisor → team-composer → pipeline-runner.

## Winner's Mechanism

`appydave-plugins:skill:bmad-story-lifecycle` wins because it is the most complete production-tested agent team composition in David's stack. It defines a named 7-agent team (Swagger/Bob/Amelia/Nate/Taylor/Lisa), each with a role, execution mode (Agent Teams vs in-context fallback), environment detection, and explicit human gates. It also handles the "partial team" case (start from Amelia, skip Bob) via the `--start-from` flag.

The environment detection block (`echo "TMUX=... AGENT_TEAMS=..."`) is load-bearing — it's a pattern for any multi-mode skill that needs to know what harness capabilities are available before designing the team.

`plan-orchestrate` (ECC) contributes the **catalogue-lookup pattern**: given a task description, look up which named agents (from a fixed catalogue) best fit each step. This prevents inventing agent names ad hoc.

`feature-dev` (ECC) contributes the **4-phase handoff shape**: explorer → architect → implementer → reviewer. Simple and reusable for any feature-level task.

`multi-workflow` (ECC) contributes the **parallel-vs-sequential routing decision** at the team level: when does each model/agent run in parallel vs wait for a predecessor? The `run_in_background: true` + `TaskOutput` wait pattern is the mechanism. (Note: `multi-workflow` uses external Codex/Gemini models, not Claude subagents — the *pattern* is portable even if the implementation isn't.)

## Non-overlapping ideas folded in

- From `plan-orchestrate`: **Skill-catalogue lookup for step→agent mapping** — `complexity: medium | optional: true | prerequisite: "ECC skills catalogue is installed or a local catalogue exists"`. Rather than ad-hoc agent naming, look up the best-fit skill from a catalogue for each plan step. Produces consistent, reusable agent names vs one-off inventions.
- From `feature-dev`: **Explorer→Architect→Implementer→Reviewer default composition** — `complexity: low | optional: false | prerequisite: none`. When no custom team is specified, fall back to this 4-role shape. Simple and universally applicable.
- From `multi-workflow`: **Explicit parallel wait contract** (start background, collect output, proceed) — `complexity: medium | optional: true | prerequisite: "parallel execution available"`. Make the wait-for-parallel-agents contract explicit in the team definition. Prevents the "agents ran but results were lost" failure mode.
- From `bmad-agent-architect` (bmad): **Architecture decision record embedded in team design** — `complexity: medium | optional: true | prerequisite: "team is for a Large/XL feature"`. For complex teams, write a 2-3 sentence ADR explaining WHY this team composition was chosen. Useful when the same team is rerun weeks later.
- From `ce-architecture-strategist` (CE): **Compliance gate in team definition** — `complexity: medium | optional: true | prerequisite: "project has explicit architecture patterns (BMAD, DDD, etc.)"`. Include a reviewer role whose sole job is checking that the implementer's output conforms to the project's architecture pattern. The architect's gate, not a code reviewer.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| bmad-story-lifecycle (appydave) | Named team with roles + modes + gates + partial-team flag, environment detection pattern | BMAD-specific agent names (Bob/Amelia/etc.) |
| plan-orchestrate (ECC) | Catalogue-lookup for step→agent mapping, ECC agent catalogue | ECC-specific /orchestrate command syntax |
| feature-dev (ECC) | Explorer→Architect→Implementer→Reviewer default shape | ECC-specific code-explorer/code-architect agents |
| multi-workflow (ECC) | Parallel wait contract (background + collect) | External Codex/Gemini model infrastructure |
| bmad-agent-architect (bmad) | ADR embedded in team definition | Full BMAD system architect persona |
| ce-architecture-strategist (CE) | Compliance gate role in team | CE-specific pattern compliance checks |

## Draft SKILL.md frontmatter

```yaml
name: agent-team-composer
description: >
  Compose the right agent team for a complex task — assign roles (explorer, architect,
  implementer, reviewer, compliance-gate), define handoffs and execution modes
  (sequential/parallel/reviewer-separated), and emit a paste-ready team setup block.
  Design-time only — does not execute the team.
  Use when: "design the agent team", "who should handle this", "set up the agents",
  "I need multiple agents", "what roles do I need", or starting any multi-agent task.
argument-hint: "[task-description | path/to/plan.md]"
allowed-tools: "Read, Bash(echo:*), Bash(cat:*)"
```

## Open questions for David

1. **Skill catalogue**: Should `agent-team-composer` reference a local catalogue of David's known skills (appydave-plugins inventory) to suggest agents by name? Or is "describe the role" sufficient and the user maps to a specific skill later?

2. **Environment detection**: The BMAD story lifecycle's environment detection block (AGENT_TEAMS / TMUX / VISIBLE_PANES) is load-bearing for mode selection. Should `agent-team-composer` always emit this block as part of the setup output, or only when the team needs parallel execution?

3. **Boundary with workflow-design-advisor**: The orchestration distill already produced `workflow-design-advisor` (topology selection). This skill is the next layer (role assignment). Should they be one skill or two? Two is more composable; one is more ergonomic for simple cases.
