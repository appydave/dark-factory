# T3-07 — Distill: system-comprehension (180) — refresh + overlap map

| field | value |
|---|---|
| ticket | wg-t3-07-distill-system-comprehension |
| track / size / priority | T3 Ingestion / M / normal |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

The candidate said "distill the system-comprehension cluster (180 artifacts)" — but authoring
recon found the distillation pass ALREADY RAN on 2026-05-17: five draft files
(`research/distillations/system-comprehension-{repo-onboarding,pre-action-scan,brownfield-forensics,intent-routing,domain-research}.md`)
plus an INDEX section. What is genuinely missing is the candidate brief's second clause: **"map
the overlap with David's existing system-context/understand tooling."** That overlap analysis is
now BADLY stale — since May, David installed the `understand-anything` plugin (v2.7.5, 8
`understand-*` skills, upstream repo never reconned into the corpus), shipped `craft-readme`,
and added `comprehend-visualise`, `session-archaeology`, and the kdd-viewer/project-digest query
CLIs. This ticket produces a **distill-phase addendum**:
`research/distillations/system-comprehension-overlap-map.md` — a per-sub-cluster re-verification
of every winner/gap claim against David's July-2026 tooling, with evidence paths — plus an
appended INDEX section, a proof report, and a commit. Done = the overlap map exists with a
verdict for all 5 sub-clusters, the 5 existing distillation files are byte-untouched, nothing
was ingested into `canonical/`, and the report lists the follow-ups this analysis surfaces.
This is ANALYSIS ONLY: the living-system spec marks all 76 existing distillations provisional
("Do not ingest from them until the cluster's Level 2 is complete" —
`docs/dark-factory-living-system-spec.md` line ~132), and this ticket respects that gate.

## Locked context

- decisions.md Q2: ingestion is a full campaign — cluster distillation work is in scope for T3.
- decisions.md Q4: everything through the engine — this war game is written for sonnet Swagger.
- decisions.md Q9: **complement, don't replace** David's existing skills — the overlap map's
  verdicts must be framed as complement/fold-in recommendations, never "replace system-context".
- Repo hard rule (CLAUDE.md): `research/` is append-only for recon/discover/distill/eval
  outputs. A NEW distill-phase file is a sanctioned append; **rewriting the 5 existing
  distillation files is not** — they stay byte-identical.
- Repo hard rule: nothing enters `canonical/` from this ticket (no provenance.json, no
  `_source/` — because no ingestion happens here at all).
- Living-system spec provisional caveat (above): no ingestion recommendation in the overlap map
  may say "ingest now"; the strongest allowed verdict is "ingestion-ready once L2 coverage
  lands (T3-14) and the provisional sweep (T3-21) clears this cluster".
- T3-05 (the 14 corpus questions A–N) is a sibling, not a dependency: if a verdict genuinely
  hinges on an unanswered corpus question, write the verdict as "pending T3-05: <letter>" —
  never guess the answer.

## Recon (verify before any work)

All paths repo-relative to `~/dev/ad/apps/dark-factory` unless absolute. Docs lag code — trust
only these checks.

1. `ls research/distillations/ | grep '^system-comprehension'` → exactly 5 files:
   `-brownfield-forensics.md`, `-domain-research.md`, `-intent-routing.md`,
   `-pre-action-scan.md`, `-repo-onboarding.md` (all verified present 2026-07-06, frontmatter
   `status: draft`, created 2026-05-17). **An `-overlap-map.md` (or similar refresh file)
   already among them** → Fork F1 before anything else. **Fewer than 5 of the originals** →
   Abort A1.
2. `grep -n 'System-Comprehension Cluster' research/distillations/INDEX.md` → the section
   exists (at authoring: starts ~line 379; its 5-row sub-cluster table names all 5 files;
   header inconsistently says "Distillation files: 4" — known cosmetic bug, record it in the
   report, do NOT fix the frozen section). **Section absent** → the files are still the source
   of truth; reconstruct the claims table from their frontmatter and note the INDEX gap in the
   report.
