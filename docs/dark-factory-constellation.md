# Dark Factory — The Constellation Map

**Status**: 2026-06-10 — the one holistic view of *all the parts and how they fit*. Read this before scoping any single component (especially Switchboard).

> **Why this doc exists.** The system was designed across many build-sessions, each solving an immediate problem on the Dark Factory floor. The result is coherent in pieces but never assembled in one place. The Symphony Spec is holistic about *one orchestrator's coordination loop* — it is **not** a map of the constellation, and it names none of our components. This doc is that missing map: what each role is, the boundaries between them, what's built vs. vapor, and where Symphony feeds in. When the model below and an older doc disagree on framing, **this doc wins on the constellation shape**; the source docs win on their own internal detail.

> **⚠️ CORRECTION (2026-06-10) — "AppyCtrl" was a wrong application.** Across the older backlog/spec docs, the process/resource/liveness observer is called **AppyCtrl**. That name and its "kills dead processes" role were wrong on both counts. The real application that *understands this machine and the other machines on the network and exposes their memory/process data via a Sentinel + MCP* is **AppyRadar** — and it is **read-only** (it never kills). AppyRadar is PoC-validated (2026-04-27), built on the AppySentinel substrate (Pilot 1). Its Sentinel rebuild landed **live** as `appyradar-sentinel` (`~/dev/ad/apps/appyradar-sentinel/`, proven 2026-06-11); the original SSH fleet collector (`scripts/audit.ts`) now lives only in the archived bespoke `_archived--appyradar/`, and the earlier typo'd `appyradar-sentinal` PoC is archived too. It is **not** a Baku app — `~/dev/baku/b-appy-radar` is only a UI mock of an AppyRadar snapshot. **Every "AppyCtrl" reference in the other docs is superseded by this map** until those docs are swept. Killing/reaping has no sentinel — it is **Marshall's** job alone.

---

## 1. The one-sentence frame

**Dark Factory is the whole system** — a self-improving capability factory you direct by talking to it. The "floor" is where agents execute. Everything else in this map is **infrastructure around the floor** that makes it operable, observable, and directable.

It is *not* one of the components below. Library (`canonical/`), Warehouse (`research/`), and Platform (`.claude/workflows/` + runtime) are the floor itself.

---

## 2. The constellation (one picture)

```
                    David (director — talks to one place)
                         │
        ┌────────────────▼─────────────────────────────────────┐
        │  CONTROL PLANE — Watchtower  (AppyStack / React)       │
        │  glass wall: decision cards, dashboards, verdicts      │
        │  └─ Marshall (the Conductor) lives here                │
        │     • the ONLY thing that runs `claude` + acts/kills   │
        │     • dispatches Swaggers (one per job, via tmux)      │
        │     • reads, records verdicts — never mutates canonical│
        └───────┬───────────────────────────────────▲───────────┘
                │ dispatch                           │ SSE (live state)
                ▼                                    │
        ┌───────────────── FLOOR — Dark Factory ─────┴──────────┐
        │  Swagger job-agents execute workflows on the floor     │
        └───────┬────────────────┬───────────────────┬──────────┘
                │ jobs/state      │ session events    │ process state
                ▼                 ▼                   ▼
   ┌────────────────────┐  ┌──────────────┐   ┌──────────────────┐
   │ COMMS + STATE       │  │  AngelEye    │   │   AppyRadar      │
   │ Switchboard         │  │ (read-only:  │   │ (read-only:      │
   │ (AppySentinel daemon│  │  session     │   │  machine + fleet │
   │  — never runs claude)│ │  last-active)│   │  resource/proc   │
   │ • job queue + state │  │              │   │  intel via SSH)  │
   │ • SSE bus + replay  │  └──────┬───────┘   └────────┬─────────┘
   │ • liveness-for-route│         └─ answer liveness/health (Marshall reaps) ─┘
   └─────────────────────┘
```

