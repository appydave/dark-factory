# Kill Switch Spec — the factory HALT convention

**Created**: 2026-07-06, per Mark Kashef distillation follow-up #6+#7 + David's go 2026-07-06.
**Status**: implemented (engine + two pulses) — this doc is the convention, `engine/halt.py` is the mechanism.

---

## 1. The convention

One flag file, factory-wide:

```
~/dev/ad/apps/dark-factory/engine/store/HALT
```

Its mere **existence** means "stop starting new work." Its **absence** means "run normally." That's the entire protocol — no daemon, no lock server, no IPC, just a file any process can `stat()` in one syscall. This is dark-factory's own file-contract convention applied to control, not just data (`docs/comms-flow.md` §4: state lives under a trusted repo path, never `/tmp`).

The file's contents are informational only (not part of the protocol):

```json
{
  "ts": "2026-07-06T04:12:00Z",
  "by": "david",
  "reason": "pausing to review yesterday's batch"
}
```

A halted-but-corrupt or empty file still reads as **halted** — existence is the ground truth, the JSON payload is just detail for `status.py`/`halt.py status` to show.

## 2. The mechanism

`engine/halt.py` — the single source of truth. Exposes:

- `is_halted()` — the check every factory process calls. Defensive: any error reading/stat-ing the path (missing, unreadable, weird filesystem state) reads as **not halted**. This switch must never itself become a crash vector for the processes it protects.
- `halt_info()` — the `{ts, by, reason}` payload, or `None` if not halted.
- CLI: `halt.py halt ["reason"] [--by <name>]`, `halt.py resume`, `halt.py status [--json]`.

Two thin wrappers for muscle memory: `bin/factory-halt` and `bin/factory-resume` (both `chmod +x`, both just exec `engine/halt.py`).

## 3. Who may write it

- **David** — directly, via `bin/factory-halt` / `bin/factory-resume`, or by hand-editing the file.
- **The orchestrator** — not today (it only reads), but reserved for a future self-halt (e.g. a runaway-cost or repeated-crash guard) without needing a new convention.
- **Roamy** — reserved. If/when a roaming health-monitor agent exists, it writes HALT the same way David does, no special-casing.
- **Watchtower** — reserved for later, once it's a real app (`docs/comms-flow.md` names it design-doc-only today). A "big red button" in its UI would just write this file.

No reader special-cases *who* wrote it — the file's existence is the only fact that matters to a checker.

## 4. Scope

**Now:**
- `engine/orchestrator.py` — checks `is_halted()` before every claim/dispatch pass. Halted -> logs `[halt] ... skipping claim/dispatch this pass` and skips leasing new tickets from `queue/`, but the reap loop for already-running tickets is untouched (see §5).
- `engine/warm_pool.py` — `WarmPool.free_worker()` also checks `is_halted()` and returns `None` while halted, so no worker is ever handed a new prompt even if some future call site forgets its own check. Belt-and-braces, not the primary gate.
- `~/dev/ad/apps/omi-fetch/pulse.py` — checks HALT at the top of `run_pulse()`, before the pulse lock. Halted -> logs `halted, skipping` to `store/pulse.log`, returns `{"halted": True}`, exits 0.
- `~/dev/ad/apps/app-registry/probe.py` — same shape, checks HALT at the top of `run_probe()`, logs `halted, skipping` to `store/probe.log`, exits 0.
- `engine/status.py` — prints a large `FACTORY HALTED` banner (human mode) and a `halt: {...}` key (`--json` mode) whenever the flag is present.
- `app-registry`'s rendered view (`lib/view.py`) — checks the flag directly at render time and shows a banner if present, independent of whether the triggering probe ran or was itself skipped.

**Future (not built by this ticket):** any new factory process — a future Switchboard dispatcher, a future Watchtower auto-action, any new pulse — **MUST** check `is_halted()` (or the equivalent path check, if it isn't Python) before starting new work. This is the one convention every future process inherits by default, the same way `store/` and `rename(2)` claim/lease already are (`docs/comms-flow.md` §4).

## 5. What it deliberately does NOT do

- **No process kills.** HALT is checked only at "am I about to start something new" decision points (claim a ticket, hand out a worker, begin a pulse tick). A worker mid-task, a tmux session already running, a pulse already past its lock — none of these are touched. The switch stops the *next* thing from starting; it never reaches into something already running.
- **No queue mutation.** Tickets sitting in `queue/` stay exactly where they are. Halting does not drain, reorder, or fail them — they're simply not claimed until resumed.
- **No cross-process signal beyond the file.** No SIGTERM, no tmux kill-session, no lock revocation. A wedged worker still only gets recovered by its existing timeout/reboot logic, unrelated to HALT.
- **No queueing of a "resume and immediately catch up" burst policy.** On `resume`, the next poll pass just resumes normal claim/dispatch — no special backlog-priority behavior is added by this switch.

## 6. Cross-machine note

**Per-machine flag, for now.** The path is a local filesystem path on whichever machine's dark-factory clone is running the check — there is no cross-machine broadcast. Halting the factory on the M4 Mini does **not** halt anything running against a dark-factory clone on the M4 Pro (or vice versa). If/when Switchboard's full state plane exists (`docs/comms-flow.md` §5, DF-7, spec-only today), a cross-machine halt broadcast is a natural extension — not built here.

## 7. Verifying it

The 10-second test (see the ticket that shipped this: `engine/store/running/20260706T-halt-switch.json`):

```
python3 engine/halt.py halt "testing"
python3 ~/dev/ad/apps/omi-fetch/pulse.py            # tail store/pulse.log -> "... halted, skipping"
python3 engine/status.py                            # big HALTED banner
python3 engine/halt.py resume
python3 ~/dev/ad/apps/omi-fetch/pulse.py            # ticks normally again
```

## Related

- `docs/comms-flow.md` §4 — the file-contract conventions this switch reuses (store under trusted repo path, never `/tmp`); §8 (appended alongside this doc) — the companion voice-law rule.
- `engine/halt.py` — the mechanism.
- `engine/store/running/20260706T-halt-switch.json` — the ticket that shipped this.
