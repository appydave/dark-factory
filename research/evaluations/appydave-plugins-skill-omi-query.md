---
artifact_id: appydave-plugins:skill:omi-query
repo: appydave-plugins
artifact_type: skill
cluster_facet: [knowledge-capture, planning]
phase_fit: [1, 2, 7, 8]
evaluated_at: 2026-05-17
---

# Eval: omi-query

**Intent**: Query extracted OMI wearable transcripts using frontmatter tags (brain, routing type, activity, recency) via the `query_omi` CLI tool.

## Scores
- **quality_score**: 4 — Two-mode output (file paths vs --meta JSON) with clear pipe-to-llm_context pattern, routing taxonomy table, and prerequisite declaration are all solid craft. The `--smart` auto-routing (clipboard vs temp file by token count) is an elegant ergonomic detail.
- **adoption_fit_final**: mid — Depends on `appydave-tools` gem and the omi-extract pipeline having run first. High value within David's system; the routing taxonomy (brain-update/til/todo-item/personal/archive) is directly reusable as a classification ontology.
- **inspiration_value**: mid — The two-mode output pattern (paths for piping vs metadata for large backlog review) is a useful API design pattern for any query skill over a large file corpus.
- **uniqueness_refined**: uncommon — OMI-specific pipeline query is unique to David's setup, but the "frontmatter-tagged file corpus + query CLI" pattern is generalisable.
- **composability**: called-by-others — Explicitly positioned as downstream of omi-extract; feeds Brain Librarian for brain-update backlog processing.
- **description_craft_refined**: trigger — Description lists eleven trigger phrases covering query, backlog, and recency intents; prerequisites stated explicitly.

## Mineable phrasing
> "Reads frontmatter tags written by omi-extract. Requires omi-extract to have run first."

## Notes
The explicit prerequisite declaration in the description field ("Requires omi-extract to have run first") is a dependency-declaration pattern that prevents confusing error states when skills are invoked out of order. The routing taxonomy (five routing types with clear semantic boundaries) is a distillable ontology pattern for any ambient-capture system. The metadata-first workflow (query --meta, then selectively load full content) is a strong token-efficiency pattern for large corpora.
