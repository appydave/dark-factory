---
id: ADR-0013
title: "Adapt HyperFrames as the shared engine for both rendered video and interactive talk-through decks, rather than adopting a presentation-native tool"
status: proposed
scope: internal
date_decided: 2026-06-11
deciders: [David Cruwys]
confidence: reconstructed
recurrence_count: 1
provenance:
  sessions: ["307792ae"]
  files: ["experiments/hyperframes-presentation-poc/FINDINGS.md", "experiments/hyperframes-presentation-poc/composition.html", "experiments/hyperframes-presentation-poc/presenter.html"]
  commits: []
tags: []
---

> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0013: Adapt HyperFrames as the shared engine for both rendered video and interactive talk-through decks, rather than adopting a presentation-native tool

**Status:** Proposed (reconstructed)

## Context

David asked whether the cortex 'how a brain works' deck's underlying HTML/animation engine (HyperFrames, an OpenAI-curated plugin in KBDE-KyberAgent-Enterprise that treats HTML as the source of truth for video) could also work as an interactive, keypress-driven talk-through presentation, since he was less interested in an actual rendered video and more in an interactive deck he could narrate live.

## Decision

Spiked a single HyperFrames composition (the 06-brain-anatomy hero slide) plus a ~120-line standalone presenter runtime that drives the composition's already-paused GSAP timeline by keypress instead of a clock (advance on arrow/space, hold on each scene's hero frame, back on left-arrow). Confirmed feasible and recommended adapting HyperFrames as the shared engine — one composition source can render to both an aitldr MP4 (`hyperframes render`) and this keypress deck — rather than adopting a presentation-native tool.

## Alternatives Considered

reveal.js (or a similar presentation-native tool) — gives presentation chrome for free (speaker notes, PDF export, remote control) but a reveal.js deck can never become the rendered video output; using it would require hand-writing the same GSAP motion layer separately, forking the render pipeline into two parallel systems.

## Consequences

The generated composition.html is NOT self-contained — opening it directly renders blank because the timeline needs a runtime driving window.__timelines; a talk-through deck is always two files (composition + presenter), which must be shipped together. Recommendation for follow-up: port reveal.js's good affordances (speaker notes, jump-to-slide) onto the HyperFrames engine, and home the presenter as a 'deck' output mode inside the Mochaccino/aitldr render line rather than as a standalone tool. This decision was not yet built into production — it is the PoC's recommendation, pending a go to build the full four-slide deck.

## Related

- Sessions: `307792ae`

## Provenance

- **Sessions** (1): `307792ae` · 2026-06-11
- **Files** (candidate-level): `experiments/hyperframes-presentation-poc/FINDINGS.md`, `experiments/hyperframes-presentation-poc/composition.html`, `experiments/hyperframes-presentation-poc/presenter.html`
- **Commits** (candidate-level): —

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
