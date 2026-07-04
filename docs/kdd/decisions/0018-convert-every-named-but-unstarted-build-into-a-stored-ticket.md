---
id: ADR-0018
title: "Convert every named-but-unstarted build into a stored, ticketable spec instead of starting it"
status: proposed
scope: internal
date_decided: 2026-06-05
deciders: [David Cruwys]
confidence: reconstructed
recurrence_count: 1
provenance:
  sessions: ["627e86a2"]
  files: [".claude/skills/millwright/SKILL.md", "backlog/specs/README.md", "backlog/specs/tickets.json"]
  commits: []
tags: []
---

> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0018: Convert every named-but-unstarted build into a stored, ticketable spec instead of starting it

**Status:** Proposed (reconstructed)

## Context

Several substantial capabilities (loop instrumentation/observability, a self-learning enforcement mechanism, tool-usage telemetry) had each been proposed and agreed as worth building across a session, but none had actually been dispatched — a recurring pattern of naming work without starting it. Separately, an A/B comparison on the same class of task (turning a messy requirement into a structured spec) showed a dedicated requirements-writing tool producing a materially more complete document — sections like goals/non-goals, a prototype-reuse map, and an explicit open-decisions section — than an ad-hoc freeform prompt covering the same ground.

## Decision

The fix for 'named but never started' is not to start building — it is to convert each named build into a written, stored spec via the dedicated requirements tool, and hold it in one registry until a later, separate decision to build it. The registry is modeled on an existing work-management spec's entity shape (a ticket key, project, integer priority where lower means higher, and a state lifecycle: spec-todo, spec-written, ticketed, building, done) rather than inventing a new shape.

## Alternatives Considered

Keep discussing/naming builds without a tracked artifact — rejected, this was the observed failure mode being fixed. Start building the highest-priority item immediately — rejected: writing and storing the requirement is explicitly the bar for done at this stage; building is a deliberately separate, later decision so it isn't started prematurely or without a spec.

## Consequences

A spec registry (a machine-readable ticket file plus a README) was created holding six tickets, each tagged with state and priority; two of the three previously-unspecced items were dispatched as spec-only jobs through the dedicated requirements tool and landed as stored specs (330 lines and 226 lines respectively) rather than as code changes. The gatekeeper skill that routes work was updated to pick the spec tool and the build technique as two separate choices, since neither had previously been treated as a deliberate routing decision.

## Related

- Sessions: `627e86a2`

## Provenance

- **Sessions** (1): `627e86a2` · 2026-06-05
- **Files** (candidate-level): `.claude/skills/millwright/SKILL.md`, `backlog/specs/README.md`, `backlog/specs/tickets.json`
- **Commits** (candidate-level): —

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
