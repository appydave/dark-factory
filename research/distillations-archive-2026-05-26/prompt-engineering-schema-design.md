---
distillation_id: prompt-engineering-schema-design
cluster: prompt-engineering
sub_cluster: prompt-schema-design
intent: "Design the data contract (JSON schema + Handlebars placeholder vocabulary) for a prompt before authoring the template body — schema-first prompt engineering"
created: 2026-05-17
status: draft
source_artifacts:
  - appydave:skill:spec-writer
  - appydave:skill:poem-slides
  - everything-claude-code:skill:cost-aware-llm-pipeline
  - everything-claude-code:agent:type-design-analyzer
  - everything-claude-code:agent:code-architect
winner_mechanism: appydave/penny-prompt-engineer (poem-os) *generate-schema + *validate commands
---

# Unified Skill: prompt-schema-designer

**Purpose**: Design the data contract for a prompt before writing its body — enumerate placeholders, assign types, define required vs optional, generate JSON schema, and validate placeholder-schema alignment. Schema-first prompt engineering following POEM conventions.

**For Agents**: Use when David says "generate a schema for this prompt", "what placeholders does this prompt need", "validate my template", "check my Handlebars syntax", "schema for prompt", or is preparing a prompt template for production use where data contract integrity matters.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Make the data contract for a prompt explicit before the template body is authored. The schema defines what data the prompt consumes — placeholder names, types, required/optional, enum constraints. The Handlebars template is then written *against* the schema, not the other way around. Post-authoring validation checks that no placeholder in the template is absent from the schema and vice versa.

## Winner's Mechanism

Penny's `*generate-schema` and `*validate` commands (POEM OS) are the only artifacts in the corpus with explicit schema-alongside-template authoring as a first-class workflow step:

1. **Schema enumeration**: list every `{{placeholder}}` in the template; for each, specify type (string, number, boolean, array, object), required/optional, validation constraints (minLength, enum, format).
2. **JSON Schema generation**: emit a JSON Schema (draft-07 compatible) co-located with the template at `/poem/schemas/<name>.json`.
3. **Alignment validation**: diff template placeholders vs schema properties — flag orphaned placeholders (in template, not in schema) and dead schema properties (in schema, not in template).
4. **Severity escalation**: missing required placeholder = error; missing optional = warning; type mismatch = error; undocumented `{{else}}` block = warning.

The mechanism applies to any Handlebars-style template, not only POEM templates.

## Non-overlapping ideas folded in

- From `everything-claude-code:skill:cost-aware-llm-pipeline`: model routing by task complexity is itself a schema design concern — the data contract of a prompt includes which model tier it is designed for (Haiku/Sonnet/Opus) and what its token budget targets are. Extend the schema with `model_tier`, `max_input_tokens`, `max_output_tokens` as optional fields. This makes cost estimation a schema-time operation rather than a runtime surprise.
- From `everything-claude-code:agent:type-design-analyzer`: the same invariant-expression discipline that applies to type design applies to placeholder schemas — a placeholder named `context` with type `string` expresses no invariant; a placeholder named `customer_incident_summary` with type `string`, `minLength: 20`, `maxLength: 500` expresses the invariant that it is always a non-trivial bounded summary. Name and type together encode the constraint. The agent's "encapsulation + invariant + usefulness" rubric maps directly to placeholder design quality.
- From `everything-claude-code:agent:code-architect`: codebase pattern analysis before blueprinting — equivalent principle: analyse existing schemas/templates in the project before designing a new one, to ensure naming conventions and type patterns are consistent. A prompt schema library is an emergent shared vocabulary across a project's prompt templates.

## Schema shape (POEM convention)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PromptName",
  "description": "One-line purpose of this prompt",
  "type": "object",
  "required": ["field1", "field2"],
  "properties": {
    "field1": {
      "type": "string",
      "description": "What this field represents",
      "minLength": 1
    },
    "field2": {
      "type": "array",
      "items": { "type": "string" },
      "description": "List of X"
    },
    "optional_field": {
      "type": "string",
      "description": "Optional context",
      "default": ""
    }
  },
  "additionalProperties": false
}
```

The `additionalProperties: false` constraint is the schema equivalent of `injection-resistance`: it prevents arbitrary additional context from being injected into the prompt through the data contract.

## Validation checklist

When running Penny's `*validate` equivalent on any prompt:

- [ ] Every `{{placeholder}}` has a corresponding schema property
- [ ] Every required schema property appears in the template (at least once)
- [ ] No `{{#if}}` block is used for a required field (required fields are always present)
- [ ] `additionalProperties` is `false` on the root schema
- [ ] `type` is specified on every property (no implicit `any`)
- [ ] Enum constraints used where domain is finite (e.g. `status`, `tier`, `severity`)
- [ ] `model_tier` field present if the template is model-tier-sensitive (cost routing concern)

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| penny/*generate-schema + *validate (poem-os) | 4-step schema workflow, validation alignment check, severity levels | POEM-specific path resolution |
| ecc:cost-aware-llm-pipeline | model_tier + token budget as schema fields, cost routing at design time | promptfoo and cost tracking infra |
| ecc:type-design-analyzer | Invariant expression discipline applied to placeholder naming | TypeScript type system specifics |
| ecc:code-architect | Consistency-first: scan existing schemas before designing new ones | Codebase feature architecture |

## Gap closed?

**PARTIAL — enforcement gap.**

David's POEM OS has Penny with `*generate-schema` but this only runs within the POEM OS workspace. The gap: no lightweight, standalone schema-design capability usable when working with prompts outside the POEM context (ad-hoc prompts, skill descriptions, CLAUDE.md system prompts). The `additionalProperties: false` discipline and the `model_tier` field are both gaps even within the existing Penny workflow — they are not currently standard POEM schema outputs.

## Connection to other sub-clusters

- **Template-author** (`prompt-engineering-template-author.md`): schema design is step 1 of template authoring (schema-first principle). These two distillations form a sequence: design-schema → author-template → eval-driven loop.
- **Eval-driven** (`prompt-engineering-eval-driven.md`): the trigger contract YAML is itself a schema-typed artifact. The same schema-design discipline that governs prompt data contracts governs eval contract authoring — positive/negative/pressure scenarios are typed test objects.

---

*Distillation pass: Phase 5 catalog:distill — prompt-engineering cluster*
