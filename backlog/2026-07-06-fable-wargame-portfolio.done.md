# Fable War-Game Portfolio — mint ~100 executor-ready tickets before Fable leaves subscription

**Date:** 2026-07-06 · **Deadline:** ~24h (Fable access window)
**PO:** David · **Dev:** Fable session in dark-factory

## Goal

Use Fable's remaining window to produce a portfolio of war-gamed tickets that the
engine's sonnet workers (`engine/orchestrator.py`) can execute for months after
Fable is gone. War game ≠ plan: every move carries expected observation, failure
signal, counter-move; forks carry triggers; each ticket ends with assumptions +
abort conditions + verification steps, written for a sonnet-class executor.

Technique sources: Thariq's "Field Guide to Fable" (blindspot pass, interview,
assumptions ledger) + the war-game prompt pattern (action/reaction/counteraction,
fork triggers, abort conditions, executor-model tailoring).

## Phases

| # | Phase | Who | Output |
|---|-------|-----|--------|
| 0 | Recon + blindspot pass | Fable + reader subagents | `plans/wargames/path-map.md`, `plans/wargames/unknowns-map.md` |
| 1 | Interview (architecture-changing unknowns only) | David + Fable | answers folded into path map; skipped Qs → `plans/wargames/assumptions-ledger.md` |
| 2 | Candidate generation (100+, one paragraph each) | Fable fan-out | `plans/wargames/candidates.md` |
| 3 | Triage board (build-now / later / kill) | David | rated candidate list |
| 4 | Deep war-gaming of survivors (~40–60) | Fable Workflow fan-out | `backlog/wargames/<slug>.md` + thin JSON ticket per war game |
| 5 | Wire-up: promotion script + drain order | Fable | `bin/promote-wargame.sh` (or py), ordering doc |

## Decisions locked

- Do NOT deep-war-game all 100 — candidates are cheap, war games are expensive;
  triage gates the spend.
- War games written for **sonnet** executor in the engine's ticket idiom
  (`engine/store/queue/*.json` referencing the war-game md).
- Assumptions David doesn't resolve get flagged in the ticket, surfacing at run
  time through the engine's `needs-decision/` HITL gate.
- Progressive drain, not bulk-drop — CAP/429 governor already paces the pool.

## Status

- [x] Phase 0 recon DONE (2026-07-06) — 4 reader passes; outputs `plans/wargames/path-map.md`
      (10 tracks), `plans/wargames/unknowns-map.md`, `plans/wargames/interview.html`.
      Headline: docs lag code — harness-eval promotion plan + most six-app-eval High items
      already shipped into `engine/`; every war game gets verify-on-disk recon moves.
- [x] Phase 1 interview DONE (2026-07-06) — all 10 answered; locked in
      `plans/wargames/decisions.md`. Headlines: ingestion = full campaign; YLO parked;
      everything executes through the engine; Watchtower = real app; +Roamy; all
      defaults accepted; top ~50 fully war-gamed.
- [x] Phase 2 candidates DONE — 110 candidates across 9 tracks in
      `plans/wargames/candidates.js` (T4 removed), pre-sorted NOW 28 / NEXT 29 /
      LATER 52 / KILL 1.
- [x] Phase 3 triage DONE (2026-07-06) — David accepted the pre-sort intact:
      NOW 28 / NEXT 29 / LATER 52 / KILL 1 (Board v6 Map view).
- [x] Phase 4 deep war-games DONE — 57/57 authored by parallel Fable agents
      (~65 min, 6.2M subagent tokens). `backlog/wargames/<ID>-<slug>.md` +
      `backlog/wargames/tickets/<ID>.json`. Lint clean; 3 depends_on refs fixed.
- [x] Phase 5 wire-up DONE — `bin/promote-wargame.py` (dependency-aware,
      self-hosting-ticket refusal, --list/--next) + `backlog/wargames/README.md`
      (index, headlines, per-ticket flags, systemic warnings).

## Summary (end of session)

Fable's 24h window converted into a 57-ticket war-gamed portfolio the sonnet engine
can execute for months: Phase 0 four-reader recon (headline: docs lag code) →
interview (10 decisions) → 110 candidates → David's triage → 57 full war games +
staged engine tickets → promotion tool. Systemic findings the authoring surfaced:
WORKER_TIMEOUT=240s too short for war games (use --max-wall 3600), five self-hosting
tickets must run attended, T1-02 saturation blocks David's own usage (parks on a
go-decision), two latent engine defects (declined HITL tickets strand in running/;
corrupt decision file silently approves). Start with:
`python3 bin/promote-wargame.py --next 3`.
