# Phase 1 interview — decisions locked (2026-07-06)

Answers from David via `interview.html`. These govern Phases 2–5.

| # | Decision |
|---|----------|
| Q1 | Portfolio mix: **Fable's call per-track** (result: ingestion largest, YLO zero — see candidates.js counts) |
| Q2 | Ingestion: **full campaign** — proof + validators + cluster distillation + rollout harness + judge calibration |
| Q3 | Switchboard state fork: **defer** → decision war-game ticket with both branches + triggers (T1-11) |
| Q4 | App-build doctrine: **everything through the engine** — every ticket written for sonnet Swagger dispatch |
| Q5 | YLO→POEM: **parked entirely** (track T4 removed, incl. the 7 cheap open loops) |
| Q6 | Watchtower: **real web app** (kanban, live agent view, bus view, curation queue) |
| Q7 | Voice/human-comms: **in** (audio-out + Samantha front door) |
| Q8 | Fleet: **+ Roamy** (Tailscale worker delegation + fix sentinel blind-to-Roamy) |
| Q9 | Parked defaults: **all accepted** — design-lint→Mochaccino/Shelly · first ingestion named `review-dimensional` · complement don't replace · delivery-review untouched · DF-ADR provenance flattened to Lisa format · Penny/Alex/Oscar retired from architecture.md · CLAUDE.md phase-b pointer fixed · harvest+draft / voice-review+ratify session split |
| Q10 | Depth: **top ~50 fully war-gamed**; rest stay one-paragraph candidates |

## Assumptions ledger (skipped / unresolved)

- Free-text "anything missed" skipped → assume reader coverage was complete; new ideas can be
  added on the triage board via notes.
- Reaper stuck-case ownership (AngelEye vs AppyRadar) not asked → war-gamed as fork inside T6-08.
- Capture-service home/name not asked → assume brief's recommendation (new standalone) with an
  abort-to-decision if David objects at triage.
- The 14 corpus questions A–N: per Q2 campaign, handled as a decision-batch ticket (T3-05),
  each with a default + trigger, not pre-answered here.
