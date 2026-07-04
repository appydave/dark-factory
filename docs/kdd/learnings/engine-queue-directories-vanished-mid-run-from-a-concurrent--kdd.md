---
topic: "Engine queue dirs vanish mid-run"
issue: "Engine queue directories vanished mid-run from a concurrent process reset"
created: "2026-06-07"
story_reference: "f8b8051a"
category: "infrastructure"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["experiments/watchtower-engine/done/q-20260607-board-v5-converge.json"]
commits: []
---

# Engine queue dirs vanish mid-run — Engine queue directories vanished mid-run from a concurrent process reset

## Problem Signature

**Symptoms**: The final `mv` into done/ failed with 'No such file or directory'; a follow-up `ls` showed the running/ and queue/ directories themselves were gone (not just empty)

**Environment**: experiments/watchtower-engine/ (running/, queue/, done/, reports/, runs/) during an in-session Swagger job run

**Triggering Conditions**: Between the initial atomic claim via claim-next.sh (which moved the ticket into running/) and the bookkeeping step several tool-calls later, running/ and queue/ were both removed by some other process — suspected concurrent reaper or state-restore sweep, not directly identified

## Root Cause
Unconfirmed — the session only observed the effect (directories missing); no process was directly caught doing the removal

## Solution
Reconstructed the done/ entry by rewriting the original ticket JSON — still held verbatim in context from the earlier Read — directly into done/, then recreated empty queue/ and running/ directories to restore the expected structure

## Prevention
Before final bookkeeping, verify the claimed-ticket file and target directories still exist rather than assuming the `mv` will succeed; if a directory is found missing mid-run, reconstruct the needed file from data already held in context rather than failing the job

## Related
- Sessions: f8b8051a
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): f8b8051a · 2026-06-07
- **Files** (candidate-level): experiments/watchtower-engine/done/q-20260607-board-v5-converge.json
- **Commits** (candidate-level): —
