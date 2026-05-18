---
artifact_id: compound-knowledge:agent:stale-knowledge-checker
repo: compound-knowledge-plugin
artifact_type: agent
cluster_facet: [compound-knowledge, knowledge-hygiene, contradiction-detection]
phase_fit: [stage-10]
evaluated_at: 2026-05-17
---

# Eval: stale-knowledge-checker

**Intent**: Sub-agent that searches `docs/knowledge/` for entries contradicted or superseded by a new learning, returning structured text recommendations without writing any files.

## Scores
- **quality_score**: 3 — Focused and well-constrained; thin by design (sub-agent role); output format is clear; "corrections always win" rule is a good invariant
- **adoption_fit_final**: mid — Portable pattern; path convention is the only coupling; read-only contract makes it safe to embed anywhere
- **inspiration_value**: low — The contradiction/superseded/complementary taxonomy is sensible but not novel
- **uniqueness_refined**: uncommon — Read-only knowledge hygiene agent called before write is an underused pattern
- **composability**: called-by-others — Designed to be dispatched by `kw-compound`; should never be the root caller
- **description_craft_refined**: summary — Description explains the role clearly but lacks user-facing trigger phrases (it's an agent, not a user-invoked skill)

## Mineable phrasing
> "Be conservative with 'remove' recommendations. Prefer 'update' or 'merge' over deletion. Knowledge is expensive to recreate."

## Notes
The hard constraint "return text only, never write files" is the key architectural decision — it keeps orchestration authority in the parent skill and prevents runaway deletions. The agent is appropriately narrow. Its value is entirely as a composable component; standalone it is too thin to justify adoption.
