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
  runs/      run records written by the skill
  bin/
    claim-next.sh        atomic claim (the mutex)
    test-atomic-claim.sh concurrency proof
  skills/run-next-workflow/SKILL.md   the polling skill
```

## The mutex

The claim is `rename(2)`: moving an entry from `queue/` to `running/` is atomic. Two sessions racing for the same entry — exactly one `mv` succeeds; the loser gets ENOENT and tries the next entry. No lock files, no daemon, no DB.

## Queue entry shape

```json
{
  "queue_id": "q-<ts>-<slug>",
  "workflow": "level-1-census",
  "harness": ".claude/workflows/level-1-census.workflow.js",
  "experiment_id": "exp-<YYYYMMDD>-<slug>",
  "args": { "...": "passed verbatim to the workflow" },
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

The seed entry `queue/20260530-000001-census-batch-1.json` is the real census batch-1 job (artifacts 5–9). To process it, invoke the `run-next-workflow` skill in a session. It will claim the entry, run `level-1-census` via the Workflow tool, append 5 records to `research/census.jsonl`, write a run record to `runs/`, and move the entry to `done/`.

To install as a real loop later: `/loop 2m run-next-workflow` across up to 4 sessions, staggered.

## What's proven vs not

- **Proven**: the atomic claim mutex under concurrency (the thing that makes 4 sessions safe).
- **Not yet run**: the end-to-end claim → Workflow-tool → record → done path (next step; needs the skill invoked once for real).
- **Out of scope here**: the AppyStack surface (writes queue entries + visualizes state) — the "easy half", built after the engine is validated.
