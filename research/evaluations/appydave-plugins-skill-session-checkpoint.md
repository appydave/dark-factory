---
artifact_id: appydave-plugins:skill:session-checkpoint
repo: appydave-plugins
artifact_type: skill
cluster_facet: [knowledge-capture, planning, workflow-architecture]
phase_fit: [1, 2, 7, 8, 9]
evaluated_at: 2026-05-17
---

# Eval: session-checkpoint

**Intent**: Capture exact mid-session task progress (step-by-step plan with statuses) to a checkpoint file so a new session can resume precisely where work stopped.

## Scores
- **quality_score**: 4 — The three-skill family disambiguation (session-checkpoint vs capture-context vs knowledge-capture) is a mature cognitive model that prevents misuse. The "YOU ARE HERE" marker in the output template, the "Before Starting Next Step" section, and the "exactly one In Progress" invariant are all high-value operational constraints.
- **adoption_fit_final**: strong — Already David's own skill, zero adoption friction. The scope options (quick/full/path/print) and the explicit resume protocol are production-hardened features.
- **inspiration_value**: mid — The three-skill family taxonomy (progress state vs session summary vs durable knowledge) is a clean conceptual split worth propagating. The "Before Starting Next Step" section in the checkpoint template is the insight: it makes pre-conditions machine-readable rather than buried in prose.
- **uniqueness_refined**: uncommon — Checkpoint-as-skill (rather than checkpoint-as-manual-habit) is not common in the corpus; the structured template with invariants is the differentiator.
- **composability**: standalone — Output is a file; no upstream/downstream agent invocations.
- **description_craft_refined**: trigger — Description uses "Use when user says..." with six trigger phrases plus a context-triggered case ("or when about to do a risky operation or context is filling up").

## Mineable phrasing
> "A checkpoint answers: 'If this session ended right now, which step would the next session start on, and what's already done?'"

## Notes
The one-sentence purpose statement ("A checkpoint answers: if this session ended right now...") is a model "what does this skill actually do" formulation — concrete, answerable, memorable. The "STOP — this is a checkpoint from a previous session. Read everything before doing anything." header in the output template is a smart anti-footgun: it prevents the next Claude instance from skipping context. The distinction between this skill and `capture-context` (handover) and `knowledge-capture` (durable patterns) is an underrated taxonomy that other skill families could replicate.
