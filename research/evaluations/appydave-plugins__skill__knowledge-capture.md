---
artifact_id: appydave-plugins:skill:knowledge-capture
repo: appydave-plugins
artifact_type: skill
cluster_facet: [memory-management, knowledge-persistence, session-handover]
phase_fit: [0]
evaluated_at: 2026-05-17
---

# Eval: knowledge-capture

**Intent**: Extracts durable, reusable patterns from a session and writes them to Claude's persistent memory files (MEMORY.md + topic files), with explicit qualification criteria for what warrants capture.

## Scores

- **quality_score**: 4. Strong qualification taxonomy (what to write vs. not), clear file structure, MEMORY.md format with lean-index + topic-files separation. Docked one point: scope options at the end feel appended rather than integrated.
- **adoption_fit_final**: `strong`. Fully stack-agnostic; the process of extracting durable knowledge from sessions applies to any project context.
- **inspiration_value**: `high`. The tri-skill role split (knowledge-capture for AI memory / capture-context for handover / brain-bridge for human docs) is a rare and precise decomposition that most systems collapse into one blob.
- **uniqueness_refined**: `uncommon`. Explicit qualification criteria ("write / do not write") for memory capture is not common; most memory skills just write everything.
- **composability**: `standalone`. No chaining required; called independently but works alongside capture-context and brain-bridge.
- **description_craft_refined**: `trigger`. Description has the tri-role disambiguation embedded in the first three lines, which is outstanding discovery design.

## Mineable phrasing

> "knowledge-capture → conversation → Claude's memory (AI persists this across all sessions)"

## Notes

The "update, don't duplicate" principle enforced as a first-class process step (read MEMORY.md before writing) prevents the common failure mode of memory accumulation without consolidation. The MEMORY.md format — brief index line + link to topic file — models a sustainable size-bounded memory architecture. The 200-line cap with topic file spill is directly reusable in any persistent memory design.
