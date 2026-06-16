# Watchtower Engine — Spike

**Status**: spike / probe — not installed product
**Date**: 2026-05-30
**Proves**: the trigger half of the Watchtower (see `docs/watchtower/`), app-free.

## What this is

The engine that runs Dark Factory workflows **without headless execution and without metered billing**. A button (eventually, in the Watchtower app) writes a queue entry. A skill — `run-next-workflow` — runs *inside an ordinary interactive Claude session*, atomically claims the oldest entry, runs the workflow inline (visible via `/workflows`), records the result, and moves the entry to `done/`. A `/loop` drives the polling. Up to 4 staggered sessions run concurrently; the atomic claim guarantees no entry runs twice.

This sidesteps the "can workflows run headless?" question entirely (REVIEW.md C2): they don't run headless — they run in-session, on David's subscription. See memory `project_workflow_trigger_architecture`.

## Layout

```
watchtower-engine/
  queue/     pending entries (*.json), timestamp-prefixed for time-order
  running/   claimed, in-flight (an entry here is owned)
  done/      completed
  failed/    errored
  deferred/  parked entries
  runs/      run records written by the skill (34+ recorded)
  reports/   per-job reports
  proof/     proof-of-behaviour write-ups (c1-first-real-run, concurrency, reaper, board-vN…)
  failures/  the factory failure register — register.jsonl + record-failure.sh + audit.sh
  registry/  staging/  spikes/   support dirs
  bin/
    claim-next.sh         atomic claim (the mutex)
    test-atomic-claim.sh  concurrency proof
    dispatch-swagger.sh   spawn a Swagger job-agent (tmux) for a claimed ticket
    reaper.sh             reap orphan tmux windows (keys off done/<id>.json mtime + grace)
    retry.sh              re-queue failed/ → queue/ with exponential backoff
    constellation-status.sh  preflight: which constellation apps are up
  skills/   run-next-workflow (the polling skill) · marshall · producer · queue-workflow
```

## The mutex

The claim is `rename(2)`: moving an entry from `queue/` to `running/` is atomic. Two sessions racing for the same entry — exactly one `mv` succeeds; the loser gets ENOENT and tries the next entry. No lock files, no daemon, no DB.

## Queue entry shape

```json
{
  "queue_id": "q-<ts>-<slug>",
  "kind": "workflow | skill | instruction",
  "workflow": "level-1-census",
  "harness": ".claude/workflows/level-1-census.workflow.js",
  "skill": "<skill-name>",
  "prompt": "<free-form task>",
  "experiment_id": "exp-<YYYYMMDD>-<slug>",
  "args": { "...": "passed verbatim" },
  "requested_at": "<iso>",
  "requested_by": "watchtower"
}
```

## Verify the mutex

```bash
./bin/test-atomic-claim.sh 50 4      # 50 entries, 4 claimers
./bin/test-atomic-claim.sh 200 8     # high contention
```

Asserts: every entry claimed exactly once, zero double-claims, zero lost.
**Result (2026-05-30): PASS** — 50×4 clean; stress 200×8×5 iterations all PASS.

## Run the engine by hand

Invoke the `run-next-workflow` skill in a session. It claims the oldest entry, runs its workflow via the Workflow tool, writes a run record to `runs/`, and moves the entry to `done/`. The original seed entry `census-batch-1` (artifacts 5–9) has already been processed — it now sits in `done/20260530-000001-census-batch-1.json`.

To install as a real loop: `/loop 2m run-next-workflow` across up to 4 sessions, staggered.

## Added since the original spike

- **Failure register** (`failures/`) — every factory failure is a structured, countable record: `register.jsonl` + `record-failure.sh` (append) + `audit.sh` (count by category; investigate at 3–4).
- **Reaper** (`bin/reaper.sh`) — reaps orphan tmux windows, keyed off `done/<queue_id>.json` mtime + a grace period (only successes land in `done/`). Proven live (`proof/reaper-live.md`).
- **Retry-with-backoff** (`bin/retry.sh`) — re-queues `failed/` → `queue/` with exponential backoff `RETRY_BASE_SECONDS * 2^(attempt-1)` (30/60/120s), then terminal.
- **Swagger dispatch** (`bin/dispatch-swagger.sh`) — spawns a job-agent in tmux for a claimed ticket.

## What's proven vs not

- **Proven**: the atomic claim mutex under concurrency (50×4 clean, 200×8×5 PASS); the **end-to-end** claim → Workflow-tool → record → done path (first real run recorded in `proof/c1-first-real-run.md`; 34+ run records in `runs/`); the reaper firing on live orphans (`proof/reaper-live.md`); the board bridge (board-v2…v5 proofs).
- **Out of scope here**: the AppyStack surface (writes queue entries + visualizes state) — the "easy half", built after the engine is validated.
