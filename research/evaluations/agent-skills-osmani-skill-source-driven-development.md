---
artifact_id: agent-skills-osmani:skill:source-driven-development
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [code-implementation, system-comprehension]
phase_fit: [0, 3, 4]
evaluated_at: 2026-05-17
---

# Eval: source-driven-development

**Intent**: Ground every framework-specific implementation decision in official documentation by explicitly detecting stack versions, fetching the relevant docs page, implementing against documented patterns, and citing sources with full URLs.

## Scores
- **quality_score**: 5 — DETECT→FETCH→IMPLEMENT→CITE workflow with stack detection from dependency files, source hierarchy table (official docs > official blog > web standards > browser compat; never Stack Overflow/blogs/AI summaries), deep-link citation rules, conflict surfacing protocol, and explicit "UNVERIFIED" flag convention are all high-craft. The "be precise with what you fetch" section (fetch the specific page, not the homepage) is actionable guidance not found elsewhere.
- **adoption_fit_final**: strong — Language-agnostic; supports all major stacks via dependency file detection. The principle (don't write from training data — verify) is universally applicable and especially important for rapidly-evolving frameworks.
- **inspiration_value**: high — The "UNVERIFIED" explicit flag convention ("I could not find official documentation for this pattern. This is based on training data and may be outdated.") is a honesty-first disclosure pattern that improves trust in agent output. The "conflict detected" surface-don't-silently-pick protocol is the right governance model for version conflicts.
- **uniqueness_refined**: rare — Systematic documentation-first coding with cite-in-code-comments + full-URL convention and explicit "not authoritative" exclusion list (Stack Overflow, blog posts, AI summaries, training data) is not found at this specificity in any other skill.
- **composability**: called-by-others — The DETECT step naturally precedes any framework-specific implementation; composable as a pre-step for any coding skill.
- **description_craft_refined**: trigger — Description gives both positive trigger ("when you want authoritative, source-cited code") and explicit "When NOT to use" guard (correctness doesn't depend on version; user explicitly wants speed).

## Mineable phrasing
> "If you cannot find documentation for a pattern, say so explicitly. Honesty about what you couldn't verify is more valuable than false confidence."

## Notes
The source hierarchy table (priority 1–4 with example URLs, "never cite as primary" section) is a formally structured epistemology for agent coding — this level of source governance is rare. The deep-link citation rule ("prefer anchors to top-level pages — anchors survive doc restructuring better") is a practical archival insight. The anti-rationalization table entry "Fetching docs wastes tokens — hallucinating an API wastes more" is the sharpest cost-justification argument for the verify-before-code habit. The explicit UNVERIFIED flag makes uncertainty a first-class output state rather than hidden hedging.
