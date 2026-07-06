# T8-05 — DF-ADR provenance flattening + KDD uniformity

| field | value |
|---|---|
| ticket | wg-t8-05-adr-flattening-kdd-uniformity |
| track / size / priority | T8 Doc truth / S / normal |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Dark Factory's 42 DF-ADR decision files (`docs/kdd/decisions/0001…0044`, two pairs merged) carry a
**nested** `provenance:` frontmatter block (`sessions`/`files`/`commits` sub-keys) that flat
frontmatter parsers silently lose — the kdd-viewer store currently shows all 42 decisions as
"no provenance recorded" while the data sits right there in the markdown. Decisions.md Q9 locked
the fix: flatten to Lisa's flat emit convention (top-level `provenance:` scalar +
`sessions:`/`files:`/`commits:` inline lists — the shape Lisa ≥5.12.1 emits and that KBDE's and
Cortex's decisions already carry). Do the flatten (42 files + TEMPLATE.md + the ADR-FORMAT-SPEC
example), record the format **reversal** properly (append-only Revision Log on ADR-0044 — David
ruled the opposite way on 2026-07-04, and that history must stay visible), close the stale
2026-07-04 uniformity findings note, correct kdd-viewer's three stale instance notes, and
re-census all four KDD instances. Done looks like: `python3 query.py` over a fresh scan shows
zero DF decisions with provenance-style "none", all four instances parse to one flat shape with
**no edits to any sibling repo**, both dark-factory and kdd-viewer committed and pushed.

**Authoring-time recon headline (2026-07-06):** the 2026-07-04 findings note's "3 of 4 divergent"
table is already stale in the good direction — KBDE (48/48) **and** Cortex (48/48) decisions now
carry flat YAML frontmatter on disk (the Roamy KDD stream landed the retrofit). Dark Factory is
the **last** divergent instance. The "sweep the 4 instances" is therefore: flatten DF + refresh
the stale truth records + re-scan — NOT a sibling-repo migration.

## Locked context

- **Q9 (plans/wargames/decisions.md):** "DF-ADR provenance flattened to Lisa format" — an
  accepted parked default (2026-07-06). This ticket IS that flatten.
- **Known contradiction, resolved by recency:** ADR-0044's Revision Log (2026-07-04 entry) and
  ADR-FORMAT-SPEC.md's ruling blockquote say the OPPOSITE ("nesting stays, parsers must speak
  YAML — flatten-for-flat-parsers rejected"). Q9 is two days newer and was David's explicit
  interview answer → Q9 wins. The reversal is RECORDED (append to the Revision Log, supersede
  the spec blockquote in place with the old ruling quoted for the record), never silently erased.
- **Append-only Revision Logs / content untouched:** this is a frontmatter-shape migration only.
  ADR body prose (including each `## Provenance` human-readable mirror section) does not change.
  Three ADRs are `status: accepted` (0009, 0028, 0031) — their bodies especially are not to be
  reworded (repo hard rule: ratified artifacts get versions, not in-place edits; a pure
  frontmatter-shape migration authorized by Q9 is the one sanctioned touch).
- **No sibling-repo edits:** Cortex, KBDE, SupportSignal repos are read-only for this ticket.
  Uniformity work outside DF happens only in kdd-viewer's own config/store (its notes are the
  stale doc-truth being fixed — that's this T8 ticket's scope; T8-01's kdd-viewer fence applies
  to T8-01, not globally).
- **Q4:** everything through the engine — you were dispatched by it; leave the ticket lifecycle
  (running/ → done/) to the engine conventions.

## Recon (verify before any work)

All paths relative to `DF=/Users/davidcruwys/dev/ad/apps/dark-factory` unless absolute.
`KV=/Users/davidcruwys/dev/ad/apps/kdd-viewer`. Run every check.

