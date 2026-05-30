# Watchtower v0 — Locked Decisions

**Decided**: 2026-05-30 by David
**Status**: binding — supersedes any conflicting recommendation in schemas.md / spec.md / plan.md

These four were the only decisions blocking the build. The three design agents disagreed; David ruled.

---

## D1 — Workflow trigger: **file-trigger + watcher**

Watchtower writes `<id>.yml` + `<id>.trigger`; a separate harness watcher claims and runs it.

- **Why**: decoupled, restartable, the files are the audit trail. Survives app crash mid-run.
- **Rejected**: shell-exec (App spawns the command directly) — fragile progress reporting, lost thread on restart.
- **Source**: Agent A (api-and-interface-design).
- **Implication**: Phase 1 builds the watcher + trigger-file contract, not a subprocess spawn.

## D2 — Run ID convention: **experiment-keyed**

`run-census-001`, `run-census-002`. Parent experiment readable from the ID.

- **Rejected**: date-keyed (`run-2026-05-30-001`).
- **Source**: Agent A.

## D3 — Promotion: **record decision only**

Clicking "Promote" writes a `promotion.yml` recording the verdict. A human performs the actual `canonical/` edit later.

- **Why**: v0 cannot corrupt the source-of-truth library. Clean line: v0 is a decision recorder, not a library mutator.
- **Rejected**: Promote writes straight into `canonical/`.
- **Source**: Agent A (Hyrum's-Law reasoning).
- **Implication**: Watchtower has NO write access to `canonical/` in v0.

## D4 — Swagger: **buttons only for v0**

Click to run, click to decide. No conversational layer.

- **Why**: ships the control surface fast. The 6 specialist roles (Architect/Builder/Runner/Evaluator/Learning Miner/Promoter) stay as concepts; only Runner + Evaluator outputs surface in v0.
- **Rejected**: build conversational Swagger now.
- **Source**: Agent B (spec-driven-development).

---

## What these decisions settle downstream

- Watchtower is **read-mostly**: only mutates `experiment.decision.chosen` and `promotion` records (D3).
- Three distinct fields, never one overloaded `status`: execution status / David's decision / promotion record.
- Integration is file-based (D1) — no MCP, no subprocess in v0. MCP is a purely additive upgrade later.
- First vertical slice remains **census-batch-1**, not thumbnail ideation (all three agents agreed).

## Still open (non-blocking — decide during build)

- Rerun semantics: mutate the experiment record vs clone it.
- Can a learning be a promotion candidate independently of its parent experiment?
- `research/*.jsonl` ↔ `data/` boundary: does the census workflow write to the frozen corpus or to Watchtower's data dir? (Leaning: census keeps writing to `research/census.jsonl`; Watchtower reads it and maintains its own experiment/run records alongside.)

## Deferred to other systems

- **Skill usage telemetry** (used vs stale): owned by AngelEye via session hooks, not the census. Not a Watchtower concern.
