# T3-26 — Promotion mechanics proof

| field | value |
|---|---|
| ticket | wg-t3-26-promotion-mechanics-proof |
| track / size / priority | T3 Ingestion / S / normal |
| executor | sonnet Swagger via engine |
| depends_on | wg-t3-02-ratify-first-ingestion (the REAL gate is a ratified artifact on disk — Recon 1) |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Run ONE full promote+demote cycle on the library's first ratified artifact to prove the
versioning semantics that so far exist only as prose: a challenger enters `variants/`, David
signs off the swap (HITL — rubric-based promotion doesn't exist yet), the old canonical is
demoted to `variants/was-canonical-<date>.md` byte-identical, the challenger becomes SKILL.md
at `version: 2` with a `version_history[]` event, and `canonical/INDEX.md` reflects it. The
cycle's second deliverable is the procedure itself: `docs/promotion-procedure.md`, pinning the
mechanics (variant naming, swap order, event schema, rollback path) that today are split —
contradictorily — between `docs/architecture.md` §3 and `docs/canonical-form-spec.md`
§Versioning. Done = the artifact is at v2 with a recoverable v1, the procedure doc exists as
executed, and a report sits at `backlog/wargames/proof/T3-26/REPORT.md` (or a documented
DECLINED outcome with the challenger parked as a bench variant and version still 1).

## Locked context

- decisions.md Q2: ingestion is a full campaign — promotion mechanics are named in its scope
  (the T3-26 candidate line: "canonical/INDEX.md + variants/was-canonical-<date>").
- decisions.md Q4: everything through the engine — the human pause uses the engine's
  needs-decision/decisions idiom, no side channels.
- CLAUDE.md hard rule: ratified artifacts NEVER get in-place edits — a change means a version
  bump. Promotion IS the version-bump mechanism; this ticket is its first exercise. Nothing
  edits SKILL.md except the swap itself, and only after David's decision.
- architecture.md §3 (the endorsed model, named by the candidate brief): challenger waits in
  `variants/`; on promotion the old canonical demotes to `variants/was-canonical-<date>.md`;
  provenance records the promotion event; **no artifact is ever destroyed**.
- Interactive `claude` only; HALT/BACKOFF respected; never clear a HALT yourself.

## Recon (verify before any work)

Docs lag code — trust only these checks. Paths repo-relative to `~/dev/ad/apps/dark-factory`
unless absolute. Recon 6–7 are the RE-ENTRY ROUTER (this war game pauses for David and may be
dispatched more than once); they tell you which move to start at.

1. **A ratified artifact exists.**
   `grep -rl '"rewrite_status": "ratified"' canonical/ --include=provenance.json`
   → ≥1 hit (expected: `canonical/skills/review-dimensional/provenance.json` — T3-01/T3-02's
   output; at authoring 2026-07-06 `canonical/` held ONLY `INDEX.md`, so anything here came
   from them). If several are ratified by execution day, use `review-dimensional` when present,
   else the earliest-ratified, and note the choice. **Zero hits** → Abort A1. Call the chosen
   artifact's folder `$ART` for every move below (e.g.
   `ART=canonical/skills/review-dimensional`).
2. **The cycle hasn't already run.**
   `python3 -c "import json;d=json.load(open('$ART/provenance.json'));print(d['version'],len(d['version_history']))"`
   → `1 0`, and `ls $ART/variants/ 2>&1` → "No such file" (no `variants/` exists anywhere in
   `canonical/` at authoring). **version ≥2, non-empty version_history, or an existing
   `variants/was-canonical-*` file** → Abort A5 (proof may already be complete — check
   `backlog/wargames/proof/T3-26/REPORT.md`).
3. **Governing docs + the known contradiction.**
   `grep -c 'was-canonical' docs/architecture.md` → ≥3 (§3's promotion model, verified
   2026-07-06) and `grep -n 'SKILL.md.v1' docs/canonical-form-spec.md` → 1 hit in §"Versioning
   a ratified artifact" (which says "optionally keep SKILL.md.v1" and never mentions
   `variants/` — the contradiction this proof resolves). Either grep empty → the docs were
   since reconciled: read whichever section survives, follow it where it conflicts with this
   war game's mechanics, and record the delta in the report. **Both docs missing** → Abort A1.
