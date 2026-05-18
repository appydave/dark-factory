---
artifact_id: appydave-plugins:skill:kcommit
repo: appydave-plugins
artifact_type: skill
cluster_facet: [documentation, test-authoring, workflow-architecture]
phase_fit: [2, 4, 6, 7, 9]
evaluated_at: 2026-05-17
---

# Eval: kcommit

**Intent**: Document and invoke David's `k*` shell function family — a complete stage→commit→pull→push→CI-watch pipeline for Ruby gems and AppyDave projects.

## Scores
- **quality_score**: 3 — Accurate and useful as a reference card, but this is documentation of existing shell functions rather than a generative skill. The trigger constraint ("Only trigger on k-function names") is unusually narrow and stack-specific.
- **adoption_fit_final**: mid — Works in David's Ruby/AppyDave context only. The CI-watch step errors silently on repos without GitHub Actions, which is already noted but represents a rough edge. Not portable to other stacks.
- **inspiration_value**: low — The pattern (commit + pull + push + CI watch in one function) is well-known. The only novel element is the explicit "No CI repos" edge case documentation.
- **uniqueness_refined**: commodity — Conventional commit wrapper with CI watch is a common pattern; the Ruby/kcops variant is stack-specific but not mechanically novel.
- **composability**: standalone — Documents shell functions; no agent composition hooks.
- **description_craft_refined**: trigger — Description uses explicit allowlist of k-function names as the trigger; the "Do NOT trigger on generic phrases" exclusion is a useful negative-trigger pattern.

## Mineable phrasing
> "Do NOT trigger on generic phrases like 'commit this', 'commit with message', or 'push'."

## Notes
The negative-trigger pattern in the description (explicit exclusion of common synonyms) is a reusable discovery mechanism for any skill that should only fire on specific invocations and not bleed into adjacent triggers. The `kcops` variant (rubocop-specific commit, no message needed) shows good ergonomic design for repetitive micro-tasks. Skill could be elevated by converting the shell-function docs into an executable agent that runs these commands rather than just describing them.
