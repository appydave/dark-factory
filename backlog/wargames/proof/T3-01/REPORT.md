# T3-01 Session-1 Report — first ingestion: `review-dimensional`

**Ticket**: `wg-t3-01-first-ingestion-review-dimensional` · **War game**: `backlog/wargames/T3-01-first-ingestion-review-dimensional.md`
**Run date**: 2026-07-11 · **Result**: `in-style` draft shipped. No abort.

---

## What was harvested

3 origins, byte-identical verbatim copies, all diffs empty:

| Origin | Path | Commit |
|---|---|---|
| Winner — `ce-adversarial-reviewer` | `_source/compound-engineering--ce-adversarial-reviewer.agent.md` | `compound-engineering-plugin@39cb9da3` |
| Fold — `ce-code-review` (+ 9-file `references/` companion bundle) | `_source/compound-engineering--ce-code-review.md` + `_source/compound-engineering--ce-code-review--references/` | `compound-engineering-plugin@39cb9da3` |
| Fold — `code-review-and-quality` | `_source/agent-skills-osmani--code-review-and-quality.md` | `agent-skills@f17c6e8` |

Voice anchors read (not copied — already in David's stack, recorded as `voice_anchors[]` in provenance): `review-blind-hunter`, `review-edge-case-hunter`, `review-code-quality`, and `code-quality/references/lenses.md` (the post-refactor single source these three now alias into).

## The draft's shape

`canonical/skills/review-dimensional/SKILL.md` — 64-line body, frontmatter has all 4 required fields, `allowed-tools: Read, Grep, Glob, Bash` (`Write` dropped from the winner's tools line — reviewers never write). Sections: Behavior (scope → size/risk estimate → depth-calibrated hunt → validate-completeness → report), Depth calibration table (Quick/Standard/Deep), Axis territory, Confidence rubric (100/75/50/suppress-≤25), Output (normalized `{AXIS}-NNN` findings + 4-question pre-report gate + verdict line), Anti-patterns, Halt conditions.

`provenance.json`: 3 origins, `rewrite_status: "in-style"`, each origin's `kept`/`modified`/`set_aside` refined to match what actually shipped in the body (not just the distillation's seed table).

`tools/style-check.py canonical/skills/review-dimensional` → **pass, no findings.**

## Findings (mandatory + discovered)

1. **May-18 backlog item's eval-file references are stale.** It names `research/evaluations/agent-skills-osmani__skill__code-review-and-quality.md` (double-underscore form) and two compound-engineering eval files. Actual files on disk use hyphen naming (`agent-skills-osmani-skill-code-review-and-quality.md`, `agent-skills-osmani-agent-code-reviewer.md`); no compound-engineering code-review evals exist at all (only ce-compound-refresh / ce-compound / ce-optimize). Used the two real files. The backlog item was written before recon settled on final naming — a documentation-lag artifact, not a decision to revisit.

2. **David's review-* skills are now thin aliases, not full specialists.** `review-blind-hunter`, `review-edge-case-hunter`, `review-code-quality` are ~15-20 lines each, pointing to `code-quality/references/lenses.md` as the single-sourced lens definition. The May-18 brief and the war game were written assuming full-bodied specialists as the voice anchor. Read `lenses.md` too, per the war game's Recon 5 update — it's now part of the voice-anchor set. **This is also Assumption 4 in the war game materializing partially**: `lenses.md`'s BH lens already has "<3 findings → re-examine" and CQ/AR/UT already have depth variants (fast/deep) — so review-dimensional's depth calibration and confidence rubric are genuinely NEW capability on top of lenses.md, not duplicative. The overlap is real but partial: lenses.md has fast/deep, not the finer 3-tier Quick/Standard/Deep with explicit line-count thresholds, and none of the 6 existing lenses have an anchored numeric confidence rubric. Flagging for David's Session-2 read as directed.

3. **provenance-spec.md's own schema example contradicts its field-rule table.** The example's `source_repo` is `"compound-engineering-plugin"`; the field-rule row says `source_repo` "matches a repo in `research/recon/<repo>.md`" — which resolves to `"compound-engineering"` (confirmed: no `research/recon/compound-engineering-plugin.md` exists, only `compound-engineering.md`... verify this filename if precision matters at ratification). Followed the field rule, not the example, per the war game's explicit call.

4. **The "4-question pre-report gate" the war game (and the original May-18 backlog item) attribute to `code-review-and-quality` does not exist verbatim in that file.** Grepped `agent-skills/skills/code-review-and-quality/SKILL.md` for "cite", "defend", "4-question", "pre-report" — zero hits. The actual closest analog on disk is `ce-code-review.md`'s **"Quality Gates"** section (6 items: actionable findings, no false positives from skimming — read the surrounding context, calibrated severity, accurate line numbers, protected artifacts respected, no linter-duplicate findings). I condensed that 6-item CE gate into the 4-question framing the brief described (cite a real line / name a concrete failure / confirm context was read / defend the severity) and folded it from `ce-code-review`, not `code-review-and-quality`. `provenance.json`'s origin-2 `modified[]` documents this explicitly. **This is a genuine misattribution in the research layer (distillation + backlog item both say "from code-review-and-quality") that should be corrected at the distillation source**, not just patched here.

5. **`tools/verify-provenance.py`'s R4 orphan-file rule cannot represent a bundled companion (file + `references/` dir) under one origin.** The rule reads a single-string `verbatim_copy` per origin and marks anything else in `_source/` not covered by SOME origin's path as an orphan. `provenance-spec.md` itself documents two valid conventions for a multi-file origin — nest everything under one subfolder, OR note the companion in prose/an extension field — but the validator code only implements neither: it has no support for an array `verbatim_copy` (fails R3 if given one) and doesn't read any `verbatim_copy_companions`-style extension field. Given this ticket's fixed, ticket-mandated flat `_source/` layout (`compound-engineering--ce-code-review.md` as a sibling file next to `compound-engineering--ce-code-review--references/` as a sibling dir — required by both the ticket's own verify text and the war game's M2 script, and already verified byte-identical), and the war game's own "exactly 3 origins" instruction (M3), there is no way to make `python3 tools/verify-provenance.py canonical/skills/review-dimensional` return 0 FAILs without either (a) violating the 3-origins constraint, (b) restructuring `_source/` against the ticket's explicit layout, or (c) editing `tools/verify-provenance.py` (out of this ticket's scope fence). **Current state: `verify-provenance.py` reports 9 R4 FAILs**, all naming the 9 files under `_source/compound-engineering--ce-code-review--references/` as orphans. `style-check.py` is unaffected and passes clean. Recommend either: extend `verify-provenance.py` to accept a `verbatim_copy_companions[]` array field (least invasive), or amend `provenance-spec.md` to mandate the nested-subfolder convention project-wide (more invasive — would also require reworking this ticket's own required flat filenames). This is a tooling gap, not a defect in this artifact's provenance — every file in `_source/` genuinely is a verbatim, traceable copy; the validator just can't see the trace for the bundle.

6. **`david-style-patterns.md` is thinner than the live skills it should anchor.** The seed doc's Template A/B match the live aliases reasonably well, but the doc doesn't yet capture the `lenses.md` consolidation (finding #2) or the fast/deep depth-variant pattern already live in `AR`/`CQ`/`UT`. Per the doc's own "To be expanded" note, this is expected — flagging as a candidate append once T3-02 ratifies review-dimensional (it'll be the first artifact to actually exercise and validate the seed doc's patterns).

## Session 2 checklist (for David / `wg-t3-02`)

- [ ] Voice review of `canonical/skills/review-dimensional/SKILL.md` — does the condensed Behavior/Output read as your operator voice, or does it need another pass?
- [ ] Ratify decision — flip `provenance.json` `rewrite_status` to `"ratified"` once satisfied (or send back for a revision round).
- [ ] `allowed-tools` call — confirm dropping `Write` (Assumption 2 in the war game) is correct; one-line frontmatter revert if not.
- [ ] Decide on Finding 5 (validator gap) — extend `verify-provenance.py`, amend the provenance-spec convention, or accept the known R4 FAIL as permanently out of scope for bundled-companion origins. This blocks a clean ratification run of `python3 tools/verify-provenance.py` regardless of SKILL.md quality.
- [ ] Decide on Finding 2 (lens overlap) — is review-dimensional's depth calibration + confidence rubric worth retrofitting onto the 6 existing lenses in `lenses.md`, or does it stay a distinct, newer pattern?
- [ ] `canonical/INDEX.md` flip — in-progress row → ratified row + date, once ratified.
- [ ] `backlog/2026-05-18-first-ingestion-code-review.md` close — move to `backlog/done/` with a `## Result` section, only at ratification.
- [ ] Consider a `david-style-patterns.md` correction pass (Finding 6) once review-dimensional is the first ratified exemplar of its pattern.
- [ ] Consider a correction to `research/distillations/code-review-dimensional-specialist.md` for Finding 4 (the misattributed 4-question-gate source).
