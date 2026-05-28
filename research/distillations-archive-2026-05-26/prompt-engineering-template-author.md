---
distillation_id: prompt-engineering-template-author
cluster: prompt-engineering
sub_cluster: template-author
intent: "Author a new prompt with schema, Handlebars template, and mock data in one structured workflow — Penny's *new mode generalised"
created: 2026-05-17
status: draft
source_artifacts:
  - appydave:skill:poem-slides
  - appydave:skill:spec-writer
  - everything-claude-code:skill:prompt-optimizer
  - everything-claude-code:agent:gan-planner
  - everything-claude-code:agent:code-architect
  - everything-claude-code:agent:planner
winner_mechanism: appydave/penny-prompt-engineer (poem-os)
---

# Unified Skill: prompt-template-author

**Purpose**: Author a net-new prompt as a Handlebars template + JSON schema + mock data set, following POEM principles — Penny's `*new` workflow generalised to any prompt context.

**For Agents**: Use when David says "write me a prompt", "create a new prompt", "new prompt for X", "build a prompt template", "I need a Handlebars template for", or is starting a new POEM-compatible workflow from scratch.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Turn a stated purpose into a production-ready prompt artifact: Handlebars template with placeholder schema, JSON schema for validation, and at least two mock data scenarios (happy path + edge case). One structured workflow, no ad-hoc authoring.

## Winner's Mechanism

`appydave/penny-prompt-engineer` (POEM OS) wins because it is the only artifact in the corpus that treats prompt authoring as a 4-step workflow with formal outputs: template file, schema file, mock data, validation report. ECC's `prompt-optimizer` is advisory only (never executes the task); ECC's `gan-planner` expands prompts into product specs, not Handlebars templates. Penny's `*new` mode is the closest thing to a template-authoring engine in the catalog.

The mechanism:
1. Gather purpose + placeholder requirements
2. Draft Handlebars template in `/poem/prompts/<name>.hbs`
3. Generate matching JSON schema in `/poem/schemas/<name>.json` — schema is always co-authored with the template, never added later
4. Generate mock data for at least two scenarios; render template to validate no broken placeholder references

## Non-overlapping ideas folded in

- From `everything-claude-code:skill:prompt-optimizer`: treat the description field as an optimizable parameter, not documentation — after drafting the template, apply the WHAT + WHEN + KEYWORDS + NEGATIVE TRIGGERS formula to write the discovery metadata block alongside it. The template and its routing description are one unit.
- From `everything-claude-code:agent:gan-planner`: before writing the template body, expand the one-line purpose into evaluation criteria — what must this prompt produce to be considered correct? The criteria feed the schema constraints and become the first eval-contract entries.
- From `everything-claude-code:agent:code-architect`: build-order discipline — define the data contract (schema) before writing the template body. Same principle as interface-before-implementation. Schema-first prevents placeholder drift.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| penny/*new (poem-os) | 4-step workflow: gather → template → schema → mock+validate | POEM-specific path resolution (`packages/poem-core/` vs `.poem-core/`) |
| ecc:prompt-optimizer | WHAT+WHEN+KEYWORDS+NEGATIVE formula for description field | Advisory-only stance (optimizer refuses to author, only advises) |
| ecc:gan-planner | Evaluation criteria before implementation | Sprint/product-spec framing (not needed for single prompt) |
| ecc:code-architect | Schema-first / data-contract-before-body discipline | Codebase-specific architecture analysis |

## Gap closed?

**YES — schema-first discipline.** David's existing `spec-writer` skill generates specs but does not enforce schema-alongside-template. POEM's penny agent does enforce it, but only within the POEM OS workspace. The gap: no lightweight skill that can be invoked *outside* the POEM OS context to author any prompt with schema in one pass.

## Adoption note

David's canonical Penny is at `prompt.supportsignal.com.au/.claude/commands/poem/agents/penny.md`. That persona handles the full POEM authoring workflow when inside the POEM OS workspace. This distillation generalises the `*new` mechanism for invocation without the POEM OS present — the skill synthesises Penny's authoring workflow + ECC's description-as-optimizable-parameter insight into a standalone capability.

---

*Distillation pass: Phase 5 catalog:distill — prompt-engineering cluster*
