---
artifact_id: agent-skills-osmani:skill:doubt-driven-development
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [verification-validation, code-review]
phase_fit: [5, 6]
evaluated_at: 2026-05-17
---

# Eval: doubt-driven-development

**Intent**: Materializes a fresh-context adversarial reviewer biased to disprove before any non-trivial decision stands, with cross-model escalation.

## Scores
- **quality_score**: 5 — Five-step checklist (CLAIM/EXTRACT/DOUBT/RECONCILE/STOP), non-trivial decision definition, adversarial prompt verbatim, cross-model escalation with Gemini/Codex CLI invocation patterns, bounded loop (max 3 cycles), "doubt theater" red flag, and degraded-mode fallback for nested subagent contexts. Exceptional procedural discipline.
- **adoption_fit_final**: strong — No equivalent in David's current stack. The orchestrator-only constraint (cannot be inside a persona) fits Claude Code's main-session model.
- **inspiration_value**: high
- **uniqueness_refined**: rare — The CLAIM/EXTRACT separation (strip reasoning before handing to reviewer), "doubt theater" anti-pattern detection, and mandatory cross-model offer are genuinely novel process safeguards.
- **composability**: calls-others — Spawns fresh-context reviewers (personas or generic subagents); explicitly integrates with TDD (RED step = doubt made concrete).
- **description_craft_refined**: trigger — High-specificity trigger with explicit "When NOT to use" scoping.

## Mineable phrasing
> "Pass ARTIFACT + CONTRACT only. Do NOT pass the CLAIM. Handing the reviewer your conclusion biases it toward agreement."

## Notes
The CLAIM/EXTRACT split is the load-bearing idea: strip your own reasoning chain from what you hand the reviewer so you get genuine adversarial review rather than confirmation. The cross-model escalation section (with shell-escaping safety notes for Gemini/Codex) shows production-level thinking. The "doubt theater" red flag (two cycles, zero actionable findings = you are validating not doubting) is a sharp meta-check. Top 3 quality candidate.
