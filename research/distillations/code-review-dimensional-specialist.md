---
distillation_id: code-review-dimensional-specialist
stage: audit
intent: "Single-axis specialist reviewer — one concern, one finding format, one verdict — composable into any fan-out orchestrator"
created: 2026-05-16
status: draft
source_artifacts:
  - compound-engineering:agent:ce-correctness-reviewer
  - compound-engineering:agent:ce-maintainability-reviewer
  - compound-engineering:agent:ce-performance-reviewer
  - compound-engineering:agent:ce-reliability-reviewer
  - compound-engineering:agent:ce-testing-reviewer
  - compound-engineering:agent:ce-api-contract-reviewer
  - compound-engineering:agent:ce-adversarial-reviewer
  - compound-engineering:agent:ce-scope-guardian-reviewer
  - compound-engineering:agent:ce-product-lens-reviewer
  - compound-engineering:agent:ce-data-migrations-reviewer
  - compound-engineering:agent:ce-schema-drift-detector
  - compound-engineering:agent:ce-previous-comments-reviewer
  - compound-engineering:agent:ce-pattern-recognition-specialist
  - appydave-plugins:skill:review-blind-hunter
  - appydave-plugins:skill:review-edge-case-hunter
  - appydave-plugins:skill:review-acceptance-auditor
  - appydave-plugins:skill:review-architecture
  - appydave-plugins:skill:review-code-quality
  - appydave-plugins:skill:review-unit-tests
  - bmad-method:skill:bmad-review-adversarial-general
  - bmad-method:skill:bmad-review-edge-case-hunter
  - everything-claude-code:agent:silent-failure-hunter
  - compound-knowledge:agent:strategic-alignment-reviewer
  - compound-knowledge:agent:data-accuracy-reviewer
winner_mechanism: compound-engineering:agent:ce-adversarial-reviewer
---

# Unified Skill: code-review-dimensional-specialist

**Purpose**: Pattern for building single-axis specialist reviewers that are composable into any fan-out orchestrator. The `ce-adversarial-reviewer` is the winner mechanism — it has the most rigorous single-axis design. David's six existing specialists already implement this pattern; this distillation captures the architecture so new dimensions can be built consistently.

**For Agents**: Use this as the **reference implementation** when David asks to build a new specialist dimension for `delivery-review` (e.g., "add a performance reviewer dimension", "build a data migrations reviewer", "create an API contract dimension"). Also use to evaluate whether an existing specialist needs hardening.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

## Intent

Define the canonical structure for a single-axis specialist reviewer: depth-calibrated scope, focused hunt list, anchored confidence rubric, explicit "what you don't flag" section, and structured JSON or normalized finding output — no scope creep into other dimensions.

## Winner's Mechanism

`compound-engineering:agent:ce-adversarial-reviewer` wins. It has the most complete single-axis specialist design in the corpus:

1. **Depth calibration** — three tiers (Quick / Standard / Deep) based on diff size and risk signals, with explicit thresholds (50 lines, 200 lines) and conditional technique activation. David's existing specialists lack this — they do the same analysis regardless of diff size.
2. **Technique taxonomy** — four distinct adversarial techniques (assumption violation, composition failures, cascade construction, abuse cases) with concrete examples per technique. No overlap with other reviewers.
3. **Explicit non-overlap** — "What you don't flag" section that names which *other* reviewers own adjacent territory. This is the anti-pattern killer: prevents specialists from drifting into each other's lane.
4. **Anchored confidence rubric** — four anchor points (100/75/50/suppress) with persona-specific examples at each level. The 25-or-below suppress rule eliminates speculative findings at the source.

David's `review-blind-hunter` (BMAD-derived) and `review-edge-case-hunter` have strong single-axis focus but lack depth calibration and the anchored confidence rubric. CE's approach is the upgrade path.

## Non-overlapping ideas folded in

