> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0023: Move job work-state off flat files onto a service-backed shared-state plane (Switchboard)

**Status:** Proposed (reconstructed)


## Context
Dark Factory's job work-state lives in flat files on the factory floor (experiments/watchtower-engine/{queue,running,done,reports}/), claimed via an atomic-rename mutex (bin/claim-next.sh — rename(2) moving queue/<id>.json to running/<id>.json so exactly one racer wins). This is correct for a single Marshall against a single folder on a single machine, but breaks for two goals: parallel orchestration (multiple Marshall sessions need to share work-state) and factory portability (operating on apps in other folders).

## Decision
State home moves to a service-backed shared-state plane: Switchboard owns the job pool/claims/ownership, AngelEye provides liveness, AppyCtrl (unbuilt) handles dead-process reaping, and Watchtower is the view. The existing atomic-rename mutex is treated as the proven scaffold being built up from, not thrown away. Produced as a SPEC ONLY document (backlog/specs/df7-switchboard-state-plane-spec.md); the build is a separate, later Ralphy-in-app leg against the switchboard repo.

## Alternatives Considered
Cloning the repo per Marshall and racing a shared running/ directory over git was considered and explicitly rejected as fork/merge-hell.

## Consequences
Five OPEN DECISIONs were left inline for David to resolve before any build starts. The spec must cohere with DF-3 (backlog/specs/stability-1-instrument-loop-spec.md) so the state plane and the observability plane share one bus without duplicating responsibilities.

## Related
- Sessions: 940816e3

## Provenance
- **Sessions** (1): 940816e3 · 2026-06-08
- **Files** (candidate-level): backlog/specs/df7-switchboard-state-plane-spec.md, experiments/watchtower-engine/bin/claim-next.sh
- **Commits** (candidate-level): —
