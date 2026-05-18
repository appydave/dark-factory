---
artifact_id: agent-skills-osmani:skill:test-driven-development
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [test-authoring]
phase_fit: [4]
evaluated_at: 2026-05-17
---

# Eval: test-driven-development

**Intent**: Writes failing tests before implementation, treating tests as proof — not optional verification — for every logic change or bug fix.

## Scores
- **quality_score**: 5 — RED/GREEN/REFACTOR cycle with visuals, the Prove-It Pattern for bugs, the Beyonce Rule, DAMP vs DRY in tests, mocking preference hierarchy (real > fake > stub > mock), and test size classification (Small/Medium/Large resource model). Comprehensive and production-calibrated.
- **adoption_fit_final**: strong — Directly applicable to every project in David's stack; the `review-unit-tests` skill already exists but this is the upstream mechanism for authoring, not reviewing.
- **inspiration_value**: high
- **uniqueness_refined**: uncommon — The Beyonce Rule, the explicit subagent-for-test-writing pattern, and the "don't re-run an unchanged test suite" anti-rationalization are notable refinements over generic TDD.
- **composability**: calls-others — References `browser-testing-with-devtools` for browser layer; spawns subagents for complex bug Prove-It tests.
- **description_craft_refined**: trigger — Three distinct trigger conditions including the Prove-It edge case.

## Mineable phrasing
> "Tests ARE the specification. They document what the code should do, not what it does."

## Notes
The subagent pattern for bug Prove-It tests (spawn a separate agent to write the reproduction test without fix knowledge) is a distinctive mechanism worth folding into any unified TDD skill. The integration with `browser-testing-with-devtools` is a clean composability example. David's `review-unit-tests` skill handles audit of existing tests; this handles authoring — two distinct grains that compose.