1. **The nested blocks are still there, in the exact shape the flatten script expects.** Run:
   ```bash
   python3 - <<'EOF'
   import glob,re
   ok=0; other=[]
   for p in sorted(glob.glob('/Users/davidcruwys/dev/ad/apps/dark-factory/docs/kdd/decisions/0*.md')):
       fm=re.match(r'^---\n(.*?)\n---\n',open(p).read(),re.S)
       m=fm and re.search(r'^provenance:\s*\n((?:[ \t]+\S.*\n?)+)',fm.group(1),re.M)
       if not m: other.append(('flat-or-missing',p)); continue
       lines=m.group(1).splitlines()
       keys=[re.match(r'\s+(\w+):\s*(\[.*\])\s*$',l) for l in lines]
       if all(keys) and [k.group(1) for k in keys]==['sessions','files','commits']: ok+=1
       else: other.append(('odd-shape',p))
   print('inline-triple:',ok,'other:',other)
   EOF
   ```
   → expect `inline-triple: 42 other: []` (verified 2026-07-06: all 42 are the inline
   sessions/files/commits triple, in that order, flow-style `[...]` lists). All 42 in `other`
   as `flat-or-missing` → the flatten already landed → **Fork F1**. Any `odd-shape` entries →
   note them; Move 1's script hard-fails on them by design → handle per Move 1's counter-move.
2. `git -C $DF status --porcelain -- docs/kdd/` → expect empty (at authoring the repo was clean
   except the untracked war-game portfolio). Any dirt under `docs/kdd/` → someone is mid-edit on
   your seam → **Abort A2**. Also
   `ls $DF/engine/store/running/ | grep -i "t8-05\|adr\|kdd"` → expect only your own ticket;
   a DIFFERENT running ticket matching → **Abort A2**; a done/ sibling matching → **Fork F1**.
3. `grep -n "DF-ADR provenance flattened" $DF/plans/wargames/decisions.md` → expect the Q9 row.
   Missing → you're in the wrong universe → **Abort A1**.
4. **No newer counter-ruling.** `grep -n "2026-07" $DF/docs/kdd/decisions/0044-adopt-a-canonical-df-adr-format.md`
   → expect the Revision Log's two 2026-07-04 lines (initial + the nesting ruling, line ~102)
   and NOTHING dated after 2026-07-06 about provenance shape. Also
   `sed -n '88,94p' $DF/docs/kdd/ADR-FORMAT-SPEC.md` → expect the `> **Ruling (2026-07-04):**`
   blockquote asserting nesting stays. If either file already contains a ruling dated
   **after** Q9 (2026-07-06) re-affirming nesting → David has ruled both ways twice →
   **Abort A1**. If they already record the flatten reversal → **Fork F1**.
5. **Lisa's flat convention is what this war game says it is** (read-only, sets your target
   shape): `sed -n '1,12p' /Users/davidcruwys/dev/kybernesis/KBDE-KyberAgent-Enterprise/docs/kdd/decisions/adr-0001-defer-decoupling-relationship-extraction-enrichment-from-the.md`
   → expect flat top-level `provenance: reconstructed-from-sessions` + `files: [...]` +
   `commits: [...]` keys (no nesting). If that file is unreadable, the same convention is in
   `/Users/davidcruwys/dev/ad/appydave-plugins/appydave/skills/lisa/scripts/reconstruct_kdd.py`
   (~line 603: the emit deliberately drops indented lines — flat-only carry). Both gone →
   proceed anyway; the target shape is fully specified in Move 1.
6. **The measurable defect is live in kdd-viewer:**
   ```bash
   python3 - <<'EOF'
   import json
   d=json.load(open('/Users/davidcruwys/dev/ad/apps/kdd-viewer/store/instances/dark-factory.json'))
   ds=[a for a in d['artifacts'] if a['type']=='decision']
   print('decisions:',len(ds),'provenance-none:',sum(1 for a in ds if a['provenance']['style']=='none'))
   EOF
   ```
   → expect `decisions: 42 provenance-none: 42` (verified 2026-07-06). `provenance-none: 0`
   with the nested blocks still on disk → the viewer grew a nested-YAML parser since authoring
   → the flatten is still Q9-mandated; proceed, but skip the "defect closed" framing in the
   note corrections and state what you observed instead.
7. **Cortex/KBDE really are flat now** (grounds the stale-note corrections you're about to
   write): count decisions whose first line is `---` —
   `head -1 /Users/davidcruwys/dev/kybernesis/KBDE-KyberAgent-Enterprise/docs/kdd/decisions/adr-*.md | grep -c '^---'`
   → expect 48; same over `/Users/davidcruwys/dev/kybernesis/cortex/docs/kdd/decisions/0*.md`
   → expect 48 (both verified 2026-07-06). Numbers lower than 48 → **Fork F3**.

## Moves

