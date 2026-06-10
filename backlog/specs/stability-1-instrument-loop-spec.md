# Spec — Instrument-then-Harden the Dark Factory Dispatch Loop

**Ticket:** DF-3 · **Experiment:** exp-20260608-stability1 · **Lane:** A (Dispatch loop) + B (Observability)
**Status:** SPEC ONLY — no build. Building is a later, separately-dispatched job.
**Author:** Swagger (spec-writer) · **Requested by:** Marshall · **Date:** 2026-06-08

---

## 1. Purpose

Give the Dark Factory dispatch loop **factory-operations telemetry**: a reliable, external record of every job's lifecycle so we can answer "what works, what doesn't, and how often" with numbers instead of anecdote — and then harden the loop against evidence rather than guesswork.

The order is deliberate and is the spine of this spec: **instrument first, harden second.** We do not fix blind.

---

## 2. Problem Statement

The dispatch loop (Marshall → Swagger → `queue/` → `done/`/`failed/`) has **almost no reliable telemetry on its own behaviour**, and — critically — **the breadcrumbs we designed for it are produced by the part of the system that fails.**

The `run-next-workflow` skill instructs each Swagger (worker) to write a `runs/` run record and a `reports/` handback before reporting done. In practice the worker skips this:

- **Verified evidence (2026-06-08):** four jobs (cortex-comprehend, cortex-render, angelsentinel-spec, and a fourth) **moved to `done/` but wrote NO run record and NO handback.** The only reliable fact left behind was "a file landed in `done/`."

Because the worker is the unreliable component, we cannot improve reliability by asking it to self-report — **you cannot ask the thing that's failing to report on its own failure.** We currently cannot measure: per-job duration, success/failure detail, whether a handback was written, whether teardown was clean, or whether tmux windows / processes were left orphaned ("left hanging").

This blindness directly undermines the PARAMOUNT requirement that the dispatch loop be **robust** — reliable comms, reliable return, clean shutdown, no leaks, no whack-a-mole.

---

## 3. Goals

1. **Observe the loop externally.** Capture the full job lifecycle from components *outside* the worker, so telemetry survives a worker that skips its own bookkeeping.
2. **Make the failure measurable.** Produce running metrics — handback-success rate, clean-teardown rate, orphan count, durations, and **failure counts** — so the 2026-06-08 incident becomes a number on a dashboard, not a memory.
3. **Land the smallest useful slice first.** Emit dispatcher + reaper events to Switchboard so that *handback-written-rate* and *clean-teardown-rate* are available immediately, before any larger build.
4. **Set up evidence-driven hardening.** Once metrics exist, every future fix must be verifiable by a movement in a metric.
5. **Respect the constellation's placement rules** — lifecycle events to Switchboard, hang detection to AppyRadar (was "AppyCtrl" — corrected 2026-06-10, see docs/appyradar.md), query/visualise to Watchtower — so this fits the existing app boundaries rather than spawning a new tool.

---

## 4. Non-Goals

- **Not** hardening the loop in this spec. Self-checks, consolidated reconcile, retry-with-backoff, claim-by-id — all deferred to a later "harden" job that this telemetry will inform.
- **Not** fixing the worker's bookkeeping by exhorting the worker to try harder. (It already has the instruction and skips it.) The worker may *also* write its records; this spec does not rely on it.
- **Not** choosing a build technology, storage engine, schema serialization, or dashboard framework. This spec is **build-technique-agnostic.**
- **Not** Claude-session-side tool/skill-usage telemetry — that is an AngelSentinel capability (complementary, separately specced).
- **Not** the AngelEye two-product split (separate spec).

---

## 5. Users and Roles

| Role | Relationship to this telemetry |
|------|--------------------------------|
| **Marshall** (Conductor) | Primary consumer. Reads metrics to decide what to harden next, to spot stranded jobs, and to verify a fix moved a metric. Also a *producer* (dispatcher emits `dispatched`). |
| **David** (PO / operator) | Wants to *see* loop health — "did the Swagger close properly? is it left hanging?" — via queries and visualisations, and trust the loop without babysitting. |
| **The engine** (`claim-next.sh`, reaper) | Producer of `claimed`, `done`, `teardown` events. |
| **AppyRadar** | Producer of orphan/hang detection events. |
| **Swagger** (worker) | The *observed subject*, explicitly **not trusted** as a telemetry source. May emit best-effort records that the external layer cross-checks but never depends on. |

