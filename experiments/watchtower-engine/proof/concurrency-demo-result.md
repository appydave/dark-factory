# Proof — concurrent Swaggers (first N>1 real-session run)

**Date:** 2026-06-06 · **Run by:** Marshall (session 7) · **Goal:** prove the dispatch loop runs more than one Swagger at once (North-Star "more than one process at a time"). Single-Swagger was proven (C3a/C3b/C3-close); N>1 real sessions had never been demonstrated.

## What ran
3 `kind:instruction` tickets (`q-20260606-conc1/2/3`) placed in one `queue/`. 3 Swaggers spawned near-simultaneously (`tmux new-window` → interactive `claude`, non-bypass), each running `run-next-workflow`. The atomic `rename(2)` claim distributed the tickets.

## Result — PROVEN
- **3 distinct sessions, 1 ticket each, no collision, no double-run:** 3 tickets → exactly 3 `done/` + 3 `runs/` + 3 `reports/`. Artifacts have different phrasing/structure = 3 independent authors.
- **Genuine concurrency (real filesystem mtimes, not self-reported):** all output landed in a **22-second window** (18:09:07 → 18:09:29) with stages **interleaved across tickets** (proof1, proof2, proof3, run1, run2, report1, run3, report2, report3) — not grouped ticket-by-ticket as a sequential drainer would produce.
- **Clean teardown:** all 3 windows reaped by name; 0 swagger windows left, `running/` empty.

## Lessons (robustness / methodology)
1. **Self-reported agent timestamps are fiction.** I told the Swaggers not to call `date` (to avoid a permission-prompt hang), so they *invented* ISO timestamps (`17:41/17:42/17:45`, falsely sequential). Real timing must come from a real clock — allow `date` in the boundary, or have the engine stamp times. Don't trust in-artifact timestamps as proof.
2. **Identical jobs are visually indistinguishable.** All 3 windows ran the same instruction, so they "looked like the same session three times" (David's observation). Concurrency without a visual layer reads as duplication → this is the concrete case for **Watchtower** (a board: Swagger N → ticket N), not reading raw transcripts.
3. **Reaping was still manual** (Marshall killed the 3 windows after verifying). The harness auto-reaper (`session.stale` → Marshall Monitor) is still owed — see `backlog/concepts.md`.

## Not yet proven
- Timing-overlap measured with a *real* clock.
- Auto-reaper (this run reaped manually).
- Scale beyond one machine (M4 Mini over Tailscale).
