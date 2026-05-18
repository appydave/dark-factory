---
artifact_id: appydave-plugins:skill:mochaccino-v1
repo: appydave-plugins
artifact_type: skill
cluster_facet: [ui-design, mockup-generation, deprecated]
phase_fit: [0]
evaluated_at: 2026-05-17
---

# Eval: mochaccino-v1

**Intent**: Original single-persona mockup skill — activates as a design collaborator, silently gathers project context, generates self-contained HTML mockups without data/view separation.

## Scores

- **quality_score**: 3. Solid foundational design (silent context discovery, "improve don't copy" principle, never-blocked rule). But deprecated status and inline-data approach are explicit limitations. Preserved intentionally as reference.
- **adoption_fit_final**: `mid`. The silent context-discovery protocol (scan .impeccable.md, CSS tokens, type defs, data samples before asking) is reusable pattern; the overall skill is superseded by Mocha.
- **inspiration_value**: `mid`. "Never blocked. Missing schema or data → proceed with reasonable assumptions." is a strong operational principle that should survive the deprecation.
- **uniqueness_refined**: `duplicate`. Superseded by mocha + mochaccino quartet; exists for reference parity.
- **composability**: `standalone`. Single-persona, no upstream or downstream chain.
- **description_craft_refined**: `trigger`. Description explains when to use v1 vs. new system and explicit "old mochaccino" trigger — good deprecation-aware routing.

## Mineable phrasing

> "Real data. Use actual names/values from the project. If not available, invent realistic data — not 'Lorem ipsum'."

## Notes

The silent design-context-discovery protocol (work top to bottom through five sources before asking a single question) is a pattern worth extracting for any design or UI skill. The "never blocked" principle and "improve don't copy" principle are direct ancestors of the v2 quartet's design philosophy. Worth preserving as a source artifact for any unified design skill.
