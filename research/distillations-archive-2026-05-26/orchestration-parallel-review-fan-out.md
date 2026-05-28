---
distillation_id: orchestration-parallel-review-fan-out
stage: orchestration
intent: "Fan-out a review task across N specialist subagents in parallel, deduplicate findings, synthesize into a single verdict"
created: 2026-05-16
status: draft
source_artifacts:
  - appydave-plugins:skill:delivery-review
  - appydave-plugins:skill:doc-review
  - appydave-plugins:skill:codebase-audit
  - appydave-plugins:skill:near-compaction
  - appydave-plugins:skill:conversation-triage
  - appydave-plugins:skill:five-personas
  - appydave-plugins:skill:review-blind-hunter
  - appydave-plugins:skill:review-edge-case-hunter
  - appydave-plugins:skill:review-acceptance-auditor
  - appydave-plugins:skill:review-architecture
  - appydave-plugins:skill:review-code-quality
  - appydave-plugins:skill:review-unit-tests
  - appydave-plugins:skill:prompt-injection-scanner
  - agent-skills-osmani:command:ship
  - ruflo:skill:agent-code-review-swarm
  - ruflo:skill:agent-reviewer
winner_mechanism: appydave-plugins:skill:delivery-review
---

# Unified Skill: parallel-review-fan-out

**Purpose**: The canonical David-style fan-out pattern — dispatch N specialist reviewers in parallel, each returns structured findings, orchestrator deduplicates and synthesizes into a single verdict.

**For Agents**: Use this as the **reference implementation** when David asks to build a new review orchestrator, expand an existing one, or understand the fan-out pattern. The existing skills (`delivery-review`, `doc-review`, `codebase-audit`) ARE instances of this pattern — this distillation captures the shared mechanism so new instances can be built consistently.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

## Intent

Orchestrate parallel specialist-reviewer subagents against a scope, merge structured findings using deduplication + severity triage, emit a unified verdict with PASS / CONDITIONAL PASS / FAIL.

## Winner's Mechanism

`appydave-plugins:skill:delivery-review` wins. It is the clearest, most complete implementation of the pattern in David's stack: 6 named dimensions, explicit agent prompts per dimension, normalized finding format (DVR-XX-NNN IDs), triage rules, cross-dimension pattern detection, and failure handling for dropped agents. It is production-tested in David's own workflow. The mechanism is reusable as-is — new orchestrators only need to swap the dimension set and adjust ID prefixes.

**Core invariants** (from David's stack):
1. Reviewers never write files — read-only, return structured findings only
2. Each reviewer gets a normalized finding format with dimension-specific IDs
3. Orchestrator deduplicates: keep most specific, note all dimensions that flagged
4. Verdict calculation: FAIL if any `reject`, CONDITIONAL PASS if any `patch`/`intent_gap`, PASS otherwise

## Non-overlapping ideas folded in

- From `agent-skills-osmani:command:ship`: Go/no-go as the terminal output phrasing — cleaner binary signal for delivery gates than PASS/FAIL/CONDITIONAL.
- From `appydave-plugins:skill:five-personas`: "Chairman synthesis" — when findings conflict across dimensions, a named synthesis role summarizes the debate rather than letting conflicts sit unresolved. Worth adding as an optional Step 4 in high-stakes reviews.
- From `ruflo:skill:agent-code-review-swarm`: 15-20 parallel reviewers with structured JSON findings + confidence scores per finding — confidence-scored deduplication (keep highest-confidence when two dimensions report the same issue) is a refinement over current any-duplicate-drop.
- From `appydave-plugins:skill:conversation-triage`: Mid-conversation triage is a **context window** application of fan-out (surface loose threads, open questions, decisions) — the same orchestrator pattern applies to non-code scopes.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| delivery-review | Full mechanism: 6 dims, prompts, triage, failure handling | Nothing — this is the winner |
| doc-review | 6 documentation dimensions (CH/GL/CA/TS/PU/XR) — shows the pattern is scope-agnostic | Scope-specific dimension names |
| codebase-audit | Three-lens variant (code-quality + test-quality + architecture) — lighter 3-dim version | Works, but less complete than delivery-review |
| ship (osmani) | Go/no-go terminal phrasing | Pre-launch checklist approach (less granular) |
| five-personas | Chairman synthesis for conflicted findings | Persona-as-identity framing |
| agent-code-review-swarm (ruflo) | Confidence-scored deduplication | Ruflo-specific swarm infrastructure |
| near-compaction | Context-saving as review domain (different scope: context not code) | Compaction-specific steps |
| conversation-triage | Non-code scope application | Mid-conversation trigger specifics |

## Draft SKILL.md frontmatter

```yaml
name: parallel-review-fan-out
description: >
  Reference implementation of David's fan-out review pattern — dispatch N specialist reviewers
  in parallel, each returns normalized findings, orchestrator deduplicates and synthesizes
  into a single PASS / CONDITIONAL PASS / FAIL verdict.
  Use when building a new review orchestrator, extending an existing one, or auditing
  whether an existing orchestrator follows the canonical pattern.
  Existing instances: delivery-review (6 dims), doc-review (6 dims), codebase-audit (3 dims).
  Use when: "build a new review skill", "add a dimension to delivery review",
  "fan-out review", "parallel specialists", "how does doc-review work".
```

## Canonical pattern structure (for skill body)

```
Step 1 — Determine scope (diff / path / file-list / "current changes")
Step 2 — Launch all N dimension agents in a single message (background, parallel)
         Each agent receives: scope + instruction to use normalized finding format with DIM-XX-NNN IDs
Step 3 — Triage & synthesize:
         a. Deduplicate (keep most specific, note all dims that flagged)
         b. Sort by severity (critical → high → medium → low → praise)
         c. Calculate verdict (FAIL if reject, CONDITIONAL PASS if patch/intent_gap, PASS otherwise)
         d. Cross-dimension patterns (when 2+ dims flag related issues)
Step 4 — Output report (verdict + per-dim summaries + required patches for CONDITIONAL)
Step 5 — Agent failure handling: note dropped dim, adjust verdict annotation
```

## Open questions for David

- Should this be a **meta-skill** (teaches the pattern and validates instances) or just documentation? It doesn't make sense as a live skill — it's already instantiated as `delivery-review`, `doc-review`, `codebase-audit`.
- Confidence-scored deduplication from Ruflo: worth adding to existing orchestrators, or over-engineering?
- Is there a review scope not yet covered by existing instances? (e.g., "design review", "prompt review", "skill review")
