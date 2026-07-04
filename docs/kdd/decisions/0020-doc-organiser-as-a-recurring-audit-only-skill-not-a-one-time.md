---
id: ADR-0020
title: "Doc organiser as a recurring audit-only skill, not a one-time cleanup or autofix"
status: superseded
superseded_by: ADR-0021
scope: internal
date_decided: 2026-06-05
deciders: [David Cruwys]
confidence: reconstructed
recurrence_count: 1
provenance:
  sessions: ["7cfe61d3"]
  files: ["backlog/2026-06-05-doc-organiser.md", "docs/INDEX.md", "docs/doc-organiser-proposal.md"]
  commits: []
tags: []
---

> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0020: Doc organiser as a recurring audit-only skill, not a one-time cleanup or autofix

**Status:** Superseded by [ADR-0021](0021-don-t-build-a-new-doc-organiser-skill-wire-the-existing-doc-.md)

## Context

docs/watchtower/symphony-spec.md and docs/watchtower/watchtower-from-symphony.md exist on disk but have no line in docs/INDEX.md — live proof the index-coverage discipline (docs/INDEX.md, Problem Register #1) already drifts because nothing checks it.

## Decision

Build a recurring `doc-organiser` audit skill, dispatched as a Watchtower instruction job — audit-only, never autofix. Four defaults locked into the proposal: (1) build the recurring skill directly, no separate one-time cleanup pass first — the skill's first run performs the same cleanup; (2) no age-based staleness flagging — only flag things that are actually broken (orphans, dead cross-refs, lying date-stamps); (3) reports print in-chat only, nothing written to docs/_reports/ — so the audit tool can't itself become the doc-sprawl it exists to catch; (4) defer the fuzzy duplication-detection check (e.g. architecture.md vs spec.md overlap) to a later version, ship v1 with only the five exact yes/no checks.

## Alternatives Considered

A one-time manual cleanup pass before building the skill — rejected, duplicates work since the skill's first run does the same cleanup. A 30/60-day staleness threshold — rejected, 'old' doesn't mean 'broken'. Writing dated report files to docs/_reports/ — rejected, report history itself risks becoming the sprawl the tool prevents. Shipping fuzzy duplicate-detection in v1 — deferred, it's guesswork compared to the other exact checks.

## Consequences

The build is parked as a side-quest in backlog/2026-06-05-doc-organiser.md, explicitly off the primary C1→C5 runtime-build spine — nothing happens with it until resurfaced. Scope is docs/ only (research/ stays out, per north-star.md's frozen-corpus rule). Duplicate-detection stays a known gap until v2.

## Related

- Sessions: `7cfe61d3`

## Provenance

- **Sessions** (1): `7cfe61d3` · 2026-06-05
- **Files** (candidate-level): `backlog/2026-06-05-doc-organiser.md`, `docs/INDEX.md`, `docs/doc-organiser-proposal.md`
- **Commits** (candidate-level): —

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
- 2026-07-04 — superseded — linked to ADR-0021, the same-day reversal of this decision (first live use of the `supersedes`/`superseded_by` fields per ADR-0044).
