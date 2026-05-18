---
distillation_id: planning-dependency-and-risk
stage: planning
intent: "Identify, order, and mitigate dependencies and risks before execution — the planning layer that prevents the 'we built in the wrong order' and 'we didn't know this would break' failure modes"
created: 2026-05-17
status: draft
source_artifacts:
  - gsd:command:gsd:analyze-dependencies
  - gsd:command:gsd:discuss-phase
  - gsd:command:gsd:list-phase-assumptions
  - gsd:command:gsd:insert-phase
  - gsd:agent:gsd-assumptions-analyzer
  - gsd:agent:gsd-advisor-researcher
  - ruflo:skill:adr
  - ruflo:skill:agent-migration-plan
  - ruflo:skill:daa
  - ruflo:agent:agent-arch-system-design
  - ruflo:skill:trading-strategist
  - everything-claude-code:skill:database-migrations
  - everything-claude-code:skill:deployment-patterns
  - everything-claude-code:skill:homelab-network-readiness
  - everything-claude-code:skill:homelab-network-setup
  - everything-claude-code:skill:production-scheduling
  - everything-claude-code:skill:inventory-demand-planning
  - everything-claude-code:skill:mle-workflow
  - gstack:skill:office-hours
  - appydave-plugins:skill:architectural-review
winner_mechanism: gsd:command:gsd:analyze-dependencies
---

# Unified Skill: planning-dependency-and-risk

**Purpose**: Before locking a phase plan or task list for execution, surface the dependency graph, identify ordering constraints, and name risks that need mitigation. Prevents the "we built Phase 2 first and now Phase 1 is impossible" and "we assumed this dependency worked" failure modes.

**For Agents**: Use when David says "what depends on what", "are there any risks here", "ordering matters for this", "analyze dependencies", "what could go wrong", "what do I need to have done first", "migration risk", "what assumptions are we making", or when a phase plan has been drafted and it's time to validate the execution order before locking. This is a **cross-cutting gate** invoked after sprint-planner and before execution.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Planning without dependency analysis produces plans where Phase 3 accidentally requires infrastructure that Phase 4 was supposed to create. Planning without risk analysis produces plans that look complete on paper but fail at the first integration point. The dependency-and-risk skill runs as a post-planning gate: once a roadmap or sprint plan exists, this skill validates the execution order and names the failure modes before any implementation begins.

This sub-cluster is **cross-horizon** — dependency analysis applies at roadmap level (phase ordering), sprint level (unit wave assignment), and task level (task prerequisites). The same mechanism runs at all three levels; the granularity of the output differs.

## Winner's Mechanism

`gsd:command:gsd:analyze-dependencies` wins for the most actionable dependency analysis format: it produces a dependency graph that feeds directly into plan wave assignment (which units run in Wave 1 vs Wave 2 vs Wave 3), with an explicit **critical path** annotation showing which dependency chain determines overall project duration. GSD's analyze-dependencies doesn't just surface "X needs Y" — it surfaces "this chain is your critical path; if X slips, everything slips."

`gsd:agent:gsd-assumptions-analyzer` is the most important companion: it takes the same plan and surfaces all assumptions that are embedded but unstated. The distinction is: analyze-dependencies finds explicit "requires" edges; assumptions-analyzer finds implicit "we assumed this is true" edges that won't show up in the dependency graph.

`ruflo:skill:adr` (Architecture Decision Records) is the persistence mechanism: for each dependency or risk that requires a non-obvious decision to resolve, emit an ADR. ADRs prevent the "we decided X two months ago but nobody remembers why" failure. They are especially valuable at phase gate transitions.

## Non-overlapping ideas folded in

