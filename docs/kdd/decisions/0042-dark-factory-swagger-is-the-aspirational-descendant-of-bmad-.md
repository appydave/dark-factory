---
id: ADR-0042
title: "Dark-Factory Swagger is the aspirational descendant of BMAD Swagger, not an unrelated namesake"
status: proposed
scope: internal
date_decided: 2026-06-24
deciders: [David Cruwys]
confidence: reconstructed
recurrence_count: 1
provenance:
  sessions: ["f85d2bbd"]
  files: ["research/bmad-pattern-mining/bmad-machinery-pattern.md"]
  commits: ["bb82517"]
tags: []
---

> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0042: Dark-Factory Swagger is the aspirational descendant of BMAD Swagger, not an unrelated namesake

**Status:** Proposed (reconstructed)

## Context

The mined BMAD machinery spec initially framed the Dark-Factory `swagger` job-agent skill and the BMAD `bmad-story-lifecycle` orchestrator persona (also called "Swagger"/"Overwatch") as a naming collision: "Same name, different artifact — do not conflate." The repo owner corrected this, explaining that Dark-Factory's Swagger was deliberately named and built to inherit the BMAD orchestrator's proven world-model and handoff strength — the two are not unrelated.

## Decision

Frame Dark-Factory Swagger as the aspirational descendant of BMAD Swagger — same lineage, different maturity, not a name collision. Port the orchestrator persona and the proven structural discipline (story-file-as-bus, append-only gate log, no-embody orchestrator, verify-from-artifacts, fresh-agent fix loops, self-maintaining doctrine) into Dark-Factory Swagger's design. Do NOT port the rigidity: BMAD Swagger is locked to one hard-coded, battle-tested workflow shape run on autopilot (a single stigmergy with no flexibility in the stigmergy itself) — reliable but slow and poor at adapting. Dark-Factory Swagger's aspiration is the same orchestration and handoff strength applied across many flexible workflow shapes, not one ordained lifecycle.

## Alternatives Considered

Keep the original framing — treat the two Swaggers as separate, unrelated artifacts that merely happen to share a name. Rejected because it discards the deliberate design intent behind the shared name and loses the actionable design brief (what structural machinery to port vs. what rigidity to deliberately leave behind).

## Consequences

The mined spec (`research/bmad-pattern-mining/bmad-machinery-pattern.md`) was edited in two places — the opening "Naming" callout and a new "Lineage note" in §4 — to state the design brief explicitly: port the orchestrator persona + structural discipline, leave the single-shape lock behind. A durable project memory (`project_swagger_lineage.md`, referenced from `MEMORY.md`) was written so future Dark-Factory Swagger design work starts from the lineage framing rather than the name-clash framing. The doc was committed (after a rebase to resolve a rejected push) and pushed to `origin/main`.

## Related

- Sessions: `f85d2bbd`

## Provenance

- **Sessions** (1): `f85d2bbd` · 2026-06-24
- **Files** (candidate-level): `research/bmad-pattern-mining/bmad-machinery-pattern.md`
- **Commits** (candidate-level): `bb82517`

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
