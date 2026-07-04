---
id: ADR-0037
title: "Leave CLAUDE.local.md without the system-context auto-import for Dark Factory"
status: proposed
scope: internal
date_decided: 2026-06-15
deciders: [David Cruwys]
confidence: reconstructed
recurrence_count: 1
provenance:
  sessions: ["f4f3d282"]
  files: ["CLAUDE.local.md", "context/CONTEXT.md"]
  commits: []
tags: []
---

> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0037: Leave CLAUDE.local.md without the system-context auto-import for Dark Factory

**Status:** Proposed (reconstructed)

## Context

The system-context skill's Bootstrap step normally ensures CLAUDE.local.md contains an `@<ctx>/CONTEXT.md` import so CONTEXT.md is auto-loaded into every session. Dark Factory's convention treats CONTEXT.md and context.globs.json as generated output, external to the working system, not files to be relied on or auto-loaded.

## Decision

During the 2026-06-16 refresh of context/CONTEXT.md, deliberately did not add the `@context/CONTEXT.md` import line to CLAUDE.local.md, leaving it untouched — deviating from the skill's default bootstrap behavior of always wiring up auto-load.

## Alternatives Considered

Follow the skill's default Bootstrap step and add the `@context/CONTEXT.md` import to CLAUDE.local.md so the document is auto-loaded into every session start.

## Consequences

CONTEXT.md stays a read-on-demand snapshot rather than an always-loaded working doc, keeping per-session context lean; the trade-off is that agents must remember to consult it explicitly since it is never surfaced automatically.

## Related

- Sessions: `f4f3d282`

## Provenance

- **Sessions** (1): `f4f3d282` · 2026-06-15
- **Files** (candidate-level): `CLAUDE.local.md`, `context/CONTEXT.md`
- **Commits** (candidate-level): —

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
