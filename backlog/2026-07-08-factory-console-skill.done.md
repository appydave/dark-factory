# Factory-console skill — the session driver (PO console for the engine)

**Date:** 2026-07-08 · raised by David after two "empty run" / two-step-gap misfires
**Status:** ✅ DONE 2026-07-11 — specced + built. See `## Status` at the bottom.

## The problem it solves

Running factory jobs today is a manual two-step (`promote-wargame --next N` to SELECT, then
`orchestrator.py ...` to RUN). The gap between them is bridged from human memory and gets
dropped — twice on 2026-07-08 (T1-11 requeue skipped → empty run; T1-14 select skipped → empty
run). A durable *memory rule* (feedback_po_seat_never_builds) won't reliably reload across
sessions. The right home for the operating contract is an **invocable skill**, not memory.

Also: Chaperone is a *watcher*, not a *driver* — it arrived late and was the wrong entry point
for "control my workflow." The missing piece is the driver.

## What the skill is

A `factory` / `factory-console` skill invoked at the start of an ops session that DRIVES:

- **Orient** — show portfolio status (`promote-wargame --list`) + engine status (`status.py`) +
  what's running, in one glance.
- **Select + run as ONE guided action** — no two-step gap: pick a ticket (or `--next N`), it
  promotes AND gives the run command (or runs it), and refuses to "run" an empty queue silently.
- **Seat/floor discipline baked in** — it authors tickets and dispatches; it never reads/edits
  impl to build (the [[feedback_po_seat_never_builds]] rule, enforced by the skill's shape not a
  memory).
- **Watch via engine signals** — liveness/progress from `store/events/` + `status.py` + tmux
  `pane_activity` + audit claim-times; drop to a transcript read ONLY to judge content drift
  (the smarter-than-blind-polling design — supersedes Chaperone's `wc -l` loop for factory work).
- **One run-path** — `promote-wargame` (select) → `orchestrator.py --worker-timeout 1800` (run);
  never the raw `claude`-in-a-window technique (retired 2026-07-08).

## Relationship to other pieces

- Precursor to the T5 Watchtower web app (Q6) — same control-plane role, terminal-first.
- Consumes the engine-events watch design that should also land in T5-03 (live-agent-view).
- Chaperone stays a thin, separate watcher for attended/non-factory sessions; the console is the
  driver. Two roles, not one.

## Next step

Spec it (interview or draft) before building — decide: standalone skill vs. extension of an
existing one; how much it runs vs. hands the human commands; whether it wraps the chaperone watch
or just launches it.

---

## Status — DONE 2026-07-11

Specced (`docs/factory-console-skill-spec.md`) then built in one session with David.

- **`factory` skill** → `.claude/skills/factory/SKILL.md`. The driver: ORIENT (disk truth, not a
  handover) → SELECT+EMIT → WATCH (Monitor/blackboard/events/SSE) → REAP. Seat/floor contract baked
  into its shape (the memory couldn't reload; the skill can).
- **`promote-wargame go`** verb added → promotes AND prints the run command in one shot; **empty-run
  guard in code** (no run command if nothing promoted). Tested both paths. Plain `<TICKET>`/`--next`
  unchanged.
- **Decisions:** home = dark-factory (staged); v1 = strictly copy-paste (hands the command off, never
  launches from the seat); named-tmux auto-launch deferred until a run can be monitored by an app.
- **Bonus catch:** ORIENT-from-disk immediately exposed handover drift — T1-15 was listed as the top
  "ready" ticket but was already done+committed (3d3328f). Exactly the failure the console prevents.
