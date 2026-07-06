# T3-01 — First ingestion: review-dimensional (Session 1: harvest + draft)

| field | value |
|---|---|
| ticket | wg-t3-01-first-ingestion-review-dimensional |
| track / size / priority | T3 Ingestion / M / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Execute the proof-of-workflow ingestion that has sat open since 2026-05-18
(`backlog/2026-05-18-first-ingestion-code-review.md`): the code-review cluster's
dimensional-specialist distillation becomes `canonical/skills/review-dimensional/` — the FIRST
artifact ever produced by the factory's original charter (canonical/ contains only INDEX.md
today; 0 of 1,100 corpus artifacts shipped in 7 weeks). This ticket is **Session 1 only**:
harvest verbatim sources into `_source/`, write a draft `provenance.json`, and draft `SKILL.md`
in David's voice, ending at `rewrite_status: "in-style"` — NEVER "ratified". Ratification is
Session 2 (war game T3-02, David's voice review + HITL). Done = the canonical folder exists
with 3 verbatim origins + companion references, a spec-valid draft provenance, an in-style
SKILL.md, an in-progress row in `canonical/INDEX.md`, a Session-2 handoff report at
`backlog/wargames/proof/T3-01/REPORT.md`, and a commit. This is a learning run — the workflow
spec itself is under test; every spec gap you hit is a finding for the report, not something
you silently work around.

## Locked context

- decisions.md Q9: name = **`review-dimensional`** (not `code-review`); **complement** David's
  existing review skills, don't replace; **`delivery-review` untouched**; **Session 1 =
  harvest+draft / Session 2 = voice-review+ratify** with an HITL pause before ratification.
- decisions.md Q2: ingestion is a full campaign — this ticket is its proof-of-workflow opener.
- Repo hard rule (CLAUDE.md): no canonical artifact without `provenance.json` + at least one
  verbatim copy in `_source/`. No exceptions.
- Repo hard rule: skills are stack-agnostic — stack-specific terminology in the canonical body
  is a defect.
- Repo hard rule: never write skill code into `~/dev/ad/appydave-plugins/` — `canonical/` is
  the staging ground.
- Governing specs (all verified present 2026-07-06): `docs/canonical-form-spec.md`,
  `docs/provenance-spec.md`, `docs/ingestion-workflow.md`, `docs/david-style-patterns.md`.

## Recon (verify before any work)

Docs lag code — trust only these checks. All paths repo-relative to
`~/dev/ad/apps/dark-factory` unless absolute.

1. `ls canonical/skills/review-dimensional canonical/skills/code-review 2>&1` → both "No such
   file" (at authoring, `canonical/` holds only INDEX.md). **Either exists** → Fork F1 before
   anything else. If an existing `provenance.json` there says `"rewrite_status": "ratified"` →
   Abort A2 (never touch a ratified artifact).
2. `ls research/distillations/code-review-dimensional-specialist.md` → exists (verified
   2026-07-06; winner_mechanism frontmatter = `compound-engineering:agent:ce-adversarial-reviewer`).
   **Missing** → Abort A1 (the mission's input is gone; research/ is frozen — something is wrong).
3. Origin files on disk (verified 2026-07-06, with upstream repo SHAs):
   ```bash
   ls -l /Users/davidcruwys/dev/upstream/repos/compound-engineering-plugin/plugins/compound-engineering/agents/ce-adversarial-reviewer.agent.md
   ls -l /Users/davidcruwys/dev/upstream/repos/compound-engineering-plugin/plugins/compound-engineering/skills/ce-code-review/SKILL.md
   ls -l /Users/davidcruwys/dev/upstream/repos/agent-skills/skills/code-review-and-quality/SKILL.md
   git -C /Users/davidcruwys/dev/upstream/repos/compound-engineering-plugin rev-parse --short HEAD   # 39cb9da3 at authoring
   git -C /Users/davidcruwys/dev/upstream/repos/agent-skills rev-parse --short HEAD                  # f17c6e8 at authoring
   ```
   → all three files exist (111 / 903 / 347 lines at authoring). Record the ACTUAL SHAs you
   observe — they go into `provenance.json` `source_commit`. **Any file missing** → Fork F2.
4. `ls /Users/davidcruwys/dev/upstream/repos/compound-engineering-plugin/plugins/compound-engineering/skills/ce-code-review/references/`
   → 9 companion files (bulk-preview, diff-scope, findings-schema.json, persona-catalog,
   review-output-template, subagent-template, tracker-defer, validator-template, walkthrough).
   **Missing/different count** → note the actual set; harvest whatever is there (M2).
5. Voice anchors: `head -5 ~/dev/ad/appydave-plugins/appydave/skills/review-blind-hunter/SKILL.md`
   and the same for `review-edge-case-hunter`, `review-code-quality` → all exist. **Known drift
   since the May-18 backlog item was written:** these are now thin ALIASES whose lens
   definitions are single-sourced in
   `~/dev/ad/appydave-plugins/appydave/skills/code-quality/references/lenses.md` (verified
   2026-07-06). Read lenses.md too — it is now part of the voice-anchor set. **Aliases gone or
   lenses.md missing** → David's review stack was refactored again; read whatever the
   `delivery-review`/`code-quality` skills now point at, use that as voice anchor, and record
   the drift in the report. Read-only either way.
6. Evaluation files — the May-18 backlog item names files that DO NOT exist. Verified actual
   state 2026-07-06:
   `ls research/evaluations/ | grep -iE 'code-review|adversarial|correctness'` →
   `agent-skills-osmani-agent-code-reviewer.md` and
   `agent-skills-osmani-skill-code-review-and-quality.md` exist (hyphen naming, not the
   backlog item's `__`-form); NO compound-engineering code-review evals exist (only
   ce-compound-refresh / ce-compound / ce-optimize). Use the two files that exist; record the
   backlog item's stale references as a finding.
7. `ls tools/verify-provenance.py tools/style-check.py 2>&1` → both "No such file" at
   authoring (T3-03/T3-04 build them) → validation in M7 is the manual checklist. **Either
   exists by execution time** → run it in M7 instead of (not in addition to skipping) the
   manual list; its verdict wins.
8. `grep -n 'first ingestion' canonical/INDEX.md` → the placeholder row naming the May-18
   backlog item (INDEX has 0 ratified / 0 in-progress at authoring, 44 lines). **Counts
   non-zero or rows present** → someone ingested something first; reconcile your M8 edit with
   what's there (append, never overwrite existing rows).

## Moves

### M1 — Read the research context (no writes)

- **Do:** Read, in order: (1) `backlog/2026-05-18-first-ingestion-code-review.md` — the PO
  brief; its three open questions are ALREADY ANSWERED by decisions.md Q9 (complement /
  `review-dimensional` / delivery-review untouched) — do not re-ask them. (2)
  `research/distillations/code-review-dimensional-specialist.md` in full — it names the winner
  mechanism, the folded-in ideas, and a "Canonical single-axis specialist structure" template
  that seeds your SKILL.md body. (3) The two evaluation files from Recon 6. (4)
  `docs/canonical-form-spec.md` + `docs/provenance-spec.md` + `docs/ingestion-workflow.md` +
  `docs/david-style-patterns.md`. (5) Skim `research/insights.md` for code-review craft bits.
- **Expect:** you can state, without re-reading: the winner mechanism
  (ce-adversarial-reviewer), the two mandatory folds (depth calibration Quick/Standard/Deep
  from ce-code-review; the 4-question pre-report gate from code-review-and-quality), and the
  two heuristics from David's own skills (blind-hunter's "<3 findings → re-examine";
  edge-case-hunter's validate-completeness pass).
- **Failure signal:** the distillation contradicts the backlog item on what to produce (e.g.
  names a different winner).
- **Counter-move:** the distillation is the later, more considered artifact — follow it, and
  record the contradiction in the report. If the contradiction is about the TARGET itself
  (not mechanism details) → Abort A3.

### M2 — Create the canonical folder and harvest verbatim

- **Do:**
  ```bash
  cd ~/dev/ad/apps/dark-factory
  mkdir -p canonical/skills/review-dimensional/_source
  SRC_CE=/Users/davidcruwys/dev/upstream/repos/compound-engineering-plugin/plugins/compound-engineering
  SRC_AS=/Users/davidcruwys/dev/upstream/repos/agent-skills
  cp "$SRC_CE/agents/ce-adversarial-reviewer.agent.md"      canonical/skills/review-dimensional/_source/compound-engineering--ce-adversarial-reviewer.agent.md
  cp "$SRC_CE/skills/ce-code-review/SKILL.md"               canonical/skills/review-dimensional/_source/compound-engineering--ce-code-review.md
  cp -R "$SRC_CE/skills/ce-code-review/references"          canonical/skills/review-dimensional/_source/compound-engineering--ce-code-review--references
  cp "$SRC_AS/skills/code-review-and-quality/SKILL.md"      canonical/skills/review-dimensional/_source/agent-skills-osmani--code-review-and-quality.md
  ```
  Verbatim means verbatim: no edits, no whitespace normalization, no link rewriting. Do NOT
  create `references/` or `scripts/` dirs in the canonical folder unless M5 actually needs
  them (empty dirs are noise). Do NOT copy David's review-* skills into `_source/` — they are
  voice anchors, recorded in provenance only (May-18 brief, still binding).
- **Expect:** byte-identical copies:
  ```bash
  diff "$SRC_CE/agents/ce-adversarial-reviewer.agent.md" canonical/skills/review-dimensional/_source/compound-engineering--ce-adversarial-reviewer.agent.md && echo IDENTICAL-1
  diff "$SRC_CE/skills/ce-code-review/SKILL.md" canonical/skills/review-dimensional/_source/compound-engineering--ce-code-review.md && echo IDENTICAL-2
  diff -r "$SRC_CE/skills/ce-code-review/references" canonical/skills/review-dimensional/_source/compound-engineering--ce-code-review--references && echo IDENTICAL-3
  diff "$SRC_AS/skills/code-review-and-quality/SKILL.md" canonical/skills/review-dimensional/_source/agent-skills-osmani--code-review-and-quality.md && echo IDENTICAL-4
  ```
- **Failure signal:** any diff non-empty, or a cp failed because a source path is gone.
- **Counter-move:** re-copy with `cp` (never an editor). Source path gone between Recon 3 and
  now → Fork F2.

### M3 — Write provenance.json (draft)

- **Do:** Write `canonical/skills/review-dimensional/provenance.json` per
  `docs/provenance-spec.md`. Pin these values (authoring-time decisions, do not re-derive):
  - `canonical_id`: `"dark-factory:skill:review-dimensional"` · `canonical_type`: `"skill"` ·
    `canonical_name`: `"review-dimensional"` · `version`: 1 · `rewrite_status`: `"draft"` ·
    `rewrite_author`: `"Claude (under direction)"` · `rewrite_date`: today ISO ·
    `version_history`: [].
  - `origins[]` — exactly 3 entries. `source_repo` values are `"compound-engineering"` (×2)
    and `"agent-skills-osmani"` — these match `research/recon/<repo>.md` filenames as the
    spec's field-rule table requires. (The spec's own EXAMPLE uses
    `"compound-engineering-plugin"`, contradicting its field rule; the field rule wins —
    record this spec bug in the report.) Each origin: the absolute `source_path` from Recon 3,
    `source_commit` = the SHA you recorded, `harvested_at` = today, `verbatim_copy` = the
    `_source/` relative path from M2, and `kept[]` (min 1) / `modified[]` / `set_aside[]`
    seeded from the distillation's Provenance table (rows: ce-adversarial-reviewer,
    ce-code-review depth calibration, code-review-and-quality 4-question gate + anti-
    rationalization). For the ce-code-review origin, note the references/ subfolder in a
    `verbatim_copy_companions` extension field or in `kept[]` prose — either is fine, just be
    findable.
  - `voice_anchors[]` — extension field, sanctioned by the May-18 brief: the three alias
    skills' absolute paths PLUS
    `~/dev/ad/appydave-plugins/appydave/skills/code-quality/references/lenses.md` (the
    post-refactor single source — Recon 5).
  - `research_sources`: distillation = the Recon 2 path; evaluations = the two REAL filenames
    from Recon 6; `cluster_distill_index`: `"research/distillations/INDEX.md#code-review-cluster"`.
