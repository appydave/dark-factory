# Switchboard Greenfield Charter — Consolidated Grounding

> **What this is:** the phase-1 grounding for the Switchboard greenfield charter, per `2026-06-09-switchboard-greenfield-KICKOFF.md`. Produced by batch-mining the 7 switchboard build-cluster transcripts (via `abridge`, greenfield lens) + reading the design-origin docs directly. Net-new findings deduped against the seed (`…greenfield-seed.md`) + memories. **This is the INPUT to `/agent-skills:spec`, not the charter.** The 15MB design-origin transcript (`627e86a2`) was deferred — the cluster + design-origin docs gave enough; escalate only if the interview needs more.
>
> **Sources mined:** 7 build transcripts (`b9153637`, `992e121b`, `0d7ebe05`, `5d7e5dfe`, `0cc44f83`, `6396f590`, `74659a99`); design-origin docs read directly: `backlog/2026-06-06-dark-factory-sentinel.md`, memory `watchtower-sentinel-bus-direction`, memory `dark-factory-is-a-constellation-of-apps`, memory `constellation-first-placement`. DF-7 spec + seed already in hand.

---

## A. The headline: this is a CONFIRM/CHALLENGE charter, not a blank-slate one

The seed framed Switchboard as "never designed — pure accretion, 5 reactive `feat:` commits, no charter." **That's true of the CODE's growth, but NOT of the design thinking.** Mining the design-origin docs surfaced a substantial, coherent prior design — David's 2026-06-06 framing — that the seed's "7 open questions" mostly under-counted as fully-open. The richest single identity source is the memory `watchtower-sentinel-bus-direction` (David's final framing), which is richer than all 7 build transcripts combined.

So the charter's real job: **lift the scattered 2026-06-06 design into one end-state-backward document, CONFIRM the rulings David already made, and CHALLENGE the few genuine gaps** — not interview from zero. The build transcripts add the *architecture-discovered-while-building* (durability split, MCP-stdio constraint, bus-is-wake), which the design docs didn't have.

---

## B. Convergent findings (all 7 mines + design docs agree)

### Identity (well-defined, not open)
- **Switchboard IS THE COMMUNICATION LAYER** (David's final framing, 2026-06-06, memory `watchtower-sentinel-bus-direction`). It owns **both** (a) the messages — send Marshall→Swagger, route between, carry results back (SSE deliver + Monitor synapse + queue) — **and** (b) the *awareness of communication*: "knowing whether someone is talking to it / watching / listening / alive is itself part of communication." **Liveness-for-routing is CORE, not bolted-on telemetry.**
- Earlier framings ("resource telemetry sentinel" / "router's fleet view" / "messaging bus + observability payload" / "observer-only") all **under-stated it** and are explicitly superseded. The README still says "observer-only telemetry collector" — that's stale scaffold boilerplate, a framing defect to fix.
- It is an **AppySentinel instance** (template at `~/dev/ad/apps/appysentinal/`), per-machine, always-on daemon, **never runs `claude`**. Three physically-separate planes: floor = `dark-factory` · control plane = **Watchtower** (AppyStack instance) · comms bus = **Switchboard** (AppySentinel instance).

### Bounded responsibility (lines drawn)
- **MAY** CRUD its own comms/queue/state domain (enqueue, claim, complete, fail, requeue a dead-claimant's record `claimed→pool`) — broker CRUD. **NEVER** mutates the external observed world (kill a process, close a window). The "observer-only" framing was **wrong for a broker** and David corrected it (D4). "Requeue a state record = legal; kill a window = not legal."
- **NOT** resource/process health → **AppyRadar** (was "AppyCtrl" — corrected 2026-06-10, see docs/appyradar.md) (David already built a PoC months ago; under-used; needs its own investigation window). **NOT** session/hook telemetry → **AngelEye**. **NOT** the killer → Marshall's Monitor (the only killer; AppyRadar is read-only and never kills). **NOT** the viz → Watchtower.
- Only **deep resource telemetry (RAM/CPU)** is genuinely peripheral — it MAY ride the bus as a payload but isn't Switchboard's identity. The current `poll-command`/`process.snapshot` collecting ps tables is **AppyRadar's turf living in Switchboard by accretion** — flagged in commit `d1506ba` as "resource-health belongs to AppyRadar." Charter must decide: strip it out, or keep Switchboard as the bus AppyRadar reports into.

### Core architecture (proven in code)
- **Bus = the WAKE; file = the exactly-once source of truth.** SSE is broadcast/replay, NOT exactly-once. `POST /jobs` writes `queue/<id>.json` (atomicWrite) **durable-first**, THEN emits the `job.queued` wake. Duplicate/replayed wakes are harmless. The atomic-claim mutex (`rename(2)`, `claim-next.sh`) is what gives exactly-once.
- **Durable vs ephemeral is a first-class split** (learned the hard way — `process.snapshot` at ~140KB/15s bloated the log to **31MB/hour**). Durable topics (`job.*`, `session.*`, `alert.*`) → logged + replayed on reconnect via `Last-Event-ID`. Ephemeral telemetry (`process.snapshot`) → live-push only, never persisted. `maxLogEntries` pruning backstop bounds even durable growth to the replay window.
- **Addressing = topic subscription, not folders.** Subscriber declares topics at connect (`?subscribe=marshall,broadcast`); broker filters server-side. Multi-Marshall / multi-Sentinel fall out free. (David's call — beats folder-per-channel.)
- **MCP binding is a standalone stdio entry point**, deliberately NOT wired into `main.ts` — stdio collides with the always-on Pino logging loop. Any future MCP-exposed recipe inherits this constraint.
- **`staleness-detector` is THE MODEL recipe** for all future coordination recipes: detect + tell, never act. Emits `session.stale`; an external reaper/operator acts. New `job-coordinator` (DF-7) goes in the same `coordination/` zone, modeled on it.

### Message surface today (built)
`job.queued` (durable) · `session.stale` (durable) · `process.snapshot` (ephemeral) · `sentinel.started` (lifecycle). Envelope: `{id(ulid), ts, schema_version, source, machine, sentinel_id, kind∈[log|metric|event|state|span], name, severity?, attributes?, payload}`. `alert.*` namespace is reserved in the durable predicate but **no recipe emits it yet**.

### State model (DF-7, all 5 decisions ruled, NOT yet built)
State machine `pool → claimed → running → done|failed`; reaper edge `claimed|running → pool` (increment `attempts`). D1 file-per-job JSON via `atomicWrite` · D2 `claimed_by` = AngelEye session-id · D3 MCP-first for Marshall / HTTP for scripts · D4 coordinator requeues state (broker CRUD, never kills) · D5 coordinator records `attempts`, client owns retry. **Current gap:** `/jobs` only enqueues; claiming is still floor-side `rename(2)`. DF-7 adds `job-state-store` + `job-coordinator` to fill it.

### Build method (the live contradiction)
Switchboard was built via `create-appysentinel` scaffold + **dark-factory Swagger through the loop** (5 feat commits), **NOT Ralphy** — but memory `ralphy-plugin-builds-apps` says constellation apps → Ralphy (AngelEye was). DF-7's `build_via` was corrected this session to flag this. Genuinely unresolved; the charter pass (Osmani-as-author) may itself reveal the right method.

---

## C. The 7 "open questions" — REFRAMED with prior thinking found

The interview should treat these as **confirm-or-revise**, not blank. Marked: 🟢 largely ruled (confirm) · 🟡 partial (resolve the delta) · 🔴 genuinely open.

| # | Question | Prior ruling found | What's actually left for the interview |
|---|----------|-------------------|----------------------------------------|
| 1 | Full message-type surface | 🟡 4 built + 4 DF-7 lifecycle (`job.claimed/completed/failed/reaped`); `alert.*` reserved-unused | What SHOULD a *designed* bus emit? Marshall↔Swagger comms topics? `david` digest topic? broadcast? Is the surface job-centric only, or general agent-comms? |
| 2 | Multi-machine / N-Marshall federation | 🟡 **Per-machine Switchboard, NOT one-across-Tailscale — already ruled** ("every machine that runs agents needs its OWN, daemonized"). Addressing = topic-sub. | The genuine gap: do N Marshalls on ONE machine share that machine's Switchboard (yes, implied) — and is there ANY cross-machine job federation (Roamy↔M4 Mini), or are machines fully independent planes? How does a client discover/reach the right one? |
| 3 | Event-log retention | 🟡 Durable (`job.*`/`session.*`) replay-bounded by `maxLogEntries`; telemetry buffer "SHORT (~1 min / 4×15s)". | Confirm: differentiated by data-class (not one policy). Open: is there ANY long-term/audit retention, or is everything replay-window-only? Does the durable message log need permanence for the build-documentary/chronicle? |
| 4 | Relationship to DF-3 without duplication | 🟢 Ruled: DF-3 = lifecycle *observability* (rates/durations/metrics), Switchboard = authoritative *state*; same bus; DF-7 must not re-implement DF-3 metrics, DF-3 must not own the claim mutex. | Confirm the line. Articulate exactly: Switchboard EMITS lifecycle Signals; DF-3 DERIVES metrics from them. Does DF-3 live IN Switchboard or as a consumer? (Leaning consumer.) |
| 5 | How much accreted bus reshapes | 🟡 Recipes mostly sound; known reshape: strip resource-health (poll-command/snapshot) toward AppyRadar; rename `api-binding` if it grows past ingest; README reframe. | Confirm the keep/reshape list. Is `coordination/` (emergent 4th zone) canonical? Does the 2-port split (5099 SSE / 5100 ingest) stay? |
| 6 | "Factory builds the apps" doctrine | 🔴 **Genuinely open.** Switchboard=Swagger-loop; AngelEye=Ralphy. Contradiction named, not resolved. | Which is right for greenfield constellation apps — and does THIS charter's authoring method (Osmani spec) become the front-end to either? |
| 7 | Scope of "awareness of communication" (smart vs dumb bus) | 🟡 Ruled CORE: liveness/presence/reachability IS Switchboard's identity (not a dumb pipe). `/health` already tracks `subscribers`. | The finer cut: does it check a target is alive *before* routing (smart delivery), or just route + let liveness be a separate queryable fact? How deep does "is this Swagger alive" go before it's AngelEye/AppyRadar's job? |

---

## D. Sharp interview agenda for David (for `/agent-skills:spec`)

Lead questions, ordered by leverage. Each is confirm-or-revise against the prior ruling above — not blank.

1. **Identity confirm** — "Switchboard = THE COMMUNICATION LAYER (messages + awareness-of-communication; liveness-for-routing is core). Still the one-liner? Anything to sharpen?"
2. **Q6 build method** — the genuine fork. Swagger-loop vs Ralphy for greenfield apps; does the Osmani-spec front-end fit?
3. **Q1 message surface** — is the bus job-centric, or the general agent-comms fabric (Marshall↔Swagger↔david topics)? This sizes everything.
4. **Q2 federation delta** — cross-machine job sharing yes/no? (Per-machine instance already ruled.)
5. **Q5 resource-health eviction** — strip `poll-command`/`process.snapshot` out to AppyRadar now, or keep Switchboard as the bus AppyRadar reports into?
6. **Q7 smart-vs-dumb delta** — check-alive-before-route, or route-and-query-separately?
7. **Q3 retention** — replay-window-only, or any permanent/audit tier (chronicle)?
8. **Q4 DF-3 line** — confirm Switchboard emits / DF-3 derives, DF-3 as consumer not embedded.
9. **DF-7 re-evaluation** — after the above: is the state-plane (job-state-store + job-coordinator) still the right NEXT slice, as-specified?

---

## E. Deferred / available-on-demand
- `docs/watchtower/symphony-spec.md` (80KB) — the job/claim/state model's origin; DF-7 already distilled its state machine + the agents covered it. Pull in if the interview needs the formal coordination semantics (port state machine, retry §8.4).
- 15MB design-origin transcript `627e86a2` — escalate only if identity/federation questions stay thin after the interview (they're now well-grounded).
