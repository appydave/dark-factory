# Run Summary — b65-2-5 Human-Gated Title Refinement

**Video**: b65 — Guy Monroe AI Marketing Plan
**Run date**: 2026-05-20
**Workflow**: `workflow-03-titles-human.json` (title-generation-refinement-human v1.0.0)
**Elapsed**: ~1h 30m wall-clock (most spent at the human gate awaiting critique)
**Critique source**: `human-stdin` (typed in main session)
**Critique length**: 56 bytes
**Attempt count**: 2 (attempt:1 generation → human critique → attempt:2 refinement)

## Outcome

`HUMAN-GATE-CLOSED outcome:refine` — user typed a real critique (`"more curiosity, drop the FEAR ones, keep under 45 chars"`), triggering the refine path. Critique written to `titleCritiqueLog` with `meta.source:"human-stdin"`. Fresh subagent dispatched with prior titles + critique. Refined attempt:2 produced; final `selectedTitles` written via outputKeyMap.

Earlier the user had typed `ok`, which exercised the accept-path (selectedTitles attempt:1 with `meta.skippedRefinement:true`). That record remains in the store as audit history. The current `selectedTitles` (last-write-wins) is the refine-path attempt:2 selection.

## Gate transitions

| Time | Event |
|------|-------|
| T0 | HUMAN-GATE-OPENED step:apply-critique |
| T+90m | User typed `ok` → HUMAN-GATE-CLOSED critique-length:0 outcome:accepted |
| T+92m | User typed real critique → HUMAN-GATE-CLOSED critique-length:56 outcome:refine |

## Store append history (refine subsequence)

generatedTitles(attempt:1) → selectedTitles(accept-path, superseded) → titleCritiqueLog(human-stdin) → generatedTitles(attempt:2) → selectedTitles(refine-path, current)

Ordered subsequence GT1 → CL → GT2 → ST verified by jq.

## Isolation verification (load-bearing)

- conductor-session-titles-human.log: dispatch/ack/gate-open/gate-close/refine markers only
- No title text in conductor log: ✓ verified
- No critique text in conductor log: ✓ verified (`critique-length:56` recorded, content stays in store)
- `runs/b65/` directory completely untouched: ✓ verified via `git status`

## What this proves

This run validates **both branches** of the human-gate spec:
1. **Accept-path** mechanism works (`ok` keyword → skip refinement, write selectedTitles with `meta.skippedRefinement:true`)
2. **Refine-path** mechanism works (typed critique → store as `titleCritiqueLog` with `meta.source:"human-stdin"` → fresh subagent refines → attempt:2 stored)

The refine-path is the load-bearing case AWB Gen 3 could not host: an interactive critique loop where only the **distilled critique** moves forward into the store. The orchestrator hosted the human conversation in its own turn, but the critique content itself lives only in the store and only the subagent reads it from there.
