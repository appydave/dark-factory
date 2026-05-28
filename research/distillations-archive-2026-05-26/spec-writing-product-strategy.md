---
distillation_id: spec-writing-product-strategy
stage: spec-writing
intent: "Create and maintain a short durable strategy document — target problem, approach, users, metrics, tracks of work — that grounds all downstream specs and planning"
created: 2026-05-17
status: draft
source_artifacts:
  - compound-engineering:skill:ce-strategy
  - everything-claude-code:skill:product-lens
  - everything-claude-code:skill:product-capability
  - bmad-method:skill:bmad-domain-research
  - bmad-method:skill:bmad-market-research
  - bmad-method:skill:bmad-technical-research
  - compound-engineering:agent:ce-product-lens-reviewer
winner_mechanism: compound-engineering:skill:ce-strategy
---

# Unified Skill: product-strategy

**Purpose**: Create and maintain `STRATEGY.md` — a short, durable anchor document capturing what the product is, who it serves, how it succeeds, and where work is being invested — that downstream spec and planning tools read as upstream grounding.

**For Agents**: Use when David says "write our strategy", "update the roadmap", "what are we working on", "set up the strategy doc", "product vision", "what problem does this solve", or when `ce-brainstorm`, `spec-writer`, or `prd-lifecycle` need upstream grounding and no strategy doc exists.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Write a one-page, durable `STRATEGY.md` that answers: what problem, for whom, by what approach, measured how, with what tracks of work. Short by design — if it can't fit in one page, the strategy isn't clear yet. Downstream skills (`spec-writer`, `prd-lifecycle`, `goal-plan`) read it as grounding. The skill is rerunnable: on a second run it updates in place, preserves what is working, challenges stale sections.

## Winner's Mechanism

`compound-engineering:skill:ce-strategy` wins because it is the most disciplined strategy-writing skill in the corpus. Its key properties: (1) short is a feature — the template is constrained by design; (2) rigor in the questions, not the headings — the interview enforces strategy discipline, not just section filling; (3) durable across runs — rerunnable, updates in place, challenges weak or stale sections; (4) downstream-grounding — `ce-brainstorm`, `ce-plan`, and `ce-ideate` all read STRATEGY.md when it exists. No other corpus member treats strategy as a machine-readable grounding document.

This sub-cluster is distinct from PRD lifecycle: a PRD captures requirements for a specific initiative. A strategy captures what the product IS and why — the context that all PRDs operate within.

## Contrast: CE strategy vs ECC product-lens vs BMAD research

| | CE strategy | ECC product-lens | BMAD domain/market/tech research |
|--|------------|-----------------|----------------------------------|
| Artifact | STRATEGY.md (concise, durable) | Inline validation questions | Research reports (domain, market, tech) |
| When | Once per product, reruns as direction evolves | Before building, to validate "why" | During early discovery, to gather evidence |
| Agent role | Interview → write → update | Challenge mode, not write | Gather external context |
| Output | One-page anchor doc | Validated direction or flagged concerns | Research artifacts fed into PRD |
| Grain | Product-level, multi-sprint | Per-build validation | Pre-PRD evidence gathering |

The three are sequenced: BMAD research gathers evidence → CE strategy anchors direction → ECC product-lens validates each build decision against strategy.

## Non-overlapping ideas folded in

- From `everything-claude-code:skill:product-lens`: Validate the "why" before building — pressure-test product direction, diagnose gaps in product thinking, challenge "we should build X" with "does X solve the right problem". — `complexity: low | optional: true | prerequisite: "a specific build decision is being considered"`. ECC product-lens is a per-decision validation pass; CE strategy is the document. The product-lens skill reads the strategy to validate individual build decisions against it.

- From `everything-claude-code:skill:product-capability`: Translate PRD intent or roadmap asks into an implementation-ready capability plan — surfaces constraints, exposes coupling, and maps requirement to capability. — `complexity: medium | optional: true | prerequisite: "PRD exists and needs to be translated into technical capabilities"`. This skill is the bridge between strategy and architecture; folded as an optional downstream step after strategy is established.

