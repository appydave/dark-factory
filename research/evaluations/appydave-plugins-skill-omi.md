---
artifact_id: appydave-plugins:skill:omi
repo: appydave-plugins
artifact_type: skill
cluster_facet: [discovery-routing, knowledge-capture, orchestration]
phase_fit: [7, 8, 9]
evaluated_at: 2026-05-17
---

# Eval: omi

**Intent**: Pipeline orchestrator for OMI wearable transcripts — sync from API, extract and classify with Gemini, surface brain-update backlog, and keep discovery queries fresh.

## Scores
- **quality_score**: 4 — The four-step pipeline (sync → extract → backlog report → update discovery queries) is well-sequenced. The monitoring ownership ("Claude does this, not the user — poll every ~30 seconds") is the right user experience design for a background-running process. The discovery query maintenance step (Step 4) is the most distinctive piece — it keeps `random-queries.yml` current based on what brains emerged from the latest batch, rather than manual curation. The quota awareness (Flash-Lite 1,000 RPD, clean resume on next-day re-run) is production-grade.
- **adoption_fit_final**: strong — David wears OMI daily, 891 transcripts already in raw-intake.
- **inspiration_value**: mid — The "update discovery queries based on what brains appeared in this batch" mechanism is the most portable idea — it's a feedback loop between raw intake and routing configuration.
- **uniqueness_refined**: rare — OMI-specific. But the intake pipeline pattern (sync → extract → classify → route → surface backlog) is portable to any ambient data source.
- **composability**: calls-others — Calls omi-fetch script and omi-extract. Outputs feed query_omi and query_brain CLI tools. Step 4 writes to random-queries.yml.
- **description_craft_refined**: trigger — Triggers are specific to OMI vocabulary. "catch up on omi" and "run omi pipeline" are the natural phrases.

## Mineable phrasing
> "After extract completes, surface the brain-update backlog so the user knows what needs actioning" — closes the loop from raw intake to knowledge curation

## Notes
The Step 4 discovery query maintenance is the most intellectually interesting part of this skill — it represents a closed feedback loop where the intake pipeline itself updates its own routing configuration based on observed topic frequency. This is a primitive form of self-organizing routing. The brains-index.json dependency for extract (knowing which brains exist to route to) is the right integration point. The "skip on routine daily syncs" qualifier for Step 4 is appropriate — it prevents unnecessary configuration churn.
