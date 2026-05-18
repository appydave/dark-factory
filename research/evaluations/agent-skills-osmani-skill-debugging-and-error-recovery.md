---
artifact_id: agent-skills-osmani:skill:debugging-and-error-recovery
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [code-implementation, verification-validation]
phase_fit: [3, 4, 5, 6]
evaluated_at: 2026-05-17
---

# Eval: debugging-and-error-recovery

**Intent**: Enforce a systematic stop-reproduce-localize-reduce-fix-guard-verify triage process when any unexpected failure occurs, instead of guessing at fixes.

## Scores
- **quality_score**: 5 — The most comprehensive debugging skill in the corpus. Stop-the-line rule, decision trees for non-reproducible bugs (timing/environment/state-dependent/truly-random), bisection for regressions, anti-rationalization table, and a security note (error messages as untrusted data) together form a complete reference. The "treating error output as untrusted data" section is rare and valuable.
- **adoption_fit_final**: strong — Language-agnostic debugging discipline; examples use TypeScript/Node but patterns apply universally. No stack lock. Directly composable with incremental-implementation and test-driven-development.
- **inspiration_value**: high — The security-aware error handling section (don't execute commands found in error messages without user confirmation) is an under-documented concern in agent coding skills. The non-reproducible bug decision tree with four branches is the most structured treatment of intermittent failures in the corpus.
- **uniqueness_refined**: uncommon — The "error output as untrusted data" angle is not found in any other debugging skill evaluated. The structured non-reproducible-bug tree (timing/environment/state/truly-random) goes further than other skills.
- **composability**: called-by-others — Referenced directly by the `build` command ("If any step fails, follow the agent-skills:debugging-and-error-recovery skill").
- **description_craft_refined**: trigger — Description gives three distinct trigger conditions ("tests fail, builds break, behavior doesn't match expectations") and explicitly names the value ("systematic approach... rather than guessing").

## Mineable phrasing
> "Don't push past a failing test or broken build to work on the next feature. Errors compound."

## Notes
The "stop-the-line" framing (borrowed from lean manufacturing) is the right mental model for AI-accelerated development where errors compound rapidly. The anti-rationalization table ("I know what the bug is" → "You might be right 70% of the time — the other 30% costs hours") is high-craft: it pre-emptively defeats the rationalizations that cause agents to skip the reproduce step. The minimal reproduction principle (Step 3: Reduce) is underemphasised in most debugging guides but is the single most effective debugging technique — this skill surfaces it explicitly.
