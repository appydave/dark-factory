# Dark Factory — Docs Index

**Status**: living index — 2026-06-01
One line per doc. Start at the top. This index is the fix for doc-sprawl — when a new design doc lands, it gets a line here or it doesn't exist.

---

## Read order (the factory's shape & purpose)

0. **`north-star.md`** — ★ the North Star + the two major paths (build the factory vs run the content). Read first.
1. **`../README.md`** — charter, repo layout, status.
2. **`architecture.md`** — ★ the full statement: Factory / Warehouse / Watchtower, the self-improvement loop, design principles (§13).
2b. **`dark-factory-constellation.md`** — ★ the holistic map of all the parts (Floor + Switchboard / AngelEye / AppyRadar / Watchtower + Marshall), the boundaries between them, where Symphony feeds in, build status. Carries the 2026-06-10 correction that the old "AppyCtrl" was a wrong app — the real process/fleet observer is **AppyRadar** (read-only). Read before scoping any single component. (2026-06-10)
2c. **`appyradar.md`** — the corrected, durable definition of **AppyRadar** (the read-only machine & fleet sensor; AppySentinel Pilot 1). Supersedes every "AppyCtrl" reference. Carries the read-vs-control principle. (2026-06-10)
3. **`dark-factory-living-system-spec.md`** — the operational spec: 5 eval levels, 3 trigger types, schemas, SkillOpt grounding.

> **`context/` is deliberately not in this list.** `CONTEXT.md` and `context.globs.json` are **generated output** of the `system-context` skill — external orientation for outside consumers, regenerated on demand. They are *not* working docs and *not* part of the system. Refresh by running the skill; never hand-edit.

> **architecture.md vs spec.md — how they relate.** They overlap on purpose but are *not* peers. `architecture.md` is the **parent** (the whole system, the metaphor, the principles). `dark-factory-living-system-spec.md` is the **operational child** (how evaluation actually runs, level by level, with schemas). If they ever disagree, architecture.md wins on framing; spec.md wins on eval mechanics. *(A full merge is proposed, not done — see PROBLEMS register.)*

## The human side (how David stays the director)

- **`intake.md`** — the front door. Ideas/papers/others' work enter here; nothing is trusted until validated.
- **`human-comms.md`** — communication is first-class, both directions: audio (talk + listen) and visual (dashboards + presentation).
- **`systemic-fixes.md`** — the problem register + "fix the class not the instance" + "good/bad is a hypothesis, not gospel."
- **`tool-registry.md`** — tools/scripts are first-class; the index of platform + repo tooling; how it stays fresh.

## The contracts (govern the build)

- **`canonical-form-spec.md`** — what a canonical SKILL.md must contain.
- **`provenance-spec.md`** — provenance.json schema + verbatim-source rules.
- **`ingestion-workflow.md`** — the 11-step ingest procedure.
- **`david-style-patterns.md`** — David's voice + templates.
- **`david-design-patterns.md`** — design-taste spec (Shelly's guidance), derived from rated work via Mocha Census; the `RUBRIC.md` source of truth.

## Operating layer & threads

- **`watchtower/`** — the v0 observation surface (sub-project): **`RE-BUCKETING.md`** (★ the ratified three-plane re-home map — read FIRST to know which watchtower docs are current vs superseded; physical moves pending), **`build-state.md`** (★ the single "where we are / what's next / the rules" doc for the C-spine runtime build), `spec.md` (control-plane viewer; SSE-ban §5/§12/R7 superseded by RE-BUCKETING), `plan.md`, `schemas.md`, `DECISIONS.md`, `symphony-spec.md` + `watchtower-from-symphony.md` + `symphony-relook-2026-06-07.md` (Symphony coordination reference, factory-floor-bound), `reaper-brief.md` (engine-state reaper), `deeper-doc-system-research-brief.md` → `deeper-doc-system-findings.md` (BMAD doc-system research: brief + its delivered output). Archive-bound (v0 process/history): `context.md`, `chatgpt-brief.md`, `REVIEW.md`, `HANDOVER.md`.
- **`sop-lifecycle.md`** — workflows as SOPs-in-data; state levels; the drift problem; spike→main-flow promotion; decision lineage.
- **`phase-b-next-steps.md`** — the next build move (first dog-food workflow).
- **`doc-organiser-proposal.md`** — proposal (2026-06-05): a recurring audit skill that reports doc-drift (orphans, stale dates, broken refs) and never edits. **Decided** (defaults locked); build parked in `backlog/2026-06-05-doc-organiser.md`.
- **`ylo-to-poem-blueprint.md`** — thread 2: YLO → POEM consolidation.
- **`capture-service-brief.md`** — proposed 5th constellation tool (DRAFT for decision, 2026-06-10).
- **`youtube-channel-catalog-workflow.md`** — AITLDR pipeline backlog (parked).
- **`workflow-tool-authoring-notes.md`** — hard-won Workflow Tool craft.
- **`agent-orchestration-capabilities.md`** — ★ what Claude Code's coordination primitives actually are (subagents / Agent Teams / Workflow tool / external queue), tmux visibility, dispatcher-vs-competing-consumers, and how each maps to the Watchtower runtime + topology build order.
- **`runtime-model.md`** — ★ who runs what: the Conductor (daily orchestrator, routes jobs) → Swagger (job-agent, judgment per job) → workflows/sub-agents (execution). Resolves the isolation-vs-coordination question.
- **`upstream-repos/`** — 3rd-party architectural reference shelf (repos to study for building the factory, distinct from `research/recon/`'s distillation cluster). Includes the 2026-06-10 fleet-orchestrator research: **finding — our stateless-floor + state-plane-services split is green-field; closest 3 to study = CAO / Composio agent-orchestrator / ccswarm.**

## Outside docs/ but load-bearing

- **`../backlog/`** — active tickets + **`problems.md`** (the problem register).
- **`../research/`** — the frozen Warehouse corpus (read-only): `INDEX.md`, `insights.md`, distillations (⚠️ provisional).
- **`../mochaccino/designs/`** — the visual layer, live at `:7420`.
- **`~/dev/ad/brains/machine-control/`** — the 4-Panel Session Layout (outside this repo).
