---
artifact_id: compound-knowledge:skill:kw-compound
repo: compound-knowledge-plugin
artifact_type: skill
cluster_facet: [compound-knowledge, knowledge-capture, session-close]
phase_fit: [stage-10]
evaluated_at: 2026-05-17
---

# Eval: kw-compound

**Intent**: Closes a work session by extracting 1-3 approved learnings, deduplicating against existing knowledge, and saving structured markdown to `docs/knowledge/`.

## Scores
- **quality_score**: 4 — Well-structured 5-step flow with explicit approval gate, duplicate check, stale-knowledge sub-agent call, and pipeline mode for automation
- **adoption_fit_final**: mid — `docs/knowledge/` path convention is light coupling; pipeline mode makes it automation-friendly; type taxonomy (insight/playbook/correction/pattern) is portable
- **inspiration_value**: mid — The "1-3 learnings max, quality over quantity" constraint and the stale-knowledge-checker delegation pattern are the reusable ideas
- **uniqueness_refined**: uncommon — Approval-required + stale-check before save is a cleaner variant than most knowledge-capture skills
- **composability**: calls-others — Delegates stale check to `stale-knowledge-checker` agent; orchestrator retains write authority
- **description_craft_refined**: trigger — "Compound this session", "Save what we learned" are natural trigger phrases embedded in When to Use

## Mineable phrasing
> "Nothing from this session seems worth saving as a standalone learning. The work is captured in the plan/deliverables."

## Notes
The explicit boundary — agents return text only, orchestrator writes files — is a clean separation of concerns worth preserving. Pipeline mode (skip confirmations, structured output) is a thoughtful addition for automation. The skill is narrow by design; its strength is the constraint "1-3 max" preventing knowledge bloat.
