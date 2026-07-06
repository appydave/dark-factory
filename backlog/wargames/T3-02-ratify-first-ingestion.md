# T3-02 — Voice-review + ratify first ingestion

| field | value |
|---|---|
| ticket | wg-t3-02-ratify-first-ingestion |
| track / size / priority | T3 Ingestion / S / high |
| executor | sonnet Swagger via engine |
| depends_on | wg-t3-01-first-ingestion-review-dimensional (the T3-01 harvest+draft war game — the REAL gate is its disk artifacts, checked in Recon 1) |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Session 2 of the first-ever canonical ingestion (locked split: session 1 = harvest+draft,
session 2 = voice-review+ratify). T3-01 left `canonical/skills/review-dimensional/` with a
David-voice draft SKILL.md, provenance.json, and verbatim `_source/` copies. This ticket runs
the mechanical validation checklist, builds a voice-review pack for David, PAUSES for his
human decision (the engine's needs-decision/decisions idiom — this pause is designed, not a
failure), then applies his verdict: ratify (`rewrite_status: "ratified"`), register in
`canonical/INDEX.md`, close the 2026-05-18 backlog item, and — the second half of the mission —
correct `docs/david-style-patterns.md` from real evidence for the first time (the file is
self-declared "seed version — refine as canonical artifacts get ratified"). Done = registry
count goes 0→1 (or a documented DECLINED outcome), style-patterns carries ≥1 evidence-backed
addition, and a report exists at `backlog/wargames/proof/T3-02/REPORT.md`.

## Locked context

- decisions.md Q2: ingestion is a full campaign — this is its first ratification gate.
- decisions.md Q9: artifact name is `review-dimensional`; it COMPLEMENTS David's existing
  review-* skills (never replaces them); the `delivery-review` orchestrator stays untouched;
  session split = harvest+draft (T3-01) / voice-review+ratify (THIS ticket).
- decisions.md Q4: everything through the engine — the human pause uses the engine's
  needs-decision/decisions idiom, no side channels.
- CLAUDE.md hard rule: ratified artifacts NEVER get in-place edits afterwards — every SKILL.md
  edit in this ticket must happen BEFORE the `rewrite_status` flip (M5). After the flip,
  changes require a version bump (out of scope here).
- Interactive `claude` only; HALT/BACKOFF respected; never clear a HALT yourself.

## Recon (verify before any work)

Docs lag code — trust only these checks. Paths repo-relative to `~/dev/ad/apps/dark-factory`
unless absolute. Recon 6–7 are the RE-ENTRY ROUTER: this war game is designed to run more than
once (pause → David decides → resume run); they tell you which move to start at.

