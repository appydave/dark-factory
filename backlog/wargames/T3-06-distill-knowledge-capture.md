# T3-06 — Distill: knowledge-capture — eval gap-fill + winner verification

| field | value |
|---|---|
| ticket | wg-t3-06-distill-knowledge-capture |
| track / size / priority | T3 Ingestion / M / normal |
| executor | sonnet Swagger via engine |
| depends_on | none (soft-reads T3-05 decision outputs if they exist — Recon 7) |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

The candidate brief said "largest undistilled cluster" — that premise is STALE. Authoring recon
(2026-07-06) found the knowledge-capture cluster ALREADY distilled: 7 draft distillation files
at `research/distillations/knowledge-capture-*.md` (2026-05-18, `status: draft`, indexed in
`research/distillations/INDEX.md` §Knowledge-Capture, byte-identical to the
`research/distillations-archive-2026-05-26/` snapshot). What is actually missing is the leg the
catalog procedure requires BEFORE distillation and never got: **per-artifact evaluations**. Only
~31 of the cluster's 201 slice artifacts have eval files, 92 of the 111 source artifacts the 7
distillations cite are un-evaluated, and 4 of the 7 winner-mechanism picks
(`architecture-decision-records`, `continuous-learning-v2`, `ck`, `ce-best-practices-researcher`)
were never scored. This ticket closes that gap: fan out per-artifact evaluations for the 92
missing sources, verify each distillation's winner-pick against the new evidence (append-only —
CONFIRMED or CONTESTED, David decides contested cases), update the two INDEX files, and stage
chained follow-on ingestion-ticket PROPOSALS for the gap-closing sub-clusters. Done = zero
missing evals on the worklist, 7 dated "Winner verification" appendices, both INDEXes updated,
3 proposal tickets staged under `backlog/wargames/proof/T3-06/next-tickets/`, a report, and a
commit. The distillation drafts themselves are NOT rewritten.

## Locked context

- decisions.md Q2: ingestion is a **full campaign** — cluster distillation is one of its named
  legs; this ticket brings the first big cluster to evidence-backed, review-ready state.
- decisions.md Q4: everything through the engine — follow-on work is staged as engine-idiom
  tickets (proposals here; David promotes).
- decisions.md assumptions ledger: the 14 corpus questions A–N are T3-05's decision batch, "not
  pre-answered". This ticket is NOT gated by them — the kc slice membership is already fixed and
  the primary-artifacts-only scope was locked 2026-05-16 (schema-history 0.0.3). Recon 7 checks
  whether T3-05 has since landed anything that overrides this.
- Repo rule (CLAUDE.md): research/ is read-only EXCEPT for append-only outputs of a sanctioned
  recon/discover/distill/eval phase. This ticket IS an eval-phase run (same sanction the
  05-17/05-18 passes used): NEW files in `research/evaluations/`, APPEND-only sections on the 7
  kc distillation files, dated status appends to the two INDEX files. Nothing else in research/
  may change — not `artifacts.jsonl`, not slices, not `recon/`, not existing eval files.
- Assessment-mode analogue: the drafts' frontmatter (`status: draft`, `winner_mechanism`) is
  never edited by this ticket. A contested winner is evidence in an appendix + report, not a
  frontmatter flip — that flip is David's review call.
- No `-p`/headless/SDK ever; interactive session only. In-session Task subagents ARE allowed
  (they are not headless spawns); use cheaper models for the eval batches per standing
  orchestrator/delegate authorization.

## Recon (verify before any work)

All paths repo-relative to `~/dev/ad/apps/dark-factory` unless absolute. Numbers in this war
game are authoring-time (2026-07-06) — trust your recount over them.

1. `ls research/distillations/knowledge-capture-*.md | wc -l` → **7** (adr-documentation,
   brain-curation, learning-instinct-promotion, memory-store-retrieve, multi-source-researcher,
   session-handover, wearable-ambient-ingest). Fewer/none → Abort A1. Extra files with new
   names → someone re-clustered; read them, reconcile the worklist to what exists, note in
   report.
