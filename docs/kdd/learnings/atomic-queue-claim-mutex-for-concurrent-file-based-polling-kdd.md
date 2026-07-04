---
topic: "atomic queue-claim mutex"
issue: "Atomic queue-claim mutex for concurrent file-based polling"
created: "2026-05-27"
story_reference: "1f8758f3"
category: "architecture"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["experiments/watchtower-engine/bin/claim-next.sh", "experiments/watchtower-engine/bin/test-atomic-claim.sh"]
commits: ["9c3d374"]
---

# atomic queue-claim mutex — Atomic queue-claim mutex for concurrent file-based polling

## Problem Signature

**Symptoms**: Design risk: staggered /loop sessions polling the same queue directory on overlapping 1-4 minute intervals could race and claim/run the same workflow twice.

**Environment**: experiments/watchtower-engine/ — the Watchtower trigger-engine spike, dark-factory repo

**Triggering Conditions**: Multiple interactive sessions independently polling the same queue directory with no coordination mechanism between them.

## Root Cause
No claim/ownership mechanism existed between the queue directory and the multiple processes that might try to pick up the same entry concurrently.

## Solution
Implemented claim-next.sh: the claim operation is a single `mv` (rename(2)) of the entry file from queue/ to running/. rename is atomic at the filesystem level, so exactly one concurrent mv succeeds per file; every losing claimant gets ENOENT (source already gone) and moves on to the next entry in the queue. Verified with a dedicated concurrency test rather than trusted on reasoning alone.

```bash
# experiments/watchtower-engine/bin/claim-next.sh
for f in $(ls -1 "$QUEUE" 2>/dev/null | sort); do
  # The atomic claim. rename() either moves the file (we win) or fails
  # because another claimant already moved it (we lose, try next).
  if mv "$QUEUE/$f" "$RUNNING/$f" 2>/dev/null; then
    echo "$RUNNING/$f"
    exit 0
  fi
done
exit 1
```

Concurrency proof result (200 entries, 8 parallel claimers, 5 iterations):
```
 total claims      : 200
 unique claims     : 200
 moved to running/ : 200
 left in queue/    : 0
PASS — every entry claimed exactly once, zero double-claims, zero lost.
```

## Prevention
When designing shared-queue coordination between concurrent processes, verify the claim mechanism with an actual concurrency stress test (seed N entries, fire multiple parallel claimers, assert total_claims == unique_claims == N and nothing is left stranded) rather than relying on reasoning about atomicity alone.

## Related
- Sessions: 1f8758f3
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 1f8758f3 · 2026-05-27
- **Files** (candidate-level): experiments/watchtower-engine/bin/claim-next.sh, experiments/watchtower-engine/bin/test-atomic-claim.sh
- **Commits** (candidate-level): 9c3d374
