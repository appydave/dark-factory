# Factory-Console Skill — Spec (draft for ratification)

**Date:** 2026-07-10 · from the 2026-07-08 brief (`backlog/2026-07-08-factory-console-skill.md`)
**Status:** BUILT 2026-07-11 — ratified; `factory` skill + `promote-wargame go` shipped. Home: `.claude/skills/factory/` (staged in dark-factory, per David). v1 = strictly copy-paste; named-tmux auto-launch deferred until we can monitor a run with an application.
**Decisions locked in the 2026-07-10 scoping interview:**
1. **Shape** — new standalone `factory` skill (the *driver*) **+** a hardened `promote-wargame go`
   subcommand it calls. Skill carries judgment; script closes the mechanical gap. Not either/or.
2. **Run/hand line** — read-only steps run in-seat; anything that dispatches/launches is **emitted
   as a copy-paste command** for another terminal, never run from this seat.
3. **Watch** — the console is a *consumer of the fleet's existing comm layer*
   (`Monitor` → blackboard MCP → engine `store/events/` → Switchboard SSE), **not** a hand-rolled
   poller. This is where the "close the loop" thread lands first.

---

## 1. Why a skill (not memory, not just a script)

- A **memory rule** (`feedback_po_seat_never_builds`) won't reliably reload across sessions — it
  did not on 2026-07-08 and the two-step gap misfired twice (empty runs).
- A **script** gives mechanical guarantees but can't hold an operating contract or adapt a watch.
- A **skill** is invoked by name (`/factory`), reloads on demand, and is the natural home for the
  operating contract + tool orchestration. It *calls* the hardened script.

**Division of labour:** skill = driver (judgment, contract, conducting). Script = one instrument
(atomic select+emit). Skill never reimplements what the script guarantees; script never holds
judgment.

---

## 2. The four moves the skill drives

### A. ORIENT (read-only → runs in-seat)
One glance, three reads, no launches:
- `promote-wargame.py --list` → portfolio (ready / blocked / queued / done counts + list)
- `engine/status.py` → queue / running / done + tmux liveness
- `pgrep -f consumer.py` → is chime alive
Output: a compact "here's the floor" summary + the single recommended next ticket (highest-priority
`ready`, non-self-host).

### B. SELECT + EMIT (the gap-closer → hands off)
No two-step gap. The skill runs **`promote-wargame go <TICKET>`** (or `go --next N`) which:
- promotes the ticket(s) (existing `promote()` path, all its guards intact), AND
- **prints the exact run command** with absolute paths, in one shot.
The skill then **hands that command to David** to run in another terminal. It never launches the
orchestrator from this seat (locked decision #2). It **refuses to emit a run command for an empty
queue** — if nothing got promoted, it says so instead of printing a command that would run nothing.

### C. WATCH (event-driven, consumes existing comms → runs in-seat, read-only)
Priority order — use the highest available, never a bespoke timer:
1. **`Monitor`** (harness) — block until `engine/store/done/` changes. Zero polling.
2. **blackboard MCP** (`bb_*`) — read a factory channel workers post progress to (when wired).
3. **engine `store/events/`** — `job.completed` events (what chime already consumes).
4. **Switchboard SSE** — the specced bus, when it's back up (C3/DF-7).
Drop to a **transcript read ONLY to judge content drift** — never as the liveness mechanism.
This supersedes Chaperone's `wc -l` polling *for factory work*; Chaperone stays a thin, separate
watcher for attended/non-factory sessions.

### D. REAP + REPORT (read-only → runs in-seat)
On `done/` change: read the result JSON, report verdict + what landed, surface the next recommended
ticket. Chime already fires the audible signal; the skill turns it into a decision.

---

## 3. Seat/floor discipline — baked into the skill's shape

The skill's own procedure enforces the contract that memory couldn't:
- **This seat authors + dispatches; it does NOT read/edit impl to build.** Tripwire written into
  the skill: *if you are grepping source to edit it for a ticket, stop and dispatch.*
- **One run-path only** — `promote-wargame` (select) → `orchestrator.py --worker-timeout 1800`
  (run). The raw `claude`-in-a-window technique is retired (2026-07-08); the skill never offers it.
- **Interactive `claude` only, never `-p`** — `warm_pool.safety_check()` already enforces; the
  skill states it so the human never tries to "speed it up" with the API.
- **Self-host tickets (T1-01/02/03/05/06) run attended** — the skill flags these and does NOT
  route them through the engine dispatch path.

---

## 4. The `promote-wargame go` subcommand (the only code change to an existing file)

Today `promote-wargame.py` takes `<TICKET>` | `--list` | `--next N`. Add one verb:

```
promote-wargame.py go <TICKET>       # promote AND print the run command
promote-wargame.py go --next N       # promote next N AND print the run command
```

`go` = existing promote path, then on success emit verbatim (absolute paths, current defaults):

```bash
cd /Users/davidcruwys/dev/ad/apps/dark-factory/engine && \
  python3 orchestrator.py --pool 1 --model sonnet --max-wall 3600 --worker-timeout 1800
```

If **nothing** was promoted (already done / blocked / empty), `go` prints the reason and **no run
command** — the empty-run guard, in code. Plain `<TICKET>` / `--next` keep today's behaviour
(select only), so nothing existing breaks.

---

## 5. What this is NOT (scope fence)

- Not an orchestrator — it dispatches, it doesn't build.
- Not a replacement for Chaperone — two roles: console = driver, Chaperone = watcher.
- Not the T5 Watchtower web app — it's the terminal-first precursor to that same control-plane role.
- Not a new comm bus — it *consumes* Monitor / blackboard / events / Switchboard; it adds none.

---

## 6. Build plan (once ratified)

1. Add `go` verb to `bin/promote-wargame.py` (+ empty-run guard) — small, testable in isolation.
2. Write `SKILL.md` for `factory` (trigger-only description in David's voice; the four moves;
   the seat/floor contract; the watch priority order).
3. Decide skill home: staged here in dark-factory first, or straight into appydave-plugins?
   (Per repo rule, dark-factory stages skill code; copying to plugins is a separate decision.)
4. Dry-run the full loop once (orient → go → watch via Monitor → reap) on a real ticket.

**Open question for David before build:** skill home (stage here vs. plugins), and whether `go`
should also *offer* to launch in a **named tmux** the human attaches to (still their action, but
one keystroke closer) — or stay strictly copy-paste.
