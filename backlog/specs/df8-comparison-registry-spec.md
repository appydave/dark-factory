# DF-8 — Adversarial-Delta Comparison Registry (`research/comparisons.jsonl` + `catalog:compare`)

**State:** spec-written · build-later · priority 3 (serves the 1100; build when the census/distillation campaign spins up)
**Origin:** 2026-06-09 — David asked "how do we centrally track these comparisons (skill-vs-skill and beyond), or does skill-vs-skill need its own structure?" after the first deliberate adversarial delta (`df7-osmani-vs-appydave-delta.md`). Evaluated via bg agent (read the corpus). See memory `adversarial-delta-technique`.

## Decision
**Pairwise/N-way COMPARISON is a distinct primitive** from the 1100's existing single-artifact-absolute structures — confirmed: a **tier-5 / `adopt` artifact LOST** the DF-7 head-to-head, a fact that cannot be derived from per-artifact rows (the absolute scores don't disagree; the signal lives only in the contest). Build **ONE general comparison registry for all artifact types — NOT a skill-vs-skill special case** (the record is type-agnostic; only the operands differ).

## Gap (existing structures, all single-artifact-absolute) — verified
- `research/census.jsonl` — `{artifact_id, quality_tier, verdict(adopt/evaluate/drop), verdict_reason, ...}`. No `vs`/`winner`/`compared_to`.
- `research/evaluations/*.md` — per-artifact dimensional scorecard; `capability-evaluate.md` line 97 **forbids** cross-artifact comparison.
- `research/distillations/*.md` — N-way `source_artifacts[]` → `winner_mechanism` + MERGE; discards the dimensional contest + any bias caveat. Answers "what's the unified skill," not "is A better than B, where."
- `tools/mocha-census/out/ratings/*.json` — single-design `{rating, label}`; `round-03-result.json` self-flags absolute-tier drift and says relative order is the trustworthy signal → the corpus already wants a relative primitive.

## Schema — `research/comparisons.jsonl` (one row per contest)
```
{
  "comparison_id": "cmp-YYYYMMDD-<slug>",
  "artifact_type": "skill|agent|workflow|design|impl",   // OPERAND type
  "operands": [ {"ref": "...", "census_id": "<census row id|null>", "path": "..."}, ... ],  // 2+ (pairwise or N-way)
  "task_context": "<free text>",          // REQUIRED — what the contest ran on
  "task_type": "greenfield|existing-app-addition|...",   // REQUIRED controlled vocab — the bias axis
  "dimensions": [ {"name": "...", "winner": "<operand ref>"}, ... ],
  "tally": { "<ref>": <int>, ... },
  "verdict": "...",
  "recommendation": "...",
  "bias_caveat": "...",                    // REQUIRED — why this result may not generalize
  "validity": "provisional-single-task|corroborated|contested",  // default provisional
  "delta_doc": "<path to full prose delta>",
  "assessed_at": "YYYY-MM-DD", "assessed_by": "..."
}
```

## Relationship to census (MVC, no duplication)
Comparisons are the **relational layer that references INTO** census (`operands[].census_id`, nullable so non-corpus operands like `appydave:spec-writer` are allowed). Census stays the breadth/absolute ledger; a board/view JOINs the two (standalone tier + head-to-head). Data-first like `tickets.json` + the mocha gallery.

## Capability
Add **`catalog:compare`** to the `dark-factory-catalog` skill — the missing 3rd verb between `evaluate` (single-artifact) and `distill` (merge). The delta doc is the *test payload*; the registry + verb is the *machine* (millwright call).

## Anti-bias (load-bearing — David's "home-turf win" worry)
`task_type` + `bias_caveat` REQUIRED; `validity` defaults to `provisional-single-task`; promotes to `corroborated` ONLY after the same operand pair is compared on a DIFFERENT `task_type`. Board groups on operand-pair × task_type — the empty cell (e.g. "greenfield: UNKNOWN") is the explicit signal that a verdict isn't safe to generalize. A single biased run can never silently become a corpus-wide conclusion.

## Build form (when greenlit)
Candidate machines: a bench/comparison `workflow.js` (judge-panel shape) · the millwright judge-panel pattern · generalize `mocha-census` bench mode (already this shape for designs). Decide at build time.