- **Expect:** `python3 -m json.tool canonical/skills/review-dimensional/provenance.json >/dev/null && echo VALID` → VALID; every `verbatim_copy` path resolves relative to the artifact folder; no `kept[]` empty.
- **Failure signal:** parse error, or a verbatim_copy path that doesn't exist on disk.
- **Counter-move:** fix and re-validate. If you can't make an origin's `kept[]` non-empty
  honestly, drop that origin per the spec's rule 8 and note why in the report — but the
  winner (ce-adversarial-reviewer) must survive; if you'd have to drop IT → Abort A3.

### M4 — Absorb the voice anchors (no writes)

- **Do:** Read the three alias SKILL.md files, `lenses.md` (Recon 5), and
  `docs/david-style-patterns.md` §"Voice — the rules in 8 lines" + Template A. Note
  concretely: description shape (quoted trigger phrases, "Part of delivery-review orchestrator
  (XX dimension)" tail), numbered standalone-run steps, `DVR-XX-NNN` finding IDs, verdict line
  (FAIL any critical · CONDITIONAL any high · PASS else), HALT-if-scope-empty rule.
- **Expect:** you can name the 3+ concrete voice features you will reproduce in M5.
- **Failure signal:** the anchors have drifted so far from david-style-patterns.md that the
  doc's templates and the live skills disagree (partially true already — the aliases are
  terser than Template A).
