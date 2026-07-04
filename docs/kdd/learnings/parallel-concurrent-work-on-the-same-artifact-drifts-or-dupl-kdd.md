---
topic: "parallel spec-drafting drift"
issue: "Parallel/concurrent work on the same artifact drifts or duplicates without coordination"
created: "2026-05-27"
story_reference: "1f8758f3, 84ec3614"
category: "process"
severity: "medium"
status: "proposed"
recurrence_count: 2
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["docs/watchtower/DECISIONS.md", "docs/watchtower/REVIEW.md", "docs/watchtower/plan.md", "docs/watchtower/schemas.md", "docs/watchtower/spec.md", "experiments/watchtower-engine/proof/cortex-88aa6bf/ (created then removed, untracked)"]
commits: ["9c3d374"]
---

# parallel spec-drafting drift — Parallel/concurrent work on the same artifact drifts or duplicates without coordination

## Problem Signature

**Symptoms**: plan.md's Phase 0.1 picked shell-exec via child_process.spawn and explicitly argued against file-trigger; spec.md also assumed shell-out; only schemas.md matched the mechanism that was eventually locked. The three docs also disagreed on run-ID format and duration_ms vs seconds, and one seed example in a doc was invalid against its own schema.

**Environment**: docs/watchtower/ — Watchtower v0 design phase, dark-factory repo

**Triggering Conditions**: Three agents were launched in parallel from a shared brief with no single already-ratified decision doc to write against, and the binding DECISIONS.md was only produced afterward — the plan and spec agents drafted before the trigger mechanism was formally decided.

## Root Cause
Fanning work out to independent agents without a shared, ratified contract lets each agent make its own defensible-but-different call on unresolved open questions; nothing forces convergence between them.

## Solution
Ran a code-review-and-quality pass (agent-skills:code-review-and-quality) over all three docs against the newly-locked DECISIONS.md. The review explicitly surfaced the contradiction (finding C1: the plan builds the mechanism David rejected) and the ID-format drift (findings I1-I4), then designated schemas.md as the canonical contract the other two docs must conform to.

## Prevention
When fanning multiple agents out to draft related design docs in parallel, either hand them a single already-ratified decisions doc up front, or budget an explicit cross-document consistency-review pass afterward before treating the combined output as ready to build from.

## Related
- Sessions: 1f8758f3, 84ec3614
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (2): 1f8758f3, 84ec3614 · 2026-05-27 → 2026-06-16
- **Files** (candidate-level): docs/watchtower/DECISIONS.md, docs/watchtower/REVIEW.md, docs/watchtower/plan.md, docs/watchtower/schemas.md, docs/watchtower/spec.md, experiments/watchtower-engine/proof/cortex-88aa6bf/ (created then removed, untracked)
- **Commits** (candidate-level): 9c3d374
