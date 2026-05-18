---
artifact_id: agent-skills-osmani:skill:security-and-hardening
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [code-implementation, verification-validation]
phase_fit: [3, 4, 5, 6]
evaluated_at: 2026-05-17
---

# Eval: security-and-hardening

**Intent**: Apply security-first practices to every line of code touching user input, authentication, data storage, or external integrations — treating all external input as hostile and all secrets as sacred.

## Scores
- **quality_score**: 5 — Three-tier boundary system (Always Do / Ask First / Never Do) is an unusually structured governance model for a coding skill. OWASP Top 10 with code examples (injection, broken auth, XSS, broken access control, misconfiguration, sensitive data exposure), input validation with Zod, file upload safety, npm audit triage decision tree, rate limiting, and secrets management patterns together form a complete security reference.
- **adoption_fit_final**: strong — Language-agnostic security principles; Express/TypeScript/Zod examples but the three-tier boundary model, OWASP coverage, and audit triage tree are universally applicable. Not stack-locked.
- **inspiration_value**: high — The three-tier boundary system (Always/Ask First/Never) is the most structured agent governance model for security decisions in the corpus — it converts security policy into a decision tree an agent can follow without human guidance. The npm audit triage tree (critical-reachable → fix immediately; critical-unreachable → fix soon; moderate-production → next cycle; dev-only → when convenient) is a pragmatic filter that prevents alert fatigue.
- **uniqueness_refined**: uncommon — The "Ask First" middle tier (requires human approval for auth flow changes, new PII storage, CORS changes, file uploads) is not found in other security skills — it acknowledges that some security decisions are not autonomous.
- **composability**: standalone — Security constraints applied during implementation; no sub-agent invocations.
- **description_craft_refined**: trigger — Description gives six distinct trigger conditions covering input, auth, storage, integrations, file uploads, and payments.

## Mineable phrasing
> "Security isn't a phase — it's a constraint on every line of code that touches user data, authentication, or external systems."

## Notes
The "Ask First" tier (human approval required before adding auth flows, storing new PII categories, or changing CORS) is the most mature autonomy-boundary statement in the corpus for security. It distinguishes between decisions an agent can make independently (input validation, parameterised queries) and decisions that require human oversight. The rate limiting section (general API vs stricter auth endpoint limit) with numeric examples (100 requests/15min vs 10 attempts/15min) converts policy into implementable specifics. The secrets management file tree (.env.example committed, .env not committed, .env.local not committed) is a clear visual that prevents the most common secrets-in-git failure.
