---
distillation_id: delivery-readiness-pre-merge-gate
stage: delivery-readiness
intent: "Verify a specific change is safe to merge — quality, security, spec compliance, and deployment risk assessed before the PR lands"
created: 2026-05-17
status: draft
source_artifacts:
  - appydave-plugins:skill:delivery-review
  - agent-skills-osmani:command:ship
  - gsd:command:ship
  - gsd:command:secure-phase
  - gsd:command:audit-milestone
  - gsd:command:audit-uat
  - compound-engineering:agent:ce-deployment-verification-agent
  - everything-claude-code:skill:production-audit
  - superpowers:skill:finishing-a-development-branch
winner_mechanism: appydave-plugins:skill:delivery-review
---

# Unified Skill: Pre-Merge Gate

**Purpose**: Verify for Agents: Use when David asks "is this ready to ship?", "delivery review", "review before merge", "pre-merge check", "should I merge this?".

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

## Intent

Run a structured pre-merge gate on a specific change — verifying quality, spec compliance, architecture alignment, security, and deployment risk — and return a PASS / CONDITIONAL PASS / FAIL verdict before any code lands.

## Winner's Mechanism

`appydave-plugins:skill:delivery-review` wins because it is already in David's stack, already production-deployed, already orchestrates 6 specialist sub-agents in parallel (BH, EC, AA, AR, CQ, UT), already has normalized finding formats and triage rules, and already produces a structured verdict. No other artifact in this cluster comes close to this level of completeness. The mechanism is exactly right: fan-out to specialists → deduplicate → classify → synthesize verdict.

## Existing-skill nesting

- **Existing mechanism**: `delivery-review` is a diff-scoped parallel fan-out across 6 dimensions. It runs fast (per PR or per wave) and returns a binary/ternary verdict. Scoped to code changes, not deployment posture.
- **New mechanism's grain (deployment verification)**: per-deploy — triggered when a PR touches production data, migrations, auth surfaces, or public endpoints. Adds SQL verification queries, rollback procedures, and monitoring plans.
- **Existing mechanism's grain**: per-PR / per-wave — runs on the diff, not the deployed state.
- **Nesting rule**: `delivery-review` fires first as the standard pre-merge gate. `deployment-verification` fires conditionally inside `delivery-review` when the diff triggers deployment-risk signals (migrations, auth, public endpoints). The deployment checklist is an optional 7th dimension, not a replacement. David decides whether to auto-trigger or require explicit invocation.

## Non-overlapping ideas folded in

- From `compound-engineering:ce-deployment-verification-agent`: SQL verification queries + rollback procedure generation for data-touching PRs — `complexity: medium | optional: true | prerequisite: diff touches database migrations or schema changes`. The deployment checklist is executable, not just advisory — it generates queries you can actually run.
- From `superpowers:finishing-a-development-branch`: Hard-gate state machine — the skill verifies tests PASS before presenting options; if tests fail, it stops and does not present merge options — `complexity: low | optional: false | prerequisite: none`. Prevents the "skip the failing tests, I'll fix later" failure mode.
- From `gsd:secure-phase`: Retroactive threat-mitigation verification — confirms declared mitigations from PLAN.md are present in code before shipping — `complexity: medium | optional: true | prerequisite: phase has a PLAN.md with threat model section`. Critical for SupportSignal (NDIS compliance, PII, auth).
- From `gsd:audit-uat`: Cross-phase UAT scan — detects stale test documentation by cross-referencing UAT items against the live codebase — `complexity: low | optional: true | prerequisite: project uses GSD .planning/ structure`. Catches "the code changed but the test doc wasn't updated" quietly.
- From `agent-skills-osmani:ship`: Fan-out to named specialist personas (code-reviewer, security-auditor, test-engineer) before synthesizing — `complexity: low | optional: false | prerequisite: none`. Already implemented in delivery-review; confirms the pattern is correct, not a new addition.
- From `everything-claude-code:production-audit`: Local-evidence posture — reads from the repo, never sends data to an external service — `complexity: low | optional: false | prerequisite: none`. David's delivery-review already runs locally; this confirms the design constraint.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `appydave-plugins:delivery-review` | Full mechanism: 6-dimension parallel fan-out, normalized finding format, triage rules, verdict | Nothing set aside — this is the winner |
| `compound-engineering:ce-deployment-verification-agent` | SQL verification queries, rollback procedure generation | Ruflo-specific deploy hooks, webhook integrations |
| `superpowers:finishing-a-development-branch` | Hard-gate state machine (test-first), structured option presentation | Worktree detection, detached HEAD handling (not relevant to `delivery-review` orchestrator) |
| `gsd:secure-phase` | Threat-mitigation verification pattern (PLAN.md → code evidence) | `gsd-security-auditor` agent (uses GSD file structure — convert pattern, not agent) |
| `gsd:audit-uat` | Stale UAT documentation detection | GSD-specific `.planning/phases/` path conventions |
| `agent-skills-osmani:ship` | Named-persona fan-out confirmation | Anti-rationalization table framing (already in BH dimension) |
| `everything-claude-code:production-audit` | Local-evidence principle | External service integrations |
| `gsd:ship` | PR body auto-generation from phase context | GSD `.planning/` structure dependency |

## Draft SKILL.md frontmatter

```yaml
name: delivery-review
description: "Orchestrate parallel delivery review across 6 quality dimensions. Launches review-blind-hunter, review-edge-case-hunter, review-acceptance-auditor, review-architecture, review-code-quality, and review-unit-tests as background agents, then triages and synthesizes findings into a unified verdict. Optionally runs deployment-verification for data-touching PRs and threat-mitigation check for phases with a threat model. Use when: 'delivery review', 'review this PR', 'review my changes', 'code review all dimensions', 'full review', 'review before merge', 'is this ready to ship', 'pre-merge check'."
allowed-tools: "Bash(git diff:*), Bash(gh pr diff:*), Bash(gh pr list:*), Read, Grep, Glob, Task"
```

## Open questions for David

1. **7th dimension (security)**: Should the threat-mitigation check from `gsd:secure-phase` become an automatic 7th dimension when a PLAN.md with a threat model is present in the project? Or always require explicit invocation?

2. **Deployment verification trigger**: Should SQL verification + rollback procedures auto-trigger when the diff contains migration files, or require `--deploy-check` flag?

3. **Hard gate before options**: Should `delivery-review` refuse to present PASS verdict if any configured test runner has un-run or failing tests (Superpowers pattern)? Currently it trusts the diff — it doesn't run tests itself.