- **Counter-move:** live skills win over the seed doc for VOICE; the doc wins for the required
  SECTION SET (purpose / behavior / output / anti-patterns). Record the divergence in the
  report — david-style-patterns.md says to expand it from real evidence, and T3-02 does that.

### M5 — Draft SKILL.md

- **Do:** Write `canonical/skills/review-dimensional/SKILL.md`:
  - **Frontmatter** (all 4 fields per canonical-form-spec):
    `name: review-dimensional`; `description:` trigger-only, ≤2 sentences, ≥3 quoted trigger
    phrases (e.g. 'dimensional review', 'single-axis review', 'add a review dimension', 'build
    a new reviewer', 'depth-calibrated review') — mimic the review-blind-hunter description
    rhythm; `argument-hint:` for the scope argument (e.g. `[diff | pr-url | file-list]`) or
    the literal comment `# N/A` noted in the body if you conclude it takes none;
    `allowed-tools:` copy from the winner's `tools:` line (`Read, Grep, Glob, Bash`) but DROP
    `Write` — reviewers never write (David's Template-B anti-pattern) — and record the drop in
    `modified[]`.
  - **Body** — seed from the distillation's "Canonical single-axis specialist structure",
    rendered in David's voice per M4: one-line purpose; axis-territory + explicit "what you
    don't flag" non-overlap section; depth calibration (Quick <50 changed lines / Standard
    50–199 / Deep 200+ or risk signals); execution steps including edge-case-hunter's
    validate-completeness pass; the 4-question pre-report gate (cite line, name failure, read
    context, defend severity); anchored confidence rubric (100/75/50/suppress-at-≤25);
    blind-hunter's "<3 findings on a non-trivial diff → re-examine"; normalized findings with
    dimension-coded IDs; verdict line; HALT-if-scope-empty; anti-patterns section (≥2 bullets,
    include lane-drift into sibling dimensions and writing files).
  - **Constraints:** stack-agnostic (no language/framework/package-manager names in the body);
    ≤400 lines (target well under — the aliases are ~20 lines; this canonical is the FULL
    pattern so 100–250 lines is the sane band); no workflow summary in the description; do not
    name `delivery-review`'s internals as dependencies beyond a "composable into any fan-out
    orchestrator" line (complement, don't couple).
- **Expect:** file exists; `wc -l` ≤ 400; frontmatter greps in Verification all pass.
- **Failure signal:** body needs >400 lines to carry the pattern.
- **Counter-move:** move overflow (e.g. the full technique taxonomy examples) to
  `canonical/skills/review-dimensional/references/<topic>.md` per canonical-form-spec — that
  is the ONLY reason to create the references/ dir. If still over, you are transcribing the
  903-line origin instead of distilling — cut to the mechanism, re-read M4's terseness notes.

### M6 — Refine provenance to in-style

- **Do:** Re-open `provenance.json`; update each origin's `modified[]` (what you ACTUALLY
  changed: voice, dropped Write, description → trigger-only, stack-agnostic rewrites…) and
  `set_aside[]` (what you deliberately did not carry: e.g. ce-code-review's 15–20-reviewer
  fan-out machinery, autofix/headless modes, persona catalog breadth; osmani's multi-model
  pass); refine `kept[]` to match the shipped body. Set `rewrite_status`: `"in-style"`.
