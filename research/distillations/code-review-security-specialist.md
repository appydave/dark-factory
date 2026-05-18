---
distillation_id: code-review-security-specialist
stage: audit
intent: "Security-focused code review — exploitable vulnerability detection, injection vectors, auth/authz bypasses, secrets hygiene — with lower confidence threshold due to high miss cost"
created: 2026-05-16
status: draft
source_artifacts:
  - compound-engineering:agent:ce-security-reviewer
  - compound-engineering:agent:ce-security-lens-reviewer
  - compound-engineering:agent:ce-security-sentinel
  - agent-skills-osmani:agent:security-auditor
  - agent-skills-osmani:skill:security-and-hardening
  - appydave-plugins:skill:security-analyst
  - appydave-plugins:skill:prompt-injection-scanner
  - ruflo:skill:agent-security-manager
  - ruflo:skill:agent-v3-security-architect
  - ruflo:skill:security-audit
  - ruflo:skill:"V3 Security Overhaul"
  - ruflo:agent:security-auditor
  - ruflo:command:aidefence
  - everything-claude-code:agent:security-reviewer
winner_mechanism: compound-engineering:agent:ce-security-reviewer
---

# Unified Skill: code-review-security-specialist

**Purpose**: Security-axis specialist reviewer that operates as a **7th dimension** available to `delivery-review`, or standalone when the diff touches auth, public endpoints, user input, or payment flows. Lower confidence threshold than other dimensions — P0 + anchor 50 always reports because the cost of missing a real vulnerability exceeds the cost of a false positive.

**For Agents**: Use when David says "security review", "check for vulnerabilities", "is this auth code safe", "review this before going public". This can run standalone or be added as an optional 7th dimension to `delivery-review` when the scope triggers security signals.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

## Intent

Detect exploitable vulnerabilities by tracing attack paths (not auditing checklists), with calibrated confidence that biases toward reporting at P0 because missed vulnerabilities compound in production while false positives are merely annoying.

## Winner's Mechanism

`compound-engineering:agent:ce-security-reviewer` wins. Its core insight is what to review and how:

- **Attack-path tracing not checklist auditing**: "read the diff and ask 'how would I break this?' then trace whether the code stops you" — this is qualitatively different from a compliance list scan.
- **Hunt taxonomy**: injection vectors (trace from entry point to dangerous sink), auth/authz bypasses (ownership checks, CSRF on state-changing ops), secrets in code/logs, insecure deserialization, SSRF/path traversal.
- **Lower effective threshold**: security findings at anchor 50 should be filed at P0 — the miss cost justifies the signal. This is explicitly stated and well-reasoned.
- **What you don't flag**: defense-in-depth on already-protected code, theoretical physical-access attacks, HTTP in dev configs, generic hardening advice without specific findings. This prevents scope bloat.

David has `prompt-injection-scanner` (excellent for pipeline input sanitization) and `security-analyst` (broader posture audit) but no focused diff-scoped security reviewer that applies attack-path tracing to code changes specifically. This is the gap.

## Non-overlapping ideas folded in

- From `agent-skills-osmani:skill:security-and-hardening`: The **Three-Tier Boundary System** (Always Do / Ask First / Never Do) — a posture layer that complements attack-path tracing. Useful as an orientation block in the skill body ("before reviewing, ground yourself in the project's security stance").
- From `agent-skills-osmani:agent:security-auditor`: `references/security-checklist.md` pattern — a companion checklist file for systematic coverage across OWASP Top 10. Separating the checklist from the skill body keeps the skill lean.
- From `appydave-plugins:skill:prompt-injection-scanner`: **Source-typed risk mode** (omi/email/web/document/paste → standard/strict) — useful as a signal for the security reviewer when the diff adds a new data ingestion path. What type of external data is being ingested?
- From `ruflo:command:aidefence`: The **Prompt Defense Baseline** block — injection resistance that belongs in every agent body processing untrusted content. When reviewing agent/skill files (not just application code), check for this block.
- From `everything-claude-code:agent:security-reviewer`: Slightly different attack taxonomy (focuses on OWASP categories) — the CE taxonomy and ECC taxonomy are complementary; ECC is more checklist-shaped, CE is more attack-path shaped. CE wins but ECC fills gaps.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| ce-security-reviewer | Attack-path tracing posture, hunt taxonomy, lower threshold rationale, explicit non-overlap | CE-specific JSON output format (use DVR format) |
| ce-security-lens-reviewer | Applied to plan/doc review scope — confirms pattern is scope-agnostic | Plan-review specifics |
| ce-security-sentinel | "Sentinel" framing — always watching, not just on trigger | Ruflo-infrastructure dependency |
| security-and-hardening (osmani) | Three-tier boundary system (Always/Ask/Never), OWASP Top 10 prevention patterns | Implementation-guidance sections (this is review, not implementation) |
| security-analyst (appydave) | Broader posture audit scope | Full-project audit mechanics (too deep for a diff reviewer) |
| prompt-injection-scanner (appydave) | Source-typed risk mode, Opus pinning for isolation | Pipeline ingestion mechanics (separate skill) |
| aidefence (ruflo) | Prompt Defense Baseline block as a review check for agent artifacts | Ruflo AI defence system mechanics |
| security-reviewer (ecc) | OWASP-category checklist structure, injection resistance baseline | ECC-specific preamble |

## Draft SKILL.md frontmatter

```yaml
name: review-security
description: >
  Diff-scoped security review — traces attack paths, not checklists. Detects injection vectors,
  auth/authz bypasses, secrets in code/logs, insecure deserialization, SSRF, path traversal.
  Lower confidence threshold: P0 findings report at anchor 50 because miss cost is high.
  Use when: "security review", "check for vulnerabilities", "auth code review", "is this safe",
  "review before public launch", "check this payment flow", "injection check".
  Automatically added as a 7th delivery-review dimension when scope touches auth, public endpoints,
  user input handling, or payment flows.
```

## Trigger signals for auto-activation

When adding as a conditional dimension to `delivery-review`, activate when diff touches:
- Auth middleware, login/logout/session management, token handling
- Public API endpoints (routes not behind auth middleware)
- Any function processing user-provided input before use in queries, commands, or output
- Permission/role checks, ownership verification
- Payment, billing, PII data handling
- External webhooks, callbacks, or untrusted data ingestion
- File upload handlers

## Open questions for David

- Should this be added as an **optional 7th dimension** to `delivery-review` with conditional activation (security signals → add dimension)? CE's approach shows this is the right model — always-on adds cost, conditional keeps it fast.
- Is `security-analyst` (project-wide posture) already covering this, making `review-security` redundant? Answer: no — `security-analyst` is a campaign-completion audit; `review-security` is a diff-scoped attack-path trace. Same relationship as `code-quality-audit` vs `review-code-quality`.
- Should `prompt-injection-scanner` be surfaced as a note inside `review-security` when the diff adds a new data ingestion path? Or stay fully separate?
