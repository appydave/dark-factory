---
artifact_id: agent-skills-osmani:skill:idea-refine
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [idea-development, divergent-thinking, spec-requirements]
phase_fit: [1]
evaluated_at: 2026-05-17
---

# Eval: idea-refine

**Intent**: Structured 3-phase ideation (diverge → converge → ship) that takes a raw idea through 7 lenses, stress-tests assumptions, and produces a one-pager with a mandatory "Not Doing" list.

## Scores

- **quality_score**: 5. Outstanding. The 7 variation lenses are specific and non-obvious (inversion, constraint removal, audience shift, simplification, 10x). Anti-yes-machine enforcement. Mandatory "Not Doing" section. References external frameworks via file, not inline.
- **adoption_fit_final**: `strong`. Fully process-encoded; no stack coupling; applies to any ideation context.
- **inspiration_value**: `high`. "The 'Not Doing' list is arguably the most valuable part" is a rare design philosophy statement that reframes ideation as constraint articulation.
- **uniqueness_refined**: `uncommon`. 7 divergence lenses as a codified list is not typical; most ideation skills just say "brainstorm."
- **composability**: `calls-others`. Explicitly positions itself as upstream of interview-me (if needed) or spec-driven-development (for concrete ideas); reads external frameworks.md and refinement-criteria.md.
- **description_craft_refined**: `trigger`. Three clean trigger phrases; concise.

## Mineable phrasing

> "The 'Not Doing' list is arguably the most valuable part. Focus is about saying no to good ideas. Make the trade-offs explicit."

## Notes

The anti-yes-machine stance ("Be honest, not supportive. If an idea is weak, say so with kindness.") is enforced through multiple structural mechanisms — not just stated as a principle. The instruction to ground variations in actual codebase patterns (use Glob/Grep/Read when inside a project) prevents the common failure of context-free ideation. Strong pairing candidate with interview-me for a unified requirements-discovery flow.