- **Expect:** JSON still valid; `grep '"rewrite_status"' …/provenance.json` → `"in-style"`.
- **Failure signal:** kept/modified/set_aside no longer reflect the real SKILL.md (drift
  between M5 edits and M3 seed).
- **Counter-move:** re-derive the three arrays from a fresh read of your own SKILL.md — the
  audit-the-rewrite promise is the point of the whole repo; don't ship a stale ledger.

### M7 — Validate (manual checklist, or the validator if it now exists)

- **Do:** Per Recon 7: if `tools/verify-provenance.py` / `tools/style-check.py` exist, run
  them and obey. Otherwise run the manual gate from `docs/ingestion-workflow.md` step 8 as
  executable checks:
  ```bash
  cd ~/dev/ad/apps/dark-factory/canonical/skills/review-dimensional
  python3 -m json.tool provenance.json >/dev/null && echo CK1-json
  python3 - <<'EOF'
  import json,os
  p=json.load(open('provenance.json'))
  for o in p['origins']:
      assert os.path.exists(o['verbatim_copy']), o['verbatim_copy']
      assert o['kept'], 'empty kept'
  print('CK2-origins')
  EOF
  head -8 SKILL.md | grep -c 'name:\|description:\|argument-hint:\|allowed-tools:'   # → 4 (CK3)
  wc -l < SKILL.md    # ≤ 400 (CK4)
  grep -icE 'npm|yarn|pip |pytest|typescript|javascript|python3?|rails|ruby|react|eslint|prettier' SKILL.md   # → 0 body hits (CK5; allow hits only inside frontmatter/allowed-tools if any, and justify each)
  ls _source/ | wc -l   # → 4 entries: 3 files + 1 references dir (CK6, no orphans)
  ```
  Also eyeball: description is trigger-only (would an LLM know WHEN to fire but not HOW it
  works? good); body has purpose/behavior-equivalent/output/anti-patterns sections.
