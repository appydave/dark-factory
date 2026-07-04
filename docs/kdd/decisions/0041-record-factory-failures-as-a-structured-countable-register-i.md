> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0041: Record factory failures as a structured, countable register instead of narrating them in prose

**Status:** Proposed (reconstructed)


## Context
Failures observed during factory operation (a job-agent skipping its own completion bookkeeping, a verification method later found inadequate, etc.) were being folded into chat narration and prose docs, one incident described in passing at a time. There was no way to see whether a given failure type was a one-off or a recurring pattern worth root-causing.

## Decision
Build a small append-only failure register: one structured JSON record per failure (what failed, when, severity, component, and what it's linked to — session id / queue id / ticket), plus a helper to append a record in one command and an audit command that counts open failures by category and flags any category that has reached an investigate threshold (default 3).

## Alternatives Considered
Continue narrating failures into whichever doc or chat turn was active at the time (rejected — makes it impossible to count occurrences or see which failure category deserves root-cause attention). A single running prose log of all failures in one file (rejected — same problem, not machine-countable by category).

## Consequences
The register paid for itself immediately: backfilling three known instances of a worker skipping its own completion handback put that category at the investigate threshold on the first run, and a later instance in the same session pushed the count to four — giving a concrete, counted trigger for a previously-only-discussed piece of standing work (instrumenting the dispatch loop externally rather than trusting workers to self-report). The register is currently populated and audited by hand; wiring automatic capture into the dispatch/reap mechanism is future work.

## Related
- Sessions: f7a95652

## Provenance
- **Sessions** (1): f7a95652 · 2026-06-08
- **Files** (candidate-level): experiments/watchtower-engine/failures/audit.sh, experiments/watchtower-engine/failures/record-failure.sh, experiments/watchtower-engine/failures/register.jsonl
- **Commits** (candidate-level): —
