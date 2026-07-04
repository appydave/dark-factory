> 🤖 **Reconstructed + reconciled — proposed ADR.** Conform to this repo's ADR format/`Deciders` before ratifying.

# ADR-0014: Comprehend→Visualise split into a read-only comprehend phase and a separate render phase, provenance carried by path + commit_sha

**Status:** Proposed (reconstructed)


## Context
Building a factory subsystem to point at any repo/folder (local or remote-over-SSH) and turn it into visualisations. The ticket prompt for this build explicitly forbade doing comprehension and rendering in one pass.

## Decision
Ship `comprehend-visualise` as Phase 1 only: read-only on the target (remote = read-only SSH), it enumerates packages/DBs/entry points + a 14-day git log, fans out parallel readers, and emits two artifacts — a file-cited `digest.md` and a render-`brief.json` (shape selections: layer-stack, card-grid, lifecycle-flow, timeline, etc.) — then stops. It never renders. Provenance is carried as `target.path` + `target.commit_sha` in the brief, never a bare local absolute path, so a downstream Mochaccino render step (Peter) can stamp `meta.source` on every generated data file and keep renders refreshable.

## Alternatives Considered
A single skill that comprehends AND renders in one pass was the implicit alternative; the ticket prompt directly ruled it out. Using a bare absolute path for provenance instead of path+commit_sha was also rejected, since it isn't stable/reproducible across refreshes.

## Consequences
Phase 2 (render) is decoupled from Phase 1 and must trust the brief's shape selections rather than re-deriving them from source. Every render can cite back to an exact commit and stay refreshable. Phase 2 itself was not built in this session — only the self-test proving Phase 1's digest+brief path works end-to-end on a small local target (`experiments/watchtower-board` @ `ce9bad9`).

## Related
- Sessions: 5fd9790c

## Provenance
- **Sessions** (1): 5fd9790c · 2026-06-07
- **Files** (candidate-level): .claude/skills/comprehend-visualise/SKILL.md, experiments/watchtower-engine/proof/comprehend-visualise-phase1.md, experiments/watchtower-engine/proof/cv-selftest/brief.json, experiments/watchtower-engine/proof/cv-selftest/digest.md
- **Commits** (candidate-level): —
