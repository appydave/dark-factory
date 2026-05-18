---
artifact_id: agent-skills-osmani:agent:test-engineer
repo: agent-skills-osmani
artifact_type: agent
cluster_facet: [test-authoring, code-review]
phase_fit: [4, 6]
evaluated_at: 2026-05-17
---

# Eval: test-engineer

**Intent**: QA-engineer persona that designs test suites, writes tests for existing code, and identifies coverage gaps using a structured scenario matrix.

## Scores
- **quality_score**: 4 — Clean persona definition, scenario matrix (happy path/empty/boundary/error/concurrency), coverage analysis output format, and explicit composition rules (no persona-calls-persona). Compact and usable.
- **adoption_fit_final**: strong — David's stack has `review-unit-tests` (audit) but no equivalent authoring persona; this fills the test-design role rather than the TDD process role.
- **inspiration_value**: mid
- **uniqueness_refined**: uncommon — The concurrency scenario row in the scenario matrix and the explicit "invoke via /ship for parallel fan-out" composition instruction are clean touches.
- **composability**: called-by-others — Explicitly designed to be invoked by `/test` command and `/ship` fan-out alongside `code-reviewer` and `security-auditor`.
- **description_craft_refined**: trigger — "Use for designing test suites, writing tests for existing code, or evaluating test quality."

## Mineable phrasing
> "A test that never fails is as useless as a test that always fails."

## Notes
The Prove-It Pattern is mirrored here from the TDD skill (write test first, confirm it fails, report ready for fix). Composition rules are explicit and prevent the anti-pattern of personas calling personas. The concurrency row in the scenario table (rapid repeated calls, out-of-order responses) is a gap often missed. Slight overlap with `test-driven-development` — these cluster together as authoring-process vs authoring-persona variants.
