# T5-07 — Reconcile the two decision-queue concepts

| field | value |
|---|---|
| ticket | wg-t5-07-decision-queue-reconcile |
| track / size / priority | T5 Watchtower / S / high |
| executor | sonnet Swagger via engine |
| depends_on | none (should land BEFORE T5-01/T5-05/T5-06 build any UI — they consume this note) |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Two mechanically unrelated systems share the name "decision queue": (A) the engine's **mid-task
HITL gate** — a running worker blocks on `engine/store/needs-decision/<tid>.json`, David answers
via `decisions/<tid>.json`, the orchestrator resumes the live worker (SHIPPED in
`engine/orchestrator.py`, wired but not yet exercised live — that proof is T1-01's job, not
this ticket's); and (B) Watchtower's **curation queue** — at-rest promote/reject decisions over
artifacts, writing promotion records, never mutating `canonical/` (DESIGN-ONLY: `docs/watchtower/`
plan + spec + a 1-commit RVETS stub at `apps/watchtower`). `docs/comms-flow.md` line 155 names
this collision as gap #1; `docs/harness-evaluation.md` row 5 already ruled "confirmed different
mechanisms, both needed, neither replaces the other." This ticket produces ONE design note,
`docs/decision-queues.md`, that locks the vocabulary and the naming rules the T5 UI builds must
follow, pins three cross-links so the lock is discoverable at every point of confusion, and
fixes the stub README's ambiguous tagline. Done looks like: the note exists with every pinned
section filled from disk evidence, the three pins are in, and NOT ONE line of engine `.py` or
watchtower client/server code changed. This is a vocabulary artifact, not a build and not a
merge of the two systems.

## Locked context

- **Q6 (decisions.md):** Watchtower = real web app (kanban, live agent view, bus view, curation
  queue). That app is exactly what will bake in the confusion if this note doesn't land first.
- **Q4 (decisions.md):** everything through the engine — this ticket runs as a sonnet Swagger
  dispatch and self-reports to `engine/store/results/`.
- **Harness-evaluation row 5 verdict (2026-06, David-accepted):** the two mechanisms are
  orthogonal; promote the HITL gate, leave the curation queue untouched. This note RATIFIES and
  extends that ruling into names — it has no authority to reverse it or to merge the systems.
- **Assessment-mode default (CLAUDE.md):** the note is a draft until David ratifies at triage;
  drafts can iterate, so naming objections are a cheap rename, not a blocker.
- **No `-p`/headless/SDK ever; interactive `claude` only** — binds how this ticket runs.
- **Ticket-first (`engine/store/queue/.CONVENTION.md`):** queue/running/done movement +
  `results/<ticket>.json` is the audit trail.

## Recon (verify before any work)

Repo root `/Users/davidcruwys/dev/ad/apps/dark-factory`; the stub is a SEPARATE git repo at
`/Users/davidcruwys/dev/ad/apps/watchtower`. All verified 2026-07-06 at authoring; re-verify
everything — docs lag code in this repo.

1. `ls engine/store/` → expect `needs-decision/` and `decisions/` present (both EMPTY at
   authoring — the gate is wired, never fired outside `--test`). Missing dirs → **Abort A1**.
2. `grep -n "NEEDS, DEC\|HITL_TIMEOUT\|--hitl" engine/orchestrator.py | head` → expect the
   dir pair (≈line 57), `HITL_TIMEOUT = 1800` (≈line 70), the `--hitl <tid>` gate flag
   (≈line 526). Then `sed -n '242,275p' engine/orchestrator.py` → the gated `task_prompt`
   (needs-decision request shape `{"ticket","question","proposed","note"}` +
   `AWAITING_DECISION` token) and `resume_prompt` (decision shape `{"action","choice","note"}`,
   decline → `ABORTED`). If the gate is gone or reshaped → **Abort A1**.
3. `grep -ni "decision\|hitl" engine/status.py` → authoring: **0 hits** — the engine's own
   status surface is blind to a blocked HITL ticket. A finding for the note (§9 follow-ons),
   not something to fix here. If hits appear, someone wired it — read and record instead.
4. `grep -n "decision.queue\|Decision Queue" docs/watchtower/plan.md | head` and
   `grep -n "Accept.*Rerun.*Promote.*Kill\|discard/rerun/improve/promote" docs/watchtower/plan.md docs/watchtower/spec.md`
   → expect plan.md to define the Decision Queue as "the only landing surface" (≈line 17) with
   decision verb `PATCH /api/promotions/:id` = discard/rerun/improve/promote (≈line 131), and
   spec.md AC-1 to use Accept/Rerun/Promote/Kill (≈line 97). The VERB DRIFT between the two is
   itself evidence for the note. If both files are gone → **Abort A1**.
5. `git -C ../watchtower log --oneline` → authoring: exactly one commit `1f4d5e9` ("Initial
   commit: Watchtower — human control surface over Dark Factory workflows").
   `sed -n '3p' ../watchtower/README.md` → the ambiguous tagline "…— a decision queue".
   `grep -rli "decision\|curation" ../watchtower/client ../watchtower/server ../watchtower/shared`
   → authoring: nothing (no code carries the confusion yet). More commits or code hits →
   **Fork F1**.
6. Prior-reconciliation check: `ls docs/decision-queues.md 2>&1` (expect missing) and
   `grep -rn "vocabulary" docs/watchtower/DECISIONS.md docs/comms-flow.md | head` and check
   for T5-01 charter output: `ls backlog/wargames/T5-01* 2>/dev/null; ls docs/watchtower/charter* ../watchtower/docs/ 2>/dev/null`.
   A charter or vocabulary doc that already names both mechanisms → **Fork F2**. A David
   ruling that MERGES the two mechanisms → **Abort A2**.
7. The split's prior art must still exist (it's what the note ratifies):
   `grep -n "CURATION queue\|MID-TASK HITL" docs/comms-flow.md` (≈lines 83, 88; finding #1
   ≈line 155) and `grep -n "curation queue" docs/harness-evaluation.md` (row 5 ≈line 52,
   ≈lines 67, 98). Gone/rewritten → read what replaced them; if the replacement already locks
   vocabulary → **Fork F2**.
8. `ls docs/INDEX.md && ls backlog/wargames/T1-01-hitl-live-proof.md` → both exist at
   authoring (INDEX gets a pin; T1-01 owns the HITL live proof this note must cite, not
   duplicate). T1-01 missing → drop that citation, keep the note self-contained.

## Moves

### Move 1 — Term-usage sweep (where the collision actually lives)

- **Do:** Build the evidence table (scratchpad notes for Move 3):
  `grep -rn -i "decision queue\|decision-queue\|curation" docs/ engine/README.md backlog/concepts.md --include="*.md" | grep -v "backlog/wargames" | head -40`
  plus the stub's surfaces from Recon 5. For each hit record: file+line · which mechanism it
  means (HITL / curation / the aggregate surface / ambiguous) · stale or current. Include the
  four known anchors: `docs/comms-flow.md` (§7c diagram + line 40 "decision-queue surface" +
  line 155 finding), `docs/harness-evaluation.md` (row 5, lines 67/96–98),
  `docs/constellation-map.md` line 71 ("HOTL decision queue"), `docs/daily-operating-model.md`
  line 78 (NEEDS-YOU aggregates `needs-decision/*.json` + `waiting:david` tickets + open doc
  decisions — the aggregate-surface reading).
- **Expect:** a table of ~10–20 rows; at least one hit classified under each of the three
  meanings; the ambiguous rows concentrated on "decision queue" used bare.
- **Failure signal:** the sweep finds a THIRD mechanism (not HITL, not curation, not an
  aggregate view) using the same name.
- **Counter-move:** add it to the table and give it its own row in the note's vocabulary table
  with a grounded name; if it is a live David-facing system this war game never anticipated
  (not just a doc phrase) → Abort A2 (the reconciliation is bigger than a vocabulary note).

### Move 2 — Pin both mechanisms' ground truth (code for A, design for B)

- **Do:** From Recon 2–5, write the two-column mechanism inventory: **HITL gate** — owner:
  engine; state: SHIPPED, unexercised live (cite `backlog/wargames/T1-01-hitl-live-proof.md`
  as the proof owner); trigger: gated ticket mid-run; blocking: yes (worker idles at REPL,
  `HITL_TIMEOUT` 1800s → `failed(no-decision)`); store: `engine/store/needs-decision/` →
  `engine/store/decisions/`; request/decision JSON shapes verbatim from `task_prompt`/
  `resume_prompt`; verbs: approve / decline / redirect (redirect = approve + `choice` field);
  alert: `notify()` on lock. **Curation queue** — owner: Watchtower; state: DESIGN-ONLY
  (plan + spec + 1-commit stub, zero decision code); trigger: artifact at rest (completed
  run/experiment or canonical candidate); blocking: no (nothing waits); store: promotion
  records (`data/promotions/<id>.yml` per plan.md ≈lines 79/295), NEVER mutates `canonical/`;
  verbs: promote-family, with the plan-vs-spec drift recorded verbatim (discard/rerun/improve/
  promote vs Accept/Rerun/Promote/Kill) and explicitly DEFERRED to T5-05 — this note does not
  pick the verb set.
- **Expect:** every cell in the inventory carries a file+line (or file+section) you re-verified
  this session; no cell sourced from memory or from a strategy doc's status claim.
- **Failure signal:** a cell you can only fill from a doc whose claim you could not confirm on
  disk (e.g. comms-flow's "lives only in the POC", which authoring PROVED stale — the gate is
  in `engine/`).
- **Counter-move:** verify on disk or mark the cell "unverified — check before relying"; stale
  doc claims go in the note's docs-lag ledger (§8), never in the inventory.

### Move 3 — Write `docs/decision-queues.md` (the vocabulary lock)

- **Do:** Author the note with EXACTLY this section skeleton, filled from Moves 1–2:
  1. **The name collision** — one paragraph; cite comms-flow line 155 (gap #1) and
     harness-evaluation row 5 (the "both needed, neither replaces" verdict this note ratifies).
  2. **Vocabulary lock** — three terms, one line each, binding on all future T5/T1 work:
     **HITL gate** = the engine's mid-task blocking mechanism (never call it a queue, never
     "curation"); **curation queue** = Watchtower's at-rest artifact-promotion mechanism
     (never "HITL", nothing blocks on it); **decision queue** (alias **Needs-You**) = a
     SURFACE ONLY — the aggregate "what needs me" view (Watchtower Today / briefing NEEDS-YOU
     per daily-operating-model line 78) that renders cards FROM both mechanisms plus
     `waiting:david` tickets, and owns NO state of its own. Bare "decision queue" may never
     again name a mechanism.
  3. **Mechanism A — HITL gate** — the Move 2 inventory column, JSON shapes verbatim.
  4. **Mechanism B — curation queue** — the Move 2 inventory column, verb-drift table, and
     the never-mutates-`canonical/` rule restated.
  5. **The surface** — what the decision-queue VIEW aggregates and the rule that it reads
     both stores and writes to whichever mechanism a card belongs to (a curation card patches
     a promotion record; a HITL card writes `decisions/<tid>.json`) — it never merges the
     stores and never invents a third store.
  6. **Naming rules for builds** (binding on T5-01/T5-02/T5-05/T5-06/T5-12): every card,
     route, type, and lane carries its mechanism — e.g. `/api/hitl/*` vs `/api/curation/*`,
     a `mechanism: "hitl" | "curation"` discriminator on any unified card type, verb sets
     never cross-pollinate (approve/decline/redirect stay HITL-only; promote-family stays
     curation-only).
  7. **What NOT to build** — no unification of the two mechanisms, no shared store, no
     auto-promotion (spec.md line ≈137), no curation writes into `canonical/`.
  8. **Docs-lag ledger** — every stale claim Move 1 caught, at minimum: comms-flow §7c "not
     yet in dark-factory's real Swaggers / lives only in the POC" (stale — gate shipped into
     `engine/` 2026-07-04); harness-evaluation Phase-3 "port … into watchtower-engine's idiom"
     (done since); the stub README tagline. Fix NONE of them here except the two pins in
     Move 4 and the tagline in Move 5 — name the rest for T8's truth reconciliation.
  9. **Follow-ons** (one-liners, not tickets): `status.py` is blind to blocked HITL tickets
     (Recon 3); T5-05 owns the curation verb-set decision; T5-06 builds the HITL inbox against
     THIS vocabulary; T1-01 owns the live-fire proof.
