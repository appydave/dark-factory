---
distillation_id: system-comprehension-pre-action-scan
stage: system-comprehension
intent: "Scan, surface, and restore working context before starting any agent action — session-boot orientation and cross-session memory"
created: 2026-05-17
status: draft
source_artifacts:
  - poem:agent:alex
  - gstack:skill:context-save
  - gstack:skill:context-restore
  - compound-engineering:skill:ce-sessions
  - compound-engineering:agent:ce-session-historian
  - appydave-plugins:skill:mocha
winner_mechanism: poem:agent:alex + gstack:skill:context-save/restore (split winner — two distinct jobs)
---

# Unified Skill: Pre-Action Scan (session-boot comprehension)

**Purpose**: Before any agent takes action on a codebase, it must orient itself — either by loading prior session context (what was decided, what was tried, where we left off) or by scanning the project to understand what it's working on. This cluster unifies two related jobs: session-state persistence (save/restore) and scan-then-act boot-time orientation.

## Intent

Surface all relevant working context before acting: prior session decisions and state (cross-session memory), plus a live scan of what the project currently is. The canonical phrase from POEM Alex: **"Scan-then-greet, not greet-then-discover."**

## Winner's Mechanism

Split winner — two mechanisms for two related but distinct jobs:

**Job 1 — Cross-session state (save/restore)**: `gstack:skill:context-save` + `gstack:skill:context-restore`
- Captures git state, decisions made, remaining work, active branch — everything needed to pick up without losing a beat
- Symmetric pair: save fires on "save progress / save state / checkpoint"; restore fires on "resume / restore context / where was I"
- Works across Conductor workspace handoffs (multi-worktree aware)
- Zero infra dependency beyond git

**Job 2 — Boot-time scan before action**: `poem:agent:alex` (activation Step 4)
- Alex scans existing prompts and schemas to build an I/O inventory BEFORE greeting the user
- Canonical phrase: "scan-then-greet, not greet-then-discover" — system comprehension embedded in agent activation, not surfaced as a separate command
- Prevents the failure mode of an agent confidently discussing a system it hasn't looked at yet

**CE's `ce-sessions`** is the third leg: searches session history across Claude Code, Codex, and Cursor to synthesize prior investigations. This complements gstack's save/restore (which is git-state focused) with natural-language session history search.

No single artifact covers all three. The unified skill is a composition.

## Existing-skill nesting

`appydave-plugins:skill:mocha` partially covers the cross-session state job (mochaccino workspace + session context). Check overlap before building new save/restore.

- **Existing mechanism (`mocha`)**: workspace-level context capture within a mochaccino session. Scoped to design/planning context.
- **New mechanism grain (context-save/restore)**: per-git-branch state snapshot. Captures decisions, remaining work, branch, git SHA. Developer-context focused, not design-focused.
- **Nesting rule**: `mocha` fires for design/planning session state; `context-save/restore` fires for developer working state (code, decisions, branch). They compose at different layers — neither replaces the other.

## Non-overlapping ideas folded in

- From `poem:agent:alex`: **scan-embedded-in-activation** — `complexity: medium | optional: false | prerequisite: agent has an activation step`. The key insight: pre-action scan should NOT be a separate command the user types. It should fire automatically when an agent activates. Building a scan step into agent activation (rather than a separate `/scan` command) makes it zero-friction. This is a design principle, not a new skill.

- From `compound-engineering:skill:ce-sessions` + `ce-session-historian`: **natural-language session history search** — `complexity: medium | optional: true | prerequisite: Claude Code session history exists`. CE searches prior sessions by topic ("what did we try for the auth bug") and synthesizes findings as prose. Complement to git-state restore: one covers what the code looked like; the other covers what was tried and decided. Together they give full context resumption.

- From `gstack:skill:context-save/restore`: **branch-aware state snapshots** — `complexity: low | optional: false | prerequisite: git repo`. Save stores git state (branch, SHA, staged files) alongside decisions and remaining work. Restore loads most recent snapshot across all branches by default, with branch-scoped fallback. The branch-aware behavior is the key design decision — most session memory tools ignore branch, losing context on checkout.

- From `compound-engineering:agent:ce-session-historian`: **investigative narrative synthesis** — `complexity: medium | optional: true | prerequisite: ce-sessions produces session skeleton`. The historian converts raw session history into prose about investigation journeys, failed attempts, and key decisions. Not a search tool — a synthesis tool. The distinction matters for routing: search first (`ce-sessions`), then synthesize (`ce-session-historian`).

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `poem:agent:alex` | Scan-then-greet principle; scan embedded in activation | POEM YAML workflow format; multi-harness compile requirement |
| `gstack:skill:context-save` | Branch-aware state snapshot; git SHA + decisions + remaining work | gstack compile pipeline (needs-compile infra) |
| `gstack:skill:context-restore` | Branch-scoped restore; "pick up where you left off" UX | gstack compile pipeline |
| `compound-engineering:skill:ce-sessions` | Cross-harness session search (Claude Code + Codex + Cursor) | Context7 MCP dependency |
| `compound-engineering:agent:ce-session-historian` | Investigative narrative synthesis from session skeletons | Dependency on ce-sessions orchestrator dispatch |
| `appydave-plugins:skill:mocha` | Existing workspace-level context mechanism | Not superseded — different grain |

## Draft SKILL.md frontmatter

Two skills (or one with modes):

```yaml
# Option A: Two separate skills
name: context-save
description: >
  Save current working context — git state, decisions made, remaining work — so any future
  session can resume without losing a beat. Use when the user says "save progress", "save state",
  "checkpoint", "save context", "save where we are", "I need to stop", or "before I switch tasks".
  Pair with context-restore.
allowed-tools: "Bash(git:*), Write, Read"
```

```yaml
name: context-restore
description: >
  Restore working context saved by context-save. Loads the most recent saved state so you can
  pick up where you left off. Use when user says "resume", "restore context", "where was I",
  "pick up where we left off", "what were we doing", "load last checkpoint".
  Pair with context-save.
allowed-tools: "Bash(git:*), Read"
```

## Open questions for David

1. **Overlap with mocha**: Does `context-save/restore` need to be a new skill, or should it be a new mode within `mocha`? The grain is different (git-state vs design-state) but the UX trigger phrases overlap ("save progress" could mean either).

2. **Session history search**: CE's `ce-sessions` searches across Claude Code, Codex, and Cursor session history. David is Claude Code-only. Does a Claude-Code-only `session-search` skill make sense, or is the session transcript already available via other means (AngELEye, OMI)?

3. **Scan-then-greet as a hook**: The "scan before acting" principle from POEM Alex could be implemented as a `UserPromptSubmit` hook rather than a per-skill step. Should this principle become a hook in `settings.json` rather than a skill?
