# Dark Factory — Production Engine

The harness on which coding agents spin up, drop down, and communicate. Not a demo,
not a spike — the queue/claim/dispatch/reap kernel that the rest of the factory
(Marshall, Swagger, Switchboard, Watchtower) is meant to run on top of.

Built per `docs/harness-evaluation.md`'s promotion plan: adapts suborch-demo's proven
warm-pool + HITL kernel (`~/dev/ad/apps/suborch-demo/`) into dark-factory's own
queue-file idiom (`experiments/watchtower-engine/`'s `rename(2)` claim + artifact-is-truth
reaping). See `docs/ENGINE-NOTES.md` for what was promoted from where and why.

## Layout

```
engine/
  orchestrator.py   the kernel: scan queue/, lease (rename+ownership), dispatch to the
                     warm pool, verify + reap, emit an event, HITL gate (present, opt-in)
  warm_pool.py       tmux-backed persistent worker pool (df-worker-1..N), adapted from
                     suborch-demo/warm_pool.py — boot once, send-keys reuse
  consumer.py        the events consumer (the missing brick, comms-flow.md §5) — polls
                     engine/store/events/ + omi-fetch/store/events/, logs + chimes
  store/
    queue/           drop a ticket <name>.json here to submit work
    running/         claimed tickets (rename(2) from queue/, ownership recorded)
    done/            committed tickets (artifact verified, never trust the worker's word)
    results/         worker self-reports (<ticket>.json) — one input to verification, not the whole thing
    events/          this engine's own events (job.completed, ...)
    events-consumed.jsonl   consumer's durable ledger (source + path + ts_consumed)
    needs-decision/  HITL gate: worker's pending decision request
    decisions/       HITL gate: human's resolution (approve/decline/redirect)
    audit.jsonl      ticket -> worker -> session_id -> transcript, append-only
```

## Run it

```bash
# 1. drop a ticket into store/queue/ (see an existing one for the shape)
# 2. boot the kernel — it drains the queue, then EXITS but LEAVES THE POOL ALIVE
cd engine
python3 orchestrator.py --pool 1 --model sonnet

# watch it
tmux ls                        # df-worker-1 should be listed
tmux attach -t df-worker-1      # watch/attach to the live worker

# consume events (separately, any time)
python3 consumer.py --once      # single pass
python3 consumer.py             # loop forever, Ctrl-C to stop
```

Flags: `--pool N` (default 1) · `--model NAME` (default sonnet) · `--max-wall SECONDS`
(default 900) · `--teardown` (kill the pool at the end instead of leaving it alive —
default is to leave it alive so a human can attach) · `--hitl <ticket-filename>` (gate
one specific ticket through the needs-decision/decisions mid-task approval flow).

## Hard rules (same as the rest of dark-factory)

- Interactive `claude` only. Never `-p`, never the Agent SDK, never an API key —
  `warm_pool.safety_check()` aborts if `ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN` is set.
- Artifact-is-truth. A ticket is only committed to `done/` after the orchestrator
  itself verifies the real deliverable — the worker's `results/<ticket>.json`
  self-report is necessary but never sufficient.
- The store is a growing ledger, not a demo scratchpad. Nothing resets it between runs.

## Ticket-first (standing rule)
Every unit of work = a ticket in `store/queue/`, even builder-agent-executed ones (`executor: builder-agent`). App ideas -> brains app-pipeline. Ratified 2026-07-04.