- **Expect:** the note exists; `grep -c "^## " docs/decision-queues.md` ≥ 9; every factual
  claim carries its evidence (file+line or command).
- **Failure signal:** a section you cannot fill from Moves 1–2 evidence.
- **Counter-move:** one bounded grep/read to close the gap, or write the gap in explicitly as
  "unverified"; never pad from a strategy doc's status line.

### Move 4 — Cross-link pins in dark-factory (three edits, one line each)

- **Do:** (a) `docs/INDEX.md`: one line in its design/decision region — doc name, "locks the
  HITL-gate vs curation-queue vocabulary; 'decision queue' = surface only", date. (b)
  `docs/comms-flow.md`: at the END of §7c, directly after the paragraph that ends "…named
  (`app-pipeline/watchtower.md`, 2026-07-02 addendum) and built nowhere." (≈line 95), insert:
  `> Vocabulary locked 2026-07-06+:
  see docs/decision-queues.md — "HITL gate" (mid-task, engine) vs "curation queue" (at-rest,
  Watchtower); "decision queue" now names only the aggregate surface.` (c)
  `docs/watchtower/plan.md`: the same one-line banner immediately under the title. No other
  dark-factory edits.
- **Expect:** `grep -rn "decision-queues.md" docs/INDEX.md docs/comms-flow.md docs/watchtower/plan.md | wc -l` → 3.
- **Failure signal:** a target file's structure has changed so much there is no sane insertion
  point (e.g. comms-flow §7 renumbered).
