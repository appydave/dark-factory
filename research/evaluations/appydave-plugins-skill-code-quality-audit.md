---
artifact_id: appydave-plugins:skill:code-quality-audit
repo: appydave-plugins
artifact_type: skill
cluster_facet: [code-review, test-authoring, workflow-architecture]
phase_fit: [2, 4, 6, 9]
evaluated_at: 2026-05-17
---

# Eval: code-quality-audit

**Intent**: Deep code quality audit of production source files graded A–D per file/layer, surfacing top-5 issues by severity with a readiness verdict.

## Scores

- **quality_score**: 4 — The skill is well-structured: upfront clarification before broad-scanning, eight audit dimensions (Correctness, Security, Performance, Maintainability, Silent Failure Modes, Data Integrity, Type Safety, Domain Semantics), A–D grading with honest discipline ("Do not soften a D to a C to be polite"), and a readiness verdict that frames the output relative to the next planned feature. The "BLOCKER = data corruption, security hole, silent data loss — must fix before building on this" definition is concrete and useful. The explicit cross-reference to test-quality-audit as a parallel sister skill (with "neither substitutes for the other") is good design.
- **adoption_fit_final**: strong — Already in David's stack. The design patterns (A–D grading, BLOCKER definition, verdict framed as readiness for next-feature, parallel sister skill invocation) are reusable in any audit skill.
- **inspiration_value**: mid — The "grade on evidence from the code, not assumptions" and "verdict is a professional recommendation, not a summary of grades" discipline notes are worth extracting. The eight audit dimensions provide a reusable checklist shape.
- **uniqueness_refined**: uncommon — The verdict-as-readiness-for-next-feature framing (rather than a static pass/fail) is not common. Most audit skills produce a report; this one produces a deployment decision.
- **composability**: called-by-others — Called both directly and by `codebase-audit` orchestrator as a subagent.
- **description_craft_refined**: trigger — Good trigger phrases; the "always launch in parallel with test-quality-audit" directive is load-bearing.

## Mineable phrasing

> "Grade on evidence from the code, not assumptions. BLOCKER = data corruption, security hole, silent data loss — must fix before building on this. Do not soften a D to a C to be polite."

## Notes

The verdict framing is the most portable pattern: instead of "here are the issues," the output answers "is this codebase ready to build [specific next feature] on top of?" This context-anchors the audit to the current work rather than producing a generic health report. The BLOCKER definition is crisp enough to be load-bearing in any code review skill. No Ruflo dependency; could be used in any Claude Code session.
