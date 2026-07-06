# T8-01 — Truth-reconciliation pass over strategy docs

| field | value |
|---|---|
| ticket | wg-t8-01-doc-truth-reconciliation |
| track / size / priority | T8 Doc truth / S / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Four strategy docs carry status lines frozen at 2026-06-01→07-04 asserting things unbuilt that
have since shipped into `engine/` (2026-07-04→06): `docs/north-star.md` says C2 is "next" and the
trigger is "unsolved"; `docs/runtime-model.md` points operators at the retired
`experiments/watchtower-engine/` queue; `docs/harness-evaluation.md` says "evaluation only, no
code changed" when its promotion plan Phases 1–3 are now built; `docs/six-app-evaluation-2026-07-04.md`
lists as missing several things that landed within 48 hours (engine `status.py`, generalized
VERIFIERS, omi-fetch search, kdd-viewer `query.py`). The engine's own as-built record
(`engine/docs/ENGINE-NOTES.md`) also lags one beat — its auto-wake row says "Not built" but
`engine/wake.py` shipped. Fix by **additive, dated, evidence-cited reconciliation blocks** — never
rewriting or deleting the original analysis (the docs are point-in-time records; the repo's own
idiom is north-star's inline "> **Correction (2026-06-05):**" blockquote). Done looks like: all
five docs carry a 2026-07-06 reconciliation block that distinguishes SHIPPED / PARTIAL / STILL
OPEN with disk evidence for every claim, open items point at their war-game tickets, a proof
report exists at `backlog/wargames/proof/T8-01/REPORT.md`, and everything is committed and pushed.
This is instance one of the docs-lag-code fix — the class is named in
`plans/wargames/unknowns-map.md` §E.

## Locked context

- **Q4 (decisions.md):** everything through the engine — this war game is written for sonnet
  Swagger dispatch.
- **Docs lag code (wargame-spec):** this ticket IS that rule applied to the docs themselves.
  Your Recon re-verifies every claim below at execution time; the authoring-time evidence is a
  map, not the territory.
- **Assessment-mode default (CLAUDE.md):** never auto-rewrite ratified artifacts. These are
  `docs/` strategy files, not `canonical/` artifacts, but honour the spirit — additive dated
  addenda, original text preserved verbatim.
- **Q9 defaults:** the CLAUDE.md stale phase-b pointer fix and the Penny/Alex/Oscar retirement
  from architecture.md are SEPARATE T8 seeds — explicitly out of scope here.
- **No YLO/POEM work; no `-p`/headless/SDK ever; interactive `claude` only** — moot here (this
  ticket edits markdown and spawns nothing).

## Recon (verify before any work)

Repo root: `/Users/davidcruwys/dev/ad/apps/dark-factory`. All paths below are relative to it
unless absolute.

1. Clean seam on the target files:
   `git status --porcelain -- docs/north-star.md docs/runtime-model.md docs/harness-evaluation.md docs/six-app-evaluation-2026-07-04.md engine/docs/ENGINE-NOTES.md`
   → expect empty. Any of the five dirty → someone is mid-change on your exact seam → **Abort A2**.
2. Already-reconciled check (race with another session):
   `grep -l "2026-07-0[5-9]" docs/north-star.md docs/runtime-model.md docs/harness-evaluation.md engine/docs/ENGINE-NOTES.md`
   → expect no hits (authoring-time: none of the four carries any July date;
   six-app-evaluation-2026-07-04.md legitimately contains "2026-07-04" — that is its subject
   date, not a reconciliation). Hits → **Fork F1** per doc.
3. Engine shipped surface (the evidence the addenda will cite — capture each output):
   - `grep -n "^CAP\|BACKOFF_COOLDOWN\|USAGE_LIMIT_SIGNATURES" engine/orchestrator.py` → expect
     `CAP = 3` (~line 63), `BACKOFF_COOLDOWN = 900` (~line 71), signatures tuple (~line 73).
   - `grep -n "external-research" engine/orchestrator.py` → expect the kind-filter skip
     (~line 195).
   - `grep -n "^VERIFIERS" -A 4 engine/orchestrator.py` → expect 3 entries:
     `constellation-4-apps`, `generic`, `artifacts` (~line 470).
   - `grep -n "needs-decision" engine/orchestrator.py` → expect the HITL gate dirs wired
     (~lines 29, 57).
   - `grep -n "ANTHROPIC_API_KEY" engine/warm_pool.py` → expect the abort-if-set guard
     (~lines 56–57).
   - `ls engine/status.py engine/wake.py engine/consumer.py engine/halt.py bin/factory-wake bin/factory-halt engine/launchd/com.appydave.dark-factory-wake.plist`
     → all exist.
   - `ls engine/store/WAKE-ARMED 2>&1` → expect "No such file" (auto-wake ships DISARMED —
     the addenda must say "built, disarmed", never "live").
   Any single item missing → **Fork F2**. `engine/orchestrator.py` or `engine/store/` missing
   entirely → **Abort A1**.
4. Six-app-eval follow-up state (per-app deltas — capture each):
   - `grep -n "\-\-search\|\-\-since\|\-\-signal" /Users/davidcruwys/dev/ad/apps/omi-fetch/lookup.py | head -3`
     → expect hits (search SHIPPED).
   - `grep -in "claude-cli\|sole real engine" /Users/davidcruwys/dev/ad/apps/omi-fetch/lib/enrich.py | head -3`
     → expect hits (Gemini replaced by a claude-CLI engine).
   - `ls /Users/davidcruwys/dev/ad/apps/kdd-viewer/query.py` → exists (SHIPPED).
   - `grep -n "\-\-list" /Users/davidcruwys/dev/ad/apps/project-digest/digest.py` → expect NO
     hits (STILL OPEN), and `ls engine/store/queue/ | grep project-digest` → expect the deferred
     ticket `20260704T0630Z-project-digest-list-and-project-2.json` still queued (if it has moved
     to `done/`, check whether `--list` now exists and write the delta accordingly).
   - `ls engine/find.py 2>&1` → expect "No such file" (STILL OPEN).
   - `grep -n "apps/omi-fetch" /Users/davidcruwys/dev/ad/appydave-plugins/appydave/skills/omi-fetch/SKILL.md | head -2`
     → expect the "Related app" pointer lines (collision-pointer fix SHIPPED). Read-only check —
     never edit appydave-plugins.
5. Anchor lines exist exactly (each is an edit target in Moves 2–5):
   - `grep -n '\*\*Status\*\*: evaluation only. No code changed.' docs/harness-evaluation.md` → 1 hit.
   - `grep -n '\*\*Status\*\*: 2026-06-02' docs/runtime-model.md` → 1 hit (~line 3).
   - `grep -n 'Correction (2026-06-05)' docs/north-star.md` → 1 hit (~line 72).
   - `grep -n '^## 1. omi-fetch (v2)' docs/six-app-evaluation-2026-07-04.md` → 1 hit (~line 39).
   - `grep -n 'Not built — out of scope for this session' engine/docs/ENGINE-NOTES.md` → 1 hit
     (~line 20), and `grep -n '^- No auto-wake' engine/docs/ENGINE-NOTES.md` → 1 hit (~line 56).
   Any anchor missing → **Fork F2** (the doc changed since authoring; find the equivalent anchor
   or route B).
6. Cross-reference targets exist:
   `ls backlog/wargames/T1-01-hitl-live-proof.md backlog/wargames/T1-02-cap-backoff-real-429.md backlog/wargames/T1-03-auto-wake-arm.md backlog/wargames/T1-11-switchboard-state-fork-decision.md backlog/wargames/T2-03-digest-list-project-2.md`
   → expect all five (verified at authoring). Missing → reference the open work by description
   instead of ticket ID; do not invent paths.
7. Baseline line counts (for the never-delete verification):
   `wc -l docs/north-star.md docs/runtime-model.md docs/harness-evaluation.md docs/six-app-evaluation-2026-07-04.md engine/docs/ENGINE-NOTES.md`
   → authoring baseline: 84 / 85 / 116 / 231 / 88. Record the actual numbers; every file must
   only GROW.

## Moves

1. **Do:** Build the evidence table first. `mkdir -p backlog/wargames/proof/T8-01` and write
   `backlog/wargames/proof/T8-01/EVIDENCE.md`: one row per claim you are about to reconcile —
   columns: doc + stale claim (quoted verbatim) · disk evidence (the Recon 3/4 command + its
   captured output) · verdict (SHIPPED / PARTIAL / STILL OPEN) · pointer (war-game ticket ID from
   Recon 6, or "—"). Minimum rows: north-star C2/C3 status; runtime-model queue path;
   harness-eval "no code changed" + Phases 1/2/3 items (blackboard MCP user-level registration —
   check `python3 -c "import json; print('blackboard' in json.dumps(json.load(open('/Users/davidcruwys/.claude.json')).get('mcpServers',{})))"`
   → authoring: True; API-key guard; warm pool; CAP; HITL) + Phase 4 open; six-app-eval's
   engine/omi-fetch/kdd-viewer/project-digest/KBDE items; ENGINE-NOTES auto-wake row.
   **Expect:** EVIDENCE.md exists, every row's evidence cell carries a real command output, no
   row says "probably".
   **Failure signal:** a row where you cannot produce disk evidence either way.
   **Counter-move:** mark that row "UNVERIFIABLE" and exclude the claim from all addenda (an
   addendum may only state what EVIDENCE.md proves). If more than 3 rows are unverifiable →
   **Abort A1** (the map is too wrong to reconcile from).

2. **Do:** Reconcile `docs/north-star.md` (additive only). (a) Directly below the existing
   `> **Correction (2026-06-05):** ...` blockquote (Recon 5 anchor, ~line 72), insert a new
   blockquote: `> **Correction (2026-07-06, truth-reconciliation wg-t8-01):**` stating — C2
   proven 2026-06-06 (commit `3d817a1` "C2 proven — talk->ticket->done across two sessions");
   the trigger/dispatch spine has since shipped as `engine/` (orchestrator.py warm-pool dispatch
   with CAP=3 + BACKOFF governor, HITL gate wired-but-unexercised → live proof is T1-01, CAP/429
   real-fire proof is T1-02); auto-wake watcher built as `engine/wake.py` + launchd plist +
   `bin/factory-wake`, ships DISARMED → arming is T1-03; the runtime home moved from
   `experiments/watchtower-engine/` to `engine/` (the old tree still exists as history); the
   "Scale (N>1…) is deferred" line below is partially superseded — the CAP=3 governor and warm
   pool shipped, N>1 remains unproven. (b) In the frontier table (~lines 66–70), append to the
   Producer row's status cell: ` — **✅ C2 proven 2026-06-06**, see 2026-07-06 correction below`
   and to the Trigger row's cell: ` — **🔨 substantially built 2026-07-04→06 (engine/), disarmed**,
   see 2026-07-06 correction below`. (c) In the build-spine list (~lines 78–82), append to item 2:
   `**✅ DONE 2026-06-06** (commit 3d817a1)` and to item 3: `**🔨 built 2026-07-04→06 as engine/
   (dispatch leg disarmed — T1-03)**` — mirroring item 1's existing DONE annotation style.
   (d) Update the header Status line (~line 3) to: `**Status**: 2026-06-01 — the orienting frame;
   read before anything else. Status lines reconciled 2026-07-06 (wg-t8-01) — see the dated
   corrections inline.` Do not touch any other line.
   **Expect:** `grep -c "Correction (2026-07-06" docs/north-star.md` → 1;
   `grep -c "Correction (2026-06-05)" docs/north-star.md` → still 1; file grew vs Recon 7 baseline.
   **Failure signal:** original correction gone, file shrank, or the diff touches lines outside
   (a)–(d).
   **Counter-move:** `git checkout -- docs/north-star.md` and re-apply once, more surgically.
   Second failure → **Abort A3**.

3. **Do:** Reconcile `docs/runtime-model.md` (additive only). (a) Directly below the Status line
   (Recon 5 anchor, ~line 3), insert a blockquote:
   `> **Status update (2026-07-06, wg-t8-01):** the three-layer model below (Marshall / Swagger /
   workflows) remains the concept of record. The OPERATIONAL mechanics in "Launch modes" are
   superseded: the runtime is now `engine/` — tickets go in `engine/store/queue/` (idiom:
   `engine/store/queue/.CONVENTION.md`), dispatch is `python3 engine/orchestrator.py` (warm-pool
   tmux workers, interactive claude only, ANTHROPIC_API_KEY guard enforced in
   `engine/warm_pool.py`), the trigger leg is `engine/wake.py` via launchd (DISARMED until
   `engine/store/WAKE-ARMED` exists — `bin/factory-wake arm`). Mode A's
   `experiments/watchtower-engine/` queue path below is the retired pre-engine era, kept as
   history. The C3d kill-on-done open item is superseded: the orchestrator reaps on
   artifact-landed (`results/<ticket>.json`), per `engine/docs/ENGINE-NOTES.md`.`
   (b) Update the Status line itself to append: ` **Reconciled 2026-07-06 — see status update
   below; "Launch modes" §§ are historical.`** Nothing else changes — the Mode A/B sections stay
   verbatim.
   **Expect:** `grep -c "Status update (2026-07-06" docs/runtime-model.md` → 1;
   `grep -c "experiments/watchtower-engine" docs/runtime-model.md` unchanged from before (the old
   paths are preserved, now framed as history); file grew.
   **Failure signal:** Mode A/B text altered or removed.
   **Counter-move:** `git checkout -- docs/runtime-model.md`, re-apply once. Second failure →
   **Abort A3**.

4. **Do:** Reconcile `docs/harness-evaluation.md` + its companion `engine/docs/ENGINE-NOTES.md`.
   (a) In harness-evaluation.md, extend the Status line (Recon 5 anchor) preserving the original
   sentence verbatim: `**Status**: evaluation only. No code changed. **Update 2026-07-06
   (wg-t8-01):** the promotion plan below has since been EXECUTED — Phases 1–3 shipped into
   `engine/` 2026-07-04→06 (warm pool = `engine/warm_pool.py` with the API-key guard; CAP=3 +
   BACKOFF 429 governor, kind-filter, generalized VERIFIERS, HITL gate = `engine/orchestrator.py`;
   audit trail = `engine/store/audit.jsonl`; blackboard MCP registered user-level in
   `~/.claude.json`). As-built record: `engine/docs/ENGINE-NOTES.md`. Still open: Phase 4 / DF-7
   state plane (fork decision → war game T1-11); the HITL gate is wired but unexercised live
   (→ T1-01); the CAP/BACKOFF governor has never met a real 429 (→ T1-02); the one-ticket
   warm-pool+HITL proof run has not happened. Auto-wake shipped after ENGINE-NOTES was written:
   `engine/wake.py` + launchd + `bin/factory-wake`, DISARMED (→ T1-03).`
   (b) In ENGINE-NOTES.md, append to the auto-wake table row's third cell (Recon 5 anchor,
   ~line 20): ` **Update 2026-07-06 (wg-t8-01): now built** — `engine/wake.py` + `engine/launchd/
   com.appydave.dark-factory-wake.plist` + `bin/factory-wake {arm|disarm|status}`; notify-always,
   dispatch only when `engine/store/WAKE-ARMED` exists; ships DISARMED.` And append to the
   `- No auto-wake — ...` limitation line (~line 56): ` **[superseded 2026-07-06 — see the
   auto-wake row above: built, disarmed.]**`
   **Expect:** `grep -c "evaluation only. No code changed." docs/harness-evaluation.md` → still 1
   (original preserved inside the extended line); `grep -c "Update 2026-07-06"
   docs/harness-evaluation.md` → 1; `grep -c "wg-t8-01" engine/docs/ENGINE-NOTES.md` → 2.
   **Failure signal:** original status sentence lost, or ENGINE-NOTES table markdown broken
   (row no longer renders — check the `|` count on the edited line matches its neighbours).
   **Counter-move:** `git checkout -- docs/harness-evaluation.md engine/docs/ENGINE-NOTES.md`,
   re-apply once. Second failure → **Abort A3**.

5. **Do:** Reconcile `docs/six-app-evaluation-2026-07-04.md`. Insert a new section immediately
   BEFORE the `## 1. omi-fetch (v2)` heading (Recon 5 anchor): `## Since shipped — status
   reconciliation (2026-07-06, wg-t8-01)` with 2–3 framing lines ("the verdict table above is the
   2026-07-04 snapshot, preserved as-is; this section records what changed in the following
   48 hours, disk-verified") and a per-app delta table with columns App · 2026-07-04 finding ·
   2026-07-06 state · evidence — rows sourced ONLY from EVIDENCE.md (Move 1): engine `status.py`
   SHIPPED; VERIFIERS generalized to 3 entries (`generic` declarative DSL + `artifacts` fallback)
   SHIPPED; `engine/find.py` STILL OPEN; omi-fetch `lookup.py --search/--since/--until/--signal`
   SHIPPED; omi-fetch enrichment engine swapped Gemini→claude-CLI SHIPPED (note: uses a `claude -p`
   subprocess — flag as an observation for David, do not act); omi-fetch skill name-collision
   pointer landed in the old SKILL.md SHIPPED; kdd-viewer `query.py` SHIPPED; project-digest
   `--list` + project #2 STILL OPEN (ticket queued → T2-03); KBDE extension still
   validated-unmounted (external D2, unchanged). Do NOT edit the verdict table or any per-app
   section — they are the point-in-time record.
   **Expect:** `grep -c "Since shipped" docs/six-app-evaluation-2026-07-04.md` → 1; the original
   verdict table rows still grep intact (e.g. `grep -c "omi-fetch (v2) | 2/5"` unchanged); file
   grew.
   **Failure signal:** any pre-existing line changed or removed.
   **Counter-move:** `git checkout -- docs/six-app-evaluation-2026-07-04.md`, re-apply once.
   Second failure → **Abort A3**.

6. **Do:** Verify, report, ship. Run the full Verification block below and capture outputs. Write
   `backlog/wargames/proof/T8-01/REPORT.md`: before/after of each status line (quoted), the
   EVIDENCE.md table (inline or by reference), any F1/F2 routes taken, the `claude -p` enrichment
   observation, and a one-line note that this is docs-lag-code instance one (class tracked in
   unknowns-map §E). Then commit and push from the repo root:
   `git add docs/north-star.md docs/runtime-model.md docs/harness-evaluation.md docs/six-app-evaluation-2026-07-04.md engine/docs/ENGINE-NOTES.md backlog/wargames/proof/T8-01 && git commit -m "docs: truth-reconciliation pass — status lines match shipped engine/ reality (wg-t8-01)" && git push`.
   **Expect:** every verification check passes; commit contains exactly the five docs + proof
   dir; push succeeds.
   **Failure signal:** a verification check fails, unrelated files in the commit, or push
   rejected.
   **Counter-move:** verification fail → fix the specific doc (one attempt) and re-verify. Push
   rejected → `git pull --rebase` then push; a conflict in a file you touched → resolve keeping
   both intents; in a file you did NOT touch → **Abort A3**. Second failure of anything →
   **Abort A3**.

## Forks

**F1 — a target doc is already reconciled (race with another session).**
Trigger: Recon 2 finds a July-2026 dated update/correction block already present in a target doc.
→ **Route A** (the existing block covers the same claims and agrees with your EVIDENCE.md):
skip that doc's move entirely; record "already reconciled by <its stated author/date>" in
REPORT.md.
→ **Route B** (partial coverage, or it asserts something your evidence contradicts): append only
the missing deltas under your own dated block — never duplicate, never edit the other session's
block. If it CONTRADICTS your disk evidence (says shipped, disk says absent), write only what the
disk proves and name the contradiction in REPORT.md.

**F2 — disk evidence contradicts the authoring-time map.**
Trigger: a Recon 3/4 item is missing (e.g. `engine/wake.py` gone, VERIFIERS back to 1 entry) or a
Recon 5 anchor line no longer exists.
→ **Route A** (isolated — one or two items, or an anchor moved but the doc is recognizably the
same): write the addendum from what IS on disk (EVIDENCE.md rules), find the equivalent anchor by
section heading, and log the divergence in REPORT.md.
→ **Route B** (systemic — `engine/` restructured, a target doc gone or unrecognizable): →
**Abort A1**.

## Assumptions ledger

1. **Additive dated addenda are the right reconciliation style** (vs rewriting the docs).
   Plausible: it is the repo's own idiom (north-star's existing Correction blockquote,
   assessment-mode default), and it preserves point-in-time records that other docs cite. **If
   false** (David wants full rewrites at triage): the addenda are a strict prerequisite for a
   rewrite anyway — nothing is lost; a rewrite becomes a follow-on ticket.
2. **The cross-referenced war-game tickets (T1-01, T1-02, T1-03, T1-11, T2-03) remain the
   canonical pointers for the still-open items.** Plausible: authored in the same portfolio,
   verified on disk at authoring. **If false** (files absent at Recon 6, or already executed):
   reference the open work by description, or — if a pointed-at proof already landed (e.g. T1-01
   done and HITL now exercised) — upgrade that claim from STILL OPEN to SHIPPED with the proof
   path as evidence.
3. **ENGINE-NOTES.md is in scope as harness-evaluation's companion status record.** Plausible:
   harness-evaluation's new status line delegates to it as "the as-built record", so leaving its
   stale auto-wake row would re-create the exact problem one hop away. **If false** (David rules
   it out of scope at triage): it is one revertible hunk in one commit — revert just that file.
4. **The `claude -p` usage inside omi-fetch's enrichment engine is out of scope.** The no-`-p`
   law was written for engine dispatch (metered billing); whether it binds an enrichment
   subprocess is David's call. This ticket reports the observation in REPORT.md and the
   six-app-eval delta table, and acts on nothing. **If false** (it is a violation): that is a new
   ticket, not an edit here.

## Abort conditions

- **A1 — the map is too wrong to reconcile from.** More than 3 EVIDENCE.md rows unverifiable,
  `engine/` fundamentally restructured, or a target doc missing/unrecognizable (F2 Route B).
  Park: write `engine/store/needs-decision/wg-t8-01-doc-truth-reconciliation.json` with
  `{"ticket": "wg-t8-01-doc-truth-reconciliation", "question": "authoring-time evidence map diverges from disk beyond safe reconciliation: <the specific divergences>. Re-author the war game against current reality, or proceed doc-by-doc?", "observed": "<the failing Recon commands + outputs verbatim>"}`.
  Leave the ticket in `running/`. Touch no docs in this state.
- **A2 — mid-change seam.** Any of the five target files dirty at Recon 1. Park with the same
  JSON shape, question: "target docs are mid-edit by another session — reconcile after it lands,
  or now?", `observed` = the `git status --porcelain` output. Never edit a dirty doc.
- **A3 — an edit will not land cleanly.** Any move's counter-move failed a second time, an
  unrelated-file conflict on push, or a broken doc you cannot restore. Restore every target file
  (`git checkout -- <files>`), confirm `git status --porcelain` is clean on them, then park with
  the intended addendum text pasted into the question so the decision is "how to land it", not
  "what to write".

## Verification

```bash
DF=/Users/davidcruwys/dev/ad/apps/dark-factory
cd $DF

# 1. every doc carries the dated reconciliation, exactly once
grep -c "Correction (2026-07-06" docs/north-star.md                          # → 1
grep -c "Status update (2026-07-06" docs/runtime-model.md                    # → 1
grep -c "Update 2026-07-06" docs/harness-evaluation.md                       # → 1
grep -c "Since shipped" docs/six-app-evaluation-2026-07-04.md                # → 1
grep -c "wg-t8-01" engine/docs/ENGINE-NOTES.md                               # → 2 (table row + limitation line)

# 2. originals preserved verbatim (the never-delete rule)
grep -c "evaluation only. No code changed." docs/harness-evaluation.md       # → 1
grep -c "Correction (2026-06-05)" docs/north-star.md                         # → 1
grep -c "Mode A — Manual worker" docs/runtime-model.md                       # → 1
grep -c "| omi-fetch (v2) | 2/5" docs/six-app-evaluation-2026-07-04.md       # → 1 (verdict table untouched)
# every file only grew (authoring baselines: 84 / 85 / 116 / 231 / 88):
wc -l docs/north-star.md docs/runtime-model.md docs/harness-evaluation.md docs/six-app-evaluation-2026-07-04.md engine/docs/ENGINE-NOTES.md

# 3. claims cite tickets for open work
grep -c "T1-01" docs/harness-evaluation.md                                   # → ≥1
grep -c "T1-03" docs/north-star.md                                           # → ≥1
grep -c "T2-03" docs/six-app-evaluation-2026-07-04.md                        # → ≥1

# 4. proof + commit shipped
ls backlog/wargames/proof/T8-01/EVIDENCE.md backlog/wargames/proof/T8-01/REPORT.md   # both exist
git log --oneline -1 | grep -c "wg-t8-01"                                    # → 1 (and pushed: git status -sb shows no ahead)

# 5. negative checks — nothing beyond the ask
git log -1 --stat | grep -cE "engine/(orchestrator|warm_pool|wake|status|consumer|halt)\.py"  # → 0 (no code touched)
git status --porcelain -- research/ canonical/ | wc -l                       # → 0
git log -1 --stat | grep -c "CLAUDE.md\|architecture.md"                     # → 0 (phase-b pointer + Penny/Alex/Oscar are other tickets)
git -C /Users/davidcruwys/dev/ad/appydave-plugins status --porcelain | wc -l # → 0 (read-only over there)
```

## Executor notes (sonnet)

- **Scope fence.** Edit ONLY the five named files + the proof dir. Do NOT touch engine code, do
  NOT fix CLAUDE.md's phase-b pointer, do NOT retire Penny/Alex/Oscar from architecture.md, do
  NOT update suborch-conformance.md / eval-architecture.md / comms-flow.md even where they also
  lag (they are other T8 seeds — list any staleness you notice in REPORT.md as findings instead),
  do NOT edit anything in appydave-plugins or the sibling apps (omi-fetch, kdd-viewer,
  project-digest — you only READ them for evidence), do NOT delete or rewrite a single
  pre-existing line in any target doc.
- **The rabbit hole: "while I'm here" doc improvement.** You will notice the four docs could be
  restructured, deduplicated, or beautifully rewritten. Skip it entirely — this ticket's value is
  a surgical, evidence-cited truth layer with a diff David can review in two minutes. A 400-line
  rewrite diff destroys that. Addenda only.
- **Every claim needs a citation.** An addendum sentence that names no file, command, ticket ID,
  or commit is a defect — EVIDENCE.md is the source; if it's not there, it doesn't go in a doc.
- **Wording discipline:** "built, disarmed" for auto-wake; "wired, unexercised" for HITL; "never
  met a real 429" for the governor. Do not write "working" or "proven" for anything that lacks a
  proof artifact on disk.
- **Prefer parking over guessing** whenever disk evidence and a doc's claim can't be reconciled
  into a single true sentence — a parked ticket with the contradiction quoted beats a confident
  addendum that starts docs-lag-code instance two.
