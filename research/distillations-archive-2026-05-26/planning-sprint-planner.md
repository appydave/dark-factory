---
distillation_id: planning-sprint-planner
stage: planning
intent: "Decompose a roadmap phase into a week-sized, parallelism-annotated execution plan with dependency ordering — mid-horizon planning between the roadmap and individual tasks"
created: 2026-05-17
status: draft
source_artifacts:
  - gsd:agent:gsd-planner
  - gsd:command:gsd:plan-phase
  - gsd:command:gsd:add-phase
  - gsd:command:gsd:insert-phase
  - gsd:command:gsd:discuss-phase
  - gsd:command:gsd:remove-phase
  - gsd:command:gsd:research-phase
  - gsd:command:gsd:list-phase-assumptions
  - gsd:agent:gsd-plan-checker
  - gsd:agent:gsd-phase-researcher
  - gsd:command:gsd:new-milestone
  - gsd:command:gsd:plan-milestone-gaps
  - gsd:command:gsd:add-backlog
  - gsd:command:gsd:add-todo
  - gsd:command:gsd:check-todos
  - gsd:command:gsd:review-backlog
  - bmad-method:skill:bmad-create-epics-and-stories
  - bmad-method:skill:bmad-create-story
  - appydave-plugins:skill:bmad-story-lifecycle
  - appydave-plugins:skill:po-templates
  - appydave-plugins:skill:po
  - appydave-plugins:skill:plan-reviewer
  - everything-claude-code:skill:multi-plan
  - everything-claude-code:skill:multi-workflow
  - everything-claude-code:skill:context-budget
  - gbrain:skill:daily-task-manager
  - gbrain:skill:daily-task-prep
winner_mechanism: gsd:agent:gsd-planner
---

# Unified Skill: planning-sprint-planner

**Purpose**: Take a roadmap phase and decompose it into a dependency-ordered, parallel-annotated execution plan where each plan unit has 2-3 tasks, explicit verification criteria, and context-budget awareness — the mid-horizon planning layer.

**For Agents**: Use when David says "plan this phase", "break this down into tasks", "what are the steps for phase X", "sprint plan", "weekly plan", "how do we execute this milestone", or when a roadmap exists and it's time to turn one phase into executable work. This is the **mid-horizon** skill — below roadmaps, above individual task execution.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

A phase goal is still too large to execute. The sprint-planner's job is to decompose one phase into a set of plan units — each with 2-3 tasks, a dependency graph showing which units must precede others, parallel execution flags for units that can run concurrently, and a plan-checker pass that validates the units will actually achieve the phase goal before execution starts.

The key constraint is **context-budget awareness**: plans should complete within ~50% of Claude's context window. Plan units that exceed that force quality degradation. The planner enforces right-sizing.

## Winner's Mechanism

