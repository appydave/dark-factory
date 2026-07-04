> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0031: Multi-Marshall parallelism via identity, not per-file locking

**Status:** Proposed (reconstructed)


## Context
The dark-factory dispatch engine was designed single-writer ('one watcher, never N') but the rule was undocumented as a guard and only actually protects job-ticket claims via rename(2); every other shared file (MEMORY.md, build-state.md, backlog/) has no protection. The repo owner wanted to fire a second Marshall on a different lane whenever an idea lands, without stepping on a first session.

## Decision
Reject the single-writer-vs-multi-writer either/or framing. Adopt a staged sequence: (0) a temporary safety latch that refuses a 2nd Marshall in the same engine dir, (1) give every Marshall/Swagger a stable ID, (2) partition shared state by ID (running/<id>/, registry-by-id) enabling multiple Marshalls on one machine with no Switchboard yet, (3) use git worktrees for build-job filesystem isolation, (4) graduate to Switchboard as the live state-owning registry once Marshalls need to coordinate (not just avoid collision). Identity is the keystone — most collisions today happen because nothing has a stable ID.

## Alternatives Considered
(a) Enforce single-writer permanently via a guard, deferring true multi-writer indefinitely — rejected as too conservative once it was clarified that only 'independent lanes' (easy parallelism) were needed, not full distributed locking across the same epic (hard parallelism, still deferred). (b) Per-file locking ('a traffic light on every shared page') — rejected outright as the wrong mechanism; state ownership belongs in a separate service (Switchboard), not scattered file locks.

## Consequences
Two independent Marshalls can run concurrently on one machine without building Switchboard first, once IDs + state partitioning exist. The known dispatch-swagger.sh serial-binding/reaper limitation is expected to resolve as a side effect of adding IDs. Caution recorded: do not build the Switchboard-registry step before proving identity + partition with two real Marshalls on two real lanes — coordination-layer bugs are subtle.

## Related
- Sessions: ef961b51

## Provenance
- **Sessions** (1): ef961b51 · 2026-06-12
- **Files** (candidate-level): .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/MEMORY.md, .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/constellation-first-placement.md, .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/parallelism-via-identity.md, AUDIT-2026-06-12.md
- **Commits** (candidate-level): —
