---
artifact_id: appydave-plugins:skill:omi-extract-haiku
repo: appydave-plugins
artifact_type: skill
cluster_facet: [knowledge-capture, planning, test-authoring]
phase_fit: [1, 2, 4, 7, 8]
evaluated_at: 2026-05-17
---

# Eval: omi-extract-haiku

**Intent**: Extract and classify OMI wearable transcripts using parallel Haiku sub-agents spawned via the Claude Code harness, without consuming external API quota.

## Scores
- **quality_score**: 4 — Concrete parallel-agent pattern (5 agents × 10 files), brain-vocab injection, validate-after-each-batch discipline, and optional Sonnet quality review step are all production-grade. Defaults table is a strong UX touch.
- **adoption_fit_final**: mid — Tightly coupled to David's OMI/raw-intake pipeline and brains-index.json path. High value within that context; not directly portable. Paired with omi-query to form a complete ETL loop.
- **inspiration_value**: high — The pattern of spawning N parallel Haiku agents for batch classification, then running a single Sonnet reviewer on a random sample, is a cost-optimised quality-gate pattern worth extracting.
- **uniqueness_refined**: uncommon — Harness-native parallel agent orchestration for data classification (no external API) is not seen elsewhere in this corpus.
- **composability**: calls-others — References ontology-schema.md, find_untagged.py, validate_tags.py, and a review-prompt.md; designed to feed omi-query downstream.
- **description_craft_refined**: trigger — Description lists six explicit trigger phrases and states the "no external API, no Gemini quota" differentiator clearly.

## Mineable phrasing
> "Spawns parallel Haiku background agents for isolated per-batch classification."

## Notes
The Sonnet-reviews-Haiku quality gate (optional "and review" trigger) is a textbook reviewer-agent-separation pattern and one of the cleaner implementations of it in David's corpus. The validate_tags.py step (strip brain names not in vocab, move violations to overflow_topics) shows defensive tagging discipline that prevents ontology drift. The `extraction_model: haiku` frontmatter tag to distinguish from Gemini-extracted files is a good provenance-tracking pattern.
