---
distillation_id: delivery-readiness-commit-quality-gate
stage: delivery-readiness
intent: "Structure every commit as a quality gate — right type, right message, hooks run, CI watched — before moving on"
created: 2026-05-17
status: draft
source_artifacts:
  - appydave-plugins:skill:kcommit
  - compound-engineering:skill:ce-commit
  - compound-engineering:skill:ce-commit-push-pr
  - spec-kit:command:speckit.git.commit
  - agent-skills-osmani:skill:git-workflow-and-versioning
  - compound-engineering:skill:ce-clean-gone-branches
  - compound-engineering:skill:ce-worktree
winner_mechanism: appydave-plugins:skill:kcommit
---

# Unified Skill: Commit Quality Gate

**Purpose**: For Agents: Use when David says "kcommit", "kfeat", "kfix", "kchore", "kdocs", "ktest", "krefactor", "kenhance", "kcops", or any k-function variant. Do NOT trigger on generic "commit this".

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

## Intent

Enforce a full commit pipeline — stage → typed commit → pull → push → CI watch → tag check — so every commit in David's Ruby/AppyDave projects is traceable, validated, and CI-green before the session moves on.

## Winner's Mechanism

`kcommit` wins for David's stack because it already exists, already works, and already solves the right problem: Ruby/AppyDave projects with pre-commit hooks (gitleaks, plugin validation), conventional commit types mapped to named functions, and CI watching built into the pipeline. The mechanism is a zsh function family, not a Claude skill — which is correct for this use case (runs in terminal, not through Claude inference).

The correct question for this cluster is not "build a new commit skill" but "what should `kcommit` fold in from the other mechanisms?"

## Existing-skill nesting

- **Existing mechanism**: `kcommit` is a zsh function pipeline: stage → typed commit → pull → push → CI watch → tag. Designed for Ruby gems and AppyDave projects. Already handles all the standard cases.
- **New mechanism's grain (CE's value-first description)**: per-commit — CE's `ce-commit` generates commit messages by summarizing what the change does for the user, not just what files changed. Currently `kcommit` takes a message from the user; CE's mechanism could suggest the message.
- **Existing mechanism's grain**: per-project-type — `kcommit` assumes Ruby/conventional-commit conventions. CE's `ce-commit` auto-detects repo conventions via `git log --oneline -10`.
- **Nesting rule**: `kcommit` remains the terminal-level pipeline. A new companion Claude skill (`appydave:easy-git` or a `suggest-commit-message` skill) could optionally generate the value-first message before the user calls `kcommit`. They compose: Claude suggests message → user calls `kfeat '<suggestion>'`.

## Non-overlapping ideas folded in

- From `compound-engineering:ce-commit`: Convention auto-detection — reads `git log --oneline -10` to infer the project's commit style before composing message — `complexity: low | optional: true | prerequisite: none`. Useful for client work (SupportSignal) where conventions differ from AppyDave defaults.
- From `compound-engineering:ce-commit`: Value-first message framing — describes what changes for the user, not which files moved — `complexity: low | optional: false | prerequisite: none`. "feat: add NDIS incident filter by date range" > "feat: update FilterPanel.tsx and useIncidents.ts".
- From `compound-engineering:ce-commit-push-pr`: Adaptive PR description depth — scales description length with change size (small fix → one-liner; large feature → structured sections) — `complexity: medium | optional: true | prerequisite: change is being pushed as a PR`. Currently `kcommit` pushes without PR body; CE auto-generates a body.
- From `agent-skills-osmani:git-workflow-and-versioning`: Atomic commit discipline — one logical change per commit; if `git diff` spans multiple concerns, surface that before committing — `complexity: low | optional: true | prerequisite: none`. Prevents "big bang" commits that break bisect.
- From `compound-engineering:ce-clean-gone-branches`: Post-merge cleanup trigger — after a PR is merged, auto-suggest running branch cleanup — `complexity: low | optional: true | prerequisite: PR has been merged`. Pairs naturally with commit-push-PR flow.
- From `compound-engineering:ce-worktree`: Worktree isolation for parallel work — when starting a new feature that should not disturb current checkout, create a worktree first — `complexity: medium | optional: true | prerequisite: parallel work on multiple features`. Not a commit concern but pairs with branch hygiene.
- From `spec-kit:speckit.git.commit`: Auto-commit-after-phase pattern — trigger a commit automatically at the end of any Spec Kit command that produces artifacts — `complexity: low | optional: true | prerequisite: project uses Spec Kit`. Useful for AppyDave projects that use spec-driven flows.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `appydave-plugins:kcommit` | Full pipeline, k-function naming, CI watch | Nothing — this is the winner |
| `compound-engineering:ce-commit` | Convention detection, value-first message framing | CE's internal file structure assumptions |
| `compound-engineering:ce-commit-push-pr` | Adaptive PR description depth scaling | `ce-commit-push-pr` description-only flow (specific to CE UI) |
| `agent-skills-osmani:git-workflow-and-versioning` | Atomic commit discipline, anti-rationalization framing | Trunk-based branching strategy (separate concern) |
| `compound-engineering:ce-clean-gone-branches` | Post-merge cleanup suggestion pattern | CE's worktree cleanup specifics |
| `compound-engineering:ce-worktree` | Worktree isolation pattern | CE's env file copying, mise/direnv trust steps |
| `spec-kit:speckit.git.commit` | Auto-commit-after-phase pattern | Spec Kit's PowerShell scripts |

## Draft SKILL.md frontmatter

```yaml
name: kcommit
description: >
  Git commit workflow for Ruby gems and AppyDave projects. Only trigger when user explicitly names
  a k-function: kcommit, kfeat, kfix, kchore, kdocs, ktest, krefactor, kenhance, kcops.
  Do NOT trigger on generic phrases like "commit this", "commit with message", or "push".
allowed-tools: "Bash(git:*), Bash(gh:*)"
```

**Note**: `kcommit` is a zsh function family, not a Claude-native skill. The `allowed-tools` above apply to the companion Claude skill that could suggest messages. The zsh functions themselves live in `aliases-kcommit.zsh`.

## Open questions for David

1. **Companion suggest-message skill**: Should there be a lightweight Claude skill that takes `git diff --staged` and suggests a value-first conventional commit message (CE's mechanism), which David can then paste into `kfeat '<suggestion>'`? Or is the current "David writes the message" workflow fast enough?

2. **PR body auto-generation**: `ce-commit-push-pr` generates adaptive PR bodies. Should `kcommit` (or a new `kpr`) trigger CE's body-generation mechanism when pushing a PR branch? Currently there's no `kpr` equivalent.

3. **Atomic commit signal**: Should the commit pipeline warn when `git diff --staged` shows changes across more than 3 unrelated files (signal of non-atomic commit)? CE's `git-workflow-and-versioning` surfaces this pre-commit.
