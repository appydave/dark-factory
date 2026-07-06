# Spec — C3 Marshall Auto-Wake (close the doing loop)

**Ticket:** DF-10 · **Project:** engine · **Lane:** doing-loop (the missing synapse)
**Status:** v1 BUILT 2026-07-06 — a filesystem-native (launchd WatchPaths) retarget of
this spec for today's engine (Switchboard down); see `docs/auto-wake.md` for the
implementation and its explicit divergence-from-this-spec section. This document
remains the v2/DF-7 end-state spec (Switchboard SSE + Marshall Monitor).
**Author:** Marshall · **Requested by:** David · **Date:** 2026-06-21
**Memory:** [[cleanup-is-harness-driven-not-remembered]], [[parallelism-via-identity]]
**Relates to:** DF-7 (Switchboard state plane — the v2 end-state this is a stepping-stone toward)

---

## 1. Purpose

Close the **doing loop** — `talk → ticket → claim → run → record → done → reap` — by wiring its one missing synapse: **Marshall auto-wakes when a new ticket lands**, instead of a human typing "process the queue." This takes the doing loop from ~80% → **100% closed** and is the single highest-leverage move in the factory: it turns a pile of proven-but-disconnected boxes into a working system.

## 2. Problem Statement

Every other link in the doing loop is proven. The producer writes tickets ✅, the consumer claims+runs+records ✅ (35 jobs through `done/`), the Swagger writes a `reports/` handback ✅ (C3b), Marshall verifies+reaps ✅. **But nothing fires automatically when a ticket lands** — Marshall is invoked by hand. This is the #1 unwired blocker named in `AUDIT-2026-06-12.md` and `docs/SESSION-ORDER.md`.

Critically, the *hard* part is **already proven**: on 2026-06-06 Marshall's `Monitor` subscribed to the daemonised Switchboard SSE stream, woke on a live event (~15s after connect) and replayed the buffered backlog (`docs/watchtower/build-state.md:21`). C3 is **retargeting a proven mechanism**, not inventing one.

## 3. What is already built (DO NOT rebuild)

| Piece | Status | Evidence |
|-------|--------|----------|
| Switchboard emits `job.queued` on `POST /jobs` | ✅ live | `apps/switchboard/src/access/bindings/api-binding.ts:170-207`; SSE on `:5099`, ingest on `:5100` |
| Monitor subscribes to SSE + topic-filter + durable replay | ✅ proven 2026-06-06 | `apps/switchboard/src/deliver/sse-deliver.ts:270-333`; pointed at `process.snapshot` |
| Atomic claim (`rename(2)`) | ✅ 200×8 stress PASS | `experiments/watchtower-engine/bin/claim-next.sh:24-31` |
| Run flow: claim→run→record→done + `reports/` handback | ✅ 35 jobs | `experiments/watchtower-engine/skills/run-next-workflow/SKILL.md` |
| Dispatch Swagger (`tmux new-window`) + registry | ✅ | `experiments/watchtower-engine/bin/dispatch-swagger.sh` |
| Reaper (kill window on `done/` + grace) | ✅ | `experiments/watchtower-engine/bin/reaper.sh` |

## 4. Goals

- **G1.** Marshall's single `Monitor` subscribes to Switchboard's **`job.queued`** topic (not `process.snapshot`).
- **G2.** Marshall tracks **`Last-Event-ID`** so a reconnect replays **only new** tickets — never re-processes `done/` jobs.
- **G3.** On wake, Marshall runs the proven chain **unchanged**: `claim-next.sh` → `dispatch-swagger.sh` → (Swagger) `run-next-workflow` → `done/` + `reports/` → reaper.
- **G4.** A `POST /jobs` with **no human in the loop** drives a ticket end-to-end to `done/` + a surfaced one-line result.
- **G5.** One watcher only (Marshall holds the single Monitor) — never N self-watchers (the dead "4 staggered sessions" model).

## 5. Non-Goals

- **NOT** moving the job pool / claims / liveness fully into Switchboard — that is **DF-7** (the canonical state plane). This spec is the minimal wake-wire and an explicit stepping-stone to it.
- **NOT** closing the **watching loop** (sensors→bus→glass) — separate, still 0%.
- **NOT** parallel orchestration / N Marshall clients — that needs DF-7 + parallelism-via-identity step 0.
- **NOT** rebuilding any proven piece in §3.

## 6. The one design decision — where does the queue live? (RULED)

Two queue dirs exist with near-identical schemas:
- **Switchboard** `queue/<queue_id>.json` (what `POST /jobs` writes) — `{queue_id, kind, workflow?, prompt?, args?, signalId}`
- **watchtower-engine** `queue/<ts>-<slug>.json` (what `claim-next.sh` scans) — same + `experiment_id, harness, requested_at, requested_by`

