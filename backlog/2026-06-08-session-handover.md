# Session Handover — 2026-06-08 (clean close → fresh start)

> **Rebuilt 2026-06-08 from transcript `627e86a2…jsonl`.** The first pass of this doc was too thin — it dropped half the loose ends. This version is reconstructed from the raw session so a cold start loses nothing. (This *is* the recurring problem DF-6 must fix: a handover must capture **all** open threads, not a summary.)

**The model (David):** don't compact — **close this window, start a fresh one.** State lives in files, not the conversation. A new `claude` + `/marshall` reads `MEMORY.md` (auto-loads) + this doc + `backlog/specs/tickets.json` → clean pickup. **A bare `/marshall` is a handover *pickup*, not a work order** — Marshall surfaces the threads below and asks what to do; it does not dispatch. (See memories `session-handover-not-compaction`, `cold-start-orient-and-ask`.)

## Read on start
1. **`MEMORY.md`** — auto-loads every durable decision/correction.
2. **`backlog/specs/tickets.json`** — the spec/ticket registry (DF-1…DF-6).
3. This doc — the full thread list.

## RUNNING at close (all verified UP 2026-06-08 — do NOT restart)
- **Mochaccino `:7420`** (Python, root `mochaccino/`) — the 8 pre-existing blackboard/POEM designs (01–08, incl. a *different* `05-probe-progression`).
- **Mochaccino `:7422`** (Python, root `.mochaccino/`) — **this session's 5 designs**: `01-session-journey`, `02-brain-remembers`, `03-four-memories`, `04-brain-sleeps`, `05-dark-factory`. ⚠️ the two galleries each have a "design 05" — naming collision.
- **Watchtower board `:7430`** (Node, `experiments/watchtower-board/`) — Floor/Lanes/Converge (board v5). NOT daemonized.
- **Switchboard `:5099`** — launchd daemon (`com.appydave.switchboard`). Survives restarts. Event log 212+ entries.
- **AngelEye `:5051`** — **David runs it MANUALLY** (`overmind start` in `~/dev/ad/apps/angeleye`). NOT daemonized. **Marshall never starts/stops/touches it** (Marshall killed David's instance + made a stale socket several times — that's why this rule is hard).

## CLEAN at close (nothing to reap)
- No Swagger windows · no monitors armed (reaper + retry both stopped) · engine `queue/` and `running/` empty.
- Parked (not abandoned): `experiments/watchtower-engine/deferred/q-20260607-board-v6-map.json` (Board v6 Map view).

---

## ⏳ Awaiting your eyes (rendered, never judged) — **Topic #1**
1. **Cortex "how a brain works"** — designs **02/03/04** at `http://localhost:7422/designs/`. You approved the *shapes* (A+B+C at the gate) but never eyeballed the rendered HTML. You said *"I feel like we're going to have problems"* — verdict still pending. Topic #1 ("how to improve our visualisations + problems specific to cortex") was **raised, never answered.**
2. **Dark Factory overview — design 05** at `:7422/designs/05-dark-factory`. Rendered for **Martin**. Awaiting your "sharpen X before ship."
3. **`05-dark-factory-v2` — RESOLVED, not a loose end.** An improved v2 was built in another conversation and **renamed back onto the original `05-dark-factory`** there. So the live `05-dark-factory` already *is* the improved version; there's nothing missing and nothing to recover. (Recorded here only to stop a future session re-chasing it.)
4. **Watchtower board v5 (`:7430`)** — you saw the converge UI, agreed it beats the scrapped promote-buttons, but never ratified it as a reference design.
5. **Specs written at close, unread by you:** Mocha Lab (`backlog/2026-06-08-mocha-lab-spec.md`, 297 lines — read §16 for open PO decisions), DF-3 (`backlog/specs/stability-1-instrument-loop-spec.md`, 330 lines), DF-4 (`backlog/specs/self-learning-guardrail-spec.md`, 226 lines).

## 🤔 Decisions surfaced, not made
- **AngelSentinel split (DF-1) — 4 open decisions** (§10 of `~/dev/ad/apps/angeleye/docs/requirements/angelsentinel-split-spec-2026-06-08.md`): ① build path — carve standalone (rec.) vs rebuild on appysentinal boilerplate; ② repo shape — two repos (rec.) vs monorepo workspaces; ③ comms contract — REST+Socket.io guarded-write (rec.) vs shared-fs-read vs Access-zone; ④ telemetry — retrospective aggregation (rec. v1) vs live hook-counters. **Settled:** naming = "AngelSentinel" (collector) / "AngelEye" (control plane). You opened a *separate* AngelEye+Ralphy conversation to build knowledge and hand back a ticket — **that Ralphy session's output is unknown here; the build never kicked off.**
- **workflow.js HITL** — confirmed: boundary-HITL (between jobs) yes; mid-run gate inside one workflow run no. One edge **unverified**: can a subagent *inside* a workflow call `AskUserQuestion`? Cheap experiment, never run.

