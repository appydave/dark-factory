# T3-08 — Spec-writing cluster (157): L2a validation + distillation refresh

| field | value |
|---|---|
| ticket | wg-t3-08-distill-spec-writing |
| track / size / priority | T3 Ingestion / M / normal |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

The candidate title ("Distill: spec-writing") is stale — authoring recon found the distillation
ALREADY EXISTS: 6 draft files (`research/distillations/spec-writing-*.md`, created 2026-05-17)
plus a full "## Spec-Writing Cluster" section in `research/distillations/INDEX.md`. What makes
them unusable is the living-system spec's caveat: all 76 existing distillations are
**provisional — written with incomplete Level-2 coverage; do not ingest from them until the
cluster's Level 2 is complete**. For spec-writing, only 3 of the ~39 source artifacts named by
the 6 distillations have L2a triage evals today. This ticket closes the L2a gap for the
cluster's load-bearing set: write triage evals for the 5 unevaled sub-cluster winners plus the
mandatory folds (cap 18 new evals), re-validate each of the 6 distillation files against that
evidence AND against David's CURRENT stack (two drifts pre-verified: `spec-writer` — the
requirements-capture winner — is now ARCHIVED; the osmani `agent-skills` plugin — including
`interview-me` and `spec-driven-development` — is now INSTALLED, invalidating "entirely absent
from David's stack" gap claims), upgrade each file's frontmatter from `status: draft` to an
L2a verdict, and emit an ingestion shortlist + T2/BA-agent handoff report. Done = new evals on
disk in `research/evaluations/`, all 6 distillations carry an `## L2a validation` section and a
non-draft status, the INDEX section is corrected, `backlog/wargames/proof/T3-08/REPORT.md`
exists with the T2 handoff, and a commit. **No canonical/ writes** — ingestion of the validated
winners is a follow-on wave (T3-19-pattern), not this ticket.

## Locked context

- decisions.md Q2: ingestion is a **full campaign** — proof + validators + **cluster
  distillation** + rollout harness + judge calibration. This ticket is the spec-writing
  cluster's distillation-validation leg.
- decisions.md Q4: everything through the engine — this runs as a sonnet-Swagger ticket.
- Living-system spec (`docs/dark-factory-living-system-spec.md`, Level-3 caveat ~line 132):
  provisional distillations must not feed ingestion until the cluster's Level 2 is complete.
  L2b (rollout) has NO harness yet (T3-15/T3-16 build it) — so this ticket can claim
  **L2a-validated only**, never "validated" or "ratified". Use exactly the status vocabulary
  in M4.
- Repo rule reconciliation: dark-factory CLAUDE.md calls `research/` read-only BUT explicitly
  scopes the prohibition to "data that wasn't sourced from a recon/discover/distill/eval
  phase". This ticket's writes ARE eval-phase and distill-phase outputs (and candidate T3-06's
  brief confirms the campaign routes distill output to `research/distillations/`). Sanctioned
  writes: `research/evaluations/*.md` (append new files only) and the 6
  `research/distillations/spec-writing-*.md` files + the Spec-Writing section of
  `research/distillations/INDEX.md`. **Frozen forever:** `research/artifacts/` (every jsonl),
  `research/census.jsonl`, `research/recon/`, everything else under `research/`.
- Assessment-mode rule: the 6 distillations are `status: draft` → drafts may iterate. But
  iterate append-first: add sections and update frontmatter; never silently rewrite a
  conclusion — a changed conclusion (e.g. a dethroned winner) is RECORDED with the old and new
  positions side by side.
- Hard rule inherited from the portfolio: no writes to `~/dev/ad/appydave-plugins/` (including
  `_archived/` — read it, never touch it), no writes to `~/dev/upstream/` (evidence).

## Recon (verify before any work)

All paths repo-relative to `~/dev/ad/apps/dark-factory` unless absolute. Docs lag code — trust
only these checks.

