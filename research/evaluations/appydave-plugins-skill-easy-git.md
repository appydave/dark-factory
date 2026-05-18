---
artifact_id: appydave-plugins:skill:easy-git
repo: appydave-plugins
artifact_type: skill
cluster_facet: [documentation, knowledge-capture, orchestration]
phase_fit: [6, 7, 8, 9]
evaluated_at: 2026-05-17
---

# Eval: easy-git

**Intent**: Safe guided Git workflow for non-experts on multi-machine setups — pull, push, sync, conflict resolution in plain English.

## Scores
- **quality_score**: 3 — Well-executed for its scope. The onboarding step (detect and configure pull.rebase + rebase.autoStash once per repo) is the right default. The conflict resolution flow (show per-file, ask keep-mine/keep-remote/manual for each, then continue) is clear and safe. The rules section (never force-push without explicit confirmation, never reset --hard without warning) is correct. Loses points because the phase_fit [6,7,8,9] is overly broad — this is primarily a workflow-boundary skill (stages 8-9) and the KDD classification into knowledge-capture feels like misclassification.
- **adoption_fit_final**: mid — David has his own kcommit skill and easy-git. The multi-machine context is accurate for his setup (5 Macs). However, David is not a Git novice — this skill is calibrated for a different user profile than his.
- **inspiration_value**: low — The mechanisms are standard Git workflow. No novel framing.
- **uniqueness_refined**: commodity — Safe Git wrappers are common in every repo that has non-expert users.
- **composability**: standalone — Self-contained. References AppySentinel for future integration but that's aspirational.
- **description_craft_refined**: trigger — Trigger phrases are natural language and accurate.

## Mineable phrasing
> `none`

## Notes
The "Sentinel Integration" future plan (automatic brain sync detection and scheduled push/pull) in references/ is the most interesting forward-looking idea. The actual skill is commodity Git workflow. The "ask rather than guess" principle is correct for a safety-first skill. Worth keeping for Jan/Mary who ARE non-expert Git users in David's team context — but for David himself, kcommit and direct git usage is the preferred path.