1. **Do:** Flatten the 42 decision frontmatters. Write this script to your scratchpad and run it
   (it is deliberately strict — any file not matching the verified inline-triple shape makes it
   exit 1 without touching that file):

   ```python
   import glob, re, sys
   root = '/Users/davidcruwys/dev/ad/apps/dark-factory/docs/kdd/decisions'
   BLOCK = re.compile(r'^provenance:[ \t]*\n((?:[ \t]+\S.*\n)+)', re.M)
   SUB   = re.compile(r'^[ \t]+(sessions|files|commits):[ \t]*(\[.*\])[ \t]*$')
   changed = skipped = 0; errors = []
   for p in sorted(glob.glob(root + '/0*.md')):
       t = open(p).read()
       m = re.match(r'^(---\n)(.*?\n)(---\n)', t, re.S)
       if not m: errors.append((p, 'no frontmatter')); continue
       fm = m.group(2)
       b = BLOCK.search(fm)
       if not b: skipped += 1; continue
       subs = {}
       for line in b.group(1).splitlines():
           sm = SUB.match(line)
           if not sm: subs = None; break
           subs[sm.group(1)] = sm.group(2)
       if subs is None or set(subs) != {'sessions', 'files', 'commits'}:
           errors.append((p, 'odd provenance shape')); continue
       scalar = 'reconstructed-from-sessions' if subs['sessions'].strip('[] \t') else 'hand-authored'
       flat = (f'provenance: {scalar}\n'
               f'sessions: {subs["sessions"]}\n'
               f'files: {subs["files"]}\n'
               f'commits: {subs["commits"]}\n')
       open(p, 'w').write(m.group(1) + fm[:b.start()] + flat + fm[b.end():] + m.group(3) + t[m.end():])
       changed += 1
   print('changed', changed, 'skipped', skipped, 'errors', errors)
   sys.exit(1 if errors else 0)
   ```

   (The sub-key VALUES are carried verbatim — no data is reformatted, only dedented. The one
   all-empty-sessions file is ADR-0044, hand-authored → `provenance: hand-authored`; the other
   41 are Lisa-reconstructed → `provenance: reconstructed-from-sessions`, matching the DF
   learnings' existing scalar.)
   **Expect:** `changed 42 skipped 0 errors []`, exit 0. Then:
   `grep -rn '^[ \t]\+sessions:' $DF/docs/kdd/decisions/0*.md | wc -l` → 0;
   `grep -l '^provenance: reconstructed-from-sessions' $DF/docs/kdd/decisions/0*.md | wc -l` → 41;
   `grep -l '^provenance: hand-authored' $DF/docs/kdd/decisions/0*.md | wc -l` → 1 (ADR-0044);
   `grep -l '^files:' $DF/docs/kdd/decisions/0*.md | wc -l` → 42; and body untouched:
   `git -C $DF diff -- docs/kdd/decisions/ | grep -c '^[-+]## '` → 0.
   **Failure signal:** non-zero exit / `errors` non-empty (files whose provenance block drifted
   from the verified shape), or any Expect count off.
   **Counter-move:** for ≤3 `odd-shape` files, flatten those by hand to the same four-line flat
   form (verbatim values, same key order) and re-run the script for the rest. More than 3
   odd-shape files, or the counts still off after that → the corpus changed shape since
   authoring → `git -C $DF checkout -- docs/kdd/decisions/` and **Abort A1**.

2. **Do:** Update the two format-definition surfaces to the flat shape.
   (a) In `docs/kdd/decisions/TEMPLATE.md`, replace the four nested lines
   (`provenance:               # nested is fine — parsers must speak YAML (ADR-0044, 2026-07-04)`
   plus its three indented sub-lines) with:

   ```yaml
   provenance: reconstructed-from-sessions   # or hand-authored — FLAT, Lisa's emit convention (Q9 2026-07-06; reverses the 2026-07-04 nesting ruling)
   sessions: []
   files: []
   commits: []
   ```

   (b) In `docs/kdd/ADR-FORMAT-SPEC.md`, make the same 4-line swap inside the frontmatter
   example (the `provenance:` + 3 indented lines, ~lines 82–85), and replace the
   `> **Ruling (2026-07-04):** …` blockquote (~lines 90–93) with:

   ```markdown
   > **Ruling (2026-07-06, supersedes 2026-07-04):** DF-ADR `provenance:` is **flattened** to Lisa's
   > flat emit convention — a top-level `provenance:` scalar plus `sessions:`/`files:`/`commits:`
   > inline lists, the shape Lisa ≥5.12.1 emits and every sibling KDD instance (SupportSignal, Cortex,
   > KBDE) now carries. Ruled by David in the war-game portfolio interview
   > (`plans/wargames/decisions.md` Q9); executed by wg-t8-05. The 2026-07-04 ruling it reverses is
   > kept for the record: *"standard YAML is the frontmatter contract — nesting is allowed, and the
   > nested `provenance:` block stays; parsers must be YAML-capable or degrade LOUDLY (fixed in
   > appydave-plugins v5.13.1); silent partial parsing is the defect, not nesting."* See ADR-0044's
   > Revision Log for the full reversal trail.
   ```

   **Expect:** `grep -c '^[ \t]\+sessions:' $DF/docs/kdd/decisions/TEMPLATE.md $DF/docs/kdd/ADR-FORMAT-SPEC.md`
   → 0 in both; `grep -c 'supersedes 2026-07-04' $DF/docs/kdd/ADR-FORMAT-SPEC.md` → 1;
   `grep -c 'nesting is allowed' $DF/docs/kdd/ADR-FORMAT-SPEC.md` → 1 (the old ruling preserved
   inside the new blockquote).
   **Failure signal:** the old blockquote text vanished entirely, or nested lines survive.
   **Counter-move:** `git -C $DF checkout -- <file>` and redo the surgical swap. Second failure
   → the file no longer matches Recon 4's shape → **Fork F1** (someone got here first) or, if
   the found text conflicts rather than pre-empts, **Abort A1**.

3. **Do:** Append the reversal to ADR-0044's Revision Log — add exactly one line at the end of
   the `## Revision Log` list in `docs/kdd/decisions/0044-adopt-a-canonical-df-adr-format.md`
   (touch nothing else in the body; Move 1 already flattened its frontmatter):

   ```markdown
   - 2026-07-06 — amended — REVERSAL of the 2026-07-04 nesting ruling: the war-game portfolio interview (plans/wargames/decisions.md Q9) accepted the parked default "DF-ADR provenance flattened to Lisa format". `provenance:` is now a flat top-level `provenance`/`sessions`/`files`/`commits` set (Lisa's emit convention, reconstruct_kdd.py emit path); all 42 DF-ADRs + TEMPLATE.md + ADR-FORMAT-SPEC.md migrated by wg-t8-05. Uniformity context: Cortex and KBDE decisions already carry flat frontmatter on disk (48/48 each, verified 2026-07-06) — dark-factory was the last divergent instance.
   ```

   **Expect:** `grep -c 'REVERSAL of the 2026-07-04' $DF/docs/kdd/decisions/0044-*.md` → 1;
   `grep -c 'Flatten-for-flat-parsers rejected' $DF/docs/kdd/decisions/0044-*.md` → 1 (the old
   entry survives — append-only); `git -C $DF diff -- docs/kdd/decisions/0044-*.md` shows the
   frontmatter hunk (Move 1) plus ONE added body line, zero removed body lines.
   **Failure signal:** any `-` body line in the diff.
   **Counter-move:** checkout the file, re-run Move 1's script (it will re-flatten just this
   file), redo the append.