4. **Challenger-delta evidence sources** (feeds Fork F1):
   `grep -in 'finding\|version bump\|candidate' backlog/wargames/proof/T3-02/REPORT.md 2>&1`
   (T3-02's executor notes bank "candidates for a future version bump" in its Findings section)
   and `python3 -c "import json;d=json.load(open('$ART/provenance.json'));print([o['set_aside'] for o in d['origins']])"`
   (documented set-asides recoverable from `_source/`). Note what each yields — F1 picks.
5. **Validator, if it landed.** `ls tools/verify-provenance.py 2>&1` → at authoring: missing
   (T3-03 builds it). **Present** → run it in M4 after the swap; a crash = fall back to the
   manual checks written there and record a finding.
6. **Re-entry router — decision state.**
   `ls engine/store/decisions/wg-t3-26-promotion-mechanics-proof.json 2>&1`:
   - **Absent** → continue Recon 7.
   - **Present** → David has decided. `python3 -m json.tool` it; parses → jump to **M4**.
     Unparseable → Abort A3 (NEVER default a corrupt decision to approve — the orchestrator's
     own corrupt-decision handling defaults to approve, orchestrator.py ~617–619; you hold a
     higher bar because a promotion rewrites a ratified artifact).
7. **Re-entry router — park state.**
   `ls engine/store/needs-decision/wg-t3-26-promotion-mechanics-proof.json 2>&1`:
   - **Absent** → fresh run: start at M1.
   - **Present** (and Recon 6 found no decision) → you are a retry re-dispatch of a
     still-parked ticket (engine re-queues an unanswered ungated worker up to MAX_RETRY=2 —
     expected noise, orchestrator.py ~664–670). If
     `grep -c 'DECISION REQUEST' backlog/wargames/proof/T3-26/PLAN.md` → ≥1, the pack is
     complete: write nothing, re-affirm the park per F2 Route B, stop. Pack missing/incomplete
     → resume at M1/M2 to finish it, then M3.
8. **HALT/BACKOFF clear.** `ls engine/store/HALT engine/store/BACKOFF 2>&1` → both "No such
   file". **HALT** → Abort A2. **BACKOFF** → wait for expiry once; second occurrence → A2.

## Moves

### M1 — Pin the challenger delta and register the variant

- **Do:** Pick ONE minimal, evidence-backed improvement via Fork F1 (a Finding from T3-02's
  REPORT.md, or a documented `set_aside[]` item satisfiable from material already in
  `$ART/_source/` — never new harvesting). Then `mkdir -p $ART/variants/` and write
  `$ART/variants/self.v2.md`: the CURRENT SKILL.md body plus exactly that one delta applied,
  nothing else re-worded. (Naming: architecture.md §Naming gives variant files as
  `<provider>.v<n>.md`, e.g. `osmani.v1.md`; a self-improvement challenger's provider is
  `self`. This naming is unspecced elsewhere — it's pinned here and lands in the procedure
  doc; ledger 2.) Record the pre-swap fingerprint now:
  `shasum -a 256 $ART/SKILL.md` — keep the hash for M2/M4.
- **Expect:** `ls $ART/variants/self.v2.md` exists;
  `diff $ART/SKILL.md $ART/variants/self.v2.md | grep -c '^[<>]'` → a small nonzero number
  (the one delta); SKILL.md itself untouched (`git status --short $ART/SKILL.md` → empty).
- **Failure signal:** F1 found no viable delta (no Findings, empty/unsatisfiable set-asides),
  or the delta you drafted needs content not present in `_source/`.
- **Counter-move:** do NOT invent an improvement to have something to promote → Abort A4
  (David names the delta). If SKILL.md shows as modified, `git checkout -- $ART/SKILL.md`
  and redo the variant file only.

### M2 — Build the promotion pack

- **Do:** `mkdir -p backlog/wargames/proof/T3-26` and write
  `backlog/wargames/proof/T3-26/PLAN.md` with EXACTLY these sections:
  1. `## What you are promoting` — 3 lines: `$ART`, the one-line delta, its evidence pointer
     (the T3-02 Finding quoted, or the origin + `set_aside[]` entry quoted).
  2. `## Diff v1 → v2` — output of `diff -u $ART/SKILL.md $ART/variants/self.v2.md`, plus the
     v1 sha256 from M1.
  3. `## Swap plan` — the M4 steps verbatim, including the exact demotion filename
     `variants/was-canonical-<today ISO>.md` and the proposed `version_history[]` event JSON
     (schema below — provenance-spec.md says version_history is "populated on version bump"
     but defines NO shape; this proof pins one; ledger 3):
     `{"version": 2, "date": "<today>", "event": "promotion", "promoted": "variants/self.v2.md -> SKILL.md", "demoted": "SKILL.md v1 -> variants/was-canonical-<today>.md", "change": "<one-line delta>", "evidence": "<pointer from section 1>", "decided_by": "david via engine/store/decisions/wg-t3-26-promotion-mechanics-proof.json", "note": "mechanics proof — rubric-based promotion (L2b) not yet built; David sign-off substitutes"}`
  4. `## Proposed doc changes` — (a) the full outline of `docs/promotion-procedure.md` you
     will write in M5 (variant naming, swap order, event schema, INDEX update, rollback =
     restore from was-canonical, and the steady-state caveat that sign-off-only promotion is
     NOT the standing trigger); (b) ONE proposed line appended to `docs/canonical-form-spec.md`
     §"Versioning a ratified artifact": `4. Promotion/demotion mechanics: see docs/promotion-procedure.md` —
     flagging that its "optionally keep SKILL.md.v1" conflicts with architecture.md's
     mandatory `variants/was-canonical-<date>.md` (Recon 3) and that this proof follows
     architecture.md.
  5. `## DECISION REQUEST` — the vocabulary, literally: `approve` = execute the swap as
     planned · `redirect` + `choice` = adjust the delta/naming/doc-changes per `choice`, then
     swap · `decline` = no swap; challenger stays in `variants/` as a bench variant; say why
     in `note`. Include the exact answer command:
     `echo '{"action":"approve","note":"…"}' > engine/store/decisions/wg-t3-26-promotion-mechanics-proof.json`.
- **Expect:** `grep -c '^## ' backlog/wargames/proof/T3-26/PLAN.md` → 5.
- **Failure signal:** you cannot produce section 2's diff (variant file vanished / unreadable).
- **Counter-move:** re-run M1; if the variant can't be rebuilt from the same evidence → Abort
  A4 with the observation.

### M3 — Park for David (the designed pause)

- **Do:** Write ATOMICALLY (temp file then `mv` — the orchestrator polls every 3s and a
  half-written needs-decision file reads as corrupt):
  ```
  printf '%s\n' '{"ticket":"wg-t3-26-promotion-mechanics-proof","question":"Promote variants/self.v2.md to canonical (demoting v1 to variants/was-canonical-<date>)? Read backlog/wargames/proof/T3-26/PLAN.md then answer approve / redirect(+choice) / decline.","proposed":"Execute the swap per PLAN.md section 3","note":"Designed HITL pause of wg-t3-26 (promotion mechanics proof). Answer: echo <decision-json> > engine/store/decisions/wg-t3-26-promotion-mechanics-proof.json"}' > engine/store/needs-decision/.tmp-t3-26 && mv engine/store/needs-decision/.tmp-t3-26 engine/store/needs-decision/wg-t3-26-promotion-mechanics-proof.json
  ```
  Do NOT write the results self-report yet — under a gated run the gate only locks while that
  file is absent (orchestrator.py ~600). Then → Fork F2 for how the pause plays out.
  Re-affirm branch (Recon 7, pack already complete): write nothing — the park file exists;
  reply per F2 Route B and stop.
- **Expect:** the needs-decision file exists and parses. Gated run: orchestrator logs
  `[HITL] locked ticket …`; when David answers you get a resume message with the decision →
  continue M4 in-session. Ungated run: nothing arrives; you stop.
- **Failure signal:** gated run, no resume within HITL_TIMEOUT=1800s (orchestrator logs
  `no decision in 1800s -> surfaced unanswered`, marks the run failed(no-decision)).
- **Counter-move:** none needed — that outcome IS the ungated path: the park file persists,
  the ticket stays in `running/`, and a post-decision re-dispatch enters at Recon 6 → M4.
  Never write, simulate, or infer David's decision; never report the pause as an error.

### M4 — Execute the verdict (entry point for decision-present re-runs)

- **Do:** Read the decision — from the resume message (gated) or
  `engine/store/decisions/wg-t3-26-promotion-mechanics-proof.json` (re-entry). Re-derive
  `$ART` per Recon 1 and re-verify the M1 fingerprint:
  `shasum -a 256 $ART/SKILL.md` must equal the hash recorded in PLAN.md §2 (if it doesn't,
  someone changed v1 since the pack → Fork F3 trigger b). Branch on `action`:
  - **approve** → the swap, in this exact order:
    1. `cp $ART/SKILL.md $ART/variants/was-canonical-$(date +%Y-%m-%d).md` then
       `shasum -a 256` both files — hashes MUST match (byte-identical demotion).
    2. `mv $ART/variants/self.v2.md $ART/SKILL.md` (the challenger becomes canonical; its
       content is preserved as SKILL.md — nothing destroyed).
    3. Update `$ART/provenance.json` via python (json.load → mutate → json.dump, 2-space
       indent): `version: 2`, `rewrite_date: <today>`, `rewrite_status` stays `"ratified"`,
       and append the PLAN.md §3 event (with real date/filenames) to `version_history[]`.
       Touch NOTHING else in the file — origins are v1 history and stay verbatim.
    4. If Recon 5 found `tools/verify-provenance.py`, run it on `$ART`; else manual: the JSON
       parses, `version == 2`, `len(version_history) == 1`, every `origins[].verbatim_copy`
       still exists, `_source/` untouched (`git status --short $ART/_source/` → empty).
  - **redirect** → apply `choice` if it is delta/naming/doc-shape scope (different wording of
    the v2 delta, different variant/demotion filename, edits to the proposed procedure-doc
    outline): update the variant file + PLAN.md accordingly, then run the approve steps.
    Structural scope → Fork F3.
  - **decline** → NO swap. SKILL.md, provenance, INDEX untouched; `variants/self.v2.md`
    STAYS on disk (a declined challenger remains a bench variant — that is itself the
    "nothing destroyed" semantic, demonstrated). Skip M5's doc-writing (an unexecuted
    procedure must not be published as proven — that would be the docs-lag-code failure this
    repo fights); go to M6 and record the decline verbatim.
