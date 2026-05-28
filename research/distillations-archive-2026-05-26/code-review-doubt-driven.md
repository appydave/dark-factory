---
distillation_id: code-review-doubt-driven
stage: audit
intent: "In-flight adversarial self-review for non-trivial decisions — spawn a fresh-context reviewer to disprove before the claim stands"
created: 2026-05-16
status: draft
source_artifacts:
  - agent-skills-osmani:skill:doubt-driven-development
  - compound-engineering:agent:ce-adversarial-reviewer
  - bmad-method:skill:bmad-review-adversarial-general
  - ruflo:agent:witness-auditor
  - everything-claude-code:agent:silent-failure-hunter
  - gstack:skill:health
winner_mechanism: agent-skills-osmani:skill:doubt-driven-development
---

# Unified Skill: code-review-doubt-driven

**Purpose**: In-flight adversarial self-review posture for non-trivial decisions. Distinct from `delivery-review` (finished artifact gate) — this is a **mid-work discipline** for surfacing correctness risks while course-correction is cheap. Spawns a fresh-context reviewer biased to disprove.

**For Agents**: Use when David says "check my reasoning", "is this thread-safe?", "am I missing something?", "verify this assumption", "adversarial review this claim". Also use proactively when about to commit irreversible changes (migrations, public API changes, production deploys). NOT a replacement for `delivery-review` at merge time.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

## Intent

Surface a fresh-context reviewer that is explicitly biased to **disprove** the current claim or implementation, catching errors while the cost of correction is low — before they compound into the next task.

## Winner's Mechanism

`agent-skills-osmani:skill:doubt-driven-development` wins. It is the only skill in the corpus that explicitly solves the **accumulated-context problem** — long sessions build up assumptions that quietly harden into "facts". The mechanism:

1. **CLAIM** — Surface the decision as a compact named claim ("this caching layer is thread-safe under...") and state why it matters. Forces clarity before scrutiny.
2. **EXTRACT** — Isolate the smallest reviewable artifact + contract, stripping the reasoning journey. Fresh-context reviewer needs the what, not the how-we-got-here.
3. **DOUBT** — Spawn a fresh-context reviewer with an adversarial prompt (biased to disprove, not approve).
4. **RECONCILE** — Classify every finding against the artifact text. Not every finding is valid — reviewer may not have full context.
5. **STOP** — Explicit stop conditions: trivial findings, 3 cycles, or user override. Prevents infinite doubt loops.

The **decision taxonomy** (non-trivial when: branching logic, cross-boundary, unverifiable property, irreversibility, blast radius) is precise enough to make the skill self-limiting. If the change is trivial by the taxonomy, skip the skill.

## Non-overlapping ideas folded in

- From `compound-engineering:agent:ce-adversarial-reviewer`: **Cascade construction** technique — multi-step failure chain tracing (A times out → B retries → overwhelms A → worse). This is the adversarial technique most likely to surface issues invisible to single-step analysis. Add as an optional technique in the DOUBT step.
- From `bmad-method:skill:bmad-review-adversarial-general`: Cynical posture language — "zero patience for sloppy work", "look for what is missing, not just what is wrong" — complements Osmani's more analytical framing. Useful for the DOUBT reviewer prompt.
- From `ruflo:agent:witness-auditor`: **Witness pattern** — a persistent auditor that tracks claimed fixes over time and verifies they were actually implemented. Different concern (post-fix verification) but adjacent: after RECONCILE, the witness-auditor could confirm that the fix applied actually addresses the claim.
- From `gstack:skill:health`: Project health check as a structured adversarial scan of the whole system state — confirms the CLAIM → DOUBT cycle is generalizable beyond individual decisions to system-level health queries.

## The accumulated-context problem (why this skill exists)

Standard review (`delivery-review`) reviews a finished artifact against quality criteria. Doubt-driven development catches a different failure mode: the reviewer and the implementer are the same session, carrying the same assumptions.

Key invariant from Osmani's skill: **the fresh-context reviewer must not receive the reasoning journey, only the artifact and contract**. This is the mechanism that makes the review genuinely independent. David's current stack has no skill that enforces this separation.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| doubt-driven-development (osmani) | Full 5-step process, decision taxonomy, stop conditions, accumulated-context framing, loading constraints | Platform-specific degraded-fallback details |
| ce-adversarial-reviewer | Cascade construction technique, depth calibration 3-tier, abuse cases technique | CE JSON output format (not needed for self-review cycle) |
| bmad-review-adversarial-general | Cynical posture language for DOUBT reviewer prompt | BMAD-specific execution context |
| witness-auditor (ruflo) | Witness-pattern concept for post-RECONCILE verification | Ruflo infrastructure dependency |
| health (gstack) | System-level adversarial scan confirms pattern generalizability | GStack-specific health dimensions |

## Draft SKILL.md frontmatter

```yaml
name: doubt-driven
description: >
  In-flight adversarial review for non-trivial decisions — spawn a fresh-context reviewer biased
  to disprove before the claim stands. Five steps: CLAIM → EXTRACT → DOUBT → RECONCILE → STOP.
  Use BEFORE committing irreversible changes, BEFORE asserting a non-obvious property
  (thread-safe, idempotent, matches spec), WHEN stuck and need a fresh perspective.
  NOT for finished-artifact gate reviews — use delivery-review for that.
  Use when: "check my reasoning", "is this safe?", "verify this claim", "adversarial review",
  "am I missing something?", "sanity check before I commit".
```

## Decision taxonomy (when to invoke)

A decision is non-trivial when at least one is true:
- Introduces or modifies branching logic
- Crosses a module or service boundary
- Asserts a property the type system cannot verify (thread safety, idempotence, ordering)
- Correctness depends on context the future reader cannot see
- Blast radius is irreversible (production deploy, data migration, public API change)

**Do NOT invoke for**: mechanical operations (renaming, formatting), unambiguous instructions, reading/summarizing existing code, one-line obvious-correctness changes.

## Open questions for David

- Should `doubt-driven` be proactively triggered by hooks at specific moments (pre-commit on files matching `*migration*`, `*auth*`, `*payment*`)? This would make the "irreversible/high-blast-radius" category automatic.
- Is the 3-cycle stop condition right? Three doubt-reconcile cycles is generous for a mid-session check. A lower limit (1-2) might be appropriate for faster cadence.
- Should `doubt-driven` and `delivery-review` be explicitly positioned in David's system as: doubt-driven = mid-task, delivery-review = merge gate? Documenting this as a workflow diagram in the agentic-os brain might prevent confusion.