- **Counter-move:** pin at the nearest section that discusses the two queues, or append a
  dated line at the file's end — a misplaced pin beats a missing one; note it in the results
  JSON.

### Move 5 — Fix the stub's tagline (fork-guarded, separate repo)

- **Do:** Only on Fork F1 Route A (stub still 1 commit, tree clean): edit
  `../watchtower/README.md` line 3 from `> Human control surface over Dark Factory workflows —
  a decision queue` to `> Human control surface over Dark Factory workflows — the decision-queue
  SURFACE: renders HITL-gate cards (engine, mid-task) and curation-queue cards (artifacts,
  at-rest) as one "what needs me" list. Vocabulary: dark-factory/docs/decision-queues.md.`
  Commit in THAT repo: `docs: disambiguate the decision-queue tagline (wg-t5-07)` with the
  standard Co-Authored-By trailer. Push only if a remote exists (`git -C ../watchtower remote -v`);
  authoring did not verify one — a local commit satisfies this move.
- **Expect:** `git -C ../watchtower log --oneline | head -2` shows the new commit above
  `1f4d5e9`; `git -C ../watchtower status --porcelain` clean.
- **Failure signal:** the edit rejected, the repo is dirty, or line 3 no longer matches.
- **Counter-move:** → Fork F1 Route B (do not force it; the handoff line in the note covers
  T5-01). Second failure of any kind here → skip the move entirely, record in results JSON —
  this pin is the cheapest and most expendable of the four.

