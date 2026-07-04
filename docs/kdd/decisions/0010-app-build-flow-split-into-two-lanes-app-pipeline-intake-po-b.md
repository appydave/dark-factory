---
id: ADR-0010
title: "App-build flow split into two lanes: App Pipeline (intake/PO, brain) and App Requirements (build-spec standard, Dev repo), seam at goal-ready"
status: proposed
scope: internal
date_decided: 2026-06-23
deciders: [David Cruwys]
confidence: reconstructed
recurrence_count: 1
provenance:
  sessions: ["2fdc2412"]
  files: ["apps/dark-factory/docs/app-requirements-spec.md", "brains/dark-factory/app-pipeline/README.md"]
  commits: ["ecc9897"]
tags: []
---

> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0010: App-build flow split into two lanes: App Pipeline (intake/PO, brain) and App Requirements (build-spec standard, Dev repo), seam at goal-ready

**Status:** Proposed (reconstructed)

## Context

David asked whether the factory had a requirements area for micro-applications, a standard, examples, and a single location — answer was 'scattered, no standard' across three half-homes (brain app-pipeline/, ad-hoc backlog/*-requirement.md, docs/*-spec.md). A first attempt created a standing `docs/app-requirements/` folder in apps/dark-factory as a peer to `brains/dark-factory/app-pipeline/`, which David flagged as structurally wrong ('it just feels wrong... maybe requirements don't belong inside the Dark Factory, they belong in the target application').

## Decision

Lane 1 (App Pipeline, `brains/dark-factory/app-pipeline/`) is a factory-owned instance store of idea-to-decision candidates — loose intake, PO side. Lane 2 (App Requirements) is NOT an instance store: the factory owns only the build-spec STANDARD (`apps/dark-factory/docs/app-requirements-spec.md`, sitting beside `canonical-form-spec.md`/`provenance-spec.md`), and every actual build-spec instance lives with its target app's own repo (or is staged transiently in the factory only if no repo exists yet, marked `migrates_to:`). The seam between lanes is a candidate's `status: goal-ready` field.

## Alternatives Considered

The rejected first cut: two parallel folders (`app-pipeline/` and `docs/app-requirements/`) as symmetric peers — this contradicted the app-pipeline's own stated rule ('built apps keep their docs in their own repos') and the dark-factory don't-absorb/staging-not-permanent-home ethos.

## Consequences

Deleted the parallel `docs/app-requirements/` folder and replaced it with a single standard file. Every future app-build candidate now carries a `build_target` field (`sentinel | appystack | kbde-extension | undecided`) that selects its Lane-2 template and constellation layer.

## Related

- Sessions: `2fdc2412`

## Provenance

- **Sessions** (1): `2fdc2412` · 2026-06-23
- **Files** (candidate-level): `apps/dark-factory/docs/app-requirements-spec.md`, `brains/dark-factory/app-pipeline/README.md`
- **Commits** (candidate-level): `ecc9897`

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
