---
artifact_id: agent-skills-osmani:skill:context-engineering
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [session-setup, context-management, rules-files]
phase_fit: [0]
evaluated_at: 2026-05-17
---

# Eval: context-engineering

**Intent**: Guides deliberate curation of what context an agent sees, structured from persistent rules files down to per-iteration error output, with anti-patterns and confusion management protocols.

## Scores

- **quality_score**: 5. Exemplary: 5-level hierarchy diagram, trust levels for loaded files, anti-rationalization table, inline planning pattern, concrete examples at each level — genuinely complete.
- **adoption_fit_final**: `strong`. Fully stack-agnostic; encodes the process of feeding an agent, not any particular tool or language.
- **inspiration_value**: `high`. The "context hierarchy" pyramid and the trust-level classification (trusted / verify / untrusted) are instantly applicable mental models.
- **uniqueness_refined**: `rare`. The combination of hierarchy + trust levels + confusion management in a single skill is not duplicated elsewhere in the corpus.
- **composability**: `called-by-others`. spec-driven-development explicitly references this skill as the loader for spec sections during implementation.
- **description_craft_refined**: `trigger`. Description names five concrete trigger scenarios, written as agent routing cues.

## Mineable phrasing

> "Context window size ≠ attention budget. Focused context outperforms large context."

## Notes

The trust-level classification (trusted / verify / untrusted) for loaded files is a rare security-aware addition that most context skills omit. The "Confusion Management" section — with structured CONFUSION: / Options: / → format — is directly mineable as a reusable pattern for any skill that encounters conflicting signals. Strongest single artifact in the stage-0 batch.
