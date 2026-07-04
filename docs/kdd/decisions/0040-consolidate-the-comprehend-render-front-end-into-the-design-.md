> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0040: Consolidate the comprehend-render front-end into the design-system skill; restore the Shape Librarian as the shape-warrant gate

**Status:** Proposed (reconstructed)


## Context
The render path's design rules had been hardcoded directly into the calling skill, which caused an SVG over-rotation across all generated output (see linked learning). Two parallel work sessions were both able to edit the same untracked skill files, creating a clobber risk with no git safety net, so a single written requirement doc was needed as the merge point both sides would align to.

## Decision
Fold the useful parts of the comprehend-front-end skill into the design-system skill as a 4th mode ('comprehend → visualise'); restore the Shape Librarian sub-agent as the graphics-warrant gate (default: clean semantic HTML, a diagram only where the content is a flow/topology/relationship and it genuinely clarifies, decided per design); demote the comprehend-front-end skill to a thin caller holding zero design/render rules — its only remaining jobs are comprehending a target into data, stamping provenance (source path + commit), and recording run-state to the failure register.

## Alternatives Considered
Keep design/render rules living in the comprehend-front-end skill (rejected — that is the exact defect that caused the SVG over-rotation, and it duplicates/overrides the Shape Librarian's specialist role). Split execution ownership across both live sessions (rejected — clobber risk on the same untracked files; one side was designated executor, the other assessor, coordinated via a written handover).

## Consequences
A proof re-render was required before treating the fix as validated: re-rendering the same source data through the refactored pipeline had to show genuine per-design shape-or-not judgment — a taxonomy-shaped page returning as plain HTML with zero drawn shapes was the key tell, not a repeat of the all-diagram regression. The design-system skill's tracked-repo changes were committed only after that proof came back green.

## Related
- Sessions: f7a95652

## Provenance
- **Sessions** (1): f7a95652 · 2026-06-08
- **Files** (candidate-level): .claude/skills/comprehend-visualise/SKILL.md, appydave/skills/mochaccino/SKILL.md, appydave/skills/shelly/SKILL.md, backlog/2026-06-09-mochaccino-consolidation-requirement.md
- **Commits** (candidate-level): 7d9eb29
