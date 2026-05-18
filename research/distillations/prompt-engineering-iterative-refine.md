---
distillation_id: prompt-engineering-iterative-refine
cluster: prompt-engineering
sub_cluster: prompt-refine
intent: "Iteratively improve an existing skill description or prompt template using a structured render → identify gap → revise → re-render loop — Penny's *refine mode generalised"
created: 2026-05-17
status: draft
source_artifacts:
  - appydave:skill:poem-slides
  - everything-claude-code:skill:prompt-optimizer
  - everything-claude-code:skill:skill-comply
  - everything-claude-code:agent:gan-generator
  - everything-claude-code:agent:refactor-cleaner
winner_mechanism: ecc:prompt-optimizer + penny/*refine (poem-os)
---

# Unified Skill: prompt-iterative-refiner

**Purpose**: Take an existing prompt template or skill description and improve it through a render-gap-revise loop — not rewriting from scratch, but making targeted improvements to precision, trigger specificity, placeholder coverage, or anti-rationalization coverage.

**For Agents**: Use when David says "improve this prompt", "refine this skill description", "make this skill trigger more reliably", "tighten this template", "the skill is triggering on the wrong things", "this prompt produces inconsistent output", or hands over a draft prompt for improvement.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Prompt refinement is different from prompt authoring. The artifact already exists and has known failure modes (wrong trigger rate, inconsistent output, placeholder gaps, rationalization bypasses). Refinement is a targeted surgery, not a full rewrite. Each iteration must be measurable — refinement without a re-render or eval check is guesswork.

## Winner's Mechanism

**ECC `prompt-optimizer`** (advisory only, never rewrites) + **Penny `*refine`** (structured 4-step loop):

### The render-gap-revise loop

```
1. LOAD: read existing template + schema + last eval run (if any)
2. RENDER: apply template to test data — at least two scenarios (happy path + edge case)
3. GAP ANALYSIS: identify the specific failure mode:
   - Wrong trigger rate → description field needs WHAT+WHEN+KEYWORDS+NEGATIVE precision adjustment
   - Placeholder drift → schema alignment check (see schema-design distillation)
   - Output inconsistency → rubric/instruction ambiguity in the template body
   - Rationalization bypass → anti-rationalization table needs new entries (see injection-resistance distillation)
4. TARGETED EDIT: change only the component that addresses the identified gap
5. RE-RENDER: verify the edit fixed the gap without introducing regression in other scenarios
```

The constraint: **only one change type per iteration**. Changing the description, the template body, and the schema simultaneously makes it impossible to isolate which change fixed the problem. ECC's `prompt-optimizer` enforces this as advisory-only — it diagnoses and recommends, but refuses to execute all changes at once.

### The WHAT+WHEN+KEYWORDS+NEGATIVE formula (applied to description refinement)

From `prompt-patterns` brain, applied during the description-field iteration:

```
WHAT: One sentence — what does this skill do?
WHEN: Trigger conditions — specific user phrases or context signals that should activate it
KEYWORDS: Comma-separated activation vocabulary (exact user phrases likely to appear)  
NEGATIVE: What should NOT trigger this skill (the most important, most often missing)
```

The NEGATIVE clause is the highest-leverage refinement target. Most description fields state what the skill does but not what it doesn't do — ambiguity on the boundary causes false positives.

## Non-overlapping ideas folded in

- From `everything-claude-code:skill:skill-comply`: after each refinement iteration, run skill-comply at 3 strictness levels (literal / paraphrase / edge). This surfaces whether the change improved compliance on strict phrasing but degraded it on paraphrased requests — a common regression introduced by over-precise descriptions. The compliance report is the re-render artifact.
- From `everything-claude-code:agent:gan-generator`: the Generator in the GAN harness iterates against evaluator feedback until quality threshold is met. The same structure applies to prompt refinement: each iteration has an acceptance criterion (pass@3 on trigger eval, or specific output rubric). Iteration stops when the criterion is met, not when it "looks good."
- From `everything-claude-code:agent:refactor-cleaner`: dead-code removal discipline applied to prompts — after refinement, audit for placeholder variables that no longer appear in the template body (orphaned schema properties), and instruction clauses that no longer have a matching output expectation. Prompt bloat degrades performance; refactoring removes it.

## Refinement decision tree

| Failure mode | Component to change | How to verify fix |
|-------------|---------------------|-------------------|
| Skill fires on wrong prompts (false positive) | Description: add NEGATIVE clause | Trigger eval — negative scenarios |
| Skill fails to fire on correct prompts (false negative) | Description: expand KEYWORDS or clarify WHEN | Trigger eval — positive scenarios |
| Output is inconsistent | Template body: add rubric anchors, remove ambiguous instructions | Output eval with llm-rubric |
| Skill bypassed by agent rationalization | Anti-rationalization table: add new entry | Pressure scenario test |
| Placeholder data arrives malformed | Schema: add constraints (minLength, enum, format) | Schema validation run |
| Template too long, token-heavy | Template body: strip dead clauses, compress instructions | Re-render token count + output quality delta |

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| ecc:prompt-optimizer | WHAT+WHEN+KEYWORDS+NEGATIVE formula, advisory-only stance, gap diagnosis before edit | Advisory-only constraint (refined version should make targeted edits) |
| penny/*refine (poem-os) | 4-step loop: load → render → gap → edit, re-validation after changes | POEM-specific path resolution, workspace-bound rendering |
| ecc:skill-comply | Post-iteration compliance check at 3 strictness levels | ECC harness tooling |
| ecc:gan-generator | Iterate until acceptance criterion met, not until it "looks good" | Full GAN product-spec loop |
| ecc:refactor-cleaner | Dead clause audit — remove what no longer serves the prompt | Code-specific dead-code tools |

## Gap closed?

**PARTIAL — iteration discipline gap.**

David has `appydave:improve` and `appydave:polish` skills for general improvement tasks. Neither applies specifically to prompt refinement with a render-eval loop. Penny's `*refine` does this within POEM OS but requires the POEM context. The gap: no skill that takes any existing prompt/description and runs the render-gap-revise loop as a standalone operation. The WHAT+WHEN+KEYWORDS+NEGATIVE formula is in the `prompt-patterns` brain but not in a skill that applies it mechanically to an existing description.

## Connection to other sub-clusters

- **Eval-driven** (`prompt-engineering-eval-driven.md`): refinement feeds into the eval loop when an existing skill is failing trigger or output evals. The failure mode from the eval run is the input to the refinement cycle.
- **Injection-resistance** (`prompt-engineering-injection-resistance.md`): if refinement reveals a rationalization bypass failure mode, the fix belongs in the anti-rationalization table (injection-resistance layer), not in the description field.
- **Schema-design** (`prompt-engineering-schema-design.md`): if refinement reveals placeholder drift, the schema-design workflow applies to audit and correct the data contract.

---

*Distillation pass: Phase 5 catalog:distill — prompt-engineering cluster*
