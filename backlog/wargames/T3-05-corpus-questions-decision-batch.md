# T3-05 — DECISION batch: the 14 corpus questions A–N

| field | value |
|---|---|
| ticket | wg-t3-05-corpus-questions-decision-batch |
| track / size / priority | T3 Ingestion / M / high |
| executor | sonnet Swagger via engine |
| depends_on | none (T3-06+ cluster-distillation tickets depend on THIS) |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

`research/INDEX.md` §"Open questions across repos" lists 14 corpus-modeling questions A–N
marked "require David's call before Phase 2" — yet Phase 2 ran, 1,150 artifacts landed, and
~30 distillations shipped on IMPLICIT defaults nobody wrote down. Per decisions.md, this
ticket turns that into a DECISION ARTIFACT, not a build: `docs/corpus-questions-a-n-decisions.md`,
one section per question, each with verified disk evidence, an honest status class (some are
already David-ruled in `research/schema-history.md`; one is resolved by recon; four are
genuinely open), a DEFAULT that all downstream distillation/ingestion tickets (T3-06…T3-23)
proceed under, and an executable ESCALATION TRIGGER that says when a default stops being safe
and David must rule. Done looks like: the doc exists with all 14 sections evidence-backed,
it's linked from `docs/INDEX.md`, a self-report sits in `engine/store/results/`, the commit is
pushed — and NOT ONE byte under `research/` changed. The defaults are PROVISIONAL until David
bulk-ratifies or line-item-overrides at triage; provisional defaults still govern downstream
tickets in the meantime (that is the unblock).

## Locked context

- **decisions.md assumptions ledger:** "The 14 corpus questions A–N: per Q2 campaign, handled
  as a decision-batch ticket (T3-05), each with a default + trigger, not pre-answered here."
  → the OUTPUT SHAPE is ruled: default + trigger per question. This ticket does not get to
  skip a question or merge questions.
- **Q2 (decisions.md):** ingestion = full campaign — this doc is the gate that lets cluster
  distillation run at scale without re-litigating scope per cluster.
- **Q4 (decisions.md):** everything through the engine — sonnet Swagger dispatch, self-report
  to `results/`.
- **Q5 (decisions.md):** YLO→POEM parked entirely — question E touches the POEM repo; the
  answer may REFERENCE POEM state but must not create POEM work.
- **CLAUDE.md hard rule:** `research/` is the frozen corpus, read-only from the executor's
  perspective. The questions live there; the ANSWERS live in `docs/`. No research/ edits,
  not even a pointer line (see Assumptions 2).
- **CLAUDE.md assessment-mode default:** never auto-rewrite a ratified artifact — if a
  ratified corpus-questions decision doc already exists, that's Abort A2, not an overwrite.
- **Ticket-first (`engine/store/queue/.CONVENTION.md`):** queue/running/done movement +
  `results/<ticket>.json` is the audit trail.
- **No `-p`/headless/SDK ever; interactive `claude` only** — binds how this ticket runs.

## Recon (verify before any work)

