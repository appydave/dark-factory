---
id: ADR-0004
title: "Workflow execution model: queue file + in-session polling skill, never headless or metered-credit execution"
status: proposed
scope: internal
date_decided: 2026-05-27
deciders: [David Cruwys]
confidence: reconstructed
recurrence_count: 1
provenance:
  sessions: ["1f8758f3"]
  files: ["docs/watchtower/HANDOVER.md", "experiments/watchtower-engine/README.md", "experiments/watchtower-engine/bin/claim-next.sh", "experiments/watchtower-engine/bin/test-atomic-claim.sh", "experiments/watchtower-engine/skills/run-next-workflow/SKILL.md"]
  commits: ["9c3d374"]
tags: []
---

> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0004: Workflow execution model: queue file + in-session polling skill, never headless or metered-credit execution

**Status:** Proposed (reconstructed)

## Context

A five-axis design review (agent-skills:code-review-and-quality) flagged (finding C2) that both candidate trigger mechanisms — file-trigger and shell-exec — silently assumed a non-Claude background process could execute a .workflow.js headlessly, which was never verified; the Workflow tool runs inside an interactive Claude Code session. Separately, Agent SDK and `claude -p` were ruled out because both start requiring metered API-credit billing from 2026-06-15, which would break the constraint that Dark Factory automation runs on David's existing subscription.

## Decision

Workflows never run headless. A trigger writes a queue entry (workflow name, experiment_id, args) to a queue directory. A skill (run-next-workflow) running inside an ordinary interactive Claude Code session polls the queue on a /loop interval, atomically claims the oldest entry by moving it from queue/ to running/ (a single rename(2)), and runs the workflow inline and visibly (via the Workflow tool / /workflows panel) rather than in a blind Task sub-agent. Up to 4 staggered sessions may poll concurrently; the atomic rename is the only coordination mechanism needed — no lock files, no daemon, no DB.

## Alternatives Considered

Headless daemon/subprocess execution of the workflow harness — rejected as unverified and likely infeasible since the Workflow tool needs a live session. Agent SDK or `claude -p` for background execution — rejected outright because both incur metered billing starting 2026-06-15. Running each queued workflow inside a blind Task sub-agent to keep the polling session's context thin — proposed then explicitly retracted: it loses live visibility into tool calls (David's objection), and turned out to be solving a problem that doesn't exist yet, since the Workflow tool already isolates each sub-agent's heavy context into its own transcript and only returns a small result to the calling session (~3-5K tokens per run vs. the full 169K-259K token workflow cost).

## Consequences

Splits the Watchtower build into two independently provable halves: the engine (queue dir + atomic-claim mutex + run-next-workflow skill — pure files + one skill, no app code) and the surface (the AppyStack app that just writes queue entries and shows state). The mutex was stress-tested (200 entries x 8 concurrent claimers x 5 iterations, zero double-claims) and then proven end-to-end for real: the engine claimed a seeded census-batch-1 entry, ran level-1-census via the Workflow tool, wrote a run record, and moved the entry to done/ — appending 5 real records to census.jsonl.

## Related

- Sessions: `1f8758f3`

## Provenance

- **Sessions** (1): `1f8758f3` · 2026-05-27
- **Files** (candidate-level): `docs/watchtower/HANDOVER.md`, `experiments/watchtower-engine/README.md`, `experiments/watchtower-engine/bin/claim-next.sh`, `experiments/watchtower-engine/bin/test-atomic-claim.sh`, `experiments/watchtower-engine/skills/run-next-workflow/SKILL.md`
- **Commits** (candidate-level): `9c3d374`

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
