---
artifact_id: agent-skills-osmani:skill:spec-driven-development
repo: agent-skills-osmani
artifact_type: skill
cluster_facet: [spec-writing, requirements, gated-workflow]
phase_fit: [1]
evaluated_at: 2026-05-17
---

# Eval: spec-driven-development

**Intent**: Four-phase gated workflow (Specify → Plan → Tasks → Implement) that writes a structured spec with six mandatory sections before any code is written, with human review gates at each phase.

## Scores

- **quality_score**: 5. The gated workflow diagram, six-section spec template, assumption-surfacing protocol, reframe-to-success-criteria technique, and living-document principles are all exemplary. One of the two anchor artifacts for stage 1.
- **adoption_fit_final**: `strong`. Stack-agnostic process skill; the spec template is applicable to any project type.
- **inspiration_value**: `high`. "Reframe instructions as success criteria" (convert "make it faster" into measurable LCP/CLS targets) is a practical technique rarely codified in skill bodies.
- **uniqueness_refined**: `uncommon`. The explicit assumption-surfacing block (ASSUMPTIONS I'M MAKING: / → Correct me now) before writing any spec content is not common in other spec skills.
- **composability**: `calls-others`. Phase 4 explicitly delegates to incremental-implementation and test-driven-development skills, and references context-engineering for loading.
- **description_craft_refined**: `trigger`. Two concise trigger conditions; clean.

## Mineable phrasing

> "Don't silently fill in ambiguous requirements. The spec's entire purpose is to surface misunderstandings *before* code gets written — assumptions are the most dangerous form of misunderstanding."

## Notes

The three-tier Boundaries section (Always / Ask First / Never) is one of the most reusable artifacts in the batch — a constraint classification system applicable to any agentic workflow. The "spec is a living document" section with commit-to-git and reference-in-PRs practices shows operational maturity beyond the write-once pattern. Strong pairing candidate with interview-me for a full requirements-to-spec pipeline.
