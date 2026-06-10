# Spec — Switchboard State Plane (service-backed shared job-state)

**Ticket:** DF-7 · **Experiment:** exp-20260609-df7-state-plane · **Target app:** `~/dev/ad/apps/switchboard`
**Status:** SPEC ONLY — produces a document; builds nothing. The build is a later, separately-dispatched Ralphy-in-app leg.
**Author:** Swagger (appydave:spec-writer) · **Requested by:** Marshall · **Date:** 2026-06-09
**Coheres with:** DF-3 (`backlog/specs/stability-1-instrument-loop-spec.md`) — *observe the loop externally via Switchboard*. DF-7 is the **state home**; DF-3 is the **observability home**. They share one bus, must not duplicate.

---

## 1. Purpose

Move Dark Factory's **job work-state** off the factory floor's flat files and onto a **service-backed shared-state plane** so that Marshall instances become **thin, stateless clients** talking to **one stateful bus**. State home = **Switchboard** (job pool / claims / ownership), with **AngelEye** for liveness and **AppyRadar** (was "AppyCtrl" — corrected 2026-06-10, see docs/appyradar.md) for the dead-process *signal* (unbuilt) — **Marshall** does the actual reaping; AppyRadar only observes and answers — and **Watchtower** for the view.

This is the single capability that unlocks two things David wants at once: **parallel orchestration** (multiple Marshalls) and **factory portability** (operate on apps in any folder).

---

## 2. Problem Statement

Job state today lives in **flat files on the floor**: `experiments/watchtower-engine/{queue,running,done,reports}/`, claimed by an **atomic-rename mutex** (`bin/claim-next.sh` — `rename(2)` moves `queue/<id>.json` → `running/<id>.json`; exactly one racer wins). This is correct **for a single Marshall against a single folder on a single machine**, and it is the proven scaffold we are building **up from**, not throwing away.

It breaks for two goals:

1. **Parallel orchestration.** Multiple Marshall sessions cannot share work-state through a local folder. The naïve fix — clone the repo per Marshall and race a shared `running/` over git — is **fork/merge-hell** ("a disaster in normal programming" — David). We explicitly do **not** design that.
2. **Factory portability.** The floor's state lives *inside* `dark-factory/`. To run the factory against an app in another folder you must `cd` out and lose the engine. State tied to one working directory cannot follow the work.

