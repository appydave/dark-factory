---
distillation_id: orchestration-governance-and-observability
stage: orchestration
intent: "Observe, measure, cost-track, and cryptographically verify what a swarm of agents is doing — the control plane layer"
created: 2026-05-16
status: draft
source_artifacts:
  - ruflo:command:witness
  - ruflo:command:intelligence
  - ruflo:command:observe
  - ruflo:agent:telemetry-analyzer
  - ruflo:agent:observability-engineer
  - ruflo:command:ruflo-cost
  - ruflo:skill:performance-analysis
  - ruflo:agent:horizon-tracker
  - ruflo:command:ruflo-loop
  - ruflo:command:ruflo-schedule
  - ruflo:command:watch
  - appydave-plugins:skill:truth-trail
  - ruflo:skill:claims
  - ruflo:skill:agentic-jujutsu
  - ruflo:agent:sparc-orchestrator
winner_mechanism: ruflo:command:observe
---

# Unified Skill: governance-and-observability

**Purpose**: Watch what agents are doing, correlate their actions with outcomes, track costs, enforce integrity rules, and verify fixes are genuine — the control plane for an agent swarm.

**For Agents**: Use when David asks "what are agents doing", "how much did that cost", "show me traces", "did that agent actually fix it", "watch the swarm", "knowledge integrity check", or needs to govern an autonomous agent run.

**Created**: 2026-05-16
**Last Updated**: 2026-05-16

---

## Intent

Observe agent swarm execution (traces + logs + metrics), track costs, enforce integrity rules (truth-trail), cryptographically verify fix manifests (witness), and surface long-horizon objective drift — all without stopping the swarm.

## Winner's Mechanism

`ruflo:command:observe` wins as the foundation — it live-streams swarm events, filters logs, correlates agent activity with application outcomes (traces + metrics together), and is non-blocking. `ruflo:command:watch` is the simpler live-stream companion.

However, **this cluster has no single winner** — the three most important mechanisms are distinct and non-overlapping:
1. **Observe** (ruflo) — real-time telemetry and log correlation
2. **Witness** (ruflo) — cryptographic fix manifest with temporal history (ADR-103), prevents "fixed it" rationalization
3. **Truth-trail** (appydave) — knowledge integrity rules for second-brain agents (don't claim memory you don't have, don't synthesize citations)

All three belong in David's stack and are composable: truth-trail governs knowledge agents, witness governs code-fixing agents, observe governs the swarm at runtime.

## Non-overlapping ideas folded in

- From `ruflo:command:witness`: **Cryptographically-signed fix manifest** — when an agent claims "it's fixed", witness requires a signed entry in the temporal manifest before the fix is accepted. Eliminates the "I verified it works" rationalization.
- From `ruflo:command:intelligence`: **Model routing rationale on demand** — which model each agent is using and why; cost-per-model breakdown. Useful for optimizing David's spend across harness.
- From `ruflo:skill:performance-analysis`: **Bottleneck detection for swarms** — which agents are slow, which tasks are choke points, optimization recommendations. Different from cost tracking (time vs money).
- From `ruflo:agent:horizon-tracker`: **Long-horizon objective tracking across sessions** — detects drift between current work and the original goal, with milestone checkpoints. The "are we still building what we meant to build?" layer.
- From `appydave-plugins:skill:truth-trail`: **Knowledge integrity rules** — specific anti-hallucination rules for second-brain agents (no phantom citations, no false memory claims). Already in David's stack; folded in as the knowledge-agent governance layer.

## Provenance

| Source artifact | What was kept | What was set aside |
|----------------|---------------|---------------------|
| ruflo:observe | Real-time trace + metrics correlation, non-blocking | Ruflo telemetry infrastructure |
| ruflo:witness | Cryptographic fix manifest (ADR-103) | Ruflo signing machinery |
| ruflo:intelligence | Model routing rationale + cost breakdown | Ruflo intelligence dashboard |
| ruflo:ruflo-cost | Cost tracking, budgets, optimization recommendations | Ruflo-specific cost DB |
| ruflo:performance-analysis | Bottleneck detection for swarms | Ruflo performance DB |
| ruflo:horizon-tracker | Long-horizon drift detection across sessions | Ruflo persistence layer |
| ruflo:watch | Live-stream swarm events (simpler than observe) | Ruflo event bus |
| truth-trail (appydave) | Knowledge integrity rules for second-brain agents | None — kept as-is |
| ruflo:claims | Claims-based authorization for agent operations | Ruflo claims infra |

## Draft SKILL.md frontmatter

```yaml
name: governance-and-observability
description: >
  Observe, cost-track, integrity-verify, and govern an agent swarm without stopping it.
  Three composable layers: observe (real-time telemetry), witness (cryptographic fix verification),
  truth-trail (knowledge integrity rules for brain agents).
  Use when: "what are agents doing", "how much did that cost", "show me traces",
  "did the agent actually fix it", "watch the swarm", "integrity check", "are we on track",
  "drift detection", "cost breakdown", "slow agent".
```

## Open questions for David

- `truth-trail` is already an appydave skill — does it belong here as a sub-skill or stay standalone? (It's narrow: knowledge integrity only, not general governance.)
- Is `witness` (cryptographic fix manifest) worth adopting? It requires buy-in to the temporal manifest format — non-trivial. OR is the core idea (require signed evidence before accepting "it's fixed") adoptable without the crypto machinery?
- Is there a simpler "governance dashboard" David could build now vs the full Ruflo telemetry stack? (E.g., a lightweight `observe` that just tails Claude's tool use log and reports what agents wrote/ran.)
