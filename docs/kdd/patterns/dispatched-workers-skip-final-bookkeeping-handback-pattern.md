---
topic: "Dispatched-worker bookkeeping gap"
issue: "Dispatched workers complete their real work but silently skip the final bookkeeping/handback steps of their procedure"
created: "2026-07-11"
category: "process"
severity: "high"
status: "proposed"
recurrence_count: 3
promoted_from_learning: "job-agents-complete-work-but-skip-writing-handback-run-recor-kdd.md"
provenance: promoted-live
provenance_grain: candidate
story_reference: "627e86a2, f7a95652, wg-t3-02 (2026-07-11)"
files: ["engine/orchestrator.py", "canonical/skills/review-dimensional/provenance.json"]
commits: ["153f42e"]
tags: [worker, telemetry, bookkeeping, hitl, engine]
---

# Pattern — Dispatched workers finish the work, skip the final bookkeeping

## The recurring shape

A dispatched worker does its actual task correctly, then **exits without the trailing bookkeeping**
its procedure requires — run records, handback reports, INDEX rows, backlog-close, ledger writes.
The work is real; the trace of it is missing.

- **×1 (2026-06-05):** watchtower-engine jobs completed (design rendered, spec written) but no
  run-record / handback existed for them.
- **×2:** same gap re-observed across the dispatch loop.
- **×3 (2026-07-11, wg-t3-02):** the ratification worker applied *some* of the artifact fixes but
  never finished the multi-step bookkeeping (INDEX ratified-count, backlog→done, learnings) → verify
  false-failed, retries exhausted. Had to be completed by the PO seat.

## Why it keeps happening

The worker is the **unreliable part of the system**, and the bookkeeping is the *last* thing in its
procedure — the first thing dropped under time pressure, a timeout, or a long apply. Asking the
worker to self-report on its own completion produces **silent gaps, not visible failures**: a skipped
step leaves no trace.

## Design implication

Do not rely on the worker to record its own completion. **Capture completion externally** — a
dispatcher/reaper emits lifecycle events; derived flags (`handback_written?`, `index_updated?`,
`bookkeeping_complete?`) are computed by comparing what *should* exist against what *does*. For
multi-step applies (ratification), make the bookkeeping **resumable and externally-verified**, not a
single atomic self-report. Tie-in: [[engine-has-no-hitl-park-state-designed-pause-read-as-wedged]]
(the same class — the engine can't model a worker that legitimately isn't "done" yet).
