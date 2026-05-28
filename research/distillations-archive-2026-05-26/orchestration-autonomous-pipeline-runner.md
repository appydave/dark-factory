---
distillation_id: orchestration-autonomous-pipeline-runner
stage: orchestration
intent: "Run a multi-step plan end-to-end using subagents per task, with mandatory review gates and deliberate context exclusion between tasks"
created: 2026-05-16
status: draft
source_artifacts:
  - superpowers:skill:subagent-driven-development
  - superpowers:skill:dispatching-parallel-agents
  - gsd:command:gsd:autonomous
  - gsd:command:gsd:execute-phase
  - gsd:command:gsd:plan-phase
  - gsd:command:gsd:map-codebase
  - compound-engineering:skill:lfg
  - appydave-plugins:skill:bmad-story-lifecycle
  - appydave-plugins:skill:ralphy
  - everything-claude-code:skill:autonomous-agent-harness
  - ruflo:skill:agent-swarm
  - ruflo:skill:swarm-advanced
  - ruflo:skill:agent-release-swarm
  - ruflo:skill:agent-tdd-london-swarm
  - ruflo:skill:agent-multi-repo-swarm
  - ruflo:command:swarm
winner_mechanism: superpowers:skill:subagent-driven-development
---

# Unified Skill: autonomous-pipeline-runner

**Purpose**: Run a multi-task plan end-to-end using fresh subagents per task — mandatory two-stage review gates, deliberate context exclusion between tasks, anti-rationalization for skipping gates.

**For Agents**: Use when David says "run the whole plan", "execute autonomously", "campaign mode", "ralphy mode", "run phase X", or wants a multi-task execution without hand-holding each step.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

## Intent

Execute a pre-existing task plan end-to-end using fresh-context subagents per task, with mandatory spec-then-quality-review gates between tasks and deliberate isolation of context to prevent cross-task contamination.

## Winner's Mechanism

`superpowers:skill:subagent-driven-development` wins for mechanism clarity. It is the sharpest articulation of three things that matter:

1. **Deliberate context exclusion** — "Subagents are about what is NOT in their context." Each subagent gets only its task text. No plan file. No sibling task context. This is the key architectural decision that keeps subagents clean.
2. **Hard-gate state machine** — spec-first → quality-review gate cannot be skipped. The anti-rationalization table ("I know it works" / "It's a small change") is embedded before the agent forms its excuse.
3. **Two-stage gate** (spec-then-quality-review) — not just "did it work" but "does the implementation satisfy the spec and is it high quality" — separate concerns, separate subagent.

`gsd:execute-phase` adds the dependency-ordered parallel wave model (phases have dependencies, tasks within a phase run in parallel waves) — a concrete scheduling mechanism the Superpowers skill doesn't specify.

## Non-overlapping ideas folded in

- From `gsd:execute-phase`: **Dependency-ordered parallel waves** — tasks within a phase run in parallel if no dependencies; blocked tasks wait. More sophisticated than serial execution.
- From `compound-engineering:skill:lfg`: **Full pipeline in one trigger** (plan → work → code review → commit → push → PR → CI watch) — the "one command does everything" UX worth preserving for David's ralphy/campaign pattern.
- From `gsd:plan-phase`: **Parallel research + planning + verification** before execution — plan quality gate before execution gate. The triple-subagent planning model (researcher, planner, verifier) is folded in as an optional pre-execution step.
- From `everything-claude-code:autonomous-agent-harness`: **Persistent memory + scheduled operations** between autonomous runs — instincts file as cross-run learning accumulator is the self-improving layer missing from Superpowers.
- From `appydave-plugins:skill:ralphy`: **Batch campaign on existing project** — Ralphy's "hands-off until done" UX is the target user experience for David's own tooling; the mechanism is Superpowers, the UX is Ralphy.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| superpowers:subagent-driven-development | Core mechanism: deliberate exclusion, hard gates, anti-rationalization | Superpowers-specific state machine IDs |
| gsd:execute-phase | Dependency-ordered parallel waves within a phase | GSD workspace file format |
| gsd:autonomous | Auto-advance through phases without user hand-holding | GSD-specific pause triggers |
| compound-engineering:lfg | Full pipeline trigger UX: plan→work→review→commit→PR→CI | Flow Nexus platform dep |
| ralphy | Batch campaign UX pattern ("Ralph Wiggum mode") | Ralphy-specific project assumptions |
| autonomous-agent-harness | Cross-run instincts + scheduled operations | ECC-specific infrastructure |
| agent-swarm / swarm-advanced (ruflo) | Swarm as execution primitive for parallel task waves | Ruflo daemon dep |
| bmad-story-lifecycle | BMAD story phases as pipeline steps | BMAD-specific doc format |

## Draft SKILL.md frontmatter

```yaml
name: autonomous-pipeline-runner
description: >
  Run a multi-task plan end-to-end using fresh subagents per task with mandatory
  spec-then-quality-review gates and deliberate context exclusion between tasks.
  Anti-rationalization for gate-skipping is built in.
  Supports dependency-ordered parallel waves within a phase.
  Use when: "run the whole plan", "campaign mode", "execute autonomously",
  "ralphy mode", "run phase", "work through the backlog", "hands-off execution".
```

## Core invariants (for skill body)

1. Each task gets a **fresh subagent** with ONLY its task text — no plan file, no sibling context
2. **Spec gate first**: subagent writes spec before touching code
3. **Quality gate second**: separate quality-review subagent reads spec + implementation
4. **Gates are hard** — anti-rationalization table embedded before execution begins
5. Tasks with no dependencies run in **parallel waves**; blocked tasks wait
6. Report progress after each wave — user can interrupt between waves if needed

## Open questions for David

- Should this replace `ralphy` or is `ralphy` the entry point that delegates to this mechanism? (Ralphy has good UX branding.)
- Is the spec gate always mandatory for small tasks, or should there be a "lightweight mode" (quality-review only, no spec)?
- GSD's dependency-ordered wave model requires a structured task file — should this skill mandate a task file format, or infer dependencies from the task list?
