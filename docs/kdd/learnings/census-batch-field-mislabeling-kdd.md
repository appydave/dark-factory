---
topic: "census batch field mislabeling"
issue: "Census batch field mislabeling"
created: "2026-05-27"
story_reference: "1f8758f3"
category: "tooling"
severity: "low"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: [".claude/workflows/level-1-census.workflow.js", "research/census.jsonl"]
commits: []
---

# census batch field mislabeling — Census batch field mislabeling

## Problem Signature

**Symptoms**: After running level-1-census twice, census.jsonl shows records tagged batch: 0 and batch: 5 instead of batch: 0 and batch: 1.

**Environment**: .claude/workflows/level-1-census.workflow.js — the Store phase, dark-factory repo

**Triggering Conditions**: Running the level-1-census workflow more than once with a batchStart value other than a true running index (e.g. batchStart=5 for the second run of batch size 5).

## Root Cause
The Store phase enriches each record with the raw batchStart arg rather than computing or tracking a separate sequential batch counter.

## Solution
Not fixed in this session — explicitly flagged as needing correction in the workflow before the census scales further, since any Watchtower aggregation by batch would otherwise look wrong.

## Prevention
Before building dashboards or aggregations on top of a workflow's output fields, verify what those fields actually encode (e.g. batchStart vs. a true sequence number) rather than assuming the field name matches the intended meaning.

## Related
- Sessions: 1f8758f3
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 1f8758f3 · 2026-05-27
- **Files** (candidate-level): .claude/workflows/level-1-census.workflow.js, research/census.jsonl
- **Commits** (candidate-level): —