- **Expect:** every check passes.
- **Failure signal:** any check fails.
- **Counter-move:** fix and re-run — drafts iterate freely (assessment-mode only protects
  RATIFIED artifacts). A check you cannot satisfy without violating a spec (specs conflict) →
  record both readings, satisfy the stricter one, flag in the report; if neither reading is
  satisfiable → Abort A3.

### M8 — Register in-progress, update the backlog item, write the Session-2 handoff

- **Do:**
  1. `canonical/INDEX.md`: add a row to the Skills table —
     `| review-dimensional | Single-axis specialist reviewer pattern — depth-calibrated, gated, composable | 3 | in-style | <today> |`
     — replacing the "(none yet…)" placeholder row, and set the Count section to
     `ratified: 0 / in progress: 1 / upstream origins ingested: 3`. (Ingestion-workflow step
     10 registers at ratify; INDEX's own status vocabulary explicitly supports draft/in-style
     rows, so an in-progress row is truthful. T3-02 flips it to ratified.)
  2. Append a `## Status` section to `backlog/2026-05-18-first-ingestion-code-review.md`:
     Session 1 complete via wg-t3-01, artifact at `canonical/skills/review-dimensional/`,
     status in-style, Session 2 (voice-review + ratify) = wg-t3-02, plus the answered-by-Q9
     note for its three open questions. Do NOT move the backlog item to done/ — it closes at
     ratification.
  3. `mkdir -p backlog/wargames/proof/T3-01` and write `backlog/wargames/proof/T3-01/REPORT.md`:
     what was harvested (paths + SHAs), the draft's shape, every finding (mandatory minimum:
     (a) the May-18 backlog item's eval-file references are stale — real filenames differ, CE
     evals absent; (b) David's review-* skills are now aliases over lenses.md — the voice-anchor
     landscape shifted after the brief was written; (c) the provenance-spec example vs
     field-rule `source_repo` contradiction; (d) any david-style-patterns.md divergence from
     the live skills (M4); (e) anything else the run surfaced), and a **Session 2 checklist**
     for David: voice review of SKILL.md, ratify decision, allowed-tools call (Write dropped —
     confirm), INDEX flip, backlog-item close, david-style-patterns.md corrections.
