---
topic: "Design-lint index blind spot"
issue: "Design-lint index blind spot: gallery index page skipped by scoped tickets"
created: "2026-06-11"
story_reference: "307792ae"
category: "process"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: [".mochaccino/designs/index.html"]
commits: []
---

# Design-lint index blind spot — Design-lint index blind spot: gallery index page skipped by scoped tickets

## Problem Signature

**Symptoms**: index.html at http://localhost:7422/designs/ retained the pre-fix brand-cold palette (0 yellow #ffde59, near-black ink #23201d, all-cool card top-bars including an all-cool hero gradient) even though the four linked design pages had already passed design-lint.

**Environment**: .mochaccino/designs/index.html (dark-factory Mochaccino gallery, static hand-written chrome, not data-driven), served on :7422

**Triggering Conditions**: The v4 re-render ticket (q-20260612-cortex-brain-v4) named only the 4 cortex design pages; design-lint's shoot-one.py + lint agents were run against that same explicit list, so neither the render nor the gate ever touched the index.

## Root Cause
Both the render ticket and the lint gate derived their target list from the ticket's named artifacts instead of from the served gallery surface (the index page plus everything it links). The index is static hand-written HTML (not data-driven), making it exactly the page a data-first re-render is most likely to skip.

## Solution
Read the index's :root palette and fixed it inline to the two-layer brand model (warm cream/brown ground, yellow #ffde59 H1 underline + hero bar, gold default card bars, cool bars kept only as sparing region-legend accents), then re-screenshotted and re-ran design-lint against it specifically, achieving a pass.

```diff-before
:root{--paper:#f6f4ef;--card:#fbfaf7;--ink:#23201d;--muted:#6f675e;--line:#d9d2c6;
      --blue:#3b6fb0;--green:#3f8c5a;--purple:#7a55bf;--teal:#2c8f93;}
```
```diff-after
:root{--paper:#f0ebe4;--card:#faf5ec;--ink:#342d2d;--muted:#6f675e;--line:#d9d2c6;
      --yellow:#ffde59;--gold:#ccba9d;--brown:#342d2d;
      --blue:#3b6fb0;--green:#3f8c5a;--purple:#7a55bf;--teal:#2c8f93;}
```

```diff-before
h1{font-family:'Bebas Neue';font-size:48px;letter-spacing:.02em;margin:0}
```
```diff-after
h1{font-family:'Bebas Neue';font-size:48px;letter-spacing:.02em;margin:0;display:inline-block;border-bottom:6px solid var(--yellow);padding-bottom:2px}
```

```diff-before
.card .bar{height:8px;background:var(--blue)}
a.hero{grid-column:1/-1}
a.hero .bar{height:10px;background:linear-gradient(90deg,var(--blue),var(--green),var(--purple),var(--teal))}
```
```diff-after
.card .bar{height:8px;background:var(--gold)}
a.hero{grid-column:1/-1}
a.hero .bar{height:10px;background:var(--yellow)}
```

## Prevention
A render/lint gate must derive its screenshot target list from the gallery index itself (the index page plus every page it links), never just the pages a ticket happens to name — treat 'landing/index page included?' as a standing checklist item for any multi-page render gate.

## Related
- Sessions: 307792ae
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 307792ae · 2026-06-11
- **Files** (candidate-level): .mochaccino/designs/index.html
- **Commits** (candidate-level): —
