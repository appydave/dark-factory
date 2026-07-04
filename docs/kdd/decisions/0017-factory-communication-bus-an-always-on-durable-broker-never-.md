---
id: ADR-0017
title: "Factory communication bus: an always-on durable broker (never runs claude) paired with in-session reactive listeners, over SSE topic-subscription rather than a filesystem"
status: proposed
scope: internal
date_decided: 2026-06-05
deciders: [David Cruwys]
confidence: reconstructed
recurrence_count: 1
provenance:
  sessions: ["627e86a2"]
  files: ["backlog/2026-06-06-dark-factory-sentinel.md", "experiments/watchtower-engine/spikes/synapse-probe/run-probe.sh", "experiments/watchtower-engine/spikes/synapse-probe/server.py"]
  commits: []
tags: []
---

> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0017: Factory communication bus: an always-on durable broker (never runs claude) paired with in-session reactive listeners, over SSE topic-subscription rather than a filesystem

**Status:** Proposed (reconstructed)

## Context

Three open problems (external session-trigger, orphan-process reaping, unreliable return-leg reporting) were each being solved piecemeal from inside a terminal session. A background research pass into a candidate always-on service template confirmed it is pure observer code with zero agent-invocation in its runtime — it cannot dispatch or execute work itself, only observe and expose data — so it cannot naively be 'the thing you message and it does work for you.'

## Decision

Split the architecture into a durable layer and an ephemeral layer: an always-on broker (built from the observer-service template) owns the queue, a process registry/reaper, and routing, and pushes events outward; each in-session agent (on the metered-free interactive subscription) arms a persistent long-running listener whose command consumes that push stream directly and turns each event into a wake-up. Transport is SSE with server-side topic subscription (a subscriber declares its topics at connect time, and the broker filters before delivery) — not per-recipient folders and not a Linux-only file-watch tool. Durability comes from one monotonic event log with replay-from-last-seen-id, not from files persisting on disk.

## Alternatives Considered

(a) Folder-per-channel with a file-watcher — rejected: the Linux file-watch tool considered doesn't exist on macOS, and folder-per-channel doesn't scale as cleanly to dynamic/multiple listeners as topic subscription; kept only as a throwaway local test scaffold. (b) Let the always-on service itself dispatch/run the work — rejected: the template is architecturally observer-only and its own documented agent-handoff path uses headless invocation, exactly the metered-billing trap the whole engine exists to avoid; dispatch/execution must stay in-session on the interactive subscription.

## Consequences

A minimal stdlib SSE pub/sub broker was written and proven with a deterministic test: a subscriber to one topic received both of its two published events and did not receive a third event published to a different topic (the id sequence with the middle id filtered out proved server-side topic filtering). The broker never needs to call `claude`, sidestepping the billing trap by construction; the in-session dispatch loop remains the sole executor. Open follow-on: the durable replay log itself still needs to be implemented so an agent offline when an event fired can catch up on reconnect.

## Related

- Sessions: `627e86a2`

## Provenance

- **Sessions** (1): `627e86a2` · 2026-06-05
- **Files** (candidate-level): `backlog/2026-06-06-dark-factory-sentinel.md`, `experiments/watchtower-engine/spikes/synapse-probe/run-probe.sh`, `experiments/watchtower-engine/spikes/synapse-probe/server.py`
- **Commits** (candidate-level): —

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
