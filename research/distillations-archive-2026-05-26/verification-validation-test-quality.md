---
distillation_id: verification-validation-test-quality
stage: verification
intent: "Verify that tests are real, bounded, and actually verify what they claim — not stubs, not unconstrained, not test-shaped assertions"
created: 2026-05-17
status: draft
source_artifacts:
  - superpowers:skill:test-driven-development
  - spec-kit:command:selftest
  - spec-kit:extension:self-test.specify
  - gbrain:skill:testing
  - compound-engineering:skill:ce-test-browser
  - compound-engineering:skill:ce-test-xcode
  - everything-claude-code:skill:ai-regression-testing
  - everything-claude-code:command:quality-gate
  - ruflo:skill:agent-tdd-london-swarm
  - ruflo:skill:agent-test-long-runner
  - ruflo:skill:testgen
  - gsd:command:add-tests
  - gsd:agent:gsd-nyquist-auditor
winner_mechanism: superpowers:skill:test-driven-development
---

# Unified Skill: verification-validation-test-quality

**Purpose**: Verify that tests are substantive, bounded in feedback latency, and structured as RED-GREEN-REFACTOR cycles rather than assertions written after the fact. Distinct from "run the tests" — this is about whether the tests actually verify the behavior they claim to verify.

**For Agents**: Use when David says "add tests", "are these tests real?", "TDD this", "write tests for X", "is the test coverage meaningful?". Also fires when a task claims "tests pass" but no test was written first. NOT a test runner — this is about test quality and TDD discipline.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Catch two failure modes that pass superficial review:

1. **Stub tests** — tests that exist, run, and pass but don't actually verify the behavior. A test that always passes regardless of implementation is not a test.
2. **Post-hoc assertions** — tests written after implementation to match existing behavior, not to specify expected behavior. These tests don't catch regressions; they cement bugs.

## Winner's Mechanism

`superpowers:skill:test-driven-development` wins. It is the only skill in the corpus that treats TDD as a **behavioral discipline with an Iron Law**, not a technique:

1. **Iron Law** — "NO IMPLEMENTATION CODE WITHOUT A FAILING TEST FIRST." No exceptions, no "just this once." The rationalization prevention table (7 documented excuses + rebuttals) is built from real agent sessions.
2. **Regression test discipline** — the red-green-revert check: write test → run test (must FAIL) → implement → run test (must PASS). If you can't make the test fail by reverting the fix, the test doesn't verify the fix.
3. **Micro-cycle rule** — RED-GREEN-REFACTOR cycles must be ≤ 30 lines of code each. Larger cycles hide mistakes. This is precise enough to be a lint rule.
4. **Multi-harness test patterns** — the skill's tests are `.sh` + `.jsonl` session transcripts asserting that test code was written before implementation code appears in the diff. This verifies TDD discipline at the transcript level, not just at the code level.

The Superpowers TDD skill is empirically validated: 52 test files across 7 test suites, including tests that verify the skill itself triggers correctly in adversarial conditions ("skip-formalities.txt" prompts).

## Overlap with code-review cluster

There is moderate overlap: `everything-claude-code:skill:ai-regression-testing` and `gbrain:skill:testing` both appear in the code-review slice. The distinction:

- **Code-review cluster**: Reviews test quality as one dimension of a PR review. "Are these tests sufficient?"
- **This cluster**: Enforces TDD discipline *during* implementation — before the PR exists. "Did you write the test first?"

The code-review reviewer catches test quality post-implementation; the TDD skill enforces test-first during implementation. Both are needed; they fire at different points in the lifecycle.

## Non-overlapping ideas folded in

- From `gsd:agent:gsd-nyquist-auditor`: **Feedback latency constraint** — automated verification in tasks must have bounded latency. No full E2E suite per task, no watch mode, no > 30 second delays. Named the Nyquist principle: sample frequently enough to catch drift early. This prevents the common failure mode where "verification" means "run the full 10-minute test suite" rather than "run the 3-second targeted test." — `complexity: low | optional: false | prerequisite: "automated test suite exists"`. The 30-second threshold is concrete and enforceable.