2. Baseline integrity:
   `for f in research/distillations/knowledge-capture-*.md; do diff -q "$f" "research/distillations-archive-2026-05-26/$(basename $f)"; done`
   → all identical (verified at authoring). Diverged → the drafts were edited since 05-26:
   work from the CURRENT files, treat current as baseline, record the divergence in the report.
   Archive files missing entirely → proceed from current files, note it.
3. Corpus sanity: `wc -l research/artifacts/_slice_knowledge_capture.jsonl` → **201**;
   `python3 -c "import json;print(sum(1 for l in open('research/artifacts.jsonl') if l.strip() and 'knowledge-capture' in (json.loads(l).get('cluster_facet') or [])))"`
   → **203** (2 re-tags landed after the slice was cut; expected, not an error). Wildly
   different (±20+) → the corpus was regenerated since authoring; recompute everything from the
   current corpus and say so in the report.
4. Eval coverage: `ls research/evaluations/*.md | wc -l` → **88** at authoring; kc coverage
   ~31/201. Expected missing-eval counts per sub-cluster (from the distillations'
   `source_artifacts` lists, fuzzy-matched to eval filenames): adr-documentation 3 ·
   brain-curation 10 · learning-instinct-promotion 14 · memory-store-retrieve 28 ·
   multi-source-researcher 21 · session-handover 7 · wearable-ambient-ingest 9 = **92**.
   Coverage now complete or near-complete → Fork F1.
5. Procedure references: the dark-factory-catalog skill is **ARCHIVED** — the live path this
   repo's CLAUDE.md cites (`~/dev/ad/appydave-plugins/appydave/skills/dark-factory-catalog/`)
   does NOT exist. Verified real location:
   `ls /Users/davidcruwys/dev/ad/appydave-plugins/_archived/appydave-skills/dark-factory-catalog/references/`
   → contains `capability-evaluate.md` + `capability-distill.md` (your procedure ground truth).
   Record the dead CLAUDE.md pointer as a report finding. Archived copy also gone →
   `find ~/dev/ad/appydave-plugins -name capability-evaluate.md`; if truly unrecoverable, use
   two existing eval files (e.g. `research/evaluations/appydave-plugins__skill__knowledge-capture.md`,
   `research/evaluations/compound-knowledge-skill-kw-compound.md`) as the format anchor and note it.
6. Upstream sources on disk (the 4 un-evaluated winners; verified 2026-07-06):
   ```bash
   ls /Users/davidcruwys/dev/upstream/repos/everything-claude-code/skills/architecture-decision-records/SKILL.md
   ls /Users/davidcruwys/dev/upstream/repos/everything-claude-code/skills/continuous-learning-v2/SKILL.md
   ls /Users/davidcruwys/dev/upstream/repos/everything-claude-code/skills/ck/SKILL.md
   ls /Users/davidcruwys/dev/upstream/repos/compound-engineering-plugin/plugins/compound-engineering/agents/ce-best-practices-researcher.agent.md
   ```
   → all exist. Any missing → Fork F3 for that artifact. (Other repos in play: gbrain, ruflo,
   GSD, gstack, BMAD-METHOD — all under `/Users/davidcruwys/dev/upstream/repos/`; per-artifact
   `file_path` comes from `artifacts.jsonl`, never guessed.)
7. Standing decisions: `ls engine/store/decisions/ engine/store/needs-decision/` and
   `grep -rl "corpus question" backlog/wargames/ plans/ 2>/dev/null` → at authoring, no T3-05
   output exists (its war game may not even be authored yet). If a T3-05 decision artifact DOES
   exist by execution time, read it; obey any ruling that touches eval scope (most likely:
   Ruflo MCP-tools scope — irrelevant here, the slice holds primary artifacts only). A ruling
   that excludes or re-clusters knowledge-capture itself → Abort A2.
8. `git -C ~/dev/ad/apps/dark-factory status --short research/` → empty (no uncommitted
   research/ changes belonging to someone else). Dirty → do NOT proceed over foreign changes;
   if the dirt is under `research/evaluations/` or the kc distillations → Abort A1 (someone is
   mid-flight on the same ground); elsewhere in research/ → note and continue.

