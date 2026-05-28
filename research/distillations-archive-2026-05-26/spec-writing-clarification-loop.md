---
distillation_id: spec-writing-clarification-loop
stage: spec-writing
intent: "Close the gap between what was asked and what is actually wanted — via one-question-at-a-time structured elicitation before any spec, plan, or code begins"
created: 2026-05-17
status: draft
source_artifacts:
  - agent-skills-osmani:skill:interview-me
  - bmad-method:skill:bmad-advanced-elicitation
  - spec-kit:command:clarify
  - gsd:command:gsd:discuss-phase
  - gsd:command:gsd:list-phase-assumptions
winner_mechanism: agent-skills-osmani:skill:interview-me
---

# Unified Skill: clarify (requirements elicitation)

**Purpose**: Extract what the user actually wants (not what they asked for) through one-question-at-a-time structured interview, surfacing hidden intent, constraints, and assumptions before any spec or plan begins.

**For Agents**: Use when David says "ask me questions first", "interview me before you write anything", "I'm not sure what I want yet", "clarify this before speccing", or when an incoming request is underspecified and the spec-writer or prd-lifecycle would otherwise silently fill in wrong assumptions.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Surface what the user actually wants through structured elicitation — not transcription of what they said. The output is a set of resolved answers (or confident assumptions) that feed directly into spec-writer, prd-lifecycle, or goal-plan. The skill itself writes nothing except the clarification artifact.

## Winner's Mechanism

`agent-skills-osmani:skill:interview-me` wins because it is the most mechanically precise elicitation skill in the corpus. Its mechanism: ask one question at a time until ~95% confidence about the underlying intent, then produce a resolution artifact. The key insight is that it fires *before any plan, spec, or code exists* — not as a post-spec review pass. Osmani's framing ("extracts what the user actually wants instead of what they think they should want") is the right intent model for David's use case: the biggest spec failures come from David knowing the solution before articulating the problem. The skill forces problem articulation before solution space.

## Contrast with spec-kit's /clarify

spec-kit's `/clarify` is a **post-spec** clarification command — it identifies underspecified areas in an *existing* spec.md and encodes answers back. Osmani's `interview-me` is **pre-spec** — it fires before any spec exists. These are distinct jobs:

| | pre-spec elicitation (interview-me) | post-spec clarification (spec-kit clarify) |
|--|-------------------------------------|---------------------------------------------|
| When | Before spec exists | After spec.md is written |
| Input | Vague request or idea | Existing spec.md |
| Output | Resolved requirements feed | Up to 5 targeted questions encoded back into spec |
| Job | Extract intent | Fill gaps in a document |

Both belong in the stack; they operate at different grains.

## Non-overlapping ideas folded in

- From `bmad-method:skill:bmad-advanced-elicitation`: Push the LLM to reconsider, refine, and improve its recent output — apply 6 elicitation techniques (fresh perspective, devil's advocate, first principles, alternative approaches, assumption challenges, steelman). — `complexity: medium | optional: true | prerequisite: "spec or output already exists and David wants to pressure-test it"`. BMAD elicitation is post-output refinement, not pre-spec elicitation — it's a different grain from interview-me and fills a gap Osmani's skill doesn't cover.

- From `spec-kit:command:clarify`: Up-to-5-targeted-questions discipline — do not fire more than 5 clarification questions at a time; resolve the most impactful ones first. — `complexity: low | optional: false | prerequisite: none`. Osmani's skill has no question count discipline; spec-kit's limit forces prioritisation and prevents elicitation becoming an interview marathon.

- From `gsd:command:gsd:discuss-phase`: Adaptive questioning producing a CONTEXT.md artifact that gates the next phase — elicitation output is a durable artifact that downstream agents consume, not just a chat exchange. — `complexity: medium | optional: true | prerequisite: "elicitation will feed a multi-phase project, not a single spec"`. GSD's discuss-phase is the only corpus mechanism that turns elicitation into a phase-gate artifact; for one-off specs the overhead is unnecessary; for multi-phase projects it prevents re-elicitation in each phase.

- From `gsd:command:gsd:list-phase-assumptions`: Surface implicit assumptions before questioning begins — "here are the assumptions I'm making about this request, correct or confirm." — `complexity: low | optional: false | prerequisite: none`. Osmani's skill extracts intent; GSD's assumption surface step makes the model's hidden priors visible before the interview, preventing the model from building an interview around wrong baseline assumptions.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| agent-skills-osmani:skill:interview-me | One-question-at-a-time discipline; 95% confidence threshold; "what they actually want vs what they asked for" framing; pre-spec-and-code gate | Specific question taxonomy — generalised to the 5-question limit rather than a fixed list |
| bmad-method:skill:bmad-advanced-elicitation | 6 elicitation techniques for post-output pressure testing; devil's advocate framing | BMAD's specific output format; the `@` agent invocation model |
| spec-kit:command:clarify | 5-question maximum; encode-answers-back-into-spec-md mechanism; post-spec grain | Extension hooks; CLI integration; speckit-specific directory structure |
| gsd:command:gsd:discuss-phase | CONTEXT.md durable artifact; phase-gate wiring; adaptive questioning | GSD multi-phase project machinery; CONTEXT.md format specifically |
| gsd:command:gsd:list-phase-assumptions | List-assumptions-before-questioning step; assumption surfacing as a separate pre-question beat | GSD phase naming and wiring |

## Draft SKILL.md frontmatter

```yaml
name: clarify
description: >
  Structured requirements elicitation — extracts what the user actually wants through
  one-question-at-a-time interview until ~95% confidence about underlying intent.
  Use before any spec, plan, or code begins when the request is underspecified, ambiguous,
  or solution-first. Triggers on: "ask me questions first", "interview me before writing",
  "clarify this", "what do I actually need", "I'm not sure what I want". Does not write
  specs — produces the resolved inputs that spec-writer or prd-lifecycle then formalise.
argument-hint: "[topic or vague request to clarify] (blank = prompts for topic)"
allowed-tools: "Read, Write"
```

## Open questions for David

1. **One skill or entry point to spec-writer?** Should `clarify` be a standalone skill, or should `spec-writer` optionally trigger a clarify pass when the brainstorm is below a legibility threshold? (Standalone is more explicit; integrated is lower friction.)

2. **CONTEXT.md artifact**: Should the clarification output always be written to a file (GSD pattern — durable, agent-consumable), or is a chat-level resolution sufficient for one-off specs? For Kybernesis-style multi-session projects, the durable artifact is load-bearing.

3. **BMAD advanced elicitation placement**: The 6 pressure-testing techniques (devil's advocate, first principles, etc.) are post-output tools, not pre-spec tools. Should they be in this skill (as an optional `--pressure-test` mode), or in a separate `pressure-test` skill that `spec-writer` hands off to?
