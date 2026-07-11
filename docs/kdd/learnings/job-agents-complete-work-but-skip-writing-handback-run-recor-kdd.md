---
topic: "Dispatch-loop telemetry gap"
issue: "Job-agents complete work but skip writing handback/run-record bookkeeping"
created: "2026-06-05"
story_reference: "627e86a2, f7a95652, wg-t3-02 (2026-07-11)"
category: "process"
severity: "high"
status: "proposed"
recurrence_count: 3
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["backlog/2026-06-08-stability-selflearning-lanes.md", "experiments/watchtower-engine/failures/register.jsonl"]
commits: []
---

# Dispatch-loop telemetry gap — Job-agents complete work but skip writing handback/run-record bookkeeping

## Problem Signature

**Symptoms**: Checking the run-record and handback-report locations after several completed jobs showed both missing for jobs that had, by other evidence, actually completed correctly (a design rendered and serving, a spec file written and non-empty).

**Environment**: dark-factory watchtower-engine dispatch loop (queue consumer + Swagger workers)

**Triggering Conditions**: Every job dispatched that day was checked; three of them (and a fourth shortly after) completed their actual work but exited without performing the final bookkeeping steps of the run procedure.

## Root Cause
Writing the run record and the handback is the worker's own responsibility at the end of its procedure, but the worker is exactly the unreliable part of the system — asking it to self-report on its own reliability produces silent gaps rather than visible failures, because a skipped self-report leaves no trace at all.

## Solution
Reframed the fix: telemetry must be captured by things other than the worker — a Dispatcher emits a 'dispatched' event, the claim step and the appearance of a file in the done folder give 'claimed'/'done', a Reaper emits 'teardown'. Derived flags (handback_written?, run_record_written?, teardown_clean?, duration, stray_running?) are computed externally by comparing what should exist against what does, never by trusting the worker's own report.

```bash
# external check that exposed the gap — none of these should ever be empty for a completed job
ls -1 experiments/watchtower-engine/runs/ | tail -6
cat experiments/watchtower-engine/reports/q-20260608-cortex-render.json      # EMPTY/MISSING
cat experiments/watchtower-engine/reports/q-20260608-angelsentinel-spec.json # EMPTY/MISSING
```

## Prevention
Never trust a worker's self-reported completion as the sole signal of a healthy run. Instrument the loop from the outside first — Dispatcher and Reaper emit lifecycle events to a durable log, and an external sweep computes success/failure rates and orphan detection — and only harden the worker's own bookkeeping second, with evidence, not before.

## Related
- Sessions: 627e86a2, f7a95652
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (2): 627e86a2, f7a95652 · 2026-06-05 → 2026-06-08
- **Files** (candidate-level): backlog/2026-06-08-stability-selflearning-lanes.md, experiments/watchtower-engine/failures/register.jsonl
- **Commits** (candidate-level): —
