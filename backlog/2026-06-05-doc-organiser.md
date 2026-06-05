# Build the doc-organiser audit skill

**Status**: awaiting build-go · created 2026-06-05
**Type**: side-quest (machinery) — **NOT on the C1→C5 spine**
**Proposal**: `docs/doc-organiser-proposal.md` — decided; 4 defaults locked (§5)

## What
A recurring `doc-organiser` audit skill at `.claude/skills/doc-organiser/SKILL.md`: runs 5 deterministic checks over `docs/` — index coverage, orphans, broken cross-refs, stale-stamp, read-order — emits an **in-chat drift report**, **never edits**. Dispatched as a Watchtower `kind:skill` job. First run doubles as the one-time cleanup.

## Locked decisions (from proposal §5)
- B+C (skill + Watchtower-dispatch); first run is the cleanup.
- No age flag (exact signals only). In-chat report (no files). Fuzzy-duplication deferred to a later version.

## Why parked
Real need — doc-drift is already happening (`docs/watchtower/symphony-spec.md` + `watchtower-from-symphony.md` are live orphans). But it's a side-quest; the **C1→C5 spine (C3 = the Marshall trigger) is the main line.** Resurface this after the spine is proven, or when a doc sweep is wanted.