Repo root `/Users/davidcruwys/dev/ad/apps/dark-factory`. All values below verified 2026-07-06
at authoring; docs lag code (INDEX.md's own stats are stale against artifacts.jsonl) —
re-verify everything.

1. `grep -c "^| [A-N] |" research/INDEX.md` → expect **14** (the questions table, authoring:
   lines 123–136, under "### Open questions across repos"). 0 or a different count → the
   premise moved → **Abort A1**.
2. `ls docs/corpus-questions*.md 2>&1` → expect "no matches". If a file exists: read it — if
   it carries a ratified/David-approved marker → **Abort A2**; if it's an unratified draft,
   read it, fold anything correct into your doc, and note the supersession in the doc header
   and results JSON.
3. Prior-ruling sweep: `grep -rli "corpus question\|questions A-N\|A–N" engine/store/decisions/
   engine/store/done/ backlog/ docs/ 2>/dev/null | grep -v wargames` → authoring: only this
   war game's own portfolio files (plans/wargames/*). Any OTHER hit that contains a David
   ruling on a specific question → **Fork F1** for that question.
4. The ruling trail exists: `grep -n "Scope decisions (David, 2026-05-16)" research/schema-history.md`
   → expect 1 hit (in the 0.0.3 entry), whose two bullets rule "Primary artifacts only …
   Templates / hooks / rules / step files / MCP tools deferred to Phase 2.5" and "Source-only
   for compile-on-install repos". Also `grep -n "beta variant" research/schema-history.md` →
   expect a hit in 0.0.4 (`notes` field evidence). Missing → the RULED/RULED-DEFERRAL
   classifications lose their basis → those questions become OPEN (Move 3 counter).
5. Question-E evidence: `grep -n "Alec" research/recon/poem.md` → expect the "Role
   confirmation" line: David sometimes calls Alex "Alec"; the file is `alex.md`, title
   "Workflow Architect". Also expect poem.md's "Out-of-Scope Agents" section naming
   `oscar.md`, `victor.md`, `field-tester.md`. Missing → E stays OPEN, don't invent.
6. Live corpus numbers (authoring values — expect DRIFT, record what you see):
   `wc -l < research/artifacts.jsonl` → authoring **1150** (INDEX.md still says 1,100);
   `grep -c '"repo": "poem"' research/artifacts.jsonl` → **2**;
   `grep -c '"repo": "david-local"' research/artifacts.jsonl` → **30** (a 15th source absent
   from INDEX.md's repo tables entirely — stale-docs ledger material).
7. De-facto type answers: run the two probes in Move 2 step (c) — authoring found gbrain
   recipes cataloged as `artifact_type:"skill"` and the osmani personas as
   `artifact_type:"agent"`. If either probe returns empty, the I/J de-facto claims are
   unfounded → classify OPEN instead.
8. Plumbing: `ls engine/store/needs-decision/ engine/store/results/ docs/INDEX.md` → all
   exist (empty dirs are fine). Missing store dirs → **Abort A1** (engine layout drifted;
   this ticket's park/report mechanics would be fiction).

## Moves

### Move 1 — Pin the questions and the ruling trail

- **Do:** Copy the 14 question rows verbatim from `research/INDEX.md` (the table Recon 1
  found) into scratchpad notes — letter, question text, "affects" column. Then extract, with
  line numbers, the governing rulings: schema-history.md 0.0.3's two "Scope decisions
  (David, 2026-05-16)" bullets, 0.0.3's facet decision, 0.0.4's `body_path`/`notes` additions
  (incl. the "beta variant" usage note), and schema-current.md's "Phase 2 scope (decided
  2026-05-16)" block. These are the citations every RULED/RULED-DEFERRAL section will carry.
- **Expect:** 14 verbatim questions + ≥4 dated ruling citations with file+line.
- **Failure signal:** a question's text in INDEX.md differs materially from the paraphrase in
  the classification table (Move 4) — e.g. a question was edited since authoring.
- **Counter-move:** the INDEX.md text WINS (it's the source); reconcile the classification
  against the current wording. If a question vanished or a letter was reused for a different
  question → **Abort A1**.

### Move 2 — Verify the de-facto corpus state (the grep battery)

- **Do:** Run each probe from repo root and record actual values (authoring values in
  brackets — drift in NUMBERS is expected and fine; drift in DIRECTION routes to Fork F2):
  (a) per-repo counts: `grep -o '"repo": "[a-z-]*"' research/artifacts.jsonl | sort | uniq -c | sort -rn`
      [ECC 365 · ruflo 219 · appydave-plugins 124 · compound-engineering 86 · gsd 81 ·
      gbrain 51 · gstack 49 · bmad 44 · osmani 33 · david-local 30 · spec-kit 23 ·
      matt-pocock 18 · superpowers 14 · compound-knowledge 11 · poem 2];
  (b) type split: `grep -o '"artifact_type": "[a-z]*"' research/artifacts.jsonl | sort | uniq -c`
      [741 skill / 224 command / 185 agent — and NO other type values: confirms no
      recipe/persona/rule/mcp-tool type ever got minted];
  (c) I/J probes:
      `grep '"repo": "gbrain"' research/artifacts.jsonl | grep -i recipe | head -3` → rows
      with `"artifact_type": "skill"` [e.g. gbrain:skill:data-research];
      `grep '"repo": "agent-skills-osmani"' research/artifacts.jsonl | grep -i persona | head -3`
      → rows with `"artifact_type": "agent"` [e.g. agent-skills-osmani:agent:code-reviewer];
  (d) L probe: `grep '"repo": "ruflo"' research/artifacts.jsonl | grep -ci mcp` [8 — i.e.
      the 305 MCP tools are NOT rows; only incidental mentions];
  (e) A/C probe: gstack rows [49] = its `.tmpl` source count per INDEX.md's repo table
      ("compiled `.md` outputs excluded") — confirms source-only held in practice;
  (f) K probe: `grep -c '"version"' research/artifacts.jsonl` [135 — version strings exist
      only inside `frontmatter_yaml`; `discovered_by_version` is the schema version, not the
      artifact's]. Confirm no top-level `version` field in `research/schema-current.md`.
- **Expect:** every probe's DIRECTION matches the bracketed authoring value (numbers may
  drift).
- **Failure signal:** a direction flip — e.g. MCP-tool rows exist, a `persona` artifact_type
  value appears, poem ≠ 2 rows, compiled outputs cataloged as rows.
- **Counter-move:** → **Fork F2** for each flipped question; carry on verifying the rest
  first (one flip must not stall the other 13).

### Move 3 — Classify all 14 (the status table)

- **Do:** Assign each question exactly one status class, reconciling the authored
  classification below against Moves 1–2 evidence and any Fork F1 rulings:
  - **RULED** (David ruled it explicitly): **A**.
  - **RULED-DEFERRAL** (David deferred the artifact class to "Phase 2.5" — the default
    codifies exclusion-until-go, it does NOT schedule Phase 2.5): **B, D, F, L**.
  - **DE-FACTO** (discover practice settled it; the default codifies observed practice):
    **C, G, I, J**.
  - **RESOLVED-BY-RECON** (the question's premise was answered by recon evidence): **E**.
  - **OPEN** (no ruling, no settled practice — Fable-proposed default, David-unratified):
    **H, K, M, N**.
  Downgrade rules: a RULED/RULED-DEFERRAL question whose ruling citation failed Recon 4 →
  OPEN. A DE-FACTO question whose Move 2 probe failed → OPEN. An OPEN question for which
  Fork F1 found a David ruling → RULED. Never upgrade without a citation.
- **Expect:** a 14-row table, every row citing its evidence (file+line or probe result).
- **Failure signal:** a row you cannot place without guessing.
- **Counter-move:** place it as OPEN with the proposed default marked "weakly grounded" —
  honesty over tidiness; if MORE THAN FOUR rows end up downgraded from the authored classes,
  the authoring premise is broken → **Abort A1**.

### Move 4 — Write `docs/corpus-questions-a-n-decisions.md`

- **Do:** Author the doc with EXACTLY this skeleton — `# ` title, a `> STATUS` banner
  ("PROVISIONAL — these defaults govern distillation/ingestion tickets now; David
  bulk-ratifies or line-item-overrides at triage. Evidence verified <execution date>."),
  then sections `## How to read this`, `## Status legend`, one `## Q-<letter> — <short
  name>` per question A–N **in letter order**, `## Ratification`, `## Stale-docs ledger
  (for T8)`. Every Q section carries exactly these six bolded fields:
  **Question** (verbatim from INDEX.md) / **Evidence (verified <date>)** / **Status** /
  **Default** / **Escalation trigger** / **Effect on distillation**.
  Fill the sections from this authored content, corrected by Moves 1–3 (evidence lines must
  show YOUR verified values, not these authoring-time ones):

  | Q | Status | Default | Escalation trigger |
  |---|--------|---------|--------------------|
  | A source-vs-compiled | RULED (0.0.3: "Source-only for compile-on-install repos … compiled outputs are build artifacts") | Track canonical source only; `file_path` = source; compiled outputs never get rows | A compiled output's body materially diverges from its source (hand-edited post-compile) — that's a new artifact, not a render; escalate before adding a row |
  | B sub-artifact granularity | RULED-DEFERRAL (0.0.3: step files deferred to Phase 2.5; bmad = 44 rows, not 44+78) | Sub-files are parent-skill metadata, not rows — but distillation/eval MUST read them as part of the parent's body when scoring (read-the-whole-tree, catalog-one-row) | A distillation names a sub-file that stands alone (usable without its parent) as a winner candidate — escalate before minting a row or ingesting it solo |
  | C multi-harness variants | DE-FACTO (consequence of A; spec-kit = 23 not ×30; osmani Gemini variants excluded; gsd split handled by `body_path`) | One row per canonical source; harness coverage in `notes` where relevant | Hand-maintained divergent variants (sibling bodies with different content, not renders) — escalate for a variant-of convention before adding rows |
  | D adapter-vs-canonical | RULED-DEFERRAL (0.0.3 deferral covers plugin bundles; ruflo = 219 without its 104 bundled; ECC's 33 `.agents/skills/` adapters excluded per source-only) | Adapters/bundles are packaging, not artifacts — no rows; counts stay in recon reports | An adapter carries unique behavior absent from its canonical (not format translation) — treat as B's stand-alone case, escalate |
  | E POEM "Alec" missing | RESOLVED-BY-RECON (recon/poem.md: Alec = Alex, `alex.md`, title "Workflow Architect"; poem = 2 rows, correct) | E is answered — nothing missing; out-of-scope POEM agents (oscar/victor/field-tester) stay out; felix/field-tester duplication is POEM-repo hygiene, not a catalog question | David expands POEM scope, or POEM gains new agent files (YLO→POEM is PARKED per Q5 — reference only, create no POEM work) — re-recon poem first |
  | F ECC rules, no frontmatter | RULED-DEFERRAL (0.0.3: rules deferred; ECC = 365 rows, rules excluded) | Rules = always-on context, not rows; distillers MAY mine rule bodies as pattern evidence in a draft's notes | A cluster distillation finds ≥3 winner mechanisms living ONLY in rules — escalate scheduling Phase 2.5 rules intake |
  | G beta-vs-stable | DE-FACTO (0.0.4 `notes` field, used as `"beta variant"` for exactly ce-work-beta/ce-polish-beta) | Betas are ordinary rows, same artifact_type, `notes:"beta variant"`; distillation prefers the stable sibling and treats the beta as variant evidence | A beta outperforms or supersedes its stable sibling in an eval — escalate which to ingest, never both silently |
  | H cross-repo dependency edges | OPEN (no edge field/registry anywhere; DF-8 registry is spec-only) | No edge schema now; record encountered edges as dated lines in the distillation draft's notes; rule of three — the third draft that independently needs edge data escalates building `edges.jsonl` | Rule-of-three fires, or the DF-8 comparison-registry build (T3-18) starts — edges belong in that design |
  | I recipes as type | DE-FACTO (gbrain's 8 recipes ARE rows, `artifact_type:"skill"`) | Recipes stay skill rows; recipe fields (secrets, health_checks, setup_time) live in `frontmatter_yaml`, not schema | An ingestion wants a canonical RECIPE (setup-shaped, secrets-bearing) that canonical-form-spec.md can't express — escalate a recipe canonical form, not a catalog type |
  | J personas as type | DE-FACTO (osmani's 3 personas ARE rows, `artifact_type:"agent"`) | Personas = agent rows; optional `notes:"persona"` where the distinction matters | Persona-vs-agent semantics distort an eval rubric (identity overlay scored as executable agent) — escalate a facet, not a type |
  | K versioning | OPEN (no top-level field; version strings survive inside `frontmatter_yaml`, ~135 rows; `discovered_by_version` is the schema's version, not the artifact's) | No top-level field; freshness is a corpus-snapshot property (`discovered_at`), not hand-maintained per-artifact metadata | Upstream-pulse (T3-25) arms and challenger detection needs version diffing — add the field in THAT schema bump, with migration note |
  | L Ruflo's 305 MCP tools | RULED-DEFERRAL (0.0.3 names MCP tools explicitly; ruflo = 219 rows, the 305 live only in recon/ruflo.md) | OUT of corpus — coordination API surface, not prompt-bearing artifacts; the catalog's unit is the prompt-bearing file; Phase 2.5 reconsideration needs its own David go | An orchestration-cluster ingestion needs MCP-tool design patterns as mechanism prior art — mine recon/ruflo.md narratively, zero rows; escalate only if rows become load-bearing |
  | M AgentShield npm package | OPEN (not in corpus; compiled TS distribution, not a prompt artifact) | OUT; cite as external prior art where security-review distillation wants it | David expands scope to packages, or a security-review ingestion can't cite-without-cataloging its mechanism |
  | N out-of-scope-but-related | OPEN (appydave `.skill` zips + archived consultants plugin never cataloged) | OUT; zips are packaging duplicates of unpacked trees; consultants plugin stays uncatalogued until David asks; a zip-only skill with no unpacked sibling enters via a normal discover pass, never ad hoc | David asks to mine the consultants plugin, or a zip-only skill is found |

  The `## Ratification` section: a 14-row checklist (letter · status · default one-liner ·
  "☐ ratify / ☐ override") plus the sentence "Unratified defaults still govern downstream
  tickets; an override propagates by editing the affected section and date-stamping it —
  never by deleting history." The `## Stale-docs ledger (for T8)` section records at
  minimum: research/INDEX.md still says the questions "require David's call before Phase 2"
  (left intact — research/ is read-only) and points nowhere; INDEX.md's corpus stats say
  1,100/13-repos while artifacts.jsonl holds <your verified count> including `david-local`
  (30) and `matt-pocock-skills` (18) absent from its repo tables; plus anything your recon
  found. Fix NONE of them.
- **Expect:** `grep -c "^## Q-" docs/corpus-questions-a-n-decisions.md` → 14;
  `grep -c '\*\*Default' docs/corpus-questions-a-n-decisions.md` → ≥14;
  `grep -c '\*\*Escalation trigger' docs/corpus-questions-a-n-decisions.md` → ≥14.
- **Failure signal:** a section whose Evidence field you cannot fill from a probe/citation
  you actually ran (writing "per INDEX.md" is the failure — INDEX.md is the QUESTION source,
  not evidence).
- **Counter-move:** run the missing probe (one bounded grep/read). If the evidence simply
  doesn't exist, the status is OPEN and the Evidence field says "unverifiable: <what you
  tried>" — never pad.

### Move 5 — Cross-link from docs/INDEX.md

- **Do:** Add ONE line to `docs/INDEX.md` in its decisions/specs region (near the T1-11
  state-authority-fork line if present): the doc name, one sentence ("the 14 corpus-modeling
  questions A–N: status + default + escalation trigger each; provisional until David
  ratifies at triage"), and date. No other edits to INDEX.md.
- **Expect:** `grep -c "corpus-questions-a-n-decisions" docs/INDEX.md` → 1.
- **Failure signal:** INDEX.md's structure offers no sane insertion point.
- **Counter-move:** append under the last section with a dated line — a misplaced index line
  beats a skipped one; note it in the results JSON.

### Move 6 — Negative sweep (prove you stayed inside the fence)

- **Do:** Run `git status --porcelain research/` (expect empty) and
  `git status --porcelain | grep -v "docs/corpus-questions\|docs/INDEX.md\|engine/store"`
  (expect empty apart from pre-existing dirt you can name). Confirm `research/artifacts.jsonl`,
  `research/schema-current.md`, `research/schema-history.md`, and `research/INDEX.md` are
  all byte-identical to HEAD.
- **Expect:** both checks clean.
- **Failure signal:** anything under `research/` shows modified.
- **Counter-move:** `git checkout -- research/` immediately, then re-verify the doc's
  affected Evidence fields against the restored files. If you cannot explain how the edit
  happened → **Abort A3** (something in your process writes where it must not).

### Move 7 — Self-report, commit, push

- **Do:** Write `engine/store/results/<this-ticket-filename>.json` in the form the
  orchestrator's task prompt demands, including: the 14-letter status summary (e.g.
  "A:RULED B:RULED-DEFERRAL … N:OPEN"), which forks fired (F1/F2 letters), and drift
  observed vs authoring values. Commit the new doc + INDEX line + results in one commit:
  `docs(ingestion): T3-05 corpus questions A-N — status, defaults, triggers (wg-t3-05)`
  with the standard Co-Authored-By trailer; push.
- **Expect:** `git log --oneline -1` shows the commit; push succeeds.
- **Failure signal:** push rejected (non-fast-forward).
- **Counter-move:** `git pull --rebase` then push; on conflict in docs/INDEX.md re-apply
  your one line on top (pure addition). Second failure → leave committed locally, note in
  results JSON.

## Forks

**F1 — A newer David ruling exists for some question.**
Trigger: Recon 3 (or anything read en route) surfaces a David ruling on a specific question
postdating 2026-07-06 — in `engine/store/decisions/`, a backlog item, or a docs note.
→ **Route A (ruling agrees with the authored default):** status becomes RULED, cite the
ruling, keep the default text.
→ **Route B (ruling contradicts the authored default):** the ruling WINS — rewrite that
section's Default to the ruling, status RULED, and note the supersession ("authored default
was X; David ruled Y on <date>"). A David ruling is the answer, never a conflict to park.

**F2 — Disk evidence flips an authored default's premise.**
Trigger: a Move 2 probe shows a DIRECTION flip (not mere count drift): MCP-tool rows exist
in artifacts.jsonl, a new artifact_type value (persona/recipe/rule) was minted, poem ≠ 2
rows, or compiled outputs appear as rows.
→ **Route A (numbers drifted, direction holds):** update the Evidence field with your
values, keep the default. Count drift is expected (the corpus grew from 1,100 to 1,150
between INDEX.md and authoring alone).
→ **Route B (direction flipped):** the affected question's section gets status
**OPEN-ESCALATED** with both the authored premise and the observed state; finish the doc
(the other 13 sections must not stall); then write ONE
`engine/store/needs-decision/wg-t3-05-corpus-questions-decision-batch.json`:
`{"ticket":"wg-t3-05-corpus-questions-decision-batch","question":"Corpus evidence contradicts the authored default(s) for question(s) <letters>: <one line each — premise vs observed>. Rule now or accept the observed practice as the default?","proposed":"accept observed practice as the de-facto default","note":"full evidence in docs/corpus-questions-a-n-decisions.md §Q-<letter>"}`
and leave the ticket in `running/` per the HITL idiom.

## Assumptions ledger

1. **The OPEN-class defaults (H, K, M, N) are Fable-proposed and David-unratified.**
   Plausible: each codifies an existing exclusion (nothing was ever cataloged for H/K/M/N)
   and David bulk-accepts well-grounded defaults (decisions.md Q9). If David overrides at
   triage → line-item edit of the affected section, date-stamped, per the doc's own
   Ratification rules; downstream tickets re-read the doc, no rework of this ticket.
2. **`research/` stays read-only, so research/INDEX.md will STILL say the questions "require
   David's call" after this ticket ships.** Deliberate: CLAUDE.md's hard rule beats
   discoverability. The gap is logged in the doc's Stale-docs ledger for T8's
   truth-reconciliation. If David authorizes a one-line pointer under the questions table,
   it's a trivial follow-up — do not do it inside this ticket.
3. **Phase 2.5 remains unscheduled.** The RULED-DEFERRAL defaults (B, D, F, L) codify
   exclusion-until-go; they do NOT schedule Phase 2.5. If a Phase 2.5 plan exists on disk at
   execution time → cite it and defer to its scope, noting it in each affected section.
4. **Corpus counts will have drifted again by execution.** Authoring saw 1,150 rows incl.
   `david-local` (30) and `matt-pocock-skills` (18) that INDEX.md's tables don't know about.
   Drift alone is Fork F2 Route A. If the corpus SHRANK, someone rewrote history in an
   append-preferred file — note it in the Stale-docs ledger and proceed; it changes no
   default.
5. **The distillation consumers (T3-06+) will cite this doc by path.** Plausible: this war
   game fixes the path `docs/corpus-questions-a-n-decisions.md`. If David renames it at
   triage, it's a `git mv` + one INDEX line fix — note, don't block.

## Abort conditions

**A1 — The questions premise is gone.** Recon 1 fails (table missing/renumbered), a letter
was reused for a different question, Recon 8 finds the engine store layout drifted, or Move 3
downgrades more than four authored classifications. Park: write
`engine/store/needs-decision/wg-t3-05-corpus-questions-decision-batch.json` with
`{"ticket":"wg-t3-05-corpus-questions-decision-batch","question":"T3-05 (authored 2026-07-06) answers the 14 corpus questions A-N in research/INDEX.md, but the premise no longer holds: <what differs>. Re-author against current state?","proposed":"re-author","note":"<observed state>"}`.
Leave the ticket in `running/`. Never write a decision doc against questions that no longer
exist as authored.

**A2 — A ratified corpus-questions decision artifact already exists.** Recon 2 finds a doc
carrying a ratified/David-approved marker (or Recon 3 finds a David ruling covering the
batch). Assessment-mode default: ratified artifacts get a new version by David's say-so,
never an in-place rewrite by an executor. Park to needs-decision/ (same shape, question:
"A ratified corpus-questions decision doc already exists at <path>. Should T3-05 become a
verify-and-extend ticket against it?").

**A3 — Scope breach imminent.** You find yourself about to edit ANYTHING under `research/`
(INDEX.md, artifacts.jsonl, schema files, recon reports), any vocabulary file under the
dark-factory-catalog skill in appydave-plugins, or any engine `.py` — including "just fixing
the stale stats while I'm here". Stop, park to needs-decision/ describing what tempted you.
This ticket ships one doc + one index line, nothing else.

## Verification

Run from `/Users/davidcruwys/dev/ad/apps/dark-factory`:

```bash
test -f docs/corpus-questions-a-n-decisions.md && echo OK          # doc exists
grep -c "^## Q-" docs/corpus-questions-a-n-decisions.md            # exactly 14
grep -c '\*\*Default' docs/corpus-questions-a-n-decisions.md       # >= 14
grep -c '\*\*Escalation trigger' docs/corpus-questions-a-n-decisions.md  # >= 14
grep -c '\*\*Evidence' docs/corpus-questions-a-n-decisions.md      # >= 14 (each dated)
grep -n "PROVISIONAL" docs/corpus-questions-a-n-decisions.md       # status banner present
grep -n "Ratification" docs/corpus-questions-a-n-decisions.md      # ratification section
grep -n "Stale-docs ledger" docs/corpus-questions-a-n-decisions.md # T8 handoff section
grep -c "corpus-questions-a-n-decisions" docs/INDEX.md             # 1 — index line
ls engine/store/results/ | grep -c wg-t3-05                        # 1 — self-report exists
git log --oneline -3 | grep wg-t3-05                               # commit landed
```

Negative checks (this was a decision artifact, not a build; research/ is sacrosanct):
```bash
git status --porcelain research/                                   # empty
git diff HEAD~1 --stat -- research/                                # empty — nothing under research/ in the commit
git diff HEAD~1 --stat -- engine/ | grep -v "store/results"        # empty — no engine code touched
wc -l < research/artifacts.jsonl                                   # unchanged vs Move 2's recorded value
```
And: `engine/store/needs-decision/` contains a wg-t3-05 file ONLY if Fork F2 Route B or an
abort fired — otherwise it must not exist.

## Executor notes (sonnet)

- **Scope fence:** writes are exactly — `docs/corpus-questions-a-n-decisions.md` (new), one
  line in `docs/INDEX.md`, your results self-report, and (only per F2-B/aborts) one
  needs-decision file. Read anything; change nothing else. `research/` is READ-ONLY without
  exception — the strongest temptation in this ticket is "fix INDEX.md's stale stats" or
  "answer question E by editing the questions table". Both are A3 territory.
- **You are codifying, not legislating.** For RULED/RULED-DEFERRAL/DE-FACTO/RESOLVED
  questions you restate what David ruled or what practice settled — with citations. For the
  four OPEN questions you carry the authored defaults verbatim unless disk evidence
  contradicts them (Fork F2). You have no authority to invent a different default because
  yours "seems better".
- **Evidence over eloquence.** Every Evidence field carries the command or file+line that
  proved it, with YOUR execution-date values. The doc's whole value is that a distillation
  ticket six months out can re-run the probes and see whether a trigger fired.
- **Prefer HITL over guessing** the moment a default's premise flips (F2-B) or a ruling
  conflict appears you can't order by date. A parked question costs minutes; a wrong scope
  default silently poisons every cluster distillation downstream.
- **The rabbit hole:** re-running discover to true-up the corpus (the 1,100→1,150 drift, the
  uncounted david-local rows, matt-pocock's pending discover run). All of it is T3-13/T8
  work. Your job is to RECORD the drift in the Stale-docs ledger and answer the 14 questions.
  Skip it.