- **Expect:** all three files changed/created; INDEX still renders as a coherent table
  (`grep -c '|' canonical/INDEX.md` grows by ~1 row).
- **Failure signal:** INDEX placeholder structure differs from expectation (Recon 8 warned).
- **Counter-move:** append rather than restructure; keep existing rows byte-identical; if the
  INDEX has been reshaped beyond recognition, add your row in the same shape the current file
  uses and note it.

### M9 — Commit

- **Do:**
  ```bash
  cd ~/dev/ad/apps/dark-factory
  git add canonical/ backlog/2026-05-18-first-ingestion-code-review.md backlog/wargames/proof/T3-01/
  git commit -m "feat(canonical): first ingestion — review-dimensional harvested + drafted in-style (wg-t3-01, Session 1 of 2)"
  ```
- **Expect:** `git log --oneline -1` shows the commit; `git status --short` shows nothing
  left under `canonical/` or the two backlog paths.
- **Failure signal:** unexpected staged files (you touched something outside the fence) or
  dirty leftovers.
- **Counter-move:** `git restore --staged` anything outside the three path groups above,
  inspect why it changed, revert it (`git checkout -- <path>`) if it was accidental, note in
  the report if it wasn't, then re-commit. Push only if the branch is main and clean —
  standing preference is commit+push finished work; a failed push (offline/diverged) is a
  report note, not a blocker.

## Forks

**F1 — A prior ingestion attempt exists at the target.**
Trigger: Recon 1 finds `canonical/skills/review-dimensional/` (or the pre-rename
`canonical/skills/code-review/`).
→ **Route A** (`rewrite_status` is `draft` or `in-style`, or provenance.json absent/partial):
salvage — keep any byte-identical `_source/` files (verify with the M2 diffs), redo
provenance/SKILL.md per this war game, and note the salvage in the report. If the old attempt
sits at the `code-review` name, `git mv` the folder to `review-dimensional` (locked name)
before proceeding.
→ **Route B** (`rewrite_status` is `ratified`): → Abort A2. Never edit or version-bump a
ratified artifact from inside this ticket.

