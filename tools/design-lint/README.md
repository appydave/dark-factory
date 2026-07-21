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

## Setup (required — the tool cannot run without this)

Playwright is **not** available on the system python (homebrew 3.14 is PEP-668 externally-managed).
It lives in a local venv:
```bash
python3 -m venv tools/design-lint/.venv
tools/design-lint/.venv/bin/pip install playwright
tools/design-lint/.venv/bin/playwright install chromium
```
Always invoke via `tools/design-lint/.venv/bin/python`, never bare `python3` — bare `python3` fails
with `ModuleNotFoundError: playwright`. This exact failure silently voided the gate once already
(see "History" below).

## Two modes

**A. Inline gate (one render).** After a render, screenshot it and run the lint agent:
```bash
tools/design-lint/.venv/bin/python tools/design-lint/shoot-one.py \
  http://localhost:7420/designs/<id>/ --out tools/design-lint/out/lint --full
# then a lint agent Reads the PNG + RUBRIC.md and returns the JSON verdict
```
⚠️ **Shoot mochaccino designs via their `:7420` URL, not a file path.** `shoot-one.py` serves the
page's *own* directory, so a design referencing `../components/copykit.{css,js}` 404s those assets
and you lint an incompletely-styled page. (Fix would be a `--root` flag; not built.)
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

The cortex "brain" screens — see `out/lint-v4/verdicts.json` (cortex-brain-v4 gate, 2026-06-12) and
`out/lint-v5/` (correctness pass, 2026-06-15, with per-page + index shots). Verdicts land in versioned
`out/lint-vN/` dirs, not the `out/lint/` default.

## History — the gate that didn't run (2026-07-11 → corrected 2026-07-21)

Commit `76e2512` (Factory Map v1) claimed the design **"passes the design-lint taste check."**
It did not: playwright was missing, `shoot-one.py` crashed on import, and a screenshot was eyeballed
manually instead. The gate never executed. Caught by the Chaperone (advisories 0019/0020).

Corrected 2026-07-21: venv installed, gate run for real on `11-factory-map`. **Real verdict = `flag`**
(`amber-orange-on-brown` — `#c8841a` used as title accent / kicker / track IDs / badge fills on cream,
where `docs/david-design-patterns.md` restricts it to 01/02/03 numbered sequences). See
`out/lint/11-factory-map.verdict.json`.

**The lesson is the tool's own rule:** a gate that cannot run is not a gate that passed. If the
screenshotter errors, the DoD is UNMET — never substitute a manual eyeball and report it as the gate.
