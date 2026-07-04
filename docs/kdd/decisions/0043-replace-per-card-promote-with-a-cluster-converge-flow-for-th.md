> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0043: Replace per-card 'promote' with a cluster CONVERGE flow for the Floor↔Lanes bridge

**Status:** Proposed (reconstructed)


## Context
The v4 Floor↔Lanes bridge put a 'promote ▶' button on every lane card — including done concepts and status notes — and each press emitted a separate, vague 'elaborate this concept' instruction ticket. This was noisy and skipped any synthesis across related concepts, which was the actual point of surfacing them together in a lane.

## Decision
Removed the per-card promote button and the POST /api/promote endpoint. Added click-to-toggle multi-select on lane cards plus a sticky bottom action bar that appears only once >=2 cards are selected ('Converge N concepts → brief ▶'), backed by a new POST /api/converge endpoint and a pure buildConvergeTicket(items, nowMs) function that writes ONE synthesis ticket per selected cluster (kind: instruction, experiment_id: exp-converge) instead of N separate elaborate tickets.

## Alternatives Considered
Keep the v4 per-card promote flow — rejected because it put a button on every card (including already-done ones), produced only vague single-concept 'elaborate' tickets, and structurally could not do cluster synthesis.

## Consequences
The converge action bar only activates at >=2 selections, so single-concept promotion is no longer possible from the Lanes view. Ticket shape changed (new prompt format asking the receiving agent to pick the brief's form and write it to docs/watchtower/converged-briefs/<slug>.md). selfcheck-promote.mjs was deleted in favor of selfcheck-converge.mjs. Floor view, /api/state, /api/concepts, and staleness logic were deliberately left untouched.

## Related
- Sessions: f8b8051a

## Provenance
- **Sessions** (1): f8b8051a · 2026-06-07
- **Files** (candidate-level): experiments/watchtower-board/selfcheck-converge.mjs, experiments/watchtower-board/server.mjs
- **Commits** (candidate-level): —