4. **Do:** Close the stale findings note. Append this section to the end of
   `backlog/2026-07-04-kdd-uniformity-findings.md`, then
   `git -C $DF mv backlog/2026-07-04-kdd-uniformity-findings.md backlog/done/2026-07-04-kdd-uniformity-findings.done.md`
   (zero inbound references verified 2026-07-06; `backlog/done/` + `.done.md` is the repo's
   completion idiom):

   ```markdown
   ## STATUS — CLOSED (2026-07-06, wg-t8-05)

   Q9 of the war-game portfolio interview (plans/wargames/decisions.md) accepted the parked
   default: DF-ADR provenance flattened to Lisa's flat convention — executed by wg-t8-05
   (42 DF decisions + TEMPLATE.md + ADR-FORMAT-SPEC.md; reversal recorded in ADR-0044's
   Revision Log). The divergence table above is now stale in the good direction: KBDE and
   Cortex decisions ALREADY carry flat frontmatter on disk (48/48 each, verified 2026-07-06 —
   the Roamy KDD stream landed the retrofit), so with dark-factory flattened all four
   instances parse to one flat shape. kdd-viewer stale instance notes corrected and all four
   instances rescanned the same day.
   ```

   **Expect:** `ls $DF/backlog/done/2026-07-04-kdd-uniformity-findings.done.md` exists;
   `ls $DF/backlog/2026-07-04-kdd-uniformity-findings.md` → No such file;
   `grep -c 'STATUS — CLOSED' $DF/backlog/done/2026-07-04-kdd-uniformity-findings.done.md` → 1.
   **Failure signal:** `git mv` refuses (path exists / not tracked).
   **Counter-move:** if a same-named file already sits in `backlog/done/`, keep the move but
   suffix yours `-wg-t8-05.done.md` and note it; if the source file is already gone, someone
   closed it → check its content for a conflicting resolution → matches Q9: continue; conflicts
   with Q9: **Abort A1**.