- From `ruflo:skill:agent-migration-plan`: **Migration risk as a first-class planning artifact** — for any plan that touches existing data, existing APIs, or existing running services, produce a migration plan (what is the rollback path? what is the migration sequence? what is the blast radius if it fails?). Migration risk is typically the highest-stakes dependency in data-adjacent work.
- From `everything-claude-code:skill:database-migrations`: **Schema migration as explicit task dependency** — schema migrations have strict ordering constraints (up/down pairs, transactional vs non-transactional) that standard dependency analysis misses. Database migrations deserve their own dependency sub-graph with rollback explicitly modeled.
- From `everything-claude-code:skill:deployment-patterns`: **Deployment dependency as planning constraint** — what deployment pattern does this plan require? Blue-green, canary, rolling restart, big-bang? The deployment pattern determines whether Phase N can run alongside Phase N-1 or requires a hard cutover. This is a planning decision, not a deployment decision.
- From `gsd:command:gsd:insert-phase`: **Urgent insertion pattern** — when a dependency analysis reveals a prerequisite phase that wasn't in the roadmap, the insert-phase mechanism allows adding it at decimal precision (between Phase 2 and Phase 3 becomes Phase 2.1) without renumbering the whole roadmap.
- From `gstack:skill:office-hours`: **Open discussion for unresolved risk** — when a dependency or risk cannot be resolved by analysis (requires a domain expert, a technology spike, or a business decision), surface it as an explicit "office hours" item: "this requires a conversation before we can proceed." Don't silently assume the answer.
- From `appydave-plugins:skill:architectural-review`: **Architecture-level dependency surface** — dependencies that live at the code level are surfaced by dependency analysis; dependencies that live at the system architecture level (which service calls which, which shared database is a coupling point) require an architectural review lens.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|--------------------|
| gsd:analyze-dependencies | Dependency graph with critical path annotation, wave assignment | GSD workspace format |
| gsd:assumptions-analyzer | Implicit assumption surfacing separate from explicit dependency analysis | GSD agent format |
| ruflo:adr | ADR emission at dependency-resolution decision points | Ruflo format |
| ruflo:agent-migration-plan | Migration risk as first-class planning artifact | Ruflo-specific |
| ecc:database-migrations | Schema migration dependency sub-graph with rollback | ECC-specific stack |
| ecc:deployment-patterns | Deployment pattern as planning constraint | ECC-specific deployment |
| gsd:insert-phase | Urgent phase insertion without renumbering | GSD command |
| gstack:office-hours | Open discussion gate for unresolvable risk | GStack persona |
| appydave:architectural-review | Architecture-level dependency lens | AppyDave stack |

## Boundary with adjacent sub-clusters

- **planning-sprint-planner**: Sprint-planner produces wave assignment (which units run in which wave). Dependency-and-risk is the analysis that FEEDS wave assignment. Sprint-planner calls dependency-and-risk internally; dependency-and-risk can also be invoked standalone after any planning artifact.
- **verification-validation cluster**: Verification-validation checks whether built work is correct. Dependency-and-risk checks whether the build order is correct before building begins. They are complementary; neither replaces the other.
- **workflow-architecture cluster**: Workflow-architecture defines the execution shape (sequential, parallel, fan-out). Dependency-and-risk defines the execution ORDER constraints. Order constraints are input to architecture shape; they are not the same thing.

## Draft SKILL.md frontmatter

```yaml
name: planning-dependency-and-risk
description: >
  Surface dependency graph, critical path, hidden assumptions, and migration/deployment risks
  before locking a plan for execution. Runs as a post-planning gate at any granularity
  (roadmap, sprint, or task level). Produces dependency graph with wave assignment, ADR
  for non-obvious decisions, and explicit assumption log.
  Use when: "what depends on what", "are there any risks here", "ordering matters for this",
  "analyze dependencies", "what could go wrong", "what do I need to have done first",
  "migration risk", "what assumptions are we making".
```

## Open questions for David

- Should dependency-and-risk run automatically as part of sprint-planner (built in, non-optional) or stay as an explicit invocation David decides to run? The cost of always running it is overhead; the cost of not running it is ordering failures.
- ADR emission: GSD doesn't mandate ADRs; Ruflo does. For David's solo workflow, when is the overhead of an ADR worth it vs just a decision note in STATE.md?
- Migration risk is the highest-stakes dependency type in data work. Does SupportSignal (NDIS app with PII) warrant a dedicated migration-risk skill that runs automatically when a plan touches auth, user data, or schema? The stakes are compliance-level.