- From `everything-claude-code:skill:ai-regression-testing`: **AI behavior regression tests** — structured approach to writing tests that verify agent/LLM behavior rather than deterministic code. Particularly relevant for David's agent-building work (skills, prompts). The failure mode: an agent's behavioral test passes because the prompt happens to work today, not because the test is actually checking the right thing. — `complexity: high | optional: true | prerequisite: "testing agent/LLM behavior rather than deterministic code"`

- From `spec-kit:extension:self-test.specify`: **Spec as a test spec** — the `self-test.specify` extension in spec-kit treats the spec itself as a test specification. Tests must be derivable from the spec's acceptance criteria, not from the implementation. This is the spec-kit's operationalization of "code serves specifications." — `complexity: medium | optional: true | prerequisite: "spec-kit workflow or equivalent spec artifact exists"`

- From `ruflo:skill:agent-tdd-london-swarm`: **London School TDD for agent systems** — mock-at-boundaries approach (mock external dependencies, test behavior via interactions, not state). Relevant for David's multi-agent work where agents communicate with each other. London TDD verifies that the agent sends the right messages, not just that it ends in the right state. — `complexity: high | optional: true | prerequisite: "testing multi-agent interactions"`

## The regression test discipline (load-bearing)

From `superpowers:skill:test-driven-development`, the regression test cycle is the highest-value idea in the cluster:

```
Write regression test → Run → MUST FAIL → Implement fix → Run → MUST PASS
```

If the test doesn't fail before the fix, the test doesn't verify the fix. This is the single most commonly skipped step in TDD. David's current stack has no explicit enforcement of this step.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| test-driven-development (superpowers) | Iron Law, RED-GREEN-REFACTOR cycle, 30-line micro-cycle rule, regression test discipline (red-green-revert), rationalization prevention table, multi-harness test pattern as verification approach | Superpowers-specific harness-comparison framing |
| gsd-nyquist-auditor | Feedback latency constraint, 30-second threshold, no-watch-mode rule, no-full-E2E-per-task rule, Nyquist framing | GSD-specific plan structure checking |
| ai-regression-testing (ecc) | AI behavior regression test concept | ECC-specific tooling |
| self-test.specify (spec-kit) | Spec-as-test-spec concept | spec-kit compile machinery |
| agent-tdd-london-swarm (ruflo) | London School TDD for agent interactions | Ruflo infrastructure dependencies |

## Draft SKILL.md frontmatter

```yaml
name: tdd-enforcer
description: >
  Enforce test-driven development discipline — NO implementation code without a failing test first.
  Verify that tests are real (RED-GREEN-REVERT cycle: test must fail before fix, pass after fix),
  bounded (≤30 second feedback latency, no full E2E suites per task), and micro-cycle scoped (≤30 LOC per RED-GREEN).
  Use when: "add tests", "TDD this", "write tests first", "are these tests real?",
  "is this test-driven?", any feature or bug fix task.
  NOT a test runner — this is about test quality and TDD discipline.
allowed-tools: Bash(npm test:*), Bash(cargo test:*), Bash(pytest:*), Bash(go test:*), Read, Edit, Write
```

## Open questions for David

- Should TDD enforcement be a **hook** on file creation events? If a `.ts` or `.rb` implementation file is created without a corresponding `.test.ts` or `_spec.rb` file in the same commit, fire the TDD enforcer. This would make the Iron Law automatic rather than invoked.
- The Nyquist 30-second threshold: is this appropriate for David's stack? SupportSignal uses Next.js + Convex — a targeted Convex query test is probably under 5 seconds; a full Playwright E2E is 2+ minutes. The threshold should be project-specific.
- The London School TDD for agents: is this the right time to establish this pattern? David is building more agents (Kybernesis). The failure mode (agent sends wrong messages but ends in correct state) will become more common. This could be a separate distillation — it's high complexity and only relevant when testing agent interactions.
