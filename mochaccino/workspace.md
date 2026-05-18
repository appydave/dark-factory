---
purpose: Decision-support visualization layer over the dark-factory-catalog
workspace_type: single
mode: text-to-documentation
audience: David solo
brand_source: brand-dave:brand
update_cadence: quick exploration, but extensible for re-renders as catalog grows
created: 2026-05-18
last_updated: 2026-05-18
---

# Dark Factory — Workspace

**Purpose**: Scannable visual layer over the dark-factory-catalog (1,100 artifacts, 76 distillation drafts, 88 deep evals, 11 pipeline stages walked). Designed so David can consume the corpus without wall-of-text overwhelm and make decisions.

**For Agents**: When opening this workspace, read this file + `learnings.md` (Rules + Recurring Notes only) before acting. Two designs live here: `01-pipeline-overview` (SDLC-strip lens) and `02-mining-view` (top-artifacts lens).

**Created**: 2026-05-18
**Last Updated**: 2026-05-18

---

## Canonical sources

This workspace's JSON data is synthesised from (paths updated 2026-05-18 after move from brains → apps):

- `../research/artifacts.jsonl` — 1,100 row corpus
- `../research/distillations/INDEX.md` + cluster sub-files — 76 unified-skill drafts
- `../research/evaluations/*.md` — 88 deep evals
- `../research/pipeline-matrix/stage-*.md` — 11 stage walks

Citations in existing `meta.source` strings reference the old brains paths; they still resolve via the
compat symlink. New regenerations should emit apps-relative paths.

## Designs

| # | Design | Data | Status |
|---|--------|------|--------|
| 01 | pipeline-overview | `pipeline.json` | active |
| 02 | mining-view | `mining.json` | active |

## Audience profile (for Mocha tone)

Solo decision-maker (David). Already in-context with the catalog work. Brevity and scan-density beat polish. Terse labels, dense cards, "what's the verdict?" framing wins over "let me walk you through it" framing.