`gsd:agent:gsd-planner` wins for the most precise phase-decomposition mechanism in the corpus: **goal-backward must-have derivation** (what must be true at each unit's completion?), **parallel wave assignment** (which units run concurrently in Wave 1 vs Wave 2 vs Wave 3?), and **plan-checker integration** (a separate `gsd-plan-checker` agent re-reads the plans and validates they cover the phase goal before execution begins). The planner explicitly distinguishes "plans are prompts, not documents that become prompts" — each PLAN.md should be immediately executable without interpretation.

The `gsd-phase-researcher` pre-pass is the critical quality gate that GSD does right and most corpus tools skip: **before decomposing, research the phase domain**. Research produces RESEARCH.md; the planner reads it before creating tasks. Plans that skip research produce tasks that re-litigate technical decisions at execution time.

`bmad-method:skill:bmad-create-epics-and-stories` covers the same mid-horizon territory from a product perspective (story decomposition from PRD). The key difference: GSD planner is implementation-first (what do we code?); BMAD stories are user-value-first (what can the user do?). David's stack has BMAD story lifecycle already; the gap is the **implementation-level** planning that maps stories to code tasks.

## Non-overlapping ideas folded in

- From `gsd:command:gsd:list-phase-assumptions`: **Explicit assumption surfacing before locking a plan** — list every assumption embedded in the phase plan before execution begins. Unexamined assumptions are the primary cause of plan failure mid-sprint. This is a mandatory pre-execution step GSD makes visible as a first-class command.
- From `gsd:command:gsd:discuss-phase`: **Discussion gate before planning** — sometimes a phase is not clear enough to plan; it needs a dialogue to clarify intent, resolve CONTEXT.md questions, and surface locked decisions first. Planning without this gate produces plans that the user immediately wants to revise.
- From `appydave-plugins:skill:plan-reviewer`: **External plan review before execution** — after the plan is written, route it through a reviewer agent before execution. GSD has a plan-checker (structural validation); the plan-reviewer covers "does this plan make sense in context of the whole project?".
- From `everything-claude-code:skill:context-budget`: **Context-budget enforcement as first-class plan constraint** — each plan unit should be sized so the implementing agent can complete it within 50% context. GSD documents this rule; context-budget makes it a tracked metric. Units that violate context-budget should be split, not assigned.
- From `gbrain:skill:daily-task-prep`: **Daily scope selection** — at the start of each work day, select which plan units from the sprint plan to execute today based on current state, energy, and blockers. This is the **daily planning** micro-layer beneath sprint planning.
- From `gsd:command:gsd:plan-milestone-gaps`: **Gap detection between milestone and sprint plans** — after a milestone spans multiple sprints, validate that all milestone requirements have plan-unit coverage. Prevents the "we planned 3 sprints but milestone requirement X has no task" failure.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|--------------------|
| gsd:gsd-planner | Goal-backward must-haves, parallel wave assignment, plan-checker integration, 2-3 tasks per plan unit, context-budget rule | GSD workspace format |
| gsd:gsd-phase-researcher | Research pre-pass before decomposition | GSD agent format |
| gsd:gsd-plan-checker | Structural validation before execution | GSD specifics |
| gsd:discuss-phase | Discussion gate before locking a plan | GSD command |
| gsd:list-phase-assumptions | Explicit assumption surfacing | GSD command |
| bmad:create-epics-and-stories | User-value framing of sprint work; BMAD story lifecycle | BMAD step-file architecture |
| appydave:plan-reviewer | Post-plan review pass | AppyDave stack |
| ecc:context-budget | Context-budget as explicit plan constraint | ECC-specific tooling |
| gbrain:daily-task-prep | Daily selection layer beneath sprint plans | GBrain format |

## Boundary with adjacent sub-clusters

- **planning-roadmap-architect**: Receives a phase from the roadmap. Does not create phases or order phases — that is roadmap-architect's job. Sprint-planner takes ONE phase and makes it executable.
- **planning-task-breakdown**: Sprint-planner produces plan units (each with 2-3 tasks). Task-breakdown (spec-kit's `/tasks`) takes plan units and generates an atomic, immediately-implementable task list with checkbox format, file paths, and dependency chains. The sprint-planner is one level above.
- **spec-writing**: Sprint-planner assumes spec is done. If a plan unit surfaces "we need to decide what this should do", that is a spec gap — return to spec-writing, not sprint-planner.

## Draft SKILL.md frontmatter

```yaml
name: planning-sprint-planner
description: >
  Decompose a roadmap phase into a dependency-ordered, parallel-annotated execution plan.
  Each plan unit: 2-3 tasks, explicit must-haves, parallel wave assignment, context-budget constraint.
  Includes research pre-pass, assumption surfacing, and plan-checker validation before execution.
  Use when: "plan this phase", "break this down into tasks", "sprint plan", "weekly plan",
  "how do we execute this milestone", "what are the steps for phase X".
```

## Open questions for David

- Should the research pre-pass (`gsd-phase-researcher`) be mandatory or optional? For well-understood phases in familiar stacks it feels like overhead, but for new technical domains it's a real quality gate.
- `context-budget` enforcement: should plan units that exceed the budget fail loudly (error) or just warn? GSD recommends ~50% context; ECC tracks it as a metric. What's the right enforcement mode for David's solo-developer workflow?
- Daily task prep (`gbrain:daily-task-prep`) is a separate micro-layer. Should it be built into sprint-planner as a "start your day" command, or stay separate?
