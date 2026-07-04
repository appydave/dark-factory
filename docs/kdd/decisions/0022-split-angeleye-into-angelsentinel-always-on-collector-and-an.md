> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0022: Split AngelEye into AngelSentinel (always-on collector) and AngelEye Control Plane (dashboard)

**Status:** Proposed (reconstructed)


## Context
AngelEye was one Express+React monorepo doing two jobs in one process: collecting Claude Code telemetry (hook ingestion, transcript reading, liveness/session-class classification) and visualising it (React dashboard + query/CRUD API). The Sentinel pattern (referenced from the appysentinal boilerplate) treats these as two distinct products: an always-on headless collector that never runs `claude`, and a separate viewer/control plane. A Swagger job (queue ticket q-20260608-angelsentinel-spec) was dispatched to research both codebases read-only and produce a split spec.

## Decision
Split AngelEye into two products: AngelSentinel — an always-on collector that never runs `claude`, owning hook ingestion endpoints, session/transcript readers, the sole-writer registry store, the liveness API, the Socket.io event broadcast, and a new tool-usage telemetry roll-up; and AngelEye Control Plane — the React client plus viz/query/CRUD API, classifier, correlator, and workflow/workspace/enrichment services, which reads from AngelSentinel. The split maps ~10 server modules to AngelSentinel and ~28 server modules plus all of client/ to the Control Plane. The research was read-only; the only write was the spec document itself.

## Alternatives Considered
Keep AngelEye as a single fused collector+viewer process (status quo) — rejected because it conflates the Sentinel and Viewer patterns and AngelEye has no production daemon/service path for headless collection (only a dev launcher and a single-process Docker setup), whereas AngelSentinel needs a launchd/systemd service modelled on appysentinal's install-service.sh.

## Consequences
Before the split can be built: 8 refactor areas were flagged (hooks.ts overloaded, monolithic shared types, fused backfill+sync, hardcoded client noise filter, non-invalidating config cache, hardcoded workflow type, unbounded write-queue, lockable seed boolean). AngelSentinel must be the sole writer of ~/.claude/angeleye/registry.json, with Control Plane mutations going through a guarded write endpoint. A new tool-usage telemetry capability (heavy/dead/never_used roll-up) becomes part of AngelSentinel's scope. The spec left 5 open decisions for David and is a design document only — Ralphy builds it later, no code was modified in this session.

## Related
- Sessions: 8fcd0c4f

## Provenance
- **Sessions** (1): 8fcd0c4f · 2026-06-07
- **Files** (candidate-level): experiments/watchtower-engine/queue/q-20260608-angelsentinel-spec.json, experiments/watchtower-engine/runs/run-angelsentinel-001.json, ~/dev/ad/apps/angeleye/docs/requirements/angelsentinel-split-spec-2026-06-08.md
- **Commits** (candidate-level): —
