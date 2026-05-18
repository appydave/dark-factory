---
artifact_id: appydave-plugins:skill:near-compaction
repo: appydave-plugins
artifact_type: skill
cluster_facet: [delivery-readiness, knowledge-capture, orchestration]
phase_fit: [6, 7, 8, 9]
evaluated_at: 2026-05-17
---

# Eval: near-compaction

**Intent**: Orchestrate all context-saving actions before the Claude context window fills up — triage what matters, run session-checkpoint / capture-context / knowledge-capture in the right order, so nothing important is lost before compaction fires.

## Scores
- **quality_score**: 5 — The triage-first design (assess session type → decide which steps apply → skip inapplicable ones) prevents cargo-cult execution of all steps on a 10-minute Q&A. The execution order rationale (each step builds on the previous — checkpoint → handover → memory) is correct and explicit. The four scope options (Full / Quick / Memory only / Dry run) cover the real usage variants. "Negative knowledge is always worth capturing — even short sessions produce 'we tried X and it failed'" is a strong principle.
- **adoption_fit_final**: strong — David's own skill, directly solving a problem he faces regularly.
- **inspiration_value**: high — The triage-before-execution pattern (assess session type, decide which steps apply) is the highest-signal portable idea. It prevents a common anti-pattern: running all steps regardless of whether the session warrants them.
- **uniqueness_refined**: rare — Compaction-aware orchestrator skills are rare in the corpus. ECC has compaction hooks but they're hook-based, not skill-based.
- **composability**: calls-others — Orchestrates session-checkpoint, capture-context, and knowledge-capture. Near-compaction IS the orchestration layer.
- **description_craft_refined**: trigger — "Near compaction", "running out of context", "save everything before we compact" are all accurate and natural.

## Mineable phrasing
> "Triage honestly — don't run all 5 steps on a 10-minute Q&A session; skip what doesn't apply" / "Negative knowledge is always worth capturing — even short sessions produce 'we tried X and it failed'"

## Notes
The triage table (question → if yes → run which skill) is a clean decision pattern that prevents wasted effort and inappropriate output. The "after running" guidance (tell user what was saved, how to resume, whether it's safe to /compact) closes the loop correctly. The distinction between session-checkpoint (which step to start on) and capture-context (what happened and why) and knowledge-capture (durable patterns) is the clearest skill-family boundary in the corpus.
