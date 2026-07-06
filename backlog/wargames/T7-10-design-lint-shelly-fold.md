# T7-10 — design-lint → Shelly fold + census bench verify

| field | value |
|---|---|
| ticket | wg-t7-10-design-lint-shelly-fold |
| track / size / priority | T7 Self-learning / S / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Execute the David-ratified fold (decisions.md Q9): the **judgment half of design-lint moves into
Shelly** as her automated self-review mode. Concretely: copy the rubric verbatim into
`~/dev/ad/appydave-plugins/appydave/skills/shelly/references/design-lint-rubric.md`, add a
`lint-render` command to Shelly's SKILL.md, point Mochaccino's Review section at it as the
automated sibling of human `review`, and demote dark-factory's `tools/design-lint/` to a
mechanical-staging remnant (shoot-one.py stays; RUBRIC.md becomes a pointer stub). Second half of
the ticket: **verify on disk whether mocha-census bench-mode / export-to-file / generator-seam
ever landed** (authoring recon says all three did NOT — confirm at execution time and record).
Done = Shelly self-lints by documented command, the 2026-06-10 placement question is closed as
resolved-by-Q9, the census verification is recorded, and both repos are committed and pushed.
This ticket builds NOTHING new — no bench mode, no batch workflow, no generator wiring; it folds
existing capability and records truth.

## Locked context

- **Q9 (decisions.md):** "design-lint→Mochaccino/Shelly" — the fold is the accepted default.
  This IS the "separate, asked-for step" that `tools/design-lint/README.md` and dark-factory
  CLAUDE.md required before touching appydave-plugins; David asked for it via the Q9 interview.
- **Q4 (decisions.md):** everything through the engine — this war game is written for sonnet
  Swagger dispatch; the work itself is markdown edits + git in two repos, no engine changes.
- **Rubric hard guardrails carry over verbatim:** flags only, no auto-fix, never policing
  diagram/colour counts (the round-04 Goodhart trap). The fold must not soften these.
- **No `-p`/headless/SDK ever; interactive `claude` only** — moot here: no Claude is spawned and
  no lint is actually run by this ticket.
- **No YLO/POEM work** — out of scope entirely.
- **Docs lag code** (wargame-spec) — every claim below was verified on disk 2026-07-06; your
  Recon re-verifies at execution time and disk beats any README sentence.
- **Canonical source-of-truth convention (global prefs):** one file owns each piece of knowledge.
  After the fold the operational rubric is owned by Shelly's references copy; the design SPEC
  stays owned by dark-factory `docs/david-design-patterns.md` (chain: spec → rubric extract).

## Recon (verify before any work)

`DF=/Users/davidcruwys/dev/ad/apps/dark-factory` · `PL=/Users/davidcruwys/dev/ad/appydave-plugins`.
Run every check.

1. `ls $DF/tools/design-lint/` → expect `README.md  RUBRIC.md  out  shoot-one.py` (state
   2026-07-06). RUBRIC.md or the directory missing → **Abort A1**.
2. `grep -c "colour-overload" $DF/tools/design-lint/RUBRIC.md` → expect ≥2 (F4 heading + output
   schema). Also confirm all four flag codes present: `cool-on-content`, `missing-warm-anchor`,
   `amber-orange-on-brown`, `colour-overload`. Any missing → the rubric moved under you →
   **Abort A1**.
3. `ls $PL/appydave/skills/shelly/` → expect `SKILL.md  references/` (references/ holds only
   `shape-catalog.md` at authoring). Then `grep -ci "lint" $PL/appydave/skills/shelly/SKILL.md`
   → expect **0** (verified 2026-07-06: Shelly is shapes + components + graphics-warrant gate,
   no lint). Non-zero → someone already folded (or half-folded) → **Fork F1**.
4. `grep -n "## Review Command" $PL/appydave/skills/mochaccino/SKILL.md` → expect 1 hit
   (~line 228; the section says review is "lightweight, always optional, never a gate"). Missing
   or the skill restructured with no Commands/Review section → **Abort A2**.
