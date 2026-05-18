---
artifact_id: agent-skills-osmani:skill:documentation-and-adrs
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [documentation, knowledge-capture]
phase_fit: [6, 7, 8]
evaluated_at: 2026-05-17
---

# Eval: documentation-and-adrs

**Intent**: Skill that records architectural decisions and the reasoning behind them via ADRs, capturing why decisions were made (not just what was built) so future engineers and agents can understand the codebase without re-deciding.

## Scores
- **quality_score**: 4 — Solid and complete: full ADR template with lifecycle states (PROPOSED → ACCEPTED → SUPERSEDED), inline comment discipline ("comment the why, not the what"), agent-specific guidance (CLAUDE.md as first-class doc target), anti-rationalization table. Slightly generic in mechanism — largely good engineering practice codified rather than novel mechanism.
- **adoption_fit_final**: mid — David has `knowledge-capture` skills and brain documentation patterns. The ADR lifecycle template is worth adopting but the broader skill overlaps heavily with existing `doc-review` family. The agent-oriented doc section ("Agents do. Future engineers do. Your 3-months-later self does.") is the most differentiated part.
- **inspiration_value**: mid — ADR template is clean and adoptable. The "APIs stabilize faster when you document them — the doc is the first test of the design" framing is useful language for convincing teams to document early.
- **uniqueness_refined**: commodity — ADR patterns are widely known. This implementation is clean but the mechanism is standard. The "rules files / CLAUDE.md as first-class documentation target for agents" section is the one genuinely novel element.
- **composability**: standalone — Can be invoked independently. Not called by other skills in the cluster.
- **description_craft_refined**: trigger — "Use when making architectural decisions, changing public APIs, shipping features, or when you need to record context that future engineers and agents will need to understand the codebase." Strong trigger-phrase coverage across four distinct entry points.

## Mineable phrasing
> "Nobody reads docs" → "Agents do. Future engineers do. Your 3-months-later self does."

## Notes
The most differentiated section is the "Documentation for Agents" block, which frames CLAUDE.md / rules files as first-class documentation targets rather than configuration files. This is directly relevant to David's brain/skill architecture. The ADR template itself is standard but well-executed; the lifecycle don't-delete rule ("don't delete old ADRs — they capture historical context") aligns with David's explicit memory principle of never deleting brain documents.
