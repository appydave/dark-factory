---
id: ADR-0024
title: "Spawn watchtower Swaggers with interactive claude, never claude -p/headless"
status: proposed
scope: internal
date_decided: 2026-06-05
deciders: [David Cruwys]
confidence: reconstructed
recurrence_count: 1
provenance:
  sessions: ["98af2b78"]
  files: [".claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/MEMORY.md", ".claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/spawn-interactive-not-headless.md"]
  commits: []
tags: []
---

> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0024: Spawn watchtower Swaggers with interactive claude, never claude -p/headless

**Status:** Proposed (reconstructed)

## Context

Marshall spawns Swagger sessions into new tmux windows to process watchtower-engine tickets. Interactive spawns leave the window hanging open after completion (see companion learning on hanging windows), which initially looked like a case for switching to `claude -p` (print/headless mode) so the process exits and the window auto-closes.

## Decision

Never use `claude -p`/headless/SDK mode to spawn watchtower-engine sessions. Always spawn interactively. As of 2026-06-15, Anthropic changed billing so that `-p`/headless/SDK invocations draw from a separate API credit pool reserved for the Claude SDK, rather than running on the Max subscription; interactive `claude` sessions continue to run on Max. The window-hanging problem is solved separately by having the watcher explicitly `tmux kill-window` once the ticket lands in `done/`.

## Alternatives Considered

Option B (rejected): spawn with `claude -p`, letting the process exit and the tmux window auto-close on its own — mechanically simpler (no explicit kill step) but, as of 2026-06-15, bills against the separate metered SDK API credit pool instead of the Max plan. Option A (accepted): keep interactive `claude` on the Max plan and have Marshall's `done/` watcher explicitly kill the window on completion — no billing change, and the transcript stays inspectable while still debugging the engine.

## Consequences

Every future Swagger/watchtower spawn must go through an interactive `claude` invocation, and the dispatching Marshall session is responsible for detecting completion (via `done/`) and killing the window itself — this still needs to be wired into the `run-next-workflow` SKILL as a standing step rather than a one-off manual `tmux kill-window` call. The rule was also written to Claude memory so the `-p` suggestion doesn't recur in future sessions.

## Related

- Sessions: `98af2b78`

## Provenance

- **Sessions** (1): `98af2b78` · 2026-06-05
- **Files** (candidate-level): `.claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/MEMORY.md`, `.claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/spawn-interactive-not-headless.md`
- **Commits** (candidate-level): —

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
