---
id: ADR-0008
title: "Adopt the adversarial A-vs-B delta (run both, critique hard, recommend canonical) as a first-class Dark Factory build technique"
status: proposed
scope: internal
date_decided: 2026-06-08
deciders: [David Cruwys]
confidence: reconstructed
recurrence_count: 1
provenance:
  sessions: ["2df0e613"]
  files: ["backlog/specs/df7-osmani-vs-appydave-delta.md", "backlog/specs/df8-comparison-registry-spec.md"]
  commits: []
tags: []
---

> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0008: Adopt the adversarial A-vs-B delta (run both, critique hard, recommend canonical) as a first-class Dark Factory build technique

**Status:** Proposed (reconstructed)

## Context

Osmani's agent-skills spec-driven-development skill was run unprompted against the same DF-7 requirement already drafted by appydave:spec-writer, producing a comparison doc with a per-dimension winner and an overall recommendation, instead of silently picking one method's output.

## Decision

Adopt this as a standing technique: at any A-vs-B fork (spec tools, designs, skills, implementations), default to producing a delta document (what each side ADDED / SHARPENED / DROPPED, per-dimension winners, a canonical recommendation) rather than a silent choice — and recognize it as the repeated motion the future ~1,100-artifact distillation campaign will need to run at scale.

## Alternatives Considered

Silently pick one tool/approach without a documented comparison (the prior default) — rejected because it hides tradeoffs and doesn't scale to a corpus where near-duplicate artifacts must be adjudicated repeatedly.

## Consequences

Captured as a durable memory. A follow-up evaluation determined pairwise comparison is a genuinely different data primitive from the corpus's existing single-artifact-absolute structures (census.jsonl, evaluations/*, distillations/*), proven because a tier-5/adopt-rated artifact still LOST its head-to-head — a fact no per-artifact score could surface. This spawned a new spec for a comparisons registry + a compare capability, spec-written and parked for the future distillation campaign.

## Related

- Sessions: `2df0e613`

## Provenance

- **Sessions** (1): `2df0e613` · 2026-06-08
- **Files** (candidate-level): `backlog/specs/df7-osmani-vs-appydave-delta.md`, `backlog/specs/df8-comparison-registry-spec.md`
- **Commits** (candidate-level): —

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
