# Unknowns Map — blindspot pass for the war-game portfolio

**Date:** 2026-07-06 · Phase 0 output. Companion: `path-map.md`.
Classification per Thariq's quadrants. Only items that change WHICH tickets get written (or how
they're war-gamed) reach the interview; the rest become recon moves or flagged assumptions
inside individual war games.

## A. Portfolio-shaping forks → INTERVIEW (answers change the whole ticket mix)

1. **Path 1 vs Path 2 rebalance.** North-star froze Path 2 (content/cargo) behind Path 1
   (machinery). Machinery is now largely built and hardened. Does Path 2 unfreeze, and at what
   weight? The factory has shipped 0 of its 1,100-artifact cargo in 7 weeks.
2. **Ingestion ambition.** Proof-of-one, full campaign (tooling + clusters + evals), or stay
   parked?
3. **Switchboard state-authority fork.** Marshall-session event-log replay vs DF-7 durable
   Switchboard state plane. Blocks auto-wake v2, DF-7, and the greenfield charter (which may
   never have been written — recon needed).
4. **App-build doctrine.** Engine-Swagger-ticket vs Ralphy campaign vs Osmani-spec-first for
   constellation app work — recurring unresolved fork; determines the FORMAT of every
   app-building war game.
5. **YLO→POEM in or out** of the 100 (blueprint unratified; .poem/ rebuild is the archive
   trigger for YLO).
6. **Watchtower ambition.** Real web app vs terminal + static Mochaccino boards.
7. **Human-comms/voice priority.** Samantha + audio-out in the portfolio or parked?
8. **Fleet scope.** This-machine-only, +Roamy, or full fleet?
9. **War-game depth split.** Top-50 full / top-30 extra-deep + rest brief / all-100 medium.

## B. Track-blocking decisions → interview quick-fire, or ticket-as-decision-war-game

- Reaper stuck-case ownership: AngelEye (session) vs AppyRadar (process) vs both.
- Capture service: new standalone app vs fold into AppyRadar vs shared lib; naming; machine.
- The 14 corpus-modeling questions A–N (gate Phase 4/5 at scale; most consequential: .tmpl vs
  compiled tracking, sub-artifact files first-class?, POEM's missing "Alec", Ruflo's 305 MCP
  tools in scope?).
- Blueprint §9's six POEM questions (Agent Engineer naming, projection ownership,
  QuickArchitect output shape, validator placement, kie.ai MCP-vs-skill, .poem/ layout).
- BA agent internals (contract pinned, mechanism open).
- Intake: physical home, capture surface, triage ownership.
- Tool-registry refresh cadence (a live cron is a standing commitment — needs explicit go).
- Two "decision queue" concepts (Watchtower curation vs engine HITL) — reconcile or keep split.

## C. Defaults already picked → bulk-accept candidates (one interview question)

- design-lint → fold into Mochaccino/Shelly (standing recommendation 2026-07-06).
- First ingestion: name `review-dimensional`; complement (don't replace) existing review
  skills; leave `delivery-review` orchestrator as-is.
- DF-ADR nested provenance: flatten to Lisa's emit convention.
- Retire Penny/Alex/Oscar naming from architecture.md (superseded by Marshall/Swagger).
- Fix CLAUDE.md's stale phase-b "START HERE" activation pointer.
- Session 1 = harvest+draft, Session 2 = voice-review+ratify (HITL pause before ratification).

## D. Verify-don't-ask → recon moves inside war games (docs can't be trusted on these)

- Anything harness-evaluation/six-app-eval claims is missing (much has since shipped).
- Was the Switchboard greenfield charter ever written? Is Switchboard up right now (contradictory
  claims: live on Roamy :5099 on 07-02 vs "DOWN" in CLAUDE.md)?
- Did mocha-census bench mode / export-to-file / generator-seam actually land?
- Does run-next-workflow/SKILL.md exist? Is the 60GB RAM-leak claim real (never verified)?
- external-research tickets: answered in-house 07-06 — confirm done/ state matches backlog docs.
- kdd-viewer search state after ticket #7; project-digest --list after the deferral.
- M4 Pro "Warehouse Keeper" cron: was it ever set up?

## E. Unknown unknowns surfaced by the readers (things nobody was tracking)

- **Docs-lag-code as a systemic class**, not an instance — the factory has no "doc truth
  reconciliation" mechanism (T8; sop-lifecycle's drift problem applies to its own docs).
- **Name-collision invisibility class** — new tools losing NL-resolution to old registered
  skills; two instances found empirically; no sweep exists for the other ~40 apps.
- **LLM-judge calibration (Gap B)** — census/triage/design-lint all run uncalibrated judges
  while David's human labels sit unused as a calibration set. Cheap, high-leverage.
- **Golden-job regression suite (Gap A)** — machinery changes ship with zero replay gate.
- **learning.yml taxonomy** — central to intake.md's design, referenced nowhere else, never
  built; the validation-gate discipline (SkillOpt) currently has no enforcement point.
- **`com.appydave.omi-sync` silently failing on every scheduled run** — known, unactioned.
- **Sentinel blind to Roamy** — fleet liveness data is currently untrustworthy and quietly
  consumed anyway.
- **Engine store grows forever by design** — no retention/pruning policy anywhere (also true
  of Switchboard's event log).
- **Stale project memory** — this session's own auto-memory still described the dead
  /loop+mutex trigger architecture; memory needs the same reconciliation discipline as docs.
