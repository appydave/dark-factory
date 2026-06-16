# Wire a doc-health sweep (don't build doc-organiser — it now exists as skills)

**Status**: retargeted 2026-06-16 · was "awaiting build-go" (created 2026-06-05)
**Type**: side-quest (machinery) — **NOT on the C1→C5 spine**
**Proposal**: `docs/doc-organiser-proposal.md` — decided; 4 defaults locked (§5)

## ⚠️ Retarget (2026-06-16)
The 2026-06-05 plan was to **build** a `doc-organiser` skill. Since then the appydave-plugins skill
family landed and already covers all 5 locked checks — so the build is unnecessary. The audit *logic*
exists twice over; what's missing is the **dispatch wiring**. Coverage map:

| Locked check (proposal §5) | Existing skill |
|---|---|
| Stale-stamp (date predates git touch) | `appydave:doc-drift` |
| Broken cross-refs | `appydave:doc-drift` + `appydave:doc-review-crossref` |
| Index coverage / orphans / read-order | `appydave:doc-review-topology` / `-gaps` |
| (Fuzzy duplication — deferred to v2) | `appydave:doc-review-coherence` |

Proven 2026-06-16: a `doc-drift` run found `david-design-patterns.md` + 2 docs missing from `INDEX.md`
(same class as the symphony-* orphans) — the skills do the job.

## What (revised)
A `doc-health` sweep dispatched as a Watchtower `kind:skill`/instruction job that runs
`appydave:doc-drift` + `appydave:doc-review` (`--crossref,--topology,--gaps`) over `docs/`, **pinned to
`report` mode**, emitting an **in-chat report**. No new skill at `.claude/skills/doc-organiser/`.

## Locked decisions (from proposal §5 — still hold)
- Watchtower-dispatched; report doubles as cleanup.
- No age flag (exact signals only). In-chat report (no files). Fuzzy-duplication deferred.
- **Guard:** both skills have a `fix` mode — an unattended/dispatched sweep MUST pin `report`, never `fix`
  (honors the proposal's "audit, not autofix" hard line, §42).

## Why parked
Side-quest; the **C1→C5 spine (C3 = the Marshall trigger) is the main line.** Resurface after the spine
is proven, or when a doc sweep is wanted. The dispatch wiring is small — it's a ticket shape, not a build.
