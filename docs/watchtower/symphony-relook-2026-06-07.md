# Symphony re-look (2026-06-07) — through the lens of what we've built

*Done inline by Marshall (high-judgment synthesis + full memory context). Re-reading `symphony-spec.md` after independently building the dispatch loop, the dispatch registry, and the engine-state reaper. Verdict: **Symphony already formalized both the registry AND the stuck-case we deferred — and its stuck-case mechanism confirms the AngelEye direction.***

## 1. Where Symphony already formalizes what we reinvented

| Ours (built from scratch) | Symphony's formalization | Verdict |
|---|---|---|
| `registry/<window>.json {queue_id}` — window↔ticket ownership | **OrchestratorState (§4.1.8)**: a single authoritative `claimed` (set), `running` (map), `retry_attempts` (map), `completed` (set) — owned by one authority | We built a thin file-based subset of `claimed`. Symphony's is richer. |
| atomic-rename claim mutex | **Claim state machine (§7.1)**: `Unclaimed → Claimed → Running → RetryQueued → Released` (explicit states) | We have the mutex but no explicit *states*. |
| reaper reaps after handback | **Run-attempt lifecycle (§7.2)**: `…StreamingTurn → Succeeded / Failed / TimedOut / Stalled / CanceledByReconciliation` | We only model "done"; Symphony names the failure terminals. |
| "verify the artifact, never trust done" | **§7 invariant**: "the orchestrator is the only component that mutates scheduling state; all worker outcomes are reported back and converted into explicit transitions" | Same principle, formalized. |
| Marshall rebuilds state from bus replay | **§7.4**: "restart recovery is tracker-driven and filesystem-driven, *without a durable orchestrator DB*" | Same idea (filesystem + bus). |

## 2. What Symphony covers that we're MISSING — the stuck case

Our reaper deferred the **stuck / no-handback** case ("needs session liveness"). **Symphony solves it — and NOT via the process tree** (which we proved dead):

- **§8.5 Part A — Stall detection (runs every tick):** for each running issue, compute `elapsed_ms` since `last_codex_timestamp` (the last event seen) — or `started_at` if none. If `elapsed_ms > codex.stall_timeout_ms` (**default 300000 = 5 min, §6.4/§10.6**), terminate the worker and queue a retry. Transitions to `Stalled` (§7.2) via the `Stall Timeout` trigger (§7.3).
- **The liveness signal is the agent's EVENT STREAM (§10.4):** the runner emits timestamped events (`session_started`, `turn_completed`, …) upstream; `last_codex_timestamp` is just the newest one. **No events for `stall_timeout_ms` = stalled.**

➡️ **This is precisely the AngelEye live-hook idea, validated.** The Claude Code hook events ARE our event stream; "last hook event timestamp for session X" is our `last_codex_timestamp`; "no events for N minutes" is our stall signal. Symphony tells us the *exact* mechanism for the reaper's stuck half — and confirms it must come from an event stream (AngelEye live hook), never the process tree.

Also missing on our side:
- **§8.5 Part B — reconcile against source-of-truth state every tick** (terminal → terminate + clean).
- **§8.4 retry-with-backoff + RetryEntry (§4.1.7):** we have NO retry model — a failed/stuck job just dies. Symphony schedules exponential-backoff retries.
- **§8.6 startup cleanup:** on start, reconcile + clean orphans (we have a partial version in run-next-workflow's reaper step 0).
- **§7.1 continuation nuance:** a successful exit ≠ issue done; re-check state, maybe run more turns (relevant if our jobs ever go multi-turn).

## 3. What to adopt — ranked

1. **Stall detection via last-event-timestamp + a stall_timeout (NOT process tree).** This is the reaper's stuck-case half and the concrete spec for *using* AngelEye's live-hook stream. Pairs with the constellation frame (AngelEye answers "last-active"; Marshall reaps). (§8.5A, §10.4)
2. **Promote the registry to explicit claim states** (`Claimed/Running/RetryQueued/Released/Stalled`). Gives the stuck-case and retries a home; our `{queue_id}` file becomes a small state record. (§7.1, §4.1.8)
3. **A periodic reconciliation pass (before dispatch), complementing our event-driven reap.** Our engine-state reap handles the common case on `reports/` events; a reconcile tick handles stalls + terminals. Monitor-driven, not a timer (per `watchtower-from-symphony.md`). (§8.1, §8.5)
4. **Retry-with-backoff** for failed/stalled jobs (§8.4 + RetryEntry §4.1.7) — we have none.
5. **Formalize idempotency/restart-recovery** (§7.4): claimed+running checks before dispatch; rebuild from filesystem + Switchboard replay on restart.

## Bottom line
We didn't waste effort — building the registry from scratch is *why* this re-look lands: we now recognise Symphony's `OrchestratorState.claimed` + stall-detection as the fuller version of our own primitives. **The single highest-value lift is §8.5 stall detection via the event stream — it's the reaper's missing half AND the concrete justification for the AngelEye live hook.** Adopt incrementally; don't port Elixir (host-agnostic — see `watchtower-from-symphony.md`).
