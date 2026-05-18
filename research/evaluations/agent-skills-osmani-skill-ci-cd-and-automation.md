---
artifact_id: agent-skills-osmani:skill:ci-cd-and-automation
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [delivery-readiness, verification-validation]
phase_fit: [5, 6]
evaluated_at: 2026-05-17
---

# Eval: ci-cd-and-automation

**Intent**: Sets up and modifies CI/CD pipelines to automate quality gates, test runners, and deployment strategies with shift-left principles.

## Scores
- **quality_score**: 4 — Full GitHub Actions YAML examples (basic CI, with Postgres integration tests, E2E), CI optimization checklist, feature flag lifecycle guidance, rollback workflow, and the "CI failure → agent feedback loop" pattern. Comprehensive for greenfield setup.
- **adoption_fit_final**: strong — David uses GitHub Actions and Vercel; the CI→agent-feedback loop pattern is directly applicable to autonomous development sessions.
- **inspiration_value**: mid
- **uniqueness_refined**: uncommon — The CI→agent feedback loop ("copy CI failure output, feed to agent, agent fixes, pushes, CI runs again") is explicitly articulated here and rarely formalized elsewhere.
- **composability**: standalone — Complete CI reference; can be invoked independently for new project setup or pipeline debugging.
- **description_craft_refined**: trigger — Three "Use when" trigger lines.

## Mineable phrasing
> "Faster is Safer: Smaller batches and more frequent releases reduce risk, not increase it."

## Notes
The "Build Cop" role definition (person responsible for keeping CI green regardless of who broke it) is a team process idea that translates to agent orchestration: designate a monitoring loop that catches green/red state. The CI optimization decision tree (cache → parallelize → path filters → matrix → optimize suite → larger runners) is a useful ordered checklist. Security reminder about test DB credentials in CI is well-placed.
