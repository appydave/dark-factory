# Design-Lint Rubric — the post-render self-check

The judgment spec the lint agent applies to a **screenshot of a rendered design/slide**.
Source of truth for the rules: `docs/david-design-patterns.md` (the "Colour as Brand vs Colour as
Data" section). This rubric is the *operational* extract — keep it in sync with that doc.

## What this is for

Catch **brand-cold output before David ever sees it.** The render loop (Mochaccino / comprehend →
Shelly → Mocha) currently has no self-check; this is it. It runs on the *output*, not the data.

## Hard guardrails (read first — these prevent the lint becoming the next Goodhart mistake)

- **Flags only. No auto-fix, no auto-rewrite.** The lint reports; a human (or a revise step) decides.
- **Do NOT police counts.** Never flag "too few diagrams", "too many colours", "needs an SVG", or any
  numeric target. Diagram/colour counts are *descriptive, never targets* (the round-04 error).
- **Cool semantic colour is NOT a defect.** It is correct and wanted on genuine structure. Only flag it
  when it is misapplied (see CONTENT test). When in doubt, **do not flag** — false alarms erode trust.
- **Judgment over rules.** These four flags are the *reliable* failures David names repeatedly. They
  are not a maximisable scorecard. A clean design with none of these flags PASSES — say so plainly.
- **`colour-overload` is a "does it shout?" judgment, NEVER a colour count.** Never flag "too many
  colours" by counting. Flag *loudness* — colour overpowering the content. A calm multi-colour legend
  PASSES.

## The two tests (from the spec)

1. **Role** — is a coloured element *structure* (a stage / node / role / legend-key in a diagram or an
   ordered set) or *content* (a card/section you read as the substance)? Cool semantic colour is
   licensed on structure; content wants warm brand emphasis.
2. **Dominance / anchor** — warm brand (brown/cream + **yellow `#ffde59`**) should be load-bearing, with
   **≥1 bright warm anchor** per screen. Cool semantic is a sparing accent.

## The four flags (the only things this lint asserts)

### F1 — `cool-on-content`
Cool semantic colour (blue/green/purple/teal) is the **dominant treatment on content** the reader is
meant to read as substance — e.g. saturated coloured top-bars/fills/headings on the primary cards —
where those cards are NOT nodes in a diagram or steps in an ordered set.
- **Flag when:** content cards are colour-coded like a legend with no diagrammatic referent.
- **Do NOT flag when:** the colours map to a diagram on the same screen, encode an ordered sequence
  (step 1–5), or are a true pros/cons / categorical split. (Cortex *Sleeps* & *Remembers* = OK;
  *Anatomy* & *Four-memories* = flag.)

### F2 — `missing-warm-anchor`
The screen has **no bright warm brand anchor** — no yellow `#ffde59`, no warm logo/badge/CTA/ghost-text
moment — and reads cool/grey overall. AppyDave is *"warm cream default, darkness a guest"*; an all-cool
screen is off-brand even when nothing else is wrong.
- **Flag when:** scanning the screen, warm brand colour is absent or vestigial and cool dominates.
- **Do NOT flag when:** a clear warm anchor is present (yellow CTA/badge, warm header, gold/ghost text).

### F3 — `amber-orange-on-brown`
Amber/orange (`~#c8841a` and muddy oranges) used as **fill or text on brown/beige/cream** — David's #1
recurring gripe, low contrast, "reads cheap." (Amber is licensed ONLY for 01/02/03 numbered sequences.)
- **Flag when:** amber/orange text or filled boxes sit on a warm (brown/beige) ground.
- **Do NOT flag when:** the warm highlight is **yellow `#ffde59`** (correct), or amber is confined to a
  small numbered-sequence badge.

### F4 — `colour-overload`  *(the #1 failure across rated slides — 103-slide round, 2026-06-10)*
The screen uses **too many competing colours, or colour too saturated/heavy**, so it **shouts over the
content**. David's most frequent complaint: *"too many colours"*, *"too bold"*, *"too heavy"*,
*"overboard"*, *"flamboyant"*, *"childish"* — and a **single hue flooding** a whole screen (*"too much
green"*, *"purple all the way through"*). Both LOVE-tier slides won on *"never overpowering."*
- **Flag when:** many saturated colours compete with no clear hierarchy; OR one hue floods most of the
  screen; OR colour is heavy enough to pull attention off the content.
- **Do NOT flag when:** colour is restrained — few colours, softened/light, mostly-neutral ground
  (grey/cream) with a **sparing accent** — even if several semantic colours appear, as long as none
  overpowers. The winning pattern is *"everything grey, only one colour made it in."*
- **This is a loudness judgment, NOT a count.** A disciplined multi-colour legend that reads calm
  PASSES. `severity`: high when it reads childish/messy/ugly; medium when merely "a bit heavy."

## Output schema (the agent returns exactly this)

```json
{
  "verdict": "pass | flag",
  "warm_anchor_present": true,
  "dominant_palette": "warm | cool | mixed",
  "flags": [
    {
      "code": "cool-on-content | missing-warm-anchor | amber-orange-on-brown | colour-overload",
      "where": "short location, e.g. 'the four region cards'",
      "evidence": "what you see that triggers it",
      "severity": "high | medium | low",
      "fix_hint": "one line, e.g. 'restore yellow anchor; cool only on the I/O diagram'"
    }
  ],
  "notes": "one or two sentences; mention what is working, not just faults"
}
```

`verdict` is `flag` if any flag fires, else `pass`. The lint never edits anything.
```
