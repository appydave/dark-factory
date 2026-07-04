---
id: ADR-0011
title: "KBDE Extension SDK incompleteness is a fragility warning for builders, not a build-blocking gate"
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

# ADR-0011: KBDE Extension SDK incompleteness is a fragility warning for builders, not a build-blocking gate

**Status:** Proposed (reconstructed)

## Context

When the constellation map's Layer-2 (surfaces/KBDE extensions) was first pinned, David's two build constraints ('dogfood the build through the factory's own loop' and 'the KBDE Extension SDK is a pending handover, not researchable') were recorded as: any Layer-2/KBDE-extension work is BLOCKED until the SDK handover lands, Layer-1 data-source work is not blocked. Hours later, on the same day the factory shipped its first real extension attempt, David corrected this reading.

## Decision

The SDK being unfinished means building against it is 'shifting ground' — expect fragility, incomplete docs, breaking changes — but building extensions is explicitly allowed and wanted. Friction reports produced by real extension builds are valuable input back into David's own SDK development, not a reason to wait.

## Alternatives Considered

The earlier, over-cautious reading — treat every `kbde-extension` candidate as fully blocked until the SDK handover is 'finished' — was rejected as a misreading; David never said none of them should be built, only that the ground was unstable.

## Consequences

Unblocked the same-day omi-fetch KBDE extension build, which produced a concrete `FRICTION.md` ranking real SDK gaps (see the companion 'KBDE extension handler wiring is not additive' learning) — direct, real-consumer input to the SDK author.

## Related

- Sessions: `2fdc2412`

## Provenance

- **Sessions** (1): `2fdc2412` · 2026-06-23
- **Files** (candidate-level): `apps/dark-factory/docs/constellation-map.md`
- **Commits** (candidate-level): `ecc9897`

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
