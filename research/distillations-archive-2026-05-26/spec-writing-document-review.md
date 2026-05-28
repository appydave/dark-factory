---
distillation_id: spec-writing-document-review
stage: spec-writing
intent: "Review an existing requirements or plan document through parallel specialist lenses — adversarial, coherence, feasibility, product, scope, security, and spec-flow — surfacing findings by tier before implementation begins"
created: 2026-05-17
status: draft
source_artifacts:
  - compound-engineering:skill:ce-doc-review
  - compound-engineering:agent:ce-adversarial-document-reviewer
  - compound-engineering:agent:ce-coherence-reviewer
  - compound-engineering:agent:ce-design-lens-reviewer
  - compound-engineering:agent:ce-feasibility-reviewer
  - compound-engineering:agent:ce-product-lens-reviewer
  - compound-engineering:agent:ce-scope-guardian-reviewer
  - compound-engineering:agent:ce-security-lens-reviewer
  - compound-engineering:agent:ce-spec-flow-analyzer
  - spec-kit:command:checklist
  - appydave-plugins:skill:doc-review
winner_mechanism: compound-engineering:skill:ce-doc-review
---

# Unified Skill: spec-review (document review before implementation)

**Purpose**: Review an existing requirements or plan document through parallel specialist agents — adversarial, coherence, feasibility, product, scope, security, spec-flow — and surface tiered findings before any implementation begins.

**For Agents**: Use when David says "review this spec", "is this requirements doc solid", "pressure-test the plan", "challenge this before we build", "are there gaps in this doc". Distinct from code-review: this reviews *documents*, not code.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Before any planning or implementation begins, run the requirements or plan document through a set of specialist reviewers that challenge different axes: Does it contradict itself (coherence)? Are the technical assumptions buildable (feasibility)? Is it scoped correctly (scope guardian)? Does it address security implications (security lens)? Are user flows complete (spec-flow)? Does it solve the right product problem (product lens)? Does it survive adversarial challenge (adversarial)?

Output: tiered findings — `safe_auto` (fix silently), `gated_auto` (fix with approval), `manual` (route to David), `FYI` (informational).

## Winner's Mechanism

`compound-engineering:skill:ce-doc-review` wins because it is the only artifact in the corpus that: (1) dispatches specialist reviewers in parallel, (2) classifies findings by fix tier (safe_auto / gated_auto / manual / FYI), (3) supports both interactive and headless modes (headless is essential for autonomous pipeline runs), (4) classifies documents by content shape, not file path. CE has the most complete multi-agent doc review orchestrator in the corpus — 7 specialist agents + a 4-option interaction model. Nothing in David's stack currently matches this.

## Gap assessment: this is a REAL gap in David's stack

David has:
- `appydave-plugins:skill:doc-review` — reviews a set of documents; does not use specialist agents; no adversarial lens; no tiered findings
- `appydave-plugins:skill:doc-review-coherence`, `doc-review-completeness`, `doc-review-crossref`, `doc-review-gaps`, `doc-review-prose`, `doc-review-topology` — 6 specialist skills, but they review knowledge-base documents (brains), not requirements or plan documents; they are not orchestrated in parallel

CE's `ce-doc-review` fills a distinct gap: **requirements and plan documents reviewed before implementation begins**, with specialist agents covering axes that David's current skills don't address (adversarial challenge, feasibility, scope-guardian, spec-flow analysis).

## Contrast: spec-kit checklist vs CE doc review

| | spec-kit checklist | CE doc-review |
|--|-------------------|---------------|
| What it reviews | Requirements doc completeness/clarity | Requirements OR plan doc — all axes |
| Mechanism | Generates quality checklist ("unit tests for spec") | Dispatches parallel specialist agents |
| Findings | Pass/fail on completeness criteria | Tiered: safe_auto / gated_auto / manual / FYI |
| Interaction | Single-pass output | Interactive walk-through or headless |
| Adversarial lens | No | Yes (premises challenged, stress-tested) |
| Feasibility check | No | Yes (technical approach actually buildable?) |

Spec-kit checklist is a completeness check; CE doc-review is a full specialist review. They are complementary.

## Non-overlapping ideas folded in

- From `compound-engineering:agent:ce-adversarial-document-reviewer`: 5-technique framework — Steelman Attack, Assumption Inversion, Alternative Reality, Failure Cascade, and Devil's Advocate — applied to stress-test decisions and premises in plans. — `complexity: medium | optional: true | prerequisite: "plan contains architectural or product-strategy decisions worth stress-testing"`. Adversarial review is the most powerful but highest-friction lens; make it conditional on plan complexity.

