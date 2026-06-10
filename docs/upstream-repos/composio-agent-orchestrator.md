# agent-orchestrator — ComposioHQ/agent-orchestrator

**Repo:** https://github.com/ComposioHQ/agent-orchestrator
**Local clone:** `~/dev/upstream/repos/agent-orchestrator/` (cloned 2026-06-10; registered in `brains/source-repos.md`)
**Stars:** 7,479 · **Latest:** v0.9.2 (May 2026) · **Created:** 2026-02-13 · **Last push:** 2026-06-09 · **Open issues:** ~944 (high activity, not abandonment) · **Status:** active
**Relevance rank:** #3 · **Highest traction in the class**
**Review status:** ☐ not yet reviewed

> ⚠️ Star count / release date captured 2026-06-10 — re-verify before citing.

## What it is

Spawns parallel CLI-agnostic coding agents — **Claude Code (default) + Codex / Aider / Cursor / OpenCode / Kimicode** — each in **its own git worktree / branch / PR**. Tagline: "Spawn parallel AI coding agents, each in its own git worktree. Agents autonomously fix CI failures, address review comments, and open PRs — you supervise from one dashboard."

## Architecture

- **Isolation:** git worktree + branch per agent; runtime-agnostic over **tmux / Docker**.
- **State:** runtime state auto-derived under `~/.agent-orchestrator/{hash}-{projectId}/` + `last-stop.json` — **per-project local files, not a central state DB.** In practice **GitHub itself acts as the de-facto state plane.**
- **Liveness / progress:** monitored via **PR status, CI results, and review comments** (reaction rules: `ci-failed` / `changes-requested` / `approved-and-green`) plus a **30-min `escalateAfter` stuck-detection timeout**.
- **Reaping:** lifecycle keyed off PR/branch resolution rather than an explicit worker-kill service.

## HITL model

**Supervise-and-merge dashboard.** Agents work autonomously (fix CI, address review comments, open PRs); the human supervises and merges from one dashboard.

## Observability

A single **dashboard** aggregating agent state from GitHub-side signals (PR/CI/review). This is its strongest feature — liveness derived from *external observable signals* rather than worker self-report.

## Overlap with Dark Factory — and where it differs

**Validates our "observe the loop externally" principle** (factory-operations-telemetry memory: don't trust the worker's own bookkeeping). It derives liveness from PR/CI/review signals + a stuck timeout — exactly the external-observation stance, proven at 7.5k stars.

**Differs:** **GitHub *is* the state plane.** Elegant and zero-infra, but it welds the whole system to GitHub and provides **no separate comms bus, no resource-health, no session-telemetry service.** Not a stateless-floor + state-plane split — it's "let GitHub be the database."

## What to steal

- **Liveness-via-external-signals + stuck-detection timeout** — the single most transferable idea; maps onto our staleness-detector / reaper.
- The **one-dashboard supervise-and-merge** UX as a Watchtower reference for the PR-producing job class.

## What it gets wrong (for our purposes)

- GitHub-as-state-plane is a ceiling: no plane separation, can't observe resource health or non-GitHub work, couples everything to one external service.

## Next-action if we review

Read the reaction-rule engine (`ci-failed` / `changes-requested` / `approved-and-green`) and the `escalateAfter` stuck-detection — port the *pattern* (external-signal liveness) onto Switchboard/AngelEye without inheriting the GitHub coupling.
