# Watchtower — Build Handover

**For**: a fresh session that will build the Watchtower app.
**How to use**: open a new Claude Code session in `~/dev/ad/apps/dark-factory/` and paste:
> "Read `docs/watchtower/HANDOVER.md` and continue building Watchtower."

---

## One-line goal

Build **Watchtower v0** — a local AppyStack app at `apps/watchtower/` that is the human control surface over Dark Factory workflows: a decision queue ("what needs me?"), not another dashboard.

## Why it exists

David hit overwhelm at N=5 census records on the Mochaccino dashboard. Visualisations show *everything*; Watchtower's primitive is a **queue** — it shows *the next decision*. Full rationale in `chatgpt-brief.md`.

## Read these first (in order)

1. `docs/watchtower/DECISIONS.md` — the 4 locked decisions. **Binding.** Supersede any conflicting prose in the docs below.
2. `docs/watchtower/REVIEW.md` — the design review. Lists what to fix before building.
3. `docs/watchtower/schemas.md` — the data contracts. **This is the canonical doc** where the three docs disagree.
4. `docs/watchtower/spec.md` — requirements (7 ACs, scope cuts).
5. `docs/watchtower/plan.md` — phased plan. **Needs re-phasing** (see below).
6. `experiments/watchtower-engine/README.md` — the trigger engine, already built and proven.

## What's already done (do NOT rebuild)

- **The trigger engine** — `experiments/watchtower-engine/`. The queue + atomic-claim mutex is built and stress-proven (200 entries × 8 claimers, zero double-claims). This is the *trigger half* of Watchtower. The app's "Run" button just writes a queue entry into `experiments/watchtower-engine/queue/` (or its promoted location); the engine + `run-next-workflow` skill do the rest.
- **The four record schemas** — defined in `schemas.md`. Generate JSON Schema files from it.
- **The 4 design decisions** — in `DECISIONS.md`.

## Locked decisions (from DECISIONS.md — do not relitigate)

1. **Trigger = file/queue, not shell-exec, not headless.** Watchtower writes a queue entry; an in-session `run-next-workflow` skill (on a `/loop`, up to 4 staggered sessions) claims and runs it. This runs on David's subscription — **never** Agent SDK / `claude -p` (those start metered billing 2026-06-15).
2. **Run IDs experiment-keyed**: `run-<exp-slug>-NNN`. Experiment IDs: `exp-YYYYMMDD-<slug>`.
3. **Promotion records a decision only** — Watchtower has NO write access to `canonical/`.
4. **Buttons only, no Swagger chat layer** in v0.

## Fix before building (from REVIEW.md)

- **C1**: `plan.md` Phase 0–1 is written for shell-exec — re-phase to the queue/file-trigger engine that already exists in `experiments/watchtower-engine/`. The app doesn't spawn subprocesses; it writes queue entries.
- **I1–I4**: conform `spec.md` and `plan.md` to `schemas.md` IDs and `duration_ms`; fix the seed `workflow.type` (`workflow_tool`, not `experiment`); use dir-per-run (`runs/<id>/run.json + log.txt`).

## What to build (v0 surface — the "easy half")

The engine is done; build the surface:

1. **Scaffold**: `appydave:create-appystack apps/watchtower` (RVETS).
2. **Reads** (validated, file-backed): experiments, runs, learnings, promotions from `data/` + the engine's `runs/`, and `research/census.jsonl` (read-only).
3. **Today screen** (the home): decision queue, capped at 5 cards, ordered oldest-first. Back-fill census batch-0 as a synthetic experiment so it's not empty.
4. **Run button**: writes a queue entry into the engine's `queue/`. Does NOT execute anything itself.
5. **Experiments + Runs drill-downs**: plain tables, no charts. Hard rule: no screen renders >50 records.
6. **Promote/Kill buttons**: write a `promotion.yml` (decision only).

## First vertical slice

Census batch-1 end-to-end: open Today → click Run on the seed experiment → a queue entry is written → (the engine, running in a session with `run-next-workflow`, picks it up and runs `level-1-census`) → run record + 5 new census rows appear → experiment surfaces on Today as "needs decision" → click Promote → `promotion.yml` written.

## Hard constraints

- Local-only, single-user, no auth.
- Files are source of truth; the app is a projection (deleting any index is harmless).
- Never modify `.claude/workflows/*.js` or write to `canonical/`.
- No metered-billing execution paths.

## Open (decide during build, non-blocking)

- Rerun semantics (mutate experiment vs clone).
- Can a learning be promoted independently of its experiment.
- Exact `data/` ↔ `experiments/watchtower-engine/` boundary (does the app use the engine's dirs directly, or its own `data/` that the engine reads?).
- Whether to promote `run-next-workflow` from the spike into an installed project skill as part of this build.
- **Nesting location (David, 2026-05-30): not convinced.** v0 was scaffolded at `dark-factory/apps/watchtower/` (nested) so app + trigger engine live in one repo, and its `.git` was removed so dark-factory tracks it as plain files. **This may move to a sibling `~/dev/ad/apps/watchtower/` later** (the standard Micro Apps slot). No need to move now — but don't bake the nested path into anything hard to change. Registered in `apps.json` as port 5060/5061, `group: apps`, status `pre-build`.

## Deferred to other systems

- Skill usage telemetry (used-vs-stale) → AngelEye, not here.