- **Expect:** approve/redirect: `was-canonical-<date>.md` hash == the M1/PLAN hash;
  `python3 -c "import json;d=json.load(open('$ART/provenance.json'));print(d['version'],d['rewrite_status'],len(d['version_history']))"`
  → `2 ratified 1`. decline: `git status --short $ART` shows only the untracked
  `variants/self.v2.md`.
- **Failure signal:** the step-1 hashes differ, or provenance.json won't parse after step 3.
- **Counter-move:** stop the swap; `git checkout -- $ART/provenance.json $ART/SKILL.md`
  (both were committed by T3-02) and delete the bad was-canonical copy; retry the swap once.
  Second failure → Abort A6 (leave the tree restored, park with the observation).

### M5 — Register + codify (skip doc-writing on decline)

- **Do:** In this order:
  1. `canonical/INDEX.md`: in the artifact's Skills-table row, bump the `Updated` column to
     today and, if the delta changed the description's first clause, refresh the
     `Description` cell; `## Count` stays `Total artifacts ratified: 1` (a version bump is
     not a new artifact — record this rule in the procedure doc); bump the header's
     `Last Updated`. Do NOT add columns or restructure the table.
  2. Write `docs/promotion-procedure.md` exactly as approved in PLAN.md §4a (adjusted for
     any redirect), documenting: challenger entry (`variants/<provider>.v<n>.md`, `self` for
     self-improvements), the 4-step swap as executed, the pinned `version_history[]` event
     schema, INDEX.md update rule, rollback (= re-promote `was-canonical-<date>.md` by the
     same procedure), and the caveat: David-sign-off substituted for rubric evidence in this
     proof; the standing trigger is benchmark evidence (L2b, unbuilt — T3-15/16).
  3. Append the one pointer line to `docs/canonical-form-spec.md` §"Versioning a ratified
     artifact" per PLAN.md §4b — append-only, delete nothing (if David's note objected,
     skip and record).
