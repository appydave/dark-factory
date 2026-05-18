---
artifact_id: agent-skills-osmani:skill:shipping-and-launch
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [delivery-readiness]
phase_fit: [6]
evaluated_at: 2026-05-17
---

# Eval: shipping-and-launch

**Intent**: Pre-launch readiness skill that ensures every production deployment is reversible, observable, and incremental — including feature flag strategy, staged rollout with numeric thresholds, rollback plan template, and post-launch verification protocol.

## Scores
- **quality_score**: 5 — Production-grade completeness: pre-launch checklist across six axes (code quality, security, performance, accessibility, infrastructure, documentation), feature flag lifecycle with explicit expiration/owner rules, staged rollout with quantified advance/hold/rollback thresholds (error rate, P95 latency, business metrics), rollback plan template with RTO targets, post-launch 1-hour protocol. Anti-rationalization table. This is one of the most operationally complete artifacts in the batch.
- **adoption_fit_final**: strong — David's `delivery-review` skill exists but focuses on review process rather than deployment readiness gates. The quantified rollout decision thresholds (advance green/hold yellow/rollback red) and the feature flag lifecycle rules are genuine gaps in the current stack. Direct integration candidate.
- **inspiration_value**: high — The rollout decision threshold table (numeric triggers for advance vs. hold vs. rollback) is immediately adoptable as a concrete mechanism. The "rolling back is responsible engineering — shipping a broken feature is the failure" framing is mineable for the anti-rationalization table.
- **uniqueness_refined**: uncommon — The combination of feature flag lifecycle rules with explicit expiration date enforcement, plus the quantified rollout thresholds, is more operationally specific than typical deployment checklists. Most deployment guides stop at "monitor after deploy"; this gives you the exact numbers.
- **composability**: called-by-others — Invoked by `/ship` command as the parent skill for the fan-out orchestration.
- **description_craft_refined**: trigger — "Use when preparing to deploy to production. Use when you need a pre-launch checklist, when setting up monitoring, when planning a staged rollout, or when you need a rollback strategy." Four distinct trigger scenarios well enumerated.

## Mineable phrasing
> "Rolling back is admitting failure" → "Rolling back is responsible engineering. Shipping a broken feature is the failure."

## Notes
The quantified rollout thresholds table is the highest-value unique mechanism here — it converts "monitor after deploy" from a vague instruction into a decision tree with numeric gates. The feature flag lifecycle (deploy with flag OFF → team → 5% canary → gradual → clean up within 2 weeks) paired with the "every feature flag has an owner and an expiration date" rule addresses one of the most common agentic deployment failure modes. David's `delivery-review` skill should be compared directly to this at distillation time to avoid mechanism overlap.
