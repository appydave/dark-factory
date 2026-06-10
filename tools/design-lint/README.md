# Design-Lint — the post-render self-check (the "design-loop pass")

A reusable Dark Factory tool that **screenshots a rendered design/slide and critiques it against
David's design spec before he ever sees it.** It closes the hole that let four brand-cold cortex
screens ship: the Mochaccino / comprehend render loop had *no* automated check on its own output —
the only review step was human (`review` mode). This is the machine half of that review.

It is the active-machinery form of the taste loop: *render → **lint** → (revise) → human-rate*. Where
Mocha Census is the **human** taste board, design-lint is the **machine** pre-filter.

## The two halves

| half | what | how |
|---|---|---|
| **mechanical** | screenshot the output | `shoot-one.py` — serves the page on a throwaway port, Playwright PNG (reuses the mocha-census pattern) |
| **judgment** | critique the screenshot | a **lint agent** applies `RUBRIC.md` → structured JSON verdict (`pass`/`flag` + flags). Model-judged, not regex — "is this colour on content or structure?" needs vision |

## What it flags (and what it deliberately does NOT)

Four **reliable** failures only — the ones David names repeatedly (see `RUBRIC.md`):
- **F1 `cool-on-content`** — cool semantic colour dominating *content* cards that aren't diagram nodes.
- **F2 `missing-warm-anchor`** — no bright warm anchor (yellow `#ffde59`); screen reads cool/grey, off-brand.
- **F3 `amber-orange-on-brown`** — muddy amber/orange as fill/text on brown/beige.
- **F4 `colour-overload`** — too many competing / too-saturated colours, or one hue flooding the screen,
  so colour *shouts over the content* (the #1 failure across the 103-slide round). A loudness judgment,
  **never a colour count**.

**Guardrails (critical):** flags only — no auto-fix. **Never** policing diagram/colour *counts* (that was
the round-04 Goodhart mistake). Cool semantic colour on genuine structure is correct and is **not**
flagged. When in doubt, don't flag.

## Two modes

**A. Inline gate (one render).** After a render, screenshot it and run the lint agent:
```bash
python3 tools/design-lint/shoot-one.py path/to/index.html --out tools/design-lint/out/lint
# then a lint agent Reads the PNG + RUBRIC.md and returns the JSON verdict
```
A `flag` verdict surfaces to the caller (Shelly / Marshall) to revise or escalate — it does not block.

**B. Batch audit (a deck / a set).** Screenshot N pages, then pipeline each through the lint agent.
This is the natural `workflow.js` fan-out (one critique agent per page, in parallel). Use it to audit a
whole slide deck or all designs in a repo. (Workflow not built yet — see "Next".)

## How it plugs in

- **Source of truth** for the rules is `docs/david-design-patterns.md`; `RUBRIC.md` is the operational
  extract. Keep them in sync — when the spec sharpens, update the rubric.
- **Wiring into Shelly** (the Mochaccino design specialist, in `appydave-plugins`) is the intended home
  for mode A — Shelly renders, then self-lints against her own gate. That edit touches David's tracked
  plugins repo, so it is a **separate, asked-for** step, not done here (dark-factory stages first).

## Next

1. `design-lint.workflow.js` — the batch fan-out (mode B), with the lint agent as the per-page stage.
2. Wire mode A into Shelly's render step (after sign-off).
3. Feed confirmed flags back as negative exemplars alongside the Mocha Census love-tier pack.

## Proven on

The four cortex "brain" screens (2026-06-10) — see `out/lint/` and the proof run recorded by Marshall.
