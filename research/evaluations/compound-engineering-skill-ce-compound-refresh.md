---
artifact_id: compound-engineering:skill:ce-compound-refresh
repo: compound-engineering
artifact_type: skill
cluster_facet: [knowledge-capture, self-improvement]
phase_fit: [7, 8, 10]
evaluated_at: 2026-05-17
---

# Eval: ce-compound-refresh

**Intent**: Maintains `docs/solutions/` by reviewing stale learning docs against the current codebase and applying Keep/Update/Consolidate/Replace/Delete classifications with headless mode for automation.

## Scores

- **quality_score**: 5 — This is the most thorough knowledge-maintenance skill in the catalog. The five-outcome maintenance model (Keep/Update/Consolidate/Replace/Delete) with explicit criteria for each is well-designed. The Phase 1.75 "Document-Set Analysis" (overlap detection, supersession signals, canonical doc identification, retrieval-value test) is an unusual and valuable layer — it reasons about the document set as a whole, not just individual documents. The headless/interactive mode split is production-quality. The inbound-link check before deletion (search markdown, classify as decorative vs substantive, only auto-delete when all three conditions hold) prevents accidental loss of load-bearing references. The "delete, don't archive" rule (git history is the archive) is an opinionated but well-justified design decision. The Discoverability Check at the end (does AGENTS.md/CLAUDE.md surface the knowledge store to agents?) is a self-referential loop that makes the system self-maintaining.
- **adoption_fit_final**: mid — The skill is tightly coupled to the compound-engineering docs/solutions/ structure and workflow. The maintenance model (five outcomes + Phase 1.75 document-set analysis) is fully portable. The headless mode and discoverability check are directly applicable to David's brains system. The platform-agnostic question-tool design (AskUserQuestion in Claude Code, request_user_input in Codex, etc.) shows cross-harness awareness.
- **inspiration_value**: high — The "Document-Set Analysis" phase (reasoning about the document set as a whole, not just individual freshness) is rare. The retrieval-value test ("would having these as separate docs improve discoverability, or just create drift risk?") is a sophisticated design criterion. The discoverability check (does the instruction file teach agents where the knowledge store is?) is a self-reinforcing loop worth adopting in brains maintenance.
- **uniqueness_refined**: rare — Five-outcome maintenance model with document-set-level analysis and inbound-link graph traversal is not common in knowledge-maintenance skills. Most maintenance skills check for freshness only.
- **composability**: calls-others — Calls investigation subagents and replacement subagents. Can be called by ce-compound after writing a new learning.
- **description_craft_refined**: trigger — Description covers the trigger cases well. The headless mode flag in argument-hint is load-bearing for automation use.

## Mineable phrasing

> "Two docs covering the same ground will eventually drift apart and contradict each other — that is worse than a slightly longer single doc."

## Notes

The document-set analysis layer (Phase 1.75) is the most portable design idea: before classifying individual documents, step back and ask whether the set as a whole is well-designed. For David's brains, this maps directly: multiple INDEX.md files across different brains can accumulate contradictory claims over time — the Phase 1.75 approach would catch this. The "delete, don't archive" rule is a clean design principle that prevents the accumulation of dead weight in knowledge systems. The discoverability check (making sure AGENTS.md/CLAUDE.md teaches future agents where the knowledge store is) is directly applicable to David's CLAUDE.md files. No Ruflo dependency.
