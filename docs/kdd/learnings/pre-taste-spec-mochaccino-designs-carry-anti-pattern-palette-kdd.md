---
topic: "taste-spec re-render"
issue: "Pre-taste-spec Mochaccino designs carry anti-pattern palettes needing systematic re-render"
created: "2026-06-08"
story_reference: "9b59ab5c"
category: "tooling"
severity: "low"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: [".mochaccino/data/02-brain-remembers.json", ".mochaccino/data/03-four-memories.json", ".mochaccino/data/04-brain-sleeps.json", ".mochaccino/data/06-brain-anatomy.json", ".mochaccino/designs/02-brain-remembers/index.html", ".mochaccino/designs/03-four-memories/index.html", ".mochaccino/designs/04-brain-sleeps/index.html", ".mochaccino/designs/06-brain-anatomy/index.html", ".mochaccino/designs/index.html", "docs/david-design-patterns.md", "experiments/watchtower-engine/runs/run-cortex-render-003.json"]
commits: []
---

# taste-spec re-render — Pre-taste-spec Mochaccino designs carry anti-pattern palettes needing systematic re-render

## Problem Signature

**Symptoms**: Prior cortex Mochaccino designs (v1) used card-grid/numbered-rail layouts and a yellow #ffde59 / gold-on-brown colour scheme — the composition and colour anti-patterns docs/david-design-patterns.md flags as low-rated (round-02, 156 rated designs).

**Environment**: Dark Factory Mochaccino design workspace: .mochaccino/designs/{06-brain-anatomy,02-brain-remembers,03-four-memories,04-brain-sleeps}/index.html and their paired .mochaccino/data/*.json, served on :7422.

**Triggering Conditions**: A watchtower-engine queue ticket (q-20260609-cortex-brain-v3, kind: instruction) explicitly asked to RE-RENDER the cortex designs through the taste spec (docs/david-design-patterns.md) and named love-tier exemplar shots to anchor on, rather than iterating on the existing gold/yellow version.

## Root Cause
The original four designs predated the taste spec and used a brown/gold/yellow (`--brown:#342d2d; --gold:#ccba9d; --yellow:#ffde59`) palette with flat card-grid/numbered-rail layouts instead of drawn semantic diagrams — exactly the two recurring flaws (colour anti-pattern + weak composition) the rated corpus identified.

## Solution
Rewrote all four designs plus the gallery index as hand-authored SVG diagrams: replaced the brown/gold/yellow tokens with a light --paper/--card palette plus four semantic hues (blue/green/purple/teal) applied per data-region; added ghost background text, thin neutral (--conn) connectors with colour kept in blocks not lines, legend strips, and INPUT/OUTPUT header pills; trimmed prose to one line per element; bumped the paired data JSON files to v2.0.0 (added hue/diagram fields) while preserving meta.source/commit_sha provenance. Verified with JSON-validity checks and HTTP 200 checks against the :7422 server for every design before marking the run complete.

Before (`.mochaccino/designs/06-brain-anatomy/index.html`, v1 — anti-pattern palette):
```css
:root{
  --brown:#342d2d; --brown-mid:#5c4d4d; --gold:#ccba9d; --yellow:#ffde59;
  --cream:#f3efe7; --paper:#fbfaf7; --ink:#2b2622; --muted:#6b625b; --line:#e4ddd0;
}
```

After (same file, rewritten — semantic-hue palette):
```css
:root{
  --paper:#f6f4ef; --card:#fbfaf7; --ink:#23201d; --muted:#6f675e; --line:#d9d2c6;
  --ghost:#ebe6dd; --conn:#a9a299; --swap:#dd8a3a;
}
```

Per-region semantic hues then applied in `.mochaccino/data/06-brain-anatomy.json`:
```json
"regions": [
  { "key": "episodic", "name": "Episodic", "hue": "blue", "db": "timeline.db" },
  { "key": "semantic", "name": "Semantic", "hue": "green", "db": "entity-graph.db" }
]
```

## Prevention
When re-rendering a Mochaccino design against docs/david-design-patterns.md, check the :root colour tokens first — any --gold/--yellow/--brown token on a --brown/--cream background is the flagged anti-pattern (design-lint's amber-orange-on-brown check). Swap to semantic-hue blocks (blue/green/purple/teal) with neutral connectors, replace card-grids/numbered-rails with a drawn SVG diagram, add ghost text + I/O header + legend, and confirm with JSON validity + HTTP 200 checks per design before marking the run complete.

## Related
- Sessions: 9b59ab5c
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 9b59ab5c · 2026-06-08
- **Files** (candidate-level): .mochaccino/data/02-brain-remembers.json, .mochaccino/data/03-four-memories.json, .mochaccino/data/04-brain-sleeps.json, .mochaccino/data/06-brain-anatomy.json, .mochaccino/designs/02-brain-remembers/index.html, .mochaccino/designs/03-four-memories/index.html, .mochaccino/designs/04-brain-sleeps/index.html, .mochaccino/designs/06-brain-anatomy/index.html, .mochaccino/designs/index.html, docs/david-design-patterns.md, experiments/watchtower-engine/runs/run-cortex-render-003.json
- **Commits** (candidate-level): —