3. `wc -l research/artifacts/_slice_system_comprehension.jsonl` → 180 (verified 2026-07-06).
   Each line is a JSON artifact with `id`, `repo`, `file_path`, `description_raw`. **Missing**
   → Abort A1.
4. David's live comprehension skills (all verified present 2026-07-06):
   ```bash
   for s in system-context craft-readme brain-query app-query llm-context capture-context session-checkpoint session-archaeology system-audit knowledge-capture; do
     test -d ~/dev/ad/appydave-plugins/appydave/skills/$s && echo "OK $s" || echo "MISSING $s"; done
   ```
   → 10× OK. **Any MISSING** → not a blocker: record it as a landscape change in the overlap
   map itself (a skill David retired since authoring is exactly the kind of drift this map
   exists to capture).
5. The understand-anything plugin (verified 2026-07-06):
   ```bash
   find /Users/davidcruwys/dev/upstream/repos/understand-anything/understand-anything-plugin/skills -name SKILL.md | wc -l   # 8 at authoring
   git -C /Users/davidcruwys/dev/upstream/repos/understand-anything rev-parse --short HEAD      # 470cc01 at authoring
   grep -o '"understand-anything@understand-anything"' ~/.claude/plugins/installed_plugins.json # installed, v2.7.5 cache path at authoring
   ls research/recon/ | grep -c understand                                                      # 0 — repo NEVER reconned into the corpus
   ```
   Record the ACTUAL SHA and skill count you observe — they go in the overlap map. **Repo
   path gone** → Fork F2.
6. Local + CLI comprehension surfaces (verified 2026-07-06):
   `ls .claude/skills/comprehend-visualise/` → exists (dark-factory-local, contains
   `comprehend-fanout.workflow.js`); `ls ~/dev/ad/apps/kdd-viewer/scan.py
   ~/dev/ad/apps/project-digest/digest.py` → both exist. `which query_brain` → **not on PATH
   at authoring** despite root CLAUDE.md claiming it's an installed CLI — another docs-lag-code
   instance; record whatever you observe, don't chase it.
7. `grep -n 'provisional' docs/dark-factory-living-system-spec.md | head -3` → the "76
   distillations … provisional … Do not ingest" caveat (~line 132 at authoring). **Gone/
   reworded to permit ingestion** → note it, but this ticket STILL does no ingestion (scope,
   not just policy).
8. `grep -ci 'system-comprehension' canonical/INDEX.md` → 0 at authoring. **Non-zero** →
   someone already moved this cluster toward canonical/ → Abort A3.
9. Eval coverage: `ls research/evaluations | wc -l` → 88 at authoring;
   `ls research/evaluations | grep -icE 'context|onboard|comprehen|investigate|research'` →
   ~3 loosely related (context-engineering, llm-context, capture-context). This THIN L2
   coverage is itself a headline finding for the map — verify, don't fix.

## Moves

### M1 — Read the existing distillation set (no writes)

- **Do:** Read, in order: (1) the System-Comprehension Cluster section of
  `research/distillations/INDEX.md` (Recon 2); (2) all 5
  `research/distillations/system-comprehension-*.md` files in full; (3) the living-system
  spec's provisional caveat paragraph (Recon 7). Build a working table: sub-cluster → winner
  mechanism → gap verdict as of 2026-05-17 → the specific David-stack claims made (e.g.
  repo-onboarding: "winner appydave:system-context, PATTERN already exists"; brownfield-
  forensics: "no equivalent in David's stack"; intent-routing: "brain-query + app-query +
  llm-context chain exists; context-degradation hook is the gap"; pre-action-scan:
  "context-save/restore gap"; domain-research: "BMAD research skills are thin").
- **Expect:** you can state all 5 winners and every claim about David's stack that needs
  re-verification, without re-reading.