5. **Do:** Commit and push dark-factory (main, per standing rule). Stage exactly the kdd docs +
   the backlog move:
   `git -C $DF add docs/kdd/ backlog/done/2026-07-04-kdd-uniformity-findings.done.md backlog/2026-07-04-kdd-uniformity-findings.md`
   then commit with message
   `docs(kdd): flatten DF-ADR nested provenance to Lisa flat convention — Q9 reversal recorded in ADR-0044 (wg-t8-05)`
   then `git -C $DF push`. Leave the untracked war-game portfolio and anything else alone.
   **Expect:** push succeeds; `git -C $DF show --stat HEAD` lists exactly: 42 decision files,
   TEMPLATE.md, ADR-FORMAT-SPEC.md, and the renamed backlog file (45 paths, one a rename);
   `git -C $DF status --porcelain -- docs/kdd/ backlog/` → empty (untracked portfolio aside).
   **Failure signal:** push rejected (remote ahead), or extra paths in the stat.
   **Counter-move:** extra paths → `git -C $DF reset HEAD~1`, restage the exact list, recommit.
   Push rejected → `git -C $DF pull --rebase` then push; a rebase conflict inside `docs/kdd/`
   → concurrent writer on your seam → **Abort A2** (leave the rebase aborted:
   `git rebase --abort`).

6. **Do:** Refresh kdd-viewer truth + re-census. In `KV=/Users/davidcruwys/dev/ad/apps/kdd-viewer`:
   (a) Append one sentence to the END of the `"notes"` string (inside the JSON string, before
   its closing quote) in each stale instance config:
   - `instances/dark-factory.json`: ` UPDATE 2026-07-06 (wg-t8-05): the nested-provenance gap described above is CLOSED — decisions.md Q9 (dark-factory war-game portfolio) flattened all 42 DF decision frontmatters to flat provenance/sessions/files/commits; the flat parser now reads decision provenance with no viewer change.`
   - `instances/cortex.json`: ` UPDATE 2026-07-06 (wg-t8-05): the 'NO YAML frontmatter' claim above is STALE — all 48 cortex decisions now carry flat YAML frontmatter on disk (adr_number/title/status/supersedes/created/deciders…), so status badges populate; note kept for history.`
   - `instances/kbde.json`: ` UPDATE 2026-07-06 (wg-t8-05): the 'NO YAML frontmatter' claim above is STALE — all 48 KBDE decisions now carry flat Lisa-convention frontmatter on disk (adr_number/title/status/created/story_reference/provenance/files/commits); note kept for history.`
   (Adjust the two 48s to Recon 7's observed counts if they differed — write what you saw,
   never the authoring-time number.)
   (b) Validate: `python3 -c "import json;[json.load(open(f'/Users/davidcruwys/dev/ad/apps/kdd-viewer/instances/{i}.json')) for i in ['dark-factory','cortex','kbde','supportsignal']];print('json ok')"`.
   (c) Re-census: `cd $KV && for i in dark-factory cortex kbde supportsignal; do python3 scan.py $i; done`
   (scan.py is read-only toward the scanned repos; it rewrites `store/instances/<id>.json` +
   `view/<id>.html`).
   **Expect:** all four scans exit 0; then Recon 6's python check now prints
   `decisions: 42 provenance-none: 0`; and
   `python3 $KV/query.py dark-factory --grep supersede --type decision` still returns the
   ADR-0020/0021 pair (lifecycle intact).
   **Failure signal:** a scan crashes, or `provenance-none` > 0.
   **Counter-move:** scan crash after your JSON edit → your notes string broke the JSON →
   re-run (b), fix the quoting. `provenance-none` > 0 → **Fork F2**.

