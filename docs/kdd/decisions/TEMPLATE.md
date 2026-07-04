---
id: ADR-NNNN
title: <imperative or noun phrase>
status: proposed | accepted | deprecated | superseded
supersedes: ADR-XXXX        # omit unless this decision reverses an earlier one
superseded_by: ADR-YYYY     # omit until status becomes `superseded` — filled on the OLD file
scope: internal | cross-app-guidance | delegated
applies_to: []               # only when scope: cross-app-guidance — list of app slugs
date_decided: YYYY-MM-DD
deciders: [David Cruwys]
confidence: reconstructed | proposed | confirmed
recurrence_count: 1
provenance:               # nested is fine — parsers must speak YAML (ADR-0044, 2026-07-04)
  sessions: []
  files: []
  commits: []
tags: []
---

# ADR-NNNN: Title

**Status:** {Proposed | Accepted | Deprecated | Superseded by ADR-YYYY}

## Context

What forces are at play. Stated factually — the problem/situation, not the solution.

## Decision

What was decided. Active voice, full sentences ("We will...").

## Alternatives Considered

Each rejected option, with why. Make these first-class — not a narrative aside.

## Consequences

All outcomes, positive and negative. What this commits us to, what it forecloses.

## Applies To

*(only when `scope: cross-app-guidance`)* Which apps this binds, and how it's enforced or expected to be
picked up (a shared skill, a schema, a ticket template, etc.).

## Related

Links to sibling/superseding/superseded ADRs, patterns, or specs.

## Provenance

Human-readable mirror of the frontmatter `provenance` block — sessions, files, commits.

## Revision Log

Append-only. One line per event, oldest first.

- `YYYY-MM-DD` — reaffirmed / corroborated / challenged — note, citing the session/ticket that triggered it.
