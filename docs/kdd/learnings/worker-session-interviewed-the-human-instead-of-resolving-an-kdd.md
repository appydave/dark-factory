---
topic: "worker interviewed human instead of terminating"
issue: "Worker session interviewed the human instead of resolving and terminating"
created: "2026-06-05"
story_reference: "7cfe61d3"
category: "process"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["docs/doc-organiser-proposal.md", "docs/watchtower/build-state.md"]
commits: []
---

# worker interviewed human instead of terminating — Worker session interviewed the human instead of resolving and terminating

## Problem Signature

**Symptoms**: The human replied 'I don't understand' to a compressed summary line listing 4 open questions, then had to separately ask where/how to run the system and what the manager role even was — confusion traced back to talking to the wrong role in the architecture.

**Environment**: experiments/watchtower-engine — the Consumer/worker role, executing an `instruction`-kind queue ticket via the run-next-workflow skill

**Triggering Conditions**: The worker finished its ticket (a proposal doc) but the proposal surfaced sub-decisions still open; instead of picking sensible defaults and closing, the worker's completion message ended with an open question and it kept the session alive to answer human follow-ups.

## Root Cause
The worker's own governing spec (docs/watchtower/build-state.md, rule #5) states workers must report and terminate, never interview the human — only the Conductor (Marshall) is meant to hold a standing conversation with the human. The worker violated this by treating its own open questions as a live discussion instead of self-resolving them.

## Solution
The worker picked all four open defaults itself and locked them into §5 of docs/doc-organiser-proposal.md, then explicitly reoriented the human: close this worker session, open the Marshall session instead, and route all future problems through Marshall rather than talking to workers directly.

## Prevention
A worker/job-agent role should resolve its own open sub-decisions with sensible defaults and record them in the artifact, never surface them as questions requiring live human interaction; only the Conductor role should converse with the human. `Review`/`CI` gates on a worker's completion message should reject a report that ends in an open question rather than a decision-recorded artifact.

## Related
- Sessions: 7cfe61d3
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 7cfe61d3 · 2026-06-05
- **Files** (candidate-level): docs/doc-organiser-proposal.md, docs/watchtower/build-state.md
- **Commits** (candidate-level): —
