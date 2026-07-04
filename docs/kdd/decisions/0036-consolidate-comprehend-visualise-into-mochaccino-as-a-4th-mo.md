> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0036: Consolidate comprehend-visualise into Mochaccino as a 4th mode; restore the shape-warrant gate

**Status:** Proposed (reconstructed)


## Context
The SVG-monoculture regression (see the related learning) was traced to a separate skill, comprehend-visualise, that David had never fully liked ('why are we creating a new skill when we already had one called Mochaccino'). Two live sessions/windows were both able to edit the same untracked skill files with no git safety net, risking a clobber if either unilaterally refactored.

## Decision
Write a single self-contained requirement proposing: fold comprehend-visualise's genuinely useful part (codebase/prose → Mochaccino data, with provenance) into Mochaccino as a 4th mode; restore Mochaccino's existing Shape Librarian specialist as the sole authority on whether/where a diagram is warranted, removing the hardcoded 'always diagram' render lever; demote comprehend-visualise itself to a thin caller that also records run success/failure state. Freeze edits to the three shared untracked files in both sessions until one session is designated the sole executor of that plan.

## Alternatives Considered
Let each session unilaterally patch the files it judged wrong — rejected explicitly because it repeats the same failure mode (one signal over-generalized into an unreviewed change) that caused the original regression, and because both sessions write the same untracked files with no git-based conflict recovery.

## Consequences
Execution is deferred to a future session — this session did not perform the refactor. Coordination overhead of writing and handing off a requirement plus a handover note, even though the immediate fix (the one-line render lever) was understood and small.

## Related
- Sessions: f2df9480

## Provenance
- **Sessions** (1): f2df9480 · 2026-06-08
- **Files** (candidate-level): .claude/skills/comprehend-visualise/SKILL.md, backlog/2026-06-09-mochaccino-consolidation-requirement.md
- **Commits** (candidate-level): —
