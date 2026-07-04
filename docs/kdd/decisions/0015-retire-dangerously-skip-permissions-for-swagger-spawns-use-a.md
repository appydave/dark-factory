---
id: ADR-0015
title: "Retire --dangerously-skip-permissions for Swagger spawns; use a one-time human permission grant instead"
status: proposed
scope: internal
date_decided: 2026-06-05
deciders: [David Cruwys]
confidence: reconstructed
recurrence_count: 1
provenance:
  sessions: ["627e86a2"]
  files: [".claude/settings.local.json", "docs/watchtower/build-state.md", "experiments/watchtower-engine/skills/marshall/SKILL.md"]
  commits: ["2d09641"]
tags: []
---

> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0015: Retire --dangerously-skip-permissions for Swagger spawns; use a one-time human permission grant instead

**Status:** Proposed (reconstructed)

## Context

The Watchtower spec spawned an unattended Swagger job-agent with `claude --dangerously-skip-permissions` because nobody is present to approve its prompts. Testing under an auto-mode Marshall session revealed two Claude Code auto-mode classifier denials: (1) spawning a `--dangerously-skip-permissions` agent was blocked as 'an unsafe agent loop with no approval gate'; (2) editing `.claude/settings.local.json` to add permission-allow rules for the Swagger was blocked as 'self-modification the user did not explicitly request.' Both denials meant an auto-mode Marshall could neither launch a bypass worker nor grant itself the permissions needed to avoid one.

## Decision

Retire the bypass spawn entirely. The human grants a scoped `permissions.allow` boundary once, out-of-band, in `.claude/settings.local.json`: `Bash(tmux new-window*|kill-window*|list-windows*)` so the Orchestrator can spawn/close workers, plus `Read/Write/Edit(<engine-dir>/**)` + scoped Bash for the engine's own scripts so the worker runs unattended with zero prompts. After that one-time grant, the Orchestrator spawns plain `claude` (never `-p`, never `--dangerously-skip-permissions`) and it runs clean.

## Alternatives Considered

(a) Keep `--dangerously-skip-permissions` as a 'temporary spike shortcut' — rejected: incompatible with an auto-mode Orchestrator by the classifier's own rule, and unsafe for an unattended process with full bypass. (b) Have the Orchestrator self-grant the allowlist at dispatch time — rejected: classifier-blocked as self-escalation, and correctly so (an agent should not expand its own privileges).

## Consequences

A non-bypass Orchestrator successfully spawned a non-bypass worker via the allowlisted `tmux new-window` with zero prompts, proving the model end-to-end (ticket claimed, executed, report written, verified, window closed). Known gap: a job that writes outside the pre-approved directory will prompt and hang under this boundary — the correct fail-safe; the allowlist must be widened deliberately per new job type, never pre-granted broadly. The settings file is gitignored, so the grant is per-machine and must be re-applied on every new machine.

## Related

- Sessions: `627e86a2`

## Provenance

- **Sessions** (1): `627e86a2` · 2026-06-05
- **Files** (candidate-level): `.claude/settings.local.json`, `docs/watchtower/build-state.md`, `experiments/watchtower-engine/skills/marshall/SKILL.md`
- **Commits** (candidate-level): `2d09641`

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