**Decision (v1):** Point **Switchboard's queue-persistence dir at `experiments/watchtower-engine/queue/`** (it is configurable). `POST /jobs` then writes the ticket *exactly where the proven claim+run flow already reads it* AND emits the `job.queued` wake. This closes the loop **today using every proven part**, with the schema gap (below) as the only real code.

**Why this and not "Switchboard fully owns the queue" now:** that is DF-7 — a larger migration of claims/ownership/liveness into the service. Doing it first would block the loop on a bigger build. v1 proves the synapse end-to-end; **v2 = DF-7** migrates the queue into Switchboard once the loop is real. Reversible: revert the config + Monitor topic.

**Schema reconciliation (the only real code):** Switchboard's ticket lacks `experiment_id` / `harness` / `requested_by`. Two options — pick at build:
- (a) extend Switchboard's `JobTicket` to carry them (validated passthrough), or
- (b) have `run-next-workflow` default them when absent (`experiment_id := exp-<date>-<queue_id>`, `requested_by := "api"`).
Lean (b) — keeps Switchboard's ticket minimal, change is local to the consumer.

## 7. The wire

```
POST /jobs (:5100) ─▶ Switchboard validates + writes ticket → wt-engine/queue/<id>.json
                      └─ emits job.queued on SSE (:5099), durable, monotonic id
                                                                      │
Marshall Monitor  subscribe=job.queued  + Last-Event-ID tracking  ◀──┘
   └─ wake ─▶ claim-next.sh ─▶ dispatch-swagger.sh <queue_id>
                                   └─ Swagger: run-next-workflow ─▶ runs/ + done/ + reports/
                                                                      └─ Marshall reaper kills window
```

## 8. Change set (small, enumerated)

1. **Config** — set Switchboard's queue dir → `~/dev/ad/apps/dark-factory/experiments/watchtower-engine/queue/` (env/config; verify the atomic-write path + filename convention are claim-compatible — `claim-next.sh` sorts lexically, so prefer a `ts-`prefixed `queue_id` or adjust the sort).
2. **Consumer** — `run-next-workflow` defaults `experiment_id`/`requested_by` when a Switchboard-shaped ticket lacks them (option 6b).
3. **Marshall Monitor** — in `.claude/skills/marshall/SKILL.md`: subscribe `http://127.0.0.1:5099/sse?subscribe=job.queued`; persist + re-send `Last-Event-ID` across reconnects; on event → claim+dispatch.
4. **Boot order doc** — Switchboard ingest (`:5100`) + SSE (`:5099`) must be running before Marshall's Monitor arms; note in the marshall preflight.

## 9. Proof criterion (one closed loop — the acceptance test)

With Switchboard running and Marshall's Monitor armed (no human typing "process the queue"):
```bash
curl -X POST http://127.0.0.1:5100/jobs -H 'Content-Type: application/json' \
  -d '{"queue_id":"q-20260621-c3-proof","kind":"instruction",
       "prompt":"Write proof/c3-autowake.md confirming this ran via auto-wake, naming the queue_id."}'
```
**PASS =** Marshall wakes on `job.queued` → Swagger claims+runs → ticket lands in `done/` → `reports/q-20260621-c3-proof.json` written → Marshall surfaces the one-line result and reaps the window. Re-POST a second ticket → only the *new* one wakes (Last-Event-ID held; no replay of the first). Write the proof to `experiments/watchtower-engine/proof/c3-autowake.md`.

## 10. Open questions (resolve at build)

- **Q1.** Filename/sort: Switchboard writes `<queue_id>.json`; `claim-next.sh` claims oldest by lexical sort. Confirm `queue_id` carries a sortable `ts-` prefix, or adjust the claim sort to a mtime sort.
- **Q2.** Schema reconciliation 6(a) vs 6(b) — recommend (b).
- **Q3.** Monitor resilience: if Switchboard is down when Marshall boots, does the Monitor retry-connect, or does preflight hard-require Switchboard up? (Lean: preflight requires it + Monitor auto-reconnects with backoff.)
- **Q4.** Does the wake carry enough to skip re-reading the file? The `job.queued` payload already has `{queue_id, kind, workflow?, prompt?, args?}` — but the claim still reads the durable file (artifact-is-truth). Keep the file read; treat the event as wake-only.

## 11. Build-via

TBD — dispatched as its own job once greenlit. Small enough for a single Swagger run; the change set is 4 bounded edits + the proof run. Not Ralphy (cross-repo: touches both `apps/switchboard` config and `apps/dark-factory` consumer + marshall skill).