---

## 6. Product Scope

### In scope
- A **lifecycle event schema** for dispatch-loop jobs.
- **External emitters** for each lifecycle event (dispatcher, claim-next, done-watcher, reaper, AppyRadar).
- A **durable event log** (Switchboard) that records every event.
- **Externally-derived flags & metrics** computed from the event log + filesystem state (not from worker self-reports).
- A **query + visualisation surface** (Watchtower) for rates, counts, durations, and failure breakdowns.
- A **first-step slice**: dispatcher + reaper events → Switchboard → handback-written-rate + clean-teardown-rate.

### Out of scope (later)
- Worker hardening (self-check, reconcile, retry, claim-by-id).
- Long-term retention / archival policy beyond what's needed to compute current-window metrics.
- Cross-machine aggregation (M4 Pro + M4 Mini over Tailscale) beyond noting it as a future axis.

### MVP vs later
- **MVP (first step):** dispatcher emits `dispatched`; reaper emits `teardown`; `done/` appearance is detected externally; derive `handback_written?` and `teardown_clean?`; expose two rates.
- **Later:** full event set, durations, orphan detection via AppyRadar, Watchtower visualisations, failure-count breakdowns by kind/cause.

---

## 7. Key Concepts / Entities

- **Job** — one queued ticket (`queue_id`) flowing `queue → running → done|failed`, with an associated Swagger window.
- **Lifecycle event** — an externally-observed fact about a job at a point in time (`dispatched`, `claimed`, `done`, `teardown`, `orphan_detected`).
- **Event log** — the durable, append-only record of lifecycle events (Switchboard).
- **Derived flag** — a boolean/value computed *externally* by inspecting the event log + filesystem (e.g. `handback_written?`), never reported by the worker.
- **Metric** — an aggregate over derived flags/events across a window (e.g. handback-success rate).
- **Orphan** — a tmux window / process with no active job (the "left hanging" condition), detected by AppyRadar.

---

## 8. Functional Requirements

### 8.1 External lifecycle emission (the core principle)
- **FR-1.** Every lifecycle event MUST be emitted by a component **outside the worker**. The worker's participation is never required for an event to be recorded.
- **FR-2.** The **dispatcher** (engine/Marshall) MUST emit `dispatched` when it places/assigns a job (with ticket id, target window, timestamp).
- **FR-3.** `claim-next.sh` MUST emit `claimed` when it atomically claims an entry (queue_id, claimant/session, timestamp).
- **FR-4.** The appearance of a file in `done/` (or `failed/`) MUST be detected externally and emitted as `done` (or `failed`) — by a done-watcher / the reaper that already watches `done/`.
- **FR-5.** The **reaper** MUST emit `teardown` when it closes a Swagger window (queue_id, window, timestamp, clean?).
- **FR-6.** **AppyRadar** MUST emit `orphan_detected` for any tmux window / process with no active job.

### 8.2 Externally-derived flags
Computed by inspecting the event log + filesystem, NOT trusted from the worker:
- **FR-7.** `handback_written?` — does `reports/<queue_id>.json` exist after `done`? (y/n)
- **FR-8.** `run_record_written?` — does a `runs/run-*` record referencing this `queue_id` exist? (y/n)
- **FR-9.** `teardown_clean?` — did the window close with no stray `running/` entry and no orphan process? (y/n)
- **FR-10.** `duration` — time between `claimed` (or `dispatched`) and `done`/`failed`.
- **FR-11.** `stray_running?` — is there a `running/<queue_id>` entry still present after the job reached a terminal state? (y/n)

### 8.3 Query & visualisation
- **FR-12.** Watchtower MUST be able to query the event log to answer "what works / what doesn't" — per-job timeline and aggregate rates.
- **FR-13.** Watchtower MUST surface **failure counts** (total failures, and broken down by cause where derivable: no-handback, no-run-record, dirty-teardown, stray-running, orphan).
- **FR-14.** Watchtower MUST surface the headline rates and counts defined in §13.

### 8.4 First-step slice (smallest shippable)
- **FR-15.** The first build increment MUST emit `dispatched` (dispatcher) and `teardown` (reaper) to the Switchboard event log, detect `done` externally, and compute **handback-written-rate** and **clean-teardown-rate** — delivering a measurable signal immediately, before the full event set or visualisations.

---

## 9. Workflow Requirements

Per-job external observation sequence (happy path):

