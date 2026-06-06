# 2026-06-07 — day possibilities (could, not will)

**Throughline:** *test + evolve the factory loop by running REAL work through it.* Every dispatch teaches us (this weekend's taught: concurrency works ✅, the reaper detector is broken 🔴, AngelEye was off 🔴). Pick work → dispatch → harvest the findings.

**Start state (preflight):** Switchboard ✅ · AngelEye ✅ (backfill only, no live hook) · Watchtower board ✅ · AppyCtrl ❓

## The menu (grouped)

**Robustness — harden the loop**
- **A. Engine-state reaper** (Marshall's Monitor): handback landed + window still open after grace → reap. No new deps. Kills the orphan we keep hitting. 🟢 RIPE
- **B. Real-clock fix** for Swagger timestamps (capability-placement: time from OS, not the model). Small.

**Constellation — observe & query**
- **C. AppyCtrl investigation** (its own window): what it is, can it own tmux/process state as a queryable source (window→liveness home). Foundational for the reaper's stuck-case. 🟡 (David-driven)
- **D. AngelEye live-hook wiring** (built IN AngelEye): real-time events, not just backfill; unblocks reaper stuck-case. Fix the :5501→:5051 doc drift there too.
- **E. AngelEye MCP server** (built IN AngelEye): so Marshall/skills query it conversationally. (API for harnesses, MCP for agents.)

**Work-pipeline — dogfood the new ideas**
- **F. Converge the "reaper cluster"**: test the fragment→convergence funnel — turn {observers-answer, AppyCtrl-state, engine-state, AngelEye-liveness} into ONE brief, then dispatch it. Produces A as output. 🟢 RIPE (meta-test)
- **G. Run real backlog work through the loop** (multi-Swagger): the actual stress-test of "test + evolve the loop."

**Visual — Watchtower**
- **H. Board v4:** Floor↔Lanes bridge (promote a lane item → a floor job) | brand skin | SSE live updates. Pick one.

**Storytelling**
- **I. Chronicle first cut:** retrospective-mine today's transcripts into a narrative (end-of-day).
- **J. Story-beat capture:** cheap real-time markers (a hook or `story.*` event).

## A coherent "could look like" arc
1. **Converge the reaper cluster** (F) → one brief = first real use of the funnel.
2. **Build/dispatch the engine-state reaper** (A) from that brief = robustness win + loop test.
3. **AppyCtrl investigation** (C, own window) = unlock the stuck-case + the tmux-state query.
4. Depending on C → **AngelEye live-hook / MCP** (D/E, in AngelEye).
5. **Run real backlog work through the loop** (G) = stress-test + evolve.
6. **End of day: Chronicle mine** (I) = the day's story.

## Persistence plan
Continuous capture is working (memories/concepts/build-state/proof/git). Add: **periodic consolidation** when a cluster ripens (converge scattered captures → a coherent brief), and the **Chronicle** as the narration layer. Trigger remains the weak link (manual); the session-end sweep is the ritual.
