---
topic: "Broken renders mistaken for bad design ratings"
issue: "Indirect render signals (HTTP 200, headless screenshot, SVG count) wrongly trusted as proof of a working render"
created: "2026-06-08"
story_reference: "f2df9480, f7a95652"
category: "testing"
severity: "high"
status: "proposed"
recurrence_count: 2
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["docs/david-design-patterns.md", "tools/mocha-census/check-health.py", "tools/mocha-census/extract.py"]
commits: []
---

# Broken renders mistaken for bad design ratings — Indirect render signals (HTTP 200, headless screenshot, SVG count) wrongly trusted as proof of a working render

## Problem Signature

**Symptoms**: Structural feature-extraction (extract.py) scored the 'shit' tier oddly (high sidebar/chrome markers, low everything else). Visually inspecting a paired contrast (wave-sprint-board vs chain-sprint-board — same content, same tokens, opposite rating) showed chain-sprint-board displaying "Failed to load: Unexpected token '<'" — a console error, not a design flaw.

**Environment**: tools/mocha-census round-01 analysis: the `chain-*` design family in ad-apps-angeleye plus ~8 other 'meh'-rated designs across other repos.

**Triggering Conditions**: Rating a screenshot without first confirming the underlying page actually rendered; the taste board captured whatever was on screen — including a broken/loading state — and both the human rater and the mechanical feature-extractor treated it as legitimate design signal.

## Root Cause
The pipeline (scan → shoot → rate → extract) had no render-health gate. A data-fetch 404 in `chain-*` designs produced an empty/error shell that got screenshotted, rated 'shit' by David (fairly, as a visual), and then fed into extract.py's structural analysis as if it were a genuine bad-design exemplar.

## Solution
Wrote check-health.py: loads each rated design headless, listens for browser console errors, and regex-matches page text for failure signatures ("failed to load", "unexpected token", "is not defined", stuck-on-"Loading…", etc.) to flag broken/stuck renders. Re-ran the structural analysis excluding the 34 flagged designs (all 3 'shit' entries plus 8 of 'meh'); the clean comparison (90 good vs 27 meh) produced a sharp, trustworthy discriminator (card-sprawl) instead of a false one derived from crashed pages.

```python
BAD=re.compile(r"failed to load|unexpected token|is not defined|cannot read|NaN|undefined is not|error:",re.I)
...
errs=[]; pg.on("console",lambda m:(errs.append(m.text) if m.type=="error" else None))
for root,items in by_root.items():
    s,port=serve(root)
    for r,p in items:
        did=re.sub(r".*/designs/(.+)/index\.html$",r"\1",p)
        errs.clear()
        pg.goto(f"http://127.0.0.1:{port}/designs/{did}/index.html")
        # flags broken/stuck renders before they are trusted as design signal
```
Result: `checked 131  broken/stuck 34` — `broken by rating: {'good': 18, 'shit': 3, 'meh': 13}` (the 18 'good' flags were false positives from the text regex; the entire 'shit' tier was confirmed genuinely broken).

## Prevention
Before mining any UI screenshot corpus for design-quality signal, run an automated render-health pass (console-error + stuck-loading detection) and exclude broken renders first — never assume a screenshot represents the intended design.

## Related
- Sessions: f2df9480, f7a95652
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (2): f2df9480, f7a95652 · 2026-06-08
- **Files** (candidate-level): docs/david-design-patterns.md, tools/mocha-census/check-health.py, tools/mocha-census/extract.py
- **Commits** (candidate-level): —
