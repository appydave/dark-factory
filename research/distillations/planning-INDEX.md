---
distillation_pass: planning
source_slice: _slice_planning.jsonl
source_artifact_count: 132
sub_cluster_count: 5
distillation_files: 6
created: 2026-05-17
status: draft
---

# Distillations — Planning Cluster

**Purpose**: Unified skill drafts distilled from the 132 planning-tagged artifacts across 12 repos.

**For Agents**: Use this index to navigate distillation files when David asks "what unified skills came out of the planning distill" or is reviewing the cluster.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Granularity observation (the key structural finding)

Planning artifacts in this corpus span **three distinct granularities** that different repos treat as one thing:

| Granularity | Horizon | Primary sources | Output artifact |
|-------------|---------|-----------------|-----------------|
| Epic / roadmap | Weeks–months | BMAD, GSD roadmapper, ECC blueprint | Phased roadmap with success criteria |
| Sprint / phase plan | Days–week | GSD planner, spec-kit plan, CE plan | Plan units with wave assignment |
| Task / checklist | Hours | Spec-kit tasks, Superpowers writing-plans, CE plan | Atomic task list with file paths |

BMAD operates primarily at **epic-level** (PRD → epics → stories). GSD spans **sprint-level** (plan-phase) and is the richest mid-horizon source. Spec-kit lives at **task-level** (its `/tasks` command is the most rigorous atomic task generator in the corpus). Superpowers' `writing-plans` is also task-level but more opinionated about code inclusion. CE-plan straddles sprint-and-task level with its guardrails-over-choreography approach.

This granularity split is why planning artifacts cross-tagged at all three levels struggle to compose naturally: a BMAD story is not the same object as a GSD plan unit is not the same object as a spec-kit task.

---

## Sub-cluster Summary

