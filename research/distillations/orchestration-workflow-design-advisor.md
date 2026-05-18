---
distillation_id: orchestration-workflow-design-advisor
stage: orchestration
intent: "Help David design the right multi-agent workflow for a task before executing it — topology selection, step sequencing, agent role assignment"
created: 2026-05-16
status: draft
source_artifacts:
  - appydave-plugins:skill:agent-orchestrator
  - appydave-plugins:skill:workflow-orchestrator
  - ruflo:skill:workflow-automation
  - gsd:command:gsd:manager
  - gsd:command:gsd:next
  - gsd:command:gsd:workstreams
  - appydave-plugins:command:ruflo-swarm-check
  - gsd:command:gsd:do
  - appydave-plugins:skill:mocha
  - appydave-plugins:skill:mochaccino
  - appydave-plugins:skill:shelly
  - appydave-plugins:skill:peter
  - gbrain:skill:ask-user
  - appydave-plugins:skill:system-context
winner_mechanism: appydave-plugins:command:ruflo-swarm-check
---

# Unified Skill: workflow-design-advisor

**Purpose**: Before executing — decide what coordination structure, agent roles, and step sequence is right for a given task. The pre-flight design layer.

**For Agents**: Use when David says "how should I structure this", "what topology", "should this be a swarm", "design the workflow", "which agents do I need", "sequential or parallel", or starts a new complex task and needs the coordination design before diving in.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

## Intent

Step-gate at task start — classify whether work is sequential single-coder, a fan-out swarm, or bespoke per-unit — then emit a lightweight coordination plan (roles, topology, step sequence) before execution begins.

## Winner's Mechanism

`appydave-plugins:command:ruflo-swarm-check` wins for the cleanest pre-execution classification: sequential vs fan-out vs bespoke-per-unit, with the decision made before any execution. The single-question gate ("does this need a swarm?") prevents over-engineering simple tasks. It is already in David's stack.

`appydave-plugins:skill:agent-orchestrator` is the fuller design advisor: interviews the user about the task, recommends topology, assigns roles. It handles the "I don't know what I need yet" case that `ruflo-swarm-check` assumes you've already resolved.

The two complement each other: `ruflo-swarm-check` is the fast gate; `agent-orchestrator` is the detailed design session.

## Non-overlapping ideas folded in

- From `gsd:command:gsd:next`: **State-aware next-step detection** — auto-advances to the logical next GSD workflow step based on what files/state exist. The "what should I do next?" oracle without explicit user input.
- From `appydave-plugins:skill:workflow-orchestrator`: **Automatic optimal workflow emission** — given a task description, emits a structured workflow (YAML or markdown) ready for execution. Design output as a first-class artifact.
- From `gsd:command:gsd:do`: **Natural language → slash command routing** — user says what they want to do in prose, system routes to the right command. Reduces the "which command do I run?" friction.
- From `gbrain:skill:ask-user`: **Explicit choice gating** — when the advisor genuinely can't decide, present structured options and gate execution until the user responds. Prevents false-confidence design.
- From `appydave-plugins:skill:mochaccino`: The Mochaccino ecosystem (Mocha + Shelly + Peter) is an example of **role specialization within a design-advisor cluster** — each persona handles a specific design domain (view, shape, data). Worth noting as the pattern for building domain-specific advisor ensembles.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| ruflo-swarm-check | Sequential / fan-out / bespoke classification gate | Ruflo-specific swarm init |
| agent-orchestrator | Detailed design session: topology recommendation + role assignment | Claude Code teammate mode specifics |
| workflow-orchestrator | Structured workflow YAML emission as design output | Brand-dave specific schema |
| gsd:manager | Phase dashboard + work dispatching (state machine view of workflow) | GSD workspace format |
| gsd:next | State-aware auto-advance | GSD state file format |
| gsd:do | NL→command routing | GSD command set |
| ask-user | Explicit choice gating | GBrain-specific |
| mochaccino/mocha/shelly/peter | Role-specialized advisor ensemble pattern | UI/UX domain |
| system-context | Scan-then-design: understand system before designing workflow | CONTEXT.md generation |

## Draft SKILL.md frontmatter

```yaml
name: workflow-design-advisor
description: >
  Design the right coordination structure for a task before executing it —
  classify (sequential / fan-out / bespoke), select topology, assign agent roles,
  emit a lightweight coordination plan.
  Fast gate: ruflo-swarm-check. Full design session: agent-orchestrator.
  Use when: "how should I structure this", "what topology", "design the workflow",
  "do I need a swarm", "which agents", "sequential or parallel",
  "what's the plan before I start".
```

## Open questions for David

- Should `workflow-design-advisor` be a real new skill, or just better documentation of the two-skill pair (`ruflo-swarm-check` as gate, `agent-orchestrator` as design)? The gap is "users don't know which to call first."
- `gsd:next` (state-aware auto-advance) is a compelling pattern for David's own pipelines — worth adopting independent of GSD? E.g., a `project-next` command that scans the current project state and recommends the next action.
- Mochaccino's multi-persona design ensemble — is this pattern worth generalizing to non-UI design domains (e.g., a "data architecture advisor" with Peter-like roles)?
