---
distillation_id: security-review-compliance-overlay
stage: security-review
intent: "Thin compliance-framework overlay (HIPAA/SOC2/GDPR) that wraps the security review stack with framework-specific guardrails — triggered only when a task is explicitly framed around a regulation"
created: 2026-05-17
status: draft
source_artifacts:
  - everything-claude-code:skill:hipaa-compliance
  - everything-claude-code:skill:security-review
  - everything-claude-code:skill:enterprise-agent-ops
winner_mechanism: everything-claude-code:skill:hipaa-compliance
---

# Unified Skill: security-review-compliance-overlay

**Purpose**: A thin, framework-specific entrypoint skill that wraps the existing security review stack with the guardrails and decision gates required by a specific compliance framework (HIPAA being the primary case for SupportSignal). Does not re-implement security review; delegates to the existing stack and adds the regulatory overlay.

**For Agents**: Use when David says "HIPAA review this", "is this PHI handling correct", "check for GDPR compliance", "is this SOC2 compliant", "compliance check", "does this meet healthcare privacy requirements", "BAA needed?". Rare trigger — only activate when the task is explicitly framed around a regulation.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

SupportSignal is an NDIS application handling health-adjacent personal data. While Australian NDIS/Privacy Act compliance is the literal requirement (not US HIPAA), the HIPAA compliance skill is the closest model in the corpus for PHI-adjacent PII handling, audit logging requirements, minimum-necessary access, and BAA-equivalent data processing agreements. The unified skill adapts the HIPAA pattern to the NDIS/Australian Privacy Act context while keeping the delegation model: this is an overlay, not a re-implementation.

## Winner's Mechanism

`everything-claude-code:skill:hipaa-compliance` wins because it exemplifies the **thin-entrypoint-plus-delegation** pattern:

- **Does NOT re-implement** security review, input validation, or auth review — it delegates those to `security-review` and `healthcare-phi-compliance` (its sibling skills).
- **HIPAA-specific decision gates** (5 questions): Is this data PHI? Is this actor a covered entity? Does the vendor need a BAA? Is access minimum-necessary? Are read/write/export events auditable?
- **Guardrails block**: 6 specific "never do this" rules for PHI handling — logs, analytics, crash reports, prompts, client-visible error strings, URLs, browser storage.
- **Framing**: "Treat third-party SaaS, observability, support tooling, and LLM providers as blocked-by-default until BAA status and data boundaries are clear." This is the single most actionable HIPAA insight for a solo developer using SaaS.

The pattern is directly applicable to NDIS work: replace "PHI" with "NDIS participant personal data", replace "HIPAA" with "Australian Privacy Act", replace "BAA" with "data processing agreement" — the structure holds.

## Non-overlapping ideas folded in

- From `everything-claude-code:skill:enterprise-agent-ops`: **Data access minimization for long-lived agents** — when AI agents have read/write access to participant data (e.g., SupportSignal backend agents), they need scoped access tokens and explicit data-minimization controls. HIPAA-compliance doesn't cover this; enterprise-agent-ops does. — `complexity: medium | optional: true | prerequisite: "agent has direct database or API access to participant personal data"`. Critical for Kybernesis-style agent deployments on SupportSignal.
- From `everything-claude-code:skill:security-review`: **LLM prompt contamination check** — the HIPAA skill mentions "never place PHI in prompts" but doesn't provide a check procedure. The security-review skill's input-validation section provides the pattern for how to verify this. — `complexity: low | optional: false | prerequisite: none`. Any LLM call in SupportSignal that uses participant data as context needs this check.

## NDIS/Australian Privacy Act adaptation notes

The skill body should document the Australian equivalents to HIPAA concepts:

| HIPAA concept | Australian Privacy Act / NDIS equivalent |
|---------------|------------------------------------------|
| PHI (Protected Health Information) | Personal information of NDIS participants (sensitive information under APPs) |
| Covered entity | NDIS registered provider, plan manager, support coordinator |
| BAA (Business Associate Agreement) | Data processing agreement required under APP 8 (cross-border disclosure) |
| HIPAA Breach Notification Rule | Notifiable Data Breach (NDB) scheme — OAIC notification within 30 days |
| Minimum necessary standard | APP 3 (collection) + APP 6 (use) — collect and use only what's needed |

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| hipaa-compliance (skill) | Thin-entrypoint + delegation model, 5 decision gates, 6 guardrails, SaaS-blocked-by-default framing | US-specific terminology (HIPAA, PHI, covered entity — replace with APPs) |
| security-review (skill) | LLM prompt contamination check pattern | Full security review workflow (delegated, not duplicated) |
| enterprise-agent-ops | Data access minimization for agents with DB/API access | Full lifecycle management (separate distillation) |

## Draft SKILL.md frontmatter

```yaml
name: security-review-compliance
description: >
  Thin compliance-framework overlay that wraps the security review stack with regulatory guardrails.
  Primary target: Australian Privacy Act / NDIS participant data (SupportSignal context).
  Pattern adapted from HIPAA — applies to any regulated personal data handling.
  Does NOT re-implement security review; delegates to review-security and adds the compliance overlay.
  Use when: "HIPAA review this", "check for compliance", "is this PHI handling correct",
  "GDPR check", "does this meet privacy requirements", "BAA needed", "compliance overlay".
  Rare trigger — only activate when the task is explicitly framed around a regulation.
allowed-tools: "Read, Bash(grep:*)"
```

## Open questions for David

- Should the Australian Privacy Act adaptation be a separate reference file (`references/australian-privacy-act-guardrails.md`) or inline in the SKILL.md body? Given that SupportSignal is the primary context and the framework is stable, a reference file allows reuse across multiple skills.
- ECC's `hipaa-compliance` delegates to `healthcare-phi-compliance` (a sibling skill in ECC that doesn't exist in David's stack). Should this distillation also define a `security-participant-data` sibling skill with the PHI-equivalent implementation detail? Or is the existing `security-review` stack sufficient?
- Kybernesis deployment: if AI agents will process NDIS participant data directly, is the compliance overlay also needed at the agent-authoring level (not just code review time)? This would mean the compliance review gate fires inside the `skill-creator` workflow for Kybernesis agent definitions.
