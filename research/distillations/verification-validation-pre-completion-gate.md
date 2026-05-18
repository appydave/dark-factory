---
distillation_id: verification-validation-pre-completion-gate
stage: verification
intent: "Block success claims until fresh evidence exists — evidence before assertions, always"
created: 2026-05-17
status: draft
source_artifacts:
  - superpowers:skill:verification-before-completion
  - superpowers:skill:finishing-a-development-branch
  - gsd:agent:gsd-verifier
  - gsd:command:verify-work
  - gsd:command:validate-phase
  - everything-claude-code:skill:verification-loop
  - everything-claude-code:command:quality-gate
  - gstack:skill:careful
winner_mechanism: superpowers:skill:verification-before-completion
---

# Unified Skill: verification-validation-pre-completion-gate

**Purpose**: Block any completion claim, satisfaction expression, or "done" statement until fresh verification evidence has been gathered in the current session. Distinct from code review (quality judgment) — this is about evidence discipline.

**For Agents**: Use when about to claim work is complete, fixed, passing, or ready. Also fires before committing, creating PRs, or moving to the next task. NOT a review of quality — it is a gate that enforces "run the command, read the output, THEN claim the result."

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Enforce the invariant that no success claim is made without fresh, in-session verification evidence. The failure mode being prevented: agents (and humans) claiming completion based on memory, prior runs, or "it should work now" — without running the verification command in this session.

## Winner's Mechanism

`superpowers:skill:verification-before-completion` wins. It is the only skill in the corpus with:

1. **An Iron Law** — "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE" — as an unconditional behavioral constraint, not a checklist
2. **A Gate Function** with a named 5-step sequence: IDENTIFY → RUN → READ → VERIFY → CLAIM. Skipping any step is explicitly called "lying, not verifying"
3. **A Rationalizations table** with 8 empirically-observed excuses and explicit rebuttals. These are production-tested anti-rationalization barriers, not documentation
4. **Red Flags list** — specific surface forms of success-claiming language that trigger the gate ("should", "probably", "seems to", "Great!", "Done!", "Perfect!" before verification ran)
5. **A Common Failures table** — maps claim types to required evidence. "Tests pass" requires test command output showing 0 failures, not "previous run" or "should pass"

The Superpowers mechanism is uniquely precise because it was built from 24 documented failure memories — "your human partner said 'I don't believe you'" is a specific incident, not a hypothetical.

## Existing-skill nesting

David's stack has `delivery-review` as the finished-artifact gate. The pre-completion gate is complementary and distinct:

- **Existing mechanism** (`delivery-review`): Fan-out orchestrator that dispatches 6+ specialist reviewers against a finished diff or PR, producing a multi-dimensional quality verdict. Fires at merge-gate time. Per-PR grain.
- **New mechanism's grain**: Per-task / per-completion-claim. Fires every time an agent is about to say "done", "fixed", "passing", or similar. Minimal overhead — just "run the command, read the output."
- **Existing mechanism's grain**: Per-PR / per-delivery event.
- **Nesting rule**: The pre-completion gate fires inside each task before any "done" signal exits to the orchestrator. `delivery-review` fires at the PR boundary after all tasks are complete. Both compose — neither replaces the other. A task that passes the pre-completion gate can still fail `delivery-review` on quality grounds; a task that skips the pre-completion gate is an evidence problem, not a quality problem.

## Non-overlapping ideas folded in

- From `superpowers:skill:finishing-a-development-branch`: **Environment-aware completion menu** — detect whether working in a normal repo, named-branch worktree, or detached-HEAD worktree, then present exactly 4 (or 3) structured options rather than open-ended "what now". This prevents the open-ended "what should I do next?" anti-pattern after verification passes. — `complexity: low | optional: true | prerequisite: "working on a feature branch that needs integration"`

- From `gsd:agent:gsd-verifier`: **Goal-backward verification** — distinguish between "task completed" (a file was created) and "goal achieved" (the feature actually works). Specifically: exists (Level 1) → substantive non-stub (Level 2) → wired to callers (Level 3) → data actually flows (Level 4). The stub-detection patterns (empty returns, placeholder components, hardcoded empty props) are the most operationally useful addition. — `complexity: medium | optional: false | prerequisite: "none"`. This idea directly prevents the "component exists but shows nothing" failure mode.

- From `everything-claude-code:skill:verification-loop`: **Verification loop with retry limit** — structured retry when verification fails (fix → re-verify → fix → re-verify, max N cycles). Prevents infinite fix loops by making the loop explicit and bounded. — `complexity: low | optional: true | prerequisite: "automated test suite exists"`

- From `gstack:skill:careful`: **Risky operation checklist** — before irreversible operations (deletes, migrations, production pushes), explicitly enumerate what is irreversible and require acknowledgment. Complements the verification gate with a "pause before destructive action" pattern. — `complexity: low | optional: true | prerequisite: "operation involves data deletion, migration, or production change"`

## The core distinction from code-review

Code review asks: "Is this good?" The pre-completion gate asks: "Did you actually verify it runs?" These are orthogonal. A PR can pass the pre-completion gate (all tests ran, exit 0) while failing code review (logic is wrong but tests don't cover the edge case). The pre-completion gate addresses the honesty failure mode; code review addresses the quality failure mode.

David's existing `delivery-review` handles quality. The gap is honesty enforcement — nothing in David's current stack prevents an agent from claiming "tests pass" without having run them in the current session.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| verification-before-completion (superpowers) | Iron Law, Gate Function 5-step, Rationalizations table, Red Flags list, Common Failures table, 24-incident framing | Platform-specific behavior shaping details |
| finishing-a-development-branch (superpowers) | Environment detection (normal/worktree/detached-HEAD), 4-option menu structure, worktree ownership check | Full git worktree cleanup procedures (too operational for this distillation) |
| gsd-verifier | Goal-backward framing, 4-level artifact verification (exists/substantive/wired/data-flows), stub-detection patterns, wiring red flags | GSD-specific tooling (gsd-tools.cjs calls), VERIFICATION.md file format |
| verification-loop (ecc) | Bounded retry loop concept | ECC-specific tooling |
| careful (gstack) | Risky operation acknowledgment pattern | GStack-specific operation catalog |

## Draft SKILL.md frontmatter

```yaml
name: verify-before-claiming
description: >
  Enforce evidence before any completion claim, success assertion, or "done" statement.
  Gate function: IDENTIFY what command proves the claim → RUN it fresh → READ full output → VERIFY → ONLY THEN claim.
  Skipping any step is lying, not verifying.
  Use BEFORE: claiming tests pass, saying "fixed", committing, creating PRs, moving to next task.
  Use when: about to say "done", "working", "passing", "fixed", "complete", "should be good".
  NOT a quality review — that's delivery-review. This is evidence discipline.
allowed-tools: Bash(npm test:*), Bash(cargo test:*), Bash(pytest:*), Bash(go test:*), Bash(git diff:*), Bash(git status:*), Read
```

## Open questions for David

- Should this skill be implemented as a **hook** rather than an invokable skill? The Superpowers implementation fires the gate automatically before any "done" signal rather than waiting for invocation. A `PreToolUse` hook on commit/push commands would enforce this unconditionally — closer to the Iron Law spirit.
- The `finishing-a-development-branch` structured-options menu: is this the right grain for David's stack, or does the existing `push` skill already cover this?
- Should the 4-level artifact verification (exists/substantive/wired/data-flows) from `gsd-verifier` be part of this unified skill or a separate "stub detection" specialist? It's high-value but adds scope.
