---
distillation_id: verification-validation-system-health-scan
stage: verification
intent: "Post-deploy or on-demand system health snapshot — observable signals confirming the system is operating correctly"
created: 2026-05-17
status: draft
source_artifacts:
  - gstack:skill:health
  - gstack:skill:qa
  - gstack:skill:qa-only
  - gstack:skill:canary
  - gbrain:skill:smoke-test
  - gbrain:skill:restart-sweep
  - gsd:command:health
  - gsd:command:audit-milestone
  - compound-engineering:skill:ce-product-pulse
  - compound-engineering:agent:ce-performance-oracle
  - ruflo:skill:agent-performance-monitor
  - ruflo:skill:agent-performance-benchmarker
  - ruflo:skill:agent-benchmark-suite
  - gstack:skill:benchmark
winner_mechanism: compound-engineering:skill:ce-product-pulse
---

# Unified Skill: verification-validation-system-health-scan

**Purpose**: Generate a structured health snapshot of the current system state — post-deploy, post-session, or on demand. Distinct from deployment verification (which gates a deploy) and code review (which reviews code quality). This is the "is the system OK right now?" pulse check.

**For Agents**: Use when David says "how's the system looking?", "health check", "post-deploy scan", "is everything working?", "product pulse", "smoke test", "did the deploy go OK?". Also fires proactively after an autonomous session completes. NOT a deployment gate — this is observability, not a blocker.

**Created**: 2026-05-17
**Last Updated**: 2026-05-17

---

## Intent

Produce a quick, structured health snapshot that surfaces observable signals about whether the system is working correctly. The failure mode being prevented: assuming everything is fine because no one reported an error, when in fact a quiet regression or drift has occurred.

Distinct from:
- `delivery-review` — quality gate on a finished artifact (pre-merge)
- `data-deploy-gate` — pre-deploy safety checklist (blocking)
- `pre-completion-gate` — evidence before success claims (per-task)
- `system-health-scan` (this) — non-blocking observability pulse (post-deploy, on-demand)

## Winner's Mechanism

`compound-engineering:skill:ce-product-pulse` wins. It is the most complete "is the system healthy from a product perspective" skill in the cluster, combining:

1. **Multi-dimensional product scan** — not just "are tests passing" but: build status, test suite, API response times, feature flag states, error rates, user-facing flows. The product perspective means it catches the case where tests pass but the app is broken for users.
2. **Trend-aware analysis** — compares current state to baseline, not just absolute values. "Error rate 0.3% (up from 0.1% yesterday)" is more actionable than "error rate 0.3%."
3. **Actionable output** — each finding includes: what was observed, what the baseline is, and a concrete next action. Not a wall of metrics — a prioritized list of signals needing attention.

The compound-engineering skill is the product-oriented framing. The technical infrastructure framing comes from the folded-in ideas below.

## Overlap with code-review cluster

Some `gsd:command:health` and `gstack:skill:health` artifacts appear in both the verification-validation and code-review slices. The distinction:

- **Code-review cluster** (if health appears there): Reviews code changes for quality issues
- **This cluster**: Observes the running system for operational health signals

The code-review cluster says "is this code good?" The system-health-scan says "is this system running OK?" Orthogonal concerns — a system can have quality code that's operationally unhealthy (misconfigured, degraded dependencies) or low-quality code that happens to be running fine.

## Non-overlapping ideas folded in

- From `gbrain:skill:smoke-test`: **Minimal sanity check protocol** — a fast (<60 second) smoke test that verifies the system's critical paths are functional before declaring health. The distinction from a full test suite: smoke tests verify the system is running and its core paths are reachable, not that all edge cases pass. Useful as the first step in any health scan. — `complexity: low | optional: false | prerequisite: "system has runnable endpoints or entry points"`

- From `gstack:skill:canary`: **Canary deployment health check** — when a new version is deployed to a canary, compare its error rate and response times against the stable fleet before promoting. The canary pattern is the mechanism; the health scan is how you read the canary signal. — `complexity: medium | optional: true | prerequisite: "canary deployment infrastructure exists"`

- From `ruflo:skill:agent-performance-benchmarker`: **Agent performance baseline** — for David's agent systems specifically, track token consumption, latency, and success rate per agent across runs. Detects the case where an agent prompt change degraded performance without failing tests. Particularly relevant for Kybernesis and autonomous pipeline work. — `complexity: medium | optional: true | prerequisite: "automated agent runs with instrumentation"`

- From `gbrain:skill:restart-sweep`: **Service restart detection** — identify which services have restarted unexpectedly since last check. An unexpected restart often indicates a crash loop or OOM condition that doesn't surface in error rates immediately. — `complexity: low | optional: true | prerequisite: "managed services with restart visibility"`

- From `gsd:command:audit-milestone`: **Milestone health audit** — at milestone boundaries, verify that all phase verifications passed, all required artifacts exist, and no deferred gaps are blocking. The milestone audit is the coarsest grain of health check: "is the entire milestone in a shippable state?" — `complexity: medium | optional: true | prerequisite: "GSD-style milestone tracking or equivalent"`

## The three health scan grains

| Grain | Timing | Duration | Artifact | Winner |
|-------|--------|----------|----------|--------|
| **Smoke test** | Post-deploy, first 5 minutes | <60 seconds | Running system | gbrain:smoke-test |
| **Product pulse** | End of session, post-deploy | 5-10 minutes | System + metrics | ce-product-pulse |
| **Milestone audit** | End of milestone | 15-30 minutes | All phase artifacts | gsd:audit-milestone |

The unified skill should expose all three grains as modes. Each fires at a different cadence and produces different output depth.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| ce-product-pulse | Multi-dimensional product scan, trend-aware analysis, actionable output format | CE-specific tooling, Every Inc. internal metrics |
| gbrain:smoke-test | Smoke test protocol, <60 second constraint, critical-path focus | GBrain-specific tooling |
| gstack:canary | Canary comparison pattern | GStack-specific deployment infrastructure |
| ruflo:agent-performance-benchmarker | Agent performance baseline concept | Ruflo instrumentation infrastructure |
| gbrain:restart-sweep | Service restart detection pattern | GBrain-specific service catalog |
| gsd:audit-milestone | Milestone health audit concept | GSD-specific phase artifact structure |

## Draft SKILL.md frontmatter

```yaml
name: health-scan
description: >
  Post-deploy or on-demand system health snapshot — observable signals confirming the system
  is operating correctly. Three modes: smoke (< 60 seconds, critical paths reachable),
  pulse (5-10 minutes, product + metrics + trends), milestone (end-of-milestone, all artifacts).
  Use when: "health check", "post-deploy scan", "is everything working?", "product pulse",
  "smoke test", "did the deploy go OK?", "how's the system?".
  Non-blocking observability — not a deployment gate, not a code review.
argument-hint: "[smoke | pulse | milestone]"
allowed-tools: Bash(curl:*), Bash(git log:*), Bash(git diff:*), Read, Bash(grep:*)
```

## Open questions for David

- Should `health-scan` be scheduled (run automatically post-deploy and at session end) rather than invoked manually? An automatic post-deploy smoke test would catch "it deployed but it's broken" immediately. The compound-engineering `ce-product-pulse` is currently a manually-invoked skill — but a hook on deploy events would be more reliable.
- What's the minimal smoke test for SupportSignal? Candidates: check auth endpoint returns 200, check a Convex query returns data, check that the NDIS participant list loads. A project-specific smoke test template would be more useful than a generic one.
- The agent performance benchmarker is specifically relevant for Kybernesis. Is this the right time to define agent performance baselines, or should that wait until the first production Kybernesis agents are running?
