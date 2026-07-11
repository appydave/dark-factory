# Backlog — First Ingestion: `code-review`

**Target**: `canonical/skills/code-review/` — David's canonical code-review skill, mined from the convergence cluster.

**Priority**: First — proves the ingestion workflow end-to-end before scaling to other artifacts.

**Created**: 2026-05-18
**Status**: open
**PO**: David (via brain session 2026-05-18)

---

## Why this one first

The code-review cluster is the **convergence zone** of the corpus — 135 artifacts across 11 repos all solving the same problem with different mechanisms. compound-engineering contributes 40 (its reviewer suite), David's own appydave-plugins contributes 27 (his review-* family + delivery-review orchestrator), agent-skills-osmani contributes 6.

If the ingestion workflow handles this case cleanly — convergent cluster + David already has substantial existing work in this space — it'll handle everything else. Failing here means the workflow spec needs amendment before scaling.

## Distillation source (read first)

- `research/distillations/code-review-dimensional-specialist.md` — the unified-skill draft for single-axis specialist reviewers (David's existing pattern, with depth calibration folded in from compound-engineering)
- `research/distillations/INDEX.md#code-review-cluster` — the cluster-level synthesis with all 6 sub-clusters

For this backlog item, focus on `dimensional-specialist`. We're producing **one canonical skill — `code-review`** — that captures David's review-pattern at the specialist level. The orchestrator (`delivery-review`) is a separate ingestion (later backlog item).

## Origins to harvest

Per the distillation, the winner mechanism is `compound-engineering:ce-adversarial-reviewer` with folds from others. Harvest verbatim into `_source/`:

1. **Primary winner**: `~/dev/upstream/repos/compound-engineering-plugin/plugins/compound-engineering/agents/ce-adversarial-reviewer.agent.md`
2. **Major fold-in (depth calibration)**: `~/dev/upstream/repos/compound-engineering-plugin/plugins/compound-engineering/skills/ce-code-review/SKILL.md`
3. **Voice anchor (David's existing specialists)**:
   - `~/dev/ad/appydave-plugins/appydave/skills/review-blind-hunter/SKILL.md`
   - `~/dev/ad/appydave-plugins/appydave/skills/review-edge-case-hunter/SKILL.md`
   - `~/dev/ad/appydave-plugins/appydave/skills/review-code-quality/SKILL.md`
4. **5-axis framework**: `~/dev/upstream/repos/agent-skills/skills/code-review-and-quality/SKILL.md`

David's existing review-* skills are read for VOICE/PATTERN — they're not "origins" in the provenance sense (they're already canonical-ish in his stack). Note them in provenance.json under `voice_anchors[]` (extension field — fine to add) but don't copy them into `_source/` since they're already in David's repos.

## Research sources to consult

- `research/evaluations/agent-skills-osmani__skill__code-review-and-quality.md` (quality 5/5, mineable phrase about the 4-question gate)
- `research/evaluations/compound-engineering__agent__ce-adversarial-reviewer.md` (if exists; otherwise nearest)
- `research/evaluations/compound-engineering__skill__ce-correctness-reviewer.md`

## Acceptance criteria

Backlog item is done when:

- [ ] `canonical/skills/code-review/SKILL.md` exists, follows `canonical-form-spec.md`, is in David's voice (mimic `review-blind-hunter` for tone)
- [ ] `canonical/skills/code-review/_source/` contains verbatim copies of all 4 numbered origins (with David's voice-anchor skills noted in provenance but not copied)
- [ ] `canonical/skills/code-review/provenance.json` validates against `provenance-spec.md`, with `rewrite_status: "ratified"`
- [ ] Frontmatter has all 4 fields (`name`, `description`, `argument-hint`, `allowed-tools`). `allowed-tools` should match what David's existing reviewers use.
- [ ] Description is trigger-only with 3+ phrases (mimic David's existing reviewer descriptions)
- [ ] `canonical/INDEX.md` updated with the new entry
- [ ] **Folds in**: depth calibration (Quick/Standard/Deep based on diff size) from `ce-code-review`
- [ ] **Folds in**: 4-question pre-report gate (cite line, name failure, read context, defend severity) from `code-review-and-quality`
- [ ] No stack-specific terminology in body
- [ ] Backlog item moved to `backlog/done/`

## Open questions for PO (David)

1. Should the new `code-review` canonical **replace** David's existing review-blind-hunter / review-edge-case-hunter etc., or **complement** them as a new dimensional specialist? (Recommendation: complement initially — make this a single new canonical that adds the depth-calibration + 4-question-gate patterns; David decides later whether the existing specialists get upgraded to inherit these patterns.)
2. Is the orchestrator (`delivery-review`) a follow-on backlog item, or does it stay as-is in David's stack since today's improvements are at the specialist layer?
3. What's the `name` field — `code-review` (clean, but conflicts conceptually with David's existing review-* names) or `review-dimensional` (clearer it's a specialist not an orchestrator)?

If David doesn't answer before execution starts, default to: complement existing, name = `review-dimensional`, orchestrator stays put.

## Execution hint

Don't try to do everything in one session. Reasonable split:

- **Session 1**: harvest verbatim + draft provenance + read voice anchors. Stop. Hand back to PO with a "draft ready for voice review" message.
- **Session 2**: write SKILL.md in David's voice, validate, ratify.

This is a learning run — the workflow itself is being proven. Move slowly, document any spec gaps you hit, propose amendments in a follow-up backlog item.

## Status

**Session 1 complete** (2026-07-11, via `wg-t3-01-first-ingestion-review-dimensional`, war game `backlog/wargames/T3-01-first-ingestion-review-dimensional.md`).

- Artifact: `canonical/skills/review-dimensional/` — the three open questions above are answered by decisions.md Q9 (2026-07-06 war-game portfolio triage): name = `review-dimensional`, complement (don't replace) David's existing review-* skills, `delivery-review` untouched.
- Status: `in-style` (harvested + drafted, not yet ratified). `canonical/INDEX.md` carries an in-progress row.
- **Session 2** (voice-review + ratify + HITL) = `wg-t3-02` if it exists by the time you read this; otherwise the checklist in `backlog/wargames/proof/T3-01/REPORT.md` is the manual handoff.
- This backlog item stays **open** — it closes at ratification, not at Session 1.

## Result

**RATIFIED 2026-07-11** (Session 2, via `wg-t3-02` + David's HITL decision).

`canonical/skills/review-dimensional/` is the factory's **first ratified canonical artifact** — the
7-week-empty `canonical/` now holds artifact #1. Both automated inspectors pass:
`tools/verify-provenance.py` → 1 pass / 0 fail (R1–R8), `tools/style-check.py` → pass.

David's decision: **redirect → table-ize the Confidence rubric to match the Depth-calibration table,
apply the `_source` directory-bundle restructure (dropping the non-spec `verbatim_copy_companions`
field that caused 3 orphan-file flags), then ratify.**

Process note: the engine could **not** complete the ratification apply — the HITL/ratification pipeline
misread the designed decision-pause as "wedged," and the multi-step apply never finished in a worker
window (3 failed attempts). The fixes were applied by the PO seat as one-time recovery; the
HITL/ratification-pipeline gap is ticketed for the post-moratorium rebuild.
