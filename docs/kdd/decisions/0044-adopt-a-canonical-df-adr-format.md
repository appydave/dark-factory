---
id: ADR-0044
title: Adopt a canonical DF-ADR format, modeled on Cortex's native template
status: proposed
scope: internal
date_decided: 2026-07-04
deciders: [David Cruwys]
confidence: proposed
recurrence_count: 1
provenance:
  sessions: []
  files: [docs/kdd/ADR-FORMAT-SPEC.md, docs/kdd/decisions/TEMPLATE.md]
  commits: []
tags: [kdd, adr, lisa, process]
---

# ADR-0044: Adopt a canonical DF-ADR format, modeled on Cortex's native template

**Status:** Proposed

## Context

The reconstruction that produced ADR-0001 through ADR-0043 used Lisa's raw output shape (Context/
Decision/Alternatives Considered/Consequences/Related/Provenance), which differs from Dark Factory's
own pre-existing `docs/watchtower/DECISIONS.md` (terse D1-D4 style). Neither format was designed with
Dark Factory's actual role in mind: it documents its own architecture, but it also issues guidance
that other microapps are expected to follow, while each app can still run its own SDLC — and none of
the existing formats distinguish those two things. Separately, decisions today are write-once; there
is no mechanism for a decision to accumulate corroborating (or contradicting) evidence as Lisa mines
later sessions, unlike learnings, which already earn promotion to patterns at recurrence ≥3.

Two sibling projects, Cortex and KBDE, already ran their own Lisa reconstructions. Cortex had a
mature native ADR format going in (48 decisions, `Status/Date/Deciders/Context/Decision/Rationale/
Consequences/See also`, explicit "never delete a superseded ADR" rule) and normalized its Lisa batch
INTO that format at ratification rather than leaving it raw. KBDE had no prior format and kept
Lisa's raw shape, same as Dark Factory today. Full grounding, including the industry survey (Nygard,
MADR, Y-statements, supersession conventions, cross-repo ADR practice, and machine-mined decision
records like Lore), is in the companion doc: `docs/kdd/ADR-FORMAT-SPEC.md`.

## Decision

Adopt one canonical format for all future Dark Factory decisions — hand-authored or Lisa-extracted —
built on Cortex's proven body shape plus three new fields Dark Factory specifically needs:

- **`scope`**: `internal` | `cross-app-guidance` | `delegated` — distinguishes DF's own architecture
  calls from guidance DF expects other microapps to follow from a decision that belongs to another
  app and DF is only cross-referencing, respecting that apps own their own SDLC.
- **`confidence` + `recurrence_count` + a `Revision Log` section**: the self-learning mechanism —
  reuses the same recurrence logic Lisa already applies to learnings/patterns, so a decision's
  confidence rises as later sessions corroborate it, and a contradicting session (Lisa's existing
  `conflict` verdict) now also triggers a supersession review instead of just sitting in a triage
  report.

Full template: `docs/kdd/decisions/TEMPLATE.md`.

## Alternatives Considered

- **Keep Lisa's raw reconstructed shape as canonical.** Rejected — it has no `scope` concept, so it
  can't distinguish DF's own decisions from cross-app guidance, and no supersession/confidence
  fields, so it can't support the self-learning goal.
- **Adopt Cortex's format unchanged.** Rejected as insufficient, not wrong — Cortex is a single-repo
  project with no cross-app guidance role and no self-learning requirement. Its body shape is sound
  and kept; its scope is too narrow for what Dark Factory needs.
- **Design a heavier, fully RACI-matrix format** (decision-makers/consulted/informed, per MADR/
  organizational-ADR practice). Rejected as over-ceremony for a factory run by one person — the
  3-value `scope` field captures the actual distinction Dark Factory needs without a matrix nobody
  will fill in.
- **Offer a Y-statement short form for trivial internal decisions.** Deferred, not rejected — worth
  revisiting if the full template turns out to suppress recording small internal calls in practice.

## Consequences

- The 41 proposed decisions from ADR-0001–0043 (post-merge) need reformatting into this template at
  ratification — not extra work, the same ratification pass already flagged, now with a concrete
  target shape.
- ADR-0020/ADR-0021 (a genuine same-day reversal — build a doc-organiser skill, then don't) should be
  linked via `supersedes`/`superseded_by` during ratification, as the first live use of the new field.
- `docs/watchtower/DECISIONS.md` stays untouched — historical, binding, predates this format.
- Cortex and KBDE are not retroactively changed — this decision is scoped to Dark Factory only.
- Follow-on, not part of this decision: extending Lisa's `extractor-schema.md` and
  `reconcile-classifier-schema.md` so future reconstructions emit `scope`/`confidence`/
  `recurrence_count` natively, instead of a manual reformat pass each time.

## Related

- `docs/kdd/ADR-FORMAT-SPEC.md` — full research grounding and rationale
- `docs/kdd/decisions/TEMPLATE.md` — the template itself
- `docs/watchtower/DECISIONS.md` — D1-D4, untouched, referenced not retrofitted
- SupportSignal `docs/kdd/meta/decision-adr-template.md` — the strongest precedent by production mileage (3 months, 631 commits); source of the `supersedes`/`superseded_by`/frontmatter-as-real-fields pattern
- Cortex `docs/kdd/decisions/0001-adr-format-and-location.md` — the precedent for folding a Lisa reconstruction batch into a native template at ratification, and the "never delete a superseded ADR" rule
- ADR-0020, ADR-0021 — the first candidate for the new supersession fields

## Provenance

Authored directly in this session (not Lisa-extracted) — reasoning grounded in a cross-project file
survey (Dark Factory, Cortex, KBDE, SupportSignal, poem-os, storyline-app) and a cited industry
research pass. See `docs/kdd/ADR-FORMAT-SPEC.md` for sources.

## Revision Log

- 2026-07-04 — proposed — initial write-up, pending David's ratification.
