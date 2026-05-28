---
distillation_id: workflow-architecture-plan-executor
stage: workflow-architecture
intent: "Execute a written implementation plan task-by-task with hard blocking checkpoints and no rationalization — the plan is law until a blocker forces a stop"
created: 2026-05-17
status: draft
source_artifacts:
  - superpowers:skill:executing-plans
  - everything-claude-code:command:prp-implement
  - everything-claude-code:skill:tdd-workflow
  - everything-claude-code:command:feature-dev
  - gsd:command:gsd:next
  - gsd:command:gsd:autonomous
  - gsd:command:gsd:resume-work
  - gsd:command:gsd:pause-work
winner_mechanism: superpowers:skill:executing-plans
---

# Unified Skill: plan-executor

**Purpose**: Load a written implementation plan, execute it task-by-task with blocking checkpoints, and stop immediately when a blocker surfaces — never accumulate broken state, never rationalize past a gate.

**For Agents**: Use when David hands over an implementation plan file and says "execute this", "run the plan", "implement from the plan doc", "do the tasks". Also activates when an autonomous pipeline transitions from planning to implementation phase.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Execute a plan as law. Each step is followed exactly. Verification runs after each step. If a test fails, fix it before moving on — never accumulate broken state. If a blocker surfaces (missing dependency, ambiguous instruction, repeated test failure), stop and surface it rather than guessing. The executor's job is execution fidelity, not design judgment.

## Winner's Mechanism

`superpowers:skill:executing-plans` wins for the cleanest separation of roles: reviewer vs executor. The skill opens with "review critically, identify questions BEFORE starting" — a mandatory pre-flight that catches plan gaps before they become mid-execution blockers. Its stop rules are explicit: stop on missing dependency, stop on ambiguous instruction, stop on repeated test failure. These aren't soft guidelines — they're the harness-level contract.

The companion directive ("if subagents are available, use superpowers:subagent-driven-development instead") captures an important design decision: execution is better delegated to subagents to avoid context contamination of the planning session.

`prp-implement` (ECC) complements with its **never-accumulate-broken-state** mandate and **validation loop** pattern: after every file edit, run the validation commands. It also adds package manager auto-detection at start (Node/Python/Rust/Go), which reduces setup friction.

`gsd:autonomous` adds the **full-phase autonomous sweep** — run all remaining phases without stopping, pausing only for user-required decisions. This is the "go" mode vs the step-by-step "review" mode. Both are needed.

## Non-overlapping ideas folded in

- From `prp-implement`: **Validation loop after every change** — `complexity: low | optional: false | prerequisite: none`. "Run checks after every change. Fix issues immediately." More explicit than Superpowers' per-task verification. Prevents the common failure of editing 5 files and then finding a type error that's hard to trace.
- From `prp-implement`: **Package manager auto-detection at plan load** — `complexity: low | optional: false | prerequisite: "project has package.json or equivalent"`. Prevents "how do I run tests?" friction at step 1.
- From `gsd:autonomous`: **"Go" mode** — execute all remaining steps without pausing at each one, stopping only at human-required gates — `complexity: low | optional: true | prerequisite: "plan has explicit gate markers"`. For when David wants hands-off execution after reviewing the plan.
- From `gsd:pause-work` / `gsd:resume-work`: **Context handoff file** — `complexity: low | optional: true | prerequisite: "session may be interrupted"`. Create a `.continue-here.md` before pausing. On resume, reload context from the handoff file rather than re-reading the whole plan. Preserves exact position in the plan across session boundaries.
- From `gsd:resume-work`: **State-aware resume** — `complexity: low | optional: true | prerequisite: "handoff file exists"`. Don't restart from the beginning; detect which tasks are marked `[ ]` vs `[x]` and resume from the first uncompleted task.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| superpowers:executing-plans | Pre-flight critical review, explicit stop rules, role separation from planning | Superpowers sub-skill directive (install-specific) |
| everything-claude-code:prp-implement | Validation loop pattern, never-accumulate-broken-state mandate, package manager detection | PRP branding, multi-harness phase structure |
| everything-claude-code:tdd-workflow | Git checkpoint convention after each TDD stage (RED/GREEN/REFACTOR) | Full TDD workflow (covered in code-implementation cluster) |
| gsd:autonomous | "Go" mode for hands-off execution | GSD workspace format |
| gsd:pause-work + resume-work | Context handoff file + state-aware resume | GSD-specific STATE.md format |
| gsd:next | State detection (which step am I on?) | GSD-specific file conventions |

## Draft SKILL.md frontmatter

```yaml
name: plan-executor
description: >
  Execute a written implementation plan task-by-task with blocking checkpoints.
  Validates after every change. Stops at blockers rather than guessing through them.
  Never accumulates broken state. Supports "go" mode (hands-off) and pause/resume.
  Use when: "execute this plan", "run the plan", "implement from the plan doc",
  "do the tasks", "go", or transitioning from plan phase to implementation phase.
argument-hint: "[path/to/plan.md] [--go (hands-off mode)]"
allowed-tools: "Read, Edit, Write, Bash, TodoWrite, TodoRead"
```

## Open questions for David

1. **Subagent delegation**: Superpowers recommends using `subagent-driven-development` instead of `executing-plans` when subagents are available. Should `plan-executor` auto-delegate to subagents when agent teams env var is set, or always run in-process?

2. **Validation strategy**: `prp-implement`'s validation loop (run checks after every file edit) is more aggressive than Superpowers' per-task verification (run at the end of each task). Which grain is right for David's typical plan step size?

3. **Handoff file format**: Should the `.continue-here.md` be a free-form context dump (GSD style) or a structured YAML with `current_task`, `completed_tasks`, `context_notes`? Structured is more machine-readable for future resume; free-form is faster to write.