- **Failure signal:** a distillation file contradicts the INDEX table (different winner or
  verdict).
- **Counter-move:** the individual distillation file wins (it is the deeper artifact; the
  INDEX is a summary) — use its claim, record the mismatch in the report.

### M2 — Inventory David's current comprehension surface (read-only)

- **Do:** For each surface below, confirm on disk and capture: absolute path, one-line role,
  and (for skills) the first ~10 lines of SKILL.md frontmatter description. Surfaces —
  (a) the 10 appydave-plugins skills from Recon 4; (b) the 8 understand-anything plugin skills
  (read each `SKILL.md` at
  `/Users/davidcruwys/dev/upstream/repos/understand-anything/understand-anything-plugin/skills/*/SKILL.md`
  — at minimum read `understand`, `understand-onboard`, `understand-domain`,
  `understand-knowledge` in full; skim the rest); (c) `.claude/skills/comprehend-visualise/`
  (dark-factory-local); (d) the query CLIs `~/dev/ad/apps/kdd-viewer/scan.py` and
  `~/dev/ad/apps/project-digest/digest.py` (read each file's docstring/help header only);
  (e) any `deep-research` skill you can locate
  (`find ~/.claude/skills ~/dev/ad/appydave-plugins -maxdepth 3 -iname '*deep-research*'`) —
  if unlocatable, record it as "visible in session listings, location unverified" and move on
  (≤2 minutes on this, it is a footnote not a pillar).
- **Expect:** an inventory table of ≥18 rows (10 + 8 + local + CLIs), each with a real path
  you verified.
- **Failure signal:** a Recon-4/5/6 surface has vanished between recon and now.
- **Counter-move:** re-run the recon check once; still gone → record as "retired since
  2026-07-06" in the inventory (that IS data), continue. understand-anything repo specifically
  gone → Fork F2.

### M3 — Re-verify all 5 sub-cluster claims against the inventory (analysis, no writes yet)

- **Do:** For each sub-cluster, compare the 2026-05-17 claim (M1) with the 2026-07 inventory
  (M2) and assign exactly one verdict from this fixed vocabulary:
  - `STILL-A-GAP` — the May claim of a gap still holds; nothing in the inventory covers it.
  - `NOW-COVERED` — something shipped/installed since May covers the sub-cluster's mechanism.
  - `PARTIALLY-COVERED` — new tooling covers part; name the residual gap in one sentence.
  - `WINNER-STALE` — the named winner's premise changed (skill refactored/retired/superseded).
  - `PENDING-T3-05: <letter>` — verdict genuinely hinges on an unanswered corpus question.
  Mandatory checks per sub-cluster (these are the known drift points; add what you find):
  1. **repo-onboarding** — winner `appydave:system-context` still exists (Recon 4); but
     `craft-readme` (explicitly "complements system-context" in its own description) and
     `understand-onboard` + `understand` now sit on the same territory. Verdict must state how
     the three-way split (CONTEXT.md internal / README external / understand-* exploratory)
     changes the May "PATTERN — already exists" line.
  2. **pre-action-scan** — May said "context-save/restore gap". Check `capture-context` and
     `session-checkpoint` SKILL.md bodies: do they now do branch-aware working-state
     persistence? Judge from their actual text, not their names.
  3. **brownfield-forensics** — May said "no equivalent in David's stack".
     `grep -ril 'investigat\|forensic\|archaeolog' ~/dev/ad/appydave-plugins/appydave/skills/ | head`
     — `session-archaeology` will hit (session-history synthesis, NOT code forensics — say
     why it does not close the gap, or why it partially does).
  4. **intent-routing** — May named the `brain-query + app-query + llm-context` chain. All
     three verified present at authoring; also weigh `understand-knowledge` and the
     `kdd-viewer`/`project-digest` CLIs as new routing surfaces.
  5. **domain-research** — May said "BMAD research skills are thin; planning-question anchor
     is the gap". Weigh `understand-domain` and any located `deep-research` against that.
  Additionally note, per sub-cluster, whether ANY evaluation file in `research/evaluations/`
  covers its winner (Recon 9 says mostly no — per-sub-cluster confirmation goes in the map).
- **Expect:** 5 verdicts, each with ≥1 evidence path from M2 and a one-sentence rationale.
- **Failure signal:** a verdict won't resolve because two live skills contradict each other
  about who owns the territory (e.g. both claim onboarding).
- **Counter-move:** that contradiction IS the finding — verdict `PARTIALLY-COVERED` with the
  contradiction named as the residual question for David. Only if you cannot even determine
  what a David-stack skill DOES (unreadable/empty SKILL.md) → mark that surface "state
  unknown" and proceed; never block on it.

### M4 — Write the overlap map

- **Do:** Write `research/distillations/system-comprehension-overlap-map.md` with:
  - Frontmatter (mirror the existing distillation idiom, Recon 1 files as reference):
    `distillation_id: system-comprehension-overlap-map`, `stage: system-comprehension`,
    `created: <today ISO>`, `status: draft`,
    `refresh_of:` list of the 5 existing distillation filenames,
    `inventory_date: <today ISO>`,
    `understand_anything_sha: <SHA from Recon 5>`.
  - **Section 1 — Why this map exists**: 1 short paragraph (May pass predates
    understand-anything install + craft-readme + comprehend-visualise; candidate T3-07 asked
    for the overlap explicitly).
  - **Section 2 — Current comprehension surface**: the M2 inventory table.
  - **Section 3 — Per-sub-cluster verdicts**: one subsection per sub-cluster: May claim →
    2026-07 verdict (fixed vocabulary) → evidence paths → residual gap sentence → eval
    coverage yes/no.
  - **Section 4 — Out-of-corpus adoption finding**: understand-anything (8 skills, installed
    v2.7.5) entered David's stack WITHOUT passing through recon/discover/distill — the factory
    pipeline was bypassed by real life. State plainly: no `research/recon/understand-anything.md`
    exists; recommend a follow-up recon ticket (name it as a suggestion, do not create it —
    ticket creation is the PO's/promotion's call).
  - **Section 5 — Ingestion readiness**: for each sub-cluster, the strongest allowed line is
    "ingestion-ready once L2 eval coverage lands (T3-14) and the provisional sweep (T3-21)
    clears this cluster" — cite the living-system spec caveat verbatim (one quoted line).
  - Keep the whole file ≤300 lines; it is a map, not a monograph.
- **Expect:** file exists; frontmatter parses visually; all 5 sub-clusters present;
  `wc -l` ≤ 300.
- **Failure signal:** you are re-deriving winner mechanisms or re-clustering artifacts (that
  is regeneration, a different ticket).
- **Counter-move:** cut back to verdict-against-inventory only. The 5 existing files carry
  the mechanisms; this map only says what has CHANGED and what OVERLAPS.

### M5 — Append the INDEX addendum

- **Do:** Append (never insert into, never edit existing sections) a new section at the very
  end of `research/distillations/INDEX.md`, following the retroactive-append idiom already
  used by the Planning and Security-Review sections there:
  ```markdown
  ---

  ## System-Comprehension Overlap Map (2026-07 refresh)

  **Source**: re-verification of the 5 system-comprehension distillations (2026-05-17)
  against David's live tooling as of <today>. Analysis only — no regeneration, no ingestion.
  **File**: [system-comprehension-overlap-map.md](system-comprehension-overlap-map.md)

  | Sub-cluster | 2026-05-17 claim | 2026-07 verdict |
  |---|---|---|
  <one row per sub-cluster, verdict from the fixed vocabulary>

  **Headline**: <1 line — the biggest single change, likely the understand-anything
  out-of-corpus adoption>
  ```
- **Expect:** `tail -30 research/distillations/INDEX.md` shows the new section;
  `git diff --stat research/distillations/INDEX.md` shows additions only (no deletions —
  pure append means 0 removed lines).
- **Failure signal:** the diff shows removed lines, or your edit landed mid-file.
- **Counter-move:** `git checkout -- research/distillations/INDEX.md` and re-append with a
  plain `cat >>` heredoc instead of an editor edit; re-check the diff.

### M6 — Write the proof report

- **Do:** `mkdir -p backlog/wargames/proof/T3-07` and write
  `backlog/wargames/proof/T3-07/REPORT.md` containing: (1) what was produced (paths); (2) the
  5 verdicts in one table; (3) findings — mandatory minimum: (a) the T3-07 candidate premise
  was stale (cluster already distilled 2026-05-17; this run did refresh+overlap, not
  greenfield distillation); (b) understand-anything bypassed the factory pipeline — suggested
  follow-up: recon ticket for the repo; (c) the INDEX "Distillation files: 4" vs 5-files-on-
  disk inconsistency; (d) L2 eval coverage for this cluster is ~3 of 88 eval files —
  quantify what you actually found; (e) `query_brain` PATH discrepancy vs root CLAUDE.md if
  still observed; (f) anything else the run surfaced; (4) a short "what would change these
  verdicts" list (T3-05 answers, T3-14 eval coverage, T3-21 sweep policy).
- **Expect:** report exists; `grep -c '^#\|^##' backlog/wargames/proof/T3-07/REPORT.md` ≥ 4
  (the four numbered parts each have a heading); findings (a)–(d) all present.
- **Failure signal:** a mandatory finding can't be written because its recon observation was
  skipped (e.g. you never counted the eval files).
- **Counter-move:** run the missing recon check now (they are all read-only one-liners) and
  finish the report; never ship the report with a finding replaced by "not checked".

### M7 — Commit

- **Do:**
  ```bash
  cd ~/dev/ad/apps/dark-factory
  git add research/distillations/system-comprehension-overlap-map.md research/distillations/INDEX.md backlog/wargames/proof/T3-07/
  git commit -m "feat(research): system-comprehension overlap map — 5 sub-cluster verdicts vs 2026-07 tooling (wg-t3-07, analysis only)"
  ```
- **Expect:** `git log --oneline -1` shows the commit; `git status --short` shows nothing
  left under the three added paths; the 5 original `system-comprehension-*.md` files do NOT
  appear in the commit (`git show --stat HEAD | grep -c 'system-comprehension-[a-z]*-' → the
  only system-comprehension file in the stat is the overlap map`).
- **Failure signal:** one of the 5 original files shows as modified.
- **Counter-move:** `git restore --staged <file> && git checkout -- <file>` for any of the 5
  originals, verify with `git diff HEAD~1 --stat` after re-committing that only the 3
  intended paths changed. Push if on main and clean (standing preference: commit+push
  finished work; a failed push is a report note, not a blocker).

## Forks

**F1 — An overlap/refresh artifact already exists.**
Trigger: Recon 1 finds `system-comprehension-overlap-map.md` (or any file whose frontmatter
says it refreshes these 5 distillations).
→ **Route A** (its `inventory_date` predates understand-anything's install or it lacks
per-sub-cluster verdicts): treat it as a prior partial pass — read it, keep it byte-identical
(append-only), and write YOUR map as the superseding file
`system-comprehension-overlap-map-<today>.md`, cross-referencing the old one in frontmatter
(`supersedes:`). Note the duplication for David in the report.
→ **Route B** (it already contains verdicts against the July-2026 tooling — understand-anything
present in its inventory): the ticket is already done by someone else → Abort A2.

**F2 — The understand-anything upstream repo is gone or moved.**
Trigger: Recon 5 / M2 can't find `/Users/davidcruwys/dev/upstream/repos/understand-anything`.
→ **Route A** (relocatable): `find /Users/davidcruwys/dev/upstream -maxdepth 3 -iname
'*understand*' -type d` → found → use the new path, record the move.
→ **Route B** (gone from upstream): read the INSTALLED plugin copy instead —
`ls ~/.claude/plugins/cache/understand-anything/understand-anything/*/skills/` (present at
authoring, v2.7.5) — inventory from the cache, record `understand_anything_sha: "unknown —
read from plugin cache v<version>"`, and flag in the report that the upstream clone was
removed. Cache ALSO gone but plugin still in `installed_plugins.json` → inventory it as
"installed, source unreadable" and continue; the map survives with one weaker row.

## Assumptions ledger

1. **A new distill-phase file may be appended to `research/distillations/`.** Plausible:
   CLAUDE.md's research rule permits appends "sourced from a recon/discover/distill/eval
   phase", the INDEX already carries retroactive appends, and `plans/wargames/candidates.js`
   T3-06 (sibling) explicitly targets `research/distillations/`. If David objects at review →
   `git mv` the map to `docs/` and revert the INDEX append — a 2-command undo; flag in the
   report so he sees the placement call.
2. **Refresh + overlap map satisfies the "Distill: system-comprehension" candidate**, rather
   than regenerating the 5 files. Grounded in: the files exist (Recon 1), regeneration of
   provisional distillations is T3-21's policy question, and the candidate brief's own
   emphasis is the overlap. If David wanted full regeneration → that is a new L-size ticket;
   the report's "what would change these verdicts" section says so explicitly.
3. **The 5 sub-cluster structure is stable enough to verdict against.** The INDEX header's
   "4 files" line contradicts the 5 files on disk; assumed cosmetic (the table itself has 5
   rows). If a 6th system-comprehension distillation file exists at execution time → include
   it as a 6th verdict row, note the growth in the report.
4. **No dependency on T3-05/T3-14/T3-21.** This map is read-only analysis and can only be
   IMPROVED by their outputs, not invalidated. If executing after any of them landed → fold
   their answers into the relevant verdicts (e.g. a cleared provisional sweep upgrades
   Section 5's language) and cite them.
5. **understand-anything plugin remains installed at execution time.** If uninstalled by then,
   the inventory row flips to "was installed v2.7.5, since removed" — which strengthens, not
   breaks, the out-of-corpus-adoption finding.

## Abort conditions

Park action for ALL aborts: write
`engine/store/needs-decision/wg-t3-07-distill-system-comprehension.json` containing
`{"ticket":"wg-t3-07-distill-system-comprehension","question":"<one-line question>","note":"<what was observed, with paths>"}`,
leave this ticket in `running/`, stop. Never guess past an abort.

- **A1 — Mission inputs unrecoverable.** Fewer than 5 of the original distillation files exist
  (Recon 1), or the 180-line slice file is missing (Recon 3). `research/` is frozen — missing
  research outputs mean something upstream is broken. Question: "T3-07's inputs (the 5
  system-comprehension distillations / the 180-artifact slice) are missing from the frozen
  research/ tree — restore from git history, or re-scope T3-07 to a from-scratch distill?"
- **A2 — Already done.** A prior overlap map already covers the July-2026 tooling (F1 Route
  B). Question: "T3-07 appears already executed — overlap map at <path> covers
  understand-anything-era tooling. Mark T3-07 obsolete, or is a delta pass wanted?"
- **A3 — Cluster already advanced past analysis.** `canonical/INDEX.md` shows a
  system-comprehension ingestion in progress or ratified (Recon 8), contradicting the
  provisional-gate premise. Question: "system-comprehension artifacts found in canonical/
  (<rows>) despite the living-system spec's do-not-ingest caveat — does T3-07's analysis-only
  framing still stand, or should the overlap map become that ingestion's review input?"

## Verification

All from `~/dev/ad/apps/dark-factory`. Positive:

```bash
test -f research/distillations/system-comprehension-overlap-map.md && echo PASS-1
head -12 research/distillations/system-comprehension-overlap-map.md | grep -q 'distillation_id: system-comprehension-overlap-map' && echo PASS-2
grep -q 'inventory_date' research/distillations/system-comprehension-overlap-map.md && echo PASS-3
for sc in repo-onboarding pre-action-scan brownfield-forensics intent-routing domain-research; do grep -qi "$sc" research/distillations/system-comprehension-overlap-map.md || echo "MISSING-$sc"; done; echo PASS-4-if-no-MISSING-lines
grep -qE 'STILL-A-GAP|NOW-COVERED|PARTIALLY-COVERED|WINNER-STALE|PENDING-T3-05' research/distillations/system-comprehension-overlap-map.md && echo PASS-5
grep -qi 'understand-anything' research/distillations/system-comprehension-overlap-map.md && echo PASS-6
[ "$(wc -l < research/distillations/system-comprehension-overlap-map.md)" -le 300 ] && echo PASS-7
tail -40 research/distillations/INDEX.md | grep -q 'System-Comprehension Overlap Map' && echo PASS-8
test -f backlog/wargames/proof/T3-07/REPORT.md && echo PASS-9
git log --oneline -5 | grep -q 'overlap map' && echo PASS-10
```

Negative (must NOT be true):

```bash
git diff HEAD~1 --name-only | grep -E 'system-comprehension-(repo-onboarding|pre-action-scan|brownfield-forensics|intent-routing|domain-research)\.md' | grep -q . || echo NEG-1   # the 5 originals untouched by the commit
git status --short canonical/ | grep -q . || echo NEG-2                       # nothing ingested
git -C ~/dev/ad/appydave-plugins diff --quiet && echo NEG-3                   # David's live skills untouched
git -C /Users/davidcruwys/dev/upstream/repos/understand-anything diff --quiet 2>/dev/null && echo NEG-4   # upstream untouched (skip silently if repo relocated per F2)
git diff HEAD~1 --numstat -- research/distillations/INDEX.md | awk '{exit ($2>0)?1:0}' && echo NEG-5      # INDEX append-only: 0 deleted lines
grep -qi 'ingest now\|ready to ingest today' research/distillations/system-comprehension-overlap-map.md || echo NEG-6   # provisional gate respected
```

## Executor notes (sonnet)

- **Scope fence:** write ONLY (1) the new
  `research/distillations/system-comprehension-overlap-map.md`, (2) an append-only section at
  the END of `research/distillations/INDEX.md`, (3) `backlog/wargames/proof/T3-07/`. NEVER
  modify the 5 existing `system-comprehension-*.md` files, anything else in `research/`,
  `canonical/`, `docs/`, `~/dev/ad/appydave-plugins/`, or `~/dev/upstream/` (read-only
  evidence). No new tickets, no backlog items — follow-ups are report suggestions.
- This ticket ships a MAP, not skills. If you find yourself drafting SKILL.md text or fold-in
  wording, you have crossed into ingestion — stop and get back to verdicts.
- Verdicts use the fixed vocabulary from M3 verbatim — downstream tickets (T3-14/T3-19-style
  ingestion waves) will grep for those strings.
- Prefer HITL over guessing: territory contradictions between live skills are FINDINGS
  (`PARTIALLY-COVERED` + a named question); missing research inputs and already-ratified
  canonical rows are ABORTS. Nothing in between justifies inventing an answer.
- **The rabbit hole:** the 180-artifact slice is 50% ECC fallback noise (90 artifacts, already
  accounted in the May INDEX section) and the May pass recommends a re-tag pass. Do NOT re-tag,
  re-cluster, or re-read the 180 artifacts one by one — the slice gets a `wc -l` and nothing
  more. Your inputs are the 5 distillation files + the live-tooling inventory. One evidence
  path per verdict beats ten.
