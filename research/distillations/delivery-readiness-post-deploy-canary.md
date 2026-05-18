---
distillation_id: delivery-readiness-post-deploy-canary
stage: delivery-readiness
intent: "Verify the live application is healthy after a deploy — endpoints, console errors, performance, and visual regressions"
created: 2026-05-17
status: draft
source_artifacts:
  - everything-claude-code:skill:canary-watch
  - gstack:skill:canary
  - gstack:skill:land-and-deploy
  - compound-engineering:agent:ce-deployment-verification-agent
  - agent-skills-osmani:skill:shipping-and-launch
  - gsd:command:health
winner_mechanism: everything-claude-code:skill:canary-watch
---

# Unified Skill: Post-Deploy Canary

**Purpose**: For Agents: Use when David says "canary", "verify deploy", "post-deploy check", "smoke test", "is production healthy", "watch the deploy", "monitor after release".

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

## Intent

After a deploy or merge, verify the live application is healthy: HTTP endpoints respond correctly, SSE streams are alive, static assets load, console errors are absent, and performance hasn't regressed beyond a threshold.

## Winner's Mechanism

`everything-claude-code:skill:canary-watch` wins because it is:
1. Already a Claude Code-native skill (no additional infrastructure)
2. Covers the broadest surface: HTTP, SSE, static assets, console errors, performance
3. Explicitly designed for post-deploy verification (not just monitoring)
4. Works on any deployed URL — not tied to a specific stack

gstack's `canary` skill covers the same ground but requires the gstack multi-harness-compile step (not in David's stack). CE's `ce-deployment-verification-agent` is pre-deploy (SQL verification, rollback planning) rather than post-deploy. `shipping-and-launch` covers process, not verification.

## Existing-skill nesting

David has no post-deploy canary skill. This is a net-new skill for his stack.

Skip this section — from-scratch build.

## Non-overlapping ideas folded in

- From `gstack:canary`: Periodic screenshot comparison against pre-deploy baseline — `complexity: medium | optional: true | prerequisite: pre-deploy baseline screenshots exist`. The baseline comparison is the key idea — canary-watch currently checks HTTP responses but doesn't compare visual state.
- From `gstack:canary`: Browse-daemon screenshot cadence (periodic, not one-shot) — `complexity: high | optional: true | prerequisite: requires Playwright MCP or similar browser control`. Continuous monitoring is overkill for most deploys; one-shot post-deploy check is sufficient for David's current cadence.
- From `compound-engineering:ce-deployment-verification-agent`: Rollback decision surface — if canary check fails, present rollback procedure (generated pre-deploy) — `complexity: medium | optional: true | prerequisite: rollback procedure exists`. Closes the loop: pre-deploy plan → deploy → canary failure → rollback from plan.
- From `agent-skills-osmani:shipping-and-launch`: Staged rollout verification — verify each rollout stage before proceeding to the next (0% → 10% → 50% → 100%) — `complexity: high | optional: true | prerequisite: deployment system supports staged rollout`. Not relevant for David's current Vercel deploys (full deploy), but worth noting for Kybernesis.
- From `gsd:health`: Planning directory integrity check post-deploy — verify `.planning/` state is consistent after a milestone deploy — `complexity: low | optional: true | prerequisite: project uses GSD .planning/ structure`. Ensures the milestone state files aren't corrupted after CI/CD runs that might touch files.
- From `everything-claude-code:skill:canary-watch` (already winner): SSE stream verification is the distinctive capability — checks that streaming endpoints are alive (critical for SupportSignal's real-time features if any).

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| `everything-claude-code:canary-watch` | Full mechanism: HTTP, SSE, static assets, console errors, performance regressions | ECC-specific `origin: community` attribution |
| `gstack:canary` | Baseline screenshot comparison concept, browse-daemon cadence pattern | gstack's multi-harness-compile requirement, browse-daemon infrastructure |
| `gstack:land-and-deploy` | Post-merge canary trigger placement in deploy flow | gstack's VERSION file, CHANGELOG update steps |
| `compound-engineering:ce-deployment-verification-agent` | Rollback decision surface concept | Pre-deploy SQL verification (separate concern) |
| `agent-skills-osmani:shipping-and-launch` | Staged rollout stage-gate concept | Checklist format (Osmani uses anti-rationalization tables) |
| `gsd:health` | Planning directory integrity check | GSD-specific `.planning/phases/` path conventions |

## Draft SKILL.md frontmatter

```yaml
name: canary-watch
description: "Verify a deployed URL is healthy after releases — checks HTTP endpoints, SSE streams, static assets, console errors, and performance regressions. Optionally compares screenshots against a pre-deploy baseline. Use when: 'canary', 'verify deploy', 'post-deploy check', 'smoke test', 'is production healthy', 'watch the deploy', 'monitor after release', 'check the live site'."
argument-hint: "[url] [--baseline] [--sse-path=/api/stream]"
allowed-tools: "Bash(curl:*), Bash(gh:*), Read, mcp__playwright__browser_navigate, mcp__playwright__browser_snapshot, mcp__playwright__browser_console_messages"
```

## Open questions for David

1. **Playwright dependency**: `canary-watch` is most capable with Playwright MCP for console error checking and screenshot comparison. Is Playwright MCP consistently available in David's sessions, or should the skill degrade gracefully to curl-only checks when Playwright is absent?

2. **SupportSignal priority**: SupportSignal is an NDIS app with PII and real-time features. Post-deploy verification there is higher stakes than AppyDave tools. Should `canary-watch` have a `--critical` mode that runs more checks (auth flows, PII endpoints, SSE streams) vs a lighter default mode?

3. **Baseline capture timing**: Screenshot baseline comparison requires a pre-deploy capture. Should this be built into the PR creation flow (capture baseline before merge, verify after deploy), or always manual?
