# Phase B — Next Steps

**Status**: thinking / not started
**Last updated**: 2026-05-25
**Context**: Spikes R11/R12/R13/R14 all verified PASS. Workflow Tool + MCP Blackboard pattern confirmed working. Phase B is unblocked.

---

## What Phase B is

Build the ingestion automation — two workflows that turn a backlog item into a ratified canonical skill:

1. **`prepare-ingestion-brief.workflow.js`** (small, validates the fan-out read pattern)
   - Reads a backlog item, extracts paths to distillations + evaluations
   - Fans out in parallel to read all relevant research files
   - Synthesizes a consolidated brief and writes it to disk
   - Output: `experiments/ingestion-runs/<slug>/brief.md`

2. **`ingest.workflow.js`** (the transpiler — automates the 11-step ingestion procedure)
   - Reads the brief
   - Locates and copies origin files verbatim to `canonical/<name>/_source/`
   - Drafts `provenance.json`
   - Rewrites `SKILL.md` in David's voice
   - Validates against spec checklists
   - Ratifies, registers in `canonical/INDEX.md`, closes backlog item

First run target: `backlog/2026-05-18-first-ingestion-code-review.md` → `canonical/skills/review-dimensional/`

---

## Open questions before starting

### 1. The "David's voice" problem

`docs/david-style-patterns.md` exists and has reasonable rules (8 voice rules, 3 structural templates, rewrite examples). But it was derived by reading existing skills — it has never been validated by actually producing a canonical artifact.

The first canonical (code-review) is as much a test of the voice model as it is a test of the pipeline. The workflow will produce a draft; David reviews it; corrections fold back into `david-style-patterns.md`.

**To think about**: Is the first run meant to be fully automated to ratification, or does it stop after draft for a manual voice-review step? The backlog item recommends: Session 1 = harvest + draft, Session 2 = voice review + ratify.

### 2. PO decisions for code-review ingestion

From `backlog/2026-05-18-first-ingestion-code-review.md`:

- **Replace or complement?** New canonical `review-dimensional` alongside existing `review-blind-hunter` / `review-edge-case-hunter`, or does this eventually supersede them?
  - Default if not answered: complement (add new canonical, existing skills unchanged)
- **Name**: `code-review` (clean, generic) or `review-dimensional` (clearer it's a specialist not orchestrator)?
  - Default if not answered: `review-dimensional`
- **Orchestrator**: Does `delivery-review` (the fan-out orchestrator) get updated to call the new canonical, or stay as-is?
  - Default if not answered: leave it, that's a separate backlog item

### 3. HITL in the workflow

The 11-step procedure has a natural human review point between draft and ratify. The Workflow Tool supports HITL via agent + user interaction. For Phase B, decide: fully automated to ratification, or hard pause before ratify?

---

## Files to read when starting

- `docs/ingestion-workflow.md` — the 11 steps in detail
- `docs/canonical-form-spec.md` — the contract for canonical artifacts
- `docs/provenance-spec.md` — provenance.json schema
- `docs/david-style-patterns.md` — voice rules + templates (the seed — update after first run)
- `backlog/2026-05-18-first-ingestion-code-review.md` — the first target, with origins + acceptance criteria
- `docs/architecture.md` §12 — Phase B in context of the full roadmap

---

## Why this matters

At 1,100 artifacts, manual ingestion isn't feasible. One successful automated run proves the pipeline. After that, scaling is a queue problem not a skill problem.

The mechanical steps (harvest verbatim, write provenance, validate checklist) are automatable. The creative step (rewrite in David's voice) is where the workflow needs to produce a good enough draft that human review takes minutes not hours.