1. Dispatcher assigns job → emits `dispatched`.
2. `claim-next.sh` claims entry → emits `claimed`.
3. Worker executes (observed, not trusted).
4. File lands in `done/`/`failed/` → external watcher emits `done`/`failed`.
5. External layer computes derived flags (`handback_written?`, `run_record_written?`, `stray_running?`, `duration`).
6. Reaper closes the window → emits `teardown` with `clean?`.
7. AppyRadar sweeps for orphans → emits `orphan_detected` if anything is "left hanging".
8. Watchtower aggregates events into rates/counts.

Failure/edge sequences the layer must handle:
- Job reaches `done/` but no handback → `handback_written? = n`, counts toward failure breakdown. (This is the 2026-06-08 case.)
- Job stranded in `running/` (dead listener) → reaper requeues; `stray_running?` recorded; emitted as a recoverable anomaly.
- Window left open after terminal state → AppyRadar `orphan_detected`; `teardown_clean? = n`.
- Worker writes no events at all → lifecycle still complete from external emitters (the whole point).

---

## 10. Data / Information Requirements — Event Schema

A lifecycle event (illustrative shape; serialization is an implementation choice, not mandated here):

```json
{
  "event_id": "<unique>",
  "type": "dispatched | claimed | done | failed | teardown | orphan_detected",
  "queue_id": "q-20260608-...",
  "experiment_id": "exp-...",
  "emitter": "dispatcher | claim-next | done-watcher | reaper | appyradar",
  "window": "<tmux window/session ref, when applicable>",
  "ts": "<iso8601>",
  "payload": {
    "clean": true,
    "cause": "no-handback | no-run-record | dirty-teardown | stray-running | orphan | error | null",
    "detail": "<one-line, optional>"
  }
}
```

Derived per-job record (computed externally, not stored by the worker):

```json
{
  "queue_id": "q-20260608-...",
  "dispatched_at": "<iso>", "claimed_at": "<iso>", "ended_at": "<iso>",
  "terminal_state": "done | failed",
  "handback_written": false,
  "run_record_written": false,
  "teardown_clean": true,
  "stray_running": false,
  "duration_seconds": 0,
  "failure_causes": ["no-handback", "no-run-record"]
}
```

**Placement of data:**
- Lifecycle events → **Switchboard** durable, append-only event log (the comms bus).
- Orphan/hang detection → **AppyRadar** (emits into the same event log).
- Derived per-job records + metrics → computed for **Watchtower** to query/visualise.

---

## 11. Business Rules

- **BR-1.** No metric or flag may depend on a worker-produced artifact as its *source of truth*. Worker artifacts (`runs/`, `reports/`) are *subjects of measurement* (e.g. "was the handback written?"), never the measurement mechanism.
- **BR-2.** Every job that is dispatched MUST eventually have a terminal lifecycle event (`done` or `failed`) recorded externally — even if the worker never reports.
- **BR-3.** The event log is **append-only**; events are never edited or deleted (auditability).
- **BR-4.** `teardown_clean? = false` whenever a stray `running/` entry or an orphan process/window is associated with the job.
- **BR-5.** A job counts as a **handback failure** if it reached a terminal state without `reports/<queue_id>.json` — regardless of whether the work itself succeeded.

---

## 12. Reporting / Dashboard Requirements (Watchtower)

- **DR-1. Headline tiles:** handback-success rate, clean-teardown-rate, orphan count, total failure count — over a selectable window (e.g. last 24h / last N jobs).
- **DR-2. Failure breakdown:** counts by cause (no-handback, no-run-record, dirty-teardown, stray-running, orphan).
- **DR-3. Duration view:** per-job durations + distribution (min/median/max), to spot stuck/slow jobs.
- **DR-4. Per-job timeline:** the lifecycle event sequence for any `queue_id` (dispatched → claimed → done → teardown), with derived flags.
- **DR-5. "What works / what doesn't":** a job-list view with derived flags as columns, sortable by failure.

---

## 13. Metrics (definitions)

| Metric | Definition |
|--------|------------|
| **Handback-success rate** | jobs with `handback_written = true` ÷ jobs reaching a terminal state, over window. |
| **Run-record-written rate** | jobs with `run_record_written = true` ÷ terminal jobs. |
| **Clean-teardown rate** | jobs with `teardown_clean = true` ÷ jobs with a `teardown` event. |
| **Orphan count** | count of `orphan_detected` events (and current live orphans) over window. |
| **Failure counts** | total terminal-with-failure jobs; plus per-cause counts (no-handback / no-run-record / dirty-teardown / stray-running / orphan). |
| **Duration** | per-job seconds from `claimed`→terminal; aggregate min/median/max. |
| **Stray-running count** | jobs with `stray_running = true` over window. |

