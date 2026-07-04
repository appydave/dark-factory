---
topic: "Drift check conflated activity with liveness"
issue: "Drift check conflated activity status with liveness"
created: "2026-06-23"
story_reference: "2fdc2412"
category: "debugging"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["apps/app-registry/lib/liveness.py", "apps/app-registry/query.py"]
commits: []
---

# Drift check conflated activity with liveness — Drift check conflated activity status with liveness

## Problem Signature

**Symptoms**: 14 apps were incorrectly reported as drifted between the constellation map and the live probe state.

**Environment**: App Registry v1's `query.py drift` command, build #2 of the 2026-07-03 factory-run cut.

**Triggering Conditions**: Comparing two similarly-named but semantically different status fields ('active' = project activity vs 'running' = liveness) as if they were interchangeable.

## Root Cause
The drift check's string comparison treated any non-matching status as drift without checking that both sides used the same vocabulary; 'active' and 'running' answer different questions.

## Solution
Narrowed the drift comparison to only compare the literal 'running' value against the live probe's verdict, dropping the false equivalence with 'active'.

## Prevention
Before diffing two status fields from different sources, confirm they encode the same concept; keep differently-scoped status fields (project-activity vs liveness vs registry-status) as separate named fields rather than collapsing them into one comparison.

## Related
- Sessions: 2fdc2412
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 2fdc2412 · 2026-06-23
- **Files** (candidate-level): apps/app-registry/lib/liveness.py, apps/app-registry/query.py
- **Commits** (candidate-level): —
