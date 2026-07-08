# T1-14 proof — WORKER_TIMEOUT resets on worker activity

Ticket: `wg-t1-14-worker-timeout-activity-reset`. Verifies the fix in `engine/orchestrator.py`:
the reboot branch now keys on `a["last_active"]` (updated whenever `WarmWorker.capture()`'s pane
text differs from the previous poll) instead of `a["started"]`, so a worker producing output is
never rebooted purely for taking a long time, while a genuinely silent worker still is.

## Method

Ran the exact algorithm now in `orchestrator.py` (capture pane -> diff against last seen pane ->
bump `last_active` on change -> reboot iff `now - last_active > worker_timeout`) against two real
tmux sessions, using `WarmWorker.capture()`'s same `tmux capture-pane -p` primitive. Timescale
compressed so the run finishes in seconds instead of the ticket's 10-minute/240s scenario:
`WORKER_TIMEOUT=6s` (vs 240s), poll window `20s` (vs 10min) — same logic, same primitive,
different clock only.

Scenario A ("chatty-no-artifact"): a pane that prints a line every 2s forever, landing no
artifact — the shape of a war-game ticket mid-recon.
Scenario B ("silent"): a pane that prints once, then goes quiet — the shape of a genuinely
wedged worker.

Script: `proof_t1_14.py` (run from scratch, not committed — reproducible from this note; see
Reproduce below).

## Result

```
WORKER_TIMEOUT=6s (compressed from 240s), DURATION=20s (compressed from 10min)

Scenario A: chatty, no artifact (prints a line every 2s)
  [chatty] SURVIVED full 20s window -- never rebooted

Scenario B: silent (prints once, then nothing)
  [silent] REBOOT at t=8.1s (inactive 6.1s > 6s)

--- RESULT ---
chatty rebooted: False  (expect False)
silent rebooted: True  (expect True, at ~6s)
PASS
```

Chatty-no-artifact survives the full window (old behaviour: rebooted at `worker_timeout`
regardless of activity). Silent worker still reboots, at `worker_timeout` after its last real
pane change, confirming the inactivity fingerprint distinguishes the two cases.

## Reproduce

```python
#!/usr/bin/env python3
import subprocess, time

WORKER_TIMEOUT = 6
POLL = 1
DURATION = 20

def tmux(*args):
    return subprocess.run(["tmux", *args], capture_output=True, text=True)

def capture(session):
    return tmux("capture-pane", "-t", session, "-p").stdout

def make_chatty(session):
    tmux("kill-session", "-t", session)
    tmux("new-session", "-d", "-s", session, "-x", "80", "-y", "20")
    tmux("send-keys", "-t", session, "-l",
         "i=0; while true; do i=$((i+1)); echo tick-$i; sleep 2; done")
    tmux("send-keys", "-t", session, "Enter")

def make_silent(session):
    tmux("kill-session", "-t", session)
    tmux("new-session", "-d", "-s", session, "-x", "80", "-y", "20")
    tmux("send-keys", "-t", session, "-l", "echo hello-once")
    tmux("send-keys", "-t", session, "Enter")

def run(session_name, label):
    last_pane, last_active, t0, rebooted_at = "", time.time(), time.time(), None
    while time.time() - t0 < DURATION:
        pane = capture(session_name)
        if pane != last_pane:
            last_pane, last_active = pane, time.time()
        if rebooted_at is None and time.time() - last_active > WORKER_TIMEOUT:
            rebooted_at = time.time() - t0
        time.sleep(POLL)
    tmux("kill-session", "-t", session_name)
    return rebooted_at

make_chatty("chatty"); a = run("chatty", "chatty")
make_silent("silent"); b = run("silent", "silent")
assert a is None
assert b is not None and b < DURATION
print("PASS")
```

## Negative checks (per ticket's Verification section)

- `grep -n "last_active" engine/orchestrator.py` — fingerprint wired at dispatch-record
  creation, HITL resume, the per-poll capture, and the reboot-gate comparison.
- `python3 -c "import ast; ast.parse(open('engine/orchestrator.py').read())"` — parses.
- `--max-wall` / `MAX_WALL` unchanged — still the separate absolute ceiling checked outside the
  per-ticket loop (`orchestrator.py` main loop, unchanged from before this ticket).
- CAP / BACKOFF / HALT logic untouched — no edits outside the dispatch-record init, the
  activity-capture block, the HITL-resume reset, and the reboot-branch condition.
- `git diff --stat` for this ticket: `engine/orchestrator.py` + this proof note only.

## Design notes

- Verify-timeout branch (artifact landed but verification failing) stays keyed on `a["started"]`,
  not `last_active` — a stuck verify is a different failure mode than a silent worker, and once
  the artifact lands the worker's pane activity may have already stopped for legitimate reasons.
- HITL resume resets `last_active` alongside `started` — a decision wait can outlast
  `worker_timeout` with zero pane activity (a human thinking, not the worker), so without this
  reset the reboot branch would trip on the very next poll after resume.