## 🔨 Named but unbuilt
- **AppyRadar** (was "AppyCtrl" — corrected 2026-06-10, see docs/appyradar.md) — named all session as the home for orphan/stale-process detection, tmux ownership (AngelEye can't walk the reparented process tree), machine health, untracked-file-rot. Preflight shows it unwired. No spec.
- **M4 Mini Swagger** — cortex comprehend ran read-only over SSH; a *persistent* M4 Swagger with its own permission boundary (Phase 3) was never set up. Needs the one-time M4 grant.
- **Floor↔Lanes bridge** — `converge N→1 brief` writes a floor ticket (Lane→Floor), but the return leg (job done → reflected back in Lanes) is unbuilt. Bridge is one-directional.
- **AngelEye daemonization** — only a dev `start.sh`; no production `serve` command / launchd plist (parity with Switchboard). An AngelEye/Ralphy job.
- **AngelEye live hook** — reportedly wired via Ralphy (28 events, `WorktreeCreate` excluded) but later found to be **backfilling from transcripts, not receiving live events**. Actual `~/.claude/settings.json` hook state **unverified at close.**
- **Board v6 Map view** — live constellation status (apps up/down, queue counts, monitor states). Ticket parked in `deferred/`.
- **Chronicle / build-documentary** — Tesla-Gigafactory story of building the factory. Raw material exists (transcripts/git/memories/proof). Neither capture layer built.
- **Deeper-documentation system** as a first-class factory subsystem — research done (FliDeck/Mochaccino/prose→schema); comprehend-visualise is only the seed.

## 🛠 Open robustness / hygiene threads
- **Bookkeeping unreliability (the core unfixed bug).** 3 of today's later Swaggers wrote **zero run records + zero handbacks**; cortex Swagger botched handback too. Band-aid (nag the ticket) worked once. Real fix = **DF-3**: observe the loop *externally* (dispatcher+reaper emit → Switchboard log → Watchtower), never trust the worker. Spec written, not built. **P1.**
- **Switchboard event log — 212 and unbounded.** Durable log accumulates `job.queued`/`session.stale` (not ephemeral `process.snapshot`). Exists for `Last-Event-ID` replay. No pruning. The fork you stopped at (below).
- **AngelEye staleness detector is broken** — walks tmux panes (BFS) to find claude, but Claude Code v2.x reparents the session to its daemon, so the pane only holds MCP servers. Fix: use `GET :5051/api/sessions/:id/liveness → last_active`. Not integrated into the reaper.
- **Monitor rot** — compaction doesn't kill monitors; re-arming stacks duplicates (had 3 alive mid-session). Doctrine fixed (arm-on-dispatch/stop-on-done/track-ids), not tooling-enforced. (memory `monitors-survive-compaction`.)
- **PreCompact hook** — fixed to emit valid JSON, but fires *after* the model stops, so it can't actually run a sweep — it's a reminder only.
- **Staggered-dispatch workaround** — parallel Swaggers needed staggered timing because "claim oldest" can't bind a window to a specific ticket → this is the **claim-by-id gap = DF-3** territory, demonstrated live.

## 🧭 In-flight understanding (forks you stopped at)
- **Switchboard = the telemetry substrate.** You built a working model (polling is Bun/TS software not claude; logs are SSE frames in a durable append log). You stopped at: **immediate** → prune the log; **bigger** → the event log *is* DF-3's external telemetry store. **Unstated next Q:** *how to set a retention window that preserves replay for reconnecting subscribers yet bounds growth* (keep last N / prune older than T, with `Last-Event-ID` still valid).
- **Mochaccino at scale — Topic #2.** Engine confirmed; FliDeck's MVC lesson absorbed. Unaddressed: structure for **hundreds** of presentations from one Mochaccino server (gallery scaling, grouping/search, manifest format). FliDeck (`~/dev/ad/flivideo/flideck`, gallery `~/dev/ad/brand-artifacts/presentation-assets/`) had 343 bespoke files with no data layer — mine its learnings.
- **Osmani agent-skills** — named as a spec/code-build candidate (`~/dev/ad/brains/agent-skills-osmani`); installed plugin name/source **unverified** — confirm before leaning on it.

## Spec backlog (write done · build LATER · `backlog/specs/tickets.json`)
| Ticket | State | Priority | Build via |
|---|---|---|---|
| DF-1 AngelSentinel split | spec-written | 2 | Ralphy (in-app) |
| DF-2 Mocha Lab | spec-written | 2 | TBD |
| **DF-3 Stability #1 — instrument the loop** | **spec-written** | **1 (most evidence)** | TBD |
| DF-4 Self-learning guardrail | spec-written | 3 | TBD |
| DF-5 Tool-usage telemetry (folded into DF-1 §7) | spec-written | 3 | Ralphy (with DF-1) |
| DF-6 Clean session handover & restart | **spec-todo** | 2 | TBD |

## Factory tooling built this session
- **`millwright`** skill — the build-side gatekeeper (picks the FORM of machine).
- **`comprehend-visualise`** skill (+ `comprehend-fanout.workflow.js`) — point at code/prose → data-first → Mochaccino render.
- **spec-writer-via-Swagger** pattern — proven on DF-1…DF-4 (spec-writer's 297-line PRD beat the ad-hoc spec).
- **Engine**: `bin/reaper.sh` (keys off `done/`), `bin/retry.sh` (3× backoff), `bin/dispatch-swagger.sh` (+registry), `bin/constellation-status.sh`.
- **Switchboard** scaffolded + configured (launchd) — *the first real build through the dispatch loop*.

## How to start fresh
1. Close this window.
2. `cd ~/dev/ad/apps/dark-factory && claude` → `/marshall`.
3. Marshall: load MEMORY.md → preflight (report only, don't start apps) → read this handover + `tickets.json` → **surface the threads above and ASK what to do next.** Do not dispatch on a bare open.
