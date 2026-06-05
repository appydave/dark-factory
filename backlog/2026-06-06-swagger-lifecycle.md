# Swagger lifecycle — no orphans, talkable, reliably reaped

**Raised**: 2026-06-06 (David, during C3b proof)
**Class**: C3d-lifecycle. Sibling of the ticket reaper (#16) but for *sessions*, not tickets.
**Status**: open — proposal stage, not built.

## The problem (felt)

Spawned Swaggers strand. Interactive `claude` idles at the REPL **forever** after its job is done; the only cleanup is Marshall running `tmux kill-window`, which fails whenever (a) the window isn't in Marshall's tmux server (e.g. `!`-pasted spawn), or (b) Marshall never catches the handback, or (c) it was a one-off test nobody cleaned up.

**Evidence (2026-06-06):** a Swagger `"Process the next ticket in experiments/watchtower-en…"` found **idle 22 hours**, plus ~4 stray `--dangerously-skip-permissions` sessions (1–3 days old). 27 `claude` processes total, most unidentifiable. David: *"I'm going to have hundreds of these sessions open and not actually understand what they're for."*

## The constraint that makes it non-trivial

Swagger is a **talkable orchestrator** (build-state rule 5, corrected this session): David is *allowed* to jump into a Swagger window and help, and Swagger may surface a help-request to David. So the fix **cannot** be "auto-kill the instant the job hits `done/`" — that would slam the window while David might still be talking to it. The lifecycle must be *deliberate*: persist while useful, reap when truly idle.

## Class-level fix to consider (smallest move first)

1. **Registry (visibility) — do this first, cheapest.** On spawn, write `experiments/watchtower-engine/swaggers/<window>.json`: `{ queue_id, window, pid, tty, purpose, started_at }`. On close, delete it. Now `ls swaggers/` answers "what is each open session and why." Even with zero auto-reaping, this kills the "hundreds I can't identify" pain.
2. **Reaper (cleanup).** A sweep (in Marshall's loop or its own /loop tick): for each registry entry whose `queue_id` is in `done/`/`failed/` AND older than a grace window (e.g. 10 min, rule-5 talk room) AND no active engagement → `kill-window` + delete the registry entry + kill the stray pid if windowless. Mirrors the ticket reaper (#16).
3. **Self-close fallback.** Swagger, as a last act after the grace window with no David input, closes its own window (`tmux kill-window` on itself). Defence-in-depth so cleanup never depends solely on Marshall being alive.

## Open question for David

- Grace window length before reap (default 10 min)?
- Is **teammate-mode** (`claude --teammate-mode tmux`, already in use elsewhere — pid 20119) the better primitive than hand-rolled tmux windows? It gives managed lifecycle + talkable agents natively. Possible larger pivot that dissolves this whole orphan class. Worth a spike before hardening the hand-rolled path.

## Done when

- A live Swagger is always identifiable from `swaggers/`.
- A finished, un-engaged Swagger is gone within the grace window — zero orphans after a run.
- David can still talk to / help a Swagger while it's working.