---

## 14. Non-Functional Requirements

- **NFR-1. Externality (hard constraint).** Telemetry capture MUST NOT depend on the worker. If the worker writes nothing, lifecycle and metrics are still complete. This is the governing NFR.
- **NFR-2. Durability.** The event log survives session end, compaction, and listener death (Switchboard is the durable substrate).
- **NFR-3. Auditability.** Append-only, timestamped, attributable to an emitter.
- **NFR-4. Low overhead.** Emitting an event MUST NOT materially slow dispatch or block the loop; emission failure MUST NOT fail the job (best-effort, fire-and-record).
- **NFR-5. No new always-on process if avoidable.** Prefer extending existing components (Switchboard log, the existing `done/` watcher/reaper, AppyRadar) over standing up a new daemon. (Per "constellation of apps" + capability-placement.)
- **NFR-6. Build-technique-agnostic.** This spec mandates *what* is observed and *where it lives*, not *how* it is built. No framework/storage/serialization is prescribed.
- **NFR-7. No-cron / in-session.** Any periodic sweeps (orphan detection, done-watching) run via the in-session /loop + Monitor pattern, not cron/API scheduling (Max plan).
- **NFR-8. Idempotent emission.** Re-emitting an event for the same `queue_id`+`type` MUST NOT double-count (dedupe on event identity), so a re-run listener can't corrupt metrics.

---

## 15. Assumptions

- Switchboard already runs a durable event/bus substrate and can accept appended lifecycle events. (To verify against current Switchboard code before build.)
- A `done/` watcher / reaper already exists and watches `done/` (per `run-next-workflow` §0 reaper and memory notes) — it is the natural emitter for `done`/`teardown`.
- AppyRadar is the designated home for process/window/orphan ("already-built / resource health") detection, even if AppyRadar is currently ✗ (not yet built) — orphan detection may land as a later increment.
- `claim-next.sh` can be extended to emit `claimed` without breaking its atomic-claim guarantee.
- The filesystem (`queue/ running/ done/ failed/ runs/ reports/`) remains the job-state ground truth that derived flags inspect.

---

## 16. Constraints

- Subscription / Max-plan: no headless `claude -p`, no cron — in-session loops only.
- Must fit existing app boundaries: Switchboard (events), AppyRadar (hang detection), Watchtower (viz). No net-new standalone tool.
- AppyRadar is not yet built (Lane B shows ✗) — orphan detection is gated on it or a minimal stand-in.
- Spec must remain build-agnostic; this is a requirements artifact, not a design.

---

## 17. Risks

