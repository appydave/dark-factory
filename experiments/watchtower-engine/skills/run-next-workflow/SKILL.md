---
name: run-next-workflow
description: "Claim and run the next queued Dark Factory job — the Consumer half of the engine. Use when the user says 'run next workflow', 'process the queue', 'run the watchtower queue', or when invoked on a /loop to drain the queue. Recovers stranded entries, atomically claims the oldest, executes it (workflow | skill | instruction), writes a run record, and moves the entry to done/ or failed/. On an idle queue it arms a queue Monitor so it wakes the instant a ticket lands."
---

# run-next-workflow (the Consumer)

The **polling half** of the Watchtower engine. Runs **inside an ordinary interactive session** (on David's subscription — never headless, never `claude -p`). One invocation processes **at most one** job, then returns. A `/loop` calls it on an interval; up to 4 staggered sessions ("listeners") can run it concurrently — the atomic claim guarantees no entry runs twice.

## Engine paths

Base: `experiments/watchtower-engine/`
- `queue/` pending · `running/` claimed/in-flight · `done/` completed · `failed/` errored · `runs/` run records

## Procedure

### 0. Recover stranded entries (reaper — #16)
Before claiming, sweep `running/` for **abandoned** entries: any file in `running/` **older than ~10 min** with **no matching `runs/` record** is stranded (a dead listener). Move it back to `queue/`:
```bash
find experiments/watchtower-engine/running -name '*.json' -mmin +10
```
For each, if no `runs/run-*` references its `queue_id`, `mv` it back to `queue/`. Keeps a dead tick from stranding work forever.

### 1. Claim the next entry (atomic)
```bash
experiments/watchtower-engine/bin/claim-next.sh "session-$(date +%s)"
```
- **Prints a path** → that file in `running/` is yours. Continue to step 2.
- **Exit 1 / no output** → queue empty. **Arm a persistent queue Monitor (#18)** on `experiments/watchtower-engine/queue/` (if one isn't already running) so this loop wakes the instant a ticket lands — then report "queue empty" and stop this tick. On a `/loop`, this is the normal idle state.

### 2. Read the claimed entry
Fields: `kind` (workflow | skill | instruction; default workflow), `experiment_id`, `args`, plus the kind-specific field below.

### 3. Execute by `kind` (#17 — generalized)
Run it **inline** (visible in `/workflows` / this session) — never bury it in a blind sub-agent.

- **`workflow`** — `harness` names the `.workflow.js`. Invoke the **Workflow tool**: `Workflow({ name: <entry.workflow>, args: <entry.args> })`.
- **`skill`** — `skill` names a skill. Invoke it via the Skill tool with `entry.args` (e.g. `refresh-claude-brain`).
- **`instruction`** — `prompt` is a free-form task. Do it directly, with judgment, using `entry.args` as context. This is the "get shit done" path.

### 4. Write the run record
`experiments/watchtower-engine/runs/run-<experiment-suffix>-NNN.json`:
```json
{ "id": "...", "kind": "run", "experiment_id": "...", "queue_id": "...",
  "executed": "workflow|skill|instruction", "status": "complete",
  "started_at": "<iso>", "ended_at": "<iso>", "result": { } }
```

### 5. Move the entry out of running/
- Success → `mv running/<file> done/<file>`
- Failure → `mv running/<file> failed/<file>`, set `run.status: "failed"`, record the error.

An entry must **never** be left in `running/` after this skill returns.

### 5b. Write the handback (`reports/`) — the terse return-leg (C3b)
After the entry is in `done/`/`failed/`, write a **one-shot terse handback** to `experiments/watchtower-engine/reports/<queue_id>.json`:
```json
{ "queue_id": "...", "status": "complete|failed",
  "outcome": "<one line: what ran + artifact / run-record path>", "ended_at": "<iso>" }
```
This is what **Marshall reads** to surface the result and decide whether to close the window — a purpose-built terse handback, distinct from the detailed run record in `runs/`. **Write it last** (success *or* failure), so its appearance = "job finished, here's the summary."

### 6. Report
One line: what kind ran, the verdict, where the run record landed. Then stop — one invocation, one job.

## Invariants
- One invocation runs **at most one** job.
- A `reports/<queue_id>.json` handback is written for **every** job (the return-leg Marshall reads) — last, after `done/`/`failed/`.
- An entry in `running/` is owned; never claim from `running/` (the reaper only requeues *stranded* ones).
- Every claimed entry ends in `done/` or `failed/` before return.
- Promotion / canonical writes are NOT this skill's job — it only runs and records.

## Spike status
Probe in `experiments/watchtower-engine/`. The atomic-claim mutex is proven (`bin/test-atomic-claim.sh`, 200×8 clean). Reaper + kind-dispatch + Monitor added 2026-06-01; not yet stress-tested.
