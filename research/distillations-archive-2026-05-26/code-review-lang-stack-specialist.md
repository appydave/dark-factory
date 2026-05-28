---
distillation_id: code-review-lang-stack-specialist
stage: audit
intent: "Language and framework-specific reviewer — stack idioms, conventions, and anti-patterns that generic reviewers miss"
created: 2026-05-16
status: draft
source_artifacts:
  - compound-engineering:agent:ce-dhh-rails-reviewer
  - compound-engineering:agent:ce-kieran-rails-reviewer
  - compound-engineering:agent:ce-kieran-python-reviewer
  - compound-engineering:agent:ce-kieran-typescript-reviewer
  - compound-engineering:agent:ce-julik-frontend-races-reviewer
  - compound-engineering:agent:ce-swift-ios-reviewer
  - everything-claude-code:command:cpp-review
  - everything-claude-code:command:flutter-review
  - everything-claude-code:command:go-review
  - everything-claude-code:command:kotlin-review
  - everything-claude-code:command:python-review
  - everything-claude-code:command:rust-review
  - everything-claude-code:skill:flutter-dart-code-review
  - everything-claude-code:skill:angular-developer
  - everything-claude-code:skill:accessibility
  - everything-claude-code:agent:a11y-architect
  - gsd:command:gsd:ui-review
  - gsd:agent:gsd-ui-auditor
  - gstack:skill:plan-devex-review
  - gstack:skill:plan-eng-review
  - gstack:skill:design-review
  - gstack:skill:plan-design-review
  - ruflo:skill:Pair Programming
winner_mechanism: compound-engineering:agent:ce-kieran-typescript-reviewer
---

# Unified Skill: code-review-lang-stack-specialist

**Purpose**: Pattern for building language and framework-specific reviewer specialists. Activates when a diff touches stack-specific code (TypeScript components, Rails models, Python services, etc.) and applies idiom-aware review that generic reviewers miss. Not a single unified skill — this is a **family pattern** for building specialized reviewers.

**For Agents**: Use this distillation when David asks to build a new language-specific reviewer or when a diff triggers stack-specific conventions that `delivery-review`'s generic dimensions would miss. Current priority stacks for David: TypeScript/Next.js, Ruby/Rails, Python.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

## Intent

Provide stack-idiomatic review that catches conventions, anti-patterns, and gotchas specific to a language or framework — the things a generic correctness or maintainability reviewer doesn't know to look for because they aren't encoded in universal principles.

## Winner's Mechanism

`compound-engineering:agent:ce-kieran-typescript-reviewer` represents the pattern best. It demonstrates:

1. **Named persona with recognized expertise** — "Kieran" is a named style authority. This is deliberate: it signals to the model to adopt a specific technical opinion, not a neutral stance. The reviewer has preferences and applies them.
2. **Framework-aware conditionals** — different checks apply to different parts of the stack (React hooks vs utility functions vs shared types vs API route handlers).
3. **Conditional activation** — selected when diff touches TypeScript components, services, hooks, utilities, or shared types. Not always-on.

The **DHH Rails reviewer** adds a second dimension: architectural opinions that override framework defaults. DHH-style Rails challenges service objects, rejects unnecessary abstractions, and enforces convention-over-configuration at the design level. This is distinct from `ce-kieran-rails-reviewer` which focuses on application conventions.

ECC's language-specific commands (`python-review`, `go-review`, `rust-review`, `flutter-review`) show the same pattern but implemented as lightweight commands rather than full persona agents. For David's stack (Next.js + occasional Ruby), the CE persona approach is richer.

## Non-overlapping ideas folded in

- From `gsd:agent:gsd-ui-auditor`: **Visual regression check** alongside code review — verify UI components render correctly, not just implement correctly. Separate concern but adjacent to TypeScript/React review.
- From `everything-claude-code:agent:a11y-architect` + `accessibility` skill: **Accessibility as a first-class review dimension** for UI code — not an afterthought check but a structural concern. When reviewing React/Next.js components, accessibility violations are functional bugs, not style preferences.
- From `gstack:skill:plan-devex-review`: **Developer experience as a review axis** — is this API pleasant to use? Does the abstraction serve the next developer? Orthogonal to correctness and architecture, adds a usability lens to code review.
- From `ruflo:skill:Pair Programming`: Live pair-style review where the reviewer suggests alternatives inline rather than only flagging issues — more collaborative than traditional review comments. Different mode, worth offering as an option.

## Candidate stack-specific specialists for David

Based on David's active projects (Next.js + TypeScript, Ruby/Rails, Python scripts):

| Persona | Activation signal | Priority |
|---------|------------------|----------|
| `review-typescript` | `.ts`/`.tsx` files, React hooks, Next.js routes | HIGH — primary stack |
| `review-rails` | `app/models/`, `app/controllers/`, migrations | MEDIUM — some client work |
| `review-python` | Python scripts, agents | LOW — occasional |
| `review-accessibility` | React components with UI elements | MEDIUM — SupportSignal is NDIS (accessibility matters) |

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| ce-kieran-typescript-reviewer | Named-persona approach, framework-conditional checks, activation signal pattern | CE-specific JSON output format |
| ce-dhh-rails-reviewer | Architectural opinions that override defaults, convention enforcement | Rails-specifics (not David's primary stack) |
| ce-julik-frontend-races-reviewer | Frontend race condition patterns (Stimulus/Turbo, DOM events, async UI) | Hotwire-specific (not David's stack) |
| ce-swift-ios-reviewer | iOS platform conventions pattern | Not David's stack |
| python-review / go-review / rust-review (ecc) | Lightweight language-command pattern as an alternative to full persona agents | ECC-specific preamble |
| a11y-architect + accessibility (ecc) | Accessibility-as-functional-bug framing, WCAG as review criterion | ECC accessibility tooling |
| gsd:ui-auditor | Visual regression concern alongside code review | GSD pipeline coupling |
| plan-devex-review (gstack) | Developer-experience review axis | Plan-review specifics |

## Draft SKILL.md frontmatter (TypeScript variant — David's primary stack)

```yaml
name: review-typescript
description: >
  TypeScript and React/Next.js specialist reviewer — idiom-aware review that catches type safety
  issues, hook rules violations, component design anti-patterns, and Next.js conventions that
  generic reviewers miss. Conditional: activates when diff touches .ts/.tsx files.
  Use when: "TypeScript review", "React review", "Next.js review", "check my components",
  "type safety review", "hooks review", "review this React code".
  Part of delivery-review as an optional 8th dimension for TypeScript projects.
```

## Open questions for David

- Should stack-specific reviewers be **added as conditional dimensions** to `delivery-review` (like CE does: "select when diff touches TypeScript"), or kept as **standalone skills** invoked explicitly? CE's model of automatic conditional selection is more ergonomic but requires the orchestrator to inspect the diff before dispatching.
- Accessibility review: is this a standalone `review-accessibility` skill, or should it be folded into `review-typescript` as a UI-components check? SupportSignal context makes this non-trivial — NDIS compliance requires WCAG AA at minimum.
- The `ce-julik-frontend-races-reviewer` covers Stimulus/Turbo async UI races. David uses React/Next.js not Rails/Turbo — but is there a React-equivalent race-condition reviewer worth building? (Concurrent renders, useEffect dependencies, stale closures.)
