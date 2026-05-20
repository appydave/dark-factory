# Run Summary — b65 Title Generation + Refinement

**Video**: b65 — Guy Monroe Marketing Plan
**Run date**: 2026-05-20
**Workflow**: `workflow-titles.json` (title-generation-refinement v1.0.0)
**Elapsed**: ~56 seconds (2 subagents + 1 conductor-writes checkpoint)
**Critique fixture**: `runs/b65/critique-fixture.txt`
**Attempt count**: 2 (attempt:1 = initial generation, attempt:2 = critique-driven refinement)

## Steps run

| Step | Type | Key written | Attempt | Status |
|------|------|-------------|---------|--------|
| generate-title | transform | generatedTitles | 1 | ✓ |
| apply-critique | checkpoint (conductor-writes) | titleCritiqueLog | 1 | ✓ |
| refine-titles | transform | generatedTitles | 2 | ✓ |
| refine-titles | transform (outputKeyMap) | selectedTitles | 2 | ✓ |

## Store append history (key ordering)

generatedTitles(attempt:1) → titleCritiqueLog → generatedTitles(attempt:2) → selectedTitles

## Isolation verification

- conductor-session-titles.log: 11 lines — dispatch/ack/critique-logged/refine/done markers only
- No title text in conductor log: ✓ verified
- No critique content in conductor log: ✓ verified (critique written to store by conductor-writes; log only records CRITIQUE-LOGGED key)

## outputKeyMap exercised

`refine-titles` step mapped `topTitle → selectedTitles`. Both records share `meta.step="refine-titles"` and `meta.attempt=2`.
