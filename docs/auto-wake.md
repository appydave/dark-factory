# Auto-Wake — the queue-notification watcher

**Created**: 2026-07-06, ticket `engine/store/running/20260706T0932Z-auto-wake-and-notify-watcher.json`,
C3 spirit (`backlog/specs/c3-marshall-auto-wake-spec.md`) retargeted to today's engine.
**Status**: implemented and installed live — notification leg active, dispatch leg
ships disarmed.

---

## 1. What this closes

Before this, nothing fired automatically when a ticket landed in `engine/store/queue/`
— a human had to notice the file and type "run the engine." This wires the one
missing synapse: **drop a ticket, get notified**, and (once armed) **get it run**,
with no human polling required.

## 2. The wire

```
ticket lands in engine/store/queue/*.json
        │
        ▼
launchd WatchPaths (com.appydave.dark-factory-wake, ThrottleInterval 10s)
        │  fires
        ▼
engine/wake.py  (stdlib only, one pass, then exits)
        │
        ├─ scans queue/, filters through the SAME dispatchable() skip rules as
        │  orchestrator.py (external-research / deferred / unparseable JSON)
        │
        ├─ diffs against engine/store/.wake-state.json ("last-seen" set)
        │
        ├─ unchanged set  ──▶  log "quiet" line, done (debounced — no repeat notify)
        │
        └─ new ticket(s) found:
              │
              ├─ ALWAYS: macOS notification (osascript) + one line appended to
              │   engine/store/wake.log
              │
              └─ DISPATCH iff ALL of:
                    engine/store/WAKE-ARMED exists
                    AND engine/store/HALT absent
                    AND engine/store/BACKOFF absent
                    AND no live engine/store/.wake.lock (dead pid = stale, taken over)
                  → launches `python3 engine/orchestrator.py --teardown --max-wall 900`
                    fully detached (own session), writes the child pid into
                    .wake.lock, logs it.
                  → any gate failing → logged skip-dispatch(reason), notification
                    still fires.
        │
        ▼
.wake-state.json updated to the current pending set either way
```

**wake.py never calls `claude` itself.** The interactive-claude-only law
(`docs/runtime-model.md`) lives entirely in `orchestrator.py`, which boots real
interactive tmux workers. wake.py's only job past the notify leg is to shell out to
`orchestrator.py` as a supervisor would — same as a human typing the command by hand,
just automatic.

## 3. Debounce

`engine/store/.wake-state.json` holds the last-seen set of *pending dispatchable
ticket filenames* (not a cumulative ever-seen log — the current queue/ contents,
filtered). Each run diffs `current - last_seen`:

- empty diff → "quiet", no notification, state still rewritten to `current` (so a
  ticket claimed out of the queue drops out of the remembered set too).
- non-empty diff → notify + log, using only the *new* filenames for the count/title
  in the notification message.