- From `compound-engineering:agent:ce-spec-flow-analyzer`: Analyze specs for missing user flows, ambiguous requirements, and edge cases from the end-user perspective — flags flows like "what happens if the user abandons mid-flow". — `complexity: low | optional: false | prerequisite: none`. The most direct complement to spec-writer: spec-writer produces the document, spec-flow-analyzer catches the gaps before planning.

- From `compound-engineering:agent:ce-feasibility-reviewer`: Evaluate whether the technical approach is actually buildable — checks architecture coherence, dependency assumptions, performance expectations, integration complexity. — `complexity: medium | optional: false | prerequisite: "plan includes technical approach, not just requirements"`. Feasibility is the most underrepresented axis in David's current doc-review toolkit.

- From `spec-kit:command:checklist`: Requirements-quality checklist as a lightweight pre-review pass — "unit tests for the spec" — checks completeness and clarity before running heavier specialist agents. — `complexity: low | optional: true | prerequisite: "spec is new or freshly written"`. spec-kit checklist as Phase 0 of doc-review: a cheap pass that catches obvious gaps before spinning up 7 specialist agents.

- From `appydave-plugins:skill:doc-review` (as baseline): David's existing fan-out pattern: dispatch N reviewers, collect findings, route to David. The architecture is the same — CE's implementation is just more sophisticated on the reviewer side. — `complexity: low | optional: false | prerequisite: none`. The fan-out pattern is already David's; adoption of CE's mechanism is an upgrade, not a replacement.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| compound-engineering:skill:ce-doc-review | Parallel dispatch + tiered findings + interactive/headless modes + document-type classification by content shape | CE-specific `AskUserQuestion` tool pre-load ceremony; `safe_auto` auto-apply mechanism (needs Claude Code native tool integration) |
| compound-engineering:agent:ce-adversarial-document-reviewer | 5-technique adversarial framework; conditional application (not always-on) | CE-specific agent invocation model |
| compound-engineering:agent:ce-coherence-reviewer | Internal-contradiction + terminology-drift detection | CE-specific agent invocation |
| compound-engineering:agent:ce-feasibility-reviewer | Technical-buildability check; architecture-coherence signals | CE-specific agent invocation |
| compound-engineering:agent:ce-product-lens-reviewer | Senior PM lens; strategic-consequence challenges | CE-specific agent invocation |
| compound-engineering:agent:ce-scope-guardian-reviewer | Right-size check; "does every abstraction earn its keep" | CE-specific agent invocation |
| compound-engineering:agent:ce-security-lens-reviewer | Pre-implementation threat model; auth/authz/PII checks in plan | CE-specific agent invocation |
| compound-engineering:agent:ce-spec-flow-analyzer | Missing user flows; edge cases from end-user perspective | CE-specific agent invocation |
| spec-kit:command:checklist | Completeness-check as lightweight pre-review pass | spec-kit CLI integration; speckit directory structure |
| appydave-plugins:skill:doc-review | Fan-out architecture as baseline | Brain-focused review heuristics (those belong in the brains doc-review skill, not requirements review) |

## Draft SKILL.md frontmatter

```yaml
name: spec-review
description: >
  Review a requirements or plan document through parallel specialist agents before implementation begins.
  Dispatches adversarial, coherence, feasibility, product, scope, security, and spec-flow reviewers in parallel.
  Returns tiered findings (safe_auto / gated_auto / manual / FYI).
  Use when David says: "review this spec", "is this requirements doc solid", "pressure-test the plan",
  "challenge this before we build", "are there gaps in this doc". Supports headless mode for pipeline use.
argument-hint: "[path/to/spec.md or requirements.md] [mode:headless]"
allowed-tools: "Read, Write, Edit, Bash(find:*), Task"
```

## Open questions for David

1. **Naming collision**: David already has `appydave-plugins:skill:doc-review` for brain document review. Should the new requirements-focused skill be `spec-review`, `requirements-review`, or an upgraded `doc-review` that auto-routes by document type?

2. **Specialist count**: CE's full suite is 7 specialist agents. For solo projects, is the full suite too heavy? A lighter default (coherence + spec-flow + feasibility, with adversarial and security as opt-in) might be more pragmatic.

3. **Headless mode priority**: The `mode:headless` flag is load-bearing for autonomous pipeline runs (where `spec-review` would fire automatically before `plan` begins). Should headless be the default for pipeline use, with interactive reserved for David-initiated review?
