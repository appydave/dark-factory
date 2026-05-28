---
distillation_id: workflow-architecture-state-machine-workflow
stage: workflow-architecture
intent: "Model a project as a state machine — phases with explicit transitions, dependency ordering, auto-advance when state is met, and pause/resume across sessions"
created: 2026-05-17
status: draft
source_artifacts:
  - gsd:command:gsd:next
  - gsd:command:gsd:manager
  - gsd:command:gsd:workstreams
  - gsd:command:gsd:new-milestone
  - gsd:command:gsd:add-phase
  - gsd:command:gsd:insert-phase
  - gsd:command:gsd:remove-phase
  - gsd:command:gsd:analyze-dependencies
  - gsd:command:gsd:progress
  - gsd:command:gsd:autonomous
  - gsd:command:gsd:pause-work
  - gsd:command:gsd:resume-work
  - gsd:command:gsd:thread
  - gsd:command:gsd:new-workspace
  - gsd:command:gsd:add-backlog
  - gsd:command:gsd:workstreams
  - everything-claude-code:skill:ralphinho-rfc-pipeline
  - everything-claude-code:command:multi-workflow
winner_mechanism: gsd:command:gsd:next
---

# Unified Skill: state-machine-workflow

**Purpose**: Model a multi-phase project as a state machine — each phase has preconditions, a body, and a transition. The `next` oracle reads current state and auto-advances to the right step, so David doesn't have to remember "where was I?".

**For Agents**: Use when David says "what's next on the project", "where did I leave off", "advance to the next phase", "auto-continue the milestone", "what should I do next", or when resuming work after a session break on a multi-phase project.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

A project's phases are a directed graph with preconditions. Instead of tracking manually ("did I finish the plan? did the tests pass? am I ready to implement?"), a state-machine workflow reads the project's current artifacts and state files to determine the exact next legal action — then either routes to it or executes it autonomously. The `next` oracle is the design-time contribution: it externalizes the "what do I do now?" judgment into a deterministic rule set.

**Design-time vs runtime**: This skill *designs* the state machine (defines phases, transitions, preconditions). The execution of phases (running the implementation) is handled by `plan-executor`. The orchestration of multiple phases in sequence is handled by `autonomous-pipeline-runner` (already distilled). The state machine is the specification that both of those skills consume.

## Winner's Mechanism

`gsd:command:gsd:next` is the winner for one reason: **state-aware auto-advance**. It detects which files and artifacts exist (is there a ROADMAP.md? is the plan complete? have all tasks been marked done?), determines the current state, and routes to the next logical action without requiring the user to specify it. This "oracle" pattern is uniquely powerful for long-running projects that span sessions.

`gsd:manager` (the milestone command center with phase dashboard) is the human-facing complement: a single terminal interface showing current phase, phase health, and dispatching work. The `next` command is what you'd run headlessly; `manager` is what you'd use when reviewing progress with a human.

`gsd:analyze-dependencies` contributes the **dependency graph analysis** — before defining phases, analyze what each phase depends on and suggest `Depends-on` entries. This prevents ordering errors where phase 3 assumes work that phase 2 hasn't completed.

`ralphinho-rfc-pipeline` (ECC) contributes the **RFC-driven DAG execution** pattern: a multi-agent workflow where work units are RFCs (structured decision documents), each moving through a fixed state machine (Draft → Review → Approved → Implemented). Quality gates prevent phase transitions until all required reviewers sign off. This is the most rigorous state-machine pattern in the corpus.

## Non-overlapping ideas folded in

- From `gsd:analyze-dependencies`: **Dependency graph auto-analysis before phase definition** — `complexity: medium | optional: true | prerequisite: "multiple phases exist in the roadmap"`. Before locking phase order, run dependency analysis to surface hidden prerequisites. Prevents phase-ordering bugs.
- From `gsd:workstreams`: **Parallel workstream management** — `complexity: medium | optional: true | prerequisite: "milestone has parallel-executable work streams"`. Not all phases are sequential. Some can run in parallel tracks. Workstreams let the state machine track multiple active branches simultaneously. Important for BMAD projects where frontend and backend can progress in parallel.
- From `gsd:thread`: **Cross-session context thread** — `complexity: low | optional: true | prerequisite: "work spans multiple sessions on a topic that doesn't map to a single phase"`. For ongoing concerns (e.g. "auth redesign notes") that don't belong to a specific phase but need to persist across sessions. Complements the `.continue-here.md` handoff (which is session-specific) with a durable topic thread.
- From `ralphinho-rfc-pipeline`: **Quality-gate state transitions** — `complexity: high | optional: true | prerequisite: "project requires formal sign-off before phase transitions"`. Phase transitions require a reviewer to explicitly approve before the state machine advances. The gate is enforced by the state file, not just convention. For David's highest-stakes work (SupportSignal NDIS compliance, Kybernesis releases).
- From `gsd:insert-phase`: **Urgent phase injection** — `complexity: low | optional: false | prerequisite: none"`. Mid-project discovery of blocking work that doesn't fit existing phases. Insert a decimal-numbered phase (e.g. 2.5) between integer phases without renumbering. This is a common real-world scenario the state machine must handle gracefully.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| gsd:next | State-aware auto-advance oracle, current-state detection logic | GSD-specific STATE.md format (make format-agnostic) |
| gsd:manager | Phase dashboard + work dispatching, single terminal command center | GSD workspace format |
| gsd:analyze-dependencies | Dependency graph analysis before phase definition | GSD-specific ROADMAP.md format |
| gsd:workstreams | Parallel workstream management | GSD workspace isolation strategy |
| gsd:thread | Cross-session context thread | GSD thread file naming |
| gsd:pause-work + resume-work | Context handoff + state-aware resume (see plan-executor for this) | Deferred to plan-executor distillation |
| ralphinho-rfc-pipeline (ECC) | Quality-gate state transitions, RFC-as-work-unit pattern | ECC-specific DAG execution infrastructure |
| multi-workflow (ECC) | Multi-phase execution with quality gates between phases | Multi-model infrastructure (Codex/Gemini) |

## Draft SKILL.md frontmatter

```yaml
name: state-machine-workflow
description: >
  Model a multi-phase project as a state machine and auto-advance to the next legal step.
  Reads project artifacts to determine current state, routes to next action,
  supports parallel workstreams, urgent phase injection, and cross-session threads.
  Use when: "what's next", "where did I leave off", "advance to the next phase",
  "what should I do next", "auto-continue", resuming a multi-phase project after a break.
argument-hint: "[project-dir | milestone-name]"
allowed-tools: "Read, Bash(cat:*), Bash(ls:*), Bash(find:*), Write"
```

## Open questions for David

1. **State file format**: GSD uses `.planning/STATE.md` + `ROADMAP.md`. BMAD uses `sprint-status.yaml` + `implementation-artifacts/`. Should `state-machine-workflow` define a new format-agnostic state contract, or detect and speak both formats? Format-agnostic is more portable; format-specific is less code to write.

2. **GSD as pattern vs GSD as dependency**: GSD is an npm package with its own CLI. Should David adopt GSD's CLI directly (npm install, use GSD commands natively) or extract only the *patterns* (state detection, dependency analysis, workstreams) and implement them natively in appydave-plugins? GSD has 81 artifacts in the corpus — it's a full system, not just a skill.

3. **Quality gates**: `ralphinho-rfc-pipeline` enforces phase transitions via reviewer sign-off. Is this worth adopting for any of David's projects, or is it overkill for solo / small-team work? If yes, which project needs it first (SupportSignal compliance? Kybernesis releases)?
