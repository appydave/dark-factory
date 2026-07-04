---
topic: "Unverified build-provenance assumption"
issue: "Build/dev-history claims stated without verifying against git history"
created: "2026-06-08"
story_reference: "1b7b1ab9, 2df0e613"
category: "process"
severity: "medium"
status: "proposed"
recurrence_count: 2
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["backlog/specs/tickets.json"]
commits: []
---

# Unverified build-provenance assumption — Build/dev-history claims stated without verifying against git history

## Problem Signature

**Symptoms**: A direct question caught an unverified claim already written into the ticket registry's build_via field: how Switchboard was actually made was never checked.

**Environment**: backlog/specs/tickets.json (the DF-7 ticket) and the millwright skill's build-technique decision matrix.

**Triggering Conditions**: The millwright matrix states 'change to a constellation app → Ralphy, in-app' as a general rule; this was applied to Switchboard without checking Switchboard's own git history.

## Root Cause
A memory documenting that one specific app was built via Ralphy was treated as a general 'all constellation apps are built via Ralphy' doctrine and never verified against Switchboard's actual history before being written into a ticket as fact.

## Solution
Ran `git log --oneline --no-merges` on the switchboard repo — confirmed it was scaffolded by create-appysentinel and built out through a series of feat: commits dispatched as dark-factory Swagger jobs, with no Ralphy/AGENTS.md/.ralphy campaign anywhere. Corrected the build_via field in tickets.json and flagged the general doctrine as needing a revisit.

```diff-before
"build_via": "ralphy (in-app — switchboard repo; add storage + coordination recipes modeled on staleness-detector)",
```
```diff-after
"build_via": "TBD — NOT ralphy (correction 2026-06-09: Switchboard was built via create-appysentinel scaffold + dark-factory Swagger through the loop, no Ralphy). Build method is itself an open question for the greenfield charter.",
```

## Prevention
Before writing a 'how was X built' or 'how X will be built' claim into a ticket/spec as fact, verify against that specific repo's git log rather than generalizing from another app's memory, even when the memory documents an established pattern elsewhere.

## Related
- Sessions: 1b7b1ab9, 2df0e613
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (2): 1b7b1ab9, 2df0e613 · 2026-06-08 → 2026-06-10
- **Files** (candidate-level): backlog/specs/tickets.json
- **Commits** (candidate-level): —
