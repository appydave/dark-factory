---
artifact_id: agent-skills-osmani:agent:security-auditor
repo: agent-skills-osmani
artifact_type: agent
cluster_facet: [code-review, verification-validation]
phase_fit: [5, 6]
evaluated_at: 2026-05-17
---

# Eval: security-auditor

**Intent**: Security-engineer persona focused on exploitable vulnerabilities, threat modeling, and practical hardening recommendations with OWASP Top 10 as baseline.

## Scores
- **quality_score**: 4 — Five review scope sections (input handling, auth/authz, data protection, infrastructure, third-party), severity classification table (Critical→Info), structured output format with proof-of-concept requirement for high/critical, seven rules. Clean and usable.
- **adoption_fit_final**: strong — David's stack includes SupportSignal (NDIS app with PII), FliVideo (multi-user), and kybernesis SaaS — all have real security surface area. David's `security-review` skill overlaps but this is the persona variant optimized for focused review sessions.
- **inspiration_value**: mid
- **uniqueness_refined**: uncommon — Proof-of-concept requirement for Critical/High findings and the "Positive Observations" section (acknowledging good security practices) are notable differentiators from generic security checklists.
- **composability**: called-by-others — Designed for `/ship` parallel fan-out alongside `code-reviewer` and `test-engineer`.
- **description_craft_refined**: trigger — "Use for security-focused code review, threat analysis, or hardening recommendations."

## Mineable phrasing
> "Focus on practical, exploitable issues rather than theoretical risks."

## Notes
The "Positive Observations" section is a craft choice that encourages balanced reviews rather than pure negative lists — valuable for agent-generated reports that need to be actionable without demoralizing. The proof-of-concept requirement for Critical/High findings enforces specificity and prevents vague "this could be vulnerable" findings. Pairs cleanly with `doubt-driven-development` for high-stakes security decisions.
