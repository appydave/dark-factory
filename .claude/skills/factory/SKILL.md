---
name: factory
description: "Factory console — the PO driver for the war-game engine. Use at the start of a dark-factory ops session, or when David says 'run the factory', 'drive the factory', 'factory console', 'what's on the floor', 'dispatch a ticket', 'promote and run', 'drain tickets'. ORIENTS (portfolio + engine status from disk, never from a handover), SELECTS+EMITS a ticket via `promote-wargame go` (hands you the run command — never launches from this seat), and WATCHES via engine signals. It authors + dispatches; it never reads/edits impl to build."
allowed-tools: Bash, Read
---

# Factory — the session driver (PO console for the war-game engine)

This session, when it invokes `factory`, plays the **driver** seat over the dark-factory engine.
It DRIVES the run-loop; it does not build, and it does not launch the engine from this seat.
Spec: `docs/factory-console-skill-spec.md`. Repo: `/Users/davidcruwys/dev/ad/apps/dark-factory`.

## The hard contract (this is the whole point of the skill)

- **Three zones (know which you're in):**
  1. **Driver tooling** (`bin/promote-wargame.py`, `engine/run.sh`, the go-lint) = the seat's OWN
     kit. A real bug here is the seat's job to fix — the engine can't maintain its own dispatch
     tooling, and you don't dispatch a whole ticket for a one-line tool fix.
  2. **A war-game ticket's impl** (the tool T3-03 builds, the fix T1-20 makes) = a worker's job,
     **dispatched**. Tripwire: grepping source to edit it *for a ticket* → STOP and dispatch.
  3. **The live engine edited from inside the seat driving it** = the hazard. Even genuine engine
     fixes go through tickets (Python doesn't hot-reload; they land next launch). Never hand-patch
     `orchestrator.py`/`warm_pool.py` while a run you're driving is live.
- **Read the DISK, never a handover, for state.** Handovers drift — a handover once flagged an
  already-done ticket as the top "next" job. ORIENT always re-derives truth from the store.
- **This seat dispatches, it does not run.** Read-only steps (orient/status/watch) run here.
  The launch is **emitted as a command David runs** in his engine/ terminal — never launched here.
- **One run-path only.** `promote-wargame go` (select, lints, emits) → `./run.sh` (run). The raw
  `claude`-in-a-window and hand-typed `orchestrator.py` techniques are retired.
- **Interactive `claude` only, never `-p`** (`warm_pool.safety_check()` enforces).
- **Self-host tickets (T1-01/02/03/05/06) run attended** — never engine-dispatched.

All commands use **absolute paths** (the cwd trap bit repeatedly). `DF=/Users/davidcruwys/dev/ad/apps/dark-factory`.

## The four moves

### A. ORIENT (read-only, runs here)
```bash
python3 /Users/davidcruwys/dev/ad/apps/dark-factory/bin/promote-wargame.py --list   # portfolio: ready/blocked/queued/done
python3 /Users/davidcruwys/dev/ad/apps/dark-factory/engine/status.py                # queue/running/done + tmux liveness
pgrep -f consumer.py >/dev/null && echo "chime: live" || echo "chime: DOWN"          # is the audible reap signal up
```
Report a compact "here's the floor" summary + the single recommended next ticket (highest-priority
`ready`, non-self-host). Do NOT trust any prior session's claim about what's ready — this read wins.

### B. SELECT + EMIT — the gap-closer (hands off)
No two-step gap. One command lints each ticket's `## Verification` block, promotes, and prints the
run command **sized to how many you queued**:
```bash
python3 /Users/davidcruwys/dev/ad/apps/dark-factory/bin/promote-wargame.py go T1-16          # one ticket -> ./run.sh
python3 /Users/davidcruwys/dev/ad/apps/dark-factory/bin/promote-wargame.py go T3-03 T3-04     # two -> ./run.sh 2 (parallel, worktree-isolated)
python3 /Users/davidcruwys/dev/ad/apps/dark-factory/bin/promote-wargame.py go --next 3        # next 3 ready
```
The **lint** blocks a ticket whose Verification block has a `<placeholder>` or would fail literally
(both wedged the engine on 2026-07-11); it warns on bare-`grep` polarity. `go` prints **NO run
command if nothing was promoted** (empty-run guard). Then **hand David the printed `./run.sh [N]`**
to run in his engine/ terminal. Parallel (`N>1`) needs the worktree isolation (wg-t1-19); CAP=3.
Never launch it from here.

### C. WATCH (event-driven, consumes existing comms — runs here, read-only)
Use the highest available signal; **never hand-roll a timer**:
1. **`Monitor`** (harness) — block until `engine/store/done/` changes. Zero polling.
2. **blackboard MCP** (`bb_*`) — read the factory channel workers post progress to (when wired).
3. **engine `store/events/`** — `job.completed` events (what chime consumes today).
4. **Switchboard SSE** — the specced bus, when it's back up (C3/DF-7).
Drop to a **transcript read ONLY to judge content drift** — never as the liveness mechanism.
(Chaperone stays a separate thin watcher for non-factory sessions; the console is the driver.)

### D. REAP + REPORT (read-only, runs here)
On `done/` change: read the result JSON, report verdict + what landed, surface the next
recommended ticket. Chime already fired the audible signal; turn it into a decision.

## What this is NOT
- Not the orchestrator (it dispatches, doesn't build).
- Not Chaperone (that's the watcher; this is the driver — two roles).
- Not the T5 Watchtower web app (this is its terminal-first precursor).
- Not a new comm bus (it consumes Monitor/blackboard/events/SSE; it adds none).
