---
name: run-next-workflow
description: "Claim and run the next queued Dark Factory workflow. Use when the user says 'run next workflow', 'process the queue', 'run the watchtower queue', or when invoked on a /loop to drain the workflow queue. Reads experiments/watchtower-engine/queue/, atomically claims the oldest entry, runs the named workflow inline (visible via /workflows), writes a run record, and moves the entry to done/ or failed/."
---

# run-next-workflow

The polling half of the Watchtower engine. Runs **inside an ordinary interactive session** (on David's subscription — never headless, never `claude -p`). One invocation processes **at most one** workflow, then returns. A `/loop` calls it on an interval; up to 4 staggered sessions can run it concurrently — the atomic claim guarantees no entry runs twice.

## Engine paths

Base: `experiments/watchtower-engine/`
- `queue/`   — pending entries (`*.json`)
- `running/` — claimed, in-flight
- `done/`    — completed
- `failed/`  — errored
- `runs/`    — run records written here

## Procedure

### 1. Claim the next entry (atomic)

Run the claim helper. It moves the oldest entry from `queue/` to `running/` with `rename(2)` — the mutex. If another session already claimed it, this returns nothing.

```bash
experiments/watchtower-engine/bin/claim-next.sh "session-$(date +%s)"
```

- **Exit 1 / no output** → queue is empty. Report "queue empty, nothing to run" and **stop**. (On a `/loop`, this is the normal idle tick.)
- **Prints a path** → that file in `running/` is yours. Continue.

### 2. Read the claimed entry

Read the claimed JSON. Fields:
- `workflow` — the workflow name
- `harness` — path to the `.workflow.js`
- `experiment_id` — parent experiment
- `args` — passed verbatim to the workflow

### 3. Run the workflow inline (visible)

Invoke the **Workflow tool** with the entry's `args`. Run it inline so the user can watch progress in the `/workflows` panel — do **not** bury it in a blind Task sub-agent. The Workflow tool already isolates the heavy sub-agent context; only the compact result returns to this session.

For `level-1-census`, that means calling `Workflow({ name: "level-1-census", args: <entry.args> })`.

### 4. Write the run record

Write `experiments/watchtower-engine/runs/<run_id>.json` where `run_id` is `run-<experiment-suffix>-NNN` (experiment-keyed, per DECISIONS.md D2). Capture:

```json
{
  "id": "run-census-batch-1-001",
  "kind": "run",
  "experiment_id": "<entry.experiment_id>",
  "queue_id": "<entry.queue_id>",
  "status": "complete",
  "started_at": "<iso>",
  "ended_at": "<iso>",
  "result": { "...": "compact summary returned by the workflow" }
}
```

### 5. Move the entry out of running/

- Success → `mv running/<file> done/<file>`
- Failure → `mv running/<file> failed/<file>` and set `run.status: "failed"`, record the error.

An entry must **never** be left in `running/` after this skill returns — that would strand it (no other session will re-claim it). If the workflow errored, still move the entry to `failed/`.

### 6. Report

One line: what ran, the verdict summary, where the run record landed. Then stop — one invocation, one workflow.

## Invariants

- One invocation runs at most one workflow.
- An entry in `running/` is owned; never claim from `running/`.
- Every claimed entry ends in `done/` or `failed/` before return.
- Run IDs are experiment-keyed (D2).
- Promotion / canonical writes are NOT this skill's job (D3) — it only runs and records.

## Spike status

This is a probe in `experiments/watchtower-engine/`, not installed product. The atomic-claim mutex is proven by `bin/test-atomic-claim.sh`. Promote to a real project skill only after the end-to-end run is validated.