## Moves

### M1 — Read the procedure and the ground (no writes)

- **Do:** Read, in order: (1) the 7 kc distillation files in full — note each `winner_mechanism`,
  `source_artifacts` list, and gap verdict from `research/distillations/INDEX.md` §Knowledge-Capture
  (line ~929: learning-instinct-promotion YES · multi-source-researcher YES · adr-documentation
  YES · brain-curation PARTIAL · wearable-ambient-ingest PARTIAL · session-handover PATTERN ·
  memory-store-retrieve ASSESSMENT); (2) `capability-evaluate.md` + `capability-distill.md` from
  Recon 5 — the eval dimensions table, file template, batching strategy, QC rules, and the
  distill prerequisite line ("data/evaluations/ has evaluations for the artifacts being
  distilled" — the rule the 05-18 pass ran ahead of); (3) THREE existing eval files as format
  anchors: `research/evaluations/appydave-plugins__skill__knowledge-capture.md`,
  `research/evaluations/compound-knowledge-skill-kw-compound.md`, and any one
  `agent-skills-osmani__skill__*.md`; (4) `research/schema-current.md` (field names, esp.
  `file_path`, `cluster_facet`).
- **Expect:** you can state without re-reading: the 7 winners, which 4 lack evals, the eval
  dimensions you will score (quality / uniqueness / mechanism / gap_closed / effort_to_adopt /
  tested_in_production / bus_factor — the starter set, extended only if the existing kc evals
  already extended it), and the anti-pattern "don't recommend adopt/skip in evaluations —
  that's distillation's job".
- **Failure signal:** the existing eval files use a materially different schema than
  capability-evaluate.md's template (they do drift — frontmatter varies, some use prose scores).
- **Counter-move:** the EXISTING FILES win for format (they are the corpus's living convention);
  the capability doc wins for the DIMENSION SET. Record the drift in the report.

### M2 — Build the resolved worklist

- **Do:** Write a script-driven worklist to `backlog/wargames/proof/T3-06/worklist.json`
  (`mkdir -p backlog/wargames/proof/T3-06` first). For each of the 7 distillations, take its
  `source_artifacts` list and resolve every id against `research/artifacts.jsonl`. **Known id
  drift (verified at authoring), resolve by normalized name match, corpus id is canonical:**
  the distillation frontmatter says `compound-engineering:skill:ce-best-practices-researcher`
  but the corpus row is `compound-engineering:agent:ce-best-practices-researcher`; the
  frontmatter says `gsd:command:gsd:pause-work`, corpus says `gsd:command:pause-work`; ruflo
  ids can carry spaces and quotes (`ruflo:skill:"AgentDB Advanced Features"` →
  `.agents/skills/agentdb-advanced/SKILL.md`). Normalize both sides
  (lowercase, strip non-alphanumerics) to match. Each worklist entry:
  `{"subcluster": ..., "distillation_id": ..., "corpus_id": ..., "file_path": ..., "file_exists": bool, "eval_exists": bool, "eval_filename": ...}`.
  An artifact already covered by an existing eval file (either naming form, `__` or `-`) is
  `eval_exists: true` — existing evals are never redone or touched.
- **Expect:** worklist parses (`python3 -m json.tool`); totals ≈ 111 entries, ≈ 92 with
  `eval_exists: false` (Recon 4 tolerances apply); ≤ a handful of `file_exists: false` or
  unresolved ids.
- **Failure signal:** an id resolves to zero or multiple corpus rows even after normalization,
  or a resolved `file_path` doesn't exist on disk.
- **Counter-move:** unresolved id → Fork F2. Missing file → Fork F3. Neither blocks the rest
  of the worklist — mark the entry, continue.

### M3 — Fan out the evaluations (the bulk write)

- **Do:** Dispatch **7 parallel Task subagents in one message** — one per sub-cluster (cheaper
  model per standing auth; sonnet if quality wobbles). Each subagent gets, inline in its prompt:
  its sub-cluster's worklist entries needing evals (corpus_id + absolute file_path), the eval
  file template + dimension table from M1, the two format-anchor eval file paths to read first,
  and these hard rules: (a) READ the artifact's actual source file — never score from the
  distillation's summary; (b) one output file per artifact at
  `research/evaluations/<repo>__<artifact_type>__<name>.md` (double-underscore form; name =
  corpus `name` field, kebab-cased, spaces→hyphens); (c) frontmatter `artifact_id` = the CORPUS
  id verbatim, plus `repo`, `artifact_type`, `evaluated_at: <today>`, and
  `evaluated_by: wg-t3-06`; (d) every dimension gets a score AND a 1–2-sentence rationale
  specific to that artifact; (e) no adopt/skip recommendations; (f) a `## Mineable phrasing`
  quote when the source genuinely has one, omitted otherwise; (g) `.tmpl` sources (gstack) are
  evaluated as-is — the template IS the artifact (T3-05 may later refine this; note it, don't
  wait for it). Collect each subagent's summary.
- **Expect:** ≈ 92 new files under `research/evaluations/`; every worklist `eval_exists: false`
  entry (minus F2/F3 skips) now has a file;
  `git status --short research/evaluations/ | grep -cv '^??\|^A '` → 0 (additions only, zero
  modifications to pre-existing files).
- **Failure signal:** a subagent modified an existing eval file, wrote outside
  `research/evaluations/`, or returned fewer files than its batch.
- **Counter-move:** `git checkout -- <modified-existing-file>` immediately; re-run only the
  missing/damaged entries in a fresh subagent with the rules restated. A subagent that fails
  its batch twice → do that batch yourself in-session, sequentially. Still failing → Abort A3.

### M4 — Quality-control the new evals

- **Do:** Run capability-evaluate's QC as executable checks over the NEW files only:
  ```bash
  cd ~/dev/ad/apps/dark-factory
  NEW=$(git status --short research/evaluations/ | awk '{print $2}')
  for f in $NEW; do python3 -c "
  import sys,re
  t=open('$f').read()
  assert re.search(r'artifact_id:', t), 'no artifact_id: $f'
  assert re.search(r'evaluated_at:', t), 'no evaluated_at: $f'
  assert re.search(r'quality', t, re.I) and re.search(r'gap_closed|gap-closed', t, re.I), 'missing dims: $f'
  "; done && echo QC-STRUCT-PASS
  grep -hoiE 'quality[^a-z]*(strong|adequate|weak|[0-9])' $NEW | sort | uniq -c   # distribution
  ```
  Then eyeball 5 random new evals: rationales must be artifact-specific, not generic ("good
  skill, well-written" = fail).
- **Expect:** QC-STRUCT-PASS; the quality distribution discriminates (not >90% one value);
  spot-checked rationales are specific.
- **Failure signal:** structural assert fails, or the distribution is flat, or rationales are
  generic boilerplate.
- **Counter-move:** structural → fix the specific files in place (they are yours this session,
  not yet committed). Non-discriminating/generic → re-run those sub-cluster batches once with
  sharpened criteria ("dock a point and say why; similar artifacts must score similarly").
  Second QC failure → Abort A3 (don't commit junk into the research corpus).

### M5 — Winner verification appendices (append-only)

- **Do:** For each of the 7 distillations, read the evals (new + pre-existing) of its source
  artifacts and judge: does the evidence still support the frontmatter `winner_mechanism`?
  APPEND to the END of each distillation file — never edit existing content or frontmatter:
  ```markdown

  ---

  ## Winner verification (wg-t3-06, <today ISO>)

  Eval coverage at verification: <n>/<total> source artifacts evaluated (was <k> at draft time, 2026-05-18).
  **Verdict: CONFIRMED** — <1–3 sentences: why the winner survives the new evidence, naming the closest challenger and the discriminating dimension.>
  ```
  or `**Verdict: CONTESTED** — <the challenger, the evidence, and what David should compare>.
  Frontmatter winner_mechanism left unchanged; the flip (if any) is David's review call.`
  Unverifiable entries (F2/F3 skips hit the winner itself): `**Verdict: UNVERIFIABLE** — <why>`.
- **Expect:** `grep -l "Winner verification (wg-t3-06" research/distillations/knowledge-capture-*.md | wc -l` → 7;
  `grep -c "winner_mechanism" research/distillations/knowledge-capture-*.md` unchanged from M1
  (one per file, in frontmatter); every file still starts with its original frontmatter
  (`head -3` of each still shows `---` + `distillation_id:`).
- **Failure signal:** a diff against the archive baseline shows changes ABOVE your appended
  section in any file.
- **Counter-move:** `git diff research/distillations/` — restore any non-append change
  (`git checkout -- <file>`, re-append cleanly). Appending is the only write these files get.

### M6 — Update the two INDEX files (append-only)

- **Do:** (1) In `research/distillations/INDEX.md`, at the END of the Knowledge-Capture Cluster
  section (directly after its closing italics line "*Distillation pass: … Regenerate after David
  reviews…*"), append a short dated block: eval coverage before → after, the 7 verdicts
  (CONFIRMED/CONTESTED/UNVERIFIABLE per sub-cluster), pointer to
  `backlog/wargames/proof/T3-06/REPORT.md`. Do not edit the existing table or status fields.
  (2) In `research/INDEX.md` §Current status, append one dated bullet:
  `**<today>** — knowledge-capture eval gap-fill (wg-t3-06): +<n> evaluations, 7/7 winner-picks verified (<x> confirmed, <y> contested); distillation drafts unchanged, awaiting David review.`
- **Expect:** both files render coherently; `git diff` shows pure insertions (no `-` lines
  except context-free none).
- **Failure signal:** the INDEX sections have been restructured since authoring and the
  anchor text isn't found.
- **Counter-move:** append in whatever shape the current file uses (dated bullet lists are the
  house style); never restructure; note the drift in the report.

### M7 — Stage the chained follow-on ticket proposals

- **Do:** `mkdir -p backlog/wargames/proof/T3-06/next-tickets` and write THREE Family-A-shaped
  ticket JSONs — **proposals, NOT queued; do not write anything into `engine/store/queue/`** —
  one per gap-closing sub-cluster (the INDEX's YES verdicts):
  `wg-t3-06a-ingest-learning-instinct-promotion.json`,
  `wg-t3-06b-ingest-multi-source-researcher.json`,
  `wg-t3-06c-ingest-adr-documentation.json`. Each: `kind: instruction`, `executor: swagger`,
  `priority: normal`, `requested_at` = real UTC now (`date -u +%Y-%m-%dT%H:%M:%SZ`),
  `requested_by: "wg-t3-06 chained proposal — David promotes"`, `depends_on:
  ["wg-t3-02-...", "wg-t3-03-...", "wg-t3-04-..."]` (voice-ratified proof + both validators —
  copy the exact ticket names from `backlog/wargames/tickets/T3-02.json`/`T3-03.json`/
  `T3-04.json` if those files exist by execution time; if they don't, use the id stems
  `wg-t3-02`, `wg-t3-03`, `wg-t3-04` and note it), and a self-contained `prompt` following the
  T3-01 Session-1 pattern (harvest winner + mandatory `optional: false` folds into
  `canonical/skills/<name>/`, provenance + verbatim `_source/`, stop at in-style). If M5
  CONTESTED a proposal's winner, say so in the first line of its prompt and mark the ticket
  `"blocked_on": "David's winner call — see Winner verification appendix"`.
- **Expect:** 3 JSONs, each parses (`python3 -m json.tool`), each names a real distillation
  file as its source; `ls engine/store/queue/ | grep -c t3-06` → 0 (nothing self-queued).
- **Failure signal:** you can't write a self-contained prompt because the distillation's
  fold-annotations are ambiguous about what is mandatory.
- **Counter-move:** mandatory = the folded ideas annotated `optional: false`; everything else
  is set-aside-by-default with a note. If a distillation lacks the annotations entirely,
  propose winner-only harvest and flag it in the proposal + report.

### M8 — Report and commit

- **Do:** Write `backlog/wargames/proof/T3-06/REPORT.md`: (1) **premise correction** — the
  candidate said "largest undistilled cluster"; disk truth is 7 drafts since 2026-05-18 (this
  finding also applies to siblings T3-07..T3-12 — every cluster they name already has
  distillation files; David should re-scope them the same way before running them); (2) eval
  coverage before/after with per-sub-cluster numbers; (3) the 7 verdicts + evidence summaries;
  (4) standing findings: dark-factory CLAUDE.md's dead catalog-skill pointer (real home is
  `~/dev/ad/appydave-plugins/_archived/appydave-skills/dark-factory-catalog/`), the
  distillation-frontmatter↔corpus id drift, the split eval-filename convention (16 `__`-form /
  72 `-`-form at authoring; you added `__`-form), the 05-18 distill-before-eval procedure
  violation now healed; (5) what was deliberately NOT done: the ~90 slice artifacts the 05-18
  pass excluded (Ruflo domain agents, ECC stack-locked, solos) remain un-evaluated — full-slice
  coverage is a separate ticket if David wants it; (6) the 3 staged proposals + promotion
  instructions (one `cp` into the Phase-5 staging dir or `engine/store/queue/`). Then commit:
  ```bash
  cd ~/dev/ad/apps/dark-factory
  git add research/evaluations/ research/distillations/ research/INDEX.md backlog/wargames/proof/T3-06/
  git commit -m "feat(research): knowledge-capture eval gap-fill — 92 evals, 7 winner-picks verified, 3 ingestion proposals staged (wg-t3-06)"
  ```
- **Expect:** commit lands; `git status --short` clean for the five path groups; push succeeds
  (standing preference: commit+push finished work; a failed push is a report note, not a
  blocker).
- **Failure signal:** unstaged leftovers outside the fence, or staged changes you can't explain.
- **Counter-move:** `git restore --staged` anything outside the five path groups, inspect,
  revert accidents (`git checkout -- <path>`), then re-commit.

## Forks

**F1 — Eval coverage already (near-)complete at execution time.**
Trigger: Recon 4 finds the worklist's missing count is 0 or trivially small — someone ran the
fan-out since authoring.
→ **Route A** (evals exist, no `Winner verification (wg-t3-06` sections in the distillations):
skip M3, run M4 in audit mode over the existing kc evals (structural checks only, no rewrites —
they're not yours), then M5–M8 as written.
→ **Route B** (evals exist AND verification sections exist): the ticket's substance is done.
Write REPORT.md reconciling who did what (git log the files), stage nothing new, commit the
report only, and note the duplicate-scheduling in the report for David's portfolio hygiene.

**F2 — A source_artifacts id won't resolve to a corpus row.**
Trigger: M2 normalization finds zero or multiple `artifacts.jsonl` matches for a distillation id.
→ **Route A** (zero matches, but a name-substring search
`grep -i '<name-fragment>' research/artifacts.jsonl` hits exactly one row): use that row;
record the id drift in the worklist + report.
→ **Route B** (still zero, or several plausible rows): skip the artifact — mark
`"unresolved": true` in the worklist, exclude from fan-out, list in the report. Never invent a
corpus row (discovery is a different phase). If the unresolvable id is a sub-cluster's WINNER,
its M5 verdict is UNVERIFIABLE with this as the stated reason.

**F3 — A resolved file_path no longer exists on disk.**
Trigger: M2 `file_exists: false`, or a subagent reports the file gone mid-M3.
→ **Route A** (relocatable): `find <upstream-repo-root> -name '<basename>'` or
`git -C <repo> log --diff-filter=R --name-status -- '<old-path>'`. Found → eval from the new
path, record old→new in the eval's notes.
→ **Route B** (gone from the repo): skip — mark `"source_unavailable": true`, list in the
report. Upstream repos are evidence: NEVER `git pull`, checkout, or otherwise mutate them to
"recover" a file. Winner case → UNVERIFIABLE verdict, prominent report flag.

## Assumptions ledger

1. **Eval/distill appends to research/ are sanctioned.** CLAUDE.md says research/ is read-only
   "from your perspective" but also defines it as append-only output of
   recon/discover/distill/eval phases — this ticket is an eval-phase run, same sanction the
   05-17/05-18 passes used, and the candidate brief explicitly targets
   `research/distillations/`. If David objects at review → everything new is additive and
   revertable in one commit; if the executor finds an explicit newer rule forbidding ALL
   research/ writes (e.g. a README dropped into research/ saying so) → park to needs-decision
   instead of writing.
2. **`__`-form eval filenames are the right convention.** Both forms exist (16 `__` / 72 `-`,
   same 05-18 mtime); `__` is unambiguous for artifact_type boundaries. If a validator or
   written convention exists by execution time → obey it and rename nothing pre-existing.
3. **"Engine-ticket-chained" means staged proposals, not self-queuing.** The Phase-5 promotion
   script / David drains staged tickets progressively; a worker enqueueing its own follow-on
   work bypasses triage. If David actually wanted auto-queue, promotion is one `cp` per file —
   stated in the report.
4. **Worklist = the 111 distillation-cited sources, not all 203 slice members.** The 05-18 pass
   deliberately excluded ~65–90 artifacts (Ruflo domain agents, ECC stack-locked, solos — its
   own closing note). Evaluating exclusions would second-guess a decision David hasn't reviewed
   yet. If false (David wants full-slice coverage) → that's a follow-on ticket, noted in the
   report.
5. **T3-05 is not a hard dependency.** The corpus questions gate distillation-at-scale and
   Phase 4/5 SCOPE, but this cluster's slice and scope were locked 2026-05-16 and the
   distillations already exist. If T3-05 lands rulings first, Recon 7 picks them up; a ruling
   that invalidates this cluster's scope → Abort A2.

## Abort conditions

Park action for ALL aborts: write
`engine/store/needs-decision/wg-t3-06-distill-knowledge-capture.json` containing
`{"ticket":"wg-t3-06-distill-knowledge-capture","question":"<one-line question>","note":"<what was observed, with paths>"}`,
leave this ticket in `running/`, stop. Never guess past an abort.

- **A1 — The distillation baseline is gone or contested.** Recon 1 finds <7 kc distillation
  files, or Recon 8 finds foreign uncommitted changes under `research/evaluations/` or the kc
  distillations (someone mid-flight on the same ground). Question: "T3-06's input state is not
  what the war game verified (missing/renamed kc distillations, or foreign dirty files at
  <paths>) — re-scope, or wait for the other work to land?"
- **A2 — A standing decision re-scopes the cluster.** Recon 7 / M1 surfaces a T3-05 (or other
  decisions/) ruling that excludes knowledge-capture, changes the cluster vocabulary it lives
  under, or freezes eval work pending the A–N answers. Question: "Decision <ref> appears to
  gate/re-scope the knowledge-capture eval pass — proceed under old scope, or re-cut the
  worklist per the ruling?"
- **A3 — Eval quality can't clear QC.** M3/M4 fan-out output fails the QC gate twice
  (structural damage, non-discriminating scores, or generic rationales after one sharpened
  re-run). Junk evals poison every later winner-pick. Question: "T3-06's eval fan-out isn't
  clearing the QC bar after a retry (evidence at backlog/wargames/proof/T3-06/) — different
  model, smaller batches, or human-scored sample first?"

## Verification

All from `~/dev/ad/apps/dark-factory`. Positive:

```bash
test -f backlog/wargames/proof/T3-06/worklist.json && python3 -m json.tool backlog/wargames/proof/T3-06/worklist.json >/dev/null && echo PASS-1
python3 - <<'EOF'
import json
w=json.load(open('backlog/wargames/proof/T3-06/worklist.json'))
import os
entries=w if isinstance(w,list) else w.get('entries',[])
missing=[e for e in entries if not e.get('eval_exists') and not e.get('unresolved') and not e.get('source_unavailable')
         and not os.path.exists('research/evaluations/'+e.get('eval_filename',''))]
print('PASS-2' if not missing else f'FAIL-2: {len(missing)} worklist entries still lack evals')
EOF
[ "$(grep -l 'Winner verification (wg-t3-06' research/distillations/knowledge-capture-*.md | wc -l)" -eq 7 ] && echo PASS-3
grep -q 'wg-t3-06' research/distillations/INDEX.md && echo PASS-4
grep -q 'wg-t3-06' research/INDEX.md && echo PASS-5
[ "$(ls backlog/wargames/proof/T3-06/next-tickets/*.json 2>/dev/null | wc -l)" -ge 3 ] && for f in backlog/wargames/proof/T3-06/next-tickets/*.json; do python3 -m json.tool "$f" >/dev/null || echo "BAD $f"; done && echo PASS-6
test -f backlog/wargames/proof/T3-06/REPORT.md && echo PASS-7
git log --oneline -5 | grep -q 'wg-t3-06' && echo PASS-8
```

Negative (must NOT be true):

```bash
git log -1 --format= --name-status -- research/evaluations/ | grep -v '^A' | grep -q . || echo NEG-1   # eval files ADDED only, none modified/deleted
head -2 research/distillations/knowledge-capture-brain-curation.md | grep -q 'distillation_id' && grep -q 'status: draft' research/distillations/knowledge-capture-brain-curation.md && echo NEG-2   # frontmatter untouched, still draft
[ "$(grep -c 'winner_mechanism' research/distillations/knowledge-capture-*.md | awk -F: '{s+=$2} END{print s}')" -eq 7 ] && echo NEG-3   # no winner flips or duplicate frontmatter
ls engine/store/queue/ | grep -q 't3-06a\|t3-06b\|t3-06c' || echo NEG-4   # proposals NOT self-queued
git -C /Users/davidcruwys/dev/upstream/repos/everything-claude-code diff --quiet && git -C /Users/davidcruwys/dev/upstream/repos/gbrain diff --quiet && echo NEG-5   # upstream evidence untouched
git status --short research/artifacts.jsonl research/artifacts/ research/recon/ | grep -q . || echo NEG-6   # corpus + slices + recon untouched
```

## Executor notes (sonnet)

- **Scope fence:** writes ONLY to (1) NEW files under `research/evaluations/`, (2) append-only
  sections at the END of the 7 `research/distillations/knowledge-capture-*.md` files, (3)
  append-only dated blocks in `research/distillations/INDEX.md` and `research/INDEX.md`, (4)
  `backlog/wargames/proof/T3-06/**`. NEVER touch: `research/artifacts.jsonl`, slice files,
  `research/recon/`, pre-existing eval files, `research/distillations-archive-2026-05-26/`,
  `engine/store/queue/`, upstream repos under `~/dev/upstream/`, or `~/dev/ad/appydave-plugins/`
  (including the archived catalog skill — it is read-only reference).
- Frontmatter of the 7 distillations is sacred this ticket: `status: draft` stays,
  `winner_mechanism` stays — even when your evidence contests it. Contested = appendix + report.
- Subagents are in-session Task fan-outs only; never spawn headless/`-p` workers.
- Prefer HITL over guessing exactly where the aborts say so; everything else in the eval scores
  is judgment you are ALLOWED to exercise — that's the evaluating job. Score honestly; a flat
  all-"strong" distribution is a defect, not diplomacy.
- **The rabbit hole:** memory-store-retrieve's 28 sources are 24-parts-Ruflo (AgentDB,
  ReasoningBank, vector/neural/hive-mind). Evaluate each artifact AS A DOCUMENT on the seven
  dimensions — do not research AgentDB internals, do not install or run anything from ruflo,
  do not chase its 305 MCP tools (explicitly deferred to Phase 2.5 / T3-05). Ten minutes per
  artifact, tops; the cluster's verdict was already ASSESSMENT ("infrastructure gap real but
  not blocking") and your job is evidence, not a memory-architecture dissertation. Equally: do
  NOT start ingesting the gap-closers into canonical/ — that is the chained tickets' job,
  gated on the T3-01/T3-02 proof and the validators.
