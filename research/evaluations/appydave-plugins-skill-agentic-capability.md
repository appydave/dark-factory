---
artifact_id: appydave-plugins:skill:agentic-capability
repo: appydave-plugins
artifact_type: skill
cluster_facet: [documentation, workflow-architecture]
phase_fit: [2, 6, 7, 9]
evaluated_at: 2026-05-17
---

# Eval: agentic-capability

**Intent**: Design advisor for choosing the right Claude Code extension mechanism (skill, command, subagent, hook, or agent team) before building anything — guides through three critical tests to resolve the mechanism decision.

## Scores
- **quality_score**: 4 — Clean decision framework with three sequential binary tests (conversation history needed? → investigative/batch? → Claude-discovers vs user-invokes?), a family structure decision table (separate skills / single skill with routing / orchestrator + subagents), and a shared boilerplate guidance rule (duplicate into each skill's references/, never a shared namespace folder). The "3 critical tests" flow is a strong cognitive scaffold.
- **adoption_fit_final**: strong — This is David's own skill. The question is whether the mechanism is robust and whether gaps exist. The three-test decision flow is sound. The family-structure option C (orchestrator skill spawning parallel subagents) maps directly onto what `/ship` implements — confirming the design pattern but showing the execution is still in Osmani territory.
- **inspiration_value**: mid — The three-test decision flow is already in David's stack. The most novel element is the explicit "do NOT recommend a namespace-level shared references/ folder — it is non-standard and fragile" anti-pattern rule, which is a concrete and unusual design constraint.
- **uniqueness_refined**: uncommon — The three-test decision tree is a clean distillation that doesn't appear in this form elsewhere in the corpus. The shared-boilerplate anti-pattern rule (no namespace-level references/) is an unusual and specific guardrail.
- **composability**: standalone — Design advisor only. Explicitly states it is "the step before skill-creator" — it terminates by recommending the next tool to invoke.
- **description_craft_refined**: trigger — Description has 10 explicit trigger phrases including "skill vs command", "what mechanism should I use", "agentic capability". Very comprehensive trigger coverage. Could be reduced without losing discovery.

## Mineable phrasing
> "Do NOT recommend a namespace-level shared references/ folder — it is non-standard and fragile."

## Notes
This is David's existing skill at a design-decision stage that correctly precedes both `skill-creator` and `agent-orchestrator`. The three-test framework is the primary mechanism. At distillation, the interesting comparison is between this skill's Option C (orchestrator + subagents) and Osmani's `/ship` command — they describe the same pattern at different levels of abstraction (design-time advisory vs. runtime executable). A unified distillation might keep this skill for the decision framework and fold the runtime execution pattern from `/ship` into a separate orchestration skill.
