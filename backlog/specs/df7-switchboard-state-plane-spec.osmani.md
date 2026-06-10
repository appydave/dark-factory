# Spec: Switchboard State Plane (DF-7)

> **Method:** Osmani `spec-driven-development` (`/agent-skills:spec`) structure — Objective · Tech Stack · Commands · Project Structure · Code Style · Testing Strategy · Boundaries (Always/Ask-first/Never) · Success Criteria · Open Questions, run through its **gated SPECIFY→PLAN→TASKS→IMPLEMENT** workflow.
> **Input answers:** the appydave:spec-writer baseline `df7-switchboard-state-plane-spec.md` (treated as pre-filled interview answers; NOT re-interviewed).
> **Target app:** `~/dev/ad/apps/switchboard` (AppySentinel recipe-app). **Status:** SPEC ONLY — produces a document; builds nothing. Build is a later Ralphy-in-app leg.
> **Ticket:** DF-7 · **exp:** exp-20260609-df7-state-plane · **Author:** Swagger (Osmani pass) · **Date:** 2026-06-09

---

## Objective

**What & why.** Move Dark Factory's **job work-state** off the factory floor's flat files (`experiments/watchtower-engine/{queue,running,done,reports}/`) onto a **service-backed shared-state plane inside Switchboard**, so every Marshall becomes a **thin, stateless client** of **one stateful broker**. This single capability unlocks two things David wants at once: **parallel orchestration** (N Marshalls) and **factory portability** (drive apps in any folder).

**User.** The dark-factory engine (`run-next-workflow`, `claim-next.sh`) and N future Marshall sessions — they are the *clients*. The human stakeholder is David (constellation owner).

**Success looks like.** A claim is atomic over the network, records *who* claimed it, survives a Switchboard restart, and a dead claimant's job returns to the pool automatically — with the floor's `rename(2)` semantics preserved exactly so the cutover is a drop-in. (Concrete, testable conditions in **Success Criteria**.)

**Root cause being fixed.** Job-state is *local and file-bound* when it must be a *shared service*. The naïve alternative — clone the repo per Marshall and race a shared `running/` over git — is fork/merge-hell and is **explicitly rejected** (Non-Goal). "Second orchestrator" = **N thin clients on 1 state plane**, NOT repo-cloning (memories `constellation-first-placement`, `dark-factory-is-a-constellation-of-apps`).

**Coheres with DF-3** (`stability-1-instrument-loop-spec.md`): DF-7 is the **state home**; DF-3 is the **observability home**. One shared bus, no duplication.

---

## Tech Stack (grounded — files read 2026-06-09)

| Layer | Concrete fact (verified in `~/dev/ad/apps/switchboard`) | Provenance |
|---|---|---|
| Runtime | AppySentinel recipe-app on `@appydave/appysentinel-core@0.1.0`, launchd `com.appydave.switchboard`, ports `:5099`/`:5100` | `appysentinel.json`, baseline §5 |
| Recipe manifest | `input:[poll-command]`, `storage:[snapshot-store]`, `interface:[mcp-binding, api-binding]`, `transport:[sse-deliver]`, `runtime:[register-as-launchd]`, `coordination:[staleness-detector]` | `appysentinel.json` (read verbatim) |
| Enqueue surface | `api-binding.ts` — Hono server: `POST /jobs {queue_id,kind,prompt?,workflow?,args?}` **durably writes** `queue/<queue_id>.json` via `atomicWrite` BEFORE emitting `job.queued`; `GET /health`. CQRS-lite Command side; binds `127.0.0.1` (observer-only posture). Validates `queue_id` (rejects path separators / `..`). | `src/access/bindings/api-binding.ts` (read verbatim) |
| Coordination model | `staleness-detector.ts` — timer coordination recipe (default 30s), **observer-only**, EMITs `session.stale`, never kills; TODO(v2) = query AngelEye `last_active`; wall-clock proxy because AngelEye offline today | `src/coordination/staleness-detector.ts` (read verbatim) |
| Storage model | `snapshot-store` — subscribes to bus, overwrites **one** JSON via `atomicWrite` ("state kind → one overwriting snapshot"); ephemeral/last-only | baseline §5 |
| Floor contract | `bin/claim-next.sh` — `rename(2)` mutex `queue/→running/`, **anonymous** claim (`claimed_by` never recorded); `bin/{dispatch-swagger,reaper}.sh` | dark-factory engine |

**Key gap DF-7 fills:** `/jobs` today only **enqueues** (durable write + wake). There is **no claim coordination and no ownership** in the service — claiming still happens via `rename(2)` on the floor. DF-7 adds exactly: a durable per-job **storage** recipe + a claim-arbitration **coordination** recipe modeled on `staleness-detector`, exposed through the **existing** api-binding (HTTP) + mcp-binding (MCP). No new app, no new transport.

