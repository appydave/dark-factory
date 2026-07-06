# T7-04 — Lightweight decision-lineage log

| field | value |
|---|---|
| ticket | wg-t7-04-decision-lineage-log |
| track / size / priority | T7 Self-learning / S / normal |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

`docs/sop-lifecycle.md` names the factory's "no decision record" gap and prescribes the exact fix:
a **lightweight decision-lineage log** — one line per decision ("decided X, diverged from Y,
because Z") tied to workflows — explicitly *instead of* ADR ritual ("A decision log is worth
building only if it's consulted… Prefer lightweight lineage over formal ADR ritual"). The heavy
end already exists (`docs/kdd/decisions/` — 42 DF-ADRs, Lisa-maintained); this ticket builds the
skim layer UNDER it: create `docs/kdd/lineage.md` with a pinned one-line grammar, backfill ≥6 real
seed entries from verifiable sources, and wire three discovery points (kdd index, sop-lifecycle
status note, CLAUDE.md end-of-session capture rule) so lines actually get written. Done looks
like: the file exists, every entry passes a grep-able grammar check, every `ref:` resolves, the
three pointers are in place, and nothing else in the repo changed.

## Locked context

- **Q4 (plans/wargames/decisions.md):** everything through the engine — this ticket is written
  for sonnet Swagger dispatch; self-report to `engine/store/results/` per the orchestrator's
  task prompt.
- **Q9 (decisions.md):** DF-ADR provenance is flattened to Lisa format — the ADR system in
  `docs/kdd/decisions/` is settled and canonical for *heavy* decisions. This ticket complements
  it; it must not modify, renumber, or mirror it.
- **Canonical-source rule (global preferences, repeated in ADR-FORMAT-SPEC.md):** one file owns
  each piece of knowledge; others reference. Lineage lines are *pointers* — a line about an
  already-recorded decision carries a `ref:` to the canonical record, never a restatement that
  could drift.
- **sop-lifecycle.md "Caution: lineage, not ceremony":** the value is "Worker B can see what
  Worker A decided," not the paperwork. Any urge to add fields, frontmatter, sections, or
  tooling beyond the pinned grammar is scope creep → Abort A3.
- **No `-p`/headless/SDK ever; interactive `claude` only** — binds how this ticket runs, not
  its content.

## Recon (verify before any work)

Docs lag code — trust nothing above until these pass. Repo root is
`/Users/davidcruwys/dev/ad/apps/dark-factory`; all paths relative to it.

1. `ls docs/kdd/` → expect `ADR-FORMAT-SPEC.md`, `index.md`, `decisions/`, `learnings/`,
   `patterns/`, `_runs/`. This is the placement anchor. Missing or radically restructured →
   **Abort A2**.
2. `ls docs/kdd/lineage.md docs/decision-lineage.md 2>&1; grep -rin "lineage" docs/kdd/index.md`
   → expect both files ABSENT ("No such file") and no lineage entry in the kdd index (verified
   absent 2026-07-06). If an equivalent log already exists anywhere → **Abort A1**.
3. `grep -n "lightweight lineage\|decided X, diverged from Y" docs/sop-lifecycle.md` → expect
   the "Caution: lineage, not ceremony" paragraph and the gap-table row "A **lightweight
   decision-lineage** log tied to workflows" (verified ≈lines 40–52). This is the mandate; if
   the doc no longer says this, the mandate may have been superseded → **Abort A2**.
4. `grep -n "Y-statements" docs/kdd/ADR-FORMAT-SPEC.md` → expect the paragraph naming the
   one-paragraph form "for high-volume small decisions where full-template ceremony would
   suppress recording them at all" (verified ≈line 47). Confirms the ADR system itself points
   at this gap rather than claiming to fill it. Absent → note in results JSON, proceed anyway
   (Recon 3 is the mandate; this is corroboration).
5. `sed -n '55,58p' engine/orchestrator.py` → expect `NEEDS, DEC = …("needs-decision",
   "decisions")` (verified line 57). Confirms `engine/store/decisions/` is the **mid-task HITL
   gate**, NOT a decision log — do not touch it, do not confuse the two. If the constant moved,
   just note it; nothing in this ticket writes there except an abort-park to `needs-decision/`.
6. Seed-source availability: `grep -c "^| Q" plans/wargames/decisions.md` → expect 10 (the
   locked portfolio decisions, richest seed source). Missing/moved → **Fork F1**. Also
   `ls docs/watchtower/DECISIONS.md engine/store/queue/.CONVENTION.md` → both exist (verified);
   and `git log --oneline -20` → expect decision-shaped commits (e.g. `304e64b` kill-switch,
   `7c619f7` CAP/429 governor — hashes may have been rebased; match by message).
7. `grep -n "^## End-of-session" CLAUDE.md` → expect the section (verified line 105). Missing
   or renamed → **Fork F3**.
8. `ls .gitattributes 2>&1` → expect absent (verified 2026-07-06). If one exists, APPEND to it
   in Move 1 instead of creating it.
9. Baseline: `git status --porcelain | head` → note pre-existing dirt so Move 5's negative
   checks don't blame this ticket for it.

## Moves

### Move 1 — Create `docs/kdd/lineage.md` with the pinned header, plus merge protection

- **Do:** Create `docs/kdd/lineage.md` containing exactly this header (then the `## Log`
  section, initially empty):

  ```markdown
  # Decision lineage — one-line ledger

  The skim layer under the ADRs. One physical line per decision, newest LAST (append-only).
  Mandated by `docs/sop-lifecycle.md` ("lineage, not ceremony"): the value is that Worker B
  can see what Worker A decided — not the paperwork.

  ## Grammar (every line, all six fields, `—` when empty)

      - YYYY-MM-DD · <scope> · decided: <X> · over: <Y> · because: <Z> · ref: <pointer>

  - **scope** — the workflow/SOP/app/ticket the decision is tied to, as a kebab/dot slug
    (`engine.dispatch`, `wargame-portfolio`, `design-lint`, `wg-t1-10`).
  - **decided / over / because** — sop-lifecycle.md's triple: decided X, diverged from Y,
    because Z. `over: —` when nothing was diverged from.
  - **ref** — repo-relative path (optionally `#anchor`), commit hash, or `—`. When the
    decision already has a canonical record (ADR, decisions.md, commit), the line is a
    POINTER to it — never a restatement that can drift.
  - One physical line, no wrapping. If one line can't hold it, put the detail in the ref
    target and keep the line terse. If it needs sections, it's an ADR — go to
    `docs/kdd/decisions/` instead.

  ## What this is NOT

  - Not `docs/kdd/decisions/` (DF-ADRs — heavy, Lisa-maintained; a recurring lineage line
    graduates there, manually).
  - Not `docs/watchtower/DECISIONS.md` (D1–D4, binding, historical — reference, don't retrofit).
  - Not `engine/store/decisions/` (the engine's mid-task HITL gate — unrelated).
  - Not a mirror of the ADR index — only log decisions at the moment they're made, or ones
    with no better home.

  ## Log
  ```

  Then create `.gitattributes` at the repo root (or append, per Recon 8) with the single line
  `docs/kdd/lineage.md merge=union` — two machines append to this file (the Roamy Lisa/KDD
  stream commits into `docs/kdd/` too); union-merge makes concurrent appends conflict-free,
  which is safe for an append-only log.
- **Expect:** both files exist; `grep -c "merge=union" .gitattributes` → 1.
- **Failure signal:** Recon 2 was wrong and a lineage file appeared between recon and now
  (another session), or write fails.
- **Counter-move:** re-run Recon 2; if an equivalent log now exists → Abort A1. A plain write
  failure (permissions/disk) is environmental — retry once, then Abort A2 with the error text.

### Move 2 — Backfill seed entries from verified sources

- **Do:** Append ≥6 (target ~10) real entries under `## Log`, oldest first, drawn ONLY from
  this menu — each `ref:` must be a path/hash you verified exists in Recon 6 or verify now:
  1. `plans/wargames/decisions.md` — the 2026-07-06 locked portfolio decisions with clean
     decided/over/because triples, e.g. Q5 (YLO→POEM parked entirely, over consolidating now),
     Q6 (Watchtower as real web app, over terminal + static boards), Q4 (everything through
     the engine, over Ralphy/spec-first per-app), Q3 (Switchboard state fork deferred to a
     decision ticket, over picking a branch now), Q8 (fleet scope +Roamy, over this-machine-only).
     `ref: plans/wargames/decisions.md` (add `#Q<n>` style anchors only if real).
  2. Recent decision-shaped commits from `git log` — e.g. the HALT flag-file kill switch
     (`304e64b`-era: decided flag-file HALT, over per-process kill, because files survive
     crashes and are the audit trail; `ref:` the commit hash you actually see), the CAP=3/429
     governor commit, the ticket-first standing rule
     (`ref: engine/store/queue/.CONVENTION.md`, dated 2026-07-04 per that file's own header).
  3. `backlog/2026-06-10-design-lint-placement-question.md` + CLAUDE.md's Design-Lint section —
     decided: build design-lint staged in dark-factory · over: direct into appydave-plugins ·
     because: dark-factory stages skill code (dated 2026-06-10).
  4. One line for THIS decision, dated today: decided: lineage log lives at
     `docs/kdd/lineage.md` with a fixed one-line grammar · over: extending the DF-ADR ritual
     downward · because: ceremony suppresses recording (sop-lifecycle.md) ·
     `ref: backlog/wargames/T7-04-decision-lineage-log.md`.

  Every date must come from the source (file header, commit date, decisions.md's 2026-07-06),
  never invented. Then grammar-check the whole log:
  ```bash
  grep -cE '^- [0-9]{4}-[0-9]{2}-[0-9]{2} · [a-z0-9.-]+ · decided: .+ · over: .+ · because: .+ · ref: .+$' docs/kdd/lineage.md
  ```
- **Expect:** the grep count equals the number of `## Log` bullet lines, and is ≥6. Every
  `ref:` path resolves (`ls <path>`) or hash resolves (`git cat-file -e <hash>`).
- **Failure signal:** a line fails the regex (usually a wrapped line or a missing `—`
  placeholder), or a ref doesn't resolve, or you can't find 6 clean triples.
- **Counter-move:** fix the line to fit the grammar (detail goes in the ref target, not the
  line). Unresolvable ref → replace with `—` or drop the entry. Fewer than 6 clean triples
  after exhausting the menu → seed what's real, note the shortfall in the results JSON, and
  continue (never fabricate a decision). If fitting a REAL decision into one line keeps
  failing without loss you'd have to hide → Abort A3.

### Move 3 — Discovery wiring: kdd index + sop-lifecycle status note

- **Do:** (a) In `docs/kdd/index.md`, add one bullet to the existing Decisions/Learnings/
  Patterns list (verified ≈lines 17–21):
  `- [Lineage](lineage.md) — one-line decided/over/because ledger tied to workflows; the skim
  layer under the ADRs (wg-t7-04, 2026-07-06)`.
  (b) In `docs/sop-lifecycle.md`, append one line directly after the "Caution: lineage, not
  ceremony" paragraph (Recon 3 located it):
  `> **Status (2026-07-06):** built — the log is docs/kdd/lineage.md (wg-t7-04).`
  Adjust the date to execution date. Change nothing else in either file.
- **Expect:** `grep -n "lineage.md" docs/kdd/index.md docs/sop-lifecycle.md` → exactly one hit
  in each; `git diff --stat docs/kdd/index.md docs/sop-lifecycle.md` shows ~1 changed line each.
- **Failure signal:** the kdd index list shape has changed and there's no obvious list to
  extend, or sop-lifecycle's caution paragraph is gone.
- **Counter-move:** index shape changed → Fork F2. Caution paragraph gone but the file exists →
  append the status line at the end of the file's decision-lineage-related section (grep
  `lineage`); if the whole mandate is gone you'd have caught it at Recon 3 → Abort A2.

### Move 4 — Capture rule in CLAUDE.md End-of-session

- **Do:** Under `## End-of-session` in `CLAUDE.md` (Recon 7), append this single paragraph,
  verbatim, after the existing backlog-item paragraphs:

  ```markdown
  If this session made a decided-over-because call about how the factory works (a workflow,
  tool, or convention choice), append one line to `docs/kdd/lineage.md` per its header
  grammar. One line, no ceremony — skip if nothing was decided.
  ```

  Touch nothing else in CLAUDE.md.
- **Expect:** `grep -n "lineage.md" CLAUDE.md` → exactly one hit, inside the End-of-session
  section; `git diff --stat CLAUDE.md` shows only this addition.
- **Failure signal:** the End-of-session section is missing/renamed (Recon 7 flagged it), or
  the diff shows more than the added paragraph.
- **Counter-move:** missing section → Fork F3. Over-wide diff → you edited more than asked;
  `git checkout -- CLAUDE.md` and redo this move as a pure append.

### Move 5 — Verify, self-report, commit, push

- **Do:** Run the full Verification battery below. Write the worker self-report to
  `engine/store/results/<this-ticket-filename>.json` in the exact form the orchestrator's task
  prompt demands (include the seed count and any noted shortfalls/drift). Commit the five
  touched files (`docs/kdd/lineage.md`, `.gitattributes`, `docs/kdd/index.md`,
  `docs/sop-lifecycle.md`, `CLAUDE.md`) plus the results file in one commit, message
  `feat(kdd): decision-lineage log — one-line ledger + capture wiring (wg-t7-04)` with the
  standard Co-Authored-By trailer; push.
- **Expect:** every verification command passes; `git log --oneline -1` shows the commit;
  `git status --porcelain` clean apart from Recon 9's pre-existing dirt.
- **Failure signal:** push rejected (non-fast-forward) — likely the Roamy KDD stream pushed.
- **Counter-move:** `git pull --rebase` then push; a conflict in `docs/kdd/lineage.md` cannot
  happen (merge=union) but a conflict in `docs/kdd/index.md` can — resolve by keeping BOTH
  sides' bullets, re-run the Move 3 grep, push again. Second push failure → leave committed
  locally, note it in the results JSON `notes`.

## Forks

**F1 — `plans/wargames/decisions.md` moved or archived at execution time.**
Trigger: Recon 6's grep fails to find the Q-table at that path.
→ **Route A (file relocated):** `git log --follow --oneline -- plans/wargames/decisions.md`
reveals the new path; use it for seeds and refs.
→ **Route B (genuinely gone):** seed entirely from the other menu items (commits,
`.CONVENTION.md`, design-lint backlog item, this ticket's own decision) — the ≥6 floor is
still reachable; note the source loss in the results JSON.

**F2 — `docs/kdd/index.md` restructured by a later Lisa run.**
Trigger: Move 3(a) finds no Decisions/Learnings/Patterns bullet list to extend.
→ **Route A (an index still exists in some form):** add the Lineage link wherever the file
lists its sections, matching the surrounding style; note the drift.
→ **Route B (index.md deleted / kdd reshaped wholesale):** → Abort A2.

**F3 — CLAUDE.md has no `## End-of-session` section.**
Trigger: Recon 7 grep returns nothing.
→ **Route A (a session-closure section exists under another name):** append the capture rule
there instead; note the rename in the results JSON.
→ **Route B (no session-closure section at all):** skip the CLAUDE.md edit entirely — do NOT
invent a new section — and record in the results JSON that capture wiring is partial (the rule
then lives only in lineage.md's header + the kdd index). The log still ships.

## Assumptions ledger

1. **Placement `docs/kdd/lineage.md` is Fable's call** — the interview never asked. Plausible:
   the KDD dir is the decision home, the promotion path (recurring line → DF-ADR) is a
   same-directory hop, and Lisa's domain already receives cross-machine commits. If David
   objects at triage or via HITL: moving is one `git mv` + re-pointing the three wiring edits —
   apply his location and continue. If he instead wants lineage folded INTO the ADR system
   (frontmatter, numbering), that contradicts the sop-lifecycle mandate this ticket exists to
   serve → park to needs-decision/, don't build it.
2. **A one-paragraph CLAUDE.md append is acceptable.** Precedent: commit `f7153d0` added a
   whole Query-tools section to CLAUDE.md as routine docs work. If David objects mid-run →
   revert that one edit (F3 Route B posture) and note it; the ticket still completes.
3. **≥6 clean seed triples exist.** Plausible: decisions.md Q1–Q10 alone offer ~8. If sources
   thinned out (F1 Route B world), seed what's real and note the shortfall — an honest short
   log beats a padded one.
4. **`merge=union` is safe here.** Union merge can interleave concurrent appends out of order —
   acceptable for a dated append-only log (order is recoverable by the date field). If David
   dislikes a repo-root `.gitattributes` → delete it, keep the log, note that cross-machine
   appends will occasionally need a trivial hand-merge.

## Abort conditions

**A1 — An equivalent log already exists.** Recon 2 (or Move 1's re-check) finds
`docs/kdd/lineage.md`, `docs/decision-lineage.md`, or any lineage-shaped one-liner ledger
already present/referenced. Park: write
`engine/store/needs-decision/wg-t7-04-decision-lineage-log.json` containing
`{"ticket":"wg-t7-04-decision-lineage-log","question":"A decision-lineage log already exists at <path> (found <date>). Extend it to the T7-04 grammar, or supersede it?","proposed":"extend in place if its shape is one-line-per-decision; supersede only if it is ADR-shaped","note":"<what was found>"}`.
Leave the ticket in `running/`. Two competing lineage logs is exactly the drift disease this
ticket treats — never create the second one.

**A2 — The anchor or the mandate is gone.** `docs/kdd/` missing/radically restructured with no
index (F2 Route B), or `docs/sop-lifecycle.md` no longer mandates lightweight lineage (Recon 3),
or an environmental failure survives a retry. Park to needs-decision/ (same shape as A1;
question: "T7-04's placement anchor / mandate has drifted since authoring: <what changed>.
Where should the lineage log live now — or is it superseded?"). Leave the ticket in `running/`.

**A3 — Ceremony creep.** You catch yourself adding fields beyond the six, frontmatter,
per-entry files, sections per decision, or a second format tier — OR real decisions repeatedly
cannot fit one line without material loss. Both mean the one-line premise needs David, not a
richer format invented by the executor. Park to needs-decision/ with the concrete offending
example in `note`. Leave the ticket in `running/`.

## Verification

Run from `/Users/davidcruwys/dev/ad/apps/dark-factory`:

```bash
ls docs/kdd/lineage.md                                                    # exists
grep -c "## Log" docs/kdd/lineage.md                                      # 1
N=$(grep -cE '^- [0-9]{4}-[0-9]{2}-[0-9]{2} · [a-z0-9.-]+ · decided: .+ · over: .+ · because: .+ · ref: .+$' docs/kdd/lineage.md); echo $N   # ≥6
grep -A200 '^## Log' docs/kdd/lineage.md | grep -c '^- '                  # equals $N (every log line passes the grammar)
grep -c "merge=union" .gitattributes                                      # ≥1
grep -c "lineage.md" docs/kdd/index.md                                    # 1
grep -c "lineage.md" docs/sop-lifecycle.md                                # 1
grep -c "lineage.md" CLAUDE.md                                            # 1 (0 only under Fork F3 Route B, noted in results)
ls engine/store/results/ | grep -c wg-t7-04                               # 1 — worker self-report exists
```

Every `ref:` in the log resolves: for each path ref `ls <path>` succeeds; for each hash ref
`git cat-file -e <hash>` succeeds.

Negative checks (nothing else changed):
```bash
git diff --stat HEAD~1 -- docs/kdd/decisions docs/kdd/learnings docs/kdd/patterns \
  docs/kdd/ADR-FORMAT-SPEC.md docs/watchtower/DECISIONS.md engine/ tools/       # empty
git diff HEAD~1 --stat -- CLAUDE.md                                             # ≤ ~5 added lines, 0 deletions
crontab -l 2>&1 | grep -ci lineage                                              # 0 — no scheduling was added
```

## Executor notes (sonnet)

- **Scope fence:** create `docs/kdd/lineage.md` + `.gitattributes` (or one appended line to an
  existing one); single-point edits to `docs/kdd/index.md`, `docs/sop-lifecycle.md`,
  `CLAUDE.md`; the results self-report — NOTHING else. Do not touch `docs/kdd/decisions/`,
  `docs/watchtower/DECISIONS.md`, `engine/` (except the results/needs-decision store files
  this ticket's lifecycle requires), or any `tools/`.
- **Pointers, not prose.** Seed lines cite their source in `ref:`; if you're writing a second
  sentence, you're doing it wrong.
- **Do not mirror the 42 ADRs into the log.** They have their own index; the log covers
  decisions at the moment they're made plus the handful of seeds named in Move 2.
- **Prefer HITL over guessing** on anything placement- or format-shaped: a needs-decision/
  park costs minutes; a second competing decision system costs exactly the drift this ticket
  exists to prevent.
- **The rabbit hole:** you will be tempted to build tooling — a `lineage.py` append/validate
  CLI, a git hook, a Watchtower view, recurrence counting, auto-promotion to ADR. Skip ALL of
  it. `echo >>` is the writer and `grep` is the reader; that IS the design (sop-lifecycle.md:
  "lineage, not ceremony"). Automation over this log is a future ticket if the log proves it
  gets consulted.