- **Expect:** `grep -c 'promotion-procedure' docs/canonical-form-spec.md` → 1 (or a recorded
  skip); `test -f docs/promotion-procedure.md`; `git diff --stat docs/canonical-form-spec.md`
  → 1 insertion, 0 deletions.
- **Failure signal:** the INDEX.md row/placeholder shapes don't match what T3-02 left
  (table restructured since authoring).
- **Counter-move:** update the row minimally wherever the artifact's name appears; if the
  registry no longer has a recognizable row for the artifact at all, that contradicts Recon 1
  → Abort A1 with the observation.

### M6 — Report, results self-report, commit

- **Do:**
  1. Write `backlog/wargames/proof/T3-26/REPORT.md`: outcome (PROMOTED /
     PROMOTED-after-redirect / DECLINED), the decision JSON verbatim, the v1 and
     was-canonical sha256 pair (proof of byte-identical demotion; decline: n/a), the
     version_history event as landed, files written, timings (parked at / decided at — file
     mtimes), and a **Findings** section (spec gaps hit — at minimum the
     architecture-vs-canonical-form-spec contradiction and how it was resolved; anything the
     docs got wrong).
  2. Commit:
     `git add canonical/ docs/promotion-procedure.md docs/canonical-form-spec.md backlog/wargames/proof/T3-26 engine/store/needs-decision engine/store/decisions && git commit -m "feat(canonical): promotion mechanics proof — <artifact> v1->v2 <outcome> (wg-t3-26)"`
     (decline path: the adds pick up only the variant file + proof pack — fine).
  3. LAST: write the results self-report
     `engine/store/results/wg-t3-26-promotion-mechanics-proof.json`:
     `{"ticket":"wg-t3-26-promotion-mechanics-proof","status":"done","files_changed":[…],"commit_sha":"<sha>","notes":"<outcome one-liner>"}`.
