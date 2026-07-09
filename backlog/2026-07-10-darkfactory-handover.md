# Dark Factory — hard handover, 2026-07-10

Resume point for a fresh session. Self-contained; absolute paths; no chat history needed.
Repo: `/Users/davidcruwys/dev/ad/apps/dark-factory` · machine: mac-mini-m4 · subscription-only (interactive `claude`, never `-p`).

## Where this stands (all verified on disk 2026-07-10)

- **Engine is hardened and PROVEN.** Shipped + golden-job-green this cycle:
  - **T1-14** — `WORKER_TIMEOUT` now resets on worker *activity* (pane output), not just artifacts. Was the 240s reclaim loop that stalled long tickets. `--worker-timeout` flag also added (default 1800 for war-game runs).
  - **T1-17** — `commit()` is idempotent: a missing `running/` file skips instead of crashing the whole kernel.
  - **T1-18** — `promote` refuses re-injecting a `done` ticket without `--force`.
  - Two clean back-to-back cycles proved `ea6012b`'s steady state (the golden-job regression check that was missing).
- **Chime is live** — `consumer.py` running (`pgrep -f consumer.py`; pid was 14040), watching `engine/store/events/` + omi-fetch events, plays Glass.aiff on `job.completed`. ⚠️ **Not reboot-persistent** (started via nohup, no launchd yet).
- **Portfolio:** 5 done · **47 ready** · 8 blocked(1) · 2 blocked(2). Index: `backlog/wargames/README.md`. Staged tickets: `backlog/wargames/tickets/`. The 52 LATER briefs: `plans/wargames/candidates.js`.
- **Git:** code clean at `5b478b6`. Only runtime store ledgers dirty (`audit.jsonl`, `.done-state.json`, `.wake-state.json`) — expected, they accumulate; commit or leave per convention.

## How to run jobs — THE ONE PATH (memorize; don't invent a second)

Select, then run. Use **absolute paths** — `promote-wargame` is at repo root, `orchestrator` is in `engine/` (the cwd trap bit us repeatedly):

```bash
python3 /Users/davidcruwys/dev/ad/apps/dark-factory/bin/promote-wargame.py --list       # portfolio status
python3 /Users/davidcruwys/dev/ad/apps/dark-factory/bin/promote-wargame.py T1-15         # select (queue a ticket)
cd /Users/davidcruwys/dev/ad/apps/dark-factory/engine && \
  python3 orchestrator.py --pool 1 --model sonnet --max-wall 3600 --worker-timeout 1800  # run
```

Watch: `python3 engine/status.py` (queue/running/done + tmux liveness) · `tmux attach -t df-worker-1` (over-the-shoulder). Chime tells you the instant a job reaps.

## Hard rules (earned this session — don't relearn them)

- **This seat authors + dispatches; it does NOT read/edit impl to build.** Building is a worker's job via the engine. Tripwire: if you're grepping source to edit it for a ticket, stop and dispatch instead. (Memory: `feedback_po_seat_never_builds`.)
- **Editing engine code is dispatchable** — Python doesn't hot-reload, so a worker safely edits `orchestrator.py` while it runs; the change lands next launch. Only tickets that *run/kill the engine* (T1-01/02/03/05/06) are `SELF-HOST` and run attended.
- **Never re-promote a `done` ticket** (now guarded, but the habit stands) — it caused a full-engine crash.
- **After any engine edit, run one full cycle before trusting it** (the golden-job check) — a parse-check + fake-pane test can't catch a commit-path crash.
- **Interactive `claude` only, never `-p`.** `warm_pool.safety_check()` enforces (aborts if `ANTHROPIC_API_KEY` set).

## Next actions (prioritized)

1. **T1-15 — independent re-verify at reap (READY, high).** The single highest-value ticket: makes the engine re-derive each ticket's verdict from its own `## Verification` block instead of trusting the worker's word. This whole session had to do that by hand; T1-15 automates it. Run it: `promote-wargame.py T1-15` → orchestrator.
2. **T1-16 — durable verdict ledger + prior-chain** (blocked on T1-15). Resume-from-disk state.
3. **Chime reboot-persistence** — make `consumer.py` a launchd agent (mirror `engine/launchd/com.appydave.dark-factory-wake.plist` + `install.sh`). Small; not yet ticketed.
4. **Spec the factory-console skill** — `backlog/2026-07-08-factory-console-skill.md`. The driver skill that closes today's frictions: one gap-free run-path, cwd-proof commands, event-driven watch (Monitor, not timer-polling), seat/floor discipline baked into its shape. David wants this; needs a short scoping interview then build.
5. The other **47 ready tickets** — drain progressively via `--next N`, watch, repeat.

## Open threads (not yet actioned)

- **"Close the loop" — David wants to point the next session at something bigger.** The insight: engine events (`job.completed`) should reach *watchers* (via `Monitor` / blackboard MCP / Switchboard SSE), not just chime to the human. Current watching is timer-polling (a stopgap). Ask David for his reference before designing this.
- **Watching should be event-driven, not polled** — use the harness `Monitor` tool (block-until-`done/`-changes) or the specced Switchboard SSE bus (C3/DF-7, blocked on Switchboard being down). The Chaperone skill's timer-polling is generic; the factory can do better.

## Key files

- `backlog/wargames/README.md` — portfolio index + systemic flags
- `bin/promote-wargame.py` · `engine/orchestrator.py` · `engine/status.py` · `engine/consumer.py`
- `engine/README.md` + `engine/docs/ENGINE-NOTES.md` — engine internals (read before touching)
- `backlog/2026-07-08-factory-console-skill.md` — the driver-skill idea
- `docs/switchboard-state-authority-fork.md` — T1-11's output (the deferred state-authority decision, both branches + triggers)
- Memories: `project_wargame_portfolio`, `feedback_po_seat_never_builds`, `project_workflow_trigger_architecture`
