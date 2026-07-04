---
id: ADR-0009
title: "Dark-factory apps are mapped as a 3-layer stack (data → surfaces → KBDE host), not a flat inventory"
status: proposed
scope: internal
date_decided: 2026-06-23
deciders: [David Cruwys]
confidence: reconstructed
recurrence_count: 1
provenance:
  sessions: ["2fdc2412"]
  files: ["apps/dark-factory/docs/constellation-map.md"]
  commits: ["ecc9897"]
tags: []
---

> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0009: Dark-factory apps are mapped as a 3-layer stack (data → surfaces → KBDE host), not a flat inventory

**Status:** Proposed (reconstructed)

## Context

An earlier request to build a 'morning briefing' digest was challenged: a briefing built from whatever data source happened to be reachable would just be another blind hidden document, and there was no visual harness to render anything anyway. A full filesystem+registry audit found the registries badly incomplete (entire Kybernesis and Baku clusters off-registry, a naming trap between appyradar-sentinal/-sentinel, stale statuses). David then pruned the raw audit list app by app, revealing it wasn't a flat list at all but three distinct roles.

## Decision

Every app in the constellation is classified into exactly one of three layers: DATA (sources → data-plane sentinels/MCP → boilerplate to scaffold more), SURFACES (a data slice + a way to see it — candidates to become KBDE extensions), and HOST (KBDE/KyberAgent, where surfaces mount as extensions across typed channels). Written as the canonical `docs/constellation-map.md`, with David's own verdicts (not inferred) tagging each app extension/data-plane/boilerplate/business/parked/dead.

## Alternatives Considered

Keep the surface-only `observability-surface-audit.md` (a live-state snapshot of only 7 surfaces) as the reference; or leave the audit as an unsorted flat table of ~40 apps with no layer/role distinction.

## Consequences

Gives every future build a clear layer to land in and exposes which layer is buildable now (data) vs blocked (surfaces, pending the KBDE SDK handover — see the companion build-constraints decision). Became the source data structure the same-day App Registry build (`app-registry`) reads to compute liveness/drift.

## Related

- Sessions: `2fdc2412`

## Provenance

- **Sessions** (1): `2fdc2412` · 2026-06-23
- **Files** (candidate-level): `apps/dark-factory/docs/constellation-map.md`
- **Commits** (candidate-level): `ecc9897`

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
