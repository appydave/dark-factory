---
artifact_id: appydave-plugins:skill:conversation-triage
repo: appydave-plugins
artifact_type: skill
cluster_facet: [code-review, knowledge-capture, orchestration]
phase_fit: [6, 7, 8, 9]
evaluated_at: 2026-05-17
---

# Eval: conversation-triage

**Intent**: Mid-conversation audit that surfaces open questions, loose threads, parked topics, decisions made, and unstated assumptions in the current session — read-only, real-time.

## Scores

- **quality_score**: 4 — The output format is the strongest feature: seven distinct bucket types (Decisions Made, Open Questions, Parked/Deferred, Loose Threads, Observations Not Followed Up, Load-bearing Assumptions, Implied Next Actions) with clear membership criteria. The disambiguation table (vs capture-context, session-checkpoint, knowledge-capture, near-compaction) is well-designed — it positions the skill precisely in a crowded space. The triage discipline ("Surface, don't resolve") prevents scope creep. The scope options (Full, Recent, Topic, Quick) provide useful granularity.
- **adoption_fit_final**: strong — Already in David's stack. The bucket taxonomy and "surface, don't resolve" discipline are directly portable to any context-recovery skill.
- **inspiration_value**: mid — The "Load-bearing Assumptions" bucket is the most valuable addition to standard triage templates — assumptions are the most commonly missed category. The "Flag blockers explicitly" discipline ([BLOCKING: X] notation) is portable.
- **uniqueness_refined**: uncommon — Seven-bucket triage with explicit "Load-bearing Assumptions" and disambiguation from related skills is more structured than most session-triage implementations.
- **composability**: standalone — Read-only, no calls to other skills, not called as subagent.
- **description_craft_refined**: trigger — Rich trigger phrase list covering all natural conversational phrasings. Functional.

## Mineable phrasing

> "Surface, don't resolve — this skill identifies open items, it doesn't close them. Err toward inclusion — if something might be a loose thread, list it."

## Notes

The "Load-bearing Assumptions" bucket is a dark-factory-relevant concept: in multi-session agent workflows, undocumented assumptions are the primary source of context corruption across sessions. A skill that specifically hunts for unstated assumptions is an observability tool for the reasoning layer. The disambiguation table design (same trigger phrases → different skills → explicit routing table) is a pattern worth applying to any skill family with overlapping trigger phrases. Ruflo-independent.