Both have the **same root cause and the same fix**: job-state is *local and file-bound* when it needs to be a *shared service*. Make the state a service; make every Marshall a thin client of it. The claim mutex moves from `rename(2)` on a local folder to an **atomic claim-by-id over the network**, recording **who** claimed it (today's claim is anonymous — `claimed_by` is never recorded).

> **Critical placement note** (memories `constellation-first-placement`, `dark-factory-is-a-constellation-of-apps`): shared state (pool / claims / liveness) belongs in the **services**, and the floor is a **stateless client**. "Second orchestrator" means **N thin clients on 1 state plane**, NOT repo-cloning. This spec is the concrete realization of that rule.

---

## 3. Goals

1. **One stateful job-state plane.** A durable, service-backed home for the job pool, claims, ownership, and lifecycle timestamps — surviving a Switchboard restart.
2. **Atomic claim-by-id with recorded ownership.** Two clients can never double-claim; every claim records `claimed_by` and `claimed_at`. This is `claim-next.sh`'s `rename(2)` mutex, lifted into the service.
3. **Thin stateless clients.** The dark-factory engine (and future N Marshalls) talk to the plane over the **existing api-binding (HTTP)** and **mcp-binding (MCP)** — no client holds authoritative state.
4. **Portability.** Because state is a service, the factory can drive jobs for apps in **any** folder; the client carries no folder-bound state.
5. **Liveness-keyed reaping.** Orphan/stranded-claim recovery keys off **AngelEye liveness** ("is the claimant alive?"), not "a file landed in `done/`."
6. **Coexistence, not big-bang.** A migration path that lets flat-file mode and service mode run side-by-side until the service mode is proven.
7. **Build on Switchboard, do not rebuild it.** Add ~2 recipes in named planes, modeled on the working `staleness-detector`. Reuse the existing `/jobs` + `/health` surfaces.

---

## 4. Non-Goals

- **NOT repo-cloning** Marshalls and racing shared files over git. Explicitly rejected.
- **NOT rebuilding Switchboard.** It already exists (launchd `com.appydave.switchboard`, ports `:5099`/`:5100`, built on `@appydave/appysentinel-core`), already has `/jobs` POST + `/health` + a `queue/` dir + a working coordination recipe. We add recipes; we do not re-found the app.
- **NOT a new app.** The state plane is recipes inside Switchboard, not a new constellation member.
- **NOT the DF-3 telemetry layer.** DF-3 owns lifecycle observability (handback-rate, teardown-rate, durations). DF-7 owns *authoritative state*. They emit onto the same bus; DF-7 must not re-implement DF-3's metrics, and DF-3 must not own the claim mutex.
- **NOT building AppyRadar or AngelEye here.** DF-7 *integrates* AngelEye liveness; if AngelEye is offline, the reaper falls back to a wall-clock proxy (same pattern `staleness-detector` already uses).
- **NOT choosing the durable storage engine's on-disk format** beyond "survives restart, atomic writes." JSON-file-per-job (atomicWrite) is the recommended default; see Open Decision D1.

---

## 5. Background — what already exists (verified 2026-06-09)

Build **on** these. Files read before writing this spec:

| Artifact | What it is | Role for DF-7 |
|---|---|---|
| `appysentinel.json` | recipe manifest: `storage:[snapshot-store]`, `interface:[mcp-binding, api-binding]`, `transport:[sse-deliver]`, `coordination:[staleness-detector]` | DF-7 adds **one storage recipe** + **one coordination recipe** to this manifest |
| `src/access/bindings/api-binding.ts` | Hono server: `POST /jobs` persists `queue/<queue_id>.json` (durable-first), emits `job.queued`, fans out over SSE; `GET /health` | The **enqueue** surface already exists. DF-7 adds **claim/complete** surfaces alongside it |
| `src/coordination/staleness-detector.ts` | timer recipe, observer-only, emits `session.stale`; already TODOs "query AngelEye for `last_active`" | **THE MODEL** to copy for the coordination recipe (timer + emit + AngelEye integration shape) |
| `src/coordination/index.ts` | `// Wire coordination recipes here.` | Where the new coordination recipe registers |
| `src/storage/snapshot-store.ts` | storage recipe: subscribes to bus, overwrites one JSON via `atomicWrite`; "state kind → one overwriting snapshot" | The storage *pattern* to extend; snapshot is ephemeral/last-only — DF-7 needs **per-job durable records**, not one snapshot |
| dark-factory `bin/claim-next.sh` | `rename(2)` mutex over `queue/`→`running/`; anonymous claim | The **client** that becomes an API/MCP call; its semantics are the contract to preserve |
| dark-factory `bin/dispatch-swagger.sh`, `bin/reaper.sh` | dispatch + done-keyed window reaper | Reaper's "key off liveness not done/" is the DF-7 upgrade |
| DF-3 spec | "observe the loop externally via Switchboard" | Cohere — shared bus, no duplication |

**Key gap:** `/jobs` today only **enqueues** (durable write + wake). There is **no claim coordination and no ownership** in the service — claiming still happens via `rename(2)` on the floor. DF-7 fills exactly that gap.

---

## 6. Recipe Inventory (the build the PRD specifies)

Two new recipes, named, modeled on `staleness-detector` and `snapshot-store`. Registered in `appysentinel.json` and wired in `src/coordination/index.ts` / `src/storage/index.ts`.

### 6.1 `job-state-store` — **storage recipe** (Storage zone)
Durable per-job state, surviving restart. Unlike `snapshot-store` (one overwriting snapshot), this keeps **one record per job, keyed by `queue_id`**, updated through its lifecycle (`pool → claimed → running → done|failed`). Recommended substrate: one atomically-written JSON file per job under a `jobs/` dir (reuses `atomicWrite` from core — the same durability primitive `api-binding` already trusts). Exposes read/update primitives the coordination recipe calls. **Open Decision D1** covers file-per-job vs embedded KV (e.g. SQLite).

### 6.2 `job-coordinator` — **coordination recipe** (Coordination zone)
The mutex, lifted into the service. Modeled structurally on `staleness-detector` (a coordination recipe that owns logic and integrates AngelEye). Responsibilities:
- **Claim-by-id (atomic):** given `queue_id` + `claimant`, transition `pool → claimed` **iff** currently `pool`; record `claimed_by` + `claimed_at`. Atomicity is enforced *in the service* (single-writer serialization via core's serial queue, or compare-and-set on the store) — the network analogue of `rename(2)`.
- **Claim-next:** server-side "oldest unclaimed job," returning the claimed record — preserves `claim-next.sh`'s oldest-first semantics so the client call is a drop-in.
- **Complete/fail:** transition `running → done|failed`, stamp `ended_at`.
- **Reap (liveness-keyed):** on a timer, find `claimed`/`running` jobs whose `claimed_by` is **no longer alive per AngelEye**, and return them to `pool` (the service-side analogue of the floor reaper requeuing stranded `running/` entries). AngelEye-offline fallback: wall-clock grace, exactly as `staleness-detector` does today.
- **Emit lifecycle Signals** (`job.claimed`, `job.completed`, `job.failed`, `job.reaped`) onto the bus so SSE fan-out + DF-3 telemetry + Watchtower all observe state transitions **without owning state**.

> Both recipes are exposed through the **existing** `api-binding` (HTTP) and `mcp-binding` (MCP) — no new transport. Marshall talks to the plane as an **MCP tool**; scripts talk to it over HTTP.

---

## 7. Job-State Data Model

One record per job, keyed by `queue_id` (already the floor's filename key and the `/jobs` validation key — reuse it verbatim). Superset of today's flat ticket + the ownership fields the floor never recorded.

```json
{
  "queue_id": "q-20260609-example",
  "kind": "workflow | skill | instruction",
  "experiment_id": "exp-...",
  "prompt": "...",            // instruction/skill kinds
  "workflow": "...",          // workflow kind (harness name)
  "args": { },
  "state": "pool | claimed | running | done | failed",
  "claimed_by": "marshall-roamy-1718000000 | null",   // NEW — ownership, never recorded today
  "claimed_at": "<iso> | null",                        // NEW
  "started_at": "<iso> | null",
  "ended_at": "<iso> | null",
  "requested_by": "marshall",
  "requested_at": "<iso>",
  "result": { },              // terse outcome, mirrors reports/ handback
  "error": "<string> | null",
  "attempts": 0               // for future retry-with-backoff (Symphony §8.4); DF-7 records, does not act
}
```

State machine (single legal path per transition; coordinator enforces):
`pool → claimed → running → (done | failed)`; reaper edge: `claimed|running → pool` (when claimant is dead, increment `attempts`).

---

## 8. Claim-by-id + Ownership Contract (HTTP + MCP)

The contract every thin client uses. Same semantics over both surfaces; MCP wraps the HTTP verbs.

| Verb | HTTP (api-binding) | MCP tool | Semantics |
|---|---|---|---|
| Enqueue | `POST /jobs` *(exists)* | `job_enqueue` | Persist record in `state:pool`, emit `job.queued` |
| Claim next | `POST /jobs/claim` `{claimant}` | `job_claim_next` | Atomically claim oldest `pool` job → `claimed`, set `claimed_by`; return record or `204` if none. **Replaces `claim-next.sh`** |
| Claim by id | `POST /jobs/{id}/claim` `{claimant}` | `job_claim` | Claim a specific job iff `pool`; `409` if already claimed (the double-claim guard) |
| Start | `POST /jobs/{id}/start` | `job_start` | `claimed → running`, stamp `started_at` (claimant must match `claimed_by`) |
| Complete | `POST /jobs/{id}/complete` `{result}` | `job_complete` | `running → done`, stamp `ended_at`, store terse `result` (the reports/ handback, now service-side) |
| Fail | `POST /jobs/{id}/fail` `{error}` | `job_fail` | `running → failed`, store `error` |
| Read | `GET /jobs/{id}` / `GET /jobs?state=` | `job_get` / `job_list` | Read-only views for clients + Watchtower |

**Ownership rule:** every mutating verb after claim requires the caller's `claimant` to equal the record's `claimed_by`; mismatch → `409`. This is what makes "who owns this job" authoritative — the property the anonymous `rename(2)` claim could never give.

---

## 9. Liveness & Orphan Reaping (via AngelEye)

The floor reaper today keys off **`done/` mtime + grace** (process-tree detection is dead — Claude Code reparents to its daemon; see `proof/reaper-livefire-finding.md`). DF-7's coordinator reaper keys off **AngelEye liveness** instead:

- Query AngelEye (`GET :5051/.../liveness`, per the staleness-detector TODO) for each `claimed`/`running` job's `claimed_by`.
- **Claimant dead + job not terminal** → return job to `pool` (increment `attempts`), emit `job.reaped`. This recovers the exact "stranded `running/` entry from a dead listener" case the floor reaper recovers, but **centrally and process-independently**.
- **AngelEye offline** → fall back to wall-clock grace on `claimed_at`/`started_at` (the proven `staleness-detector` proxy). DETECT + TELL only for the *window*-killing half; the *state*-requeue half is safe to act on because it only moves a record back to `pool`.

> Division of labor stays inside the constellation rules: **Switchboard** requeues dead-claimant *state*; **AppyRadar** (unbuilt) provides the dead-*process* signal while **Marshall** does the actual reaping (`tmux kill-window`); **AngelEye** answers *who's alive*; **Watchtower** *shows* it. DF-7 wires the state half and consumes AngelEye; it does not build AppyRadar.

---

## 10. Thin-Client Contract (how the floor + N Marshalls connect)

The dark-factory engine becomes a **client** of the plane:

- **`claim-next.sh` → an API/MCP call.** Its body collapses to: `POST /jobs/claim {claimant}` (or `job_claim_next` MCP) → print the returned record. The `rename(2)` mutex is gone; the service owns atomicity. Same stdout contract (print claimed record / empty on none) so `run-next-workflow` step 1 is unchanged above the call.
- **`run-next-workflow` lifecycle** maps 1:1 onto the verbs: claim → `start` → execute → `complete`/`fail`. The `reports/` handback becomes the `result` on `complete` (service-side, durable — directly addressing DF-3's "the worker skips its own bookkeeping": the *coordinator* stamps terminal state even if the worker forgets, because the worker can't reach `done` without calling `complete`).
- **N Marshalls** each run their own thin client against the same `:5099`/`:5100`. No client holds state; the plane serializes claims. This is "N thin clients on 1 state plane."
- **Portability:** the client takes a `--target-app` / cwd argument that is just *job context* — the authoritative state lives in Switchboard, so the same client drives jobs for any folder.

---

## 11. Migration / Coexistence (no big-bang)

Four-step, reversible:

1. **Shadow.** Build `job-state-store` + `job-coordinator`; the floor keeps running `rename(2)`. The engine *additionally* mirrors each lifecycle event to the plane (write-through). Compare service state vs floor state — prove parity, no behavior change. (DF-3 telemetry already emits to Switchboard; reuse that bus.)
2. **Read-shadow.** `claim-next.sh` calls the service for the claim **but** still moves the floor file, asserting the service's choice matches the `rename(2)` winner. Catches divergence with the floor as ground truth.
3. **Cutover (flag).** A `WT_STATE_PLANE=service` env flag flips `claim-next.sh` to service-authoritative; floor dirs become a passive mirror (or stop being written). One Marshall first, then N. Flip back to `file` instantly if anything regresses.
4. **Retire floor state.** Once service mode is proven under parallel load, delete the floor claim path; `queue/done/` dirs become optional debug artifacts.

Each step is independently shippable and reversible — the DF-3 "instrument first, then change against evidence" discipline applies: don't cut over a step until its parity metric is green.

---

## 12. Decisions (ALL RULED — David, 2026-06-09)

- **D1: Durable substrate — RESOLVED ✅** = **file-per-job JSON via `atomicWrite`** (matches `api-binding`'s existing durability primitive, zero new deps, greppable, floor-parity). Revisit only if job volume makes directory scans slow.
- **D2: Claimant identity scheme — RESOLVED ✅** = **adopt AngelEye's session-id as `claimed_by` directly** (single identity namespace; ownership + liveness both key off it). ⚠️ contingent on AngelEye exposing a stable session-id — verify before build.
- **D3: MCP vs HTTP primary path — RESOLVED ✅** = **MCP-first for Marshall** (rides the existing mcp-binding), **HTTP retained for shell clients** (`claim-next.sh`).
- **D4: Reaper authority over state requeue — RESOLVED ✅** = the `job-coordinator` **MAY requeue a dead-claimant's state record** `claimed→pool` (this is broker CRUD over Switchboard's OWN comms/queue domain — NOT a violation; Switchboard is the durable write-side/broker, not read-only). It **never** mutates the external observed system (kill a process / `tmux kill-window`) — that stays Marshall's Monitor (the only killer); AppyRadar only observes process state and answers/emits, it never kills. (Corrects the earlier "observer-only" framing.)
- **D5: Retry-with-backoff ownership — RESOLVED ✅** = **coordinator records `attempts`; client owns retry policy** for now (Symphony §8.4 stays on the floor). Revisit once N-Marshall is live.

---

## 13. Acceptance Criteria

1. `appysentinel.json` lists `job-state-store` (storage) and `job-coordinator` (coordination); both wired in their `index.ts` and start cleanly under launchd.
2. **No double-claim:** a concurrency test (model on dark-factory `bin/test-atomic-claim.sh`, 200×8) shows every job claimed **exactly once** across N concurrent clients over HTTP **and** MCP, with `claimed_by` recorded on each.
3. **Survives restart:** claimed/running jobs and their ownership persist across a Switchboard restart (durable store).
4. **Liveness reaping:** a job whose `claimed_by` is dead-per-AngelEye returns to `pool` with `attempts` incremented and a `job.reaped` Signal emitted; AngelEye-offline falls back to wall-clock grace.
5. **Thin-client parity:** `claim-next.sh` in `WT_STATE_PLANE=service` mode produces the same claim ordering (oldest-first) and stdout contract as the `rename(2)` version, proven in read-shadow (step 2).
6. **Ownership enforcement:** a `start`/`complete`/`fail` from a non-owner `claimant` is rejected (`409`).
7. **Coexistence:** the system runs correctly in `file` mode and `service` mode, switchable by env flag, reversible with no data loss.
8. **No duplication with DF-3:** lifecycle Signals are emitted once, on the shared bus; DF-3 telemetry consumes them without DF-7 re-implementing metrics.
9. **Portability:** a job targeting an app outside `dark-factory/` is claimed, run, and completed through the plane with no floor-local state.

---

## 14. Build-via Note

Built **in-app via Ralphy**, inside the `switchboard` repo (recipes are added to Switchboard, not authored here). This spec is authored in dark-factory (`backlog/specs/`) per the constellation rule that **Marshall authors requirements here**; the in-app Ralphy build leg copies it into `switchboard/docs/requirements/` and executes against the live recipe scaffold. Recommended build order mirrors the migration: storage recipe → coordinator (claim-by-id) → MCP/HTTP verbs → liveness reaping → shadow/cutover. Each recipe modeled on the working `staleness-detector` / `snapshot-store` — copy their shape, do not invent a new recipe pattern.

---

*Stack-agnostic where the concept allows; Switchboard/AppySentinel specifics are intentional — the target system **is** Switchboard.*
