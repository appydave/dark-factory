---
distillation_id: spec-writing-prd-lifecycle
stage: spec-writing
intent: "Create, validate, and evolve a Product Requirements Document through a structured lifecycle — problem-first, hypothesis-driven"
created: 2026-05-17
status: draft
source_artifacts:
  - bmad-method:skill:bmad-prd
  - bmad-method:skill:bmad-create-prd
  - bmad-method:skill:bmad-edit-prd
  - bmad-method:skill:bmad-validate-prd
  - bmad-method:skill:bmad-prfaq
  - bmad-method:skill:bmad-product-brief
  - bmad-method:skill:bmad-agent-pm
  - agent-skills-osmani:skill:spec-driven-development
  - everything-claude-code:command:prp-prd
  - everything-claude-code:command:plan-prd
winner_mechanism: bmad-method:skill:bmad-prd
---

# Unified Skill: prd-lifecycle

**Purpose**: Create, update, validate, or analyze a Product Requirements Document through an explicit intent-driven lifecycle — problem-first, hypothesis-driven, with the PRD as the primary artifact that drives all downstream planning.

**For Agents**: Use when David says "create a PRD", "update the PRD", "validate the PRD", "work backwards from the customer", "PRFAQ this", "product brief", or when starting a new product rather than a single feature (use `spec-writer` for features; use `prd-lifecycle` for product-level decisions).

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Manage the full lifecycle of a Product Requirements Document: create from scratch (problem-first interview → hypothesis → PRD), update when direction changes, validate against constitution or principles, analyze for gaps. The PRD is the source of truth that spec-writer outputs feed into.

## Winner's Mechanism

`bmad-method:skill:bmad-prd` wins because it is the only artifact in the corpus that explicitly handles all four intents (create / update / validate / analyze) within a single skill with intent detection — avoiding the maintenance burden of separate `bmad-create-prd`, `bmad-edit-prd`, and `bmad-validate-prd` skills (two of which are explicitly deprecated in BMAD v7). BMAD's PRD lifecycle is the most mature product-management workflow in the corpus with versioned semantics, and it treats the PRD as the driving artifact rather than a document that supports code. The `bmad-prfaq` and `bmad-product-brief` are upstream artifacts that feed into PRD creation; they are folded in as non-overlapping ideas rather than replaced.

## Contrast: heavy PRD-lifecycle vs lightweight requirements capture

This is the key tension in the spec-writing cluster:

| Dimension | prd-lifecycle (heavy) | spec-writer (lightweight) |
|-----------|----------------------|--------------------------|
| Scope | Product-level, multi-sprint | Feature-level, single spec |
| Starting point | Problem discovery → hypothesis | Brainstorm → transformation |
| Lifecycle | Create → update → validate → analyze | Single activation |
| Artifact persistence | PRD evolves over time | Spec saved, rarely updated |
| When to use | New product, major pivot | Feature, story, one-off request |

The two are **complementary**, not competing. `spec-writer` outputs feed into PRD sections. `prd-lifecycle` creates the container that `spec-writer` results populate.

## Non-overlapping ideas folded in

- From `everything-claude-code:command:prp-prd`: Hypothesis-driven FRAME phase — "We believe {capability} will {solve problem} for {users}. We'll know we're right when {measurable outcome}." — `complexity: low | optional: false | prerequisite: none`. BMAD's PRD create path does not force a hypothesis statement; ECC's prp-prd does. A falsifiable hypothesis is the strongest anti-scope-creep mechanism in the corpus.

- From `everything-claude-code:command:plan-prd`: Hard boundary enforcement — when implementation detail creeps into the PRD, stop and cut it. Anti-fluff rule: `TBD — needs validation via {method}` rather than invented requirements. — `complexity: low | optional: false | prerequisite: none`. BMAD's PRD can get verbose; ECC's lean PRD enforces a cleaner boundary.

- From `bmad-method:skill:bmad-prfaq`: Working Backwards PRFAQ challenge as an optional upstream elicitation mode — write the press release and FAQ before the PRD to surface the product's core value proposition. — `complexity: medium | optional: true | prerequisite: "new product, not an existing product update"`. PRFAQ is Amazon's mechanism for avoiding products nobody wants; folded as an optional pre-phase, not a mandatory step.

- From `bmad-method:skill:bmad-product-brief`: Product Brief as a lighter-weight pre-PRD artifact for early-stage products where full PRD is premature. — `complexity: low | optional: true | prerequisite: "pre-discovery phase, idea not yet validated"`. The brief is the one-pager before the PRD; both fit the same intent under different maturity levels.

- From `spec-kit` (via `spec-driven.md`): Version the PRD with semver (MAJOR for new product direction, MINOR for scope changes, PATCH for clarity edits) and maintain a Sync Impact Report when MAJOR changes propagate to downstream artifacts. — `complexity: medium | optional: true | prerequisite: "PRD is under active multi-sprint development"`. spec-kit is the only corpus member with explicit PRD versioning; without it, "current PRD" is ambiguous across sessions.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| bmad-method:skill:bmad-prd | Four-intent routing (create/update/validate/analyze); PRD as primary driver; lifecycle framing | BMAD's `@` agent invocation model; role-specific personas (PM agent, Analyst agent) — not portable to David's single-agent pattern |
| bmad-method:skill:bmad-prfaq | Working Backwards PRFAQ challenge; press-release-first framing | BMAD-specific workflow wiring; Amazon-internal vocabulary where not needed |
| bmad-method:skill:bmad-product-brief | Product Brief as pre-PRD lightweight artifact | BMAD ceremony around brief creation |
| everything-claude-code:command:prp-prd | Hypothesis statement (falsifiable, measurable); QUESTION SET 1→GROUNDING→2→RESEARCH→3→GENERATE flow; evidence-before-building rigor | Market research ceremony (Phase 3 grounding) — too heavyweight for David's solo stack; external research agents not available |
| everything-claude-code:command:plan-prd | Hard PRD/plan boundary enforcement; lean structure; TBD-with-method anti-fluff | Nothing else — the whole lean PRD framing is folded in |
| agent-skills-osmani:skill:spec-driven-development | "Spec is the source of truth; code serves spec" framing | Six-area tech spec template — that's a planning artifact, not PRD content |

## Draft SKILL.md frontmatter

```yaml
name: prd-lifecycle
description: >
  Product Requirements Document lifecycle manager — create, update, validate, and analyze a PRD.
  Treats the PRD as the primary artifact that all planning derives from, not a document that supports code.
  Use when user says: "create a PRD", "update the PRD", "validate the PRD", "PRFAQ this",
  "product brief", "work backwards from the customer", "write the product requirements",
  "we need a PRD for", "product-level spec". Use for new products or major pivots.
  For single features, use spec-writer instead.
argument-hint: "[intent: create|update|validate|analyze] [product-name or description]"
allowed-tools: "Read, Write, Edit"
```

## Open questions for David

1. **PRD vs spec-writer entry point**: Should there be an explicit routing rule — "if single feature, use spec-writer; if new product or multi-sprint initiative, use prd-lifecycle"? Or should prd-lifecycle detect scope and self-route?

2. **PRFAQ as mandatory pre-step**: Amazon uses PRFAQ before PRD for every new product. Is that the right discipline for David's products (especially AppyStack, new apps), or is the press-release exercise too much ceremony for AppyDave-scale projects?

3. **PRD versioning**: semver for PRDs only makes sense when multiple sessions iterate on the same PRD. Is Kybernesis the right project to introduce PRD versioning on, or is it still too early?
