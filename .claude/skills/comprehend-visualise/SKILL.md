---
name: comprehend-visualise
description: "Use when pointing the factory at a codebase or prose to produce a provenanced Mochaccino visual — 'visualise this repo / conversation / doc', 'comprehend and visualise X'. A THIN caller: comprehend a target → Mochaccino-ready data + provenance, hand off to Mochaccino to render, and record run-state. Holds NO design or render rules — shape/look judgment is Shelly's, inside Mochaccino."
---

# comprehend-visualise — the factory's comprehend caller for Mochaccino

A **thin mechanism, not a design engine.** It does three honest jobs and nothing else:

1. **Comprehend a target → data** — read the target and produce a Mochaccino-ready *cited* model.
2. **Provenance** — stamp `meta.source` = target path + `commit_sha` so the visual is refreshable.
3. **Run-state recording** — record success / failure / state to the failure register + run logs.

It then hands off to **Mochaccino** (`appydave:mochaccino`), whose **comprehend → visualise mode** owns the actual visual: Peter shapes the data, **Shelly decides shape-or-not** (her graphics-warrant gate — default HTML, a diagram only where a flow/topology genuinely warrants one, sparingly), Mocha renders.

> **This skill holds NO design/render rules.** It never tells the renderer how to look — no shape levers, no diagram mandates, no taste-spec conditioning. All of that lives in **Mochaccino / Shelly**. Encoding render rules here is the exact defect that caused the SVG over-rotation — see `backlog/2026-06-09-mochaccino-consolidation-requirement.md` and memory `shapes-are-annotation-not-the-medium`.

## The one rule it owns — DATA-FIRST + PROVENANCE
No handoff before real DATA exists. Target → cited model → `.mochaccino/data/NN-*.json` with `meta.source` = target path + `commit_sha`. Then Mochaccino renders. A hand-drawn mockup ahead of data is a defect (`structure-first-then-render`).

## Procedure
0. **Orientation** — is there a `.mochaccino/` workspace here? Report state + a recommendation, not a menu.
1. **Scenario** — absorb target + intent + output location + audience.
2. **COMPREHEND → DATA:**
   - **prose target** → read it directly.
   - **codebase target** → run the comprehend fan-out workflow `comprehend-fanout.workflow.js` (parallel *cited* readers per subsystem + `git log`) → ONE cited model.
   - Write `.mochaccino/data/NN-*.json` with `meta.source` = target path + `commit_sha`. **No render here. Do NOT pre-pick shapes.**
3. **HAND OFF to Mochaccino** — invoke Mochaccino's *comprehend → visualise* mode on the data. Mochaccino runs the shape brief (**Shelly: shape-or-not, default HTML**), Peter finalises data, Mocha renders + serves + regenerates the gallery. Positioning-for-audience and all look/shape decisions are Mochaccino's, not this skill's.
4. **RECORD run-state** — on completion, record outcome externally: success/failure + key facts to the run log, and on failure call `experiments/watchtower-engine/failures/record-failure.sh`. Never trust the worker's self-report — record from outside the job (DF-3, memory `factory-operations-telemetry`).

## What this skill is NOT
- **NOT** a renderer, shape-picker, or taste authority. Shelly + Mocha own the look; `docs/david-design-patterns.md` is guidance **Shelly** consults, never consumed here.
- **NOT** a duplicate of Mochaccino. It only ADDS: comprehend-a-target → data, provenance, dispatch, run-state recording (memory `its-mochaccino-not-comprehend-visualise`).

## Form (from Millwright)
Thin SKILL (this caller) + WORKFLOW.js (`comprehend-fanout.workflow.js`, the parallel comprehend burst) → hands to the **Mochaccino** engine (Peter / Shelly / Mocha). The skill is mechanism + provenance + state; **all design judgment is Mochaccino's.**
