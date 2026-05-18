---
artifact_id: appydave-plugins:skill:enrich-metadata
repo: appydave-plugins
artifact_type: skill
cluster_facet: [knowledge-capture]
phase_fit: [7, 8]
evaluated_at: 2026-05-17
---

# Eval: enrich-metadata

**Intent**: Enrich markdown documents with structured metadata (tags, topics, relationships, summaries, entities) using cheap LLM providers (Gemini free tier or Codex).

## Scores
- **quality_score**: 4 — The constrained vs unconstrained schema modes are the key design decision — constrained mode with overflow candidates is exactly the right approach for vocabulary-controlled enrichment (prevents tag sprawl). The provider selection table (Gemini default, Codex fallback) with explicit cost and reliability notes is practical. The batch processing with progress reporting and quota awareness (1,000 RPD) is production-grade. The "present to caller — results for human review, never auto-write" rule is correct and important.
- **adoption_fit_final**: strong — Directly integrated with Lexi and the brains system. Called by lexi when doing tag suggestions.
- **inspiration_value**: mid — The constrained mode with overflow candidates pattern is the most portable idea — it's the right mechanism for any vocabulary-controlled classification task.
- **uniqueness_refined**: uncommon — Provider-agnostic with explicit cost trade-off documentation is uncommon. Most metadata enrichment tools are single-provider.
- **composability**: called-by-others — Explicitly a called service — by lexi and by standalone users. Part of the intake pipeline.
- **description_craft_refined**: trigger — "Also triggered when brain-librarian needs tag suggestions" is a good agent-to-agent trigger definition.

## Mineable phrasing
> "matched_tags: [in vocabulary] + overflow: [discovered tag not in vocabulary] — The caller decides what to do with overflow — promote, map to synonyms, or discard"

## Notes
The vocabulary-constrained mode with overflow candidates is a clean solution to the vocabulary drift problem in tag-based knowledge systems. Overflow candidates become vocabulary growth proposals rather than silent noise. The "never auto-write" rule prevents LLM-generated metadata from corrupting documents without review. The entity type vocabulary (person, tool, framework, concept, project, organization, platform) is well-calibrated for technical documentation.
