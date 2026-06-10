# PLAN — Comprehend→Visualise running inside a Dark Factory process

**Date:** 2026-06-07. **Companion to:** `2026-06-07-comprehend-visualise-process.md` (the what/why). This = the how/sequence.
**Acceptance test:** point the factory at `~/dev/kybernesis/cortex` (M4) → autonomous, provenanced visualisations of the ~8-package / 4-DB system, served, refreshable.

## Verdict: possible, and mostly glue
All engines exist + proven (comprehension fan-out · Peter/Shelly/Mocha · the queue/dispatch/reaper loop · M4 reachable with claude+Mochaccino+cortex present). The only NEW risk is small and front-loaded: (a) **autonomous (non-interview) Mochaccino**, (b) **cross-machine** execution.

## Two forks — my recommendation (decide before Phase 1)
1. **Where it runs:** **on the M4, as a Swagger** (code + Mochaccino + claude are all there; Mochaccino renders where the code lives; avoids dragging a repo over SSH). Cross-machine dispatch is then the thing we prove. *(Alt: read cortex from Roamy over SSH, render locally — rejected: slower, loses "factory works anywhere.")*
2. **v1 mechanism:** **a Swagger running a `comprehend-visualise` SKILL — NOT the formal Workflow tool yet.** Prove the glue end-to-end first; add `workflow.js` parallel fan-out in Phase 5 once the recipe is settled. (Smallest move; honours "exploration first, automate once settled.")

## Phases

### Phase 1 — The `comprehend-visualise` skill (the fs-aware wrapper)
The human-facing / filesystem-aware layer that a Swagger runs. Inputs: `{target repo, intent, output location}`. It:
- Enumerates packages / databases / key components; reads `git log` (last 2 weeks).
- Fans out parallel readers (one per package/subsystem) → a single grounded, cited **comprehension digest**.
- Decides candidate shapes (architecture→layer-stack, packages→card-grid, schemas→matrix/ER, git history→timeline, flows→lifecycle-flow).
- Emits a clean **brief** (file list, what each is, chosen shapes, output location) — the `args` packet for the render step.
**Done:** running the skill against cortex produces the digest + brief (no rendering yet). Proves comprehension.

### Phase 2 — Autonomous Mochaccino render (non-interview)
Drive Peter→Shelly→Mocha from the brief, headless:
- **Peter** writes `data/*.json` with `meta.source` provenance pointing at cortex code + commit SHAs.
- **Shelly** confirms shapes; **Mocha** renders to the output location; gallery regenerated; served (:7420 on M4).
- v1 scope: ~4–6 visualisations (architecture, package map, DB/schema, one key flow, the 2-week change story).
**Done:** cortex visualisations exist + serve, each citation-stamped back to source. Proves autonomous Mochaccino.

### Phase 3 — Wrap in the factory process (the actual ask)
Make it a dispatchable job:
- Marshall writes a queue ticket `{kind: skill, target: cortex, intent, location}`.
- `dispatch-swagger.sh` spawns a Swagger **on the M4** (cross-machine) → Swagger runs the `comprehend-visualise` skill → outputs land → writes `done/` → reaper closes the window.
**Done:** one Marshall dispatch → cortex visualised end-to-end, no hand-holding. This is "running it all within a Dark Factory process." **= the acceptance test.**

### Phase 4 — Boundary HITL + refresh
- **Review:** David opens the gallery; "revise shape X / give me 10 ways of Y" = re-dispatch (exploration stays conversational + boundary-gated).
- **Refresh:** on new cortex commits, re-dispatch reading the same provenance chain → visuals stay live.
**Done:** the human-in-the-loop + refresh loop works via re-dispatch.

### Phase 5 (later, once settled) — harden + scale
- Promote the settled recipe's mechanical core to a `workflow.js` (parallel comprehension fan-out, deterministic sequencing).
- **blackboard MCP** (`bb_get/set/list/delete`, already live) as the durable store between jobs / the inspectable state layer the Workflow tool lacks.
- Cross-machine dispatch hardening; code-specific Shelly shapes (dependency graph, ER) if the existing 6–7 fall short.

## Risks & mitigations
- **Autonomous Mochaccino unproven** → Phase 2 is the isolation test; if the interview is load-bearing, the skill (Phase 1) supplies those answers as the brief.
- **Cross-machine Swagger** → prove the M4 Swagger spawn + done/ return in Phase 3; fall back to Roamy-over-SSH render if M4 dispatch is flaky.
- **Provenance across machines** → `meta.source` must cite cortex path + commit SHA, not a local absolute path.
- **Scope creep** → v1 = ~5 visualisations of ONE repo via ONE dispatch. Decks/hundreds-of-slides, FliDeck hosting, formal workflow.js = explicitly later.

## Execution topology — who does what, where (David asked)
**One Marshall — here on Roamy. No second Marshall on M4. David sets up nothing on the M4.**
- **Phases 1–2 (prove the pipeline):** Marshall drives the M4 *over Tailscale SSH* from here — SSH-spawned readers comprehend cortex, Mochaccino renders (on M4 where the code is, or reading cortex over SSH). **Zero M4 setup, zero human action.** (We already proved today that SSH-dispatched readers against M4 work.)
- **Phase 3 (unattended factory dispatch, a real Swagger ON M4):** this is the ONLY place that needs one human action, ONCE — a **permission grant on the M4** (allowlist in `~/dev/kybernesis/cortex/.claude/settings.local.json` or the dark-factory one: Read/Glob/Grep, `Bash(git *)`, Write→output, the Mochaccino skill). Reason: a Swagger spawned in a detached M4 tmux has nobody at its keyboard to approve permission prompts, so it stalls without the grant. Same one-time-grant model as local ([[watchtower-permission-model]]); Marshall **cannot self-grant** — David approves it. Marshall tees it up when we reach Phase 3, not before.
- **The brain (Marshall + queue/bookkeeping) stays on Roamy; the M4 only runs the worker.** Whether the engine/queue mirrors onto M4 or the M4 Swagger reports back over SSH = a Phase-3 detail.

## First move
Phase 1: build the `comprehend-visualise` skill and run it against cortex to produce the comprehension digest. Everything downstream hangs off that brief. **No M4 setup needed for Phase 1 — driven from here over SSH.**