### Move 6 — Self-report, commit, push

- **Do:** Write `engine/store/results/<this-ticket-filename>.json` in the form the
  orchestrator's task prompt demands, noting: fork routes taken, whether the stub tagline was
  fixed or deferred, and the docs-lag ledger's row count. Commit the dark-factory changes
  (new note + three pins + results) in one commit:
  `docs(watchtower): T5-07 decision-queue vocabulary locked — HITL gate vs curation queue (wg-t5-07)`
  with the standard Co-Authored-By trailer; push.
- **Expect:** `git log --oneline -1` shows the commit; `git status --porcelain` clean apart
  from pre-existing dirt.
- **Failure signal:** push rejected (non-fast-forward).
- **Counter-move:** `git pull --rebase` then push; on conflict in the pinned files re-apply
  your one-line pins on top (pure additions). Second failure → leave committed locally, note
  in results JSON.

## Forks

**F1 — The stub has moved.**
Trigger: Recon 5 finds >1 commit in `../watchtower`, a dirty tree, or decision/curation code
in client/server/shared.
→ **Route A (still the 1-commit clean stub):** Move 5 proceeds — the tagline edit is safe and
nothing else references it.
→ **Route B (grown or dirty):** do NOT touch the watchtower repo at all. Instead add to the
note's §9 a directive line: "apps/watchtower has advanced past the stub; its owner (T5-01)
must align README + any coined names with §2 before merging further UI work." If the grown
code already contains a name that CONTRADICTS the lock (e.g. a `decisionQueue` store holding
both kinds), record it in §8 and ALSO write needs-decision/ per Abort A2's shape — the
confusion this ticket exists to pre-empt has landed; David chooses rename-now vs rename-at-T5-01.

