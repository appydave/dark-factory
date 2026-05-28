---
distillation_id: knowledge-capture-adr-documentation
stage: knowledge-capture
intent: "Capture architectural decisions and rationale as durable ADRs during sessions — not docs about decisions, but decision-capture as a first-class skill"
created: 2026-05-17
status: draft
source_artifacts:
  - agent-skills-osmani:skill:documentation-and-adrs
  - everything-claude-code:skill:architecture-decision-records
  - everything-claude-code:skill:agentic-engineering
  - everything-claude-code:skill:agentic-os
  - appydave-plugins:skill:truth-trail
winner_mechanism: everything-claude-code:skill:architecture-decision-records
---

# Unified Skill: ADR & Decision Capture

## Intent

Capture architectural decisions made *during* Claude Code sessions as structured ADRs — automatically, at decision points — so the reasoning is preserved where the next session or a new engineer can find it without re-reading conversation history.

## Winner's Mechanism

ECC's `architecture-decision-records` is the winner: it captures decisions *during Claude Code sessions* as structured ADRs, which is the unique mechanism not found elsewhere. The key insight is the trigger: ADR creation is *session-contextual* (fire when a significant decision is made in-session) rather than post-hoc documentation. Osmani's `documentation-and-adrs` is the runner-up — it captures the "why not just what" principle and applies it to both ADRs and API documentation. Both share the philosophy that context is the primary artifact; the decision record is the delivery mechanism.

David has `truth-trail` (knowledge integrity rules for second-brain agents) which is adjacent but different — it's a constraint enforcement system, not a decision-capture skill. There is no ADR skill in David's current stack.

## Existing-skill nesting (upgrading existing skills)

This is a from-scratch build — no equivalent skill exists in David's stack.

## Non-overlapping ideas folded in

- From `agent-skills-osmani:documentation-and-adrs`: **"Why, not what" phrasing constraint** — the ADR records why a decision was made, what was rejected and why, and what would trigger reversal — `complexity: low | optional: false | prerequisite: none`. ECC's ADR focuses on recording the decision; Osmani adds the explicit negative-knowledge structure (what was considered and rejected), which is more valuable for future readers.
- From `agent-skills-osmani:documentation-and-adrs`: **API change trigger** — any change to a public API surface (not just architecture) should trigger a mini-ADR capturing backwards-compatibility intent — `complexity: low | optional: true | prerequisite: "public API surface exists"`. Relevant for Kybernesis (KyberBot SDK will have a public API) and SupportSignal (Convex schema is effectively a public API for the frontend).
- From `everything-claude-code:agentic-engineering`: **Eval-first ADR** — before implementing, capture the decision to use eval-first execution as an ADR with the specific quality criteria — `complexity: low | optional: true | prerequisite: "multi-agent or pipeline work"`. Documents *why* the team chose eval-first, preventing future drift.
- From `appydave-plugins:truth-trail`: **Integrity rules linkage** — after writing an ADR, check if it creates or resolves a truth-trail integrity constraint — `complexity: low | optional: true | prerequisite: "truth-trail is active for project"`. ADRs and truth-trail rules are complementary: ADRs capture the decision, truth-trail enforces the downstream constraints.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `ecc:architecture-decision-records` | Session-contextual capture trigger, structured ADR format | ECC's specific ADR file path conventions |
| `osmani:documentation-and-adrs` | Why-not-what principle, rejected-alternatives section, API-change trigger | Osmani's broader documentation scope |
| `ecc:agentic-engineering` | Eval-first ADR pattern | ECC's broader agentic engineering framework |
| `appydave:truth-trail` | Integrity-rule linkage after ADR write | Truth-trail's full constraint system |

## Draft SKILL.md frontmatter

```yaml
name: adr
description: >
  Capture architectural decisions made during Claude Code sessions as structured ADRs —
  preserves the why, the rejected alternatives, and the reversal trigger. Use when user
  says: "record this decision", "write an ADR", "document why we chose X", "capture this
  architectural decision", "why did we pick X over Y", "log this choice", "ADR for X".
  Also fires automatically when a significant architecture, API, or data-model decision
  is surfaced during a session.
argument-hint: "[title] [--api] [--agent]"
allowed-tools: Read, Write
```

## Open questions for David

1. **Auto-trigger vs manual**: ECC's ADR skill triggers automatically when a significant decision is made during a session (via session observation). David's skills are typically manual-invocation. Should `adr` be triggered by Claude's judgment mid-session, or only when David explicitly says "record this decision"?

2. **ADR storage location**: Should ADRs live in `docs/decisions/` (per-project, checked into git) or in `~/.claude/projects/.../adrs/` (Claude-local, not in repo)? For SupportSignal and Kybernesis, in-repo ADRs are better for team visibility. For personal brains, local is fine.

3. **Truth-trail integration**: David has `truth-trail` for knowledge integrity rules. Should the `adr` skill automatically add a truth-trail rule when the ADR contains a constraint (e.g., "we decided all API responses use snake_case → truth-trail: API responses must use snake_case")? This wires decision capture to constraint enforcement.
