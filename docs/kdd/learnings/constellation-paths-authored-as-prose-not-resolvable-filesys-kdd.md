---
topic: "Constellation paths are prose, not resolvable"
issue: "Constellation paths authored as prose, not resolvable filesystem paths"
created: "2026-06-23"
story_reference: "2fdc2412"
category: "tooling"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["apps/app-registry/lib/crossref.py", "apps/dark-factory/docs/constellation-map.md"]
commits: []
---

# Constellation paths are prose, not resolvable — Constellation paths authored as prose, not resolvable filesystem paths

## Problem Signature

**Symptoms**: The liveness probe could not resolve a real absolute path for many constellation entries; a subset (the Kybernesis cluster) also lived at a different base directory than assumed (`~/dev/kybernesis/*`, not `~/dev/ad/kybernesis/*`).

**Environment**: App Registry v1 build (`apps/app-registry`), consuming `apps/dark-factory`'s constellation-map-derived data, 2026-07-03.

**Triggering Conditions**: Probing every constellation app for liveness (process/port/launchd signals) requires a resolvable absolute path per app; the source data was authored for a human reader, not for machine consumption.

## Root Cause
constellation.json stored `path_raw` as prose strings copied from the human-facing constellation-map.md instead of verified absolute paths, and the Kybernesis cluster's real location differed from the naming pattern used elsewhere in the monorepo.

## Solution
Built a 30-entry, filesystem-verified PATH_OVERRIDES table mapping each app id to its real absolute path, used instead of trusting the raw prose path field.

## Prevention
When a build (Dev-side) consumes data authored for a human (PO-side canonical doc), verify every path actually resolves on disk before treating it as load-bearing — don't assume prose fields in a narrative doc are machine-usable paths.

## Related
- Sessions: 2fdc2412
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 2fdc2412 · 2026-06-23
- **Files** (candidate-level): apps/app-registry/lib/crossref.py, apps/dark-factory/docs/constellation-map.md
- **Commits** (candidate-level): —
