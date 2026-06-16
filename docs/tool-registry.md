# Dark Factory — Tools & Scripts (first-class)

**Status**: new — 2026-06-01 · seeded, deliberately incomplete
**Companion docs**: `systemic-fixes.md` (fix the class), `architecture.md` §5 (the Pulse pattern), `INDEX.md`

---

## The principle

**Before doing a job, ask: what tools would make this job efficient — and should I build them first?**

Tools and scripts are **first-class**, not scaffolding you reach for ad hoc. A factory without a sharp, indexed, *current* toolset re-solves the same problems by hand every time. The tooling layer is part of the system, not a side effect of it.

Two kinds of tool matter:

1. **Platform tools** — what Claude Code itself gives you: `Workflow`, `/loop`, `/simplify`, ultracode, `Agent`/subagents, `ScheduleWakeup`, skills, MCP servers. These are *capabilities you already have* — but only if you know they exist and what they're for.
2. **Repo tools** — the scripts and workflows this project owns (`tools/`, `.claude/workflows/`).

## The standing rule

> An index of tools that isn't kept current rots exactly like docs do. **A tool registry is only worth building if its refresh is automated.**

So this doc has two halves: the **index** (below), and the **freshness mechanism** (further below). The index without the mechanism is a liability.

---

## Index — Platform tools (Claude Code)

| Tool | Use it for | Notes |
|------|-----------|-------|
| `Workflow` | Deterministic multi-agent orchestration (fan-out, pipeline, loop-until) | The factory's runtime substrate |
| `Agent` / subagents | One fresh-context task; parallel independent work | No context pollution |
| `/loop` | Recurring task on an interval, or self-paced | Polling, babysitting |
| `/simplify` | Reuse/simplification/efficiency cleanup of a diff | Quality, not bug-hunting |
| `/code-review` | Bug + cleanup review (low→ultra effort) | `ultra` = cloud multi-agent |
| ultracode | Standing opt-in to author+run workflows for every substantive task | Off by default |
| `ScheduleWakeup` / cron | Timed re-entry; scheduled triggers | Pulse jobs |
| Skills | Discoverable, description-triggered capabilities | See the skill roster |
| MCP servers | External tools (blackboard, brave, chrome, notebooklm…) | Per-session |

⚠️ **This table is a snapshot.** Claude Code ships new tools constantly. Treat any entry older than the last refresh as suspect.

## Index — Repo scripts

| Path | What |
|------|------|
| `tools/serve.sh`, `tools/stop.sh` | Mochaccino server control (:7420) |
| `tools/mocha-census/run-full.sh` | Design audit + rate-and-label board across both machines (:7440) |
| `tools/design-lint/shoot-one.py` | Post-render lint gate — screenshots a render, agent critiques vs `RUBRIC.md` |
| `tools/youtube-assets/` | YouTube asset scripts |
| `experiments/watchtower-engine/bin/claim-next.sh` | Atomic ticket claim (the engine mutex) |
| `experiments/watchtower-engine/bin/test-atomic-claim.sh` | Concurrency proof for the claim |
| `experiments/watchtower-engine/bin/dispatch-swagger.sh` | Spawn a Swagger job-agent (tmux) for a claimed ticket |
| `experiments/watchtower-engine/bin/reaper.sh` | Reap orphan tmux windows (keys off `done/<id>.json` mtime + grace) |
| `experiments/watchtower-engine/bin/retry.sh` | Re-queue `failed/` → `queue/` with exponential backoff |
| `experiments/watchtower-engine/bin/constellation-status.sh` | Preflight: report which constellation apps are up |

## Index — Workflows (`.claude/workflows/`)

Workflows are first-class tools and get the same **when + what** visibility as skills/agents/scripts. A workflow is an SOP-in-data (`sop-lifecycle.md`).

| Workflow | What it does | When it runs |
|----------|--------------|--------------|
| `daily-review` | End-of-day digest: activity, what needs David, idle/stale drift | end of day / on the engine queue / `/loop` |
| `level-1-census` | Census a batch of artifacts (parallel fan-out, schema-validated) | per census-batch ticket |
| `content-analysis` | YLO probe — analyse transcript/content | YouTube-launch lane |
| `title-gen` | YLO probe — generate titles | YouTube-launch lane |
| `titles-human` | YLO probe — title selection (HITL) | YouTube-launch lane |
| `thumbnails` | YLO probe — thumbnail ideation/render | YouTube-launch lane |
| `nail-salon-video` | YLO probe — domain video flow | on demand |
| `aitldr-enrich` | AITLDR lane — enrich content metadata | YouTube-launch lane |
| `transcript-recategorize` | AITLDR lane — recategorize transcripts | YouTube-launch lane |
| `hello`, `hello-blackboard` | Smoke tests (plain / MCP-blackboard) | spikes / validation |

⚠️ **Visibility gaps** (logged in `backlog/problems.md`): no single place yet shows *last-run / status / cost* per workflow (that's the Watchtower view), and the Workflow-tool name registry is **loaded at session start** — newly authored workflows must be run by `scriptPath` until the session reloads.

---

## Freshness mechanism — reuse, don't reinvent

David's instinct: *"a little cron job that drops a workflow execution entry once a day to keep the Claude Code brain up to date."*

**This is right in shape — and it mostly already exists.** The honest, fix-the-class answer is *not* a new bespoke cron:

- **`refresh-claude-brain` skill already exists** (`brand-dave:refresh-claude-brain`) — "refresh claude brain / what's new in claude code / anthropic updates / hooks docs / SDK changes." The refresher is built.
- **`framework-pulse` is already a planned workflow** (`architecture.md` §5) — "the same shape as Upstream Pulse, pointed at anthropics/claude-code + community workflow collections, to catch new primitives and patterns." That is *exactly* the daily-CC-tool-refresh job.

So the missing piece is not a tool — it's **wiring**: schedule the existing refresher (cron drops a ticket → workflow runs → updates this registry's platform-tools table). That's the Scheduled trigger type from the spec, using the Intake/ticket model (`intake.md`) — cron writes a ticket, it does not spawn a session.

## Open decisions

- **Schedule cadence** — daily? weekly? (CC moves fast; daily is defensible.)
- **Refresh target** — does the pulse write into *this* file's platform-tools table, or into a brain that this file links to?
- **`refresh-claude-brain` vs `framework-pulse`** — are these one job or two? (Skill = interactive refresh; workflow = headless scheduled. Likely the workflow *invokes* the skill's logic.)
- **Cron wiring** — needs explicit go-ahead (a live scheduled job is a standing outward commitment).
