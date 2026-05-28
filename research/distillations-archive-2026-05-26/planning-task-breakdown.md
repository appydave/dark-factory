---
distillation_id: planning-task-breakdown
stage: planning
intent: "Convert a plan unit or feature spec into an atomic, dependency-ordered, immediately-executable task list — the granular planning layer closest to implementation"
created: 2026-05-17
status: draft
source_artifacts:
  - spec-kit:command:tasks
  - spec-kit:command:lean.tasks
  - spec-kit:command:plan
  - spec-kit:command:lean.plan
  - compound-engineering:agent:ce-plan
  - compound-knowledge:skill:kw:plan
  - compound-knowledge:skill:kw:work
  - everything-claude-code:skill:plan
  - everything-claude-code:skill:plan-prd
  - everything-claude-code:skill:plan-orchestrate
  - everything-claude-code:skill:prp-plan
  - everything-claude-code:skill:prp-implement
  - everything-claude-code:skill:blueprint
  - everything-claude-code:skill:multi-plan
  - superpowers:skill:writing-plans
  - agent-skills-osmani:skill:planning-and-task-breakdown
  - agent-skills-osmani:skill:plan
  - ruflo:skill:agent-planner
  - ruflo:agent:agent-code-goal-planner
  - gstack:skill:autoplan
winner_mechanism: compound-engineering:agent:ce-plan
---

# Unified Skill: planning-task-breakdown

**Purpose**: Convert a feature spec, plan unit, or implementation requirement into an atomic, dependency-ordered task list — each task with file paths, stable IDs, test scenarios, and explicit guardrails. The granular planning layer that makes the jump from "what to build" to "here is each step in order."

**For Agents**: Use when David says "break this into tasks", "create tasks for this feature", "give me the implementation plan", "task list", "atomic steps", "what's the checklist to implement this". This is the **most granular** planning layer — below roadmaps, below sprint plans, directly above implementation.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

A plan unit still requires interpretation before execution. The task-breakdown layer eliminates that interpretation gap: it produces a list where each task has an ID, file path(s), action description specific enough that a different agent (or future David) can execute it without asking follow-up questions, and a verification criterion that proves the task is done.

The canonical failure mode this prevents: "implement the authentication module" — a task that a plan unit might contain, which is not executable. Task-breakdown produces: "Create `src/auth/middleware.ts`. Implement `verifyJWT(token: string): User | null`. Check: `npm test auth/middleware.test.ts` passes with no new assertions needed."

## Winner's Mechanism

`compound-engineering:agent:ce-plan` wins on the most rigorous **guardrails-over-choreography** principle: it captures WHAT must be true (decisions, scope boundaries, atomic units U1/U2/U3, files, test scenarios) without pre-writing HOW to satisfy those constraints. Plans that pre-write implementation are brittle; plans that specify guardrails stay portable across weeks of code change and across implementer (human or Claude).

The mechanism that makes CE stand out: **stable U-IDs** (never renumbered even after reordering), **origin tracing** (R-IDs from brainstorm flow through to task test scenarios), and **automatic confidence check** (after writing the plan, targets sub-agents at weak sections before calling the plan done). The expensive moment to find a thin section is during planning, not during execution.

`superpowers:skill:writing-plans` adds the most actionable format rule: **no placeholders** — every step must contain actual content, every code step must show the code, "TBD" is a plan failure. The Superpowers plan format (Task N with Files + Steps with checkboxes) is the clearest visual structure in the corpus for a human/agent reading a plan.

`spec-kit:command:tasks` adds **user-story-organized task structure**: each story gets its own phase, with setup tasks, foundational tasks, and story-specific tasks in order. The checklist format (`- [ ] T001 [P] [US1] Description with file path`) is the most machine-parseable task format in the corpus.

## Non-overlapping ideas folded in

