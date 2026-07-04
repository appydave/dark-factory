> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0007: Switchboard has CRUD authority over its own comms domain; 'never kill' applies only to the externally observed system

**Status:** Proposed (reconstructed)


## Context
DF-7's spec proposed the job-coordinator recipe requeue a dead claimant's job-state record (claimed→pool). This was initially challenged by reading the 'detect+tell, Switchboard doesn't kill' doctrine as 'Switchboard must be read-only/observer-only,' recommending requeue logic live in Marshall's reaper/Monitor instead.

## Decision
Switchboard is a switchboard — it routes and owns the durable write-side of its own domain (queue, job-state records, routing, event log), so requeuing a dead claimant's state record is broker CRUD and belongs in Switchboard's job-coordinator. The 'never kills' rule is narrow: it only forbids mutating the externally observed system (killing a process, tmux kill-window, touching watched files) — those destructive actions stay with Marshall's Monitor / AppyCtrl.

## Alternatives Considered
Keep all requeue/ownership-mutation logic external to Switchboard (in Marshall's reaper/Monitor), treating Switchboard as purely detect+report — rejected because it conflated 'doesn't kill externally' with 'read-only,' which contradicts the switchboard-bus-direction design ('owns the queue... on-grain, not an observer-only violation').

## Consequences
DF-7's D4 approved as originally spec'd (coordinator may requeue state). Two memories corrected (cleanup-is-harness-driven-not-remembered, and the DF-7 spec itself) to state the CRUD-vs-kill line explicitly, preventing future mis-reads of the 'detect+tell' doctrine as 'observer-only.'

## Related
- Sessions: 2df0e613

## Provenance
- **Sessions** (1): 2df0e613 · 2026-06-08
- **Files** (candidate-level): backlog/specs/df7-switchboard-state-plane-spec.md
- **Commits** (candidate-level): —
