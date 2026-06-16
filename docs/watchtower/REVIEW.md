# Watchtower v0 — Design Review

> **⚠️ ARCHIVE-BOUND (2026-06-06) — see [`RE-BUCKETING.md`](RE-BUCKETING.md).** Process/history from the v0 drafting
> era; kept for provenance, not current design. For the live three-plane model read RE-BUCKETING.md +
> [`../dark-factory-constellation.md`](../dark-factory-constellation.md).

**Reviewer**: code-review-and-quality (five-axis)
**Date**: 2026-05-30
**Subject**: `schemas.md`, `spec.md`, `plan.md` reviewed as the PR that defines the build, against locked `DECISIONS.md`.
**Verdict**: **Request changes** — strong design, but the plan contradicts a locked decision, three docs disagree on IDs, and the execution model rests on an unverified assumption. All fixable in <1 hour of doc edits + one spike.

---

## Critical (must resolve before any code)

### C1 — The plan contradicts the locked trigger decision (D1)
- **DECISIONS.md D1**: file-trigger + watcher.
- **plan.md Phase 0.1**: picks **shell-exec via `child_process.spawn`** and explicitly argues *against* file-trigger ("doubles the contract").
- **spec.md**: also assumes shell-out (§7, assumption 4, Q2 rec a).
- **schemas.md**: correctly uses file-trigger (§7).
- **Impact**: Phases 0–1 of the plan — the spine, the first two days — are written for the rejected mechanism. If you build the plan as-is you build the thing you decided against.
- **Fix**: Re-phase plan §0.1 and §1.2 around the file-trigger contract already specified in `schemas.md §7.1`. The plan author's objection ("workflow doesn't know it was triggered") is answerable: the harness *watcher* wraps the workflow; the workflow stays ignorant. Override the rationale.

### C2 — The execution model is unverified (real Phase-0 blocker)
- Both mechanisms (file-trigger *and* shell-exec) assume a **non-Claude process can execute a `.workflow.js`**. The Workflow Tool runs *inside* a Claude Code session. Nobody has confirmed a detached watcher/subprocess can run a workflow headless.
- Memory note "Workflow Tool WORKING as of 2026-05-23" refers to *in-session* use, not headless.
- plan.md Q1 and spec.md R10/Q2 both circle this but neither resolves it.
- **Impact**: If workflows can't run headless, the entire "click a button → workflow runs" premise collapses, and v0 becomes "Watchtower writes a trigger; David runs it in his open Claude session" (human-in-the-loop trigger). That's still fine — but it's a *different app*, and you want to know now.
- **Fix**: One spike before Phase 1 — can `level-1-census` run from a plain `node`/CLI invocation outside a Claude session? Answer determines whether the trigger is autonomous or HITL.

---

## Important (resolve before the schema is built against)

### I1 — Three different ID conventions across the docs
| Doc | experiment ID | run ID |
|-----|--------------|--------|
| schemas.md (contract) | `exp-20260528-thumbnail-ideas` | `run-thumbnail-ideas-001` (experiment-keyed ✓ D2) |
| spec.md | `exp-2026-05-28-census-batch-1` (dashed date) | `run-<ISO date>-<seq>` (date-keyed ✗ D2) |
| plan.md | `exp-census-level1` (no date) | `run-census-2026-05-26` (date-ish ✗ D2) |
- **D2 locked experiment-keyed run IDs.** spec + plan violate it. And all three disagree on experiment-ID shape.
- **Fix**: `schemas.md` is the contract — adopt `exp-YYYYMMDD-<slug>` and `run-<exp-suffix>-NNN` everywhere. Correct spec §7.2 and plan §2.1.

### I2 — `duration_ms` vs `duration_seconds`
- schemas.md uses `duration_ms` (with a documented dissent). spec.md AC-4 still says `duration_seconds`.
- **Fix**: schemas wins (`duration_ms`). Update spec AC-4.

### I3 — spec's seed YAML is invalid against its own schema
- schemas.md `workflow.type` enum = `workflow_tool | manual | shell`.
- spec.md §8 and plan.md §2.1 seed experiments use `type: experiment` — not in the enum.
- **Fix**: seed should be `type: workflow_tool, harness: .claude/workflows/level-1-census.workflow.js`.

### I4 — Run file path disagreement
- schemas.md: `data/runs/<run-id>.json` + optional sidecar dir.
- plan.md §0.3: `data/runs/<run_id>/run.json + log.txt` (dir-per-run).
- **Fix**: pick dir-per-run (plan's is better — logs live with the run). Update schemas §5.

---

## Nits / FYI

- **Nit**: spec.md §11 success criterion 6 ("Mochaccino 09 no longer primary surface") is a behavioural outcome, not a testable AC — keep as a goal, not an acceptance gate.
- **FYI (security)**: plan's shell-exec interpolates JSON into a command line (`--args '<json>'`) — a command-injection surface. Irrelevant under single-user v0, but the file-trigger decision (D1) removes it entirely. One more point for D1.
- **FYI**: `index.json` is in schemas (§5) from day 1 but plan defers it to Phase 4. Fine — the plan's glob-first approach is correct for v0 volumes; just don't let the schema imply it's required earlier.

---

## What's genuinely strong (approve, keep)

- **Read-mostly stance** (schemas §6.1) — Watchtower mutates only decision + promotion records. Excellent, and consistent with D3. This is the design's backbone.
- **Decision-queue-as-only-landing** (plan Phase 4, User-First graft) — the correct structural answer to the N=1,150 overwhelm. The "no screen renders >50 records" hard rule is the right discipline.
- **Three separate fields, never one overloaded `status`** (schemas §2.1.1, §8) — clean state modelling.
- **Aggressive, explicit out-of-scope** in all three docs — scope discipline is real here.
- **Back-fill batch-0 as a synthetic experiment** (plan Phase 2, MVP graft) — solves the empty-state problem cheaply.

---

## Required actions before build

1. **Re-phase plan.md §0.1 + §1** around file-trigger (C1).
2. **Spike the headless-execution question** (C2) — blocks Phase 1.
3. **Unify IDs to schemas.md convention** across spec + plan (I1, I2, I3, I4).

Items 1 and 3 are doc edits (~30 min). Item 2 is a ~30-min spike. After those, the design is ready to build.