- From `spec-kit:command:tasks`: **Parallelizability flags** — tasks marked `[P]` can be assigned to parallel agents. Tasks without `[P]` are sequential. This is the task-level equivalent of GSD's wave assignment at plan-unit level. Plan units that have parallel tasks unlock fan-out execution.
- From `spec-kit:command:plan`: **Constitution check** — before generating tasks, check the project's `constitution.md` (the invariants that cannot be violated). Tasks that violate the constitution fail the gate. This is the task-level enforcement of spec-kit's most important mechanism.
- From `superpowers:writing-plans`: **Spec coverage self-review** — after writing all tasks, skim each section of the spec and confirm you can point to a task that implements it. Missing coverage = missing tasks, not "implied tasks". This is a mandatory self-review step, not a subagent dispatch.
- From `compound-engineering:ce-plan`: **Universal planning** — the same task-breakdown engine works for non-software multi-step work (study plans, event planning, maintenance routines). U-IDs, dependency ordering, and guardrails transfer; the software-specific confidence check is skipped.
- From `agent-skills-osmani:planning-and-task-breakdown`: **Anti-rationalization for planning decisions** — before locking the task list, surface the top 3 ways you might be rationalizing (hiding work in a vague task, postponing a difficult decision to "later", assuming a dependency works without verifying). Name them and resolve them before execution.
- From `gstack:skill:autoplan`: **Auto-planning from minimal input** — given a description of what to build, auto-derive the task structure without explicit phase/unit setup. The fast path for well-understood work where full sprint-planning ceremony is overkill.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|--------------------|
| compound-engineering:ce-plan | Guardrails-over-choreography, U-IDs, origin tracing, confidence check + auto-deepening, universal planning | CE research agents (covered by sprint-planner's phase-researcher) |
| superpowers:writing-plans | No-placeholders rule; Files + Steps format; spec coverage self-review; execution handoff (subagent vs inline) | Superpowers harness specifics |
| spec-kit:tasks | Checklist format with T-IDs, parallelizability flags, user-story organization | Spec-kit harness adapters |
| spec-kit:plan | Constitution check pre-gate | Spec-kit setup scripts |
| agent-skills-osmani:planning | Anti-rationalization for planning decisions | Osmani persona |
| gstack:autoplan | Minimal-input auto-planning fast path | GStack format |

## Boundary with adjacent sub-clusters

- **planning-sprint-planner**: Sprint-planner produces plan units (2-3 tasks each, in waves). Task-breakdown takes ONE plan unit and produces an atomic task list. If a plan unit says "implement authentication module", task-breakdown turns it into 8 specific tasks with file paths and test verification.
- **spec-writing**: Task-breakdown assumes the spec is done. "What should this feature do?" is a spec question. "How do I implement what the spec requires?" is a task-breakdown question.
- **code-implementation**: Task-breakdown produces the task list. Implementation executes it. The handoff is a tasks.md file that the implementing agent reads and executes task by task, using `spec-kit:implement` or `superpowers:executing-plans`.

## Draft SKILL.md frontmatter

```yaml
name: planning-task-breakdown
description: >
  Convert a feature spec, plan unit, or requirement into an atomic task list.
  Each task: stable ID, file paths, action description, verification criterion.
  Applies guardrails-over-choreography (WHAT, not HOW), no-placeholders rule,
  parallelizability flags, constitution check, and post-write spec coverage review.
  Use when: "break this into tasks", "create tasks for this feature",
  "give me the implementation plan", "task list", "atomic steps",
  "what's the checklist to implement this".
```

## Open questions for David

- CE's guardrails-over-choreography is philosophically opposed to Superpowers' "show the actual code in every step" rule. CE: plans that pre-write code go stale. Superpowers: plans without code are useless. Both are right for different contexts. Should David's unified skill default to one style, or let the user choose?
- The spec-kit constitution check (project invariants that tasks cannot violate) is a powerful gate. Does David have an equivalent? Would it be worth creating a `constitution.md` for each project?
- U-IDs (stable across reordering) vs simple task numbering: U-IDs prevent reference breakage in PR descriptions and conversations. Is the overhead worth it for David's solo workflow?
