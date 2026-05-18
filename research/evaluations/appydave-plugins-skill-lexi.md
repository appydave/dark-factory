---
artifact_id: appydave-plugins:skill:lexi
repo: appydave-plugins
artifact_type: skill
cluster_facet: [code-review, knowledge-capture, orchestration]
phase_fit: [6, 7, 8, 9]
evaluated_at: 2026-05-17
---

# Eval: lexi

**Intent**: Portable brain librarian — curate, onboard, maintain, and analyse second-brain knowledge collections, from a single brain to a full multi-brain collection.

## Scores
- **quality_score**: 5 — The most complete knowledge management skill in the corpus. The four-mode detection (single brain onboarding / collection onboarding / single brain maintain / collection maintain / raw intake) driven by folder state inspection rather than user selection is a sophisticated design. The three-layer schema (universal core / category rules / per-brain overrides) is a clean extensibility model. The script suite (check_frontmatter, fix_frontmatter, sync_file_counts, validate_links, report_ontology, detect_duplicates, detect_srp_violations, detect_isolation, detect_negative_knowledge, detect_orphans, check_starters, list_clusters, run_audit, build_brain_index) is production-grade. The "brains vs upstreams" distinction is architecturally important.
- **adoption_fit_final**: strong — David's own tool, central to the entire brains system. Already the canonical library maintenance tool.
- **inspiration_value**: high — The negative-knowledge audit (find brains documenting only the happy path) is the highest-signal portable idea. The isolation audit (brains with zero inbound cross-references) and starter graduation tracking are also distinctive.
- **uniqueness_refined**: rare — A multi-mode, self-configuring brain librarian with a full script suite, vocabulary-controlled tagging, and provenance tracking is genuinely unique in the corpus.
- **composability**: calls-others — Calls enrich-metadata for tag suggestions. Called by clipboard-intake. Central hub of the knowledge maintenance ecosystem.
- **description_craft_refined**: trigger — The description is an exhaustive trigger list — almost too long, but every trigger is accurate and distinctive.

## Mineable phrasing
> "Negative knowledge audit — for any brain with 5+ files, check whether any file contains anti-patterns, pitfalls, or warning sections. Brains with zero negative knowledge are documenting only the happy path."

## Notes
Lexi is the most sophisticated artifact in stages 7+8. The "brains vs upstreams" distinction (brain = curated knowledge maintained by Lexi; upstream = raw source material Lexi ignores) is an architectural clarity that prevents a common confusion. The `.audit/` dotfolder convention (generated output, never audited by Lexi itself) is a clean separation of concerns. The mode selection algorithm (detect folder state → pick mode automatically, never ask the user) is the right UX for a maintenance tool. The "never rewrite existing content" and "always offer dry-run first" rules are production-appropriate safety constraints.
