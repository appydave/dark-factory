---
artifact_id: appydave-plugins:skill:app-query
repo: appydave-plugins
artifact_type: skill
cluster_facet: [file-discovery, context-assembly, app-navigation]
phase_fit: [1]
evaluated_at: 2026-05-17
---

# Eval: app-query

**Intent**: Queries app files using semantic glob categories (backend, frontend, understand, codebase) defined in context.globs.json, with 4-tier alias resolution, and outputs file paths for piping into llm_context.

## Scores

- **quality_score**: 4. The alias vocabulary (backend → services+routes, understand → context+docs+types+config) is excellent practical design. Parallel structure with brain-query shows intentional ecosystem design. Docked one point: requires context.globs.json and locations.json setup.
- **adoption_fit_final**: `mid`. The semantic category vocabulary and alias resolution pattern are adoptable; the specific CLI and config file dependencies are not.
- **inspiration_value**: `mid`. The composite glob pattern (understand, codebase, full as pre-built bundles) is a smart layer above raw file paths.
- **uniqueness_refined**: `uncommon`. Semantic category aliases over glob patterns with multi-tier resolution is not common in file-discovery tools.
- **composability**: `calls-others`. Explicitly upstream of llm-context; parallel to brain-query in the same pipeline.
- **description_craft_refined**: `trigger`. Description has rich trigger phrases including specific vocabulary ("RVETS backend code", "X api", "X routes").

## Mineable phrasing

> "`understand` → `context` + `docs` + `types` + `config`"

## Notes

The "understand" composite glob category encodes what information an agent needs to orient itself to an unfamiliar app — a useful vocabulary decision. The --pattern flag for cross-app queries (all RVETS backend code) shows that the same discovery model scales from single-app to multi-app patterns. The vocabulary table (docs / types / config / services / routes / components / views) is a candidate for a standard context-assembly vocabulary in any unified skill.
