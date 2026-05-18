---
artifact_id: appydave-plugins:skill:skill-miner
repo: appydave-plugins
artifact_type: skill
cluster_facet: [knowledge-capture, self-improvement, skill-authoring]
phase_fit: [7, 8, 9, 10]
evaluated_at: 2026-05-17
---

# Eval: skill-miner

**Intent**: Mines Claude Code session transcripts (JSONL files) for recurring patterns and promotes them into skill candidates via a friction × frequency × cost scoring model, with decay over time.

## Scores

- **quality_score**: 5 — This is one of the most sophisticated self-improvement skills in the catalog. The design decisions are all well-justified: friction over frequency (corrections are better signal than repetition), hot-capture > cold mining (mid-session log mode carries higher weight), accumulation with decay (60/120/180-day scoring multipliers), evidence not summarisation (verbatim snippets, session IDs). The two-mode design (scan vs log) addresses both retrospective and in-the-moment capture. The promotion threshold (3+ instances, within 90 days, no existing promoted/<slug>.md) is concrete and testable. The integration with AngelEye (live) vs skill-miner (retrospective) is a well-thought-out separation of concerns.
- **adoption_fit_final**: strong — Already in David's stack. The friction × frequency × cost scoring model and the candidate decay system are uniquely his design. Highly relevant to stage 10 (observability of the harness itself).
- **inspiration_value**: high — The "friction over frequency" principle is a genuinely better heuristic than raw repetition for skill candidate identification. The "hard rules" section (never auto-install, never paraphrase examples, cap at 5 snippets) articulates what makes skill-mining trustworthy rather than noisy. The decay model prevents the candidates list from becoming stale cruft.
- **uniqueness_refined**: rare — Session-transcript mining with friction-weighted scoring and decay is not a common pattern. Most self-improvement skills capture in-session only; this adds a batch retrospective mode with statistical reasoning.
- **composability**: calls-others — Log mode integrates with AngelEye (live ingestion) and promotion feeds into skill-creator. Embedded in a larger pipeline.
- **description_craft_refined**: trigger — Description is detailed and contains all trigger phrases across both modes. Slightly long but justified by the two-mode design.

## Mineable phrasing

> "Friction > frequency. Pure repetition counts are weak signal. The same question asked twice is just normal work; a question that triggered a correction twice is a skill-shaped hole."

## Notes

The friction-over-frequency principle is directly applicable to David's stage 10 (observability gap identification): the places where the harness causes corrections, dead ends, or high cost are where new skills are needed — not places where tasks are simply repeated. The decay model (60/120/180-day multipliers with archiving at 180 days) is an observability mechanism for the skill-candidate pipeline itself — it surfaces not just "what patterns exist" but "what patterns are still active." This is a rare example of a skill that reasons about its own data quality. No Ruflo dependency.
