---
artifact_id: compound-engineering:skill:ce-compound
repo: compound-engineering
artifact_type: skill
cluster_facet: [knowledge-capture, self-improvement]
phase_fit: [7, 8, 10]
evaluated_at: 2026-05-17
---

# Eval: ce-compound

**Intent**: Orchestrates parallel subagents to document a recently solved problem into `docs/solutions/` using dual-track (bug vs knowledge) schema with overlap detection, session history integration, and discoverability check.

## Scores

- **quality_score**: 5 — This is the highest-quality knowledge capture skill in the catalog. Key design strengths: (1) dual-track schema (bug track vs knowledge track) with different section shapes for each — bugs get symptoms/what-didn't-work/root-cause/prevention; knowledge gets context/guidance/why-it-matters/when-to-apply/examples; (2) overlap detection before creating a new doc (high overlap → update existing, not create duplicate); (3) the `validate-frontmatter.py` post-write check for silent YAML corruption issues (unquoted `#` in scalars, unquoted `: `); (4) headless mode (same quality output, no blocking questions, for automation); (5) auto memory scan (checks MEMORY.md for relevant prior context before research); (6) the discoverability check loop. The "Common Mistakes to Avoid" table is a production-honesty document — it names the exact failure modes (subagents writing files, research and assembly running in parallel, multiple files created).
- **adoption_fit_final**: mid — The skill is tightly coupled to the compound-engineering docs/solutions/ directory structure, YAML schema, and specialized subagents (ce-sessions, ce-performance-oracle, ce-security-sentinel, etc.). The dual-track classification, overlap detection, and discoverability check are directly portable. The full pipeline requires the compound-engineering plugin ecosystem — not a drop-in.
- **inspiration_value**: high — The dual-track schema (bugs vs knowledge with different section shapes) is a significant design improvement over flat "lessons learned" templates. The overlap detection before write (don't create a duplicate — update the existing) prevents knowledge base fragmentation. The `validate-frontmatter.py` post-write validation is a dark-factory data-integrity gate. The auto-invoke triggers ("that worked", "it's fixed", "working now") are a novel session-lifecycle hook.
- **uniqueness_refined**: rare — Dual-track schema + overlap detection + YAML validation + headless mode + auto-invoke triggers in a single skill is not found elsewhere in the catalog.
- **composability**: calls-others — Calls ce-sessions, Context Analyzer, Solution Extractor, Related Docs Finder, ce-compound-refresh (selectively), plus domain-specific reviewer subagents. Complex orchestration tree.
- **description_craft_refined**: summary — Description describes what it does more than when to trigger it. The auto-invoke trigger phrases ("that worked", "it's fixed") in the SKILL body are more useful triggers than the description.

## Mineable phrasing

> "Each unit of engineering work should make subsequent units of work easier—not harder."

## Notes

The dual-track classification (bug vs knowledge) is the most immediately portable design idea for David's context: when capturing learnings, the question of whether something is "a fix for a specific problem" vs "a pattern to apply going forward" changes the structure of useful documentation significantly. The overlap-before-write check is the dark-factory data-integrity principle applied to knowledge: don't add redundancy, update the canonical source. The YAML validation script (checking for silent corruption, not just schema) is a rarely-seen data-quality gate. The compound-knowledge variant (kw-compound) is a lighter version of the same idea — evaluate both together. The full skill requires Compound Engineering plugin ecosystem, but design patterns are Ruflo-independent.