**F2 — An origin file has moved or vanished upstream.**
Trigger: Recon 3 or M2 can't find one of the three source paths.
→ **Route A** (relocatable): `find <repo-root> -name '<filename>'`, or check `git -C <repo>
log --diff-filter=R --name-status -- '<old-path>'` for a rename. Found → use the new path,
record old + new in provenance (`source_path` = new, note the move in the report), continue.
→ **Route B** (gone from the repo): if it's a FOLD source (ce-code-review or
code-review-and-quality) → apply ingestion-workflow's edge case: keep the origin entry,
`verbatim_copy: "[origin removed before harvest]"`, mine the fold's content from the
distillation + evaluation record instead, flag prominently in the report. If it's the WINNER
(ce-adversarial-reviewer.agent.md) → Abort A1 — the mission's central mechanism has no
verbatim source, and the no-verbatim-no-canonical hard rule can't be met.

## Assumptions ledger

1. **`source_repo` naming follows the field rule (recon filenames), not the spec's example.**
   Plausible: the rule table is normative ("matches a repo in `research/recon/<repo>.md`");
   the example predates it. If false (a validator lands by execution time and enforces the
   example's naming) → obey the validator, note the flip in the report.
2. **Dropping `Write` from allowed-tools is the right call.** Invented here from David's
   "reviewers never write" anti-pattern; the winner agent ships `Write` in its tools line. If
   David disagrees at Session-2 review it's a one-line frontmatter change — flagged explicitly
   in the REPORT.md Session-2 checklist.
3. **An in-style INDEX row in Session 1 is acceptable** despite step 10 registering at ratify
   — INDEX's status vocabulary supports it and the truthful in-progress count beats an
   invisible draft. If David objects, it's a one-row revert; flagged in the handoff.
4. **The lens refactor doesn't collapse the mission's value.** If lenses.md turns out to
   already contain depth calibration + an anchored confidence rubric (the two "gaps" this
   canonical adds), the canonical is partially redundant as CARGO — but the ticket's primary
   value is proving the ingestion WORKFLOW, so proceed and record the overlap as a major
   report finding for David's Session-2 read.
5. **T3-02 exists as the Session-2 vehicle** (in `plans/wargames/candidates.js` at authoring;
   its war game may or may not be authored/promoted by execution time). If no wg-t3-02 ticket
   exists when you finish, the REPORT.md Session-2 checklist is still the handoff — say so in
   the backlog item's Status section so a human can run Session 2 manually.

## Abort conditions

Park action for ALL aborts: write
`engine/store/needs-decision/wg-t3-01-first-ingestion-review-dimensional.json` containing
`{"ticket":"wg-t3-01-first-ingestion-review-dimensional","question":"<one-line question>","note":"<what was observed, with paths>"}`,
leave this ticket in `running/`, stop. Never guess past an abort.

- **A1 — Mission input unrecoverable.** The distillation file is missing (Recon 2), or the
  winner-mechanism origin is gone with no relocation (F2 Route B, winner case). Question:
  "T3-01's winner source (ce-adversarial-reviewer) / distillation is gone — re-run recon on
  compound-engineering, or re-scope the first ingestion?"
- **A2 — Target already ratified.** A ratified `review-dimensional` (or `code-review`)
  canonical exists (Recon 1 / F1 Route B). In-place edits to ratified artifacts are forbidden;
  version-bumping is a PO call, not this ticket's. Question: "review-dimensional already
  ratified at <path> — is T3-01 obsolete, or do you want a v2 ticket?"
- **A3 — Spec/target contradiction with no conservative resolution.** The distillation and the
  locked decisions disagree on WHAT to produce (M1), the winner origin can't honestly appear
  in `origins[]` (M3), or two specs give unsatisfiable conflicting requirements (M7).
  Question: "T3-01 hit a spec contradiction: <the two readings>. Which wins?"

## Verification

All from `~/dev/ad/apps/dark-factory`. Positive:

```bash
test -f canonical/skills/review-dimensional/SKILL.md          && echo PASS-1
test -f canonical/skills/review-dimensional/provenance.json   && echo PASS-2
test -f canonical/skills/review-dimensional/_source/compound-engineering--ce-adversarial-reviewer.agent.md && echo PASS-3
test -f canonical/skills/review-dimensional/_source/compound-engineering--ce-code-review.md                && echo PASS-4
test -d canonical/skills/review-dimensional/_source/compound-engineering--ce-code-review--references      && echo PASS-5
test -f canonical/skills/review-dimensional/_source/agent-skills-osmani--code-review-and-quality.md       && echo PASS-6
python3 -m json.tool canonical/skills/review-dimensional/provenance.json >/dev/null && echo PASS-7
grep -q '"rewrite_status": *"in-style"' canonical/skills/review-dimensional/provenance.json && echo PASS-8
grep -q '"source_commit"' canonical/skills/review-dimensional/provenance.json && echo PASS-9
head -8 canonical/skills/review-dimensional/SKILL.md | grep -q 'name: review-dimensional' && echo PASS-10
[ "$(wc -l < canonical/skills/review-dimensional/SKILL.md)" -le 400 ] && echo PASS-11
grep -q 'review-dimensional' canonical/INDEX.md && echo PASS-12
grep -q '## Status' backlog/2026-05-18-first-ingestion-code-review.md && echo PASS-13
test -f backlog/wargames/proof/T3-01/REPORT.md && echo PASS-14
git log --oneline -5 | grep -q 'review-dimensional' && echo PASS-15
diff /Users/davidcruwys/dev/upstream/repos/compound-engineering-plugin/plugins/compound-engineering/agents/ce-adversarial-reviewer.agent.md canonical/skills/review-dimensional/_source/compound-engineering--ce-adversarial-reviewer.agent.md && echo PASS-16   # verbatim really verbatim
```

Negative (must NOT be true):

```bash
grep -q '"rewrite_status": *"ratified"' canonical/skills/review-dimensional/provenance.json || echo NEG-1   # Session 1 never ratifies
git -C ~/dev/ad/appydave-plugins diff --quiet && echo NEG-2       # David's plugin repo untouched (delivery-review + review-* + lenses.md intact)
git -C ~/dev/upstream/repos/compound-engineering-plugin diff --quiet && git -C ~/dev/upstream/repos/agent-skills diff --quiet && echo NEG-3   # upstream repos untouched
git status --short research/ | grep -q . || echo NEG-4            # frozen corpus untouched
test ! -f backlog/done/2026-05-18-first-ingestion-code-review.md && echo NEG-5   # backlog item NOT closed (closes at ratification, T3-02)
```

## Executor notes (sonnet)

- **Scope fence:** write ONLY under `canonical/skills/review-dimensional/`,
  `backlog/wargames/proof/T3-01/`, the one `## Status` append to
  `backlog/2026-05-18-first-ingestion-code-review.md`, and the one row+counts edit to
  `canonical/INDEX.md`. NEVER write to `~/dev/ad/appydave-plugins/` (hard rule),
  `~/dev/upstream/` (evidence), `research/` (frozen corpus), or `docs/` (spec amendments are
  report findings / follow-up backlog notes, not edits).
- Session 1 stops at `in-style`. Setting `ratified` — even if every checklist passes — is a
  defect: ratification is David's HITL call in T3-02.
- Verbatim copies via `cp` only. If you catch yourself "tidying" a `_source/` file, stop and
  re-copy.
- Spec gaps are findings, not blockers: this run's second deliverable is telling David where
  ingestion-workflow.md was wrong or silent. Log every one in REPORT.md.
- Prefer HITL over guessing: any ambiguity about whether something belongs in the canonical
  body vs set_aside is a judgment you CAN make (that's the drafting job); ambiguity about the
  TARGET, ratification, or touching David's live skills is not → park per the abort convention.
- **The rabbit hole:** the distillation's frontmatter lists 24 source_artifacts and the
  ce-code-review origin is 903 lines with 9 reference files of orchestrator machinery. You
  harvest THREE origins and distill ONE pattern. Do not chase the other 21 artifacts, do not
  transcribe the fan-out orchestrator, do not build the 7th-dimension reliability reviewer the
  distillation muses about (that's a Session-2/PO question). Small, in-style, handed off.
