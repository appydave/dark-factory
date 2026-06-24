# Eval Architecture — The Two Eval Surfaces (Map, Not a Spec)

**Purpose**: One map that names Dark Factory's **two distinct eval surfaces**, points each at the spec that already owns it, and flags the two genuine gaps that nothing covers yet. This is an index + gap register, not a new spec — the specs already exist.

**For Agents**: Read this to orient before touching anything eval/observability-related. It tells you which existing spec owns the work and what is genuinely unbuilt, so you don't duplicate `stability-1-instrument-loop` or `df8-comparison-registry`.

**Methodology source of truth**: `~/dev/ad/brains/evals/` (provider/project-agnostic). This doc is the *application* of that brain to Dark Factory. Update the brain for "how to eval"; update this doc for "how Dark Factory evals".

**Created**: 2026-06-24
**Last Updated**: 2026-06-24

---

## The reframe: there are TWO things here both called "evals"

```
SURFACE 1 — ARTIFACT EVAL   (is this SKILL/agent/command worth adopting?)
   L1 census → L2a triage → L2b rollout → L3 distill → L4 ratify   (+ DF-8 comparison)
   grades work PRODUCTS entering canonical/

SURFACE 2 — LOOP EVAL       (does the dispatch FACTORY run correctly?)
   queue → claim → run → record → done  + failures/register.jsonl + proof/
   grades the Marshall→Swagger→workflow MACHINERY itself
```

Conflating these is the main source of confusion. State which surface you mean before designing anything. (Methodology: `~/dev/ad/brains/evals/agentic-eval-fundamentals.md` § two surfaces.)

---

## Surface 1 — Artifact eval (mostly specced)

| Stage | Owner / artifact | State |
|-------|------------------|-------|
| L1 census | `level-1-census.workflow.js` → `research/census.jsonl` | running (batches 0–1 done) |
| L2a triage | `research/evaluations/*.md` | 88 files, PROVISIONAL |
| **L2b rollout** | *(run skill on held-out tasks, score outputs)* | **unbuilt — known gap** |
| L3 distillation | `research/distillations/*.md` | 76 files, PROVISIONAL |
| L4 ratification | `docs/canonical-form-spec.md` + `docs/provenance-spec.md` (HITL) | 0 ratified yet |
| Pairwise/N-way comparison | **`backlog/specs/df8-comparison-registry-spec.md`** | spec-written, build-later |

→ L2b and the DF-8 comparison registry are the artifact-side promote/demote evidence. **DF-8 already covers shadow-run comparison** (with anti-bias `task_type` + `bias_caveat`). Don't re-spec it.

## Surface 2 — Loop eval (already specced in depth)

| Concern | Owner / artifact | State |
|---------|------------------|-------|
| External trace capture (fixes DF-3 bookkeeping-skip) | **`backlog/specs/stability-1-instrument-loop-spec.md`** | spec-written, build-later |
| Failure taxonomy (process-eval by exception) | `experiments/watchtower-engine/failures/register.jsonl` + `docs/systemic-fixes.md` | live, ~17 categories |
| Behavioural proofs (N=1) | `experiments/watchtower-engine/proof/*.md` | live |
| Resource/health telemetry | `backlog/2026-06-06-observability.md` | open |
| Run records | `experiments/watchtower-engine/runs/*.json` | live but worker-written (unreliable) |

→ `stability-1-instrument-loop-spec` **already is** the "enforce traces externally" work, including the externality principle ("you cannot ask the thing that's failing to report on its own failure"). Don't re-spec it. The failure register is already a process-eval taxonomy — it just needs surfacing as a *trending metric* (covered by stability-1 §12–13).

---

## The TWO genuine gaps (nothing owns these yet)

Everything above is specced or live. These two are not:

### Gap A — Golden-job regression suite
There are 35+ runs in `done/`, but no frozen set replayed on every machinery change to catch "a change to C2 silently broke C1".
- **Shape**: pick ~5 canonical jobs; freeze expected outcome + cost/step envelope + trajectory shape; replay + diff on each change. The loop's CI gate.
- **Depends on**: stability-1 traces landing first (need reliable traces to diff against).
- **Methodology**: `~/dev/ad/brains/evals/eval-harness-and-metrics.md` § golden-job regression.

### Gap B — LLM-judge calibration against the mocha-census labels
L1 census, L2a triage, and `tools/design-lint/` all run **LLM-judges**, but none are calibrated or version-pinned — so judge drift moves scores while artifacts stay still.
- **The asset hiding in plain sight**: `tools/mocha-census/out/ratings/*.json` (David's love/good/average human labels) is a ready-made **calibration set**.
- **Shape**: pin judge model+version; score judge agreement against those human labels before trusting it; re-check on judge upgrades. `design-lint`'s "only 4 reliable flags" instinct is already the right Goodhart-avoidance.
- **Methodology**: `~/dev/ad/brains/evals/eval-harness-and-metrics.md` § LLM-as-judge.

---

## At a glance

```
Surface 1 (artifact):  L1–L4 ✅specced · L2b ❌gap-ish · DF-8 compare ✅specced
Surface 2 (loop):      stability-1 traces ✅specced · failure register ✅live · observability ✅open
GENUINE GAPS:          A) golden-job regression suite   B) judge calibration vs mocha-census
```

Build priority (my read, defer to PO): Gap B is cheap and high-leverage (calibration set already exists). Gap A waits on stability-1 traces landing. Both reference the methodology in `~/dev/ad/brains/evals/` rather than restating it.
