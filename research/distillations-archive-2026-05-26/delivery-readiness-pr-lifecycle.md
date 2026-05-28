---
distillation_id: delivery-readiness-pr-lifecycle
stage: delivery-readiness
intent: "Manage the full PR lifecycle — create with structured body, resolve reviewer feedback in parallel, and land cleanly"
created: 2026-05-17
status: draft
source_artifacts:
  - compound-engineering:skill:ce-commit-push-pr
  - compound-engineering:skill:ce-resolve-pr-feedback
  - compound-engineering:agent:ce-pr-comment-resolver
  - gsd:command:pr-branch
  - gsd:command:ship
  - gstack:skill:ship
  - gstack:skill:land-and-deploy
  - gstack:skill:landing-report
  - spec-kit:command:taskstoissues
  - ruflo:skill:agent-github-pr-manager
  - appydave-plugins:skill:pr-lifecycle
winner_mechanism: compound-engineering:skill:ce-resolve-pr-feedback
---

# Unified Skill: PR Lifecycle

**Purpose**: For Agents: Use when David says "create PR", "resolve PR feedback", "respond to review comments", "resolve review threads", "pr lifecycle", or "land this PR".

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

## Intent

Manage the full PR lifecycle: create a PR with a value-first adaptive body, evaluate incoming review threads for validity, resolve them in parallel (fix code, reply with reasoning, close thread), and land the PR cleanly with a post-merge verification pass.

## Winner's Mechanism

`compound-engineering:ce-resolve-pr-feedback` wins because it solves the hardest problem in this cluster: PR review feedback is often ignored, half-addressed, or addressed with performative agreement. CE's mechanism — evaluate validity, spawn parallel resolver per thread, fix, reply with reasoning, close thread via GitHub GraphQL — is production-tested at EveryInc and directly addresses the failure mode where PRs sit with unresolved threads.

This skill is the gap in David's stack. He can create PRs (via `kcommit` push), but has no systematic mechanism for addressing review feedback.

## Existing-skill nesting

`appydave-plugins:skill:pr-lifecycle` already exists. Assess what it covers before building from scratch — it may only need the `ce-resolve-pr-feedback` mechanism folded in.

- **Existing mechanism**: `pr-lifecycle` (currently unknown depth — check SKILL.md before building). Likely covers PR creation and basic lifecycle.
- **New mechanism's grain (resolve feedback)**: per-thread — spawns one resolver agent per review thread, evaluates validity independently, then implements fix if valid.
- **Existing mechanism's grain**: per-PR — manages PR creation and status.
- **Nesting rule**: `pr-lifecycle` orchestrates the PR creation and status tracking. `resolve-pr-feedback` is invoked inside `pr-lifecycle` when review threads need addressing. The resolver agents are sub-agents of the lifecycle skill's resolution phase.

## Non-overlapping ideas folded in

- From `compound-engineering:ce-resolve-pr-feedback`: Validity evaluation before fixing — each reviewer thread is assessed: "is this feedback valid?" before fixing — `complexity: low | optional: false | prerequisite: none`. Prevents implementing feedback that contradicts the spec or was already addressed elsewhere.
- From `compound-engineering:ce-pr-comment-resolver`: Cluster mode — groups related threads and resolves them together in one agent call — `complexity: medium | optional: true | prerequisite: PR has multiple related threads`. Reduces agent spawning overhead for dense review feedback.
- From `compound-engineering:ce-commit-push-pr`: Adaptive PR body depth — body scales with change size: single-commit fix → one-liner body; multi-file feature → structured sections with motivation, testing, rollback — `complexity: low | optional: false | prerequisite: none`. Produces PR bodies reviewers actually read.
- From `gsd:pr-branch`: Planning artifact filtering — cherry-picks only code commits onto the PR branch, excluding `.planning/` changes — `complexity: medium | optional: true | prerequisite: project uses GSD .planning/ structure`. Keeps PR diffs clean for reviewers who don't want to see AI planning artifacts.
- From `gstack:landing-report`: Queue dashboard before creating PR — shows which VERSION slots are claimed and which slot the next PR would claim — `complexity: medium | optional: true | prerequisite: project uses gstack VERSION convention`. Prevents slot collisions in parallel PR workflows.
- From `spec-kit:taskstoissues`: Task-to-issue promotion — converts tasks.md entries into dependency-ordered GitHub Issues before creating the PR — `complexity: low | optional: true | prerequisite: project uses Spec Kit tasks.md`. Links the PR to properly-formed issues.
- From `gstack:land-and-deploy`: Post-merge canary check — after landing the PR, run canary verification against the deployed URL — `complexity: medium | optional: true | prerequisite: project has a deployed URL and post-deploy canary configured`. Closes the loop from merge → verified deploy.
- From `superpowers:finishing-a-development-branch` (via cross-cluster): Structured option presentation (merge / PR / keep / discard) with test verification before presenting options — `complexity: low | optional: false | prerequisite: none`. Prevents the "create PR on failing tests" failure mode.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `compound-engineering:ce-resolve-pr-feedback` | Validity evaluation, parallel resolver agents, reply + close thread, GraphQL thread resolution | CE's internal task routing conventions |
| `compound-engineering:ce-pr-comment-resolver` | Cluster mode for related threads, structured summary with reply text | CE's color coding and model=inherit conventions |
| `compound-engineering:ce-commit-push-pr` | Adaptive PR body depth scaling | Description-only mode (specific to CE review UI) |
| `gsd:pr-branch` | Planning artifact filtering pattern | GSD's `.planning/` path structure |
| `gstack:ship` | Version slot assignment, CHANGELOG update | gstack's multi-harness-compile requirement |
| `gstack:land-and-deploy` | Post-merge canary verification trigger | gstack's browse-daemon infrastructure |
| `gstack:landing-report` | Queue dashboard pattern | gstack's VERSION file convention |
| `spec-kit:taskstoissues` | Task-to-issue dependency ordering | Spec Kit's prerequisite scripts |
| `ruflo:agent-github-pr-manager` | Stub name only — mechanism too shallow to assess | Everything — duplicate stub with no mechanism |

## Draft SKILL.md frontmatter

```yaml
name: pr-lifecycle
description: "Manage the full PR lifecycle — create with value-first adaptive body, evaluate review threads for validity, resolve feedback in parallel (fix + reply + close), and land cleanly with post-merge verification. Use when: 'create PR', 'open PR', 'resolve PR feedback', 'respond to reviewer', 'resolve review threads', 'land this PR', 'pr lifecycle', 'address review comments'."
argument-hint: "[pr-url | pr-number | blank for current branch]"
allowed-tools: "Bash(gh api:*), Bash(gh pr:*), Bash(git:*), Read, Edit, Write, Task"
```

## Open questions for David

1. **Existing pr-lifecycle SKILL.md**: Read `/Users/davidcruwys/dev/ad/appydave-plugins/appydave/skills/pr-lifecycle/SKILL.md` before building — it may already cover creation and only need the resolve mechanism added.

2. **GraphQL thread resolution**: CE's `ce-pr-comment-resolver` resolves threads via GitHub GraphQL API (`gh api graphql`). Does David's stack have `gh` configured with the right auth scopes for mutations? This is a prerequisite for the resolver to actually close threads, not just reply.

3. **Post-merge canary scope**: The gstack `land-and-deploy` canary pattern requires a deployed URL to verify against. Should `pr-lifecycle` optionally accept a `--canary-url` flag to enable post-merge verification, or is this always manual?
