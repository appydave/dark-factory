# Handover — 2026-06-07 (midday). Compact-survival + day plan.

**Read first:** `MEMORY.md` (every durable concept/decision loads from there). This doc = current state + loose ends + the day's next steps. Verify live state with:
`bash experiments/watchtower-engine/bin/constellation-status.sh`

## ⚠️ Re-arm after compact (Monitors die with the session)
Two standing Marshall **Monitors run in the session and will NOT survive a compact** — re-arm both first thing:
- **reaper**: `bash experiments/watchtower-engine/bin/reaper.sh` (keys off `done/`, 60s grace; auto-closes finished Swagger windows)
- **retry**: `bash experiments/watchtower-engine/bin/retry.sh` (failed → re-queue, exp backoff, max 3)

## Running now (apps, NOT in-session — survive compact)
- **Watchtower board** → http://localhost:7430 — tabs Floor / Lanes (Map = v6, queued, not built). `node experiments/watchtower-board/server.mjs`.
- **Switchboard** daemon (launchd `com.appydave.switchboard`) — :5099 SSE, :5100 jobs.
- **AngelEye** — server :5051, client :5050. Running; live hook wired (28 events). NOT daemonized (dies on machine restart; don't daemonize until Sentinel/control-plane split).

## Built & proven this session
- Switchboard durable-log refactor (topic-selective) — verified live.
- Concurrency (N Swaggers at once) — proven twice.
- Board v1 Floor · v2 Lanes · v3 idea-staleness · v4 promote (scrapped) · v5 converge bridge.
- Engine-state **reaper** (keys off `done/`) — proven; standing Monitor.
- **Retry-with-backoff** — proven; standing Monitor.
- Dispatch **registry** (`registry/<window>.json`) + `bin/dispatch-swagger.sh` (auto-registers).
- Constellation **preflight** (`bin/constellation-status.sh`) + baked into the marshall skill.
- **AngelEye live hook** wired via Ralphy — HANDBACK received (liveness API contract).
- **Symphony re-look** — our registry = its `claimed`; reaper stuck-case = its §8.5 stall-detection.

## Open loose ends (actionable)
- **Map view (v6)** — ticket `q-20260607-board-v6-map.json` is QUEUED, not dispatched.
- **Reaper STUCK-case** — build from AngelEye liveness: `GET :5051/api/sessions/:id/liveness` → `last_active`+`server_now`; stall = `(server_now-last_active)>timeout`; key on `last_active` NOT `status`. **Blocker:** registry is window→queue_id but AngelEye is by `session_id` → record the Swagger's `$CLAUDE_SESSION_ID` in the registry on dispatch.
- **`running ∩ done` reconcile rule** + harden run-next-workflow (a Swagger botched bookkeeping: skipped handback + left a `running/` stray).
- **Symphony lifts** — explicit claim-states + ONE consolidated reconcile loop (unify reaper+retry+stuck).
- **AppyCtrl** — investigate in its own window; could own tmux/process state (window→liveness, rot detector).
- **Auto-dispatch** of re-queued tickets (queue-Monitor / C3c) — retry re-queues but nothing auto-runs it yet.
- **Architecture visualisation** — do it structure-first (schema/JSON → Mochaccino), not started.
- **AngelEye** — M4-vs-Roamy hook target (parked); daemonize after Sentinel/control-plane split.

## THE DAY PLAN — start here post-compact (simple, will morph)
1. **Deeper documentation system** (David's #1 — make it first-class). Research deckhand slides (~30-40 categories) + Mochaccino + brains prose→schema work (**maybe on M4 Mini**) → first-class factory subsystem. Memory: `deeper-documentation-system`.
2. **Reaper stuck-case** (AngelEye liveness; handback in hand).
3. **Map view (v6)** — dispatch, or fold into #1.
4. **`running ∩ done` reconcile** + harden run-next-workflow.
5. **AppyCtrl** investigation (own window).
6. **Symphony lifts** (claim-states / consolidated reconcile).

## Key pointers
- AngelEye handback (reaper contract): `~/dev/ad/apps/angeleye/docs/requirements/live-hook-and-liveness-2026-06-07.HANDBACK.md`
- Keystone memories: `structure-first-then-render`, `mochaccino-prose-to-visual-engine`, `deeper-documentation-system`, `cleanup-is-harness-driven-not-remembered` (reaper + stuck-case + handback), `constellation-preflight-marshall-not-blind`, `canonical-hooks-spec`, `ralphy-plugin-builds-apps`. (All indexed in `MEMORY.md`.)
- Docs: `docs/watchtower/{build-state.md, reaper-brief.md, symphony-relook-2026-06-07.md}`; `backlog/concepts.md`; `backlog/2026-06-07-day-possibilities.md`.
- Method correction: **Ralph Loop ≠ Dark Factory**; **Communication = visual** (board = live-ops; architecture = structure→Mochaccino, not mermaid, not in-app); dropped the 60GB thread.
