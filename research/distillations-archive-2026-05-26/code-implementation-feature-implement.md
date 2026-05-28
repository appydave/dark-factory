---
distillation_id: code-implementation-feature-implement
stage: code-implementation
intent: "Execute a feature or change request from plan or bare prompt, with complexity triage, subagent dispatch for multi-task work, and incremental commits"
created: 2026-05-17
status: draft
source_artifacts:
  - compound-engineering:skill:ce-work
  - compound-engineering:skill:lfg
  - gsd:command:execute-phase
  - gsd:command:fast
  - gsd:agent:gsd-executor
  - spec-kit:command:implement
  - spec-kit:command:lean.implement
  - superpowers:skill:executing-plans
  - superpowers:skill:subagent-driven-development
  - bmad-method:skill:bmad-quick-dev
  - agent-skills-osmani:skill:incremental-implementation
winner_mechanism: compound-engineering:skill:ce-work
---

# Unified Skill: Feature Implement

## Intent

Execute a feature or change from a plan document or bare prompt, routing by complexity (trivial → inline; small/medium → task list; large → warn and plan first), dispatching subagents for multi-task plans, and committing incrementally at logical unit boundaries.

## Winner's Mechanism

CE's `ce-work` is the winner because it is the most complete, production-tested feature-execution skill in the corpus with the clearest complexity triage:

1. **Phase 0 complexity triage** — Trivial (1-2 files, no behavioral change) → implement directly; Small/Medium (under 10 files) → task list; Large (cross-cutting, 10+ files, auth/payments/migrations) → warn and recommend planning first. No other skill has an explicit routing gate at the front.

2. **Parallel Safety Check** — before dispatching subagents in parallel, build a file-to-unit mapping and check for intersection. If overlap exists without worktree isolation, downgrade to serial dispatch. This prevents the git-index-contention and test-interference failures that plague naive parallel implementation.

3. **Worktree isolation protocol** — subagent isolation via `isolation: "worktree"` + post-batch merge flow with conflict-abort-and-re-dispatch (not silent conflict resolution). This is the correct mechanism; none of the other skills get this right.

4. **Plan as decision artifact, not execution script** — "Do not edit the plan body during execution. The plan is a decision artifact; progress lives in git commits." This is a key insight: plans should not be mutated by execution. Prevents the drift where agents mark plans done while implementation lags.

5. **Scope Boundaries section awareness** — explicitly reads `Deferred to Implementation` and `Scope Boundaries` sections before starting. Prevents scope creep during execution.

6. **Simplify as you go** — after every 2-3 related implementation units, review for consolidation opportunities. Prevents accumulated complexity from subagents with isolated context.

Superpowers' `subagent-driven-development` has the best two-stage review loop (spec compliance → code quality) but lacks CE's complexity triage and worktree protocol. GSD's `execute-phase` has the strongest wave-based parallelization model but requires GSD's plan format. Both contribute folded ideas.

## Existing-skill nesting

David has `dev` as a direct invocation point in his skills. `baku` and `nano-banana` are not general-purpose implementation skills. The primary collision is with `bmad-story-lifecycle` → `bmad-dev-story` for sprint work.

- **Existing mechanism**: `bmad-story-lifecycle` → `bmad-dev-story` for BMAD sprint stories. Story-file-scoped, sprint-integrated, runs inside Amelia persona, handles AC validation and sprint-status updates.
- **New mechanism's grain**: per-feature, per-PR, or per-session. Invoked for work that is NOT a BMAD sprint story: hotfixes, standalone features, client requests, experiments, one-off improvements.
- **Existing mechanism's grain**: per-story, inside sprint, coupled to story file and sprint-status.yaml.
- **Nesting rule**: `feature-implement` fires for any feature work where no BMAD story file exists. When David is in a BMAD sprint, `bmad-story-lifecycle` owns execution. They do not overlap — routing is by presence or absence of a story file.

## Non-overlapping ideas folded in

- From `superpowers:skill:subagent-driven-development`: **Two-stage review per task** — spec compliance review first (does the implementation match the spec?), then code quality review (is it well-built?). The ordering is critical: do not start quality review before spec compliance is confirmed. — `complexity: medium | optional: true | prerequisite: "plan has structured units with spec requirements"`. Prevents over/under-building and catches quality issues before they compound across tasks.

