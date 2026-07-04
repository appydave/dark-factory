> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0016: Worker session teardown must be a deliberate, gated lifecycle — never auto-kill the instant a job completes

**Status:** Proposed (reconstructed)


## Context
Investigating the orphan-process bug surfaced a design constraint: the operator explicitly wants to be able to jump into a running worker's window and help, or have the worker surface a question directly to the operator — not just report to the Orchestrator. That rules out the simplest fix for orphaning ('kill the window the instant its job hits the done folder'), because that could forcibly close a window the operator is mid-conversation with.

## Decision
A worker (Swagger) is a talkable orchestrator, not a sealed batch job: it may delegate to sub-agents/workflows AND the operator may engage it directly. What is banned is a worker silently blocking on an unexpected interactive Q&A instead of putting the question in its deliverable and continuing — not human contact itself. Consequently, teardown must be a deliberate lifecycle (a persisted registry entry + a reaper sweep + a grace window after job completion), never an immediate auto-kill on job completion.

## Alternatives Considered
Auto-kill the window the instant the ticket lands in the done folder — rejected: this is the fix that would work for the orphaning bug in isolation, but it conflicts with the talkable-orchestrator requirement and would forcibly close a session the operator might still be using.

## Consequences
The orphan-lifecycle fix (registry + reaper + grace window) became its own backlog item rather than a one-line auto-kill; a reaper script was later built and used successfully across multiple dispatch runs (including a staggered two-worker dispatch) with a grace period before reaping a finished window.

## Related
- Sessions: 627e86a2

## Provenance
- **Sessions** (1): 627e86a2 · 2026-06-05
- **Files** (candidate-level): backlog/2026-06-06-swagger-lifecycle.md, docs/watchtower/build-state.md
- **Commits** (candidate-level): 2d09641
