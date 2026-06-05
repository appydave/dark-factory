# Dark Factory Sentinel — always-on front desk for the Watchtower

**Raised**: 2026-06-06 (David). **Status**: opportunity / spike-proposal — not started.
**Relates to**: `2026-06-06-swagger-lifecycle.md` (the orphan reaper), problems #15 (session-trigger), #19 (return-leg).

## The idea (David)

What if a **Dark Factory Sentinel** — built from the AppySentinel template (`~/dev/ad/apps/appysentinal/`) — were an always-on background service that (a) watches for & cleans up stray `claude`/tmux Swagger processes, and (b) hosts the queue + a message bus, so instead of driving the factory from inside a terminal, David **sends it messages** and it queues/dispatches/reports on his behalf?

## What the research found (agent review, 2026-06-06)

- **AppySentinel = boilerplate**, not an app. `npx create-appysentinel <name>` scaffolds a Sentinel. Plain TypeScript/Bun (deps: pino/ulid/zod). Supervised always-on via **launchd/systemd, `KeepAlive=true`**. (Also supports on-demand mode.)
- Spine: collect → Signal → store → expose (MCP / HTTP / CLI). **Inbound messaging = a file-watched `state/` command inbox** — the same file-as-IPC pattern the Watchtower queue already uses.
- **HARD WALL: a Sentinel is pure observer code. It never runs `claude`, never spawns agents, never dispatches work.** (Its own documented agent-handoff uses `claude -p` — the Max-billing footgun we ban.) It is, by rule, "not an orchestrator" (observer-only, spec §12).

## The resulting architecture — the communication bus (the nervous system)

Extended 2026-06-06 (David): the Sentinel isn't just an inbox — paired with **Monitor** it becomes a full **bidirectional communication bus**. The Sentinel *writes* events; each in-session agent arms a `persistent` **Monitor** whose command consumes those events and turns each into a chat notification → the agent wakes and responds. The Sentinel never runs `claude`; the Monitor (an in-session Max primitive) does the waking. **Durable write side + reactive listen side.**

### Transport — stream, not filesystem (David, 2026-06-06)

The Monitor's `command` is *any* long-running shell command; its own canonical examples include `node watch-for-events.js` ("a WebSocket listener"). ✅ So the Monitor can consume a **stream directly** — no filesystem in the hot path:
- **Production:** Sentinel pushes **SSE** (or a socket) outward; each agent's Monitor runs e.g. `curl -N https://sentinel/sse?subscribe=marshall,broadcast`. On-grain with AppySentinel's `api-binding` (Hono HTTP) + the "Deliver" recipe zone (pushing out ≠ observer-only violation).
- **Testing only:** files + **`fswatch`** (macOS FSEvents; NOT `inotifywait`, which is Linux) to prove "Monitor wakes on event" before building the SSE server.

### Addressing — topic subscription, not folder-per-channel (David, 2026-06-06)

A subscriber declares its topics **at connect time** (`?subscribe=marshall,broadcast`); the **broker (Sentinel) filters server-side**. The agent only receives what it subscribed to. Standard pub/sub — multiple Marshalls, multiple Sentinels, dynamic topics all fall out for free. Beats folder fan-out: dynamic subscriptions, routing in one place, no FS sprawl.

### Durability — one event log + `Last-Event-ID` replay (the gap in pure-stream)

SSE/sockets are ephemeral: if no Marshall is connected at push time, the message is lost — the exact survive-a-dead-session property we need (today's orphan bug violated it). Fix without folders: Sentinel appends every event to **one durable log** with monotonic IDs; a reconnecting agent sends **`Last-Event-ID`** and the broker replays the gap. **Durable AND reactive, no folder-per-channel.**

```
DURABLE (plain code, always-on)                 EPHEMERAL (Max subscription)
Sentinel ──SSE(topic-filtered)──▶  Monitor(curl -N ?subscribe=marshall) ── Marshall
  │ queue, reaper, registry,       Monitor(?subscribe=swagger-7) ───────── Swagger #7
  │ router, event-log+IDs          (?subscribe=david) ──▶ digest/push ───▶ David
  ▼                                ▲ reconnect → Last-Event-ID → replay gap
reads ps/tmux, Supabase, hooks…
```

- **Sentinel (write side) = FRONT DESK + BROKER:** inbox David messages (HTTP/MCP/CLI, incl. Tailscale Funnel), writes tickets into `queue/`, holds **registry + reaper**, **routes** events to subscribed topics, keeps the durable event log.
- **Monitor (listen side) = SYNAPSE:** subscribes to its topics; the bus **pushes** to it — no terminal polling.
- **In-session (Max) = WORKERS:** existing `/loop` + `run-next-workflow` (or teammate-mode Swaggers) claim tickets, run interactive `claude`, **never `-p`**.

**Collapses four open problems into one mechanism:** #15 (external msg → Monitor wakes Marshall), **C3c** (Marshall auto-wake = a Monitor subscribed to `marshall`, same mechanism), #19 (result → `david` topic), #8 (Sentinel watches processes → bus alert).

## Fit verdict

- **(a) stray-process registry/reaper — STRONG fit.** On-grain except reaping is a *mutation* (template is observer-only) → add reaping as a deliberate scoped waiver (planned `mcp-tools` recipe, spec §12/§15). The registry alone retires the swagger-lifecycle "step 1".
- **(b) message-bus — PARTIAL.** Great as inbox/queue/return-leg; **cannot be the dispatcher/executor** (that stays in-session on Max). Using it as a *work-dispatch* bus runs against the observer-only grain; using it as a queue-and-report observer is on-grain.

## Recommended smallest probe

1. `npx create-appysentinel dark-factory-sentinel` → wire **`poll-command` (ps/tmux/pgrep) + `snapshot-store` + `mcp-binding`**, **read-only registry, NO reaping**. Proves an always-on host on Max + kills orphan-invisibility, without touching `claude`.
2. **In parallel:** a `claude --teammate-mode tmux` probe — may dissolve the orphan class natively (managed lifecycle + talkable agents). Pick the path that makes orphans *impossible* vs merely *cleaned up*.

## Risks

- Spec↔code drift in the template (CLI doesn't auto-handoff; `handoff.ts` uses `-p`) — boilerplate not fully proven; budget for rough edges.
- Single-process-per-Sentinel + dev-while-deployed file/port contention (spec §9.4) — Sentinel and in-session worker must not fight over the queue dir.
- Using a Sentinel as a *work inbox* is new territory for it (existing instances are telemetry observers only).

## Reference

Full report in session 2026-06-06. Conceptual brain doc: `~/dev/ad/brains/dark-factory/appysentinel-otel.md`. AppyRadar reference Sentinel: `github.com/appydave/appyradar-sentinal`.
