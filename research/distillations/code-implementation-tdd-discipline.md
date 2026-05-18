---
distillation_id: code-implementation-tdd-discipline
stage: code-implementation
intent: "Enforce Red-Green-Refactor discipline with anti-rationalization immune system — no production code without a failing test first"
created: 2026-05-17
status: draft
source_artifacts:
  - superpowers:skill:test-driven-development
  - bmad-method:skill:bmad-dev-story
  - everything-claude-code:skill:tdd-workflow
  - everything-claude-code:skill:laravel-tdd
  - everything-claude-code:skill:springboot-tdd
  - compound-engineering:skill:ce-work
winner_mechanism: superpowers:skill:test-driven-development
---

# Unified Skill: TDD Discipline

**Purpose**: One-line description of what this unified skill does.

## Intent

Enforce the Red-Green-Refactor cycle with a hard iron law ("no production code without a failing test first") and an explicit anti-rationalization table that blocks common skipping excuses before they take hold.

## Winner's Mechanism

Superpowers' `test-driven-development` is the winner because:

1. **Iron Law framing** — the absolute prohibition ("Delete means delete") is stronger than any checklist. It eliminates the ambiguity that allows rationalization to creep in.
2. **Anti-rationalization table** — 11 named excuses with direct rebuttals. Osmani and BMAD both enforce TDD, but neither provides named-excuse counters. This is the mechanism that makes the skill sticky under pressure.
3. **Verify-RED as mandatory gate** — requiring the test to fail *for the expected reason* (not just fail) before writing implementation code. This catches false-green tests before they breed false confidence.
4. **Red-flag checklist at completion** — the verification checklist prevents premature "done" declarations. BMAD's `bmad-dev-story` has a similar gate but it's embedded in a 10-step workflow; Superpowers makes it a standalone moment.

CE's `ce-work` folds TDD in as an execution note per unit rather than a first-class discipline — good for pragmatic work but weaker enforcement. BMAD's `bmad-dev-story` Step 5 implements the same RED-GREEN-REFACTOR cycle but inside a story-file orchestration workflow David controls via `bmad-story-lifecycle`, so the TDD mechanics are already available there.

## Existing-skill nesting

David already uses `bmad-dev-story` (via `bmad-story-lifecycle`) for BMAD sprint work. The TDD cycle is wired into Step 5 there. This unified skill is NOT a replacement for that.

- **Existing mechanism**: `bmad-story-lifecycle` → `bmad-dev-story` Step 5 runs RED-GREEN-REFACTOR per story task. Story-file-scoped, sprint-integrated, runs inside Amelia persona.
- **New mechanism's grain**: per-task, per-session, invokable outside BMAD sprint context (one-off features, hotfixes, experiments, any non-story work).
- **Existing mechanism's grain**: per-story, inside sprint workflow, coupled to story file state machine.
- **Nesting rule**: `tdd-discipline` fires for any implementation work that is NOT a BMAD sprint story. When David is in a sprint, `bmad-story-lifecycle` owns the TDD loop. When working on a hotfix, standalone feature, or proof-of-concept, `tdd-discipline` is the invocation. They do not overlap — they cover different grains of work.

## Non-overlapping ideas folded in

- From `superpowers:test-driven-development`: **Verify-fail-for-the-right-reason** gate — confirm the test fails because the feature is missing, not due to a typo or unrelated error. — `complexity: low | optional: false | prerequisite: none`. The discipline is worthless without this step; passing tests before implementation invalidates the whole cycle.

- From `bmad-method:skill:bmad-dev-story`: **Completion-gate formalism** — "NEVER mark a task complete unless ALL conditions are met — NO LYING OR CHEATING." The explicit anti-cheating framing prevents the "I'll mark it done and fix tests later" failure mode. — `complexity: low | optional: false | prerequisite: none`. Directly prevents the most common TDD-in-practice failure.

- From `compound-engineering:skill:ce-work`: **Test Scenario Completeness check** — before writing tests, verify the plan's test scenarios cover happy path, edge cases, error/failure paths, and integration. Supplement gaps before coding. — `complexity: low | optional: true | prerequisite: "plan document exists with test scenarios"`. Prevents under-specified test suites when a plan is present.

- From `compound-engineering:skill:ce-work`: **System-Wide Test Check** — before marking any task done, trace callbacks, middleware, observers, and event handlers two levels out from the change. — `complexity: medium | optional: true | prerequisite: "framework with callbacks or middleware (Rails, Next.js middleware, etc.)"`. Catches the hidden-dependency failure mode that unit tests alone miss.

- From `everything-claude-code:skill:tdd-workflow`: **Stack-agnostic test runner invocation patterns** — explicit per-language test run commands baked in rather than requiring the agent to guess. — `complexity: low | optional: true | prerequisite: "known project stack"`. Removes friction for the mandatory Verify-RED and Verify-GREEN steps.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `superpowers:test-driven-development` | Iron Law, Verify-RED gate, anti-rationalization table, completion checklist, Red Flags list | Graphviz cycle diagram (adds noise in text skill) |
| `bmad-method:bmad-dev-story` | Anti-cheating task completion gate, review-continuation detection | Story-file orchestration, sprint-status tracking, Amelia persona (already in bmad-story-lifecycle) |
| `compound-engineering:ce-work` | Test Scenario Completeness, System-Wide Test Check, test-first execution note pattern | Full ce-work orchestration pipeline (not needed here) |
| `everything-claude-code:tdd-workflow` | Multi-language test runner patterns | Framework-specific TDD scaffolding (Laravel, SpringBoot — not David's stack) |

## Draft SKILL.md frontmatter

```yaml
name: tdd-discipline
description: "Enforce Red-Green-Refactor discipline for any implementation task outside a BMAD sprint. Use when implementing a feature, hotfix, refactor, or experiment where no story file exists. Triggers on: 'implement this', 'build this', 'add X to the codebase', 'write the code for', or any request to produce new production code."
argument-hint: "[task description or file path to spec]"
allowed-tools: "Bash, Read, Edit, Write"
```

## Open questions for David

1. **Invocation boundary**: Should `tdd-discipline` explicitly detect the presence of a BMAD story file and hand off to `bmad-story-lifecycle` when one is found, or leave that routing to the human? The risk without detection: double-TDD-loop with conflicting state.

2. **Refactor phase scope**: Superpowers says "remove duplication, improve names, extract helpers — keep tests green, don't add behavior." CE's `ce-work` adds "simplify as you go" at phase boundaries. Should the refactor phase be per-cycle (Superpowers) or per-cluster-of-tasks (CE)? CE's approach is better for multi-task sessions; Superpowers' is safer for one-off work.
