---
distillation_id: planning-ideation-and-requirements
stage: planning
intent: "Upstream ideation and requirements crystallization — turning a vague idea or direction into a scope-bounded, stakeholder-understood brief ready for roadmapping"
created: 2026-05-17
status: draft
source_artifacts:
  - compound-engineering:skill:ce-brainstorm
  - compound-engineering:skill:ce-ideate
  - compound-engineering:skill:ce-strategy
  - compound-knowledge:skill:kw:brainstorm
  - compound-knowledge:agent:past-work-researcher
  - agent-skills-osmani:skill:idea-refine
  - agent-skills-osmani:skill:interview-me
  - appydave-plugins:skill:brainstorm
  - appydave-plugins:skill:scope-analyst
  - appydave-plugins:skill:architectural-review
  - appydave-plugins:skill:relay-register
  - appydave-plugins:skill:delegation-router
  - everything-claude-code:skill:council
  - everything-claude-code:skill:literature-review
  - everything-claude-code:skill:api-design
  - everything-claude-code:skill:strategic-compact
  - superpowers:skill:brainstorming
  - ruflo:agent:agent-arch-system-design
  - ruflo:agent:agent-architecture
  - ruflo:skill:agent-migration-plan
  - ruflo:skill:domain-modeler
  - ruflo:skill:ddd
  - ruflo:skill:daa
  - ruflo:skill:ruflo-sparc
  - gsd:command:gsd:new-project
  - gsd:command:gsd:plant-seed
  - gsd:command:gsd:analyze-dependencies
  - gsd:agent:gsd-advisor-researcher
  - gsd:agent:gsd-research-synthesizer
  - gsd:agent:gsd-project-researcher
  - gsd:agent:gsd-assumptions-analyzer
winner_mechanism: compound-engineering:skill:ce-brainstorm
---

# Unified Skill: planning-ideation-and-requirements

**Purpose**: Transform a vague idea, direction, or "I want to build X" into a scope-bounded requirements document that is strong enough for roadmapping to proceed — without inventing product behavior or over-specifying implementation. The upstream gate before roadmapping.

**For Agents**: Use when David says "let's brainstorm", "help me think through this", "I want to build X but not sure what it needs", "what should this become", "ideate on this", "what are the requirements for this", "help me scope this", "let's define what this is before building". This is the **most upstream** planning skill — use it when the WHAT is unclear, not just the HOW.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Requirements documents fail in predictable ways: they invent product behavior when the user meant something different; they fail to name what is NOT in scope; they conflate capability (what users can do) with implementation (how the system does it); they don't pressure-test premises ("are we solving the right problem?") before generating approaches.

The ideation-and-requirements skill runs a structured dialogue — one question per turn — that pressure-tests the premise, names real scope boundaries, explores 2-3 concrete approaches before committing to one, and produces a requirements artifact that planning can use without re-litigating product decisions at every downstream step.

## Winner's Mechanism

`compound-engineering:skill:ce-brainstorm` wins for the most complete ideation-to-requirements pipeline: **named gap lenses** force rigor on premises before generating approaches (instead of jumping from "idea" to "approach A"); **one-question-per-turn discipline** prevents the common failure mode of five questions in one message (where two get answered and three are lost); **right-sized ceremony tiers** (Lightweight / Standard / Deep / Deep-product) let it scale with project stakes; and **stable requirement IDs** (R-IDs, A-IDs, F-IDs, AE-IDs) that flow through to the downstream plan ensure nothing gets silently dropped.

The lenses are the key mechanism: before proposing any approach, CE-brainstorm forces the user to verify:
- What problem does this actually solve?
- Who is affected?
- What are the scope boundaries (especially: what is explicitly NOT this)?
- What existing patterns or constraints apply?
- Are there dependencies being assumed that need surfacing?

`gsd:command:gsd:new-project` adds the most lightweight entry point: `/gsd-new-project` bootstraps the whole planning chain from a raw project description. It is not as dialogue-rich as CE-brainstorm, but it is the right tool when scope is relatively clear and you want to get to a roadmap quickly.

`gsd:agent:gsd-assumptions-analyzer` adds a mechanism CE-brainstorm handles implicitly: **make all assumptions explicit and logged before proceeding**. Running assumptions-analyzer after brainstorm surfaces the "we assumed this was true but never said it" class of planning errors.

## Non-overlapping ideas folded in

