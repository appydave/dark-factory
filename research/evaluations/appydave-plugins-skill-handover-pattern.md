---
artifact_id: appydave-plugins:skill:handover-pattern
repo: appydave-plugins
artifact_type: skill
cluster_facet: [knowledge-capture]
phase_fit: [7, 8]
evaluated_at: 2026-05-17
---

# Eval: handover-pattern

**Intent**: Standard format for PO ↔ Developer bidirectional communication — structured templates for both handover directions with concrete examples.

## Scores
- **quality_score**: 3 — The bidirectional design (PO→Dev AND Dev→PO) is the key structural insight. The worked examples (FR-136 Gling export) are valuable — they make the anti-patterns concrete. The five key principles (hierarchical information, references not walls of text, actionable, clear scope, traceable) are correct. Loses points because the description is too narrow ("PO ↔ Developer communication") — this is a general handover pattern that applies beyond BMAD project management, but the skill doesn't recognize that.
- **adoption_fit_final**: strong — David uses BMAD, has FR-numbers, and the pattern is already in use on FliVideo.
- **inspiration_value**: low — Standard handover template. The "FR number + file:lines reference" specificity is David-specific rather than portable.
- **uniqueness_refined**: commodity — PO/Dev handover templates are standard practice.
- **composability**: standalone — Self-contained template application.
- **description_craft_refined**: absent — The description is just "Standard format for PO ↔ Developer communication" with no trigger guidance. Triggers are only in the skill body.

## Mineable phrasing
> "References, not walls of text — Link to docs, don't paste them" / "Traceable — FR numbers, file locations, line numbers"

## Notes
The "references not walls of text" principle is the most portable idea and directly relevant to any skill that produces handover or summary documents. The bidirectional template design (each direction has distinct sections appropriate to that role) is the key structural decision. The anti-pattern examples (too vague / too much detail / missing references) are the most pedagogically valuable content. The description field needs trigger phrases added to be properly discoverable.
