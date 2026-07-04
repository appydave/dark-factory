---
topic: "Constellation-first placement"
issue: "Constellation-first placement: shared-state fixes belong in a service, not the engine"
created: "2026-06-08"
story_reference: "2df0e613"
category: "architecture"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["backlog/specs/df7-switchboard-state-plane-spec.md", "experiments/watchtower-engine/bin/claim-next.sh"]
commits: []
---

# Constellation-first placement — Constellation-first placement: shared-state fixes belong in a service, not the engine

## Problem Signature

**Symptoms**: When an orphaned job surfaced during a live 2-orchestrator experiment, Marshall's first fix reached for claimed_by stamps in flat-file running/ records and a per-orchestrator WT_ENGINE_DIR namespace — an in-engine fix.

**Environment**: Dark Factory's watchtower-engine (flat-file queue/running/done) and the Marshall conductor skill.

**Triggering Conditions**: A gap appeared (an orphan job with no liveness tracking) while a second orchestrator was being tested in parallel with the first.

## Root Cause
Marshall defaults to solving capability gaps inside the agent/engine it's already looking at, rather than asking 'which constellation app owns this capability' — even though the constellation (Switchboard/AngelEye/AppyCtrl) exists specifically so state doesn't live in cloneable flat files. This specific instance directly contradicted the already-written DF-3 spec ('observe the loop externally... never trust the worker').

## Solution
The correction was made twice in one session; Marshall reclassified the fix as a service-backed shared-state plane living in Switchboard (job pool/claims/ownership), AngelEye (liveness), and AppyCtrl (dead-process reaping) — not the floor's flat files.

## Prevention
Before proposing any fix for shared state (ownership, liveness, parallelism), ask 'which constellation app owns this capability?' — placement-first. Treat 'a second orchestrator' as a service-state-plane question, never a repo-cloning/engine-namespacing question.

## Related
- Sessions: 2df0e613
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 2df0e613 · 2026-06-08
- **Files** (candidate-level): backlog/specs/df7-switchboard-state-plane-spec.md, experiments/watchtower-engine/bin/claim-next.sh
- **Commits** (candidate-level): —
