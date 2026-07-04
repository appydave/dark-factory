---
topic: "Design-lint rubric missed top failure"
issue: "Design-lint rubric built from a small sample missed the top real failure mode"
created: "2026-06-09"
story_reference: "a69afeb2"
category: "process"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["tools/design-lint/README.md", "tools/design-lint/RUBRIC.md"]
commits: []
---

# Design-lint rubric missed top failure — Design-lint rubric built from a small sample missed the top real failure mode

## Problem Signature

**Symptoms**: tools/design-lint/RUBRIC.md (written earlier in the same session from 4 pasted 'cortex' screenshots) flagged only cool-on-content, missing-warm-anchor, and amber-orange-on-brown. When David's 103 real slide ratings were tallied by theme, colour-overload complaints ('too many colours', 'too bold', 'too heavy', 'overboard', 'flamboyant', 'childish') plus single-hue-flood complaints ('too much green', 'purple all the way through') totalled 22 occurrences — more than any other failure category, including the contrast failures the rubric already covered — yet the rubric had no flag for it.

**Environment**: tools/design-lint/RUBRIC.md and tools/design-lint/README.md in the dark-factory repo

**Triggering Conditions**: David pasted his full slide-rating export (localStorage key mocha-slides-ratings-v1, 103 of 349 slides rated) and asked for the design rules to be updated from that real data rather than impression.

## Root Cause
The rubric's flags were derived by theorizing over a small, illustrative set of screenshots (4 cortex-deck images) rather than validated against a real quantified sample, so it missed the failure mode that only becomes visible at volume.

## Solution
Tallied label themes across the 103 rated slides with a small python counter script over round-01.json, confirmed colour-overload/single-hue-flood was the largest failure category (12 overload + 10 single-hue-flood vs 9 contrast-fail mentions), then added a 4th flag F4 colour-overload to tools/design-lint/RUBRIC.md with an explicit 'loudness judgment, never a colour count' guardrail (to avoid repeating an earlier round-04 Goodhart mistake where diagram/colour counts got treated as targets), and mirrored the change into README.md and durable memory.

```diff-before
- Judgment over rules. These three flags are the reliable failures David names repeatedly. They
  are not a maximisable scorecard. A clean design with none of these flags PASSES — say so plainly.
```
```diff-after
- Judgment over rules. These four flags are the reliable failures David names repeatedly. They
  are not a maximisable scorecard. A clean design with none of these flags PASSES — say so plainly.
- colour-overload is a "does it shout?" judgment, NEVER a colour count. Never flag "too many
  colours" by counting. Flag loudness — colour overpowering the content. A calm multi-colour legend
  PASSES.
```

```diff-after (new section added)
### F4 — colour-overload  (the #1 failure across rated slides — 103-slide round, 2026-06-10)
The screen uses too many competing colours, or colour too saturated/heavy, so it shouts over the
content. David's most frequent complaint: "too many colours", "too bold", "too heavy",
"overboard", "flamboyant", "childish" — and a single hue flooding a whole screen ("too much
green", "purple all the way through"). Both LOVE-tier slides won on "never overpowering."
- Flag when: many saturated colours compete with no clear hierarchy; OR one hue floods most of the
  screen; OR colour is heavy enough to pull attention off the content.
- Do NOT flag when: colour is restrained — few colours, softened/light, mostly-neutral ground
  (grey/cream) with a sparing accent — even if several semantic colours appear, as long as none
  overpowers. The winning pattern is "everything grey, only one colour made it in."
- This is a loudness judgment, NOT a count. A disciplined multi-colour legend that reads calm
  PASSES. severity: high when it reads childish/messy/ugly; medium when merely "a bit heavy."
```

```diff-before (README.md)
Three reliable failures only — the ones David names repeatedly (see RUBRIC.md):
- F1 cool-on-content — cool semantic colour dominating content cards that aren't diagram nodes.
- F2 missing-warm-anchor — no bright warm anchor (yellow #ffde59); screen reads cool/grey, off-brand.
- F3 amber-orange-on-brown — muddy amber/orange as fill/text on brown/beige.
```
```diff-after (README.md)
Four reliable failures only — the ones David names repeatedly (see RUBRIC.md):
- F1 cool-on-content — cool semantic colour dominating content cards that aren't diagram nodes.
- F2 missing-warm-anchor — no bright warm anchor (yellow #ffde59); screen reads cool/grey, off-brand.
- F3 amber-orange-on-brown — muddy amber/orange as fill/text on brown/beige.
- F4 colour-overload — too many competing / too-saturated colours, or one hue flooding the screen,
  so colour shouts over the content (the #1 failure across the 103-slide round). A loudness judgment,
  never a colour count.
```

## Prevention
Before finalizing a judgment rubric or spec, validate it against a real quantified rating sample rather than a handful of illustrative examples — a small anecdotal set under-represents the highest-frequency failure mode.

## Related
- Sessions: a69afeb2
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): a69afeb2 · 2026-06-09
- **Files** (candidate-level): tools/design-lint/README.md, tools/design-lint/RUBRIC.md
- **Commits** (candidate-level): —
