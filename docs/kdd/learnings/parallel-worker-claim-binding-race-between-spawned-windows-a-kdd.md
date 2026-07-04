---
topic: "Parallel worker claim-binding race"
issue: "Parallel worker claim-binding race between spawned windows and tickets"
created: "2026-06-05"
story_reference: "627e86a2"
category: "infrastructure"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["backlog/2026-06-08-stability-selflearning-lanes.md"]
commits: []
---

# Parallel worker claim-binding race — Parallel worker claim-binding race between spawned windows and tickets

## Problem Signature

**Symptoms**: No misbinding occurred in this run because the dispatch was staggered deliberately, but the mechanism was identified live as the root cause of a known, previously logged instability item.

**Environment**: dark-factory watchtower-engine spike, multi-worker dispatch via tmux

**Triggering Conditions**: Multiple tickets present in the queue directory at the same time as multiple workers being spawned — the atomic-rename claim step picks 'the oldest' with no way to steer a specific spawned window to a specific ticket.

## Root Cause
The claim mechanism (atomic rename of the oldest queue file into a running folder) has no concept of which spawned process should get which ticket — it is a race by design once more than one ticket and more than one spawn are in flight simultaneously.

## Solution
Dispatch one worker, poll until that worker has actually claimed its ticket (confirmed by the queue directory draining), and only then write the second ticket and spawn the second worker — serializing the claim step even though the workers subsequently run concurrently.

```bash
# dispatch worker A (only ticket in queue) and WAIT for it to claim before releasing ticket B
bash experiments/watchtower-engine/bin/dispatch-swagger.sh swagger-angel q-20260608-angelsentinel-spec
# ...poll queue/ until it drains (worker A claimed) ~18s...
# only now write/queue ticket B and dispatch worker B
bash experiments/watchtower-engine/bin/dispatch-swagger.sh swagger-cortex-render q-20260608-cortex-render
```

## Prevention
The durable fix is claim-by-id (a Worker is told exactly which ticket id to claim, not merely 'the oldest'), so the Dispatcher never needs to serialize spawns to get correct binding. Until that is built, the Dispatcher must stagger: wait for a confirmed claim before releasing or dispatching the next ticket.

## Related
- Sessions: 627e86a2
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 627e86a2 · 2026-06-05
- **Files** (candidate-level): backlog/2026-06-08-stability-selflearning-lanes.md
- **Commits** (candidate-level): —
