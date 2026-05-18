---
distillation_id: code-implementation-worktree-isolation
stage: code-implementation
intent: "Establish isolated workspace via git worktree before any implementation, with native fallback to branch-only isolation"
created: 2026-05-17
status: draft
source_artifacts:
  - superpowers:skill:using-git-worktrees
  - compound-engineering:skill:ce-worktree
  - compound-engineering:skill:ce-work
winner_mechanism: superpowers:skill:using-git-worktrees
---

# Unified Skill: Worktree Isolation

## Intent

Before executing any non-trivial implementation, establish an isolated workspace — preferring a git worktree over a plain branch so that the working directory is physically separate and parallel work doesn't pollute the main workspace or each other.

## Winner's Mechanism

Superpowers' `using-git-worktrees` is the winner for one reason: it handles the fallback correctly. When `git worktree` is unavailable (shallow clone, certain CI environments), it falls back to a plain branch checkout with a clear message — rather than failing silently or requiring the human to diagnose. The skill is zero-dependency (no external tools, just git) and idempotent — safe to call at the start of any implementation session.

CE's `ce-worktree` is the companion/alternative: it creates a branch from the default branch in an isolated worktree and is explicitly invoked by `ce-work` during Phase 1 environment setup. Both skills do the same job; Superpowers' version has the cleaner fallback.

## Existing-skill nesting

David does not currently have a worktree-isolation skill in his stack. This is a gap-fill.

Skip this section — from-scratch build.

## Non-overlapping ideas folded in

- From `compound-engineering:skill:ce-worktree`: **Worktree lifecycle management** — after subagent work completes, unlock the worktree (`git worktree unlock`), remove it (`git worktree remove`), and delete the branch (`git branch -d`). Without this, worktrees accumulate as orphans. — `complexity: low | optional: false | prerequisite: "worktree was created for subagent work"`. Cleanup is part of the contract, not a follow-up task.

- From `compound-engineering:skill:ce-work`: **Meaningful branch name check** — if the current branch name is auto-generated or opaque (e.g., `worktree-jolly-beaming-raven`), suggest renaming before starting work. A meaningful name (`feat/email-validation`) aids future review and bisect. — `complexity: low | optional: true | prerequisite: none`. Low-friction improvement to commit history legibility.

- From `compound-engineering:skill:ce-work`: **Default-branch protection** — never commit to main/master without explicit user confirmation ("yes, commit to [branch]"). If on the default branch, always propose creating a feature branch or worktree first. — `complexity: low | optional: false | prerequisite: none`. The most common source of unintended main-branch contamination.

- From `superpowers:skill:using-git-worktrees`: **Isolation-before-implementation principle** — invoke this skill at the start of any feature work or plan execution. Make "is there an isolated workspace?" a precondition check, not an afterthought. — `complexity: low | optional: false | prerequisite: "non-trivial implementation work"`. The skill's core value: prevents the failure mode where implementation starts on the wrong branch.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `superpowers:using-git-worktrees` | Worktree creation, native vs. branch fallback, idempotent precondition check | Platform-specific subagent isolation flags (Codex `spawn_agent` etc.) |
| `compound-engineering:ce-worktree` | Worktree lifecycle management (unlock → remove → delete branch) | Worktree-from-default-branch-only assumption (Superpowers' approach is more general) |
| `compound-engineering:ce-work` | Meaningful branch name check, default-branch protection | Full ce-work orchestration (belongs in feature-implement) |

## Draft SKILL.md frontmatter

```yaml
name: worktree-isolation
description: "Establish an isolated workspace via git worktree before any implementation work. Use when starting feature work, executing a plan, or before any non-trivial code change. Triggers on: 'start a worktree', 'create isolated workspace', or automatically at the start of feature-implement or subagent-driven-development."
argument-hint: "[branch name, or leave blank to derive from current task/plan]"
allowed-tools: "Bash(git worktree:*), Bash(git branch:*), Bash(git checkout:*)"
```

## Open questions for David

1. **Standalone vs. sub-skill**: Should `worktree-isolation` be a standalone skill users invoke directly, or purely a dependency that `feature-implement` and `subagent-driven-development` call? If standalone, the description needs user-facing trigger phrases. If dependency-only, it can be leaner.

2. **Claude worktrees collision**: Claude Code creates its own worktrees under `.claude/worktrees/` for subagent isolation. The skill should detect and avoid naming collisions with those paths. Is `.claude/worktrees/` already in the gitignore for David's projects?

3. **Worktree vs. branch for BMAD sprints**: BMAD's `bmad-dev-story` doesn't explicitly require a worktree — it just says "implement on current branch." Should `worktree-isolation` be a recommended precondition for `bmad-dev-story` too, or leave that to BMAD's own workflow?
