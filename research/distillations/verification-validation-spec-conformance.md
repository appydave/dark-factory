---
distillation_id: verification-validation-spec-conformance
stage: verification
intent: "Cross-artifact consistency gate — does the implementation match the spec before execution begins?"
created: 2026-05-17
status: draft
source_artifacts:
  - spec-kit:command:analyze
  - spec-kit:command:checklist
  - bmad-method:skill:bmad-validate-prd
  - bmad-method:skill:bmad-check-implementation-readiness
  - gsd:agent:gsd-plan-checker
  - compound-engineering:agent:ce-spec-flow-analyzer
  - appydave-plugins:skill:review-acceptance-auditor
  - compound-knowledge:agent:strategic-alignment-reviewer
  - bmad-method:skill:bmad-checkpoint-preview
winner_mechanism: gsd:agent:gsd-plan-checker
---

# Unified Skill: verification-validation-spec-conformance

**Purpose**: Verify that what was planned or built actually conforms to the spec, requirements, and user decisions — before execution burns context (plan-check) or before a PR is raised (acceptance audit). Two sub-intents: pre-execution plan conformance and post-implementation AC coverage.

**For Agents**: Use when David asks "does this plan cover all the requirements?", "does the implementation meet the spec?", "check the ACs", "verify acceptance criteria", "does this match what we agreed?". The plan-check variant runs before execution; the acceptance-audit variant runs post-implementation against a diff or PR.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Catch the gap between what was agreed (spec/requirements/decisions) and what was planned or built — when it is cheapest to fix. Two application points:

1. **Pre-execution** — plans look complete but silently miss requirements, contradict user decisions, or reduce scope without acknowledgment
2. **Post-implementation** — code exists but doesn't satisfy the stated acceptance criteria

## Winner's Mechanism

`gsd:agent:gsd-plan-checker` wins for the unified mechanism. It is the most complete spec-conformance checker in the corpus with 11 named verification dimensions. Key unique contributions:

1. **Goal-backward framing** — starts from what must be TRUE for the goal to be achieved, not from a task checklist. "Plan completeness ≠ goal achievement" is the core principle.
2. **Scope reduction detection** (Dimension 7b) — catches the most insidious failure mode: plans that reference a user decision (D-26) but deliver only a shadow of it (static labels instead of calculated costs). This pattern is documented from a real incident.
3. **Nyquist compliance** (Dimension 8) — ensures verification commands are present in plans and have bounded latency (no full E2E suite per task, no watch mode, no > 30 second delays). This prevents plans that "verify" via unbounded test runs.
4. **Cross-plan data contracts** (Dimension 9) — when two plans share a data pipeline, checks that one plan's transformation doesn't conflict with another's assumptions (strip/sanitize vs. parse-original).
5. **Context compliance** (Dimension 7) — user locked decisions must be implemented; deferred ideas must not appear.

The `gsd-plan-checker` is production-tested as part of GSD's `/gsd-plan-phase` loop and is the only artifact in the cluster with explicit scope-reduction detection as a first-class blocking issue.

## Existing-skill nesting

David's stack has `review-acceptance-auditor` (AA dimension in `delivery-review`). This distillation covers a broader and earlier-in-lifecycle concern:

- **Existing mechanism** (`review-acceptance-auditor`): Maps each AC in the spec to implementation evidence (file paths, line numbers). Runs post-implementation, per-PR. Produces pass/conditional-pass/fail verdict.
- **New mechanism's grain**: Pre-execution (plan → spec conformance check) + post-implementation (AC mapping). The plan-check variant fires BEFORE the implementation runs; the acceptance-audit variant is the same grain as the existing skill.
- **Existing mechanism's grain**: Per-PR, post-implementation.
- **Nesting rule**: The plan-check variant fires before `/gsd-execute-phase` equivalent. The acceptance-audit variant is an upgrade to the existing `review-acceptance-auditor` — add scope-reduction detection and goal-backward framing as additional dimensions. They compose: plan-check prevents wasted execution on bad plans; acceptance-auditor catches what slipped through execution. The existing AA skill remains the PR-level gate; the plan-check is the pre-execution gate.

## Non-overlapping ideas folded in

- From `spec-kit:command:analyze`: **Cross-artifact consistency gate** — spec.md + plan.md + tasks.md must be internally consistent before implementation runs. The `analyze` command is strictly read-only and must pass before `implement` runs. The "constitution authority" concept (non-negotiable principles that override all other analysis) is the spec-kit's most distinct contribution. — `complexity: low | optional: false | prerequisite: "spec + plan artifacts exist in structured form"`

