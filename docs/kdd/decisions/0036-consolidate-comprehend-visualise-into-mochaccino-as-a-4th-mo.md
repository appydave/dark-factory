---
id: ADR-0036
title: "Consolidate comprehend-visualise into Mochaccino as a 4th mode; restore the shape-warrant gate"
status: proposed
scope: internal
date_decided: 2026-06-08
deciders: [David Cruwys]
confidence: reconstructed
recurrence_count: 2
provenance:
  sessions: ["f2df9480", "f7a95652"]
  files: [".claude/skills/comprehend-visualise/SKILL.md", "appydave/skills/mochaccino/SKILL.md", "appydave/skills/shelly/SKILL.md", "backlog/2026-06-09-mochaccino-consolidation-requirement.md"]
  commits: ["7d9eb29"]
tags: []
---

> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.
> Merged 2026-07-04 from two same-day reconstructed candidates (sessions `f2df9480` and `f7a95652`,
> both 2026-06-08) that recorded the proposal and its later execution — originally staged separately
> as ADR-0036 and ADR-0040.

# ADR-0036: Consolidate comprehend-visualise into Mochaccino as a 4th mode; restore the shape-warrant gate

**Status:** Proposed (reconstructed)

## Context

An SVG-monoculture regression was traced to a separate skill, `comprehend-visualise`, that David
had never fully liked ("why are we creating a new skill when we already had one called
Mochaccino"). The render path's design rules had been hardcoded directly into that calling skill,
causing an SVG over-rotation across all generated output. Two live sessions/windows were both able
to edit the same untracked skill files with no git safety net, risking a clobber if either
unilaterally refactored.

## Decision

Fold `comprehend-visualise`'s genuinely useful part (codebase/prose → Mochaccino data, with
provenance) into Mochaccino as a 4th mode ("comprehend → visualise"); restore Mochaccino's existing
Shape Librarian sub-agent as the sole authority on whether/where a diagram is warranted (default:
clean semantic HTML, a diagram only where the content is a flow/topology/relationship and it
genuinely clarifies, decided per design) — removing the hardcoded "always diagram" render lever;
demote `comprehend-visualise` itself to a thin caller holding zero design/render rules, whose only
remaining jobs are comprehending a target into data, stamping provenance (source path + commit),
and recording run-state to the failure register. One session was designated executor, the other
assessor, coordinated via a written handover/requirement doc rather than both sides patching the
same untracked files.

## Alternatives Considered

- **Let each session unilaterally patch the files it judged wrong** — rejected: repeats the same
  failure mode (one signal over-generalized into an unreviewed change) that caused the original
  regression, on files with no git-based conflict recovery.
- **Keep design/render rules living in `comprehend-visualise`** — rejected: that is the exact
  defect that caused the SVG over-rotation, and it duplicates/overrides the Shape Librarian's
  specialist role.

## Consequences

A proof re-render was required before treating the fix as validated: re-rendering the same source
data through the refactored pipeline had to show genuine per-design shape-or-not judgment — a
taxonomy-shaped page returning as plain HTML with zero drawn shapes was the key tell, not a repeat
of the all-diagram regression. The design-system skill's tracked-repo changes were committed only
after that proof came back green (commit `7d9eb29`).

## Related

- Sessions: `f2df9480`, `f7a95652`

## Provenance

- **Sessions** (2): `f2df9480` · 2026-06-08, `f7a95652` · 2026-06-08
- **Files** (candidate-level): `.claude/skills/comprehend-visualise/SKILL.md`, `appydave/skills/mochaccino/SKILL.md`, `appydave/skills/shelly/SKILL.md`, `backlog/2026-06-09-mochaccino-consolidation-requirement.md`
- **Commits** (candidate-level): `7d9eb29`

## Revision Log

- 2026-07-04 — reconstructed — Lisa KDD pipeline extraction (session-mined). Reformatted into DF-ADR template; not yet manually ratified.