**F2 — Someone already reconciled the vocabulary.**
Trigger: Recon 6/7 finds an existing vocabulary doc, a T5-01 charter that names both
mechanisms, or a rewritten comms-flow §7 that locks terms.
→ **Route A (it agrees with harness-evaluation row 5 — two mechanisms, distinct names):** do
not write a competing doc. Reduce this ticket to: verify that artifact's claims against the
Move 2 ground truth, fix any stale cells it has, add whichever of the four pins are missing
so it is discoverable, and self-report "reconciliation pre-existed; pinned + verified".
→ **Route B (it MERGES the mechanisms or contradicts row 5):** → Abort A2 — a newer David
ruling may have superseded the verdict this war game ratifies; never overwrite a ruling with
a vocabulary note.

## Assumptions ledger

1. **The locked names — "HITL gate", "curation queue", "decision queue = surface only" — are
   acceptable to David.** Plausible: they are exactly the disambiguated terms comms-flow §7c
   and harness-evaluation row 5 already use; this note only promotes existing usage to law.
   If David objects at triage: assessment-mode makes it a rename inside one draft doc + four
   one-line pins — note it, don't park.
2. **The curation verb set stays OPEN.** The plan-vs-spec drift (discard/rerun/improve/promote
   vs Accept/Rerun/Promote/Kill) is recorded, not resolved — T5-05 owns it. If the executor
   finds a David ruling that already picked the verbs, record it in §4 as decided and cite it.
3. **`apps/watchtower` may have no git remote** (authoring verified only the single local
   commit). A local commit satisfies Move 5; if push fails or no remote exists, say so in the
   results JSON — do not create a remote.
4. **`brains/dark-factory/app-pipeline/watchtower.md` (outside this repo) adds an attention-
   alert requirement** ("charm/sound", cited by comms-flow line 95). Treated as read-only
   context; the note may cite it via comms-flow without opening the brain. If the executor
   cannot read it, nothing in this ticket depends on it.
5. **T5-01 has not yet coined vocabulary.** Authoring found no T5-01 war game or charter on
   disk. If it lands first, Fork F2 handles it. (Portfolio note: promoting T5-07 ahead of
   T5-01 in the drain order avoids the race entirely.)

## Abort conditions

**A1 — Ground truth has moved.** Recon 1/2 fails (HITL gate gone or reshaped in
`engine/orchestrator.py`, store dirs missing) or Recon 4 fails (Watchtower design docs gone).
The collision this note documents may no longer exist as framed. Park: write
`engine/store/needs-decision/wg-t5-07-decision-queue-reconcile.json` with
`{"ticket":"wg-t5-07-decision-queue-reconcile","question":"T5-07 (authored 2026-07-06) locks vocabulary for a HITL-gate/curation-queue split, but ground truth has moved: <what differs>. Re-author against current state?","proposed":"re-author","note":"<observed state>"}`.
Leave the ticket in `running/`. Never lock vocabulary onto systems that aren't there.

