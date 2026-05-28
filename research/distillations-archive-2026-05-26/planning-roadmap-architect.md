---
distillation_id: planning-roadmap-architect
stage: planning
intent: "Transform requirements into a phased roadmap with observable success criteria — the long-horizon planning layer before any sprint or task breakdown"
created: 2026-05-17
status: draft
source_artifacts:
  - gsd:agent:gsd-roadmapper
  - bmad-method:skill:bmad-prd
  - bmad-method:skill:bmad-create-prd
  - bmad-method:skill:bmad-edit-prd
  - bmad-method:skill:bmad-agent-pm
  - bmad-method:skill:bmad-sprint-planning
  - bmad-method:skill:bmad-sprint-status
  - bmad-method:skill:bmad-correct-course
  - everything-claude-code:skill:blueprint
  - everything-claude-code:skill:product-capability
  - everything-claude-code:skill:strategic-compact
  - everything-claude-code:skill:investor-materials
  - appydave-plugins:skill:goal-plan
  - appydave-plugins:skill:scope-analyst
  - ruflo:skill:goals
  - ruflo:agent:goal-planner
  - ruflo:agent:agent-goal-planner
  - ruflo:skill:adr
  - gstack:skill:plan-ceo-review
  - gstack:skill:plan-eng-review
  - gstack:skill:plan-design-review
  - gstack:skill:plan-devex-review
winner_mechanism: gsd:agent:gsd-roadmapper
---

# Unified Skill: planning-roadmap-architect

**Purpose**: Turn a set of requirements into a delivery-ordered roadmap with phases, per-phase observable success criteria, and 100% requirement coverage — the strategic planning layer that commits to WHAT gets built and in what order, before any sprint or task breakdown begins.

**For Agents**: Use when David says "build a roadmap", "phase this out", "what order should we build these", "plan the project", "map requirements to phases", "define milestones", "how should this be structured before we code". This is the **longest-horizon** planning skill — use it when scope is a set of features, not a single task.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

There is a moment in every project when requirements have been gathered (by PRD, brainstorm, or raw list) and the question shifts from "what do we want?" to "in what order do we build it, and how do we know when each phase is done?" That moment is the roadmap-architect's domain.

The output is a phased roadmap: each phase delivers one coherent, independently verifiable capability; every requirement maps to exactly one phase; success criteria are observable user behaviors, not implementation tasks.

## Winner's Mechanism

`gsd:agent:gsd-roadmapper` wins on mechanism precision: it enforces **goal-backward phase design** (each phase starts with "what must be TRUE for users when this phase completes?" not "what should we build?"), **100% requirement coverage validation** before closing (no orphans), and **anti-enterprise scope hygiene** ("if it sounds like corporate PM theater, delete it"). The granularity configuration (coarse / standard / fine) lets it compress or expand without manual intervention.

Key insight: phases are derived from requirements, not imposed as template. "All projects need Setup → Core → Features → Polish" is explicitly rejected. The work determines the structure.

`bmad-method:skill:bmad-prd` is the complementary upstream skill — it produces the requirements input that roadmap-architect consumes. BMAD's PRD covers the "what do users need and why?" question; roadmap-architect answers "in what order, and what is done at each step?"

## Non-overlapping ideas folded in

- From `appydave-plugins:skill:scope-analyst`: **Explicit Out-of-Scope anchoring** — forces naming what will NOT be built in this round before any planning proceeds. Prevents scope creep at roadmap level. GSD doesn't make this a first-class gate; it should be.
- From `appydave-plugins:skill:goal-plan`: **Definition of Done as single exit condition** — the six-section schema (Stack, In Scope, Out of Scope, Definition of Done, Acceptance Criteria, Key References) is a more lightweight alternative to GSD's full roadmap for single-feature scoping. Use goal-plan when scope is one feature; use roadmap-architect when scope is multiple phases.
- From `bmad-method:skill:bmad-sprint-status` + `bmad-correct-course`: **Phase drift detection** — if the current phase is running over or under-scoped, there should be a mechanism to surface this. GSD STATE.md covers current position; BMAD covers course correction. Combine as a "phase health check" that runs at phase completion.
- From `gstack:skill:plan-ceo-review` + `plan-eng-review`: **Multi-lens plan review** — before locking a roadmap, run it past functional lenses (business viability, technical feasibility, developer experience). GSD assumes one reviewer; GStack's multi-perspective review catches blind spots the solo architect misses.
- From `ruflo:skill:adr`: **Architecture Decision Record at phase gate** — each phase boundary that makes a non-obvious technical choice should emit an ADR. Roadmaps that change architecture without logging the decision create confusion when the phase is implemented weeks later.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|--------------------|
| gsd:gsd-roadmapper | Goal-backward phase derivation, 100% coverage validation, anti-enterprise scope hygiene, granularity calibration, STATE.md progress tracking | GSD workspace format specifics |
| bmad-method:bmad-prd | PRD as upstream requirements source; capabilities-not-implementation discipline; non-goals explicit | BMAD multi-agent ceremony overhead |
| bmad-method:bmad-sprint-planning | Phase gate → sprint breakdown link | Sprint ceremony specifics |
| appydave:scope-analyst | Explicit out-of-scope anchoring before planning | AppyDave-specific |
| appydave:goal-plan | Single-feature scoping as a lighter-weight alternative to roadmapping | Six-section schema detail |
| gstack:plan-*-review | Multi-lens review before locking a roadmap | GStack persona specifics |
| ruflo:adr | ADR emission at architecture-changing phase boundaries | Ruflo infrastructure |

## Boundary with adjacent sub-clusters

- **spec-writing**: Roadmap-architect receives a spec (PRD, requirements list) as input; it does not write specs. A spec says what users need and why. The roadmap says in what order those needs are delivered and what "done" looks like per phase.
- **planning-sprint-planner**: Roadmap-architect creates phases. Sprint-planner (below) decomposes a phase into executable week-sized chunks. Roadmap output is the sprint-planner's input.
- **workflow-architecture**: Workflow-architecture defines what shape of process executes the work (sequential, parallel, swarm). Roadmap-architect defines what work exists and its delivery order — a different dimension, not the execution shape.

## Draft SKILL.md frontmatter

```yaml
name: planning-roadmap-architect
description: >
  Transform a requirements set into a phased roadmap with observable success criteria
  and 100% coverage validation — the strategic planning layer before sprint or task breakdown.
  Derives phases from requirements (not templates), applies goal-backward success criteria,
  enforces explicit out-of-scope anchoring, and validates no orphaned requirements exist.
  Use when: "build a roadmap", "phase this out", "what order should we build these",
  "plan the project", "map requirements to phases", "define milestones",
  "how should this be structured before we code".
```

## Open questions for David

- Should `scope-analyst` be folded INTO roadmap-architect as a mandatory pre-gate, or kept as a standalone skill David calls first before handing the output to roadmap-architect?
- GSD STATE.md tracks phase progress autonomously. Is this pattern worth adopting for David's own projects, or does the lightweight goal-plan approach (single file) cover enough?
- Should multi-lens plan review (CEO / Eng / Design / DevEx lenses from gstack) be an optional flag on roadmap-architect, or a separate skill invoked after the roadmap draft?
