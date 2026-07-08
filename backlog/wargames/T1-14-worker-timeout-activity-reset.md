# T1-14 — WORKER_TIMEOUT activity-based reset

| field | value |
|---|---|
| ticket | wg-t1-14-worker-timeout-activity-reset |
| track / size / priority | T1 Engine / S / high |
| executor | **build HERE (thinking seat) or attended — NOT engine-dispatched** |
| depends_on | none (but see Execution note) |
| authored | 2026-07-08, from the live T1-11 reclaim incident |

## Mission

The orchestrator reboots any worker that hasn't produced an artifact within `WORKER_TIMEOUT`
(240s, `orchestrator.py:65`). War-game tickets spend all their recon/evidence moves writing
nothing until a late authoring move, so a long ticket is killed mid-recon and the fresh worker
restarts from scratch — forever. Proven live 2026-07-08: T1-11 re-dispatched 3× at 240s
intervals, doc never produced. The `--worker-timeout` flag (added 2026-07-08) is a stopgap that
raises the ceiling; this ticket makes the timeout **reset on worker activity** (pane output /
tmux change) instead of only on artifact-landed, so an actively-working worker is never rebooted
and a genuinely-wedged one still is. Done looks like: a worker that keeps producing pane output
is never rebooted regardless of elapsed time; a silent worker is still rebooted after the
inactivity window; existing `--worker-timeout` flag still sets that window.

## Execution note (why this is NOT engine-dispatched)

The engine cannot reliably fix its own reboot loop while running under it — dispatching this to a
worker that the loop keeps killing is circular. Build it in the thinking seat or an attended
session. This is the one deliberate exception to Q4 (everything-through-the-engine): a bootstrap
fix to the dispatch substrate itself.

## Locked context

- Interactive `claude` only; no `-p`. `warm_pool.safety_check()` enforced.
- Keep the `--worker-timeout` flag semantics: it now sets the INACTIVITY window, not the
  wall-clock ceiling.
- Do not change `--max-wall` (total run guard) or CAP/BACKOFF/HALT logic.

## Recon (verify before any work)

1. `grep -n "WORKER_TIMEOUT\|worker_timeout\|a\[.started.\]" engine/orchestrator.py` → expect
   the two `time.time() - a["started"] > worker_timeout` checks (verify + reboot branches, ≈642/645)
   and the `--worker-timeout` parse in `main()`. If the flag parse is absent → the stopgap was
   reverted; re-add it first.
2. `grep -n "def capture\|send-keys\|last_active\|started" engine/warm_pool.py engine/orchestrator.py`
   → find where a worker's dispatch record `a` is built (the dict with `"started"`) and whether
   `WarmWorker.capture()` already returns pane text (research confirmed it does — reused by the
   BACKOFF sniff). Activity = pane text changed since last poll.
3. Confirm the poll loop cadence (`POLL = 3`, `orchestrator.py:70`) — activity is checked once
   per poll.

## Moves

### Move 1 — Add a per-worker activity fingerprint
- **Do:** Where the dispatch record `a` is created, add `a["last_active"] = a["started"]` and
  `a["last_pane"] = ""`. Each poll, for a running ticket, call `w.capture()`; if the pane text
  differs from `a["last_pane"]`, set `a["last_active"] = time.time()` and `a["last_pane"] = <new>`.
- **Expect:** every running worker carries a `last_active` that advances while it works.
- **Failure signal:** `capture()` is expensive or returns empty on a healthy worker.
- **Counter-move:** if `capture()` cost is a concern at POLL=3, sample every Nth poll; if it
  returns empty for a live worker, fall back to tmux pane `#{history_size}` or activity flag
  (`tmux display -p -t <pane> '#{pane_activity}'`) as the fingerprint instead of full text.

### Move 2 — Gate the reboot on inactivity, not elapsed
- **Do:** Change the reboot branch from `time.time() - a["started"] > worker_timeout` to
  `time.time() - a["last_active"] > worker_timeout`. Leave the verify-timeout branch keyed on
  `started` (a stuck *verify* is a different case) OR also move it to `last_active` — decide and
  comment which. Rename the flag help text: "inactivity window before rebooting a silent worker".
- **Expect:** a worker emitting output every few seconds never trips the reboot.
- **Failure signal:** a fast, chatty-but-looping worker (spinning, printing, never converging)
  now never reboots — an infinite-loop escape hatch is lost.
- **Counter-move:** keep `--max-wall` as the absolute backstop (it already caps total run); add a
  comment that max-wall is the hard ceiling and inactivity-timeout is the soft one. Do NOT remove
  max-wall.

### Move 3 — Prove it
- **Do:** Write a tiny fake worker test: a tmux pane that prints a line every 30s for 10 minutes
  with no artifact. Old behaviour: rebooted at 240s. New behaviour: survives (activity resets).
  Then a silent pane (no output): still rebooted after the window. Capture both in a proof note
  under `engine/docs/` or the ticket result.
- **Expect:** chatty-no-artifact survives; silent gets rebooted.
- **Failure signal:** can't distinguish them (capture fingerprint not changing for the chatty one).
- **Counter-move:** → Move 1 counter-move (switch fingerprint source).

## Assumptions ledger
1. `WarmWorker.capture()` returns current pane text cheaply — research confirmed it exists and is
   reused by BACKOFF; if it's costly, Move 1's counter-move switches to a tmux activity flag.
2. Default inactivity window stays 240s (fine now that it resets on activity). If David wants a
   different default, one-line change — note, don't block.

## Abort conditions
- **A1 — `capture()` unreliable as an activity signal** (empty/garbled for healthy workers and no
  tmux activity flag available). Park to `needs-decision/` describing what was observed; do not
  ship a timeout that never fires or always fires.

## Verification
```bash
grep -n "last_active" engine/orchestrator.py            # fingerprint wired
python3 -c "import ast; ast.parse(open('engine/orchestrator.py').read()); print('parses')"
# behavioural (from the Move 3 proof): chatty-no-artifact worker survives >240s; silent rebooted
```
Negative: `--max-wall` still present and still the hard ceiling; CAP/BACKOFF/HALT untouched
(`git diff --stat` shows only orchestrator.py + a proof note).

## Executor notes
- Scope fence: `engine/orchestrator.py` (activity fingerprint + reboot gate) and a proof note.
  Do not touch warm_pool's boot/kill logic or the claim/reap renames.
- The rabbit hole: rebuilding the whole dispatch loop around an event model. Don't — this is a
  two-field addition (`last_active`, `last_pane`) plus one changed comparison.
