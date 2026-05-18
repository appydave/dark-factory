---
artifact_id: appydave-plugins:skill:truth-trail
repo: appydave-plugins
artifact_type: skill
cluster_facet: [knowledge-capture, orchestration, verification-validation]
phase_fit: [5, 6, 7, 8, 9]
evaluated_at: 2026-05-17
---

# Eval: truth-trail

**Intent**: Knowledge integrity rules system enforcing four pillars (Canonical, Synthesis, Citation, Provenance Chain) whenever any agent writes a derivative document.

## Scores
- **quality_score**: 4 — Four pillars clearly defined, required frontmatter schema specified, violation patterns table, integration roadmap (Lexi/ALS hook/validation script), and honest current-maturity assessment (voluntary guidance, not enforcement). Well-structured for a rules-system skill.
- **adoption_fit_final**: strong — Directly governs David's second-brain synthesis workflow. Already installed and active. The ALS hook integration path is planned for the brains system.
- **inspiration_value**: mid
- **uniqueness_refined**: rare — The four-pillar framing (Canonical + Synthesis + Citation + Provenance Chain as a complete integrity set) and the `status: unverified` default (agents cannot self-verify) are original contributions to knowledge management.
- **composability**: called-by-others — Consulted by any agent before writing a synthesis document; not an interactive skill.
- **description_craft_refined**: trigger — Comprehensive trigger phrase list (20+ phrases including "is this cited?", "orphaned knowledge", "provenance chain").

## Mineable phrasing
> "Synthesis without citation = orphaned knowledge. Canonical without synthesis = dead-end knowledge."

## Notes
The "agents cannot self-verify" rule (`status: verified` set by agent is a violation pattern) is a sharp epistemic constraint — verification requires human review. The current-maturity transparency section (voluntary now, enforcement-path when ALS hooks exist) is a valuable pattern for skills that need to evolve. The skill is currently guidance-only which limits its effectiveness but the roadmap is clear.
