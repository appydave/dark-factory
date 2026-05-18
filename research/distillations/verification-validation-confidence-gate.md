---
distillation_id: verification-validation-confidence-gate
stage: verification
intent: "Epistemic gate — honestly surface what you know and don't know before committing to a plan or execution path"
created: 2026-05-17
status: draft
source_artifacts:
  - compound-knowledge:skill:kw-confidence
  - bmad-method:skill:bmad-checkpoint-preview
  - bmad-method:skill:bmad-correct-course
  - gstack:skill:careful
  - gstack:skill:health
  - gsd:command:health
  - compound-knowledge:agent:strategic-alignment-reviewer
winner_mechanism: compound-knowledge:skill:kw-confidence
---

# Unified Skill: verification-validation-confidence-gate

**Purpose**: Non-destructive epistemic interrupt that surfaces what the agent knows, what it doesn't know, and whether enough is known to proceed — in plain prose, not a number or checklist. Designed to fire mid-workflow without losing state.

**For Agents**: Use when David says "are you sure?", "do we know enough to proceed?", "confidence check", "gut-check this", "what might we be missing?". Also fires proactively before committing to irreversible plans. NOT a quality review of an artifact — it is an honest self-assessment of agent knowledge state.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Pause before committing to a course of action and honestly say what you know and don't know — the way a trusted colleague would, not an optimistic project manager. Surface gaps and decide whether to proceed, pause to gather more information, or restructure the plan.

The failure mode being prevented: confident action on shaky epistemic ground. The agent proceeds as if it knows the answer when it doesn't, carrying unverified assumptions forward until they cause failures.

## Winner's Mechanism

`compound-knowledge:skill:kw-confidence` wins. It is the only skill in the cluster built specifically as an **epistemic interrupt** rather than a quality gate on an artifact. Key mechanism:

1. **No numbers, no scales** — prose assessment only. "87% confident" is theater; "I've read the files and the approach matches established patterns — no gaps I can identify" is honest.
2. **Four assessment areas** — task understanding, information sufficiency, approach certainty, risk awareness. Assessed independently to prevent confidence in one area masking uncertainty in another.
3. **Three recommendation paths** — "Proceed", "Proceed, but [caveat]", "Pause for [specific thing]". Forces a concrete decision, not hedged non-commitment.
4. **Specific "increase confidence" ranked list** — if gaps exist, produce actionable steps ranked by impact. "Read `data/q4-results.csv` to confirm the $50K benchmark" not "gather more data." Distinguishes what Claude can do autonomously vs what needs user input.
5. **Non-destructive interrupt with re-anchor** — "Resuming `/kw:work` at Task 3." The confidence check doesn't restart the parent workflow; it pauses and resumes precisely.

The `kw:confidence` distinction from `/kw:review` is load-bearing: confidence assesses *your epistemic state*, review assesses *an artifact*. They are complementary but different. David's stack has review-oriented skills; the epistemic gate is absent.

## Distinction from doubt-driven-development

`code-review-doubt-driven` (already distilled) and this confidence gate solve related but different problems:

| Skill | Problem | Mechanism | When |
|-------|---------|-----------|------|
| `doubt-driven` | Accumulated-context problem — reviewer shares implementer's assumptions | Spawn fresh-context reviewer biased to disprove | Before committing irreversible changes; for non-trivial decisions |
| `confidence-gate` | Epistemic groundlessness — agent proceeds without knowing if it knows enough | Honest self-assessment, no fresh context needed | Before any plan commitment; mid-workflow; after research |

`doubt-driven` requires a second agent context; the confidence gate is a self-assessment. They are complementary: confidence gate first (do I know enough?), then doubt-driven if the decision passes that test (is my reasoning sound?).

## Non-overlapping ideas folded in

- From `bmad-method:skill:bmad-checkpoint-preview`: **Mid-execution state check** — at phase boundaries, verify the current implementation trajectory still tracks the original spec and hasn't drifted. Distinct from the confidence gate (which is epistemic) — this is a drift-detection checkpoint. Fold in as an optional "checkpoint variant" of the confidence gate that compares current state to plan rather than assessing agent knowledge. — `complexity: medium | optional: true | prerequisite: "mid-implementation, not beginning of session"`

- From `bmad-method:skill:bmad-correct-course`: **Course correction mechanism** — when the confidence gate surfaces significant gaps or drift, the correct-course skill provides a structured path to update the plan rather than abandon it. Complements the confidence gate's "Pause for X" recommendation path with a concrete next action. — `complexity: medium | optional: true | prerequisite: "gap identified requires plan revision"`

- From `gstack:skill:health`: **System-level confidence scan** — when confidence is assessed about a system's current state (not a plan), the health skill pattern provides a structured scan of observable signals. Useful for "are we OK to deploy?" vs "do I know enough to plan?". — `complexity: low | optional: true | prerequisite: "assessing readiness of a running system"`

## Proportionality rule (from winner mechanism)

The confidence gate is deliberately lightweight when confidence is high. "High confidence. Task is clear, I've read the relevant files, the approach matches established patterns. No gaps I can identify. Ready to proceed." — two sentences is sufficient. The skill must not become a wall of text that adds friction to routine work. The three-path recommendation forces a concrete decision rather than hedging.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| kw:confidence (compound-knowledge) | No-numbers prose assessment, four independent areas, three recommendation paths, specific "increase confidence" ranked list, non-destructive interrupt + re-anchor pattern, proportionality rule | Every Inc. Proof integration, pipeline mode boilerplate |
| bmad:checkpoint-preview | Mid-execution drift detection variant | BMAD workflow orchestration context |
| bmad:correct-course | Plan revision mechanism after gap identified | BMAD story lifecycle |
| gstack:health | System-level confidence scan variant | GStack-specific health dimensions |

## Draft SKILL.md frontmatter

```yaml
name: confidence
description: >
  Honest epistemic self-assessment before proceeding — surface what you know, what you don't know,
  and whether it's safe to proceed. Produces prose assessment (never numbers/percentages),
  one of three concrete recommendations (Proceed / Proceed-with-caveat / Pause-for-X), and
  a ranked actionable list to close gaps if needed. Non-destructive: resumes exactly where
  the workflow left off after assessment.
  Use when: "are you sure?", "do we know enough?", "confidence check", "gut-check this",
  "what might we be missing?", before committing to an irreversible plan.
  NOT a quality review of an artifact — use delivery-review for that.
```

## Open questions for David

- Should the `checkpoint` variant (mid-execution drift detection) be part of this unified skill or a separate `checkpoint` skill? The compound-knowledge framing ("epistemic state") and BMAD framing ("trajectory vs plan") are different enough that they might warrant separate triggers.
- The confidence gate currently has no hook-based auto-invocation. Should it fire automatically before certain high-stakes operations — e.g., before spawning any autonomous subagent run? This would mirror how Superpowers' `verification-before-completion` fires before any completion claim.
- David currently has no equivalent to this skill. Is the priority high enough to build it before the other gaps (pre-completion-gate, data-deploy-gate) given that those gaps cause more observable failures?