- From `appydave-plugins:review-blind-hunter`: "If fewer than 3 findings, re-examine before concluding" rule — prevents lazy PASS on small diffs. Good calibration heuristic to add to depth Quick tier.
- From `appydave-plugins:review-edge-case-hunter`: Three-step validate-completeness pass (Step 3) after initial finding collection — forces a second scan before reporting. Simple and effective.
- From `everything-claude-code:agent:silent-failure-hunter`: "Zero tolerance" framing for swallowed errors — a specialist in error propagation that is a gap in David's current 6 dimensions (reliability/error-handling is not a current dimension). Candidate for a new dimension.
- From `compound-engineering:agent:ce-scope-guardian-reviewer`: Document-type adaptation (adjusts review depth based on whether the input is a requirements doc vs an implementation plan) — valuable for the acceptance auditor dimension.
- From `compound-knowledge:agent:strategic-alignment-reviewer`: Knowledge-domain review applying same pattern to non-code artifacts — confirms the specialist pattern is scope-agnostic.

## Canonical single-axis specialist structure

Every specialist reviewer should have:

```
---
name: review-{axis}
description: Single-axis specialist reviewer. [What it hunts]. Designed to run as one dimension in delivery-review or standalone.
---

# {Axis} Review

**Dimension code:** {2-char code}
**Axis territory:** [precise boundary — what this reviewer catches that others don't]

## What you don't flag
[Named list of adjacent territory owned by sibling reviewers]

## Depth calibration

**Quick** (< 50 changed lines, no risk signals): [what to check]
**Standard** (50-199 lines, minor risk signals): [what to check]
**Deep** (200+ lines OR {axis-specific risk signals}): [what to check, techniques activated]

## Execution

### Step 1: Scope
[How to load scope — identical across all specialists]

### Step 2: {Axis} Analysis
[Axis-specific hunt list with concrete examples per category]

### Step 3: Validate completeness
Revisit every category from Step 2. Add newly found unhandled items. Discard confirmed-handled ones.

### Step 4: Findings
[Normalized delivery review finding format with DIM-XX-NNN IDs]

## Confidence rubric
Anchor 100: [axis-specific mechanical certainty example]
Anchor 75: [full traceable path example]
Anchor 50: [partial evidence example — surface only as P0 or soft bucket]
Anchor 25 or below: suppress

## Halt conditions
- HALT if scope is empty or unreadable
```

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| ce-adversarial-reviewer | Depth calibration 3-tier, technique taxonomy, explicit non-overlap section, anchored confidence rubric | Ruflo JSON output format (use David's normalized DVR format) |
| review-blind-hunter | "< 3 findings re-examine" heuristic, adversarial posture language | BMAD-specific framing |
| review-edge-case-hunter | Three-step validate completeness pass, scope rules for diff vs full-file | n/a — all kept |
| ce-correctness-reviewer | Correctness hunt list (null propagation, race conditions, state transitions, error propagation) | CE-specific confidence anchor examples |
| ce-maintainability-reviewer | Maintainability hunt list (premature abstraction, unnecessary indirection, dead code) | CE-specific confidence examples |
| ce-performance-reviewer | "Higher effective threshold" calibration (performance false positives waste engineering time) | CE agent JSON output format |
| ce-testing-reviewer | Testing gaps hunt list (untested branches, false confidence tests, brittle tests, behavioral changes with no test additions) | CE agent JSON output format |
| ce-reliability-reviewer | Reliability hunt list (missing error handling on I/O, retry without backoff, missing timeouts, error swallowing) | CE agent JSON output format |
| silent-failure-hunter (ecc) | Zero-tolerance framing for silent failures — candidate for a new "reliability" dimension | ECC-specific injection resistance preamble |
| strategic-alignment-reviewer | Confirms pattern applies to non-code review scopes | Knowledge-domain specifics |

## Open questions for David

- Should `delivery-review` grow a **7th dimension**: reliability/error-handling? `silent-failure-hunter` from ECC and `ce-reliability-reviewer` from CE both cover this axis — David's current 6 don't. It's a genuine gap.
- Should depth calibration (Quick / Standard / Deep) be retrofitted to David's existing 6 specialists, or only applied to new ones? Retrofitting would make small diff reviews faster and reduce noise.
- `ce-data-migrations-reviewer` and `ce-schema-drift-detector` are highly specialized (Rails schema.rb + migrations). Is there a generic "data migrations" dimension worth adding to David's stack, or is this too stack-specific?
- Should the anchored confidence rubric (100/75/50/suppress) replace David's current PASS/CONDITIONAL PASS/FAIL per-dimension verdict? The rubric is more precise but requires updating all 6 existing specialists.