- From `superpowers:skill:subagent-driven-development`: **Four implementer statuses** — DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, BLOCKED. Each has an explicit handling protocol; BLOCKED is the only one that escalates to human. — `complexity: low | optional: false | prerequisite: "subagent dispatch mode"`. Prevents the "ignore concerns and mark done" failure mode.

- From `superpowers:skill:subagent-driven-development`: **Model selection by task complexity** — cheap/fast model for mechanical isolated tasks (1-2 files, clear spec); standard model for multi-file integration; most capable for architecture and review. — `complexity: low | optional: true | prerequisite: "multiple model tiers available"`. Cost optimization that doesn't compromise quality.

- From `gsd:command:execute-phase`: **Dependency-ordered wave batching** — build a dependency graph from tasks, group into waves (all tasks with no unmet deps = wave 1, etc.), dispatch wave by wave. Catches the case where naive parallelism dispatches tasks whose prerequisites aren't complete. — `complexity: medium | optional: true | prerequisite: "plan has explicit task dependencies"`. The right structure for multi-wave feature work.

- From `gsd:command:fast`: **Trivial task fast path** — for tasks too small to justify planning overhead (typo, config change, small refactor), execute inline with no subagents, no task list. Explicit "this is too small for the full workflow" gate. — `complexity: low | optional: false | prerequisite: none`. Prevents the overhead-to-value inversion for trivial work.

- From `agent-skills-osmani:skill:incremental-implementation`: **Consistency principle** — match naming, structure, and patterns from the existing codebase before introducing anything new. Read the `Patterns to follow` field for each unit before implementing. — `complexity: low | optional: false | prerequisite: none`. The most common source of "technically works but is wrong for this codebase" implementations.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `compound-engineering:ce-work` | Phase 0 complexity triage, Parallel Safety Check, worktree isolation protocol, plan-as-decision-artifact principle, Scope Boundaries awareness, simplify-as-you-go, System-Wide Test Check | Figma design sync (not David's primary workflow), Codex/Pi alternative tool names |
| `superpowers:subagent-driven-development` | Two-stage review per task, four implementer statuses, model selection by complexity | Single-session-only constraint (CE's worktree approach is more general), the specific prompt template files |
| `superpowers:executing-plans` | Parallel session alternative (for when cross-session handoff is desired) | Most content — ce-work is the richer mechanism |
| `gsd:execute-phase` | Wave-based dependency-ordered batching | GSD-specific plan format requirements, GSD agent orchestration protocol |
| `gsd:command:fast` | Trivial task fast path | GSD pipeline integration |
| `spec-kit:implement` | Sequential task processing from tasks.md | Nothing unique over ce-work |
| `bmad-method:bmad-quick-dev` | Scope standard (900-1600 tokens per spec unit), single-goal test | BMAD config/customization infrastructure (not needed here) |
| `agent-skills-osmani:incremental-implementation` | Consistency principle, patterns-to-follow field | Nothing unique over ce-work |

## Draft SKILL.md frontmatter

```yaml
name: feature-implement
description: "Execute a feature, change request, or plan document. Use when the user wants to implement a feature, fix, refactor, or any code change outside a BMAD sprint story. Triggers on: 'implement this', 'build X', 'execute this plan', 'make this change', or when handed a plan document to execute."
argument-hint: "[plan file path, or description of what to build]"
allowed-tools: "Bash(git:*), Bash(gh:*), Read, Edit, Write, Agent"
```

## Open questions for David

1. **Boundary with bmad-quick-dev**: `bmad-quick-dev` is in the cluster with `uniqueness: uncommon`. Its step-file architecture (just-in-time loading, sequential enforcement) is more heavyweight than CE's inline phases. Should `feature-implement` reference `bmad-quick-dev`'s step-file pattern for larger features, or keep everything inline as CE does?

2. **Two-stage review integration**: Superpowers' spec-compliance + code-quality two-stage review is excellent but adds token cost. Should it be opt-in (invoked only when the user asks for high-confidence execution) or the default for any plan-driven work?

3. **LFG relationship**: CE's `lfg` is the end-to-end autonomous pipeline (plan → work → review → test → commit → push → PR → CI watch → CI fix). Should `feature-implement` be a sub-skill of `lfg`, or is `lfg` a separate invocation that calls `feature-implement` internally? The topology matters for how David wires the skills.
