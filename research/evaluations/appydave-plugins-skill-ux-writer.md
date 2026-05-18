---
artifact_id: appydave-plugins:skill:ux-writer
repo: appydave-plugins
artifact_type: skill
cluster_facet: [documentation, spec-writing, verification-validation]
phase_fit: [1, 5, 6, 7]
evaluated_at: 2026-05-17
---

# Eval: ux-writer

**Intent**: Transforms long messy brainstorms into structured, decision-useful UX requirements documents covering screen inventories, user flows, interaction specs, and IA.

## Scores
- **quality_score**: 4 — 20-section output structure, extraction checklist (experience framing, screen inventory, IA, interaction patterns, states, flows, data, business rules, notifications, gaps), role definition (analyst/designer/IA/PO — not visual designer or frontend engineer), and transformation rules. Thorough and practically scoped.
- **adoption_fit_final**: mid — Selected for stage 5 (UAT) but more naturally a stage 1/2 (spec-writing) tool. Useful for David's FliVideo and kybernesis UX work but the phase fit here is verification of existing spec coverage rather than new UX authoring.
- **inspiration_value**: mid
- **uniqueness_refined**: uncommon — The "what you are NOT" role definition (not a visual designer, not a frontend engineer, not a copywriter) is a sharp anti-scope statement. The explicit state inventory (empty/loading/error/partial/disabled/success) per screen is a useful completeness checklist.
- **composability**: standalone — Self-contained brainstorm-to-spec transformation.
- **description_craft_refined**: trigger — Rich trigger phrase list for UX-related requests.

## Mineable phrasing
> "Brainstorms describe the happy path. Add: empty states, error handling, edge cases, permissions, undo/recovery, mobile/responsive considerations, accessibility flags."

## Notes
The "do not simply summarise the brainstorm — distill it into a usable UX specification" framing is a strong identity statement for the skill. The "Recommended MVP UX" section (minimum screens and flows to validate the concept) is a practical focus lens. Phase fit in stage 5 is as a UAT companion — checking whether implemented UX matches spec rather than generating new spec — which is a secondary use case.