---

## Commands

*(Switchboard repo — confirm against its `package.json` during the Ralphy build leg; **Ask-first** boundary applies.)*

```
Build:   npm run build         # tsc → dist/
Test:    npm test              # recipe unit + integration
Lint:    npm run lint          # eslint
Restart: launchctl kickstart -k gui/$(id -u)/com.appydave.switchboard
Health:  curl -s localhost:5099/health
Concurrency proof (claim mutex):  bash bin/test-state-plane-claim.sh   # NEW — modeled on dark-factory bin/test-atomic-claim.sh (200×8)
```

---

## Project Structure (where the new recipes land in Switchboard)

```
src/storage/job-state-store.ts        → NEW storage recipe — durable per-job records, keyed by queue_id
src/storage/index.ts                  → register job-state-store (currently wires snapshot-store)
src/coordination/job-coordinator.ts   → NEW coordination recipe — claim/start/complete/fail/reap (the lifted mutex)
src/coordination/index.ts             → register job-coordinator (`// Wire coordination recipes here.`)
src/access/bindings/api-binding.ts    → EXTEND — add /jobs/claim, /jobs/{id}/{claim,start,complete,fail}, GET /jobs[/{id}]
appysentinel.json                     → add "job-state-store" (storage) + "job-coordinator" (coordination)
jobs/<queue_id>.json                  → NEW runtime dir — one durable record per job (gitignored, like queue/)
docs/requirements/df7-state-plane.md  → the Ralphy build copies THIS spec here
```

Authored in dark-factory `backlog/specs/` (constellation rule: **Marshall authors requirements here**); the in-app Ralphy leg copies it into `switchboard/docs/requirements/` and builds against the live scaffold.

---

## Code Style (copy the working recipe shape — do not invent a new pattern)

Both new recipes mirror `staleness-detector` (coordination: timer + emit + AngelEye integration shape) and `snapshot-store` (storage: subscribe + `atomicWrite`). One real shape, abbreviated:

```ts
// job-coordinator.ts — coordination recipe. Owns the claim mutex IN the service.
// Atomicity = single-writer serialization via core's serial queue (the network
// analogue of rename(2)); compare-and-set on the store guards every transition.
export interface JobCoordinatorOptions {
  reapIntervalMs?: number;   // default 30_000 — same cadence as staleness-detector
  graceMinutes?: number;     // AngelEye-offline wall-clock fallback (proven proxy)
}
export function jobCoordinator(s: Sentinel, opts: JobCoordinatorOptions = {}) {
  // claim(queue_id, claimant): pool → claimed IFF state===pool; stamp claimed_by/at; else 409
  // claimNext(claimant): oldest pool job → claimed (preserves claim-next.sh oldest-first)
  // start/complete/fail(queue_id, claimant): ownership-checked transition; mismatch → 409
  // reap(): on timer — claimed|running whose claimed_by is dead-per-AngelEye → pool, attempts++, emit job.reaped
  // every transition EMITs a Signal (job.claimed|started|completed|failed|reaped) onto the existing bus
}
```

**Data model — one record per job, keyed by `queue_id`** (the floor's filename key and `/jobs` validation key, reused verbatim). Superset of today's ticket + the ownership fields the floor never recorded:

```json
{
  "queue_id": "q-20260609-example", "kind": "workflow|skill|instruction",
  "experiment_id": "exp-...", "prompt": "...", "workflow": "...", "args": {},
  "state": "pool|claimed|running|done|failed",
  "claimed_by": "marshall-roamy-1718000000 | null",   // NEW — ownership
  "claimed_at": "<iso>|null", "started_at": "<iso>|null", "ended_at": "<iso>|null",
  "requested_by": "marshall", "requested_at": "<iso>",
  "result": {}, "error": "<string>|null", "attempts": 0
}
```

State machine (coordinator enforces single legal path): `pool → claimed → running → (done|failed)`; reaper edge `claimed|running → pool` (claimant dead, `attempts++`).

**Claim-by-id + ownership contract** (same semantics over HTTP + MCP; MCP wraps the HTTP verbs):

| Verb | HTTP | MCP tool | Semantics |
|---|---|---|---|
| Enqueue | `POST /jobs` *(exists)* | `job_enqueue` | persist `state:pool`, emit `job.queued` |
| Claim next | `POST /jobs/claim {claimant}` | `job_claim_next` | atomically claim oldest `pool` → `claimed`; record `claimed_by`; record or `204`. **Replaces `claim-next.sh`** |
| Claim by id | `POST /jobs/{id}/claim {claimant}` | `job_claim` | claim iff `pool`; `409` if already claimed (double-claim guard) |
| Start | `POST /jobs/{id}/start` | `job_start` | `claimed→running`, stamp `started_at` (claimant==`claimed_by`) |
| Complete | `POST /jobs/{id}/complete {result}` | `job_complete` | `running→done`, stamp `ended_at`, store terse `result` (= the reports/ handback, service-side) |
| Fail | `POST /jobs/{id}/fail {error}` | `job_fail` | `running→failed`, store `error` |
| Read | `GET /jobs/{id}` / `GET /jobs?state=` | `job_get`/`job_list` | read-only views for clients + Watchtower |

**Ownership rule:** every mutating verb after claim requires caller `claimant == claimed_by`; mismatch → `409`. This is the authoritative "who owns this job" the anonymous `rename(2)` claim could never give.

---

## Testing Strategy

| Concern | Level | Where / how |
|---|---|---|
| No double-claim under concurrency | Integration (the load-bearing test) | `bin/test-state-plane-claim.sh`, **modeled on dark-factory `bin/test-atomic-claim.sh` (200×8)** — every job claimed exactly once across N concurrent clients over **both** HTTP and MCP, `claimed_by` recorded |
| State machine transitions | Unit | per-transition: legal path passes, illegal transition → `409`; ownership mismatch → `409` |
| Durable survival | Integration | claimed/running jobs + ownership persist across a `launchctl kickstart` restart |
| Liveness reaping | Integration | dead-per-AngelEye `claimed_by` → job back to `pool`, `attempts++`, `job.reaped` emitted; AngelEye-offline → wall-clock grace fires |
| Thin-client parity | Integration (read-shadow) | `claim-next.sh` in `WT_STATE_PLANE=service` mode reproduces oldest-first ordering + stdout contract vs `rename(2)` |
| No DF-3 duplication | Assertion | lifecycle Signals emitted once on the shared bus; DF-3 consumes without DF-7 re-implementing metrics |

Each recipe lands with its tests before cutover; **no cutover step ships until its parity metric is green** (DF-3 "instrument first, change against evidence" discipline).

---

## Boundaries

**Always do**
- Model new recipes on the **working** `staleness-detector` / `snapshot-store` shape — copy, don't invent.
- Reuse `atomicWrite` (core's existing durability primitive) and the existing `queue_id` key.
- Emit every state transition as a Signal on the **existing** bus (SSE fan-out + DF-3 + Watchtower all observe without owning state).
- Keep flat-file mode and service mode **switchable by env flag**, reversible with no data loss.
- Run the concurrency proof before declaring the mutex correct.

**Ask first (David)**
- **D1 — Durable substrate.** Recommend **file-per-job JSON via `atomicWrite`** (matches api-binding's primitive, zero new deps, greppable, parity-comparable). Alt: embedded SQLite (better at high volume, new dep, less greppable). *Start file-per-job; revisit only if directory scans get slow.* **STILL OPEN.**
- **D2 — Claimant identity scheme.** Recommend `claimed_by = "<role>-<machine>-<epoch>"` (e.g. `marshall-roamy-1718000000`). *Adopt AngelEye's session-id directly as `claimed_by` if one exists, to avoid a second identity namespace.* **STILL OPEN — depends on AngelEye session identity.**
- **D3 — MCP vs HTTP as Marshall's primary path.** Both specified. Recommend **MCP-first for Marshall** (already speaks MCP; ergonomics + auth ride mcp-binding), **HTTP for shell clients** (`claim-next.sh`). **STILL OPEN.**
- **D5 — Retry-with-backoff ownership.** DF-7 *records* `attempts`, does not act. Symphony §8.4 retry exists on the floor. Recommend **coordinator records attempts; client owns retry policy for now** — revisit once N-Marshall is live. **STILL OPEN.**
- Confirming Switchboard's real `package.json` script names before the build leg trusts the Commands block.

**Never do**
- **NOT repo-clone Marshalls** and race shared files over git (fork/merge-hell — rejected).
- **NOT rebuild Switchboard** or found a new app — DF-7 is *recipes inside Switchboard*.
- **NOT re-implement DF-3's telemetry** — DF-7 owns authoritative state; DF-3 owns lifecycle metrics; one bus.
- **NOT build AppyRadar (was "AppyCtrl" — corrected 2026-06-10, see docs/appyradar.md) or AngelEye here** — DF-7 *integrates* AngelEye liveness; offline → wall-clock proxy.
- **NEVER mutate the external observed system** from Switchboard — no process kill, no `tmux kill-window`, no touching watched files. (See D4-RESOLVED for the precise line.)

---

## D4 — RESOLVED 2026-06-09 (David). Reaper authority over state requeue.

The baseline asked, as an *open* question: *"does coordinator-requeues-state violate Switchboard's observer-only stance?"* **It does not — RESOLVED YES, the coordinator MAY requeue state.**

**Resolution (verbatim intent):** Switchboard is a **SWITCHBOARD** — the broker / durable write-side that **OWNS the queue**. It is **CRUD over its own comms domain**: the queue, the job-state records, **requeueing a dead-claimant's record `claimed → pool`**, routing, and the event log. Mutating its *own* state is its job, not a violation.

The `staleness-detector` **"never kills"** rule is **narrow**: never mutate the **external observed system** — kill a process, `tmux kill-window`, touch watched files. Those stay with **Marshall's Monitor** (the only killer); AppyRadar is read-only and never kills — it only observes process/window state and emits a Signal. So:

- ✅ `job-coordinator` requeues dead-claimant **state** (`claimed|running → pool`, `attempts++`, emit `job.reaped`) — this is broker CRUD over Switchboard's own domain.
- ❌ Killing the orphaned window / dead process stays **Marshall** (the only killer; AppyRadar only DETECTs+TELLs — observes process state and emits a Signal, never kills) — Switchboard too only DETECTs+TELLs there (emits a Signal), exactly as `staleness-detector` does for `session.stale`.

Division of labor (unchanged constellation rule): **Switchboard** requeues dead-claimant *state*; **AppyRadar** (unbuilt) provides the dead-*process* signal while **Marshall** does the actual reaping (`tmux kill-window`); **AngelEye** answers *who's alive*; **Watchtower** *shows* it.

---

## Success Criteria

1. `appysentinel.json` lists `job-state-store` (storage) + `job-coordinator` (coordination); both wired in their `index.ts`; start cleanly under launchd.
2. **No double-claim** — concurrency test (200×8, both HTTP and MCP) shows every job claimed exactly once with `claimed_by` recorded.
3. **Survives restart** — claimed/running jobs + ownership persist across a Switchboard restart.
4. **Liveness reaping** — dead-per-AngelEye `claimed_by` → job to `pool`, `attempts++`, `job.reaped` Signal; AngelEye-offline → wall-clock grace.
5. **Thin-client parity** — `claim-next.sh` in `service` mode matches oldest-first ordering + stdout contract vs `rename(2)`, proven in read-shadow.
6. **Ownership enforcement** — `start`/`complete`/`fail` from a non-owner `claimant` → `409`.
7. **Coexistence** — correct in both `file` and `service` mode, env-switchable, reversible, no data loss.
8. **No DF-3 duplication** — lifecycle Signals emitted once on the shared bus; DF-3 consumes without re-implementing.
9. **Portability** — a job targeting an app outside `dark-factory/` is claimed, run, completed through the plane with no floor-local state.

---

## Plan → Tasks (Osmani PLAN/TASKS phases — the build leg, gated)

Migration *is* the plan; each step independently shippable and reversible.

- [ ] **T1 — `job-state-store`** (storage recipe). Acceptance: durable per-job record CRUD keyed by `queue_id` survives restart. Verify: restart test. Files: `src/storage/{job-state-store,index}.ts`, `appysentinel.json`.
- [ ] **T2 — `job-coordinator` claim-by-id** (coordination recipe). Acceptance: atomic `pool→claimed` with `claimed_by`; double-claim → `409`. Verify: 200×8 concurrency test. Files: `src/coordination/{job-coordinator,index}.ts`.
- [ ] **T3 — MCP/HTTP verbs**. Acceptance: full verb table live on both bindings, ownership-checked. Verify: per-verb integration + `409` on non-owner. Files: `src/access/bindings/api-binding.ts` (+ mcp-binding wiring).
- [ ] **T4 — Liveness reaping**. Acceptance: dead claimant requeued, `job.reaped` emitted; AngelEye-offline fallback. Verify: liveness integration test. Files: `src/coordination/job-coordinator.ts`.
- [ ] **T5 — Shadow → Read-shadow → Cutover(flag) → Retire floor** (baseline §11). Acceptance: parity green at each gate; `WT_STATE_PLANE` flips one Marshall then N; instant rollback to `file`. Verify: parity metric per step. Files: dark-factory `bin/claim-next.sh`.

**Gate:** do not advance a phase until its parity/verify metric is green and (for D1/D2/D3/D5) the Ask-first decision is made.

---

## Open Questions (carried forward — NOT resolved here)

- **D1** durable substrate · **D2** claimant identity scheme · **D3** MCP-vs-HTTP primary path · **D5** retry-with-backoff ownership.
- **D4 is RESOLVED** (above) and removed from this list.
- **4 decisions still open.**

---

*Provenance: target system **is** Switchboard — Switchboard/AppySentinel specifics are intentional, not a stack-agnostic defect. All §"Tech Stack" facts read verbatim from the live repo 2026-06-09. Baseline answers from `df7-switchboard-state-plane-spec.md` (appydave:spec-writer).*