- **Expect:** `git log --oneline -1` shows the commit; results file parses.
- **Failure signal:** commit rejected (hook / concurrent dirty store).
- **Counter-move:** commit path-by-path; if `engine/store/` is dirty from a concurrent run,
  commit only your `wg-t3-26*` files and note the concurrency in the report. Results file is
  written regardless — the reaper needs it.

## Forks

**F1 — Where the challenger delta comes from (M1).**
Trigger: Recon 4's two evidence sources.
→ **Route A** (T3-02's REPORT.md Findings contains ≥1 explicit version-bump candidate): use
the first one that is textual and satisfiable without new harvesting; quote it in PLAN.md §1.
→ **Route B** (no usable Finding, but some origin's `set_aside[]` names a mechanism present
in that origin's `_source/` verbatim copy): fold that one item back in; quote the set_aside
entry + source file in PLAN.md §1. Both routes empty → Abort A4.

**F2 — Gated vs ungated pause (how M3 resolves).**
Trigger: after the M3 park, does a resume message arrive?
→ **Route A** (this run was dispatched HITL-gated; your task prompt told you to write
needs-decision and reply `AWAITING_DECISION`): reply exactly `AWAITING_DECISION`, wait; the
orchestrator resumes you with David's decision inline (≤30 min) → M4 in-session.
→ **Route B** (ungated, or gated-but-unanswered): stop after the park — end your turn stating
you are parked awaiting `engine/store/decisions/wg-t3-26-promotion-mechanics-proof.json`.
Expected engine noise: the reaper times you out, re-queues up to twice (each re-dispatch hits
Recon 7's re-affirm branch), then `failed(timeout)` with the ticket left in `running/` — the
park file keeps the question alive. Completion happens on a post-decision re-dispatch via
Recon 6 → M4.

**F3 — Verdict or tree exceeds the pinned swap.**
Trigger: (a) M4 redirect whose `choice` is structural — a different delta needing new
harvesting, add/drop an origin, rename the artifact, change what `kept`/`set_aside` mean, or
"skip the HITL next time" (a standing-trigger policy change); or (b) M4's fingerprint check
shows SKILL.md changed since the pack was built.
→ **Route A** (trigger b, and `git log --oneline -- $ART/SKILL.md` shows the change is
David's own commit/edit): rebuild the variant + PLAN diff on top of his version (his edit is
part of v1, not a verdict), re-park via M3 — the pack he decides on must show the true diff.
→ **Route B** (trigger a, or an unexplained non-David change): → Abort A4 quoting the exact
words/observation; a locked-scope reversal or a policy change is a new ticket, not an
improvisation.

## Assumptions ledger

1. **The ratified artifact is `canonical/skills/review-dimensional/`** (T3-01/T3-02's
   output; authored in parallel, not yet on disk). Recon 1 is name-agnostic — any single
   ratified artifact satisfies the mission. If T3-02 ended DECLINED (its valid alternate
   outcome), there is nothing ratified → Abort A1, and this ticket waits.
2. **Variant naming (`self.v2.md`) and mv-on-promotion are pinned by this proof.** Plausible:
   architecture.md's examples (`osmani.v1.md`, `gsd.v2.md`) give `<provider>.v<n>.md`, and a
   promoted variant's content survives as SKILL.md (nothing destroyed). No other doc specs
   it. If David's verdict overrides either, apply his form and record it in the procedure doc
   — his answer becomes the spec.
3. **The `version_history[]` event schema is this proof's proposal.** provenance-spec.md
   requires the field but defines no shape (verified 2026-07-06). David pre-reads the schema
   in PLAN.md §3; if his note amends it, the amended shape lands in both provenance.json and
   the procedure doc.
4. **David-sign-off may substitute for rubric evidence, once.** architecture.md gates
   promotion on "enough rubric evidence"; the eval harness (L2b) is unbuilt. This proof is
   explicitly a MECHANICS proof — the procedure doc must carry the caveat, and if David's
   note objects to sign-off-substitution itself, that is a decline, not a redirect.
5. **HITL-gated dispatch is possible but not guaranteed** (whether Phase 5's promotion script
   passes `--hitl` was unknown at authoring). The war game converges either way (F2); a third
   dispatch mechanism entirely → park via A3 rather than adapt on the fly.

## Abort conditions

Park action for ALL aborts: write ATOMICALLY (temp + `mv`)
`engine/store/needs-decision/wg-t3-26-promotion-mechanics-proof.json` containing
`{"ticket":"wg-t3-26-promotion-mechanics-proof","question":"<one-line question>","note":"<observation, with paths>"}` —
unless the abort happens AFTER the M3 park, in which case OVERWRITE the existing park file so
the human queue carries the newer, sharper question. Leave the ticket in `running/`; stop.
Never guess past an abort.

- **A1 — No ratified artifact, or canon docs missing** (Recon 1/3, M5 counter-move).
  Question: "T3-26 needs a ratified canonical artifact to promote against: <what's missing>.
  Finish/re-run T3-01+T3-02 first, or re-scope the proof?"
- **A2 — HALT present, or BACKOFF recurs** (Recon 8). Question: "Factory halted/usage-limited
  (<payload>). Resume T3-26 when clear?"
- **A3 — Decision channel corrupt or dispatch shape unknown** (Recon 6, ledger 5). Question:
  "Your decision file for wg-t3-26 is unreadable / dispatch shape unknown: <detail>. Re-write
  the decision?" (Never default-approve a promotion.)
- **A4 — No evidence-backed challenger delta, or verdict exceeds swap scope** (M1/F1 empty,
  F3 Route B). Question: "T3-26 has no evidence-backed v2 delta to promote / your correction
  requires <structural change / new harvest / policy change>. Name the delta, open a new
  ticket, or park the proof?"
- **A5 — Cycle already ran** (Recon 2: version ≥2 / was-canonical present). Question: "The
  promotion cycle already exists on <artifact> (version <n>). Is wg-t3-26 already complete
  (check backlog/wargames/proof/T3-26/REPORT.md), or do you want a second cycle?"
- **A6 — Swap integrity failure, retry exhausted** (M4 counter-move failed twice). Tree
  restored via git first. Question: "The v1→v2 swap on <artifact> failed integrity twice
  (<hashes/paths>). Working tree restored. Investigate before any retry?"

## Verification

From repo root, `$ART` per Recon 1. PROMOTED path (approve or in-scope redirect):

```bash
python3 -c "import json;d=json.load(open('$ART/provenance.json'));print(d['version'],d['rewrite_status'],len(d['version_history']))"   # → 2 ratified 1
python3 - <<'EOF'                                                     # event shape + demotion integrity
import json,glob,hashlib,os,sys
art=glob.glob('canonical/*/*/provenance.json'); art=[a for a in art if json.load(open(a))['version']>=2][0]
d=json.load(open(art)); root=os.path.dirname(art)
ev=d['version_history'][0]
for k in ('version','date','event','promoted','demoted','change','decided_by'): assert k in ev, f'missing event key {k}'
assert ev['event']=='promotion' and ev['version']==2
wc=glob.glob(os.path.join(root,'variants','was-canonical-*.md')); assert len(wc)==1, wc
for o in d['origins']:
    assert os.path.exists(os.path.join(root,o['verbatim_copy'])), o['verbatim_copy']   # _source/ intact
print('PASS-promotion')
EOF
ls $ART/variants/was-canonical-*.md                                    # → exactly one, dated
grep -c "$(shasum -a 256 $ART/variants/was-canonical-*.md | cut -d' ' -f1)" backlog/wargames/proof/T3-26/REPORT.md   # → ≥1 (hash pair recorded = byte-identical demotion proven)
test -f docs/promotion-procedure.md && grep -c 'was-canonical' docs/promotion-procedure.md   # → ≥1
grep -c 'promotion-procedure' docs/canonical-form-spec.md              # → 1 (pointer line; 0 only with a recorded skip)
grep -c 'Total artifacts ratified: 1' canonical/INDEX.md               # → 1 (version bump ≠ new artifact)
test -f backlog/wargames/proof/T3-26/PLAN.md   && echo PASS-pack
test -f backlog/wargames/proof/T3-26/REPORT.md && echo PASS-report
test -f engine/store/decisions/wg-t3-26-promotion-mechanics-proof.json && echo PASS-decision   # David really decided
test -f engine/store/results/wg-t3-26-promotion-mechanics-proof.json   && echo PASS-results
git log --oneline -5 | grep 'wg-t3-26'                                 # → the commit
```

Negative (must NOT be true, any path):

```bash
git status --short research/ | grep . && echo FAIL-touched-research            # frozen corpus
ls $ART/SKILL.md.v1 2>/dev/null && echo FAIL-skillmd-v1                        # the canonical-form-spec alt model must NOT be used
git log --oneline -3 -- $ART/_source/ | grep 'wg-t3-26' && echo FAIL-touched-source   # promotion never edits _source/
git diff HEAD~1 --stat docs/canonical-form-spec.md | grep -E '\s[2-9][0-9]* deletion' && echo FAIL-spec-rewritten   # append-only pointer
git -C ~/dev/ad/appydave-plugins status --short | grep . && echo FAIL-touched-plugins
```

DECLINED path replaces the promoted block with: provenance `version` still 1,
`version_history` empty; no `was-canonical-*` file; `variants/self.v2.md` EXISTS (declined
challenger stays on the bench); no `docs/promotion-procedure.md`; INDEX.md unchanged;
REPORT.md outcome = DECLINED with David's reason verbatim; decision/results/commit checks
unchanged. A run that ends parked (needs-decision present, no decision, ticket in `running/`)
is a valid intermediate state, not a failure.

## Executor notes (sonnet)

- **Scope fence:** write only under `$ART/` (SKILL.md, provenance.json, `variants/`),
  `canonical/INDEX.md`, `docs/promotion-procedure.md`, the ONE appended line in
  `docs/canonical-form-spec.md`, `backlog/wargames/proof/T3-26/`, and your own
  `engine/store/` files. NEVER touch `research/`, `$ART/_source/`, `docs/architecture.md`,
  engine code, other queue tickets, or anything in `~/dev/ad/appydave-plugins/`.
- **The pause is the product's gate.** A promotion without a real decision file from David is
  the one unforgivable failure of this ticket. Never write `engine/store/decisions/…`
  yourself; never infer approval from silence; a parked end-state is a SUCCESSFUL single run.
- **Order discipline in M4:** demote-copy + hash check BEFORE the mv; provenance bump after
  both; INDEX/doc writes only in M5; results self-report LAST (it releases the gate/reaper).
- **Atomic writes** (temp + `mv`) for every `engine/store/needs-decision/` file — a torn read
  parses as corrupt, and the orchestrator's corrupt-decision handling defaults to approve.
- **Prefer HITL over guessing:** doc contradiction resolving differently than Recon 3
  expects, ambiguity about what T3-02 left behind, any verdict you can't classify → park with
  a sharp question. A parked question costs hours; a botched first promotion poisons the
  library's versioning precedent.
- **The rabbit hole:** improving the artifact while you're in there. The v2 delta is ONE
  pinned change — you will see three more things worth folding in, and a tempting "demote it
  back to also prove rollback". Don't: rollback is documented as a procedure path, not
  performed; extra improvements go in REPORT.md Findings as future version-bump candidates.
