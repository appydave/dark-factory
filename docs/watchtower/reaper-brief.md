# Reaper — design brief (converged 2026-06-07)

*First output of the **fragment→convergence funnel**: scattered reaper fragments (the live-fire finding, the observers-answer frame, the harness-driven-cleanup doctrine, the two-case split, AppyRadar (was "AppyCtrl" — corrected 2026-06-10, see docs/appyradar.md)/AngelEye liveness) synthesized into one cohesive brief that drives the build.*

## Problem
Swagger windows strand: a Swagger finishes (or hangs) and its tmux window stays alive, idling at the REPL. Manual reaping has failed repeatedly (Marshall forgetting; Swagger self-close has no permission). Orphans accumulate → fragile loop.

## What we learned (don't repeat)
- **Process-tree detection is a DEAD END** (live-fire 2026-06-06): Claude Code v2.x reparents the `claude` session to the `claude daemon`, so it is NOT under the tmux pane — BFS from the pane finds only MCP servers. `proof/reaper-livefire-finding.md`.
- **Cleanup is harness-driven, not remembered**: detect → tell → reap. Self-action fails both ways (Marshall forgets; Swagger can't kill itself).

## Frame
**Observers answer; the floor acts.** Sentinel apps (AngelEye, AppyRadar, Switchboard) are queryable sources of truth — they don't kill. **Marshall's privileged Monitor reaps** (it alone holds tmux perms). David confirmed: Marshall's Monitor runs the reaper.

## Two cases (split the problem)
1. **Common — finished-but-open** (the orphan we keep hitting): the handback landed in `reports/` (job done) but the window is still open. **Signal = engine state** (the engine's own artifacts). No process detection, no AngelEye needed. **← BUILD NOW.**
2. **Stuck — no handback** (hung mid-job): no engine signal exists. Needs **session liveness** — query AngelEye (claude-session last-active) and/or AppyRadar (process/tmux state). **← DEFER** until AngelEye live-hook + AppyRadar-state exist.

## Decision (v1 = engine-state reaper)
Build the **engine-state reaper** now; defer the stuck-case.

**Runtime owner:** Marshall's persistent Monitor (privileged, in Marshall's session).
**Builder:** Marshall, inline — it's Marshall's own capability (a Monitor command, no Swagger artifact to hand back).

### The missing primitive: a dispatch registry (window ↔ queue_id)
The reaper must map a handback (`queue_id`) → its tmux window. Window names (`swagger-board-v2`) don't equal queue_ids (`q-20260606-board-v2-lanes`), so we need an explicit link. **On dispatch, Marshall records `{window_name, queue_id, started_at}`** to `experiments/watchtower-engine/registry/<window>.json`. Bonus: this also satisfies the "every live Swagger is identifiable/explainable" rule (swagger-lifecycle backlog).

### v1 spec
- **Dispatch (Marshall):** when spawning `swagger-<slug>` for `queue_id X`, write `registry/swagger-<slug>.json = {window, queue_id:X, started_at}`.
- **Reaper (Marshall's Monitor):** watch `reports/` for new handbacks. On handback for `X`: look up its window in the registry; wait a **grace period (default 60s** — allows rule-5 follow-up talk); if the window still exists → `tmux kill-window`; deregister; emit one line `reaped <window> (job done)`. If the window is already gone (Marshall closed it on the happy path) → no-op, deregister.
- **Idempotent + safe:** reaping an absent window is a harmless no-op; replays/dupes don't matter.

### Test plan (live)
Dispatch one quick real job → it finishes (handback lands) → confirm the reaper auto-closes its window after grace, registry cleaned, 0 orphans. This tests the reaper AND exercises the loop.

## Explicitly out of scope (v1)
Stuck/no-handback detection (→ AngelEye/AppyRadar liveness, later); Switchboard-emits-`session.reapable` SRP-purist variant (more moving parts than v1 warrants — Marshall's Monitor reads engine state directly for now).

## Open questions
- Grace period: 60s a good default? (tunable)
- Registry: per-window files vs one `registry.json`? (per-window = simpler atomic writes/deletes)
- Should the happy-path close ALSO deregister, so the registry is always truthful? (yes)
