---
artifact_id: appydave-plugins:skill:brain-query
repo: appydave-plugins
artifact_type: skill
cluster_facet: [knowledge-discovery, file-pipeline, context-assembly]
phase_fit: [0]
evaluated_at: 2026-05-17
---

# Eval: brain-query

**Intent**: CLI-backed skill that resolves brain names via 4-tier matching (exact → alias → substring → tag) and outputs file paths for piping into llm_context.

## Scores

- **quality_score**: 4. Tight, purposeful, role-separated — knows what it is (discoverer, not assembler) and says so clearly. Docked one point for being David-system-specific (brains-index.json dependency).
- **adoption_fit_final**: `mid`. The pipeline pattern (query → paths → llm_context) is universally adoptable; the specific CLI tool is not. Reframe: the pattern is the asset.
- **inspiration_value**: `mid`. 4-tier resolution strategy and the query→assembler split are instructive.
- **uniqueness_refined**: `uncommon`. CLI-backed discovery piped to assembler is a clean separation, but the pattern itself is known; what's uncommon is seeing it codified as a skill.
- **composability**: `calls-others`. Explicitly upstream of llm-context; designed to be composed.
- **description_craft_refined**: `trigger`. Rich trigger phrase list in description, plus explicit "Different from focus and brain-librarian" disambiguation.

## Mineable phrasing

> "File discovery tool — returns paths for piping into llm_context. Different from focus (orientation) and brain-librarian (curation)."

## Notes

The role differentiation between brain-query (find), llm-context (assemble), focus (orient), and brain-bridge (write-back) is an unusually disciplined single-responsibility decomposition — each skill has one verb. That four-role pattern is worth capturing in any unified context-management skill design.
