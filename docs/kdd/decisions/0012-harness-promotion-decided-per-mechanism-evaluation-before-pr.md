> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0012: Harness promotion decided per-mechanism (evaluation before promotion), not as a wholesale 'promote suborch's kernel'

**Status:** Proposed (reconstructed)


## Context
After shipping the day's 6-item micro-app cut, an OMI voice-memo review pointed out the cut only tested the Claude Code (subagent) harness, never the factory's own dispatch/claim/reap loop. The first response proposed 'promote suborch-demo's proven kernel (warm tmux pool, CAS lease, artifact-is-truth) into dark-factory as the real dispatch.' David pushed back: dark-factory had already done substantial work on this itself, suborch was a from-scratch experiment that referenced dark-factory, and a blind promotion of 'the newest thing' risked discarding dark-factory's own proven pieces (35 real jobs run) without comparison.

## Decision
Ran an explicit evaluation comparing dark-factory's own machinery against suborch-demo mechanism by mechanism, and adopted a hybrid, per-mechanism verdict: promote suborch's warm-pool dispatch and its mid-task HITL gate; keep dark-factory's claim/lease (rename(2)) and reaping (artifact-is-truth), importing only suborch's starvation bug-fix; keep dark-factory's Switchboard for observability; rebuild the state model fresh per the DF-7 spec rather than keeping either side's flat files.

## Alternatives Considered
Wholesale promotion of suborch's kernel (the original, premature framing) — rejected. Doing nothing and re-litigating from first principles was also unnecessary: two prior docs already in the repo (`darkfactory-reconciliation.md` 2026-06-16, `docs/suborch-conformance.md` 2026-06-18) had independently reached the same hybrid conclusion; the evaluation confirmed rather than overturned it.

## Consequences
Became the concrete, file-level promotion plan executed the same day in `engine/` — the production engine build ran one real ticket end-to-end through the factory's own harness (warm-pool worker in tmux, CAS claim, artifact verification, reap, event consumed) and it held with zero repair attempts.

## Related
- Sessions: 2fdc2412

## Provenance
- **Sessions** (1): 2fdc2412 · 2026-06-23
- **Files** (candidate-level): apps/dark-factory/docs/harness-evaluation.md, apps/dark-factory/engine/consumer.py, apps/dark-factory/engine/orchestrator.py, apps/dark-factory/engine/warm_pool.py
- **Commits** (candidate-level): 1cbbf2b, 96fe799, cb998d4
