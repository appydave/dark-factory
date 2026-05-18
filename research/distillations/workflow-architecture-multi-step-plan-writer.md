---
distillation_id: workflow-architecture-multi-step-plan-writer
stage: workflow-architecture
intent: "Write a complete, zero-placeholder implementation plan before touching code — one that a fresh agent can execute without asking questions"
created: 2026-05-17
status: draft
source_artifacts:
  - superpowers:skill:writing-plans
  - everything-claude-code:command:prp-plan
  - everything-claude-code:command:prp-prd
  - appydave-plugins:skill:agent-orchestrator
  - appydave-plugins:skill:workflow-orchestrator
  - bmad-method:skill:bmad-create-architecture
  - poem:agent:alex
winner_mechanism: superpowers:skill:writing-plans
---

# Unified Skill: multi-step-plan-writer

**Purpose**: Design-time authoring skill that produces a zero-placeholder, TDD-structured, bite-sized implementation plan before execution begins. The plan is a self-contained artifact — a fresh agent (or a different session) can execute it without asking further questions.

**For Agents**: Use when David says "write a plan", "draft the implementation steps", "plan before coding", "spec this out", "what's the task breakdown", or hands over a PRD/RFC and says "plan this". Output is a markdown file in `docs/superpowers/plans/` (or project-specified location).

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Translate a spec or feature description into an executable step-by-step plan — one action per step, with exact file paths, test-first structure, and commit checkpoints. The goal: after writing the plan, the author's context is no longer needed. A plan is done when a fresh agent can execute it cold.

## Winner's Mechanism

`superpowers:skill:writing-plans` wins for its insistence on zero-placeholder completeness and the principle that "if you would need to search the codebase during implementation, capture that knowledge NOW in the plan." Its bite-sized task granularity (2-5 minutes per step, write failing test → run it fails → implement → run passes → commit) is the clearest articulation of how a plan becomes executable vs aspirational.

Key mechanism: **scope check before planning** — if the spec covers multiple independent subsystems, break into sub-plans first. Each sub-plan produces working, testable software on its own. This prevents the "big-bang plan" failure mode.

`prp-plan` (ECC) contributes the **complexity assessment gate** (Small/Medium/Large/XL with line-count heuristics) that determines whether to split before writing. It also enforces a golden rule complementary to Superpowers: "everything you'd search for during implementation gets captured in the plan."

## Existing-skill nesting (ONLY when upgrading an existing skill)

David has `agent-orchestrator` (design-advisor for multi-agent workflows) and `workflow-orchestrator` (emit structured workflow from description). These are different grain:

- **Existing mechanism** (`agent-orchestrator` + `workflow-orchestrator`): per-workflow design session — topology, agent roles, step sequence. Output is a coordination plan or YAML.
- **New mechanism's grain** (`multi-step-plan-writer`): per-feature / per-task implementation plan — which files change, what tests to write, how to commit. Output is a markdown task list for a single execution unit.
- **Nesting rule**: `agent-orchestrator` fires when designing *who does what*; `multi-step-plan-writer` fires when designing *what steps to take*. They compose sequentially: first decide the coordination structure, then write the implementation plan for each unit of work that agents will execute.

## Non-overlapping ideas folded in

- From `prp-plan`: **Complexity assessment gate** (Small/Medium/Large/XL) before writing — `complexity: low | optional: false | prerequisite: none`. Prevents over-planning simple tasks and under-planning complex ones. Saves time when the right answer is "this is 2 files, skip the formal plan."
- From `prp-prd`: **Ambiguity gate with user story format** — `complexity: medium | optional: true | prerequisite: "spec is product-level (new feature vs bug fix)"`. If requirements are fuzzy, gather them in product-manager mode before writing the technical plan. Prevents plans that solve the wrong problem.
- From `prp-plan`: **PRD-parsing capability** — `complexity: low | optional: true | prerequisite: "a .prd.md or Implementation Phases document exists"`. Auto-extract the next pending phase and use it as the plan scope, rather than requiring the user to specify. Reduces friction for BMAD-workflow projects (SupportSignal).
- From `poem:agent:alex`: **I/O contract validation between steps** — `complexity: medium | optional: true | prerequisite: "workflow has multiple agents or handoff points"`. For each step, specify what it receives and what it emits. Alex's `validate-io-compatibility` discipline. Catches schema mismatches before execution, not during.
- From `bmad-create-architecture`: **Architecture decision brief before task decomposition** — `complexity: medium | optional: true | prerequisite: "plan is Large or XL"`. For large plans, write a 2-3 sentence architecture summary before the task list. Prevents tactical steps that contradict the design intent.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| superpowers:writing-plans | Zero-placeholder completeness principle, scope check, bite-sized TDD task structure, plan header with sub-skill notice, save location convention | Specific file paths (customize to project) |
| everything-claude-code:prp-plan | Complexity assessment gate, PRD-parsing capability, golden rule phrasing ("capture what you'd search for") | Multi-harness CLI flags, Wirasm PRP branding |
| everything-claude-code:prp-prd | Ambiguity gate, user story format, problem-first questioning | Full PRD generation workflow (separate concern) |
| poem:agent:alex | I/O contract discipline, validate-io-compatibility principle | POEM-specific YAML workflow format |
| bmad-create-architecture | Architecture decision brief before task decomposition | BMAD-specific personas and ceremony |
| agent-orchestrator + workflow-orchestrator | Nesting context (these are coordination-layer, not implementation-plan layer) | Coordination logic (separate skill) |

## Draft SKILL.md frontmatter

```yaml
name: multi-step-plan-writer
description: >
  Write a zero-placeholder, TDD-structured implementation plan before touching code.
  Each step is 2-5 minutes, test-first, with exact file paths and commit checkpoints.
  A done plan is executable cold by a fresh agent without asking questions.
  Use when: "write a plan", "plan before coding", "implementation steps", "task breakdown",
  "spec this out", "what do I build first", or handed a PRD/RFC to plan.
argument-hint: "[spec-or-feature-description | path/to/prd.md]"
allowed-tools: "Read, Write, Bash(cat:*), Bash(find:*)"
```

## Open questions for David

1. **Plan location convention**: `docs/superpowers/plans/YYYY-MM-DD-<feature>.md` is Superpowers' default. For SupportSignal (BMAD project) it might be `_bmad-output/implementation-artifacts/`. Should the skill auto-detect the project type and pick the location, or always ask?

2. **Sub-plan split trigger**: The scope check (split if multiple independent subsystems) is manual in Superpowers. Should the skill auto-suggest splitting when complexity is XL, or only when the user explicitly says "this covers N subsystems"?

3. **I/O contract discipline**: Alex's IO validation is designed for POEM OS YAML workflows. Should `multi-step-plan-writer` adopt a lightweight version (just "output of step N = input of step N+1") for any multi-agent plan, or scope it only to POEM OS plans?
