---
distillation_id: documentation-pr-description-gen
stage: delivery-readiness
intent: "Generate a value-first PR description (title + body) that scales in depth with the change, with optional evidence capture"
created: 2026-05-17
status: draft
source_artifacts:
  - compound-engineering:skill:ce-commit-push-pr
  - appydave-plugins:skill:pr-lifecycle
  - gsd:command:pr-branch
  - appydave-plugins:skill:kcommit
winner_mechanism: compound-engineering:skill:ce-commit-push-pr
---

# Unified Skill: pr-description-gen

**Purpose**: Generate a PR title and body from the branch diff — adaptive depth, value-first framing, optional evidence capture. Handles description-only, description-update, and full commit+push+PR flows.

**For Agents**: Use when user says "create a PR", "write a PR description", "ship this", "open a pull request", "rewrite the PR body". Do not use for resolving PR feedback (that's `pr-lifecycle`).

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Generate a PR title and body from the branch diff, with adaptive depth and value-first framing, plus optional evidence capture for observable changes.

## Winner's Mechanism

`compound-engineering:skill:ce-commit-push-pr` is the most complete PR authoring mechanism in the corpus. Key qualities:

- **Mode dispatch** (description-only / description-update / full-workflow) — clean conditional routing, no multi-purpose bloat
- **Adaptive depth** — body scales with the change size; small fixups get short prose, large features get sections
- **Evidence decision tree** — explicit 3-way fork: user asked, agent judges observable vs non-observable, otherwise ask
- **`--body-file` correctness** — explicitly prohibits stdin/heredoc-to-stdin patterns that silently produce empty bodies
- **Cross-harness blocking question** — uses `AskUserQuestion`, `request_user_input`, `ask_user` per harness, with fallback
- **`fix:` vs `feat:` discipline** — adds behavior you couldn't previously accomplish is `feat:`; remedies broken/missing behavior is `fix:`
- `pr-description-writing.md` reference file is the actual composition engine — the skill is a clean dispatch wrapper

David's `pr-lifecycle` skill is already in the stack and handles resolution (what comes after). The gap is the **authoring step** before the PR is created.

## Existing-skill nesting

David has `pr-lifecycle` (resolve review feedback) but no `pr-description` authoring skill. These are adjacent, not overlapping:

- **`pr-description-gen` grain**: per-PR, fires before PR is opened or to refresh an existing PR body
- **`pr-lifecycle` grain**: per-PR, fires after review threads accumulate
- **Nesting rule**: `pr-description-gen` produces the initial description; `pr-lifecycle` resolves downstream feedback on that PR. Neither replaces the other; the natural sequence is `pr-description-gen` → reviewer reads → `pr-lifecycle` resolves.

Also adjacent: `kcommit` (Ruby-gem-specific commit conventions). `kcommit` handles commit message formatting for gems; `pr-description-gen` handles the PR body for any repo. They share the conventional-commits baseline but are orthogonal concerns.

## Non-overlapping ideas folded in

- From `gsd:command:pr-branch`: cherry-pick approach that strips `.planning/` artifacts from the PR branch before opening — `complexity: medium | optional: true | prerequisite: "GSD planning artifacts exist in repo"`. Prevents implementation artifacts (specs, wave files) from polluting the PR diff.

- From `appydave-plugins:skill:kcommit`: explicit `git log` scan to match repo's existing commit-message convention before picking a type/scope — `complexity: low | optional: false | prerequisite: none`. Already present as a principle in the winner; worth calling out explicitly in Step 2.

- From `appydave-plugins:skill:pr-lifecycle` (relationship section): explicit "do not mix authoring and resolution" boundary — `complexity: low | optional: false | prerequisite: none`. The winner already does this via mode dispatch; the relationship note in `pr-lifecycle` provides good boilerplate language for the references.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `ce-commit-push-pr` | Mode dispatch, adaptive depth, evidence decision tree, `--body-file` correctness, cross-harness blocking question, `fix:`/`feat:` discipline, `pr-description-writing.md` composition reference | `ce-demo-reel` dependency for evidence (David doesn't have `ce-demo-reel`) |
| `pr-lifecycle` | Relationship framing (this skill authors; pr-lifecycle resolves) | Entire resolution mechanism (correct tool, different skill) |
| `gsd:command:pr-branch` | Planning-artifact-strip idea for clean PR branches | GSD-specific cherry-pick machinery |
| `kcommit` | Convention-scan principle (inspect recent commits before choosing message type) | Ruby gem scope/format specifics |

## Draft SKILL.md frontmatter

```yaml
name: pr-description-gen
description: "Generate a PR title and body from the branch diff — adaptive depth, value-first framing. Also handles description-only and description-update flows. Use when: 'create a PR', 'write a PR description', 'ship this', 'open a pull request', 'rewrite the PR body', 'what should the PR say'."
argument-hint: "[PR number or URL for description-only/update mode; blank for full workflow]"
allowed-tools: Bash(git *), Bash(gh *), Read, Write
```

## Open questions for David

1. **`ce-demo-reel` dependency**: The winner's evidence capture delegates to `ce-demo-reel` (screen recording). David doesn't have this. Options: (a) skip the demo section entirely for now, (b) accept a user-provided URL/image, (c) build a lightweight screenshot-only path. Which?

2. **`pr-description-writing.md`**: The winner depends on a `references/pr-description-writing.md` reference file that contains the actual composition steps (Pre-A through G). Should David port this reference file verbatim, adapt it, or write from scratch in David's voice?

3. **Naming**: `pr-description-gen` vs `pr-description` vs `commit-push-pr`. The winner uses the latter; David's naming pattern uses hyphenated verb-nouns. Suggested: `pr-description` (matches the purpose, consistent with `doc-review`).
