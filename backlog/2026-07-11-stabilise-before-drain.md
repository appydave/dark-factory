# Stabilise before drain — engine moratorium after T1-21

> **Author: the Chaperone** (the outside-eye session watching `dark-factory-c2` on 2026-07-11).
> This is *not* the seat's own note. It's written from the vantage of the one party with
> cross-session memory — the watcher — so the next factory seat reads today's friction the
> way an observer saw it, not the way the operator (understandably) narrated it mid-fight.
> Channel: `dark-factory-coherence` · digest: `docs/_chaperone-feed.md`.

## The one-line ask

**Freeze the engine after T1-21 lands. Then run only *product* tickets at pool=1, off one
dead-simple command, until value visibly flows — before touching the engine or parallelism again.**

## The diagnosis (why it feels like a shit fight)

David's words today: *"it never gives me clear instructions and I don't know why."* It's not
the operator and it's not bad driving. It's structural:

**The factory is self-hosting — you are using the machine to fix the machine.** Nearly every
ticket touched this session was the engine repairing *itself*, not producing anything:

| Ticket | What it was | Category |
|--------|-------------|----------|
| T1-16 | durable verdict ledger | engine self-repair |
| T1-19 | worktree-per-worker isolation | engine self-repair |
| T1-20 | reap settles verify-fail promptly | engine self-repair |
| T1-21 | verify runs in worktree as one script | engine self-repair |
| **T3-03 / T3-04** | **real tools** (verify-provenance, style-check) | **actual product — and both got eaten by engine bugs, then hand-rescued** |

So each run's "output" is not a delivered thing — it's *another bug discovered in the engine*.
That is exactly why it feels like no progress and no clear instruction: **the ground shifts
under you every single run.**

## Why the *instructions* specifically are never clear

The run interface changed **three times in one day**:

1. `POOL=2 bash engine/run.sh` (env-var form)
2. → `./run.sh 2` (positional form, after a DX complaint)
3. → the seat handing over `python3 ../bin/promote-wargame.py go T1-21` (raw, cwd-trap-prone,
   rejected by David as unusable) — the ask now is a clean `/factory t1-21` wrapper.

Plus: the `/factory` console skill was **built this same morning**, and the 2026-07-10 handover
**contradicted the disk** (claimed T1-15 pending; it was already done). **You cannot get stable
instructions from an interface that is still being poured.** The map keeps disagreeing with the
territory because both are being drawn while you walk.

## What the pool=2 proof actually showed (the good news underneath)

The mechanism is *sound*: parallelism, worktree isolation (T1-19), independent re-verify at reap
(`verdict_source=engine` — the engine correctly caught workers claiming done when checks
disagreed), and no-spin retries (T1-20) **all held under real concurrency.** The engine's bones
are good. What's missing is *finish* and *stability*, not correctness.

## Recommendation — stop drilling two holes at once

1. **Land T1-21, then declare an engine moratorium.** No more `T1-xx` engine tickets for a
   defined stretch. The machine is ~70% scaffolding; it needs to become *boring* before it's useful.
2. **One command, then leave it alone.** Settle on `/factory <ticket>` (or `./run.sh`) as THE
   surface and freeze it. Every interface change costs a fresh round of "wait, how do I run it."
3. **Drain only *product* tickets at pool=1** — real tools, real artifacts (the `T3-xx` family) —
   until you can watch value flow end-to-end without an engine bug eating it. Parallelism was a
   *proof*, not a need; it can wait behind the moratorium.

## What "done with this note" looks like

- T1-21 dispatched, reaped engine-verified, and the `## Verification` line-in-separate-shell bug +
  worktree-stranding both confirmed fixed by a clean pool=1 product-ticket run.
- A single, frozen run command documented in one place.
- The next 3–5 tickets are product, not engine. If an engine bug surfaces, **ticket it and keep
  draining** — don't drop back into engine-repair mode mid-drain.

## Caveats carried forward (from today)

- **Ledger vs location mismatch:** `T1-16` durable ledger records T3-03/T3-04 as `fail`, but they
  now sit in `done/`. The seat correctly overrode a *proven false-negative* with independent proof
  (tool self-tests 11/11 + 15/15) — but record "engine false-negative, manually verified" in the
  ticket/ledger so a future reader doesn't read it as a contradiction.
- **Interface authority rule (settled today):** David runs dispatch commands in his own terminal;
  the seat only *emits* the command, never runs it. (`feedback_engine_run_command.md`,
  `feedback_po_seat_never_builds.md`.)

---
*If you're the next factory seat reading this on activation: this is an advisory from the
Chaperone, non-blocking. Weigh it, but David decides. The recurrence signal is the point —
"engine self-repair keeps eating product work" has now been the shape of multiple sessions.*
