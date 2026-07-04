> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0021: Don't build a new doc-organiser skill — wire the existing doc-drift + doc-review skill family instead

**Status:** Proposed (reconstructed)


## Context
An earlier proposal called for building a new recurring audit skill (5 deterministic checks: stale-stamp, broken cross-refs, index coverage, orphans, read-order) dispatched as a job, with the build parked awaiting a decision to proceed. By the time it resurfaced, a doc-drift skill (doc-vs-code drift) and a doc-review skill family (`-crossref`, `-topology`, `-gaps`, `-coherence` — doc-vs-doc-set checks) had since landed as existing plugin skills, and between them already covered all 5 of the proposal's locked checks.

## Decision
Do not build the originally-proposed skill. Retarget the parked backlog item from 'build a skill' to 'wire a doc-health sweep' — a dispatched job in report mode that fans out the existing doc-drift and doc-review checks over the docs directory. Stamp the original proposal doc as superseded so it no longer reads as if a fresh build is still the path.

## Alternatives Considered
Build the originally-proposed skill from scratch as planned — rejected because the check logic it would implement already exists twice over across two other skills; building a third copy is unnecessary duplication. The only genuinely missing piece is the dispatch wiring (a scheduled/on-demand job that fans the existing checks out), not the underlying audit logic.

## Consequences
Avoids a full skill build. Produces a coverage map (stale-stamp/cross-refs → doc-drift; index-coverage/orphans/read-order → doc-review-topology/-gaps; duplication, deferred → doc-review-coherence) that becomes the reference for the future dispatch ticket. Carries forward one hard guard from the original proposal: an unattended/dispatched sweep must pin report mode, never fix mode, since both underlying skills support a fix mode and the proposal's rule was audit-only, never autofix.

## Related
- Sessions: 84ec3614

## Provenance
- **Sessions** (1): 84ec3614 · 2026-06-16
- **Files** (candidate-level): backlog/2026-06-05-doc-organiser.md, docs/doc-organiser-proposal.md
- **Commits** (candidate-level): 6b91d46
