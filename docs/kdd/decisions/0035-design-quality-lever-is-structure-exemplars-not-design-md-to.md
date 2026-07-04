> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0035: Design-quality lever is structure + exemplars, not DESIGN.md token expansion

**Status:** Proposed (reconstructed)


## Context
David asked what single change to the design system would have the most leverage on design quality, guessing it was expanding DESIGN.md (colour/type tokens). A matched pair from the rated corpus — chain-sprint-board (shit) vs wave-sprint-board (good), same content, same brand tokens — showed tokens were already identical across the good and bad piles.

## Decision
Reject expanding DESIGN.md as the lever. Instead build two separate artifacts: a pattern rubric (docs/david-design-patterns.md — composition/layout-grammar rules and anti-patterns) and a curated exemplar pack (JSON of top-rated designs by archetype) to feed the render step, while DESIGN.md continues to own only colour/type.

## Alternatives Considered
Expand DESIGN.md with more/better colour and typography rules — rejected on evidence: distinct-colour counts and font stacks were statistically near-identical between the good and bad/meh piles (17 vs 16 colours, same font stack), so tokens could not be the discriminator.

## Consequences
Required building a mechanical feature-extractor (extract.py) and a render-health checker (check-health.py) as prerequisite tooling before the rubric could be trusted. The initial 'composition' rubric itself later needed a correction round once broken renders were found to have confounded the first pass, so the artifact took at least two revision rounds before it was reliable.

## Related
- Sessions: f2df9480

## Provenance
- **Sessions** (1): f2df9480 · 2026-06-08
- **Files** (candidate-level): docs/david-design-patterns.md, tools/mocha-census/extract.py, tools/mocha-census/out/ratings/exemplars.json
- **Commits** (candidate-level): —
