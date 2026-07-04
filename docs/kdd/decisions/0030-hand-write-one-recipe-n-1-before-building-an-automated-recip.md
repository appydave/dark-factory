---
id: ADR-0030
title: "Hand-write one recipe (N=1) before building an automated recipe-builder"
status: proposed
scope: internal
date_decided: 2026-06-10
deciders: [David Cruwys]
confidence: reconstructed
recurrence_count: 1
provenance:
  sessions: ["d9b55fdb"]
  files: []
  commits: []
tags: []
---

> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0030: Hand-write one recipe (N=1) before building an automated recipe-builder

**Status:** Proposed (reconstructed)

## Context

David proposed building a general 'recipe builder' — an interview-driven system, built on the AppySentinel foundation, that would generate an app like AppyRadar Sentinel from a spec, with a skill developed recursively along the way. Before scoping the build, the session needed to decide how big a first step to take.

## Decision

Park the grand automated recipe-builder (interview automation, generative spec engine, skill recursion, conformance harness) and instead hand-write a single recipe by reverse-engineering the already-built AppyRadar Sentinel (214 tests) into one bounded artifact — the spec, the interview questions, and the verbatim tricky bits (pulse-serialization chain, snapshot merge) — applying the north-star doctrine of proving one mechanism per session rather than theorising.

## Alternatives Considered

(1) Build the full automated recipe-builder machine first (interview automation + generative spec + skill recursion + conformance harness) — rejected as 'theorising ... before you've written a single app-archetype recipe even once,' which violates the standing N=1/no-theorise doctrine. (2) Justify the builder as leverage to stop hand-building future Sentinels — ranked weakest, since only three Sentinels have been built over months and the existing `configure-sentinel` skill already covers most of that need.

## Consequences

Defers commitment to interview automation, the generative-spec/skill-recursion machinery, and open questions like whether the interview should be a POEM workflow or where the recipe should live; produces a real second full app-archetype exemplar (alongside the AppyStack, AppySentinel, and Symphony recipe formats) usable as a demo/teaching asset; and generates the decision data needed to judge whether the bigger automated builder is worth the investment, instead of guessing.

## Related

- Sessions: `d9b55fdb`

## Provenance

- **Sessions** (1): `d9b55fdb` · 2026-06-10
- **Files** (candidate-level): —
- **Commits** (candidate-level): —

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
