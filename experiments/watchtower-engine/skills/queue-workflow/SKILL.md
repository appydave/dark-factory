---
name: queue-workflow
description: "Queue a Dark Factory workflow for the engine to run — the Producer / talk->ticket front door. Use when the user says 'queue a workflow', 'tell the factory to run X', 'add X to the queue', 'queue a daily review', 'queue census batch N', 'have the factory do X'. Writes a properly-shaped ticket to experiments/watchtower-engine/queue/; the run-next-workflow loop (the Consumer) drains it. In-session only — never cron."
---

# queue-workflow (the Producer)

The **producer** half of the Watchtower engine. Turns a natural-language request into a **queued ticket**. The consumer (`run-next-workflow`, on a `/loop`) drains it. Together: **talk → ticket → run**, all in-session (Max plan; never cron/API).

This is the front door to the North Star — "talk to it and tell it what to do" (`docs/north-star.md`). One invocation **queues**; it never runs the workflow (that's the consumer's job).

## Procedure

### 1. Identify the job + kind
Pick the `kind` that fits the request:
- **`workflow`** — a pre-built SOP in `.claude/workflows/*.workflow.js` (`daily-review`, `level-1-census`, `content-analysis`, `title-gen`, `titles-human`, `thumbnails`, `nail-salon-video`, `hello`).
- **`skill`** — an existing skill should do it (e.g. `refresh-claude-brain`).
- **`instruction`** — free-form "do X" with no pre-built workflow/skill. The "get shit done" path.

Ambiguous → **ask**. Don't guess.

### 2. Determine args
- Use the workflow's **own defaults** when the request doesn't specify (e.g. `daily-review` defaults `since` to "1 day ago" — don't override unless asked).
- For `level-1-census`, the request must name the artifact batch/range.

### 3. Write the ticket
Write `experiments/watchtower-engine/queue/<UTC-timestamp>-<slug>.json` (timestamp prefix = lexical = time-order, so FIFO claim works):
```json
{
  "queue_id": "q-<ts>-<slug>",
  "kind": "workflow | skill | instruction",
  "workflow": "<name>",                       // kind=workflow
  "harness": ".claude/workflows/<name>.workflow.js",  // kind=workflow
  "skill": "<skill-name>",                     // kind=skill
  "prompt": "<free-form task>",                // kind=instruction
  "experiment_id": "exp-<YYYYMMDD>-<slug>",
  "args": { },
  "requested_at": "<iso>",
  "requested_by": "<who asked>"
}
```
Include only the field(s) for the chosen `kind`.

### 4. Report
One line: what was queued, the `queue_id`, and that the loop/runner will pick it up. Then stop.

## Invariants
- One invocation queues **at most one** ticket — unless the user explicitly asks for a batch of N, then write N tickets.
- **Never run** the workflow here — producing ≠ running (`run-next-workflow` runs).
- Args default to the workflow's canonical defaults; override only on explicit request.
- **In-session only.** This is not a scheduler. A human or a self-pacing session is the trigger (problem #15 — the unsolved part).
