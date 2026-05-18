---
distillation_id: spec-writing-requirements-capture
stage: spec-writing
intent: "Transform a vague request or brainstorm into a structured, decision-useful requirements document"
created: 2026-05-17
status: draft
source_artifacts:
  - appydave-plugins:skill:spec-writer
  - agent-skills-osmani:skill:spec-driven-development
  - compound-engineering:skill:ce-brainstorm
  - spec-kit:command:specify
  - gsd:command:gsd:new-project
  - bmad-method:skill:bmad-agent-analyst
  - bmad-method:skill:bmad-agent-pm
  - everything-claude-code:command:plan-prd
winner_mechanism: appydave-plugins:skill:spec-writer
---

# Unified Skill: spec-writer (requirements capture)

**Purpose**: Transform a vague request, brainstorm, or voice dump into a structured requirements document — covering purpose, users, scope, functional requirements, business rules, gaps, and open questions.

**For Agents**: Use when David says "spec this out", "write a spec", "turn this brainstorm into requirements", "BA this", "product spec", "write the PRD", or any variation of formalising an idea before planning.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Formalise a messy input into a requirements document that another person or agent can use for scoping, design, and planning — without having to re-ask the originator.

## Winner's Mechanism

`appydave-plugins:skill:spec-writer` wins because it is the most complete and explicitly David-shaped mechanism in the corpus. It covers the full extraction surface (21-section output, covering framing → users → scope → functional → data → business rules → NFRs → gaps → open questions), specifies the exact writing style ("not a marketing document, not meeting notes, not a brainstorm restatement"), includes reverse-engineering rules ("if solution-heavy, infer the underlying business need"), and closes with three hard deliverables: key assumptions made, what appears missing, and the 5 most important decisions the product owner still needs to make. It is already in David's stack — this sub-cluster is about making it provably the best version of itself.

## Existing-skill nesting

`spec-writer` already exists as `appydave-plugins:skill:spec-writer`. This distillation identifies two non-overlapping ideas to fold in (from CE and Osmani) and one gap to close (structured elicitation before transformation, currently absent).

- **Existing mechanism**: takes a pasted brainstorm, immediately transforms it into a structured document using 21 predefined sections, then offers to save.
- **New mechanism's grain** (from CE): per-session gate — if the brainstorm is thin or ambiguous, optionally run a focused one-question-at-a-time elicitation pass before transformation rather than inferring everything silently.
- **Existing mechanism's grain**: per-activation transformation pass.
- **Nesting rule**: elicitation fires only when the brainstorm is below a legibility threshold (e.g., fewer than 3 recoverable entities or no discernible user). The transformation pass fires regardless. Both compose inside the same activation.

Skip this section for from-scratch builds.

## Non-overlapping ideas folded in

- From `agent-skills-osmani:skill:spec-driven-development`: Surface assumptions explicitly before writing content — present an ASSUMPTIONS block ("Correct me now or I'll proceed with these") before the spec body. — `complexity: low | optional: false | prerequisite: none`. Prevents silent wrong-assumption propagation into the document; Osmani's spec is the only mechanism in the corpus that makes assumptions blocking, not footnoted.

- From `compound-engineering:skill:ce-brainstorm`: Scope-decomposition gate — if the request describes multiple independent subsystems, flag this before speccing and help the user decide the decomposition before writing the first spec. — `complexity: low | optional: true | prerequisite: "request spans >2 independent subsystems"`. Keeps a single spec bounded; without this, multi-subsystem requests produce specs that are too wide to scope.

- From `spec-kit:command:specify`: Numbered artifact IDs (R1, A1, F1, AE1 for requirement, actor, flow, acceptance-example) in the output — makes individual items addressable in downstream steps and in review feedback. — `complexity: medium | optional: true | prerequisite: "spec will be reviewed by an agent or fed to a planning tool"`. spec-kit is the only corpus member that assigns stable IDs; without them, document references in plan.md and tasks.md are positional and break on edit.

- From `everything-claude-code:command:plan-prd` (anti-fluff rule): When a section's information is missing, write `TBD — needs validation via {method}` rather than inventing plausible-sounding requirements. — `complexity: low | optional: false | prerequisite: none`. The winner mechanism says "where detail is missing, infer carefully and label the inference" — the TBD-with-method format is stricter and more useful for autonomous runs.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| appydave-plugins:skill:spec-writer | Full 21-section structure, extraction taxonomy, writing style rules, transformation rules, output location offer | Nothing set aside — this is the winner |
| agent-skills-osmani:skill:spec-driven-development | Explicit blocking ASSUMPTIONS block before spec content; six-area spec template (Objective, Commands, Project Structure, Code Style, Testing, Boundaries) | Commands/Project-Structure/Code-Style sections — those belong in a planning artifact, not a requirements doc; Osmani's spec blurs spec and plan |
| compound-engineering:skill:ce-brainstorm | Scope-decomposition gate for multi-subsystem requests; YAGNI applied to carrying cost; right-size ceremony | Phase system and blocking-question tooling — too much ceremony for David's stack where spec-writer is a one-shot transformation |
| spec-kit:command:specify | Numbered artifact IDs; per-feature directory scaffold (`specs/<NNN-feature-name>/`); pre-execution extension hooks | Extension hook system — Ruflo/spec-kit infrastructure dependency; git-feature-branch integration — belongs in `goal-plan`, not requirements capture |
| gsd:command:gsd:new-project | PROJECT.md with deep context gathering; phase-boundary awareness | Multi-phase project wiring — out of scope for a single feature spec; belongs in plan-to-goal sub-cluster |
| bmad-method:skill:bmad-agent-pm | PRD format with PRD lifecycle framing | BMAD-specific agent roles and `@` invocation model — not portable to David's single-agent pattern |
| everything-claude-code:command:plan-prd | TBD-with-method anti-fluff rule; lean problem-first framing | Separate-PRD-from-plan hard boundary — David's spec-writer already covers this by "not acting like an engineer choosing frameworks" |

## Draft SKILL.md frontmatter

```yaml
name: spec-writer
description: >
  Expert product owner, business analyst, and requirements strategist. Takes a long, messy
  brainstorm and transforms it into a clear, structured, decision-useful requirements document.
  Use when user says: "spec writer", "write a spec", "turn this brainstorm into a spec",
  "requirements document", "spec this out", "product spec", "BA this", "write the requirements
  for", "turn this into a requirements doc", "write the PRD", "document these requirements".
  Works on any app, domain, or system.
argument-hint: "[brainstorm text or topic] (blank = prompts for input)"
allowed-tools: "Read, Write, Edit"
```

## Open questions for David

1. **Elicitation gate threshold**: Should the assumptions-first block fire on every activation, or only when the brainstorm is below a legibility threshold? (Always-on is safer; threshold requires a heuristic that can misfire.)

2. **Numbered artifact IDs**: spec-kit's IDs (R1, A1, etc.) are load-bearing if a planning agent reads the spec — but they add friction for quick one-off specs. Should IDs be optional (off by default, toggled by `--structured` argument)?

3. **Scope decomposition**: Is the multi-subsystem decomposition gate better here, or should it live in `goal-plan`? (It affects scoping before spec writing, which suggests it belongs in `goal-plan`'s interview rather than inside `spec-writer`.)