- From `bmad-method:skill:bmad-domain-research`: Domain research pass — investigate domain-specific context (industry structure, regulatory environment, existing solutions) before writing strategy. — `complexity: medium | optional: true | prerequisite: "unfamiliar domain or new market"`. BMAD's research trinity (domain + market + technical) is the evidence-gathering layer that feeds strategy. For David's known-domain projects (NDIS, creator economy) this is less critical; for new domains it's load-bearing.

- From `compound-engineering:agent:ce-product-lens-reviewer`: As a document-review agent — after strategy is written, run the product-lens reviewer as a challenge pass: "Does this strategy solve the right problem? Are the metrics the right ones? Is the approach realistic?" — `complexity: medium | optional: true | prerequisite: "strategy doc is written and David wants to pressure-test it"`. Distinct from the product-lens skill (which validates build decisions); the reviewer challenges the strategy document itself.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| compound-engineering:skill:ce-strategy | STRATEGY.md as a machine-readable grounding file; interview-then-write pattern; rerunnable with section-targeted updates; "short is a feature" principle; downstream-reading by brainstorm and plan | CE-specific `AskUserQuestion` blocking-question tool; `references/interview.md` (skill-internal detail) |
| everything-claude-code:skill:product-lens | "Validate why before building" framing; product-diagnostic questions (is this the right problem? right users? right metric?) | ECC-specific formatting; ECC-internal taxonomy |
| everything-claude-code:skill:product-capability | Capability-mapping from PRD to technical capabilities; constraint surfacing | Detailed implementation planning elements — belongs in plan step |
| bmad-method:skill:bmad-domain-research | Domain-research as upstream evidence gathering; structured research report format | BMAD's specific `@` agent invocation; BMAD format requirements |
| bmad-method:skill:bmad-market-research | Market context; competitive analysis; customer validation | Same BMAD wiring as domain-research |
| bmad-method:skill:bmad-technical-research | Technical feasibility research; stack options analysis | Same BMAD wiring |
| compound-engineering:agent:ce-product-lens-reviewer | Strategy-document challenge pass | CE-specific agent invocation model |

## Draft SKILL.md frontmatter

```yaml
name: product-strategy
description: >
  Create or maintain STRATEGY.md — a short, durable anchor document capturing what the product is,
  who it serves, how it succeeds, and where work is being invested. Downstream spec and planning
  skills read it as upstream grounding. Rerunnable: updates in place, challenges stale sections.
  Use when David says: "write our strategy", "update the roadmap", "set up the strategy doc",
  "what problem does this solve", "product vision", "what are we working on".
  Distinct from spec-writer (features) and prd-lifecycle (requirements): strategy is the WHY
  that all requirements operate within.
argument-hint: "[section to revisit: 'problem'|'approach'|'metrics'|'tracks'] (blank = full strategy)"
allowed-tools: "Read, Write, Edit"
```

## Open questions for David

1. **STRATEGY.md vs north-star brain**: David already has a `north-star` brain that captures long-horizon direction (Star, Vehicle, Waypoints, Orbits). Where does product-level STRATEGY.md fit relative to that? (Suggestion: north-star is personal/life; STRATEGY.md is per-product, reads the relevant north-star section as context.)

2. **Kybernesis adoption**: Kybernesis is the most complex active product (three founders, external capital). A STRATEGY.md for Kybernesis that David, Ian, and Martin can all read/update would prevent the strategy from living only in David's head. Is this the right first deployment?

3. **Research trinity gate**: BMAD's domain + market + technical research are upstream inputs to strategy. For SupportSignal (NDIS, known domain), these aren't needed. For Kybernesis (new market), they are. Should `product-strategy` optionally trigger a research pass if the domain is unfamiliar?
