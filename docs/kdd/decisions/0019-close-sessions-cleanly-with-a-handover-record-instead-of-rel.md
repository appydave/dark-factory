> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0019: Close sessions cleanly with a handover record instead of relying on conversation compaction

**Status:** Proposed (reconstructed)


## Context
The default mechanism for a long session running low on context is compaction, which keeps a degraded copy of the conversation itself alive. The operator does not want that — the desire is to be able to close a session down entirely and pick the work back up cleanly in a brand-new window.

## Decision
Treat the conversation as disposable and put all state that matters into files instead: auto-loading memory entries for durable decisions/corrections, a spec/ticket registry for planned work, the on-disk state of the working engine (queue/running/done/runs/reports folders), any served artifacts, and a written handover document listing what's running, what's clean, and what's next. A fresh session in a new window reads the auto-loaded memories plus the handover document and the registry to resume with no loss.

## Alternatives Considered
Compaction with a handover layered on top of it — rejected by the operator explicitly: it keeps a degraded conversation alive instead of cleanly discarding it, which was the behaviour being rejected, not just supplemented.

## Consequences
A handover document was written for this session capturing what's running (must not be restarted), what's clean (nothing to reap), and the current state of the spec registry, structured so a new session's startup routine can read it directly. This depends on state genuinely being externalized during the session (memories, registry, on-disk engine state) — a session that only holds decisions in the conversation cannot produce an accurate handover.

## Related
- Sessions: 627e86a2

## Provenance
- **Sessions** (1): 627e86a2 · 2026-06-05
- **Files** (candidate-level): backlog/2026-06-08-session-handover.md
- **Commits** (candidate-level): —
