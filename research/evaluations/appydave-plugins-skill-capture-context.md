---
artifact_id: appydave-plugins:skill:capture-context
repo: appydave-plugins
artifact_type: skill
cluster_facet: [knowledge-capture]
phase_fit: [7, 8]
evaluated_at: 2026-05-17
---

# Eval: capture-context

**Intent**: Produce a structured session handover document that lets a new Claude session resume without re-reading the conversation or rediscovering key context.

## Scores
- **quality_score**: 5 — Exceptionally well-designed. The three-skill comparison table (capture-context vs session-checkpoint vs knowledge-capture) is exactly the right disambiguation. The output format is battle-tested — every section has a clear purpose. The "Gotchas are the most valuable section" principle is actionable and correct. The explicit "never write into the project directory" rule prevents a common mistake.
- **adoption_fit_final**: strong — David's own skill, already in use. No adoption friction.
- **inspiration_value**: high — "What We Ruled Out" as a first-class section (negative knowledge as session artifact) is the highest-signal portable concept. "Gotchas are the most valuable section" is a reusable framing principle.
- **uniqueness_refined**: uncommon — Most handover patterns exist but the explicit negative-knowledge section and the "decisions need rationale not just what" framing are differentiated.
- **composability**: called-by-others — Called by near-compaction as step 2. Can run standalone.
- **description_craft_refined**: trigger — All trigger phrases are first-person natural language. Well-crafted.

## Mineable phrasing
> "Gotchas are the most valuable section — capture anything that took effort to discover or would be easy to get wrong again" / "What We Ruled Out is the second most valuable — prevents the next session repeating dead ends"

## Notes
The three-skill disambiguation (capture-context / session-checkpoint / knowledge-capture) is the clearest skill-family boundary documentation in the corpus. The output template's STOP header ("STOP — this is a handover from a previous session. Read everything before doing anything.") is a clever mechanism to prevent the next session from acting before understanding. The "never write into the project directory" constraint is specific and correct.