1. `ls research/distillations/spec-writing-*.md | wc -l` → **6** (clarification-loop,
   constitution-style, document-review, prd-lifecycle, product-strategy, requirements-capture;
   all verified 2026-07-06, all `status: draft`, created 2026-05-17). Count ≠ 6 or files gone →
   Abort A1. Any already NOT `status: draft` → Fork F3 before anything else.
2. `grep -n '## Spec-Writing Cluster' research/distillations/INDEX.md` → one hit (~line 775 at
   authoring). Known authoring-time finding: the section header says "Sub-cluster count: 5" and
   "Distillation files: 5" but its own table has **6** rows — record as a report finding and fix
   in M5. Section missing → Abort A1.
3. `wc -l < research/artifacts/_slice_spec_writing.jsonl` → **157**; records carry a
   `file_path` field (verified). Missing/short → Abort A1.
4. Eval store reality: `ls research/evaluations/*.md | wc -l` → **88 at authoring**;
   `ls research/evals.jsonl` → does NOT exist (the living-system spec's "stored in
   research/evals.jsonl" is aspirational — markdown files are the real store; report finding).
   If `evals.jsonl` EXISTS at execution time → someone built the machine-readable store since;
   append a record there for every eval you write in M3, matching whatever line schema its
   existing records use.
5. Existing coverage of this cluster's source artifacts (verified 2026-07-06 — exactly three):
   `research/evaluations/agent-skills-osmani__skill__interview-me.md`,
   `research/evaluations/agent-skills-osmani__skill__spec-driven-development.md`,
   `research/evaluations/appydave-plugins-skill-doc-review.md`. Also note the filename
   convention split: 72 hyphen-form vs 16 `__`-form files — new evals use the majority
   **hyphen form** `<repo>-<artifact_type>-<name>.md` (report finding, don't "fix" old names).
6. Upstream repos + SHAs (all verified present 2026-07-06 — record the ACTUAL SHAs you observe;
   they go in each eval's `source_version`):
   ```bash
   for r in agent-skills BMAD-METHOD spec-kit GSD compound-engineering-plugin everything-claude-code; do
     echo -n "$r "; git -C /Users/davidcruwys/dev/upstream/repos/$r rev-parse --short HEAD; done
   # authoring values: f17c6e8 / 5090cfb0 / 81e9ecd / 7f5ae23 / 39cb9da3 / 4423f10c
   ```
   Any repo missing → Fork F2 for its artifacts.
7. The five unevaled winners' source paths (from the slice, verified 2026-07-06):
   - `spec-kit:command:constitution` → `/Users/davidcruwys/dev/upstream/repos/spec-kit/templates/commands/constitution.md` ✓
   - `compound-engineering:skill:ce-doc-review` → `/Users/davidcruwys/dev/upstream/repos/compound-engineering-plugin/plugins/compound-engineering/skills/ce-doc-review/SKILL.md` ✓
   - `compound-engineering:skill:ce-strategy` → `/Users/davidcruwys/dev/upstream/repos/compound-engineering-plugin/plugins/compound-engineering/skills/ce-strategy/SKILL.md` ✓
   - `bmad-method:skill:bmad-prd` → `/Users/davidcruwys/dev/upstream/repos/BMAD-METHOD/src/bmm-skills/2-plan-workflows/bmad-prd/SKILL.md` ✓
   - `appydave-plugins:skill:spec-writer` → slice path
     `/Users/davidcruwys/dev/ad/appydave-plugins/appydave/skills/spec-writer/SKILL.md` is
     **MISSING** — the skill was archived; live copy verified at
     `/Users/davidcruwys/dev/ad/appydave-plugins/_archived/appydave-skills/spec-writer/`
     (SKILL.md + references/). This is the pre-verified stack-drift centerpiece — see M4/F1.
   Any of the four ✓ paths gone at execution → Fork F2.
8. Stack-drift anchors (both verified 2026-07-06):
   `ls ~/dev/ad/appydave-plugins/appydave/skills/ | grep -E 'spec-writer'` → empty (archived), and
   `grep -c 'agent-skills' ~/.claude/settings.json` → ≥1 (the osmani agent-skills plugin is
   installed/wired). If spec-writer is BACK in the live skills dir → the drift reversed;
   invert the M4 finding accordingly. If agent-skills is no longer wired → the distillation's
   original "absent from stack" claims stand; adjust M4.
9. `ls engine/store/needs-decision/ >/dev/null && echo OK` → OK (park destination exists).
10. `ls backlog/wargames/proof/T3-08 2>&1` → "No such file" (fresh run). Exists → Fork F3.

## Moves

### M1 — Read the evidence base (no writes)

- **Do:** Read in full: (1) the 6 `research/distillations/spec-writing-*.md` files — note each
  file's `winner_mechanism`, its "Non-overlapping ideas folded in" bullets (each carries
  `complexity | optional | prerequisite` markers), its Provenance table, and its "Open
  questions for David"; (2) the "## Spec-Writing Cluster" section of
  `research/distillations/INDEX.md` (sub-cluster table, the "Top 3 gaps", the two
  judgment-needed items); (3) the Level-2a/2b/3 sections of
  `docs/dark-factory-living-system-spec.md` (field lists for an eval record); (4) the three
  existing evals from Recon 5 — `agent-skills-osmani__skill__interview-me.md` is the format
  anchor: frontmatter `artifact_id / repo / artifact_type / cluster_facet / phase_fit /
  evaluated_at`, then Intent, a Scores block (`quality_score`, `adoption_fit_final`,
  `inspiration_value`, `uniqueness_refined`, `composability`, `description_craft_refined`),
  Mineable phrasing, Notes; (5) `research/schema-current.md` (id format `<repo>:<type>:<name>`).
- **Expect:** you can state the 6 winners, that exactly 3 source artifacts are evaled, and the
  six score-field names, without re-reading.
- **Failure signal:** a distillation file lacks `winner_mechanism` frontmatter or the
  folded-ideas markers.
- **Counter-move:** derive the winner from the file's "Winner's Mechanism" prose section and
  treat every fold as `optional: false` (conservative); record the schema gap in the report.

### M2 — Build the capped eval worklist

- **Do:** Compute the union of `source_artifacts` across the 6 files (~39 unique ids at
  authoring, dupes like `spec-driven-development` ×3 collapse), subtract the 3 already-evaled
  ids, then order and CAP:
  1. the 5 unevaled winners (Recon 7);
  2. every fold marked `optional: false` in any of the 6 files;
  3. folds marked `optional: true`;
  4. remaining source artifacts — REAL-GAP sub-clusters first (clarification-loop,
     document-review, product-strategy), then requirements-capture, prd-lifecycle,
     constitution-style.
  **Hard cap: 18 new evals.** Full 157-coverage is T3-14's job, not yours. Resolve each id to
  its source file via the slice:
  ```bash
  cd ~/dev/ad/apps/dark-factory
  python3 - <<'EOF'
  import json
  for line in open('research/artifacts/_slice_spec_writing.jsonl'):
      d = json.loads(line)
      print(d['id'], '\t', d['file_path'])
  EOF
  ```
  Ids not in the slice (cross-cluster artifacts like `bmad-method:skill:bmad-agent-pm` may live
  in another slice) → grep `research/artifacts/artifacts.jsonl` for the id and use that
  record's `file_path`. Write the final worklist (id, file_path, priority rank) to
  `backlog/wargames/proof/T3-08/worklist.md` (create the dir).
- **Expect:** a worklist of ≤18 rows; every row has an on-disk file_path (or is flagged for F2);
  all 5 winners present in rows 1–5.
- **Failure signal:** an id resolves to no record in slice OR artifacts.jsonl.
- **Counter-move:** the distillation's Provenance table names the repo — locate the file with
  `find /Users/davidcruwys/dev/upstream/repos/<repo> -iname '*<name>*'`. Found → use it and
  record the corpus gap in the report. Not found → Fork F2.

### M3 — Write the L2a triage evals

- **Do:** For each worklist row: read the source file in full, then write
  `research/evaluations/<repo>-<artifact_type>-<name>.md` (hyphen form per Recon 5; sanitize
  any `:` in names to `-`, e.g. `gsd:discuss-phase` → `gsd-command-gsd-discuss-phase.md`).
  Match the interview-me anchor's shape exactly, plus one addition:
  - frontmatter: `artifact_id` (the corpus id), `repo`, `artifact_type`, `cluster_facet`
    (copy from the slice record), `phase_fit`, `evaluated_at` (today ISO), and
    `source_version: <repo HEAD SHA from Recon 6>` (the living-system spec's refresh-trigger
    field; for the archived spec-writer use the appydave-plugins repo SHA and note the
    archive path).
  - body: `# Eval: <name>` · **Intent** (one sentence) · **Scores** — all six fields, each
    with a one-to-three-sentence justification grounded in the source text, scored the way the
    existing 88 do (quality_score 1–5; the other five use the vocabulary you saw in the
    anchors: strong/partial/weak, high/medium/low, rare/uncommon/common, standalone/
    calls-others/called-by, trigger/workflow/vague) · **Mineable phrasing** (one real quote,
    or omit the section if nothing earns it) · **Notes** (incl. gap_analysis substance: what
    this adds that David's CURRENT stack lacks — use the Recon 8 facts, not the distillation's
    2026-05 claims).
  These are TRIAGE evals — judged by reading, not by running (running is L2b; no harness
  exists). Work through the list in priority order so a cap or time stop still leaves the
  winners covered.
- **Expect:** ≤18 new files in `research/evaluations/`; `ls research/evaluations/*.md | wc -l`
  = 88 + your count; each parses as frontmatter+body (`head -12 <file>` shows `---` fences and
  `artifact_id:`).
- **Failure signal:** a source file is unreadably huge or is a directory of many sub-files
  (e.g. BMAD workflow folders) and you're transcribing instead of triaging.
- **Counter-move:** triage from the artifact's entry file + its immediate README/frontmatter
  only; note "evaluated from entry file" in Notes. An eval is a scored read, not a summary of
  every reference file.

### M4 — Validate each distillation against the evidence (6 passes)

- **Do:** For each of the 6 `spec-writing-*.md` files, in this order — requirements-capture
  (has the archived winner), clarification-loop, document-review, product-strategy,
  prd-lifecycle, constitution-style:
  1. **Winner check:** does the winner's new (or existing) eval hold up against the evaled
     contenders in the same sub-cluster? Winner clearly beaten or its source lost → Fork F1.
  2. **Fold check:** does each `optional: false` fold survive its eval? (A fold whose source
     scored quality ≤2 gets flagged, not silently kept.)
  3. **Stack-drift check** against David's stack TODAY (Recon 8): pre-verified corrections you
     must apply — (a) requirements-capture: winner `spec-writer` is ARCHIVED, so "winner
     already in stack — PARTIAL gap" is now false; (b) clarification-loop: `interview-me` is
     now INSTALLED via the agent-skills plugin, so "pre-spec elicitation entirely absent" is
     stale — the gap is now "installed but not composed into any pipeline"; (c) check each
     remaining file's "gap closed?"/current-position claims against
     `ls ~/dev/ad/appydave-plugins/appydave/skills/` and the installed agent-skills plugin
     (`spec-driven-development` is also live) and correct likewise.
  4. **Append** (never rewrite the existing body) a section:
     ```markdown
     ## L2a validation — <today ISO> (wg-t3-08)

     - Coverage: <n> of <total source_artifacts> source artifacts now have L2a evals (was <m>).
     - Winner: CONFIRMED | CHANGED (old → new, evidence) | CONTESTED (see report).
     - Folds: <per-fold one-liners: holds / flagged (why)>.
     - Stack drift since 2026-05-17: <the corrections from step 3>.
     - Ingestion readiness: READY | READY-WITH-CAVEAT (<caveat>) | NOT-READY (<why>) — pending
       L2b policy (no rollout harness exists; see T3-15/T3-21).
     ```
  5. **Frontmatter:** change `status: draft` → `status: l2a-validated` (winner CONFIRMED or
     CHANGED-with-clear-evidence) or `status: l2a-contested` (F1 Route B); add
     `l2a_validated: <today ISO>` and `l2a_coverage: "<n>/<total>"`; add
     `winner_changed: true` + updated `winner_mechanism` only on F1 Route A.
- **Expect:** `grep -L 'status: draft' research/distillations/spec-writing-*.md` lists all 6;
  `grep -l '## L2a validation' research/distillations/spec-writing-*.md` lists all 6.
- **Failure signal:** ≥3 of 6 winners end CHANGED/CONTESTED/source-lost — the evidence is
  invalidating the distillation layer itself, not annotating it.
- **Counter-move:** → Abort A2 (that's a re-distillation job, bigger than this ticket).

### M5 — Correct the INDEX section

- **Do:** Edit ONLY inside the "## Spec-Writing Cluster" section of
  `research/distillations/INDEX.md`: fix the header counts ("Sub-cluster count: 5" → 6,
  "Distillation files: 5" → 6 — the authoring-time inconsistency from Recon 2); add one line
  under the header block: `**L2a validation**: <today ISO> (wg-t3-08) — statuses and
  per-sub-cluster readiness in each file's "L2a validation" section.`; if any winner changed
  (F1 Route A), update that row's Winner cell and note `(changed <today>, was <old>)`. Bump the
  file-top `**Last Updated**: 2026-05-17` line (~line 29 at authoring) to today. Touch nothing
  in other clusters' sections.
- **Expect:** `grep -A3 'Sub-cluster count' research/distillations/INDEX.md | grep 6` hits
  within the spec-writing block; `git diff --stat research/distillations/INDEX.md` shows one
  file, small line count.
- **Failure signal:** the diff bleeds into other clusters' sections.
- **Counter-move:** `git checkout -- research/distillations/INDEX.md` and redo with a
  narrower edit; if the file's structure has changed beyond recognition since authoring,
  append your validation line directly under the `## Spec-Writing Cluster` heading in whatever
  shape the current file uses and note it in the report.

### M6 — Write the report (ingestion shortlist + T2 handoff)

- **Do:** Write `backlog/wargames/proof/T3-08/REPORT.md` with these sections:
  1. **Coverage** — evals before (3/~39) → after (n/~39); worklist + cap decisions; anything
     skipped and why.
  2. **Per-sub-cluster verdicts** — the 6 status lines with one-line evidence each.
  3. **Findings** (mandatory minimum): (a) T3-08's candidate premise was stale — the cluster
     was already distilled 2026-05-17; the portfolio's "Distill: X" family (T3-06, T3-07,
     T3-09..12) likely shares this and should be re-scoped the same way; (b) `spec-writer`
     archived → requirements-capture winner no longer in stack (resurrect-vs-replace is a
     David call); (c) agent-skills plugin installed → the cluster's gap analysis was stale in
     the other direction too; (d) `research/evals.jsonl` from the living-system spec never
     built (or note if F-found); (e) eval filename convention split 72/16; (f) INDEX header
     counted 5 files, table had 6; (g) anything the run surfaced.
  4. **Ingestion shortlist** — ordered next-wave recommendation with target canonical names
     (e.g. clarification-loop → `canonical/skills/clarify/`), each labeled with its readiness
     verdict; explicitly "L2a-ready, pending the L2b/provisional policy (T3-15 / T3-21)".
  5. **T2 / BA-agent handoff** — the reason this cluster ranked: which validated spec-writing
     mechanisms the BA-agent pipeline (wg-t2-01) should compose — pre-spec elicitation gate
     (clarification-loop), post-spec document review gate (document-review), product-level
     STRATEGY anchor (product-strategy) — each with a pointer to its eval file and the
     one-line mechanism.
  6. **Consolidated open questions for David** — the "Open questions" from all 6 files plus
     any F1-Route-B contested calls, as a triage-board-ready list (these are notes for the
     board, NOT needs-decision parks — none of them block this ticket's completion).
- **Expect:** file exists; contains all six section headings; the shortlist names ≥1 READY or
  READY-WITH-CAVEAT sub-cluster (at authoring, clarification-loop and document-review are the
  likely leaders — both winners scored, both gaps real).
- **Failure signal:** every sub-cluster came out NOT-READY.
- **Counter-move:** that's a legitimate result, not a defect — say so plainly in the shortlist
  and make finding (a) + the NOT-READY evidence the report's headline; do not soften scores to
  manufacture readiness.

### M7 — Commit

- **Do:**
  ```bash
  cd ~/dev/ad/apps/dark-factory
  git add research/evaluations/ research/distillations/ backlog/wargames/proof/T3-08/
  git commit -m "feat(research): spec-writing cluster L2a validation — <n> evals + 6 distillations validated (wg-t3-08)"
  ```
- **Expect:** `git log --oneline -1` shows the commit; `git status --short` clean for the
  three path groups; the staged diff contains NO changes under `research/artifacts/`,
  `research/census.jsonl`, or `research/recon/`.
- **Failure signal:** frozen-corpus paths appear in the staged diff, or unexpected files
  staged.
- **Counter-move:** `git restore --staged <path>` + `git checkout -- <path>` for anything
  outside the fence, work out why it changed, note it in the report, re-commit. Push only if
  on main and the push succeeds cleanly; a failed push is a report note, not a blocker.

## Forks

**F1 — A sub-cluster winner doesn't survive validation.**
Trigger: M4 step 1 — the winner's eval scores clearly below an evaled contender's
(quality_score gap ≥2, or adoption_fit strong-vs-weak), or the winner's source is lost with no
relocation (F2 Route B on a winner).
→ **Route A** (evidence is clear and mechanical): update `winner_mechanism` in frontmatter,
add `winner_changed: true`, set `status: l2a-validated`, and document old → new with the
evidence in the L2a section. The Provenance table and folded-ideas body stay as historical
record — the L2a section is the correction layer. This is distill-phase work; you are allowed
to do it.
→ **Route B** (the call hinges on David's strategy, not evidence — the pre-verified case:
requirements-capture's winner `spec-writer` is David's own ARCHIVED skill; whether to
resurrect it via canonical ingestion or re-crown the now-installed
`agent-skills-osmani:skill:spec-driven-development` is a product call; also any case where
winner and contender score within 1 point): keep the original winner, set
`status: l2a-contested`, and put the question with both options' evidence in REPORT.md §6.
Never park for this — it is recorded and reversible and does not block the other 5 files.

**F2 — A worklist artifact's source file is missing on disk.**
Trigger: Recon 6/7 or M2/M3 — file_path doesn't resolve (and it isn't the known spec-writer
archive case, whose live path is given in Recon 7).
→ **Route A** (relocatable): `find` the repo for the filename, or
`git -C <repo> log --diff-filter=R --name-status -- '<old-path>'` for a rename; found → eval
from the new path, record old + new in the eval's Notes.
→ **Route B** (gone): write the eval from the slice record's `description_raw`/
`description_normalized` + the distillation's quotes only; set `deprecated: true` in
frontmatter with reason "[source removed upstream]"; cap the quality_score justification to
what the metadata supports. If the artifact is a sub-cluster WINNER → its M4 pass goes to F1.

**F3 — A prior or partial run already touched this cluster.**
Trigger: Recon 1 finds non-draft statuses, or Recon 10 finds `backlog/wargames/proof/T3-08/`,
or winner evals already exist beyond the three named in Recon 5.
→ **Route A** (complete: all 6 files have L2a sections + non-draft statuses + a report
exists): the ticket was executed already — verify the Verification block passes, write a
one-paragraph reconciliation note into the existing REPORT.md, commit nothing else, finish.
→ **Route B** (partial): salvage — keep existing evals (never rewrite another run's eval;
gaps only), run M4 only on still-draft files, extend rather than replace the report, and note
the salvage.

## Assumptions ledger

1. **Writing eval/distill outputs into `research/` is sanctioned.** Plausible: CLAUDE.md's
   prohibition is scoped to non-phase data; candidate T3-06's brief explicitly routes
   distill output to `research/distillations/`; decisions.md Q2 ratified the full campaign.
   If false (an execution-time guard — hook, validator, changed CLAUDE.md — rejects the
   writes) → Abort A3.
2. **Hyphen-form eval filenames are the right convention** (72/16 majority at authoring). If a
   naming decision landed meanwhile (check `engine/store/decisions/` and
   `research/schema-current.md` changelog for anything newer than 0.0.4), obey it and note the
   flip in the report.
3. **`status: l2a-validated` / `l2a-contested` is acceptable new status vocabulary.** Invented
   here because the living-system spec defines levels but no distillation status ladder. If a
   T3-05 / T3-21 decision defines different vocabulary by execution time (check
   `engine/store/decisions/` and `plans/wargames/decisions.md` for updates), use theirs —
   the append-section content is unchanged either way.
4. **L2a-only validation is worth shipping without L2b.** The rollout harness doesn't exist
   (T3-15/16); the strict living-system reading ("Level 2a AND 2b complete") would block every
   cluster for months. The shortlist is therefore labeled "pending L2b policy" and T3-21 owns
   the provisional-sweep policy. If David objects at triage, the statuses are one-line
   reverts — flagged in REPORT §6.
5. **T3-05's corpus questions A–N don't block this ticket.** They gate corpus MODELING at
   scale (.tmpl tracking, sub-artifact files), not triage evals of already-cataloged
   artifacts. If a landed T3-05 decision contradicts an eval-schema choice here, the decision
   record wins (see assumption 2's check).
6. **The other "Distill:" candidates (T3-06/07/09–12) share the stale premise.** Authoring
   recon saw distillation files on disk for knowledge-capture, system-comprehension,
   verification-validation, planning, delivery-readiness, and code-implementation too. Not
   this ticket's job to fix — it's REPORT finding (a), for David and the portfolio authors.

## Abort conditions

Park action for ALL aborts: write
`engine/store/needs-decision/wg-t3-08-distill-spec-writing.json` containing
`{"ticket":"wg-t3-08-distill-spec-writing","question":"<one-line question>","note":"<what was observed, with paths>"}`,
leave this ticket in `running/`, stop. Never guess past an abort.

- **A1 — Mission input unrecoverable.** The 6 distillation files, the INDEX section, or
  `_slice_spec_writing.jsonl` are missing/renamed (Recon 1–3) — the frozen corpus changed
  under the portfolio. Question: "T3-08's inputs moved or vanished (<what/where>) — re-recon
  the spec-writing cluster, or re-scope the ticket?"
- **A2 — The distillation layer is invalidated, not annotatable.** ≥3 of 6 winners end
  CHANGED/CONTESTED/source-lost in M4 — the 2026-05 distillation needs regeneration from the
  new evidence, which is a different (larger) ticket. Park with the per-sub-cluster evidence
  summary in the note; the evals you already wrote stay committed (commit them with a
  `wip(research): evals only` message before parking). Question: "spec-writing distillation
  failed L2a validation wholesale — regenerate the 6 files from the new evals, or annotate
  anyway?"
- **A3 — research/ writes rejected.** A guard (hook, validator, updated CLAUDE.md rule)
  blocks writing to `research/evaluations/` or `research/distillations/`. Question: "Campaign
  says eval/distill outputs go in research/, repo guard says read-only — where do L2a evals
  live now?"

## Verification

All from `~/dev/ad/apps/dark-factory`. Positive:

```bash
# the five winner evals exist (interview-me pre-existed)
test -f research/evaluations/spec-kit-command-constitution.md            && echo PASS-1
test -f research/evaluations/compound-engineering-skill-ce-doc-review.md && echo PASS-2
test -f research/evaluations/compound-engineering-skill-ce-strategy.md   && echo PASS-3
test -f research/evaluations/bmad-method-skill-bmad-prd.md               && echo PASS-4
test -f research/evaluations/appydave-plugins-skill-spec-writer.md       && echo PASS-5
# every new eval carries a pinned source_version
grep -l 'source_version' research/evaluations/spec-kit-command-constitution.md research/evaluations/bmad-method-skill-bmad-prd.md >/dev/null && echo PASS-6
# all six distillations validated: no draft left, L2a section present, coverage stamped
[ "$(grep -L 'status: draft' research/distillations/spec-writing-*.md | wc -l)" -eq 6 ] && echo PASS-7
[ "$(grep -l '## L2a validation' research/distillations/spec-writing-*.md | wc -l)" -eq 6 ] && echo PASS-8
[ "$(grep -l 'l2a_coverage' research/distillations/spec-writing-*.md | wc -l)" -eq 6 ] && echo PASS-9
# INDEX corrected + stamped
grep -q 'L2a validation' research/distillations/INDEX.md && echo PASS-10
# report with shortlist + T2 handoff
test -f backlog/wargames/proof/T3-08/REPORT.md && echo PASS-11
grep -qi 'ingestion shortlist' backlog/wargames/proof/T3-08/REPORT.md && echo PASS-12
grep -qi 'BA-agent\|T2' backlog/wargames/proof/T3-08/REPORT.md && echo PASS-13
# commit landed
git log --oneline -5 | grep -q 'wg-t3-08' && echo PASS-14
```

Negative (must NOT be true):

```bash
git status --short research/artifacts/ research/census.jsonl research/recon/ | grep -q . || echo NEG-1  # frozen corpus untouched
git diff HEAD~1 --name-only | grep -qE '^canonical/' || echo NEG-2                                       # no ingestion happened here
git -C ~/dev/ad/appydave-plugins diff --quiet && echo NEG-3                                              # David's plugins (incl. _archived) untouched
git -C ~/dev/upstream/repos/spec-kit diff --quiet && git -C ~/dev/upstream/repos/BMAD-METHOD diff --quiet && echo NEG-4  # upstream evidence untouched
[ "$(ls research/evaluations/*.md | wc -l)" -ge 93 ] && echo NEG-5                                       # evals only ever added (88 + ≥5), none deleted
grep -q 'status: ratified\|status: validated$' research/distillations/spec-writing-*.md || echo NEG-6    # never overclaim past l2a-validated
```

## Executor notes (sonnet)

- **Scope fence:** write ONLY new files under `research/evaluations/`, edits to the 6
  `research/distillations/spec-writing-*.md` files, the Spec-Writing section (+ Last-Updated
  line) of `research/distillations/INDEX.md`, and `backlog/wargames/proof/T3-08/`. NEVER
  write: anything else under `research/` (artifacts/, census.jsonl, recon/, other clusters'
  distillations), `canonical/` (no ingestion in this ticket), `docs/`,
  `~/dev/ad/appydave-plugins/` (read-only, including `_archived/`), `~/dev/upstream/`
  (evidence).
- These are L2a TRIAGE evals — scored reads. You never RUN a skill (that's L2b, no harness
  exists) and you never draft canonical SKILL.md bodies (that's the next wave's ticket).
- Append-first on the distillations: the 2026-05 body text is the historical record; your L2a
  section is the correction layer. A reader must be able to see what the 05-17 pass believed
  AND what the 07 validation found.
- Prefer HITL over guessing exactly once: the resurrect-vs-replace call on `spec-writer` (F1
  Route B) is David's — mark it contested, don't decide it. Everything else in this ticket is
  evidence work you are equipped to finish.
- **The rabbit hole:** document-review's source list names 8 individual ce-* reviewer
  sub-agents and prd-lifecycle names 7 BMAD artifacts backed by deep workflow folders. Do not
  eval every sub-agent and every BMAD workflow file — the cap (18) and the priority order
  exist precisely so the winners + mandatory folds get covered and the long tail waits for
  T3-14. Stay under the cap, ship the six validations, hand off.
