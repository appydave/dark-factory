---
artifact_id: everything-claude-code:skill:agent-payment-x402
repo: everything-claude-code
artifact_type: skill
cluster_facet: [everything-claude-code, agent-payments, x402, spending-controls]
phase_fit: [stage-10]
evaluated_at: 2026-05-17
---

# Eval: agent-payment-x402

**Intent**: Adds x402 HTTP payment execution to AI agents with per-task/session budget caps, allowlisted recipients, non-custodial ERC-4337 wallets, and MCP tool integration.

## Scores
- **quality_score**: 4 — Solid decision tree (Base vs X Layer), four distinct error paths in preToolCheck, security notes on key pinning and env var whitelisting; points off for crypto-domain specificity limiting general adoption
- **adoption_fit_final**: weak — Tightly coupled to blockchain infrastructure (Base, X Layer, ERC-4337); only relevant if building agent-to-agent payment flows or paid API access
- **inspiration_value**: mid — The spending controls model (per-task budget + allowlisted recipients set by orchestrator, not agent) is a clean autonomy-limiting pattern applicable beyond payments
- **uniqueness_refined**: rare — Agent-native payment execution with policy-gated budgets is genuinely novel in the skills catalog space
- **composability**: standalone — MCP server integration; no skill dependencies, but requires external wallet infrastructure
- **description_craft_refined**: trigger — "Add x402 payment execution to AI agents" is precise; use-cases listed are specific enough to avoid false positives

## Mineable phrasing
> "Set budgets before delegation: When spawning sub-agents, attach a SpendingPolicy via your orchestration layer. Never give an agent unlimited spend."

## Notes
The orchestrator-sets-policy-before-delegation pattern (not the agent itself) is the extractable governance idea for dark-factory: any high-privilege capability should be policy-bound at spawn time, not at execution time. The fail-closed preToolCheck implementation is production-grade. Adoption is niche — skip unless x402/crypto payments are on the roadmap.
