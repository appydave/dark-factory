---
topic: "Mochaccino gallery index is hand-written, not generated"
issue: "Mochaccino gallery index is hand-written HTML, not generated from a manifest"
created: "2026-06-08"
story_reference: "f2df9480"
category: "architecture"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: [".mochaccino/_archive/05-dark-factory-index-v1-2026-06-08.html", ".mochaccino/designs/05-dark-factory/index.html", ".mochaccino/designs/index.html"]
commits: []
---

# Mochaccino gallery index is hand-written, not generated — Mochaccino gallery index is hand-written HTML, not generated from a manifest

## Problem Signature

**Symptoms**: David reported an improved page rendered correctly at its own `-v2` URL, but the gallery's '05 · system-map' card still linked to the old `05-dark-factory/index.html`, and no card existed for `-v2` at all.

**Environment**: dark-factory `.mochaccino/designs/index.html` (the Mochaccino gallery for this repo).

**Triggering Conditions**: Generating a new or revised Mochaccino design in one working session while the gallery index was never regenerated — it's static hand-authored HTML, so nothing auto-registers.

## Root Cause
`.mochaccino/designs/index.html` is curated by hand (hardcoded `<a>` cards per design) instead of being rendered from a designs manifest. This violates the repo's own 'structure-first, generate from schema' pattern and means every new or updated design requires manual index surgery.

## Solution
Worked around it for this instance: promoted the current `05-dark-factory-v2/index.html` into the canonical `05-dark-factory/` slot (backing up the old file to `_archive/` first), retired the `-v2` URL, and cleaned the leftover '(v2)' labels from the title and provenance string. Verified via curl that the canonical URL now serves the improved page and the old `-v2` URL 404s. The actual root-cause fix — generating the index from a manifest — was identified but deliberately left as follow-up work, not applied in this session.

```bash
mkdir -p _archive
cp designs/05-dark-factory/index.html "_archive/05-dark-factory-index-v1-2026-06-08.html"   # backup old
cp designs/05-dark-factory-v2/index.html designs/05-dark-factory/index.html                  # promote v2 into canonical slot
```
```diff-before
<title>The Dark Factory — a factory you run by talking to it (v2)</title>
```
```diff-after
<title>The Dark Factory — a factory you run by talking to it</title>
```

## Prevention
Mochaccino galleries should be rendered from a manifest (id/group/title/blurb → generated index), not hand-curated HTML, so new/updated designs auto-register and 'promote vN over vN-1' becomes a one-line manifest edit instead of file surgery.

## Related
- Sessions: f2df9480
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): f2df9480 · 2026-06-08
- **Files** (candidate-level): .mochaccino/_archive/05-dark-factory-index-v1-2026-06-08.html, .mochaccino/designs/05-dark-factory/index.html, .mochaccino/designs/index.html
- **Commits** (candidate-level): —
