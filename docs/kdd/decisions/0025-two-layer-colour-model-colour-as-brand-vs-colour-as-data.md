---
id: ADR-0025
title: "Two-layer colour model — Colour as Brand vs Colour as Data"
status: proposed
scope: internal
date_decided: 2026-06-09
deciders: [David Cruwys]
confidence: reconstructed
recurrence_count: 1
provenance:
  sessions: ["a69afeb2"]
  files: ["docs/david-design-patterns.md"]
  commits: []
tags: []
---

> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0025: Two-layer colour model — Colour as Brand vs Colour as Data

**Status:** Proposed (reconstructed)

## Context

David's own rated exemplars gave inconsistent-looking verdicts on cool (green/blue/purple) vs warm (brown/cream/yellow) colour use across Mochaccino designs. An earlier round's 'kill orange-on-brown' correction had been over-applied to a cortex-deck re-render, stripping warm colour out almost entirely and producing a result David called brand-cold — even though the intended fix was to remove a bad colour *value* (muddy amber `#c8841a` with poor contrast), not the warm *role* itself.

## Decision

Codify two independent colour palettes with distinct jobs into docs/david-design-patterns.md: (1) Colour as Brand — warm, brown/cream/gold/yellow `#ffde59`, load-bearing, used for identity + content emphasis; (2) Colour as Data — cool, green/blue/purple/teal, a sparing accent used only for genuine structural/categorical encoding (a stage, node, or legend-key), never for content. Restore yellow `#ffde59` as the bright warm anchor; restrict amber `#c8841a` to numbered-sequence use only (01/02/03); cool colour must never become the dominant/load-bearing treatment.

## Alternatives Considered

Continuing the prior 'kill orange-on-brown → remove all warm/orange accents' correction was the option already in effect (it's what shipped on the cortex deck) but was rejected: it over-corrects into a brand-cold, generic-SaaS look with no warm anchor. Verified as the wrong read against David's own love-tier exemplars (lexi-profile, layout-29), which are warm-dominant with cool used only sparingly, and against his own AITLDR semantic-colors.md, which already stated the same two-layer split a year earlier for a different brand.

## Consequences

docs/david-design-patterns.md's orange-on-brown rule was rewritten to separate role (correct) from value (wrong). The design-lint rubric being built in the same session is grounded directly in this model (F1 cool-on-content, F2 missing-warm-anchor, F3 amber-orange-on-brown). Durable memory (colour-as-brand-vs-data.md) was created to persist the model across a cold restart.

## Related

- Sessions: `a69afeb2`

## Provenance

- **Sessions** (1): `a69afeb2` · 2026-06-09
- **Files** (candidate-level): `docs/david-design-patterns.md`
- **Commits** (candidate-level): —

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