**Three planes + two read-only sensors:**
- **Floor** (Dark Factory) — agents execute (Marshall dispatches; Swaggers run jobs).
- **Comms + state** (Switchboard) — the nervous system: queue, job-state, message bus.
- **Control plane** (Watchtower) — the glass wall where the human decides.
- **AngelEye** + **AppyRadar** — two read-only sensors: AngelEye answers *session* liveness (Claude hook events); AppyRadar answers *machine/fleet* resource + process health (SSH across the 5-Mac network). **Neither kills** — Marshall is the only actor that reaps.

---

## 3. The roles, defined

| Role | Owns | Substrate | Build status |
|---|---|---|---|
| **Dark Factory** | The floor + Library/Warehouse/Platform — the whole | repo | live |
| **Marshall** (Conductor) | Conducting: dispatch, and the *act* of reaping (`tmux kill-window`). The only `claude` runner. Talks to David. | skill in dark-factory, runs in Watchtower | partial (C1 done) |
| **Switchboard** | **Communication + state**: job queue, claims/ownership, SSE bus + durable `Last-Event-ID` replay, liveness-for-routing | AppySentinel daemon, per-machine, never runs `claude` | **substantially built** |
| **AngelEye** | **Session liveness** — Claude Code hook events; answers "when was session X last active?" Feeds the reaper; never kills. | Claude Code hooks | **unbuilt / offline** |
| **AppyRadar** | **Read-only machine + fleet intelligence** — health, resource pressure (RAM/CPU/process), AI activity, maintenance debt across the 5-Mac network; exposed via Sentinel + MCP. **Does not kill.** (Supersedes the mis-named "AppyCtrl".) | AppySentinel (Pilot 1) | Sentinel rebuild landed **live** (`appyradar-sentinel`, 2026-06-11); original `scripts/audit.ts` collector now archived (`_archived--appyradar/`) |
| **Watchtower** | **The view + human control**: decision cards (≤5 Today), dashboards, verdict records; reads, never mutates `canonical/` | AppyStack / React | partial (Consumer proven) |

---

## 4. The boundaries (the rules that keep it clean)

### The CRUD-vs-kill rule (DF-7 Decision D4 — the load-bearing boundary)
> **Switchboard MAY do CRUD over its *own* comms/queue/state domain** — enqueue, claim, complete, fail, requeue a dead claimant's record `claimed→pool`. **It NEVER mutates the external observed world** — kill a process, close a tmux window. *"Requeue a state record = legal; kill a window = not legal."*

This corrects the old "observer-only" framing, which was right for pure watchers but **wrong for a broker**.

### Who owns what
- **State** → Switchboard owns job-state (pool/claims/ownership/lifecycle). The floor owns `canonical/`/`research/`. Watchtower reads state and writes *verdict records only*.
- **Liveness/health** → AngelEye (session/hook level) + AppyRadar (machine/process/fleet level, read-only). Switchboard tracks *subscriber presence* for routing only.
- **Killing/reaping** → **Marshall is the only killer** (`tmux kill-window`); there is no killer-sentinel. AppyRadar and AngelEye only observe and answer; Switchboard requeues *state* but never touches the external world.
- **The view** → Watchtower (and only Watchtower) is the human surface.
- **Messaging** → Switchboard is the bus (SSE pub/sub + durable log). An in-session **Monitor** is the listen-side synapse.

### The read-vs-control principle (David, 2026-06-10) — the rule that keeps the sensors clean
- **Sensors read and make queryable; they do not act.** AngelEye reads Claude Code sessions/hooks → queryable. AppyRadar reads machine/process/tmux observations → queryable.
- **Communication and control live in Switchboard, Watchtower, or the floor agents** — not in the sensors.
- A sensor *may* host an action if it genuinely belongs there, but anything that **does** something (kill, delete, mutate) should go **through a proper control program** (Switchboard / Watchtower / floor), which may *call* a sensor if it makes sense for the action to live near the data.
- Corollary: a sensor emitting a *detection event* (`machine.offline`, `session.stale`, an `orphan_detected` signal) is still observe-and-tell — that's allowed. Acting on it is not the sensor's job. See `appyradar.md` §4.