7. **Do:** Commit and push kdd-viewer — its repo is dirty with UNRELATED files (a deleted
   `plans/goal.txt`, untracked `docs/6*` notes — verified 2026-07-06): stage ONLY
   `git -C $KV add instances/ store/instances/ view/` then commit with message
   `chore(instances): 2026-07-06 KDD uniformity re-census — DF provenance flattened, cortex/kbde stale notes corrected (wg-t8-05)`
   then `git -C $KV push`.
   **Expect:** push succeeds; `git -C $KV show --stat HEAD` touches only `instances/`,
   `store/instances/`, `view/`; `git -C $KV status --porcelain` still shows the pre-existing
   unrelated dirt, untouched.
   **Failure signal:** the commit swept in `plans/goal.txt`'s deletion or the untracked docs.
   **Counter-move:** `git -C $KV reset HEAD~1`, restage the three paths exactly, recommit.
   Push rejected → `pull --rebase` then push; conflict in files you touched → **Abort A2**.

## Forks

**F1 — the flatten already landed (race with a sibling or a Roamy-stream commit).**
Trigger: Recon 1 finds all 42 `flat-or-missing`, Recon 4 finds the reversal already recorded, or
Recon 2 finds a done/ sibling claiming this work.
→ **Route A** (disk state matches this war game's end state: flat frontmatter, spec + ADR-0044
reversal recorded, findings note closed): switch to verify-and-close — run the Verification
block; patch only genuinely missing pieces (commonly: kdd-viewer notes/rescan, Move 6–7, since
that's a second repo); record in the result that the core flatten pre-existed.
→ **Route B** (partially landed — e.g. files flat but ADR-0044/spec still assert nesting, or
flat but with DIFFERENT key names than Lisa's convention): complete only the missing moves if
the landed shape matches this spec exactly; if the landed shape CONFLICTS (different flat
vocabulary, e.g. `provenance_files:`), do not layer a second migration → **Abort A1** with a
sample diff.

**F2 — rescan still shows provenance-none > 0 after the flatten.**
Trigger: Move 6's Expect fails on the store check.
→ **Route A** (data problem): open one offending file (the store JSON's `path` tells you which);
if its frontmatter is malformed (bad quoting, stray indent), fix that file by hand to the
four-line flat form, re-run Move 6(c). This is the expected route for ≤3 stragglers.
→ **Route B** (parser problem): the file on disk is correct flat YAML yet still parses to none —
kdd-viewer's `lib/normalize.py`/`lib/frontmatter.py` changed since authoring (at authoring,
top-level `files`/`commits`/`sessions` are in `RECONSTRUCTED_FIELDS` and a `provenance` scalar
takes precedence — verified). Do NOT freelance parser edits in kdd-viewer → **Abort A3**.

**F3 — Cortex/KBDE are not actually flat at execution time.**
Trigger: Recon 7 counts < 48 on either.
→ **Route A** (counts merely moved — e.g. 52 decisions now, all flat): use observed numbers in
the Move 6 note corrections and proceed; the mission is unchanged.
→ **Route B** (a real regression/mixed corpus — some decisions bare again): DF's flatten still
proceeds (Q9 binds regardless), but "all four instances parse to one flat shape" is no longer
true and fixing sibling repos is outside this ticket's fence → write the honest observed state
into the kdd-viewer notes, finish Moves 1–7, then ALSO park the sibling question:
`engine/store/needs-decision/wg-t8-05-adr-flattening-kdd-uniformity.json` with question
"Cortex/KBDE decisions regressed to bare frontmatter (<observed counts>) — who owns the
retrofit: their own SDLC, a Roamy Lisa re-run, or a DF-issued ticket?" — and note in the result
that the ticket completed with a parked follow-up (this is the one abort-file that does NOT stop
the run; everything in-fence was done).

## Assumptions ledger

1. **`provenance: hand-authored` is an acceptable scalar for ADR-0044** (the one non-reconstructed
   decision; its sessions list is empty). Plausible: Lisa's vocabulary only defines
   `reconstructed-from-sessions`, which would be a lie for a hand-written ADR; "hand-authored" is
   descriptive and the ADR-FORMAT-SPEC itself uses the word. **If false** (David wants a
   different value, or wants the scalar omitted): a one-line edit to one file — note the choice
   prominently in the result so David can veto cheaply; do not park over it.
2. **Moving the findings note to `backlog/done/` is wanted.** Plausible: its open question is
   answered by Q9, `backlog/done/*.done.md` is the established completion idiom, and zero
   inbound references exist (grepped 2026-07-06). **If false** (David prefers findings notes to
   stay put): the closure section is the substance; the move is a `git mv` trivially reversed —
   note it, don't agonize.
3. **Editing kdd-viewer's instance notes + rescanning is in-scope for "KDD uniformity".**
   Plausible: kdd-viewer is the uniformity instrument, its notes are the stale doc-truth this T8
   track exists to fix, and the candidate brief says "sweep the 4 KDD instances to one shape" —
   which the re-census proves. T8-01's "don't touch kdd-viewer" fence is T8-01's own scope
   boundary, not a global rule. **If false**: skip Moves 6–7, finish 1–5, and park the rescan
   question to needs-decision with the Recon 6 before-numbers as evidence.
4. **No Lisa re-run is needed.** Plausible: Lisa ≥5.12.1 already emits flat (verified in
   reconstruct_kdd.py's carry logic), and the updated TEMPLATE.md means future DF emissions
   conform (Lisa's decision template explicitly defers to the host project's own template).
   **If false** (a future reconstruction re-emits nested): that's a Lisa/appydave-plugins bug
   ticket, not this repo's — note it, don't fix Lisa here.

## Abort conditions

- **A1 — ruling/truth conflict.** Recon 3 finds no Q9; Recon 4 finds a post-2026-07-06 ruling
  re-affirming nesting; Move 1's corpus no longer matches any verified shape; Fork F1 Route B or
  Move 4's counter finds a conflicting resolution. Park: write
  `engine/store/needs-decision/wg-t8-05-adr-flattening-kdd-uniformity.json` with
  `{"ticket": "wg-t8-05-adr-flattening-kdd-uniformity", "question": "DF-ADR provenance flatten (Q9, 2026-07-06) conflicts with <found ruling/state, dated> — David has ruled both ways; which is current?", "observed": "<the exact lines/diff found>"}`.
  Revert any partial docs/kdd/ changes (`git -C $DF checkout -- docs/kdd/`), leave the ticket in
  `running/`, stop. Never leave the corpus half-flattened.
- **A2 — concurrent writer on the seam.** Recon 2 dirt under `docs/kdd/`, a running/ sibling on
  ADR/KDD work, or a rebase conflict in files this ticket owns (either repo). Park with question
  "wg-t8-05 collided with a concurrent edit on <paths> — who owns this seam right now?",
  observed = the `git status`/conflict text. Leave in `running/`, stop.
- **A3 — viewer parser drift.** Fork F2 Route B: correct flat data still parses to
  provenance-none. Park with question "kdd-viewer's frontmatter/normalize contract changed —
  DF decisions are flat per Q9 but the store still shows provenance:none; fix the viewer, or was
  the contract redefined?", observed = one file's frontmatter + its store record. The
  dark-factory commit (Move 5) STANDS — data-side work is correct regardless; only Moves 6–7
  stay unfinished. Leave in `running/`, stop.

## Verification

```bash
DF=/Users/davidcruwys/dev/ad/apps/dark-factory
KV=/Users/davidcruwys/dev/ad/apps/kdd-viewer

# 1. No nested provenance blocks anywhere in the decision corpus (incl. TEMPLATE + spec example)
grep -rn '^[ \t]\+sessions:\|^[ \t]\+files:\|^[ \t]\+commits:' \
  $DF/docs/kdd/decisions/ $DF/docs/kdd/ADR-FORMAT-SPEC.md | wc -l          # → 0

# 2. The flat Lisa-convention shape, everywhere
grep -l '^provenance: reconstructed-from-sessions' $DF/docs/kdd/decisions/0*.md | wc -l  # → 41
grep -l '^provenance: hand-authored' $DF/docs/kdd/decisions/0*.md | wc -l                # → 1
grep -l '^files:' $DF/docs/kdd/decisions/0*.md | wc -l                                   # → 42
grep -c '^sessions: \[' $DF/docs/kdd/decisions/0021-*.md                                 # → 1

# 3. The reversal is recorded, append-only
grep -c 'REVERSAL of the 2026-07-04' $DF/docs/kdd/decisions/0044-*.md       # → 1
grep -c 'Flatten-for-flat-parsers rejected' $DF/docs/kdd/decisions/0044-*.md # → 1 (old entry kept)
grep -c 'supersedes 2026-07-04' $DF/docs/kdd/ADR-FORMAT-SPEC.md             # → 1
grep -c 'nesting is allowed' $DF/docs/kdd/ADR-FORMAT-SPEC.md                # → 1 (old ruling quoted)

# 4. Findings note closed and filed
test -f $DF/backlog/done/2026-07-04-kdd-uniformity-findings.done.md && echo filed   # → filed
grep -c 'STATUS — CLOSED' $DF/backlog/done/2026-07-04-kdd-uniformity-findings.done.md  # → 1

# 5. The defect is measurably gone in the re-census
python3 - <<'EOF'
import json
d=json.load(open('/Users/davidcruwys/dev/ad/apps/kdd-viewer/store/instances/dark-factory.json'))
ds=[a for a in d['artifacts'] if a['type']=='decision']
bad=[a['path'] for a in ds if a['provenance']['style']=='none']
print('decisions:',len(ds),'provenance-none:',len(bad),bad[:3])   # → decisions: 42 provenance-none: 0 []
EOF
python3 $KV/query.py dark-factory --grep supersede --type decision | grep -c "0021"   # → ≥1
grep -c 'wg-t8-05' $KV/instances/dark-factory.json $KV/instances/cortex.json $KV/instances/kbde.json | grep -vc ':1$'  # → 0 (each exactly once)

# 6. Negative checks — what must NOT have changed
grep -c '^supersedes: ADR-0020' $DF/docs/kdd/decisions/0021-*.md            # → 1 (lifecycle intact)
grep -l '^status: accepted' $DF/docs/kdd/decisions/0*.md | wc -l            # → 3 (0009, 0028, 0031)
git -C $DF log --oneline -3 | grep -c 'wg-t8-05'                            # → 1
git -C $DF show --stat HEAD~0 -- docs/kdd/decisions/ | grep -c '## '        # (bodies unreworded: spot-check)
git -C $DF diff HEAD~1 HEAD -- research/ canonical/ engine/ CLAUDE.md | wc -l   # → 0
git -C /Users/davidcruwys/dev/kybernesis/cortex status --porcelain | wc -l               # → unchanged from Recon (read-only)
git -C /Users/davidcruwys/dev/kybernesis/KBDE-KyberAgent-Enterprise status --porcelain | wc -l  # → unchanged from Recon (read-only)

# 7. Both repos pushed
git -C $DF status --porcelain -- docs/kdd/ backlog/done/ | wc -l            # → 0
git -C $KV log --oneline -1 | grep -c 'wg-t8-05'                            # → 1
git -C $KV status --porcelain -- instances/ store/ view/ | wc -l            # → 0
```

## Executor notes (sonnet)

- **Scope fence.** Two writable repos ONLY: dark-factory (`docs/kdd/**`, the one backlog file
  move) and kdd-viewer (`instances/*.json`, regenerated `store/instances/`, `view/`). Cortex,
  KBDE, and SupportSignal repos are READ-ONLY — no edits, no commits, no `git pull`, even though
  their stale-looking notes will tempt you. Do NOT touch `docs/kdd/_runs/` (Lisa run history),
  `docs/kdd/learnings/`, `docs/kdd/patterns/` (already flat), `research/`, `canonical/`,
  `engine/*.py`, anything in appydave-plugins (Lisa herself needs no change — she already emits
  flat), or kdd-viewer's `lib/`/`scan.py`/`query.py` code.
- **Frontmatter only, values verbatim.** You are changing the SHAPE of one frontmatter block in
  42 files. Do not rewrap, re-quote, reorder, or "clean up" any other frontmatter field, and do
  not touch body prose — the `## Provenance` body sections stay exactly as the human-readable
  mirror (ADR-FORMAT-SPEC still says so). Three ADRs are `accepted` — their bodies are ratified.
- **The reversal is the sensitive part.** David ruled "keep nesting" on 07-04 and "flatten" on
  07-06. Your job is to execute the newer ruling while keeping the older one visible (Revision
  Log append, old ruling quoted inside the new spec blockquote). If you find ANY sign of a
  third, newer ruling — stop and park (A1); never arbitrate a rule-both-ways loop yourself.
- **The rabbit hole: fixing kdd-viewer's parser or Lisa's emitter.** Reading normalize.py /
  frontmatter.py / reconstruct_kdd.py will surface tempting improvements (real YAML parsing!
  emit `scope`/`confidence` natively! — the spec's own rollout item 7). Resist: flat data makes
  the flat parser correct as-is, and Lisa-side emission work is an explicitly flagged follow-on
  ticket in ADR-FORMAT-SPEC.md, not yours. One line in your result's notes at most.
- **Prefer parking over guessing** on anything touching whose-format-wins across projects
  (F3 Route B): DF issuing format edicts to Cortex/KBDE is exactly the `scope:` boundary
  ADR-0044 exists to police.
