---
artifact_id: appydave-plugins:skill:apps-registry
repo: appydave-plugins
artifact_type: skill
cluster_facet: [discovery-routing, orchestration]
phase_fit: [9]
evaluated_at: 2026-05-17
---

# Eval: apps-registry

**Intent**: Read, write, and shape the canonical AppyDave app registry at `~/.config/appydave/apps.json` — three operations (query, mutate, derive projections) over a flat JSON app catalog.

## Scores

- **quality_score**: 3 — The skill is clean and well-scoped. The three-operation structure (Read/Write/Shape) is a reasonable API. The atomic-write requirement (temp file + rename) and schema validation gate show operational maturity. The skill is narrow enough that it does one thing well. Deduction: the Shape operation has only one implemented projection (`family-runtime-matrix`) and several marked "future" — suggesting this is still partially aspirational. The adjacent skills section (app-query, app-launcher) is useful but adds the sense that the ecosystem is still being assembled.
- **adoption_fit_final**: strong — This is David's own skill over his own registry format. Already in production. The evaluation purpose is pattern recognition for catalog-like skills in other contexts.
- **inspiration_value**: low — The Read/Write/Shape tripartite design is sound but not particularly novel. The schema versioning (v1.2 additive over v1.1) and backward-compatibility discipline are worth noting for any registry skill pattern.
- **uniqueness_refined**: commodity — Registry CRUD skills are common. This one's distinction is its awareness of four existing consumers and backward-compatibility discipline.
- **composability**: called-by-others — Other skills (app-launcher, screenshot-tour) read from this registry. The skill is infrastructure for the rest of the ecosystem.
- **description_craft_refined**: trigger — Description lists explicit trigger phrases well. Functional.

## Mineable phrasing

`none`

## Notes

This skill is an example of a well-scoped infrastructure skill: it manages a canonical file that other skills depend on, enforces schema versioning, and supports three distinct use patterns without conflation. The "four existing consumers" design constraint (backward compatibility) is a dark-factory infrastructure principle — don't break downstream consumers when evolving schema. Not relevant to Ruflo; fully standalone.
