---
domain: "architecture"
name: "Design-taste correlation over-generalized into an absolute SVG/diagram-first render rule"
status: "proposed"
created: "2026-06-08"
story_references: ["2df0e613", "307792ae", "50ceee75", "5eae009f", "f2df9480", "f7a95652"]
last_updated: "2026-06-12"
recurrence_count: 6
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: [".claude/skills/comprehend-visualise/SKILL.md", ".mochaccino/designs/02-brain-remembers/index.html", ".mochaccino/designs/03-four-memories/index.html", ".mochaccino/designs/04-brain-sleeps/index.html", ".mochaccino/designs/06-brain-anatomy/index.html", ".mochaccino/designs/index.html", "docs/david-design-patterns.md", "experiments/watchtower-engine/queue/q-20260612-cortex-brain-v4.json", "tools/design-lint/RUBRIC.md"]
commits: []
---

# architecture — Design-taste correlation over-generalized into an absolute SVG/diagram-first render rule Pattern

## Context
grep for the brand-yellow hex #ffde59 found 0 occurrences across designs 02, 03, 04, 06 — only the two untouched designs (01, 05) still carried it. Cool semantic colour (blue/green/purple/teal) had become the dominant treatment on content-card headings and bars.

Cool semantic colour was used as load-bearing identity colour on content cards (card top-bar + coloured heading) rather than being confined to genuine flow/diagram content; the warm brand yellow #ffde59 anchor was dropped entirely, and one design also carried a live amber-orange-on-tint swap marker that risked the amber-orange-on-brown lint flag.

## Implementation
Re-rendered all four regressed designs: added --brand-yellow/--gold/--cream CSS custom properties; gave the single 'answer/hub/mind' element per screen a yellow left-border warm anchor; demoted content-card coloured bars/headings to a neutral gold bar + ink heading, keeping cool colour only as a small legend-key dot; left cool colour untouched where it was a genuine diagram (04-brain-sleeps loop, 02-brain-remembers spine); neutralised the amber/orange-on-tint swap markers in 06-brain-anatomy's organ-swap diagram to grey to remove the amber-orange-on-brown risk. Verified before closing the ticket: grep count of #ffde59 per file (>=1 each), curl HTTP 200 on all 5 pages, and Playwright screenshots of the worst-case (06) and the cycle screen (04).

## Examples
Add brand tokens and restore the warm anchor (06-brain-anatomy/index.html):
```diff-before
  :root{--paper:#f6f4ef;--card:#fbfaf7;--ink:#23201d;--muted:#6f675e;--line:#d9d2c6;--ghost:#ece7de;--conn:#a9a299;--swap:#b96f24;}
```
```diff-after
  :root{--paper:#f6f4ef;--card:#fbfaf7;--ink:#23201d;--muted:#6f675e;--line:#d9d2c6;--ghost:#ece7de;--conn:#a9a299;--swap:#6f675e;--brand-yellow:#ffde59;--gold:#ccba9d;--cream:#f0ebe4;}
```
```diff-before
  .mind{position:relative;overflow:hidden;background:var(--card);border:1px solid var(--line);border-radius:16px;margin-top:16px;padding:20px 24px}
```
```diff-after
  .mind{position:relative;overflow:hidden;background:var(--card);border:1px solid var(--line);border-left:6px solid var(--brand-yellow);border-radius:16px;margin-top:16px;padding:20px 24px}
```

Demote a content card from saturated colour to neutral bar + legend dot:
```diff-before
    return `<a class="rcard" href="../${esc(rg.drill)}/index.html"><div class="bar" style="background:${c}"></div><div class="b">
      <div class="head"><h3 style="color:${c}"><span class="dot" style="background:${c}"></span>${esc(rg.name)}</h3>
```
```diff-after
    return `<a class="rcard" href="../${esc(rg.drill)}/index.html"><div class="bar" style="background:var(--gold)"></div><div class="b">
      <div class="head"><h3><span class="dot" style="background:${c}"></span>${esc(rg.name)}</h3>
```

Neutralise the amber-orange-on-tint swap marker (kills the amber-orange-on-brown lint risk):
```diff-before
    g+=`<rect x="${sx-13}" y="60" width="26" height="9" rx="2" fill="#fbe9d4" stroke="${'#b96f24'}" stroke-width="1"/>`;
    g+=`<text x="${sx}" y="92" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" fill="#b96f24">⇄ swap</text>`;
```
```diff-after
    g+=`<rect x="${sx-13}" y="60" width="26" height="9" rx="2" fill="#f0ebe4" stroke="${'#6f675e'}" stroke-width="1"/>`;
    g+=`<text x="${sx}" y="92" text-anchor="middle" font-family="Roboto Mono" font-size="9.5" fill="#6f675e">⇄ swap</text>`;
```

## Rationale
Cool semantic colour was used as load-bearing identity colour on content cards (card top-bar + coloured heading) rather than being confined to genuine flow/diagram content; the warm brand yellow #ffde59 anchor was dropped entirely, and one design also carried a live amber-orange-on-tint swap marker that risked the amber-orange-on-brown lint flag.

## Anti-Patterns
Dev: keep cool semantic colour confined to genuine diagrams/flows — never load-bearing on plain content cards (design-lint RUBRIC.md flags this as missing-warm-anchor / amber-orange-on-brown). After any colour-system edit, verify with a grep count of the brand-warm hex per file plus an HTTP-status pass and a screenshot before closing the ticket — don't trust the diff alone as proof the fix landed visually.

## Related
- Originated from learnings:
  - The factory's distilled design-taste spec dropped the qualifier 'used sparingly, where it fits' and was hardened into a near-universal 'render everything as an SVG diagram' mandate, which then propagated into a live render that forced connectors onto content that was legitimately a flat comparison layout.
  - A prior render ticket (v3) explicitly instructed dropping the brand's warm yellow anchor and forcing SVG diagrams, producing a brand-cold cortex deck that had to be diagnosed and reversed.
  - A prior render pass made cool semantic colour (blue/green/purple/teal) load-bearing on content cards, dropping the warm brand-yellow anchor to zero occurrences across four of six cortex mochaccino designs.
  - Mochaccino designs rendered their entire body inside one giant <svg> (with HTML content embedded via foreignObject) instead of HTML-primary layout with sparing SVG diagrams.
  - A design-taste spec distilled from rated screenshots noted that loved designs correlated with SVG diagrams; that correlation was written into a downstream skill as an absolute rule ('draw it as a diagram — the #1 love-trigger'), causing a render loop to convert everything to SVG node-graphs — a shape-rendering monoculture David never asked for that regressed the six-months-proven, varied HTML house style.
  - A one-shot fix to wire a distilled design-taste spec into an automated render path encoded a correlational signal ('loved designs tended to be diagrams') as a hard 'diagram-first' render rule, causing every generated page to become an SVG node-graph and silently re-skinning the whole HTML house style.
- Related patterns: []
- ADRs: []

## Provenance
- **Sessions** (6): 2df0e613, 307792ae, 50ceee75, 5eae009f, f2df9480, f7a95652 · 2026-06-08 → 2026-06-12
- **Files** (candidate-level): .claude/skills/comprehend-visualise/SKILL.md, .mochaccino/designs/02-brain-remembers/index.html, .mochaccino/designs/03-four-memories/index.html, .mochaccino/designs/04-brain-sleeps/index.html, .mochaccino/designs/06-brain-anatomy/index.html, .mochaccino/designs/index.html, docs/david-design-patterns.md, experiments/watchtower-engine/queue/q-20260612-cortex-brain-v4.json, tools/design-lint/RUBRIC.md
- **Commits** (candidate-level): —