1. **T3-01 artifacts exist.** `ls canonical/skills/review-dimensional/` → `SKILL.md`,
   `provenance.json`, `_source/` (at authoring 2026-07-06 `canonical/` held ONLY `INDEX.md` —
   everything under `skills/` is T3-01's output). `_source/` must hold ≥1 file (the 05-18
   backlog item names 4 origins; fewer is T3-01's documented call, zero is a broken harvest).
   **Missing folder, missing SKILL.md, or empty `_source/`** → Abort A1.
2. **Draft is reviewable (in David's voice already).**
   `python3 -c "import json;print(json.load(open('canonical/skills/review-dimensional/provenance.json'))['rewrite_status'])"`
   → `in-style` (per the Q9 split T3-01 drafts the voice). `draft` + a SKILL.md whose body is
   clearly Template-A/B/C shaped (purpose line → Behavior → Output → Anti-patterns per
   `docs/david-style-patterns.md`) → treat as in-style with a stale status field, note it, and
   proceed. `draft` + body still in origin voice (marketing prose, "This skill provides…") →
   Fork F1. **`ratified` already** → Abort A5 (never re-edit a ratified artifact in place).
3. **Governing docs present** (they are the checklist source):
   `ls docs/canonical-form-spec.md docs/provenance-spec.md docs/ingestion-workflow.md docs/david-style-patterns.md`
   → all four. **Any missing** → Abort A1 (the ratification bar is undefined without them).
4. **Validators: use them if they landed.** `ls tools/verify-provenance.py tools/style-check.py 2>&1`
   → at authoring: both missing ("No such file") — T3-03/T3-04 build them and may have landed
   by execution day. **Present** → run them in M1 instead of the manual greps (their verdict
   supersedes the manual checklist; a crash in the tool = fall back to manual and record a
   finding). **Absent** → manual checklist in M1, as written.
5. **Backlog item location** (Step-11 close target):
   `ls backlog/2026-05-18-first-ingestion-code-review.md backlog/done/2026-05-18-first-ingestion-code-review.md 2>&1`
   → exactly one exists. In `backlog/` = you close it in M5. Already in `backlog/done/` =
   T3-01's war game moved it; you only APPEND the ratify result there in M5. **Neither** →
   proceed (M5 skips the move, report notes the missing item); **both** → keep the `done/`
   copy, flag the duplicate in the report.
6. **Re-entry router — decision state.**
   `ls engine/store/decisions/wg-t3-02-ratify-first-ingestion.json 2>&1`:
   - **Absent** → first pass (or pre-decision retry): continue Recon 7.
   - **Present** → David has decided. Verify it parses
     (`python3 -m json.tool engine/store/decisions/wg-t3-02-ratify-first-ingestion.json`) and
     jump to **M4**. Unparseable → Abort A3 (NEVER default a corrupt decision to approve — the
     orchestrator's own corrupt-decision behavior defaults to approve, orchestrator.py ~617–619;
     you hold a higher bar because ratification is one-way).
7. **Re-entry router — park state.**
   `ls engine/store/needs-decision/wg-t3-02-ratify-first-ingestion.json 2>&1`:
   - **Absent** → fresh run: start at M1.
   - **Present** (and Recon 6 found no decision) → you are a retry re-dispatch of a still-parked
     ticket (the engine re-queues an unanswered ungated worker up to MAX_RETRY=2 — expected
     noise, orchestrator.py ~664–670). Check the pack:
     `grep -c 'DECISION REQUEST' backlog/wargames/proof/T3-02/REVIEW.md` → ≥1 means the pack is
     complete — do NOT rebuild it; re-affirm the park (M3, write-nothing branch) and stop.
     Pack missing/incomplete → resume at M1/M2 to finish it, then M3.
8. **HALT/BACKOFF clear.** `ls engine/store/HALT engine/store/BACKOFF 2>&1` → both "No such
   file". **HALT** → Abort A2. **BACKOFF** → wait for expiry once (the engine auto-clears);
   second occurrence → Abort A2.

## Moves

### M1 — Mechanical validation of the draft (record, don't fix)

- **Do:** Run the Step-8 checklist (`docs/ingestion-workflow.md`) mechanically and RECORD every
  result — no edits to `canonical/` in this move (if this run is HITL-gated, the engine's gate
  instruction forbids pre-decision edits; deferring fixes to M4/M5 keeps both gated and ungated
  paths identical). If Recon 4 found the validators, run
  `python3 tools/verify-provenance.py canonical/skills/review-dimensional` and
  `python3 tools/style-check.py canonical/skills/review-dimensional` and record their output
  instead of the manual equivalents below. Manual checks, from repo root:
  1. `python3 -m json.tool canonical/skills/review-dimensional/provenance.json > /dev/null && echo PARSES`
  2. Required fields per `docs/provenance-spec.md` field table — check `canonical_id`,
     `canonical_type`, `canonical_name`, `version`, `rewrite_status`, `rewrite_date`,
     `rewrite_author`, `origins[]` (≥1, each with `source_repo`, `source_path`, `harvested_at`,
     `verbatim_copy`, `kept` non-empty, `modified`, `set_aside`), `version_history` (must have
     exactly 0 entries for version 1).
  3. Every `origins[i].verbatim_copy` exists on disk; every file under `_source/` is referenced
     by some origin (no orphans).
  4. Frontmatter: `sed -n '/^---$/,/^---$/p' canonical/skills/review-dimensional/SKILL.md` →
     has `name: review-dimensional`, `description`, `argument-hint` (or a noted N/A),
     `allowed-tools`.
  5. Description discipline: trigger-only, ≤2 sentences, ≥3 explicit trigger phrases
     ("Use when…" phrasing, per `docs/canonical-form-spec.md` §Description discipline). A
     workflow summary ("This skill reviews…") is a FAIL.
  6. `wc -l canonical/skills/review-dimensional/SKILL.md` → body ≤400 lines (or `references/`
     used for overflow).
  7. Stack-agnostic scan:
     `grep -nEi 'npm |yarn |pnpm |eslint|prettier|pytest|rspec|tsconfig|TypeScript|node_modules' canonical/skills/review-dimensional/SKILL.md`
     → ideally no hits in the BODY (hits inside the frontmatter `allowed-tools` line or inside
     a quoted "origin says X → rewrite to Y" example are acceptable; judge per
     `docs/david-style-patterns.md` §Stack-locked table and record any accepted exception).
  8. The two locked fold-ins from the 05-18 backlog item are present in the body: depth
     calibration (Quick/Standard/Deep) and the 4-question pre-report gate — `grep -in 'depth\|quick.*standard.*deep\|four.question\|4.question' canonical/skills/review-dimensional/SKILL.md`
     → hits for both concepts. Absent = T3-01 set them aside; check `provenance.json`
     `set_aside[]` for a documented reason and record which way it went.
- **Expect:** a pass/fail line per check, captured into a table you keep for M2. Failures are
  EXPECTED at this stage — that's what the review is for.
- **Failure signal:** a check cannot be evaluated at all (provenance unparseable, SKILL.md
  unreadable) rather than merely failing.
- **Counter-move:** unparseable provenance.json or missing SKILL.md at this point contradicts
  Recon 1–2 → re-run Recon; if confirmed broken → Abort A1. Everything else: record and
  continue — fixes come after David's decision.

### M2 — Build the voice-review pack

- **Do:** `mkdir -p backlog/wargames/proof/T3-02` and write
  `backlog/wargames/proof/T3-02/REVIEW.md` with EXACTLY these sections:
  1. `## What you are ratifying` — 3 lines: artifact path, one-line purpose, origins count +
     repos (from provenance.json).
  2. `## Checklist results` — the M1 table verbatim, failures at top, each failure with the
     one-line fix you PROPOSE to apply post-approval.
  3. `## Voice evidence` — side-by-side: (a) the draft's full frontmatter description vs the
     description of `~/dev/ad/appydave-plugins/appydave/skills/review-blind-hunter/SKILL.md`
     (the tone anchor named by the 05-18 backlog item — read it, quote it); (b) the draft's
     Behavior section vs the 8 voice rules in `docs/david-style-patterns.md` §Voice — cite any
     rule the draft strains, with the draft's exact line quoted.
  4. `## Proposed corrections to david-style-patterns.md` — the ≥1 evidence-backed additions
     you intend to append in M6, drafted in full so David reviews them in the same pass. Source
     each from real evidence only: a rewrite decision recorded in provenance `modified[]`, a
     checklist failure pattern from M1, or a gap you hit applying the doc (e.g. a rewrite case
     its "Common rewrites" table doesn't cover). Inventing a pattern with no evidence pointer
     is a defect.
  5. `## DECISION REQUEST` — the decision vocabulary, literally:
     `approve` = ratify as-is (M1 mechanical fixes applied first) · `redirect` + `choice` =
     apply the voice corrections in `choice`, then ratify · `decline` = do not ratify; say why
     in `note`. Include the exact answer command for David:
     `echo '{"action":"approve","note":"…"}' > engine/store/decisions/wg-t3-02-ratify-first-ingestion.json`.
- **Expect:** REVIEW.md exists, all 5 sections present, `grep -c '^## ' backlog/wargames/proof/T3-02/REVIEW.md` → 5.
- **Failure signal:** you cannot quote voice evidence because the anchor skill at
  `~/dev/ad/appydave-plugins/appydave/skills/review-blind-hunter/SKILL.md` is missing (existed
  2026-07-06).
- **Counter-move:** substitute any of `review-edge-case-hunter` / `review-code-quality` from
  the same folder (also verified 2026-07-06) and note the substitution; if the whole
  `appydave-plugins` skills folder is gone → Abort A1 (voice canon lost = no review possible).

### M3 — Park for David (the designed pause)

- **Do:** Write ATOMICALLY (temp file then `mv` — the orchestrator polls every 3s and a
  half-written needs-decision file is read as corrupt):
  ```
  printf '%s\n' '{"ticket":"wg-t3-02-ratify-first-ingestion","question":"Ratify canonical/skills/review-dimensional as the first canonical artifact? Read backlog/wargames/proof/T3-02/REVIEW.md then answer approve / redirect(+choice) / decline.","proposed":"Ratify after applying the mechanical fixes listed in REVIEW.md section 2","note":"Designed HITL pause of wg-t3-02 (voice-review+ratify). Answer: echo <decision-json> > engine/store/decisions/wg-t3-02-ratify-first-ingestion.json"}' > engine/store/needs-decision/.tmp-t3-02 && mv engine/store/needs-decision/.tmp-t3-02 engine/store/needs-decision/wg-t3-02-ratify-first-ingestion.json
  ```
  Do NOT write the results self-report (`engine/store/results/wg-t3-02-ratify-first-ingestion.json`)
  — under a gated run the gate only locks while that file is absent (orchestrator.py ~600).
  Then → Fork F2 (gated vs ungated) for how the pause plays out.
  Re-affirm branch (from Recon 7, pack already complete): write nothing — the park file already
  exists; just reply per F2 Route B and stop.
- **Expect:** the needs-decision file exists and parses. Gated run: the orchestrator log prints
  `[HITL] locked ticket …` and, once David answers, sends you a resume message containing the
  decision — continue at M4 in-session. Ungated run: nothing arrives; you stop.
- **Failure signal:** gated run and no resume message within the engine's HITL window
  (HITL_TIMEOUT=1800s → the orchestrator logs `no decision in 1800s -> surfaced unanswered`
  and marks the run failed(no-decision)).
- **Counter-move:** none needed — that outcome IS the ungated path: the park file persists,
  the ticket stays in `running/`, and a later re-dispatch (after David writes the decision)
  enters at Recon 6 → M4. Never simulate, assume, or write David's decision yourself, and never
  treat the pause as an error in the report.

### M4 — Apply the verdict (entry point for decision-present re-runs)

- **Do:** Read the decision — from the in-session resume message (gated) or
  `engine/store/decisions/wg-t3-02-ratify-first-ingestion.json` (re-entry). Branch on `action`:
  - **approve** → apply the M1 mechanical fixes exactly as proposed in REVIEW.md §2 (these are
    draft-stage fixes: provenance field gaps, description tightening, orphan `_source/` file
    referencing — nothing structural), update provenance `modified[]` for anything you changed
    in SKILL.md, re-run the failed M1 checks to confirm green → M5.
  - **redirect** → the `choice`/`note` text is David's voice correction. If it is textual/voice
    scope (wording, description, section shape, tone) → apply it to SKILL.md + the M1 fixes,
    update provenance `modified[]`, re-run the checklist → M5. If it changes MECHANISM or scope
    (different `kept`/`set_aside` decisions, add/drop an origin, rename the artifact, touch
    `delivery-review`) → Fork F3.
  - **decline** → NO ratification. Do not edit SKILL.md. Record David's reason verbatim in the
    report; leave `rewrite_status` as-is; skip M5; go to M6 (the decline reason is itself
    style-patterns evidence) then M7. The backlog item stays open — append a `## Status`
    section to it quoting the decline instead of closing it.
- **Expect:** approve/redirect: every previously-failing M1 check now passes. decline: zero
  changes under `canonical/`.
- **Failure signal:** a checklist item STILL fails after applying fixes, or David's redirect
  is self-contradictory (e.g. demands a workflow-summary description, which
  `docs/canonical-form-spec.md` forbids).
- **Counter-move:** one more fix iteration, re-check. Still failing, or spec-vs-David conflict
  → do not ratify against the spec and do not overrule David: re-park (fresh needs-decision
  file quoting the exact conflict — "your correction X violates spec rule Y; amend spec or
  revise correction?"). A SECOND redirect round after that re-park gets one more application
  pass; a third → Abort A4.

### M5 — Ratify + register (skip entirely on decline)

- **Do:** In this exact order (nothing may edit SKILL.md after step 1):
  1. Final read: confirm SKILL.md is the text David approved — then flip
     `canonical/skills/review-dimensional/provenance.json`: `"rewrite_status": "ratified"`,
     `"rewrite_date": "<today ISO>"`. Keep `version: 1`, `version_history: []`.
  2. Update `canonical/INDEX.md`: replace the Skills-table placeholder row
     (`*(none yet — first ingestion…)*`) with
     `| review-dimensional | <first clause of the description> | <n> origins | ratified | <today> |`;
     update the `## Count` section: ratified 1, in-progress 0, upstream origins ingested =
     `ls canonical/skills/review-dimensional/_source/ | wc -l`; bump `Last Updated`.
  3. Close the backlog item per Recon 5: if still in `backlog/`, `git mv` it to `backlog/done/`
     and append the `## Result` block per `docs/ingestion-workflow.md` Step 11 (ratified path,
     origins count, source list, one notable decision — use David's verdict). If already in
     `done/`, append the Result block only.
- **Expect:** `python3 -c "import json;print(json.load(open('canonical/skills/review-dimensional/provenance.json'))['rewrite_status'])"`
  → `ratified`; `grep -c review-dimensional canonical/INDEX.md` → ≥1;
  `ls backlog/done/2026-05-18-first-ingestion-code-review.md` → exists.
- **Failure signal:** you notice a SKILL.md defect after step 1's flip.
- **Counter-move:** if not yet committed (M7 hasn't run): revert the flip (set back to
  `in-style`), fix, re-flip — the flip isn't real until committed. If already committed:
  STOP — that's a version-bump situation (`docs/canonical-form-spec.md` §Versioning), out of
  this ticket's scope → record as a finding + follow-on note in the report, do not hot-fix.

### M6 — Correct david-style-patterns.md from real evidence (runs on ratify AND decline paths)

- **Do:** Append the corrections David saw in REVIEW.md §4 (adjusted for anything his verdict
  changed — a redirect's voice correction is itself prime evidence; a decline's reason doubly
  so) to `docs/david-style-patterns.md`: new rows in "Common rewrites" / "Stack-locked" tables
  where they fit, a new `## Evidence from ratified artifacts` section for anything table-shaped
  patterns don't cover. Each addition carries a one-line evidence pointer
  (`(evidence: review-dimensional T3-02 — <what happened>)`). Update the header: bump
  `Last Updated` to today and replace the `*(seed version — refine as canonical artifacts get
  ratified)*` note with `*(first evidence pass: review-dimensional, <today>)*`. Do NOT delete
  or rewrite existing seed content — append/extend only (the file is canon other agents read;
  removals need their own PO decision).
- **Expect:** `git diff --stat docs/david-style-patterns.md` → additions only (no deleted
  lines beyond the two header lines you replaced); ≥1 new evidence-tagged entry.
- **Failure signal:** you find you have zero evidence-backed corrections (nothing learned).
- **Counter-move:** do not invent one. Write the finding "first ingestion produced no
  style-pattern corrections — seed doc held" in REPORT.md, still bump the header note (that
  claim is itself the evidence pass), and say so explicitly in the report — David locked this
  ticket expecting corrections, so a null result must be loud, not silent.

### M7 — Report, results self-report, commit

- **Do:**
  1. Write `backlog/wargames/proof/T3-02/REPORT.md`: outcome (RATIFIED / RATIFIED-after-redirect /
     DECLINED), the decision JSON verbatim, checklist before/after table, style-patterns
     additions list, timings (parked at / decided at — from file mtimes), and a **Findings**
     section (spec gaps hit, T3-01 drift observed, anything the ingestion-workflow doc got
     wrong — this is a learning run by charter).
  2. Commit everything:
     `git add canonical/ docs/david-style-patterns.md backlog/done/ backlog/2026-05-18-first-ingestion-code-review.md backlog/wargames/proof/T3-02 engine/store/needs-decision engine/store/decisions && git commit -m "feat(canonical): first ratification gate — review-dimensional <outcome> (wg-t3-02)"`
     (decline path: the `canonical/` add picks up nothing — fine).
  3. LAST: write the results self-report
     `engine/store/results/wg-t3-02-ratify-first-ingestion.json` per the engine idiom:
     `{"ticket":"wg-t3-02-ratify-first-ingestion","status":"done","files_changed":[…],"commit_sha":"<sha>","notes":"<outcome one-liner>"}`.
- **Expect:** `git log --oneline -1` shows the commit; `git status` clean for the paths above;
  results file parses.
- **Failure signal:** commit rejected (pre-commit hook / concurrent dirty store).
- **Counter-move:** commit path-by-path; if `engine/store/` is dirty from a concurrent engine
  run, commit only your `wg-t3-02*` files and note the concurrency in the report. Results file
  is written regardless — the engine's reaper needs it.

## Forks

**F1 — Draft exists but is still in origin voice.**
Trigger: Recon 2 — `rewrite_status: "draft"` AND the SKILL.md body reads as upstream prose
(marketing adjectives, "This skill provides…", no Template-A/B/C shape).
→ **Route A** (only the status field is stale; body is genuinely David-voice): note it,
proceed — M4's provenance update fixes the field.
→ **Route B** (body genuinely un-rewritten): the Q9 session split drifted — writing the voice
draft is T3-01 scope, and silently doing it here would ratify a rewrite David never saw
staged. → Abort A1 with the specific observation ("T3-01 delivered harvest but no voice
draft").

**F2 — Gated vs ungated pause (how M3 resolves).**
Trigger: after the M3 park, does a resume message arrive?
→ **Route A** (this run was dispatched with `--hitl wg-t3-02-ratify-first-ingestion.json`; your
original task prompt told you to write needs-decision and reply `AWAITING_DECISION`): reply
exactly `AWAITING_DECISION`, wait; the orchestrator resumes you with David's decision inline
(≤30 min window) → continue M4 in-session.
→ **Route B** (ungated, or gated-but-unanswered): stop after the park — end your turn stating
you are parked awaiting `engine/store/decisions/wg-t3-02-ratify-first-ingestion.json`. Expected
engine noise, do not fight it: the reaper will time you out (WORKER_TIMEOUT 240s), re-queue up
to twice (each re-dispatch hits Recon 7's re-affirm branch), then mark the run
`failed(timeout)` with the ticket left in `running/` — the park file keeps the question alive
on the human queue. Completion happens on a post-decision re-dispatch via Recon 6 → M4.

**F3 — Redirect is structural, not voice.**
Trigger: M4 redirect whose `choice` changes mechanism/scope: different kept/set_aside, add or
drop an origin, rename away from `review-dimensional`, or touch `delivery-review`/existing
review-* skills.
→ **Route A** (small structural change fully specified by David AND satisfiable from material
already in `_source/` + provenance — e.g. "also keep the anti-rationalization table from the
osmani origin"): apply it, document in provenance `modified[]`/`kept[]`, re-run checklist → M5.
→ **Route B** (needs new harvesting, contradicts a locked Q9 default — rename, replace-not-
complement, touching delivery-review — or is ambiguous): → Abort A4 quoting his words; a
locked-decision reversal or new harvest is a new ticket, not an improvisation.

## Assumptions ledger

1. **T3-01's engine ticket id is `wg-t3-01-first-ingestion-review-dimensional`.** Authored in
   parallel — the id is inferred from the spec's naming rule + candidates.js, not read from its
   file. The real dependency gate is Recon 1's disk check, so a wrong guess cannot cause a
   false start; if the id differs, fix `depends_on` at promotion time (Phase 5 drain order —
   the engine itself ignores `depends_on`, verified in `dispatchable()` 2026-07-06).
2. **T3-01 leaves `rewrite_status: "in-style"` with a David-voice SKILL.md** (Q9 locked split;
   note the OLD 05-18 backlog "execution hint" put SKILL-writing in session 2 — decisions.md
   supersedes it). If false → Fork F1 / Abort A1; never silently absorb T3-01's scope.
3. **David answers via the decisions-file idiom.** He may instead hand-edit SKILL.md between
   runs. If a decision-present re-entry finds SKILL.md changed since the park
   (`git log --oneline -- canonical/skills/review-dimensional/SKILL.md` shows a commit after
   the pack was built, or the working tree is dirty there), treat David's edits as part of the
   redirect: keep them verbatim, record them in provenance `modified[]` as "David's direct
   edit", and do not re-style his words. If SKILL.md changed but NO decision file exists →
   stay parked (edits alone are not a ratification verdict).
4. **The style-patterns correction needs no separate PO gate** — the doc's own "To be
   expanded" section instructs appending, and David pre-reads the proposed corrections in
   REVIEW.md §4 as part of the same decision. If David's `note` objects to any correction,
   drop that one and record it.
5. **HITL-gated dispatch is possible but not guaranteed for this ticket** (the Phase 5
   promotion script did not exist at authoring; whether it passes `--hitl` is unknown). The
   war game is written to converge either way (F2); if execution day reveals a third dispatch
   mechanism entirely, park via A3 rather than adapt on the fly.

## Abort conditions

Park action for ALL aborts: write ATOMICALLY (temp + `mv`)
`engine/store/needs-decision/wg-t3-02-ratify-first-ingestion.json` containing
`{"ticket":"wg-t3-02-ratify-first-ingestion","question":"<one-line question>","note":"<observation, with paths>"}` —
unless the abort happens AFTER the M3 park, in which case OVERWRITE the existing park file so
the human queue carries the newer, sharper question. Leave the ticket in `running/`; stop.
Never guess past an abort.

- **A1 — Dependency incomplete or canon missing.** T3-01 artifacts absent/unreviewable
  (Recon 1–3, F1 Route B), or the voice-anchor skills folder is gone (M2). Question: "T3-02
  can't review: <what's missing>. Re-run/finish T3-01, or re-scope?"
- **A2 — HALT present, or BACKOFF recurs.** Question: "Factory halted/usage-limited
  (<payload>). Resume T3-02 when clear?"
- **A3 — Decision channel corrupt or unrecognizable.** Decision file exists but won't parse
  (Recon 6), or the dispatch mechanism doesn't match anything this war game knows (ledger 5).
  Question: "Your decision file for wg-t3-02 is unreadable / dispatch shape unknown: <detail>.
  Re-write the decision?" (Never default-approve a ratification.)
- **A4 — Redirect exceeds voice-review scope, or fix-iterate loop exhausted** (F3 Route B; M4
  third redirect round). Quote David's exact words. Question: "Your correction requires
  <structural change / spec amendment / locked-default reversal>. New ticket, or revise the
  correction?"
- **A5 — Artifact already ratified at entry** (Recon 2). In-place re-edit of a ratified
  canonical is forbidden; a re-run after successful completion is a no-op, and anything else
  is a version-bump question. Question: "review-dimensional is already ratified. Is wg-t3-02
  already complete (check backlog/wargames/proof/T3-02/REPORT.md), or do you want a v2?"

## Verification

From repo root. RATIFIED path (approve or voice-redirect):

```bash
python3 -c "import json;d=json.load(open('canonical/skills/review-dimensional/provenance.json'));print(d['rewrite_status'],d['version'])"   # → ratified 1
python3 - <<'EOF'                                                     # provenance self-consistency
import json,os
d=json.load(open('canonical/skills/review-dimensional/provenance.json'))
src='canonical/skills/review-dimensional/_source'
assert d['origins'], 'no origins'
for o in d['origins']:
    assert o['kept'], f"empty kept: {o['source_repo']}"
    assert os.path.exists(os.path.join('canonical/skills/review-dimensional',o['verbatim_copy'])), o['verbatim_copy']
print('PASS-provenance')
EOF
grep -c 'review-dimensional' canonical/INDEX.md                       # → ≥1 (registry row)
grep -c 'Total artifacts ratified: 1' canonical/INDEX.md              # → 1
test -f backlog/done/2026-05-18-first-ingestion-code-review.md && grep -c '## Result' backlog/done/2026-05-18-first-ingestion-code-review.md   # → ≥1
grep -c 'evidence: review-dimensional' docs/david-style-patterns.md   # → ≥1
grep -c 'seed version' docs/david-style-patterns.md                   # → 0 (header note replaced)
test -f backlog/wargames/proof/T3-02/REVIEW.md  && echo PASS-pack
test -f backlog/wargames/proof/T3-02/REPORT.md  && echo PASS-report
test -f engine/store/decisions/wg-t3-02-ratify-first-ingestion.json && echo PASS-decision   # David really decided
test -f engine/store/results/wg-t3-02-ratify-first-ingestion.json   && echo PASS-results
git log --oneline -5 | grep 'wg-t3-02'                                # → the commit
```

Negative (must NOT be true, any path):

```bash
git -C ~/dev/ad/appydave-plugins status --short -- appydave/skills/delivery-review appydave/skills/review-blind-hunter appydave/skills/review-edge-case-hunter appydave/skills/review-code-quality | grep . && echo FAIL-touched-existing-skills   # locked: complement, don't replace
git status --short research/ | grep . && echo FAIL-touched-research   # frozen corpus
grep -c 'This skill' canonical/skills/review-dimensional/SKILL.md | grep -qx 0 && echo NEG-voice   # no assistant-voice tell
```

DECLINED path replaces the ratified block with: `rewrite_status` unchanged from entry;
`canonical/INDEX.md` still shows `Total artifacts ratified: 0`; backlog item still in
`backlog/` with a `## Status` quoting the decline; REPORT.md outcome = DECLINED;
style-patterns evidence check still ≥1 (or the loud null-result finding per M6);
decision/results/commit checks unchanged.

## Executor notes (sonnet)

- **Scope fence:** write only under `canonical/skills/review-dimensional/`,
  `canonical/INDEX.md`, `docs/david-style-patterns.md`, the 2026-05-18 backlog item,
  `backlog/wargames/proof/T3-02/`, and your own `engine/store/` files. NEVER touch
  `research/`, `engine/*.py`, anything in `~/dev/ad/appydave-plugins/` (voice anchors are
  READ-ONLY), or other queue tickets.
- **The pause is the product.** Ratification without a real decision file from David is the
  one unforgivable failure mode of this ticket. No decision → parked is a SUCCESSFUL state
  for a single run. Never write `engine/store/decisions/…` yourself; never infer approval
  from silence.
- **Order discipline in M5:** all edits BEFORE the ratified flip; the flip before INDEX.md;
  results self-report LAST (it releases the gate/reaper).
- **Atomic writes** (temp + `mv`) for every `engine/store/needs-decision/` file — a torn read
  parses as corrupt and, in the orchestrator's own decision handling, corrupt defaults to
  approve.
- **Prefer HITL over guessing:** any conflict between David's words and the specs, any
  ambiguity about what T3-01 delivered → park with a sharp question. A parked question costs
  hours; a bad first ratification poisons the canon's founding precedent.
- **The rabbit hole:** improving the SKILL.md beyond David's verdict. After a redirect you
  will see three more things you'd polish. Don't — apply exactly the correction given, note
  the rest in REPORT.md Findings as candidates for a future version bump.
