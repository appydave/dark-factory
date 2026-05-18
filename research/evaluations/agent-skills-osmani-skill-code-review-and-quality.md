---
artifact_id: agent-skills-osmani:skill:code-review-and-quality
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [code-review]
phase_fit: [6]
evaluated_at: 2026-05-17
---

# Eval: code-review-and-quality

**Intent**: Multi-axis code review skill that evaluates changes across five dimensions (correctness, readability, architecture, security, performance) before any merge, covering both agent-authored and human-authored code.

## Scores
- **quality_score**: 5 — Exceptional depth: five axes fully defined, change-sizing guidelines with explicit line counts, severity-labelled feedback taxonomy (Critical/Nit/Optional/FYI), multi-model review pattern, dead-code hygiene protocol, anti-rationalization table, honesty norms. Everything a reviewable skill needs.
- **adoption_fit_final**: strong — Skill-shaped, no stack lock. David already has `code-quality-audit` and `architectural-review` in his stack but neither covers the full five-axis framework with this fidelity. Direct integration candidate.
- **inspiration_value**: high — The severity-label taxonomy (prefix-based severity vs. mandatory/optional distinction) and the anti-rationalization table ("AI-generated code is probably fine" → "AI code needs more scrutiny, not less") are immediately adoptable language.
- **uniqueness_refined**: rare — The multi-model review pattern (Model A writes, Model B reviews, human makes final call) is a concrete mechanism not present in David's existing review skills. The dead-code hygiene ask-before-delete protocol is also uncommon.
- **composability**: called-by-others — Invoked explicitly by `/review` command and by `/ship` fan-out. Can also be invoked standalone.
- **description_craft_refined**: trigger — Description uses "Use before merging any change. Use when reviewing code written by yourself, another agent, or a human." Well-formed trigger phrasing across three actor types.

## Mineable phrasing
> "AI-generated code is probably fine" → "AI code needs more scrutiny, not less. It's confident and plausible, even when wrong."

## Notes
This is the reference mechanism for code review in the Osmani cluster. The five-axis framework with explicit severity labels solves the common problem of authors treating all feedback as mandatory. The multi-model review pattern (cross-reviewer blind spots) is a genuine mechanism gap in David's current stack — his `code-quality-audit` skill focuses on static quality but lacks the agent-to-agent review dispatch concept.