| Sub-cluster | File | Source artifacts | Winner | Gap closed? |
|-------------|------|-----------------|--------|-------------|
| [ideation-and-requirements](#ideation-and-requirements) | [planning-ideation-and-requirements.md](planning-ideation-and-requirements.md) | ~30 | compound-engineering:ce-brainstorm | PARTIAL — ce-brainstorm is new to David's stack; strategy-anchor is a genuine gap |
| [roadmap-architect](#roadmap-architect) | [planning-roadmap-architect.md](planning-roadmap-architect.md) | ~22 | gsd:gsd-roadmapper | YES — goal-backward roadmapping with coverage validation is absent from David's stack |
| [sprint-planner](#sprint-planner) | [planning-sprint-planner.md](planning-sprint-planner.md) | ~28 | gsd:gsd-planner | YES — mid-horizon plan-unit decomposition with plan-checker gate is a real gap |
| [task-breakdown](#task-breakdown) | [planning-task-breakdown.md](planning-task-breakdown.md) | ~27 | compound-engineering:ce-plan | YES — guardrails-over-choreography + no-placeholders is absent from David's current task creation |
| [session-and-context-continuity](#session-and-context-continuity) | [planning-session-and-context-continuity.md](planning-session-and-context-continuity.md) | ~12 | appydave:session-checkpoint | PARTIAL — checkpoint exists; machine-parseable STATE.md + OMI-to-state flow are the gaps |
| [dependency-and-risk](#dependency-and-risk) | [planning-dependency-and-risk.md](planning-dependency-and-risk.md) | ~13 | gsd:analyze-dependencies | YES — dependency graph + critical path + hidden assumptions is entirely absent from David's planning stack |

---

## Artifacts excluded from sub-clusters

### ECC domain-specific planning stubs (~18 artifacts)
`everything-claude-code` contributed 40 planning-tagged artifacts. Many are domain-specific plan generators that are not generalizable: `angular-developer`, `customer-billing-ops`, `homelab-network-readiness`, `homelab-network-setup`, `netmiko-ssh-automation`, `mle-workflow`, `production-scheduling`, `inventory-demand-planning`, `literature-review`, `seo`, `investor-materials`, `gan-planner`, `gan-build`, `gan-design`, `multi-backend`, `multi-frontend`, `multi-execute`. These are domain instances of the planning pattern, not planning mechanisms. Set aside.

### Ruflo domain-specific stubs (~6 artifacts)
`ruflo:trading-strategist`, `ruflo:ddd`, `ruflo:daa`, `ruflo:ruflo-sparc` — Ruflo-infrastructure or domain-specific. Pattern value extracted; infrastructure dependency set aside.

### True solos
- `appydave:po` + `appydave:po-templates` — Product Owner templates; adjacent to planning but closer to spec-writing. Set aside pending spec-writing distill.
- `gsd:plant-seed` — project inception trigger, not a planning skill itself.
- `compound-knowledge:kw:work` — execution skill, not planning.

---

## Top 3 unified skills that close real gaps in David's stack

### 1. `planning-sprint-planner` — mid-horizon gap
David's stack jumps from BMAD stories (epic-level) directly to implementation. The **mid-horizon decomposition** layer — taking one phase and producing 2-3 task plan units with dependency waves and a plan-checker gate — is entirely absent. GSD's planner fills this gap exactly, and it is the highest-leverage skill to adopt or build.

### 2. `planning-dependency-and-risk` — ordering failure prevention
David has no mechanism for surfacing the dependency graph and critical path before executing a plan. The most common planning failure is not bad tasks — it is tasks in the wrong order. The analyze-dependencies + assumptions-analyzer pairing from GSD closes this gap cleanly, and the migration-risk extension is especially relevant for SupportSignal (NDIS, PII, compliance).

### 3. `planning-task-breakdown` — guardrails-over-choreography
CE-plan's principle that plans should capture WHAT not HOW (guardrails, not implementation choreography) is the most valuable planning insight in the corpus. David's current goal-plan is close but doesn't enforce the no-placeholders rule or run a confidence check. Adopting CE-plan's U-IDs + confidence check + no-placeholders rule would make David's plans substantially more reliable.

---

## Top 2 sub-clusters needing David's judgment

### 1. `planning-ideation-and-requirements` — ce-brainstorm vs david's existing approach
CE-brainstorm is the most dialogue-rich ideation skill in the corpus but it is not in David's stack. The question is not whether it's good (it is) but whether the one-question-per-turn discipline fits David's working style, or whether `goal-plan` is already sufficient for the "what do I want to build?" question.

### 2. `planning-session-and-context-continuity` — STATE.md adoption
GSD's STATE.md pattern (machine-parseable session checkpoint) is valuable but requires committing to a planning workspace format. David's `session-checkpoint` is already in his stack; the question is whether to formalize it as STATE.md (structured, machine-readable, feeds GSD-style command pipeline) or keep it lightweight (human-readable session summary).

---

## Overlap watch (planning vs adjacent clusters)

| Planning sub-cluster | Adjacent cluster | Boundary rule |
|---------------------|-----------------|---------------|
| ideation-and-requirements | spec-writing | Planning crystallizes WHAT; spec-writing produces the document the implementing agent reads |
| roadmap-architect | workflow-architecture | Roadmap defines delivery order; workflow-architecture defines execution shape (sequential, parallel, fan-out) |
| sprint-planner | orchestration | Sprint-planner defines what work exists in a unit; orchestration defines how agents coordinate to do it |
| task-breakdown | code-implementation | Tasks.md is the handoff; code-implementation executes it |
| dependency-and-risk | verification-validation | Dependency-and-risk runs before execution; verification-validation runs after |

---

## Open question for David (cross-cluster)

The planning cluster has the most **granularity diversity** of any cluster analyzed so far. BMAD, GSD, spec-kit, CE, and Superpowers each cover different layers and have different philosophies about what a "plan" is. Before building any of these as unified skills:

**Should David's planning stack be a single pipeline** (ideation → roadmap → sprint → tasks → execute) **or a set of independent skills** that David assembles based on the work's scope?

GSD argues for a single pipeline (every project goes through new-project → roadmap → plan-phase → execute). CE argues for independent skills (ce-brainstorm and ce-plan each stand alone; you don't need the chain). The answer probably depends on project size: single-pipeline for multi-phase projects, independent skills for single-feature work.

---

## Corpus notes

- **GSD**: 24 of 132 artifacts. Dominates sprint-level planning. The most coherent end-to-end planning pipeline in the corpus. Heavy GSD-workspace format dependency but the mechanisms are extractable.
- **ECC**: 40 of 132 artifacts. Broad coverage but much of it is domain-specific stubs rather than planning mechanisms. `plan`, `plan-prd`, `blueprint`, `prp-plan`, `loop-start` are the generalizable mechanism artifacts.
- **Ruflo**: 18 artifacts. Strong in architecture-level planning (adr, agent-migration-plan, agent-arch-system-design). Infrastructure-heavy; the vocabulary is extractable even when the specific agents are not.
- **CE**: 4 artifacts but highest mechanism-density per artifact. CE-plan is the most rigorous task-breakdown skill in the corpus. CE-brainstorm is the most rigorous ideation skill.
- **Spec-kit**: 4 artifacts. The `/tasks` command format (T-IDs, parallelizability flags, user-story organization, checklist format) is the most machine-parseable task structure in the corpus.
- **BMAD**: 9 artifacts. Epic-level coverage. PRD → epics → stories pipeline is mature. The gap vs GSD is mid-horizon: BMAD has no equivalent to GSD's phase-planner.
- **Superpowers**: 2 artifacts. `writing-plans` has the clearest no-placeholders rule and spec-coverage self-review in the corpus.

---

*Distillation pass: Phase 5 catalog:distill — planning cluster. Regenerate after David reviews and approves/adjusts sub-clusters.*