- From `compound-engineering:skill:ce-strategy`: **Strategy-anchored scoping** — before brainstorming what to build, anchor against documented product strategy. "Does this feature serve the current strategic direction?" prevents building correct features in the wrong direction. CE-strategy is the upstream gate even before CE-brainstorm. David doesn't have this equivalent; it's a real gap.
- From `compound-engineering:skill:ce-ideate`: **Multi-option exploration before committing** — present 2-3 concrete approaches with explicit trade-offs before recommending one. CE-brainstorm does this but CE-ideate makes it the primary output (a menu of directions, not a single direction). Useful when the problem space is genuinely undecided.
- From `superpowers:skill:brainstorming`: **Visual companion and spec-document reviewer** — after brainstorming, dispatch a spec-document reviewer to check the output against the original input. Prevents the common failure of a brainstorm output that diverges from what the user actually said. The reviewer asks: "does this requirements doc reflect the conversation we had?"
- From `agent-skills-osmani:skill:interview-me`: **Structured interview for self-discovery** — when David doesn't know what he wants, interview him with domain-specific questions rather than open-ended brainstorming. The interview mode surfaces requirements the user has but hasn't articulated; brainstorming mode explores possibilities the user hasn't considered. Both are valid entry points.
- From `ruflo:skill:domain-modeler`: **Domain model as requirements output** — for data-intensive features, the most useful requirements artifact is not a prose spec but a domain model (entities, relationships, key behaviors). Domain modeling before planning prevents "we built the wrong data structure" failures.
- From `gsd:agent:gsd-research-synthesizer`: **Research synthesis as brainstorm input** — for unfamiliar technical domains, run research BEFORE brainstorming, not during planning. Knowing what patterns already exist shapes what requirements are realistic. GSD's research-synthesizer produces a SUMMARY.md that feeds project kickoff; the equivalent is missing from David's upstream ideation.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|--------------------|
| compound-engineering:ce-brainstorm | One-question-per-turn, named gap lenses, right-sized ceremony tiers, R/A/F/AE-IDs, spec-document reviewer post-check | CE-specific integration details |
| compound-engineering:ce-ideate | Multi-option exploration before committing to a direction | CE ideation chain specifics |
| compound-engineering:ce-strategy | Strategy-anchored scoping as upstream gate | CE strategy document format |
| superpowers:brainstorming | Visual companion; spec-document reviewer post-output check | Superpowers harness |
| agent-skills-osmani:interview-me | Structured interview mode for self-discovery | Osmani persona |
| ruflo:domain-modeler | Domain model as requirements artifact for data-intensive features | Ruflo-specific |
| gsd:new-project | Lightweight project bootstrap as fast entry point | GSD workspace specifics |
| gsd:assumptions-analyzer | Post-brainstorm assumption surfacing | GSD agent format |

## Boundary with adjacent sub-clusters

- **planning-roadmap-architect**: This skill produces the requirements input; roadmap-architect consumes it and produces the phased delivery plan. If requirements exist (PRD, issue, list), skip this skill. If the WHAT is unclear, start here.
- **spec-writing**: The `spec-writing` cluster (separate from planning) covers writing specs for implementation. Ideation-and-requirements covers crystallizing what the spec should be about — upstream of spec-writing.
- **planning-task-breakdown**: Task breakdown is many levels downstream. Ideation doesn't produce tasks; it produces a requirements document strong enough that the whole planning chain (roadmap → sprint → tasks) can proceed without re-litigating product decisions.

## Draft SKILL.md frontmatter

```yaml
name: planning-ideation-and-requirements
description: >
  Transform a vague idea into a scope-bounded requirements document ready for roadmapping.
  Runs one-question-per-turn dialogue, applies named gap lenses to pressure-test premises,
  explores 2-3 approaches before recommending, produces stable requirement IDs (R/A/F/AE).
  Use when: "let's brainstorm", "help me think through this", "I want to build X but unsure what it needs",
  "what should this become", "ideate on this", "what are the requirements", "help me scope this",
  "let's define what this is before building".
```

## Open questions for David

- `ce-strategy` (strategy-anchor before brainstorming) is a genuine gap. David has `north-star` brain for his direction, but no skill that checks "does this proposed feature serve the current strategic direction?" before allowing brainstorming to proceed. Worth building as a pre-gate?
- Interview mode (`interview-me`) vs brainstorm mode: these feel like different cognitive postures for different situations. Should they be separate skills with distinct triggers, or a mode within a single ideation skill?
- Domain modeling (`ruflo:domain-modeler`) as requirements output is most useful for data-intensive features. Should this be an optional output format of ideation-and-requirements, or a separate skill invoked after requirements crystallization?