5. Census three-claims check (this is half the ticket's mission — record each result):
   a. `grep -rn -i "bench" $DF/tools/mocha-census/*.py $DF/tools/mocha-census/*.sh` → expect
      **0 hits** (bench mode is README-"planned" only; verified 2026-07-06).
   b. `grep -n "export" $DF/tools/mocha-census/out/shots/gallery.html` → expect a
      `copy ratings JSON` button writing to the **clipboard** (~lines 92, 211) — i.e. rating
      ingest is still copy-paste, NOT export-to-file.
   c. `grep -rn -i "david-design-patterns\|exemplar" $PL/appydave/skills/mochaccino/ $PL/appydave/skills/mocha/`
      → expect **0 hits** (generator seam unwired: neither skill references the design spec or
      the love-tier exemplar pack).
   Any of a/b/c contradicted (feature actually landed) → **Fork F2** for that item.
6. `git -C $PL status --porcelain` → expect empty (clean at v6.1.0, 2026-07-06). Dirty anywhere
   under `appydave/skills/shelly/` or `appydave/skills/mochaccino/` → **Abort A3**; dirty only
   elsewhere → proceed but stage ONLY your files in Move 7.
7. `git -C $DF status --porcelain -- tools/design-lint tools/mocha-census backlog/2026-06-10-design-lint-placement-question.md`
   → expect empty. Dirty → **Abort A3**.
8. `ls $DF/backlog/2026-06-10-design-lint-placement-question.md` → expect present (the open
   placement question this ticket closes). Already renamed `.done.md` → treat as evidence of
   Fork F1 and check Recon 3's result again before deciding.
9. `ls $DF/docs/david-design-patterns.md` → expect present (the spec the rubric declares as its
   source of truth). Missing → **Abort A1** (the provenance chain you're documenting would dangle).
10. `python3 -c "import json;print(json.load(open('$PL/appydave/.claude-plugin/plugin.json'))['version'])"`
    → expect `6.1.0` (authoring state). Higher is fine (other tickets land in parallel) — just
    bump minor from whatever you find in Move 7.

## Moves

1. **Do:** Record the census verification. Take the three Recon-5 results and write them into a
   short block you will reuse twice (Move 6 appends it to the closed backlog item; Move 7 puts a
   one-liner in the commit message). Format, exactly three lines plus a date header:
   ```
   ## Census claims verified on disk (wg-t7-10, <today's date>)
   - bench mode: NOT landed (no bench code in tools/mocha-census/*.py|*.sh; README "planned" is accurate)
   - export-to-file: NOT landed (gallery.html still clipboard "copy ratings JSON"; rounds are pasted to out/ratings/)
   - generator seam: NOT wired (no david-design-patterns/exemplar reference in mochaccino or mocha skills)
   ```
   Adjust any line whose Recon-5 check contradicted authoring (per Fork F2). Do NOT edit
   `tools/mocha-census/README.md` if the claims verify as above — it already truthfully labels
   all three as planned/open.
   **Expect:** the block matches your Recon-5 observations exactly.
   **Failure signal:** a Recon-5 check was skipped or ambiguous (e.g. gallery.html missing).
   **Counter-move:** re-run the specific grep; if `out/shots/gallery.html` doesn't exist on this
   machine, say so in the block ("gallery.html absent locally — export mechanism unverifiable
   here, README claim stands") rather than guessing. If ALL THREE files/dirs are missing,
   mocha-census itself moved → **Abort A1**.

2. **Do:** Create `$PL/appydave/skills/shelly/references/design-lint-rubric.md`: the ENTIRE
   current content of `$DF/tools/design-lint/RUBRIC.md`, byte-for-byte below a provenance header
   you prepend:
   ```markdown
   <!-- Folded from dark-factory tools/design-lint/RUBRIC.md on <today's date> (wg-t7-10,
        decisions.md Q9). Source of truth for the RULES remains
        ~/dev/ad/apps/dark-factory/docs/david-design-patterns.md — when that spec sharpens,
        update this extract. The mechanical screenshotter (shoot-one.py) stays in
        dark-factory tools/design-lint/. -->
   ```
   Do not edit, soften, or "improve" the rubric body — verbatim copy only (note: the source file
   ends with a stray ``` fence on its last line; carry it as-is — fidelity beats tidiness).
   **Expect:** `grep -c "colour-overload" <new file>` gives the same count as Recon 2 gave for
   the source; `diff <(tail -n +7 <new file>) $DF/tools/design-lint/RUBRIC.md` is empty (adjust
   the tail offset to your actual header line count).
   **Failure signal:** diff shows body drift.
   **Counter-move:** re-copy with `cat`, don't retype. If the copy keeps drifting something
   environmental is wrong → **Abort A3** with the diff as evidence.

3. **Do:** Edit `$PL/appydave/skills/shelly/SKILL.md`, two surgical changes:
   **(a)** In the YAML `description`, after "extract this component"," insert the triggers
   `"lint this render", "self-lint", "design lint", "check this against the design spec",` —
   keeping the rest of the description untouched.
   **(b)** Add a new command section after `### add-component` (before the
   `## Shape Catalog (built-in patterns)` heading), exactly this shape:
   ```markdown
   ### lint-render
   Automated self-review of a RENDERED design — the machine sibling of Mochaccino's human
   `review`. Folded in from dark-factory `tools/design-lint/` (wg-t7-10, decisions.md Q9).

   1. Input: a screenshot PNG of the rendered page. If the caller hands you HTML instead,
      have them shoot it first — the portable screenshotter is
      `~/dev/ad/apps/dark-factory/tools/design-lint/shoot-one.py` (serves the page's dir on a
      throwaway port, writes the PNG; see its `--help`).
   2. Read the PNG and `references/design-lint-rubric.md`. Apply the rubric's two tests
      (role: structure vs content · dominance: warm anchor) and ONLY its four flags.
   3. Return the rubric's JSON verdict verbatim (`pass`/`flag` + flags array). Nothing else.

   **Hard guardrails (from the rubric — non-negotiable):** flags only, never edit or auto-fix;
   never police diagram/colour COUNTS (`colour-overload` is a loudness judgment, not a count);
   cool semantic colour on genuine structure is correct, not a flag; when in doubt, do not flag.
   A `flag` verdict goes back to the caller (Mochaccino / Marshall) to revise or escalate — it
   never blocks.
   ```
   **(c)** In the `## References` list at the bottom, add
   `- \`references/design-lint-rubric.md\` — the four-flag post-render lint rubric (operational extract of dark-factory docs/david-design-patterns.md)`.
   **Expect:** `grep -c "lint-render" $PL/appydave/skills/shelly/SKILL.md` → ≥2 (command heading
   + nothing else needed); YAML frontmatter still parses (description block intact, file still
   starts `---` / `name: shelly`).
   **Failure signal:** frontmatter broken (description quoting mangled) or the section landed
   inside the Shape Catalog table.
   **Counter-move:** `git -C $PL checkout -- appydave/skills/shelly/SKILL.md` and redo the edit
   surgically. Second failure → **Abort A3** with the diff.

4. **Do:** Edit `$PL/appydave/skills/mochaccino/SKILL.md`: inside the `## Review Command`
   section (after the line "`review` is lightweight, always optional, never a gate. Mochaccino
   offers it — the user decides."), insert one short paragraph:
   ```markdown
   **Automated sibling — Shelly's `lint-render`.** After Mocha renders, Mochaccino MAY hand the
   rendered page's screenshot to Shelly's `lint-render` for the machine pre-check (four reliable
   flags, flags-only, never a gate, never auto-fix — see Shelly's SKILL.md). Human `review`
   stays the taste channel; `lint-render` only catches brand-cold output before David sees it.
   ```
   Touch nothing else in the file.
   **Expect:** `grep -c "lint-render" $PL/appydave/skills/mochaccino/SKILL.md` → 2 (bold lead +
   body mention); `git -C $PL diff --stat` shows exactly 2 skill files + (later) plugin.json.
   **Failure signal:** diff shows hunks outside the Review Command section.
   **Counter-move:** checkout and redo. Second failure → **Abort A3**.

5. **Do:** Demote dark-factory's copy to staging remnant. **(a)** Replace the entire content of
   `$DF/tools/design-lint/RUBRIC.md` with a pointer stub:
   ```markdown
   # Design-Lint Rubric — MOVED (wg-t7-10, 2026-07-06 fold)

   The operational rubric now lives with its owner:
   **`~/dev/ad/appydave-plugins/appydave/skills/shelly/references/design-lint-rubric.md`**
   (Shelly's `lint-render` self-review mode — decisions.md Q9).

   Source of truth for the RULES is still `docs/david-design-patterns.md` in this repo.
   The mechanical screenshotter stays here: `shoot-one.py`.
   ```
   **(b)** In `$DF/tools/design-lint/README.md`, insert directly under the H1 a status block:
   ```markdown
   > **FOLDED (2026-07-06, wg-t7-10, decisions.md Q9):** the judgment half now lives in Shelly
   > (`appydave-plugins/appydave/skills/shelly/` — `lint-render` command +
   > `references/design-lint-rubric.md`). This directory keeps only the mechanical half
   > (`shoot-one.py`) and historical `out/` verdicts. RUBRIC.md here is a pointer stub.
   ```
   Leave the rest of the README intact (it is accurate history). Do NOT touch `shoot-one.py` or
   anything under `out/`.
   **Expect:** `grep -c "MOVED" $DF/tools/design-lint/RUBRIC.md` → 1;
   `grep -c "FOLDED" $DF/tools/design-lint/README.md` → 1; `git -C $DF diff --stat` touches only
   these two files so far.
   **Failure signal:** shoot-one.py or out/ appears in the diff.
   **Counter-move:** checkout the stray file and redo.

6. **Do:** Close the placement question. `git mv` (or rename)
   `$DF/backlog/2026-06-10-design-lint-placement-question.md` →
   `$DF/backlog/2026-06-10-design-lint-placement-question.done.md`, then append at the bottom:
   a `## Resolution (2026-07-06, wg-t7-10)` section of ~5 lines — David locked the fold via the
   war-game portfolio interview (decisions.md Q9); rubric folded to Shelly `lint-render`;
   dark-factory keeps shoot-one.py + stub; batch workflow + generator seam remain unbuilt —
   followed by the census block from Move 1.
   **Expect:** old filename gone, `.done.md` present, tail of file shows Resolution + census block.
   **Failure signal:** both filenames exist (copy instead of move).
   **Counter-move:** delete the stale original, keep `.done.md`.

7. **Do:** Commit and push BOTH repos, plugins first.
   **(a)** Plugins: bump `$PL/appydave/.claude-plugin/plugin.json` `"version"` minor (6.1.0 →
   `6.2.0`; if HEAD already moved past 6.1.0, minor-bump whatever you found in Recon 10). Stage
   exactly: `appydave/skills/shelly/SKILL.md`,
   `appydave/skills/shelly/references/design-lint-rubric.md`,
   `appydave/skills/mochaccino/SKILL.md`, `appydave/.claude-plugin/plugin.json`. Message:
   `feat(shelly): lint-render self-review mode — design-lint fold (appydave v6.2.0, wg-t7-10)`.
   **(b)** dark-factory: stage exactly `tools/design-lint/RUBRIC.md`,
   `tools/design-lint/README.md`, the backlog rename, and
   `backlog/2026-06-10-design-lint-placement-question.done.md`. Message:
   `chore(design-lint): judgment folded to Shelly; census bench/export/seam verified unlanded (wg-t7-10)`
   (adjust the "verified unlanded" phrase if Fork F2 changed a verdict).
   **Expect:** both pushes succeed; `git status --porcelain` in each repo shows none of YOUR
   files remaining.
   **Failure signal:** push rejected (remote ahead — parallel war-game tickets).
   **Counter-move:** `git pull --rebase` then push. Conflict in a file you touched → resolve
   keeping both intents; conflict in a file you did NOT touch → **Abort A4**.

## Forks

**F1 — Shelly already mentions lint at execution time.**
Trigger: Recon 3 finds `lint` hits in Shelly's SKILL.md (someone folded, or half-folded, in a race).
→ **Route A** (equivalent fold landed: a lint/self-review command exists, references a rubric
file carrying all four flag codes, and keeps flags-only/no-count guardrails): skip Moves 2–4;
still do Moves 1, 5, 6 (staging demotion + backlog close + census record — check each isn't also
already done; skip the ones that are) and commit whatever remains. Note "fold pre-existed" in
your result.
→ **Route B** (a CONFLICTING lint exists: different flag set, auto-fix language, count-policing,
or no rubric file): → **Abort A4** — never reconcile two rubrics by guess.

**F2 — a census claim is contradicted (feature actually landed).**
Trigger: any Recon 5a/5b/5c finds the feature on disk (bench code, a write-to-file export path,
or spec/exemplar wiring in the render skills).
→ **Route A** (found and plausibly working): change that line of the Move-1 block to
"LANDED — <path>, <one-line evidence>" and additionally update the ONE stale sentence in
`$DF/tools/mocha-census/README.md` that still calls it planned/open (surgical, that sentence
only; stage the README in Move 7b). Do not test-drive or extend the feature.
→ **Route B** (found half-built or broken — e.g. bench code exists but errors on import): record
"PARTIAL — <path>, <state>" in the block, touch NO census code, do not finish it (that is a
different ticket David hasn't asked for). The record is the deliverable.

## Assumptions ledger

1. **Q9 authorizes editing appydave-plugins for this fold.** dark-factory CLAUDE.md says
   "copying to plugins is a separate decision" — the Q9 interview ruling (2026-07-06) IS that
   decision, and both the design-lint README and the placement backlog item name Shelly as the
   intended home. **If false** (you find a later dated note from David reversing Q9 — e.g. a
   newer backlog item or decisions.md edit): stop before Move 2 and park to needs-decision with
   both citations.
2. **`lint-render` is an acceptable command name.** David never named the mode; the name follows
   Shelly's existing verb-noun idiom (`get-shape`, `add-component`). **If false** (David renames
   at triage): a one-file find-replace across the two SKILL.mds; note the alternative in your
   result rather than parking.
3. **`out/lint-v5/` (claimed by the design-lint README "Proven on" section) is absent locally**
   — only `out/lint/` and `out/lint-v4/` exist on this machine (verified 2026-07-06). Assume it
   lives on Roamy or was never committed; it is not load-bearing for this ticket. **If you
   notice it:** leave the README's history paragraph alone either way — do NOT chase the
   missing directory across machines.
4. **Minor version bump is the plugins convention** for a new capability (observed:
   v5.14.0 new skill, v6.0.0 restructure, v6.1.0 revert). **If false** (a VERSIONING.md or
   similar convention file contradicts): follow the repo's own convention and note it.
5. **The placement backlog item is still open at execution time.** **If false** (already
   `.done.md`): read its resolution — if it records this same fold, treat as Fork F1 Route A
   evidence; if it records a DIFFERENT resolution, park to needs-decision quoting it.

## Abort conditions

Park action for every abort: write
`engine/store/needs-decision/wg-t7-10-design-lint-shelly-fold.json` with
`{"ticket": "wg-t7-10-design-lint-shelly-fold", "question": "<the specific question>", "observed": "<command output / diff / quotes>"}`,
leave the ticket in `running/`, and stop. Never guess past an abort.

- **A1 — source artifacts missing.** `tools/design-lint/` or its RUBRIC.md (with the four flag
  codes), `docs/david-design-patterns.md`, or all of mocha-census is gone/moved. Question:
  "design-lint fold blocked — source artifact <path> missing/moved; where did it go, and does
  the fold still apply?"
- **A2 — target skill restructured.** Shelly's or Mochaccino's SKILL.md is missing, or
  Mochaccino no longer has a Review Command section to anchor Move 4. Question: "Mochaccino/
  Shelly skills restructured since 2026-07-06 — where does lint-render belong now?"
- **A3 — seam conflict.** Plugins repo dirty under shelly/ or mochaccino/, dark-factory dirty
  under the ticket's paths (Recon 6/7), or a surgical edit fails twice. Question: "who owns this
  seam right now?" with the `git status` / diff evidence.
- **A4 — conflicting prior fold or foreign rebase conflict.** Fork F1 Route B (a different lint
  rubric already in Shelly), or a push-rebase conflicts in a file this ticket never touched.
  Question: "two lint rubrics exist / foreign conflict at <path> — which is authoritative?"

## Verification

```bash
DF=/Users/davidcruwys/dev/ad/apps/dark-factory
PL=/Users/davidcruwys/dev/ad/appydave-plugins

# 1. Rubric lives with Shelly, all four flags intact, provenance header present
test -f $PL/appydave/skills/shelly/references/design-lint-rubric.md && echo rubric-ok
for f in cool-on-content missing-warm-anchor amber-orange-on-brown colour-overload; do
  grep -q "$f" $PL/appydave/skills/shelly/references/design-lint-rubric.md && echo "flag-$f ok"; done
grep -c "Folded from dark-factory" $PL/appydave/skills/shelly/references/design-lint-rubric.md  # → 1

# 2. Shelly command + triggers; Mochaccino cross-link
grep -c "### lint-render" $PL/appydave/skills/shelly/SKILL.md            # → 1
grep -c "lint this render" $PL/appydave/skills/shelly/SKILL.md           # → 1 (YAML trigger)
grep -c "lint-render" $PL/appydave/skills/mochaccino/SKILL.md            # → 2
head -1 $PL/appydave/skills/shelly/SKILL.md                              # → "---" (frontmatter intact)

# 3. Guardrails survived the fold (flags-only, no counts) — in BOTH new homes
grep -ci "no auto-fix\|never edit or auto-fix" $PL/appydave/skills/shelly/SKILL.md        # → ≥1
grep -ci "count" $PL/appydave/skills/shelly/references/design-lint-rubric.md              # → ≥3 (the never-count guardrails)

# 4. dark-factory demoted to staging remnant
grep -c "MOVED" $DF/tools/design-lint/RUBRIC.md                          # → 1 (stub)
grep -c "FOLDED" $DF/tools/design-lint/README.md                         # → 1
test -f $DF/tools/design-lint/shoot-one.py && echo shooter-stays-ok      # mechanical half untouched

# 5. Backlog closed with resolution + census record
test ! -f $DF/backlog/2026-06-10-design-lint-placement-question.md && echo old-name-gone-ok
grep -c "Census claims verified" $DF/backlog/2026-06-10-design-lint-placement-question.done.md  # → 1
grep -c "Resolution" $DF/backlog/2026-06-10-design-lint-placement-question.done.md              # → ≥1

# 6. Negative checks — what must NOT have changed
git -C $DF diff HEAD~1 --stat -- tools/design-lint/shoot-one.py tools/design-lint/out | wc -l   # → 0
git -C $DF diff HEAD~1 --stat -- tools/mocha-census | wc -l              # → 0 (unless Fork F2-A: then README only)
git -C $DF diff HEAD~1 --stat -- docs/david-design-patterns.md engine/ | wc -l                  # → 0
grep -rci "bench" $DF/tools/mocha-census/shoot.py                        # → 0 (no bench mode built)
grep -c "workflow.js" $PL/appydave/skills/shelly/SKILL.md                # → 0 (no batch workflow promised)

# 7. Committed and pushed, both repos; plugin version bumped
git -C $PL status --porcelain | wc -l                                    # → 0 (or only pre-existing non-ticket dirt from Recon 6)
git -C $PL log --oneline -1 -- appydave/skills/shelly                    # → the wg-t7-10 feat(shelly) commit
python3 -c "import json;v=json.load(open('$PL/appydave/.claude-plugin/plugin.json'))['version'];assert v>='6.2.0',v;print('version',v)"
git -C $DF status --porcelain -- tools/design-lint backlog | wc -l       # → 0
git -C $DF log --oneline -1 -- tools/design-lint                         # → the wg-t7-10 chore commit
```

## Executor notes (sonnet)

- **Scope fence.** Do NOT build census bench mode, export-to-file, the generator seam, or
  `design-lint.workflow.js` (batch fan-out) — all four are verify-and-record only here; each is
  its own future decision. Do NOT touch `shoot-one.py`, anything under `tools/design-lint/out/`,
  any mocha-census `.py`/`.sh`, the `mocha` skill, `docs/david-design-patterns.md`, or `engine/`.
  Do NOT run an actual lint (no Playwright, no vision judging) — this ticket folds capability
  docs, it does not exercise them.
- **The rabbit hole: proving the lint end-to-end.** The temptation is to render something, shoot
  it, and run a lint agent to "verify the fold works." Skip it — the rubric already has
  true/false-positive proof (`out/lint-v4/verdicts.json`), the fold is a documentation move, and
  a live lint run drags in Playwright deps and a model-judgment session this ticket doesn't
  budget. Structural greps in Verification are the acceptance bar.
- **Verbatim beats improved.** Copy the rubric byte-for-byte (Move 2). Every softening of
  "flags only / never count" is a regression toward the round-04 Goodhart mistake, even if the
  wording feels repetitive. Fidelity of the guardrails IS the deliverable.
- **Two repos, surgical diffs.** appydave-plugins is David's tracked plugin repo — stage only
  the four named files there; anything else in the diff is a defect. Prefer
  `git checkout -- <file>` and redo over hand-fixing a mangled hunk.
- **Prefer parking over guessing** on any sign of a prior/parallel fold (F1) or a dirty seam
  (A3) — Mochaccino-family skills get edited from many sessions; if you find half-landed work,
  park with evidence, don't merge by guess.