### The one unifying mechanism ("four problems → one")
*Sentinel pushes topic-filtered SSE → an in-session Monitor (`persistent: true`) subscribes → it wakes Marshall or Swagger → the agent acts.* Durable write side + reactive listen side. This single pattern solves: external message wakes the factory (#15), Marshall auto-wake (C3c), result returns to David (#19), and process-watch alerts (#8).

---

## 5. Where the Symphony Spec fits

The Symphony Spec (`watchtower/symphony-spec.md`, from OpenAI, 2026-06-02) is an **external reference skeleton** — a headless daemon that polls Linear, runs a Codex subprocess per issue, and handles retries/reconciliation/stall-detection. It names **none** of our components.

Its role is **source material for the floor's coordination loop**, lifted piecemeal:
- **§8.5 stall-detection-by-timestamp** → the spec that justifies and shapes AngelEye ("last hook event timestamp" = liveness; "no events for N minutes" = stall; *never* read the process tree for this).
- **§7 claim states** (`Unclaimed → Claimed → Running → RetryQueued → Released`) → richer than today's thin file-registry; the model DF-7 promotes toward.
- **Retry-with-backoff** → a model the floor currently lacks (a stuck job just dies today).
- Its OPTIONAL dashboard (§13.4/§13.7) is *dropped* — Watchtower replaces it.

It feels holistic because it's a complete, self-consistent orchestrator design — but it's holistic about **the loop, not the constellation**.

---

## 6. The honest tensions (why it has felt incohesive)

These are real structural gaps, not just doc-sprawl:

1. **The "empty box" was a wrong name, not a missing app.** The older docs put a phantom "AppyCtrl" in the process/liveness slot. The real app is **AppyRadar**, which *exists* (PoC-validated 2026-04-27; live SSH collector). So the box isn't empty — it was mislabeled, and its true owner is a read-only fleet tool, not a killer. ⚠️ The ~10 backlog/spec docs that still say "AppyCtrl" now carry a wrong name and a wrong "kills processes" role — they need a sweep (see §7).
2. **Switchboard has identity drift.** It currently polls `ps`/processes (`poll-command`) — that's **AppyRadar's** domain (machine/process resource intelligence), accreted into Switchboard. Its README still calls it an "observer-only telemetry collector," contradicting its real broker identity.
3. **The stuck-case liveness owner is unsettled.** Marshall reaps its own windows; Switchboard requeues state; **nothing else kills**. The open question is which read-only sensor owns the *stuck-case* signal the reaper needs — AngelEye (session last-active) or AppyRadar (process/tmux state). Process-tree detection was already proven a dead end (claude reparents to its daemon).
4. **AngelEye offline blocks Switchboard's full design.** The staleness detector and DF-7's liveness-keyed reaping both run on wall-clock *fallbacks* because the real liveness source isn't there yet.

---

## 7. Implications for "what to do with Switchboard"

With the map in place, the Switchboard question narrows to three scoped moves:
- **Evict** the process-polling (`poll-command`/`process.snapshot`) toward **AppyRadar** (its rightful home — fleet/machine resource intelligence) — or consciously decide Switchboard hosts it until AppyRadar's Sentinel rebuild lands.
- **Fix the identity** — retire the "observer-only telemetry collector" framing in the README; state it as the communication + state plane.
- **Decide DF-7 timing** — build the state-plane (`job-state-store` + `job-coordinator`) now with wall-clock fallback, or wait for AngelEye to come online so liveness-keyed reaping is real on day one.

> **Source docs this map consolidates:** `north-star.md`, `backlog/2026-06-06-dark-factory-sentinel.md`, `watchtower/symphony-spec.md` + `watchtower/symphony-relook-2026-06-07.md` + `watchtower/watchtower-from-symphony.md`, `backlog/2026-06-09-switchboard-charter-grounding.md`, `backlog/specs/df7-switchboard-state-plane-spec.md`, `watchtower/reaper-brief.md`, `watchtower/DECISIONS.md`, `runtime-model.md`, `architecture.md`.