This means: a ticket that sits in `queue/` untouched across many launchd fires (e.g.
a deferred one skipped by the filter, or one nobody's armed to claim) is only ever
notified once, not on every WatchPaths fire.

## 4. The lock (dispatch de-duplication)

`engine/store/.wake.lock` holds a bare pid (the detached orchestrator child's pid,
written the instant `Popen` returns). Before dispatching, wake.py checks:

- no file → free, dispatch.
- file exists, pid dead (`os.kill(pid, 0)` raises `ProcessLookupError`) → stale,
  take over, dispatch, overwrite the file with the new pid.
- file exists, pid alive → **skip dispatch**, log `skip-dispatch (live lock pid=N)`.
  The notification still fires — only the dispatch leg is suppressed.

There's no separate "clear the lock on exit" step — staleness is detected lazily on
the next wake, by checking whether the recorded pid is still alive. This is
deliberately the same shape as `engine/store/HALT`/`BACKOFF`: existence + one cheap
check, no daemon, no IPC (`docs/kill-switch-spec.md` §1).

## 5. Arm / disarm / status

```bash
bin/factory-wake arm       # create engine/store/WAKE-ARMED ({ts, by}) — dispatch leg goes live
bin/factory-wake disarm    # remove it — back to notify-only
bin/factory-wake status    # ARMED/DISARMED, whether launchd is loaded, last 3 wake.log lines
```

This mirrors `bin/factory-halt` / `bin/factory-resume`'s shape exactly (thin bash
wrapper delegating to the Python module's own arm/disarm/status handling) so the two
gates — HALT (stop everything) and WAKE-ARMED (allow auto-dispatch) — read
identically to a human. **Ships disarmed.** Installing the launchd job does NOT arm
dispatch; those are two independent switches by design (you can have the notifier
live for weeks before ever trusting it to dispatch unattended).

## 6. Install / uninstall

```bash
bash engine/launchd/install.sh     # loads com.appydave.dark-factory-wake, WatchPaths=engine/store/queue
bash engine/launchd/uninstall.sh   # unloads + removes the plist
```

Copies the proven `mochaccino/mochaccino/launchd/` pattern (commit `0416edc`) —
`sed` the `__APP_ROOT__` placeholder into a real plist, drop it in
`~/Library/LaunchAgents/`, `launchctl load`. The one difference: mochaccino's job is
`KeepAlive` (always-running server); this one is `WatchPaths`-triggered (runs once
per queue change, `ThrottleInterval 10` coalesces bursts), so there's no port to
clear before install.

## 7. Divergence from the C3 spec

`backlog/specs/c3-marshall-auto-wake-spec.md` (2026-06-21, Marshall/David) specced
the *real* end-state: Switchboard emits `job.queued` over SSE (`:5099`), Marshall's
single `Monitor` subscribes with `Last-Event-ID` tracking so a reconnect replays
only new tickets, and the wake wire is a proper event bus, not a filesystem poll.

That mechanism was already proven once (2026-06-06, SSE wake ~15s after connect,
replayed the buffered backlog — see C3 spec §2). **It is not what got built here.**

**Why the divergence:** Switchboard is down (this repo's `CLAUDE.md` — "Switchboard
is DOWN"), and the engine itself moved from `experiments/watchtower-engine/` to
`engine/` since the spec was written. Waiting for Switchboard to close this loop
would leave the highest-leverage gap in the factory (nothing fires when a ticket
lands) open indefinitely. So this ships a **filesystem-native equivalent** of the
same wire using what's here today:

| C3 spec (SSE, spec-only) | This build (v1, shipped) |
|---|---|
| Switchboard emits `job.queued` on `POST /jobs` | launchd `WatchPaths` fires on `engine/store/queue/` mtime change |
| Marshall's `Monitor` subscribes, tracks `Last-Event-ID` | `wake.py`, one pass per fire, debounced via `.wake-state.json`'s last-seen set |
| Reconnect replays only new tickets since last id | Diff against last-seen set replays only new *filenames* |
| `claim-next.sh` → `dispatch-swagger.sh` → Swagger runs it | `orchestrator.py --teardown --max-wall 900`, gated by WAKE-ARMED/HALT/BACKOFF/lock |
| One Monitor only (never N self-watchers) | One launchd job only, `ThrottleInterval` coalesces bursts |

**What's explicitly deferred, not abandoned:** the Switchboard SSE leg, `Last-Event-ID`
durable replay across a Switchboard restart, and the cross-machine broadcast this
would eventually enable — all tracked as **DF-7** (the canonical Switchboard state
plane, `docs/comms-flow.md` §5). When DF-7 lands, this filesystem watcher is the
piece that gets swapped for a real SSE subscribe; the ARMED/HALT/BACKOFF/lock gating
and the orchestrator dispatch call underneath stay exactly as they are.

## 8. Return leg (C4)

The notify leg above covers the *queue* side (a ticket showed up to run). C4 closes
the other end — **a ticket finished** — which was previously silent: `orchestrator.py`
only notifies on HITL/BACKOFF, and builder-agent tickets get moved into
`engine/store/done/` by hand with no signal at all.

The wire: `engine/store/done/` is a second `WatchPaths` entry on the same
`com.appydave.dark-factory-wake` launchd job (`ThrottleInterval 10` still applies).
On fire, `wake.py`'s `main()` calls `done_pass()` right after `run_pass()`:

- diffs `done/*.json` against `engine/store/.done-state.json`'s `last_seen` set
  (same last-seen-set idiom as `.wake-state.json`, own file so the two legs never
  collide).
- **first run ever** (no `.done-state.json`): records the full current set, logs
  `[return] baseline: N existing done ticket(s) recorded, no notify` and does
  **not** notify — otherwise installing this against an already-populated `done/`
  would fire one popup per historical ticket.
- **every run after**: one `notify()` call per pass naming the first new ticket +
  count (`"N ticket(s) done: <first one-liner>"` — one popup per batch, not per
  ticket), plus one `[return] done: <one-liner> [<fname>]` wake.log line per new
  file. The one-liner is `done_one_liner()`, which mirrors `engine/status.py`'s
  `done_outcome()` duality: status comes from `store/results/<fname>.json` if
  present, else the ticket's own embedded `result` (string or `{status, notes}`
  dict), else `"unknown"` — any read/parse failure on a single file falls back to
  filename + "unknown" rather than killing the whole pass.
- state is saved either way, so a claimed/removed file also drops out of
  `last_seen`.

No dispatch logic lives in this leg — it is notify-only, on purpose (`docs/kill-switch-spec.md`'s
HALT/BACKOFF gates only apply to the queue→orchestrator dispatch path).

**Dummy-file test procedure** (used to prove the launchd wire live, not just the
code): drop a throwaway ticket into `engine/store/done/` (filename convention
`<ts>-DUMMY-<slug>.json`, containing an embedded `result: {status, notes}`), wait
&gt;10s for the throttled launchd fire, confirm a `[return] done: ...` line appears in
`wake.log` **without running wake.py by hand**, then delete the dummy file and run
`wake.py` once more to re-baseline `.done-state.json` back to the real set. The
ledger (`done/`) must hold zero dummy files once the test is done.

**Second surface:** a macOS notification only reaches David while he's at that
machine. `~/dev/ad/apps/project-digest`'s morning briefing (`lib/shipped.py`) reads
the same `engine/store/done/` directory as a third SHIPPED source (alongside git
commits and `backlog/done/`), so `digest.py dark-factory` also reports what the
factory shipped even if every popup was missed. Windowed by file mtime, same
defensive-zeros shape as the existing `backlog_done_in_window`.

**Overlap note:** `engine/consumer.py` already reads `job.completed` events and
could theoretically chime on completion — it's not used for this because it only
sees orchestrator-path events (no signal for hand-moved builder-agent tickets) and
nobody keeps it running; the done/ directory watch covers both landing paths.

## 9. Related

- `backlog/specs/c3-marshall-auto-wake-spec.md` — the original spec (status line
  points here as of 2026-07-06).
- `docs/kill-switch-spec.md` — the HALT flag-file idiom this reuses for WAKE-ARMED/
  BACKOFF-style existence checks.
- `mochaccino/mochaccino/launchd/` — the proven launchd pattern this was copied from
  (commit `0416edc`).
- `engine/wake.py` — the mechanism.
- `engine/store/running/20260706T0932Z-auto-wake-and-notify-watcher.json` — the
  ticket that shipped this.
