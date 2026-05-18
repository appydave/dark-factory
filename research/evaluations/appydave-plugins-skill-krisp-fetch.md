---
artifact_id: appydave-plugins:skill:krisp-fetch
repo: appydave-plugins
artifact_type: skill
cluster_facet: [knowledge-capture]
phase_fit: [7, 8]
evaluated_at: 2026-05-17
---

# Eval: krisp-fetch

**Intent**: Fetch meeting recordings and transcripts from the Krisp API and save them to the raw-intake pipeline for AI processing.

## Scores
- **quality_score**: 3 — The git-aware sync script (pull → fetch → commit → push) mirrors the OMI sync pattern correctly — consistency across intake sources is good. The token refresh instructions (DevTools Bearer token grab) are specific and practical. The timezone handling (UTC → Bangkok display) reflects real usage. Loses points because the Bearer token approach is session-scoped and the error handling table, while correct, covers the same ground as OMI. This skill has narrow adoption scope (Krisp-specific).
- **adoption_fit_final**: strong — David uses Krisp on mobile and desktop. Already in use.
- **inspiration_value**: low — The OMI/Krisp parallel intake pattern is interesting but covered better by the OMI skill.
- **uniqueness_refined**: rare — Krisp API integration is unique to David's personal stack.
- **composability**: called-by-others — Output feeds into raw-intake pipeline, which is then processed by omi-extract.
- **description_craft_refined**: trigger — Trigger phrases cover all the natural ways to invoke it.

## Mineable phrasing
> `none`

## Notes
The "mirrors the OMI sync pattern" note in the skill is the right documentation approach — it connects this narrow tool to the broader intake architecture. The `krisp_sync.sh` script approach (git-aware, pull before push) is the right pattern for any intake sync that writes to a tracked repo. The file format (`YYYY-MM-DD-HHmm-{title-slug}.md`) is consistent with the OMI intake format, enabling unified downstream processing. Limited inspiration value beyond David's specific setup.