**A2 — The split is already resolved differently.** A David ruling (decisions/ artifact, doc,
or built code per F1-B/F2-B) merges the two mechanisms, coins conflicting vocabulary, or a
third same-named live mechanism surfaces (Move 1 counter-move). Park to needs-decision/ (same
shape; question: "T5-07 ratifies harness-evaluation row 5 (two mechanisms, distinct names),
but <evidence> points the other way. Which ruling governs?"). Do not arbitrate between rulings.

**A3 — Scope breach imminent.** You find yourself about to edit any `engine/*.py`, any file
under `../watchtower/client|server|shared`, anything in `canonical/`, or to build any UI "to
demonstrate the vocabulary". Stop, park to needs-decision/ describing what tempted you. This
ticket ships one note + four one-line pins, nothing else.

## Verification

Run from `/Users/davidcruwys/dev/ad/apps/dark-factory`:

```bash
test -f docs/decision-queues.md && echo OK                              # note exists
grep -c "^## " docs/decision-queues.md                                   # >= 9 sections
grep -n "HITL gate" docs/decision-queues.md | head -1                    # term locked
grep -n "curation queue" docs/decision-queues.md | head -1               # term locked
grep -ni "surface" docs/decision-queues.md | head -1                     # third meaning pinned
grep -n "Accept.*Rerun.*Promote.*Kill" docs/decision-queues.md           # verb drift recorded
grep -rn "decision-queues.md" docs/INDEX.md docs/comms-flow.md docs/watchtower/plan.md | wc -l   # 3 pins
ls engine/store/results/ | grep -c wg-t5-07                              # 1 — self-report exists
git log --oneline -3 | grep wg-t5-07                                     # commit landed
```

Stub pin (only if Fork F1 Route A ran):
```bash
git -C ../watchtower log --oneline | head -2                             # wg-t5-07 commit above 1f4d5e9
grep -n "decision-queues.md" ../watchtower/README.md                     # tagline points at the lock
```

Negative checks (vocabulary artifact, not a build):
```bash
git diff HEAD~1 --stat -- engine/ | grep "\.py"; echo "py-diff-exit:$?"  # exit 1 — no .py touched
git diff HEAD~1 --stat -- canonical/ | wc -l                             # 0 — canonical untouched
git -C ../watchtower status --porcelain                                  # empty (clean either way)
git -C ../watchtower diff 1f4d5e9 --stat -- client server shared | wc -l # 0 — no stub code touched
```
And: `engine/store/needs-decision/` contains a wg-t5-07 file ONLY if an abort or F1-B's
contradiction branch fired — otherwise it must not exist.

## Executor notes (sonnet)

- **Scope fence:** writes are exactly — `docs/decision-queues.md` (new), one line each in
  `docs/INDEX.md` + `docs/comms-flow.md` + `docs/watchtower/plan.md`, the fork-guarded
  README tagline in `../watchtower`, your results self-report, and (only per aborts/F1-B) one
  needs-decision file. Read anything; change nothing else. `engine/*.py` and all watchtower
  client/server/shared code are READ-ONLY for you.
- **You are naming, not building and not deciding.** The two-mechanisms verdict is
  harness-evaluation row 5's, already accepted; your note ratifies it into vocabulary. If your
  sweep convinces you the mechanisms SHOULD merge, that opinion goes nowhere — the note
  records pressure only if evidence (not taste) surfaced it, and A2 exists for real conflicts.
- **Evidence over eloquence.** Every claim carries the command or file+line that proved it —
  this note exists precisely because the surrounding docs contradict the code (comms-flow
  still says the gate "lives only in the POC"; it shipped). A stale claim in the vocabulary
  lock would poison every T5 build that trusts it.
- **Prefer HITL over guessing** whenever a newer ruling, charter, or built surface conflicts
  with the split (A2/F1-B/F2-B): a parked question costs minutes; two competing vocabularies
  cost every future session.
- **The rabbit hole:** "while I'm here" — resolving the curation verb drift, wiring
  `status.py` to show blocked HITL tickets, sketching the Today-screen card component, or
  fixing every stale line the sweep catalogues. All out of scope: the drift belongs to T5-05,
  the status gap and stale docs are §8/§9 ledger lines for T8 and T1. Ship the note, pin the
  links, stop.
