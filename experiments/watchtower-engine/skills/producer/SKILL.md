---
name: producer
description: "Turn a talked request into a schema-valid Watchtower queue ticket — the Producer half of the engine (talk -> ticket). Use when David says 'make a ticket', 'queue a job', 'producer', 'I want to run X', 'add a job', or describes work he wants the factory to do. Elicits only what's missing, writes one ticket to queue/, never executes."
---

# producer (the Producer)

The **front door** of the Watchtower engine. Runs inside an ordinary session. Turns a loose spoken request into **one** schema-valid ticket in `queue/`, then stops. It **never executes** — `run-next-workflow` does that.

Minimal by design (2026-06-05). The only "target" metadata is `label` (client/project). Enhance later.

## Engine paths

Base: `experiments/watchtower-engine/`
- `queue/` — where the ticket lands (timestamp-prefixed filename for time-order).

## The contract (what makes a ticket valid)

Valid = **`run-next-workflow` can read it.** Emit exactly these fields, nothing invented:

| Field | Rule |
|-------|------|
| `queue_id` | `q-YYYYMMDD-<slug>` |
| `kind` | `instruction` \| `skill` \| `workflow` (default `instruction`) |
| kind-field | `instruction`→`prompt` · `skill`→`skill` · `workflow`→`workflow` + `harness` |
| `experiment_id` | `exp-YYYYMMDD-<slug>` |
| `args` | object; **must hold `label`** (client/project; default `"internal"`). Other args verbatim. |
| `requested_at` | ISO 8601 with offset |
| `requested_by` | `"david"` unless told otherwise |

## Procedure

### 1. Parse the request
From what David said, fill in what you can of: **kind**, **label**, and the **task** (+ its kind-field). Don't ask about anything already clear.

### 2. Elicit ONLY what's missing
Ask the *minimum* set of short questions to make a valid ticket. Typically at most three:
- **kind?** — if not obvious. Default `instruction`.
- **label?** — which client/project. Default `internal`.
- **the task** — for `instruction`: the `prompt` **plus a done-condition**; for `skill`: the skill name (+ any args); for `workflow`: the workflow name + `.workflow.js` harness path (+ args).

If David already gave enough, **skip straight to writing** — don't ask for the sake of it.

### 3. Generate IDs + filename
- `<slug>` = short kebab-case from the task (e.g. `census-batch-2`).
- `experiment_id` = `exp-<YYYYMMDD>-<slug>`, `queue_id` = `q-<YYYYMMDD>-<slug>`.
- filename = `queue/<YYYYMMDD>-<HHMMSS>-<slug>.json`.

### 4. Write the ticket
Write the file with exactly the contract fields above. Put `label` and any extra context in `args`.

### 5. Read it back (one line) and stop
> `Wrote q-<slug> — kind:<kind>, label:<label>. Run it?`

Then stop. One invocation = one ticket. Do **not** claim, execute, or run anything — that's `run-next-workflow`.

## Invariants
- Producer **only writes** to `queue/`. Never touches `running/`, `done/`, `runs/`.
- Emit only the contract fields; the sole optional-but-default extra is `args.label`.
- One request → one ticket.

## Future
Standalone now. In C3 this same elicit-and-write behaviour becomes **Marshall's intake** — Marshall takes the talk, produces the ticket, then routes it to a Swagger. Keep the contract identical so the move is a lift, not a rewrite.
