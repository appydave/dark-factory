> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0006: Move Dark Factory job-state off flat files into a Switchboard-hosted shared state plane

**Status:** Proposed (reconstructed)


## Context
Dark Factory's job state lived in flat files (queue/running/done) on the factory floor, with an anonymous atomic-rename claim mechanism (claim-next.sh). This breaks for two goals: (1) parallel orchestration — multiple Marshall sessions can't run without merging work-state via shared files; (2) factory portability — running the factory against other repos required cd-ing out rather than a truly portable capability. An orphaned job-state file surfaced during a live 2nd-orchestrator experiment and exposed the gap.

## Decision
Invest in a Switchboard-hosted service-backed shared-state plane (a durable job-state storage recipe + a claim-arbitration coordination recipe, modeled on Switchboard's existing staleness-detector), turning Marshall instances into stateless clients that talk to ONE stateful bus, rather than cloning the repo/engine per orchestrator.

## Alternatives Considered
(a) In-engine fix — stamp claimed_by + use a per-orchestrator WT_ENGINE_DIR namespace (rejected: solves ownership 'from within the agent,' contradicts the DF-3 spec's 'observe externally' principle). (b) Two independent per-orchestrator engine directories, each its own flat-file queue (rejected: still cloneable flat files racing each other — 'a disaster in normal programming').

## Consequences
DF-7 ticket created (priority 1) with a full requirement PRD (via appydave:spec-writer), 5 open decisions (durable substrate, claimant identity, MCP/HTTP path, reaper requeue authority, retry ownership) all later ruled. Build leg is separate and out-of-app (in the switchboard repo). The same capability simultaneously unblocks factory portability.

## Related
- Sessions: 2df0e613

## Provenance
- **Sessions** (1): 2df0e613 · 2026-06-08
- **Files** (candidate-level): backlog/specs/df7-switchboard-state-plane-spec.md, backlog/specs/tickets.json, experiments/watchtower-engine/bin/claim-next.sh
- **Commits** (candidate-level): —