- From `ce-spec-flow-analyzer`: **User-flow gap identification before implementation** — walk the spec as a user, map entry points → decision points → happy path → terminal states, then find unhappy paths, state transitions, and permission boundaries not specified. The severity ranking (Critical/Important/Minor) with specific question formulation ("What breaks if left unspecified") is more actionable than generic gap-finding. — `complexity: medium | optional: false | prerequisite: "spec describes user-facing flows"`

- From `bmad-method:skill:bmad-validate-prd`: **PRD completeness gate** — checks that a PRD has sufficient detail for implementation to begin. Distinct from the plan-checker: this fires on the requirements artifact itself, not on the derived plan. — `complexity: low | optional: true | prerequisite: "BMAD or story-based workflow"`

- From `compound-knowledge:agent:strategic-alignment-reviewer`: **Strategic alignment check** — confirms that the plan/implementation aligns with declared strategic direction, not just technical spec. Prevents technically-correct implementations that contradict product strategy. — `complexity: medium | optional: true | prerequisite: "strategic context document exists"`

- From `bmad-method:skill:bmad-checkpoint-preview`: **Mid-stream checkpoint** — fires at phase boundaries to check that implementation is still tracking the spec, not drifted during execution. This is the "verify during" variant; plan-checker is "verify before"; acceptance-auditor is "verify after". — `complexity: low | optional: true | prerequisite: "multi-phase implementation"`

## The double sub-cluster: pre-execution vs post-implementation

These are two faces of the same concern: spec conformance. The distinction matters for when they fire:

| Variant | When | Artifact checked | Winner |
|---------|------|-----------------|--------|
| Plan-conformance | Before execution | Plans + ROADMAP | gsd-plan-checker |
| Acceptance-audit | After implementation | Code + diff | review-acceptance-auditor (existing) |
| Flow-gap analysis | Before implementation | Spec/PRD | ce-spec-flow-analyzer |

The unified skill should expose all three as invocation modes, not three separate skills — the shared vocabulary (spec, requirements, acceptance criteria) is the clustering signal.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| gsd-plan-checker | 11 verification dimensions, goal-backward framing, scope reduction detection, Nyquist compliance, cross-plan data contracts, CONTEXT.md compliance, structured issue format | GSD tooling (gsd-tools.cjs), GSD-specific XML task structure |
| spec-kit:analyze | Cross-artifact consistency gate, constitution authority concept, strictly read-only mode, hook integration pattern | spec-kit multi-harness compile machinery |
| ce-spec-flow-analyzer | User-flow gap identification, severity ranking, question formulation pattern, default assumption per gap | CE-specific codebase context loading |
| bmad:bmad-validate-prd | PRD completeness gate concept | BMAD-specific workflow integration |
| review-acceptance-auditor (appydave) | AC-to-implementation mapping, scope creep detection, per-dimension verdict | Already in David's stack — upgrade not replace |
| strategic-alignment-reviewer (kw) | Strategic alignment check concept | Every Inc. internal product references |
| bmad-checkpoint-preview | Mid-stream checkpoint pattern | BMAD execution context |

## Draft SKILL.md frontmatter

```yaml
name: spec-conformance
description: >
  Verify that plans or implementations actually conform to the spec, requirements, and user decisions.
  Two modes: (1) pre-execution plan-check — plans cover all requirements, no scope reduction, user decisions implemented;
  (2) post-implementation acceptance-audit — every AC is met by the implementation with evidence.
  Use when: "does this plan cover the requirements?", "check the ACs", "does this meet the spec?",
  "verify acceptance criteria", "did we implement what was agreed?".
argument-hint: "[plan-check | acceptance-audit | flow-gap] [spec-file or 'current changes']"
allowed-tools: Read, Bash(git diff:*), Bash(git diff --cached:*), Bash(grep:*), Bash(find:*)
```

## Open questions for David

- Should the **plan-conformance** variant be integrated into the GSD-style `/gsd-plan-phase` orchestrator equivalent in David's stack, or remain a standalone invocable skill? Integration makes it automatic; standalone keeps it opt-in.
- The scope-reduction detection in `gsd-plan-checker` is based on language patterns ("v1", "simplified", "static for now"). Should David adopt this vocabulary as a banned-phrase list in his CLAUDE.md, making it a hook-enforced constraint rather than a review?
- Is there overlap with `review-acceptance-auditor`? Recommended answer: the existing AA skill is the post-implementation AC mapping (keep it); the new unified skill adds the pre-execution plan-check variant and flow-gap analysis as new modes. David reviews.
