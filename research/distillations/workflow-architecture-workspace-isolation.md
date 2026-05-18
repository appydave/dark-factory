---
distillation_id: workflow-architecture-workspace-isolation
stage: workflow-architecture
intent: "Isolate feature work in a git worktree before executing a plan — detect existing isolation, prefer native harness tools, fall back to manual git, never fight the harness"
created: 2026-05-17
status: draft
source_artifacts:
  - superpowers:skill:using-git-worktrees
  - everything-claude-code:skill:git-workflow
  - gsd:command:gsd:new-workspace
  - gsd:command:gsd:remove-workspace
  - gstack:skill:freeze
  - gstack:skill:unfreeze
winner_mechanism: superpowers:skill:using-git-worktrees
---

# Unified Skill: workspace-isolation

**Purpose**: Set up an isolated workspace (git worktree or native harness equivalent) before starting feature work — detect existing isolation first, prefer native tools, fall back to git worktrees, and document cleanup. Prerequisite pattern for any parallel or context-sensitive implementation.

**For Agents**: Use when David says "isolate this work", "set up a worktree", "create an isolated workspace", "don't touch main while I work on this", or before executing a Large/XL implementation plan. Also use when `plan-executor` or `agent-team-composer` requests workspace isolation before starting.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Workspace isolation is a prerequisite, not a separate task. Before executing any multi-step plan on a feature branch, confirm the current workspace is isolated from main. If not, create isolation via the harness-native tool (e.g., `EnterWorktree` command) before the first file edit. The core principle: **detect before create, prefer native, fall back to git, never fight the harness.**

This is a design-time concern: the decision to isolate (and the mechanism) is part of the workflow architecture, not an afterthought during execution.

## Winner's Mechanism

`superpowers:skill:using-git-worktrees` wins for the **submodule guard** — the non-obvious check that `GIT_DIR != GIT_COMMON` is also true inside git submodules (not just linked worktrees). Without this guard, a skill running inside a submodule would incorrectly conclude "already isolated" and skip worktree creation. This is a real footgun that the skill explicitly handles.

The three-step priority order is the clearest articulation of the isolation decision tree in the corpus:
1. Detect existing isolation (git dir check + submodule guard)
2. Try native harness tool (EnterWorktree, /worktree command, --worktree flag)
3. Fall back to `git worktree add`

The consent gate ("would you like me to set up an isolated worktree?") before creating one prevents unilateral filesystem changes in projects where worktrees may conflict with existing CI configuration.

`gsd:new-workspace` contributes the **worktree-vs-clone decision**: for some projects, an isolated clone (rather than a linked worktree) is the right isolation strategy (e.g., when the project's tooling breaks with worktree-style `.git` files). GSD exposes both options. Superpowers only covers worktrees.

`gstack:freeze` / `gstack:unfreeze` contribute a lighter-weight **directory-scope lock** pattern: when full worktree isolation is overkill, restrict edits to a specific directory for the session. Useful for focused refactors within a monorepo without spinning up a new worktree.

## Non-overlapping ideas folded in

- From `gsd:new-workspace`: **Clone-as-isolation fallback** — `complexity: medium | optional: true | prerequisite: "project tooling breaks with linked worktrees"`. When `git worktree add` causes build/CI failures (common with certain npm setups or monorepo tools), a clone is the safer isolation strategy. GSD's `--clone` strategy covers this.
- From `gsd:remove-workspace`: **Cleanup contract** — `complexity: low | optional: false | prerequisite: none"`. Worktrees and clones leave state behind. The isolation skill must document the cleanup procedure (prune worktree, delete branch, remove clone) at creation time, not when the user asks "how do I clean this up?".
- From `gstack:freeze` + `gstack:unfreeze`: **Directory-scope lock as lightweight isolation** — `complexity: low | optional: true | prerequisite: "only one directory needs protection, not the whole branch"`. For focused refactors, freeze the target directory (blocks Edit/Write outside it) rather than creating a worktree. Lower overhead for small scoped changes.
- From `superpowers:using-git-worktrees`: **Detached HEAD handling** — `complexity: low | optional: false | prerequisite: "CI or external process may create detached HEAD worktrees"`. If the worktree is in detached HEAD state, branch creation is deferred to finish time. This edge case is undocumented in most worktree guides but comes up in CI-generated worktrees.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| superpowers:using-git-worktrees | Submodule guard, 3-step priority order, consent gate, detached HEAD handling | Superpowers-specific finishing-branch sub-skill directive |
| gsd:new-workspace | Clone-as-isolation fallback, worktree vs clone decision | GSD workspace format (.planning/ directory) |
| gsd:remove-workspace | Cleanup contract | GSD-specific cleanup steps |
| gstack:freeze + unfreeze | Directory-scope lock pattern | gstack-specific session model |
| everything-claude-code:git-workflow | Branch strategy, commit conventions | Full git workflow (separate concern) |

## Draft SKILL.md frontmatter

```yaml
name: workspace-isolation
description: >
  Set up an isolated workspace before feature work — detect existing isolation first,
  prefer native harness tools (EnterWorktree), fall back to git worktrees or clone.
  Includes submodule guard, consent gate, cleanup contract, and freeze alternative.
  Use when: "isolate this work", "set up a worktree", "create isolated workspace",
  "don't touch main", before executing a Large/XL plan, or when plan-executor
  or agent-team-composer requests workspace isolation.
argument-hint: "[feature-branch-name | --clone | --freeze-only]"
allowed-tools: "Bash(git:*), Bash(echo:*), Read"
```

## Open questions for David

1. **EnterWorktree availability**: The `EnterWorktree` deferred tool is listed in the system-reminder but its schema isn't loaded. When should `workspace-isolation` prefer `EnterWorktree` vs manual `git worktree add`? Is `EnterWorktree` available in all David's sessions, or only in specific worktree-aware projects?

2. **gstack:freeze as a skill**: `freeze` and `unfreeze` are gstack-specific. Should David have a standalone `workspace-freeze` skill in appydave-plugins for directory-scope locks without the full gstack install? It's a 5-line implementation — worth having as a standalone utility.

3. **Cleanup automation**: Should `workspace-isolation` produce a cleanup script at creation time (a one-liner that prunes the worktree and deletes the branch), or just document the cleanup steps in plain text? A script is safer (no memory required); documentation is more flexible.
