---
artifact_id: agent-skills-osmani:skill:api-and-interface-design
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [api-design, interface-contracts, spec-requirements]
phase_fit: [1]
evaluated_at: 2026-05-17
---

# Eval: api-and-interface-design

**Intent**: Guides the design of stable, hard-to-misuse interfaces (REST, GraphQL, module boundaries, component props) using Hyrum's Law, contract-first, boundary validation, and additive extension principles.

## Scores

- **quality_score**: 5. The Hyrum's Law treatment is exceptional — not just cited but unpacked into design implications. Input/Output separation, branded types, consistent error semantics, anti-rationalization table. A genuine reference document.
- **adoption_fit_final**: `strong`. Entirely stack-agnostic at the principle level; TypeScript examples are illustrative, not prescriptive.
- **inspiration_value**: `high`. Hyrum's Law framing ("every observable behavior becomes a de facto contract") is the standout. The One-Version Rule (avoid forcing version choices) is equally underrepresented in most API skills.
- **uniqueness_refined**: `rare`. The combination of Hyrum's Law + One-Version Rule + trust boundary for third-party API responses is not found elsewhere in the corpus.
- **composability**: `standalone`. Can be invoked independently or as part of a spec-driven pipeline.
- **description_craft_refined**: `trigger`. Description names five specific design scenarios as triggers.

## Mineable phrasing

> "With a sufficient number of users of an API, all observable behaviors of your system will be depended on by somebody, regardless of what you promise in the contract."

## Notes

The "third-party API responses are untrusted data" call-out (validate shape and content before using in any logic, rendering, or decision-making) is a security-aware addition most API design skills miss. The framing of testing limitations ("Even with perfect contract tests, Hyrum's Law means 'safe' changes can break real users who depend on undocumented behavior") is a honest, uncommon admission that elevates this above a boilerplate API guide.
