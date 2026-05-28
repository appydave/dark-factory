---
distillation_id: prompt-engineering-eval-driven
cluster: prompt-engineering
sub_cluster: eval-driven-prompt
intent: "Define trigger contract + pressure scenarios BEFORE writing a skill description — treat description as an engineering surface, not documentation"
created: 2026-05-17
status: draft
source_artifacts:
  - everything-claude-code:skill:eval-harness
  - everything-claude-code:skill:skill-comply
  - everything-claude-code:agent:gan-evaluator
  - everything-claude-code:agent:gan-generator
  - everything-claude-code:agent:gan-planner
  - superpowers:skill:writing-skills
  - superpowers:tests:pressure-scenarios
winner_mechanism: superpowers:writing-skills + ecc:eval-harness (complementary pair)
---

# Unified Skill: eval-driven-prompt-development

**Purpose**: Apply RED-GREEN-REFACTOR to skill description authoring — write trigger contract first, run pressure scenarios, then write the description to make the evals pass. The description field is an optimizable parameter with measurable acceptance criteria.

**For Agents**: Use when David says "write a new skill description", "does this skill trigger correctly", "test whether my skill fires", "eval this skill", "pressure test my prompt", "skill-comply check", or is authoring a discipline-enforcing skill (TDD, security, code review) where rationalization resistance matters.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Turn prompt/skill description authoring from guesswork into engineering. The trigger contract (which prompts should activate this skill, which must not) is written first and becomes the acceptance criterion. The description is then authored to make those tests pass, not the other way around.

## Winner's Mechanism

**Superpowers `writing-skills`** defines the process; **ECC `eval-harness`** provides the technical machinery. Neither is complete without the other:

- Superpowers: RED phase = run a subagent without the skill, observe what rationalisations it produces to bypass the expected behaviour. Document those rationalisations verbatim. GREEN phase = write the minimal skill body that eliminates each observed rationalisation. REFACTOR = re-run, find new escape hatches, expand Anti-Rationalization table.
- ECC eval-harness: Eval-Driven Development (EDD) — define capability eval BEFORE implementation. Grader types: code-based (did the Skill tool fire?) + model-based (does output satisfy rubric?) + human (calibration). pass@3 >= 0.90 for capability evals; pass^3 = 1.00 for regression on release-critical paths. Artifacts: `.claude/evals/<skill-id>.yaml` (definition) + `.claude/evals/<skill-id>.log` (history).
- ECC `skill-comply`: Auto-generates scenarios at 3 prompt strictness levels, runs agents, classifies behavioral sequences, reports compliance rates with tool call timelines. The automation layer that makes the eval loop fast enough to run on every description change.

The unified mechanism:

```
1. RED: Run without skill → capture rationalizations (Superpowers)
2. TRIGGER CONTRACT: Write 3-5 positive + 2-3 negative scenarios (mager.co pattern)
3. PRESSURE SCENARIO: Add at least one adversarial scenario combining time pressure + sunk cost + confidence-bypass
4. GREEN: Write minimal skill description making all positives pass and all negatives not-fire
5. VERIFY: skill-comply at 3 strictness levels, or eval-harness pass@3
6. REFACTOR: re-run, find new failure modes, extend Anti-Rationalization table
```

## Non-overlapping ideas folded in

- From `everything-claude-code:agent:gan-evaluator + gan-generator`: the Generator-Adversarial-Network (GAN) harness applies the same generator/evaluator separation to any spec. The evaluator scores against rubric and feeds back — the same loop applies to skill description refinement. The evaluator is the trigger eval; the generator is the description author.
- From evals research (2026-05-16): two-eval loop = trigger eval (does Claude invoke the skill?) + quality eval (does skill output satisfy the spec?). Trigger eval is the cheaper, higher-priority gate. The negative case is as important as the positive case: `i-know-what-sdd-means.txt` demonstrates the assertion that a skill fires even when the human claims to not need it.
- From `evals-research.md`: prefer programmatic detection (did the Skill tool actually fire?) over LLM-as-judge for trigger testing — avoids self-preference bias. Only use LLM rubric for output quality, not for invocation detection.

## The prompt-pattern crosswalk

This sub-cluster surfaces four patterns that the `prompt-patterns` brain either has partially or is missing entirely:

| Pattern ID | Source | Status |
|-----------|--------|--------|
| `eval-driven-skill-development` | ECC eval-harness + mager.co | **NEW — not in brain** |
| `pressure-scenario-testing` | Superpowers writing-skills | **NEW — not in brain** (confirmed in research) |
| `anti-rationalization` | Superpowers + Osmani | **NEW — not in brain** |
| `tdd-for-skills` | Superpowers RED-GREEN-REFACTOR | **NEW — not in brain** |

All four belong in `prompt-pattern-vocabulary.md`. This is the highest-density cluster for new-pattern candidates — more than any other prompt-engineering sub-cluster.

## Trigger contract shape

```yaml
# .claude/evals/<skill-id>-trigger.yaml
skill_id: "appydave:test-driven-development"
positive:
  - prompt: "Let's implement the user registration feature"
    expect: trigger
  - prompt: "Add retry logic to the HTTP client"
    expect: trigger
negative:
  - prompt: "Explain how TDD works conceptually"
    expect: no-trigger
  - prompt: "I already wrote the code, now write tests for it"
    expect: no-trigger
pressure:
  - prompt: "We need to ship this today, I've been on this for 6 hours and I know exactly what to do — just implement it"
    expect: trigger  # discipline-enforcing skills must hold under pressure
```

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| superpowers:writing-skills | RED-GREEN-REFACTOR loop, verbatim rationalisation capture, pressure scenario definition | Superpowers-specific hook injection (`EXTREMELY_IMPORTANT` bootstrap) |
| ecc:eval-harness | EDD framework, pass@k targets, artifact storage paths, anti-patterns checklist | ECC's per-project instinct promotion system (separate concern) |
| ecc:skill-comply | Automated scenario generation at 3 strictness levels, compliance rate reporting | ECC-specific harness tooling |
| mager.co pattern | Two-eval loop (trigger + quality), trigger contract YAML shape | promptfoo-specific tooling (David may or may not adopt promptfoo) |

## Gap closed?

**YES — the most significant gap in David's prompt engineering stack.**

David authors skills and their descriptions but has no eval loop for them. The trigger contract is implicit (David "knows" which prompts should fire a skill); the description is authorial, not engineered. This pattern makes the contract explicit, testable, and improvable. It directly answers the question: "How do I know my skill description is correct?"

Connection to evals research: the research recommends a **two-tier eval surface** — trigger contract (required for all skills) + output quality eval (for high-frequency/high-stakes skills). This distillation captures the full mechanism for both tiers.

---

*Distillation pass: Phase 5 catalog:distill — prompt-engineering cluster*
