# Factory Map v1 — spec (goal-ready)

**Date:** 2026-07-11 · from the stabilise-before-drain moratorium ([[ADR-0045]]).
**One-line purpose:** kill *"I don't know what we're building"* — one legible view of the whole Dark
Factory: every pipeline, its status, its gaps, and how the pieces fit.

## Decisions (locked, 2026-07-11 interview)
- **Form:** a **Mochaccino design** (in the existing gallery, AppyDave brand, rendered by Mocha; data in `mochaccino/data/`). Refreshes/supersedes the stale `01-pipeline-overview`.
- **Altitude:** **both, layered** — a status board on top, an architecture layer underneath.
- **Data source:** **curated snapshot for v1** (hand-placed from real backlog + KDD, true as-of-today). Auto-feed is a deferred future ticket (ADR-0030: hand-write N=1 first).

## Stack
Mochaccino design: `mochaccino/data/factory-map.json` (Peter) → `mochaccino/designs/10-factory-map/index.html` (Mocha), AppyDave brand + the copy-kit components. Served on `:7420`.

## In scope (v1)
1. **Status board (top layer)** — the ~9 tracks as swim-lanes/cards:
   `T1 engine · T2 producer/BA · T3 ingestion · T5 watchtower · T6 constellation (micro-apps) · T7 self-learning · T8 doc-truth · T9 voice/comms · T10 fleet`.
   Each card: name, one-line purpose, a status rollup (done / in-progress / ready), and **red gap markers** for unbuilt pieces.
2. **Architecture layer (underneath)** — how the pieces fit: the constellation 3-layer stack (data → surfaces → KBDE host) + engine/comms/micro-app relationships, grounded in `docs/constellation-map.md`.
3. **Gaps in red, sourced from the KDD** — at minimum: HITL/ratification pipeline unbuilt (ADR-0045 + learning), style-check coherence gap, on-machine parallel uncertified, verify/authoring fragility (now guarded). Each red marker cites its KDD entry.
4. **Truth-checked** — track status cross-checked against `promote-wargame --list`; gaps against `docs/kdd/`.

## Out of scope (v1)
- Auto-feeding from disk (a later ticket). - Per-ticket detail (it's a map, not the backlog). - Interactivity beyond scan + the standard copy-kit. - Editing state from the page.

## Definition of Done
- The design renders at `:7420/designs/10-factory-map/`, in AppyDave brand, showing all 9 tracks (status + red gaps) **and** the architecture layer.
- David can answer, without opening the backlog: *what's built · what's in progress · what's missing · how it fits.*
- Passes `design-lint` (the taste self-check).

## Acceptance criteria
- [ ] All 9 tracks present; status accurate vs `promote-wargame --list`.
- [ ] Every KDD-recorded gap appears as a red marker citing its entry.
- [ ] Architecture layer reflects `docs/constellation-map.md`.
- [ ] Brand-compliant; registered in the mochaccino gallery index; `01-pipeline-overview` noted as superseded.

## Key references
- `backlog/wargames/README.md` — the T-track structure + live status.
- `docs/kdd/` (index, ADR-0045, the 2026-07-11 learnings) — the gaps.
- `docs/constellation-map.md` — the architecture layer.
- `mochaccino/` — the design system, Mocha renderer, `01-pipeline-overview` to supersede; `appydave:mochaccino` / `appydave:mocha` / `appydave:peter` skills.

## /goal condition (paste-ready)
> Build the Factory Map v1 as a new Mochaccino design `10-factory-map` per `backlog/2026-07-11-factory-map-spec.md`. Two layers in one AppyDave-brand page: (top) a status board of the 9 Dark-Factory tracks (T1 engine, T2 producer, T3 ingestion, T5 watchtower, T6 constellation, T7 self-learning, T8 doc-truth, T9 voice, T10 fleet) each showing purpose + a done/in-progress/ready rollup + red gap markers; (bottom) an architecture layer showing the constellation data→surfaces→host stack. Curated snapshot only — hand-place status from `promote-wargame --list` and gaps from `docs/kdd/` (HITL unbuilt, style-check coherence gap, parallel uncertified), each red marker citing its KDD entry. Data in `mochaccino/data/factory-map.json`, view in `mochaccino/designs/10-factory-map/index.html`, register it in the gallery, note `01-pipeline-overview` superseded, and it must pass design-lint. Done = David can see what's built / in-progress / missing / how it fits without opening the backlog.
