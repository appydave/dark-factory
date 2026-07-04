> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.
> Merged 2026-07-04 from two same-day reconstructed candidates (sessions `940816e3` and `2df0e613`,
> both 2026-06-08) that recorded the same decision from two passes over the same working day —
> originally staged separately as ADR-0006 and ADR-0023.

# ADR-0006: Move Dark Factory job-state off flat files into a Switchboard-hosted shared state plane

**Status:** Proposed (reconstructed)


## Context
Dark Factory's job work-state lives in flat files on the factory floor
(`experiments/watchtower-engine/{queue,running,done,reports}/`), claimed via an atomic-rename mutex
(`bin/claim-next.sh` — `rename(2)` moving `queue/<id>.json` to `running/<id>.json` so exactly one
racer wins). This is correct for a single Marshall against a single folder on a single machine, but
breaks for two goals: (1) parallel orchestration — multiple Marshall sessions can't run without
merging work-state via shared files; (2) factory portability — running the factory against other
repos/apps required cd-ing out rather than a truly portable capability. An orphaned job-state file
surfaced during a live 2nd-orchestrator experiment and exposed the gap.

## Decision
State home moves to a service-backed shared-state plane: **Switchboard** owns the job pool/claims/
ownership (modeled on its existing staleness-detector), **AngelEye** provides liveness, **AppyCtrl**
(unbuilt) handles dead-process reaping, and **Watchtower** is the view — turning Marshall instances
into stateless clients that talk to ONE stateful bus, rather than cloning the repo/engine per
orchestrator. The existing atomic-rename mutex is treated as the proven scaffold being built up
from, not thrown away. Produced as a SPEC ONLY document (`backlog/specs/df7-switchboard-state-plane-spec.md`);
the build is a separate, later Ralphy-in-app leg against the switchboard repo.

## Alternatives Considered
- **In-engine fix** — stamp `claimed_by` + use a per-orchestrator `WT_ENGINE_DIR` namespace.
  Rejected: solves ownership "from within the agent," contradicts the DF-3 spec's "observe
  externally" principle.
- **Two independent per-orchestrator engine directories**, each its own flat-file queue. Rejected:
  still cloneable flat files racing each other.
- **Cloning the repo per Marshall**, racing a shared `running/` directory over git. Explicitly
  rejected as fork/merge-hell.

## Consequences
DF-7 ticket created (priority 1) with a full requirement PRD (via `appydave:spec-writer`). Five
OPEN DECISIONs were left inline for David to resolve before any build starts (durable substrate,
claimant identity, MCP/HTTP path, reaper requeue authority, retry ownership) — all later ruled. The
spec must cohere with DF-3 (`backlog/specs/stability-1-instrument-loop-spec.md`) so the state plane
and the observability plane share one bus without duplicating responsibilities. Build leg is
separate and out-of-app (in the switchboard repo). The same capability simultaneously unblocks
factory portability.

## Related
- Sessions: `2df0e613`, `940816e3`

## Provenance
- **Sessions** (2): `2df0e613` · 2026-06-08, `940816e3` · 2026-06-08
- **Files** (candidate-level): `backlog/specs/df7-switchboard-state-plane-spec.md`, `backlog/specs/tickets.json`, `experiments/watchtower-engine/bin/claim-next.sh`
- **Commits** (candidate-level): —
