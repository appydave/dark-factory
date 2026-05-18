---
artifact_id: appydave-plugins:skill:frontmatter-indexer
repo: appydave-plugins
artifact_type: skill
cluster_facet: [documentation-health, metadata-indexing, schema-validation]
phase_fit: [0]
evaluated_at: 2026-05-17
---

# Eval: frontmatter-indexer

**Intent**: Recursively scans markdown directories, auto-detects frontmatter schema type (brain/ADR/learning/epic), validates required fields, and exports structured indexes in CSV/JSON/Markdown.

## Scores

- **quality_score**: 4. Clear schema detection strategy, multi-format output, real validation error examples. A solid operational tool skill. Docked one point: the skill is quite David-ecosystem-specific (brain-index, poem-os schemas).
- **adoption_fit_final**: `mid`. The schema detection + validation + multi-format export pattern is universally applicable; the specific schema types are environment-specific. The mechanism is adoptable even if the schemas aren't.
- **inspiration_value**: `mid`. The identifier-field-based schema detection pattern (one field → schema type) is clean and instructive.
- **uniqueness_refined**: `uncommon`. YAML frontmatter schema validation as a first-class skill is not common; usually buried in CI scripts.
- **composability**: `standalone`. No upstream or downstream skill dependencies declared; can be piped to others but doesn't require chains.
- **description_craft_refined**: `trigger`. Description has 12+ trigger phrases including varied vocabulary (health check, validation, index, scan).

## Mineable phrasing

none

## Notes

The pattern of using a single identifier field per schema type (brain: → brain-index, adr_number: → ADR, etc.) is a minimal-friction schema detection approach worth noting in any documentation health system. The validation-first, then export workflow models a good "quality gate before artifact" sequence applicable to research-discovery pipelines.
