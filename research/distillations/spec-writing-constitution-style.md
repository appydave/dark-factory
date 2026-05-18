---
distillation_id: spec-writing-constitution-style
stage: spec-writing
intent: "Establish or update the immutable principles that govern all subsequent specs, plans, and code in a project — so the same workflow produces consistent, traceable artifacts across agents and sessions"
created: 2026-05-17
status: draft
source_artifacts:
  - spec-kit:command:constitution
  - spec-kit:command:lean.constitution
  - agent-skills-osmani:skill:spec-driven-development
winner_mechanism: spec-kit:command:constitution
---

# Unified Skill: project-constitution

**Purpose**: Establish a per-project constitution — 5–9 immutable principles that constrain all downstream specs, plans, and code — so any agent (in any session) generates consistent, principled output without re-negotiating fundamentals.

**For Agents**: Use when David says "set up the project principles", "write the constitution", "establish our non-negotiables", "what are our immutable constraints", or when starting a new multi-session project where spec-first discipline is required. This is a project-setup skill, not a per-feature skill.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Write a per-project `.specify/memory/constitution.md` (or equivalent) that captures 5–9 "immutable" principles. Downstream skills read the constitution and flag any spec, plan, or task that conflicts with a MUST principle as CRITICAL. The constitution is the SDD answer to "how do we prevent LLM output from drifting across runs?"

## Winner's Mechanism

`spec-kit:command:constitution` wins because it is the only artifact in the corpus with explicit constitution-as-authority semantics: (1) versioned with semver, (2) changes propagate via Sync Impact Report to dependent templates, (3) downstream skills load it and treat MUST principles as blocking constraints. The `lean.constitution` variant strips optional steps for faster onboarding — both are the same mechanism, different ceremony levels.

Note: This sub-cluster is small (2 artifacts, both from spec-kit). The mechanism is uniquely spec-kit's. The value is in capturing the design philosophy and assessing whether it fits David's project patterns — not in finding a competing mechanism to compare against.

## Contrast: constitution (spec-kit) vs Osmani's Boundaries section

Osmani's `spec-driven-development` includes a Boundaries section ("Always do / Ask first / Never do") inside each spec. This is per-spec constraint declaration, not a per-project constitution:

| | spec-kit constitution | Osmani's Boundaries |
|--|----------------------|---------------------|
| Scope | Per-project, immutable | Per-spec, contextual |
| Lifecycle | Versioned, propagates | Written once, stays in spec |
| Authority | Blocks downstream commands | Informs the agent |
| Persistence | `.specify/memory/constitution.md` | Inside spec.md |

Both are valid; they operate at different levels. Constitution is project-level policy; Boundaries are spec-level context.

## Non-overlapping ideas folded in

- From `agent-skills-osmani:skill:spec-driven-development`: "Always / Ask first / Never" Boundaries section as an inline per-spec constitution — lightweight constitution for projects where a formal constitution file is overkill. — `complexity: low | optional: true | prerequisite: "single-session project or simple feature where per-project constitution is not needed"`. The inline Boundaries section gives the agent enough constraint information without requiring constitution file setup.

- From `spec-kit:command:lean.constitution`: Stripped-of-optional-steps variant for faster team onboarding — same core principles capture, fewer ceremony beats. — `complexity: low | optional: true | prerequisite: "new project with time pressure or solo dev who doesn't need the full constitution workflow"`. The lean variant is the right default for David's solo projects; full constitution for multi-agent or team contexts (Kybernesis).

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| spec-kit:command:constitution | Immutable-principles model; semver versioning; Sync Impact Report on MAJOR change; extension hooks pre/post; template-fill execution flow | Extension hook system specifics — Ruflo/spec-kit CLI dependency; `speckit.git.initialize` branch wiring |
| spec-kit:command:lean.constitution | Lean variant (stripped optional steps); faster onboarding path | Nothing — lean variant is folded as an optional mode |
| agent-skills-osmani:skill:spec-driven-development | Inline Boundaries section as lightweight per-spec constitution; "Always/Ask first/Never" structure | Osmani's broader 6-area spec template — covered in requirements-capture sub-cluster |

## Draft SKILL.md frontmatter

```yaml
name: project-constitution
description: >
  Establish or update the per-project immutable principles that govern all subsequent specs, plans, and code.
  Creates a versioned constitution document that downstream spec and planning tools treat as authoritative.
  Use when starting a new multi-session project, when project principles keep being re-negotiated,
  or when David says: "set up the constitution", "write our non-negotiables", "establish project principles",
  "what are our immutable constraints". Project-setup skill — run once per project, not per feature.
argument-hint: "[project-name or 'lean' for stripped-down version]"
allowed-tools: "Read, Write, Edit, Bash(mkdir:*)"
```

## Assessment: should David adopt this?

This sub-cluster is small and spec-kit-specific. The question for David:

**When does a project actually need a constitution?**

- **AppyDave apps** (AppyStack, new apps): A Boundaries section inside each spec is sufficient — projects are small, David is the only agent.
- **Kybernesis** (multi-person, multi-session, potentially multi-agent): A versioned constitution is load-bearing. Without it, three different people (David, Ian, Martin) and multiple agent sessions will drift on fundamentals like "Library-First", "Test-First NON-NEGOTIABLE", "CLI Interface".
- **SupportSignal** (client app, compliance requirements): HIPAA-adjacent constraints should be in a constitution, not repeated in every spec.

**Recommendation**: Adopt the constitution for Kybernesis and SupportSignal. Use Osmani's inline Boundaries for AppyDave solo projects.

## Open questions for David

1. **Constitution file location**: spec-kit uses `.specify/memory/constitution.md`. David's project structure uses `.claude/` for harness config. Should the constitution live at `.claude/constitution.md` or project root `CONSTITUTION.md`?

2. **CLAUDE.md vs constitution**: CLAUDE.md already captures project-level instructions in David's stack. Is a separate constitution file needed, or should the "immutable principles" section live inside CLAUDE.md?

3. **Kybernesis adoption**: Kybernesis is the one multi-person project where constitution discipline is highest value. Should this be introduced there first before generalising?
