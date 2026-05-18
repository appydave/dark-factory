---
artifact_id: agent-skills-osmani:command:ship
repo: agent-skills-osmani
artifact_type: command
cluster_facet: [delivery-readiness, orchestration]
phase_fit: [6, 9]
evaluated_at: 2026-05-17
---

# Eval: /ship (command)

**Intent**: Fan-out orchestrator that spawns `code-reviewer`, `security-auditor`, and `test-engineer` subagents in parallel against the current change, then synthesizes their reports into a single go/no-go shipping decision with mandatory rollback plan.

## Scores
- **quality_score**: 5 — Sophisticated orchestration artifact with three clearly separated phases: (A) parallel fan-out via simultaneous Agent tool calls, (B) merge in main context with explicit cross-persona conflict resolution rules, (C) decision template with mandatory rollback plan. Includes persona resolution priority rules (user-defined agents override plugin agents), skip-fan-out threshold (≤2 files, <50 lines, not touching auth/payments/data/config), and explicit constraint documentation (subagents cannot spawn subagents). This is the most mechanically complete orchestration command in the corpus.
- **adoption_fit_final**: strong — David's `delivery-review` skill and `agent-orchestrator` skill cover related territory but neither provides a concrete three-persona parallel fan-out with a merge protocol and a quantified skip threshold. The "issue all three Agent tool calls in a single assistant turn" instruction is a load-bearing implementation detail that David's current skills lack. Gap-closing artifact.
- **inspiration_value**: high — The skip-fan-out rule ("skip only if: ≤2 files, <50 lines, AND not touching auth/payments/data/config/env") converts a judgment call into a deterministic gate. The persona resolution priority table (user-defined → project-level → plugin) is immediately adoptable as a design principle for any fan-out system.
- **uniqueness_refined**: rare — The three-phase fan-out + merge + decision structure with explicit parallelism instructions ("issue all three in a single assistant turn — sequential calls defeat the purpose") is a specific and unusual mechanism. Most orchestration patterns describe the concept; this one gives executable instructions.
- **composability**: calls-others — Orchestrates `code-reviewer`, `security-auditor`, and `test-engineer` as parallel subagents. The merge phase runs in main context, not delegated.
- **description_craft_refined**: trigger — "Run the pre-launch checklist via parallel fan-out to specialist personas, then synthesize a go/no-go decision." Concise and accurate trigger description.

## Mineable phrasing
> "Issue all three Agent tool calls in a single assistant turn so they execute in parallel — sequential calls defeat the purpose of this command."

## Notes
This is the highest-value orchestration artifact in the stage 6 batch. The three-phase structure (fan-out → merge → decision) with explicit parallelism enforcement and a quantified skip threshold is a concrete mechanism David does not have in his current stack. The persona resolution priority rule (user-level > project-level > plugin) is an important design insight for building extensible fan-out systems. At distillation, this should be the winner mechanism for the "delivery-gate-orchestration" cluster.