- **R-1.** Emitters themselves become unreliable (e.g. dispatcher forgets to emit) — mitigate by deriving as much as possible from filesystem state transitions that already happen (`done/` appearance), so events are reconstructable.
- **R-2.** AppyRadar absence delays orphan metrics — mitigate by shipping the non-orphan metrics first (first-step slice doesn't need AppyRadar).
- **R-3.** Double-counting on listener re-runs corrupts rates — mitigate via NFR-8 idempotent emission.
- **R-4.** Scope creep into hardening — mitigate by the explicit instrument-then-harden boundary; hardening is a separate dispatched job.
- **R-5.** Metric without action — telemetry that nobody reads. Mitigate by making Marshall's workflow include reading the headline rates when deciding the next hardening job.

---

## 18. Recommended MVP (the smallest first step)

**Emit dispatcher + reaper events to Switchboard; derive two rates.**

1. Dispatcher emits `dispatched` to the Switchboard event log on assignment.
2. The existing `done/`-watcher/reaper detects terminal state and emits `done`/`failed`.
3. The reaper emits `teardown` with `clean?`.
4. Externally compute, per job: `handback_written?` (does `reports/<queue_id>.json` exist?) and `teardown_clean?`.
5. Expose **handback-written-rate** and **clean-teardown-rate** as the first two numbers — even as a flat query over the log, before any Watchtower UI.

This makes the 2026-06-08 incident immediately visible as a metric (handback-written-rate would have read ~0% that day) and proves the external-observation principle end-to-end with the fewest moving parts.

---

## 19. Future Enhancements

- Full event set + durations + per-job timeline in Watchtower.
- AppyRadar orphan/hang detection feeding `orphan_detected` + orphan count.
- Failure-cause breakdown visualisations.
- Cross-machine aggregation (M4 Pro + M4 Mini over Tailscale).
- Feed metrics into the *harden* phase: each hardening fix paired with the metric it should move (verify-the-fix loop).
- Tie-in with AngelSentinel for the Claude-session-side complement.

---

## 20. Open Questions / OPEN PO DECISIONS

1. **Switchboard event API shape** — does Switchboard expose a clean "append lifecycle event" entry point today, or does this need a small extension first? (Verify before MVP.)
2. **AppyRadar now or later?** AppyRadar is ✗ (unbuilt). Do we (a) ship non-orphan metrics first and add orphan detection when AppyRadar lands, or (b) build a minimal orphan-sweep stand-in now? *(Recommendation: a — orphan metrics are not on the MVP critical path.)*
3. **Window for rates** — last-24h, last-N-jobs, or both? Affects how Watchtower queries and tiles are framed.
4. **Where do derived flags get computed** — in Switchboard on ingest, in Watchtower on query, or a small external deriver? (Build-time, but PO should know it's a placement decision.)
5. **Does the worker keep trying to write `runs/`/`reports/`?** It's now *measured, not trusted* — but do we keep the instruction (so the artifacts exist to measure) or treat the external layer as the sole record? *(Recommendation: keep the worker instruction so `handback_written?` remains a meaningful, improvable metric.)*

---

## 21. Acceptance Criteria Summary (testable)

- **AC-1.** Given a job dispatched and run by a Swagger that writes **no** `runs/` record and **no** `reports/` handback, the event log STILL contains `dispatched`, `done`, and `teardown` for that `queue_id`. *(Externality proven.)*
- **AC-2.** Given the 2026-06-08 scenario (terminal, no handback), the system reports `handback_written = false` for those jobs and the **handback-success rate reflects the miss**.
- **AC-3.** A `teardown` event with a lingering `running/<queue_id>` entry or an orphan window yields `teardown_clean = false` and increments the dirty-teardown failure count.
- **AC-4.** Querying the log returns, for a chosen window: handback-success rate, clean-teardown rate, orphan count, total failure count, and per-cause failure counts.
- **AC-5.** Per-job duration is computable from `claimed`→terminal events.
- **AC-6.** Re-running a listener that re-emits an already-recorded event does NOT change any metric (idempotency, NFR-8).
- **AC-7. (First-step gate)** The MVP slice yields **handback-written-rate** and **clean-teardown-rate** from dispatcher + reaper events alone, without AppyRadar and without any worker cooperation.
- **AC-8.** No emission path can fail a job: simulating an event-log write failure leaves the job's own terminal state (`done/`/`failed/`) intact (NFR-4).

---

### Key assumptions made
- Switchboard can host an append-only lifecycle event log (substrate exists; entry point to verify).
- The reaper/done-watcher already observes `done/` and is the right emitter for `done`/`teardown`.
- Filesystem state (`running/`, `done/`, `reports/`, `runs/`) is reliable enough to derive flags from, even when the worker is not.
- AppyRadar is the designated (future) home for orphan/hang detection.

### What appears to be missing from the brainstorm
- Retention/rotation policy for the event log (how long do we keep events?).
- Exact Switchboard append interface / current capability (needs code verification).
- Whether metrics should aggregate across machines (M4 Pro + M4 Mini) from day one.
- A defined owner/cadence for *acting* on the metrics (who reads them, when) — telemetry without a consumer ritual decays.
- Alerting thresholds (e.g. "alert if handback-rate < X") — out of MVP but unstated.

### The 5 most important decisions the product owner still needs to make
1. **AppyRadar now or later** for orphan detection (gates the orphan-count metric; recommend later — not on MVP path).
2. **Switchboard event API** — accept current shape or extend it first (verify before MVP).
3. **Metric window** — 24h vs last-N-jobs vs both (shapes Watchtower queries).
4. **Where derived flags are computed** — Switchboard ingest vs Watchtower query vs external deriver.
5. **Keep the worker's `runs/`/`reports/` instruction** (so `handback_written?` stays a meaningful, improvable metric) vs treat the external layer as the sole record. *(Recommend: keep it.)*
