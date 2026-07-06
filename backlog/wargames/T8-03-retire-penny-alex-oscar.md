# T8-03 — Retire Penny/Alex/Oscar from architecture.md

| field | value |
|---|---|
| ticket | wg-t8-03-retire-penny-alex-oscar |
| track / size / priority | T8 Doc truth / S / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

`docs/architecture.md` (§6) still presents three POEM personas — **Penny** (Prompt Orchestrator),
**Alex** (Prompt Architect), **Oscar** (Prompt Engineer) — as Dark Factory's conversational
interface, with four more references scattered through §7, §8, the §11 diagram, and the §12
roadmap. That layer was **superseded a day after the doc's last-updated date**: architecture.md
says `Last updated: 2026-06-01`; commit `5d2e14a` ("Name the runtime: Marshall (Conductor) +
Swagger (job-agent)") landed 2026-06-02, `docs/runtime-model.md` pinned the three-layer runtime
the same day, and the persona agents were **never built** (`.claude/agents/` does not exist in
this repo — verified 2026-07-06). `docs/watchtower/chatgpt-brief.md:99` already states the truth
plainly ("Swagger is the daily interface. Not Penny, Alec, or Oscar directly") — architecture.md
never caught up. Done looks like: all five persona references in architecture.md replaced with
their Marshall/Swagger equivalents, §6 carrying an explicit dated **supersession note** (retire
≠ erase — the history is recorded, not deleted), the header date bumped, zero
Penny/Alex/Oscar mentions in the file outside that note, and **no other file touched**.

## Locked context

- **Q9 (plans/wargames/decisions.md):** parked defaults all accepted, including "Penny/Alex/Oscar
  retired from architecture.md" — this ticket IS that default; the retire-vs-keep question is
  already decided, do not relitigate it.
- **Brief's locked default (candidate list):** "superseded by Marshall/Swagger a day after
  writing, never formally killed; **note the supersession**" — the section gets a dated
  supersession note, not a silent deletion.
- **Q5 (decisions.md):** YLO→POEM parked entirely — the personas are still *live concepts inside
  POEM* (`docs/ylo-to-poem-blueprint.md` §5, POEM repos). This ticket retires them **from
  dark-factory's architecture claim only**; no POEM-side file may be touched.
- **Q4 (decisions.md):** everything through the engine — sonnet Swagger dispatch; self-report to
  `engine/store/results/` per the orchestrator's task prompt.
- **Assessment-mode rule (CLAUDE.md):** never auto-rewrite a *ratified canonical* artifact.
  architecture.md is `docs/`, self-declared "**Status**: living document" (line 3) — in-place
  edit is the correct mechanism here, not a new version.
- **No `-p`/headless/SDK ever; interactive `claude` only** — binds how this ticket runs, not its
  content.

## Recon (verify before any work)

Docs lag code — trust nothing above until these pass. Repo root is
`/Users/davidcruwys/dev/ad/apps/dark-factory`; all paths relative to it. **Line numbers below
were true at authoring (2026-07-06) — treat them as hints; anchor every edit by grep, never by
line number.**

1. `ls docs/architecture.md && grep -n "Last updated" docs/architecture.md` → expect the file
   exists and the header says `**Last updated**: 2026-06-01` (verified line 4). File missing or
   moved → **Abort A1**. A *later* date than 2026-06-01 means someone touched it since
   authoring → run Recon 2 extra carefully; the anchors may have drifted (→ Fork F1 if so).
2. `grep -n "Penny\|Alex\|Oscar" docs/architecture.md` → expect exactly these five sites
   (verified 2026-07-06, 10 matching lines total):
   - §6 block ≈lines 282–294: heading `## 6 — The conversational layer: Penny, Alex, Oscar`,
     a 3-row persona table, and two paragraphs (one saying "These are agents
     (`.claude/agents/`) that live in dark-factory").
   - ≈line 318: bullet `- Talks to Penny/Alex/Oscar` (under §7 "This machine = Factory Floor").
   - ≈line 338: code-block line `> Penny, run the code-review factory on this branch.` (§8).
   - ≈line 412: ASCII-diagram row `│    Penny / Alex / Oscar (agents)` … `│` (§11).
   - ≈line 450: `**Phase E — Shadow Runs + Penny/Alex/Oscar (later)**` + the bullet
     `- Build the three persona agents` two lines below (§12).
   Zero matches → **Fork F1** (someone already retired them). Sites present but reshaped →
   anchor by the grep text you actually see; if a site is unfindable → **Fork F1 Route B**
   logic per-site.
3. `ls .claude/agents 2>&1` → expect `No such file or directory` (verified) — proof the persona
   agents were never built, which the supersession note asserts. If the directory NOW exists,
   check `ls .claude/agents/` for penny/alex/oscar files: present → **Abort A2** (the note's
   central claim would be false — reality changed under the ticket).
4. `git log --format="%ad %h %s" --date=short 5d2e14a -1 2>&1` → expect
   `2026-06-02 5d2e14a Name the runtime: Marshall (Conductor) + Swagger (job-agent)` (verified).
   Confirms the supersession date/commit the note will cite. Hash unknown (rebased history) →
   `git log --oneline --all | grep -i "Name the runtime"` and use the hash you find; if no such
   commit exists at all, cite `docs/runtime-model.md`'s own header date (2026-06-02) instead
   and drop the hash from the note.
5. `head -3 docs/runtime-model.md && ls .claude/skills/marshall/SKILL.md .claude/skills/swagger/SKILL.md .claude/skills/millwright/SKILL.md`
   → expect runtime-model.md header `**Status**: 2026-06-02 — resolved in design session` and
   all three skill files present (verified). These are the replacement targets the new text
   points at. Any missing → **Abort A2** (can't point retirement at a successor that isn't
   there).
6. `grep -c "Penny" docs/ylo-to-poem-blueprint.md` → expect ≥5 (verified: many). Confirms the
   personas are live POEM concepts — reinforces the scope fence (touch NOTHING outside
   architecture.md).
7. Baseline: `git status --porcelain` → note pre-existing dirt so verification's negative checks
   don't blame this ticket for it.

## Moves

### Move 1 — Rewrite §6 as Marshall/Swagger + a dated supersession note

- **Do:** In `docs/architecture.md`, replace the entire §6 block — from the line
  `## 6 — The conversational layer: Penny, Alex, Oscar` down to (not including) the next `---`
  separator — with exactly:

  ```markdown
  ## 6 — The conversational layer: Marshall & Swagger

  Dark Factory's human interface is the runtime pair defined in `docs/runtime-model.md`:

  | Role | What it is | What you ask |
  |------|-----------|--------------|
  | **Marshall** (Conductor) | David's primary daily orchestrator, in the Watchtower. Routes; never coordinates. | "What's in flight?" "What should we work on next?" "Run the code-review factory on this branch." |
  | **Swagger** (job-agent) | Owns ONE job end-to-end with judgment; runs workflows and/or sub-agent panes. | Dispatched by Marshall; or "own this job." |

  Marshall's build-side sibling **Millwright** decides the *form* of new machinery (skill /
  workflow / agent-job). Skills: `.claude/skills/marshall/`, `.claude/skills/swagger/`,
  `.claude/skills/millwright/`.

  > **Superseded (noted 2026-07-06, wg-t8-03).** This section originally specified three POEM
  > personas — Penny (Prompt Orchestrator), Alex (Prompt Architect), Oscar (Prompt Engineer) —
  > as the conversational interface. They were superseded **one day after this doc's 2026-06-01
  > update** by the Marshall/Swagger naming (commit `5d2e14a`, 2026-06-02; `docs/runtime-model.md`)
  > but never formally retired here. The persona agents were never built in this repo
  > (`.claude/agents/` was never created). The personas remain live concepts **inside POEM**
  > (`docs/ylo-to-poem-blueprint.md` §5; POEM repos) — retired here from the dark-factory
  > architecture claim only.
  ```

  Two substitutions while writing it: (a) if Recon 4 produced a different hash, use that hash;
  no hash found → cite only "2026-06-02; `docs/runtime-model.md`". (b) Replace the note's
  `noted 2026-07-06` with the actual execution date.
- **Expect:** `grep -n "## 6 — The conversational layer: Marshall & Swagger" docs/architecture.md`
  → 1 hit; `grep -c "Superseded" docs/architecture.md` → 1; the only Penny/Alex/Oscar mentions
  inside §6 are within the blockquote note.
- **Failure signal:** the §6 heading text doesn't match (drifted since authoring), or the
  section boundary (`---`) isn't where expected and the replacement eats neighbouring content.
- **Counter-move:** re-locate by `grep -n "conversational layer" docs/architecture.md` and
  bound the section by the surrounding `## 5`/`## 7` headings instead of `---`. If §6 no longer
  discusses a conversational layer at all → Fork F1. If you clobbered neighbouring content:
  `git checkout -- docs/architecture.md` and redo from Recon 2. Second clobber → Abort A3.

### Move 2 — Fix the §7 bullet and the §8 example (surgical, one line each)

- **Do:** (a) Replace the line `- Talks to Penny/Alex/Oscar` with
  `- Talks to Marshall (the Conductor), who dispatches Swaggers`.
  (b) In the §8 code block, replace `> Penny, run the code-review factory on this branch.` with
  `> Marshall, run the code-review factory on this branch.`
  **Change nothing else in §7** — its Warehouse-Keeper/Factory-Floor content is also stale, but
  that is a separate T8 ticket's job (see Executor notes).
- **Expect:** `grep -n "Talks to Marshall" docs/architecture.md` → 1 hit;
  `grep -n "Marshall, run the code-review" docs/architecture.md` → 1 hit; neither old line
  remains.
- **Failure signal:** either old line not found verbatim.
- **Counter-move:** re-grep for the fragment (`Talks to`, `run the code-review factory`) and
  edit whatever persona-referencing form you find; if the line is simply gone (already fixed),
  skip that sub-edit and note it in the results JSON.

### Move 3 — Fix the §11 ASCII diagram row without breaking box alignment

- **Do:** In the §11 diagram, replace the row
  `│    Penny / Alex / Oscar (agents)` (trailing spaces + `│`) with
  `│    Marshall → Swagger (job-agents)` **padded with spaces so the trailing `│` stays in the
  exact same column** — the replacement text (35 chars) is 2 chars longer than the original
  (33 chars), so remove 2 padding spaces. Verify alignment by eye: print the row with its
  neighbours (`grep -n -B2 -A2 "Marshall → Swagger" docs/architecture.md`) and confirm all
  trailing `│` line up.
- **Expect:** the diagram renders with all right-edge `│` characters in one column; grep for
  `Penny` in the diagram region returns nothing.
- **Failure signal:** trailing `│` misaligned (off-by-N spaces), or the diagram row isn't found.
- **Counter-move:** count and fix the padding (each `│…│` row in this diagram is the same
  total width — match a neighbouring row's length exactly, e.g. with
  `awk 'length($0)>0 {print length($0)}'` on the diagram lines). Row not found → the diagram
  was redrawn; grep the diagram region for any persona name and apply the same one-row
  substitution to whatever form exists; none found → skip, note in results JSON.

### Move 4 — Fix the §12 Phase E roadmap line + bump the header date

- **Do:** (a) Replace `**Phase E — Shadow Runs + Penny/Alex/Oscar (later)**` with
  `**Phase E — Shadow Runs (later)**` and replace the bullet
  `- Build the three persona agents` (two lines below it) with
  `- Conversational layer already shipped as Marshall/Swagger (2026-06-02) — see §6`.
  (b) In the header, change `**Last updated**: 2026-06-01` to `**Last updated**: <execution
  date>` (real date, `date +%Y-%m-%d`).
- **Expect:** `grep -c "Penny\|Alex\|Oscar" docs/architecture.md` now counts ONLY the
  supersession-note lines from Move 1 (3 lines: the two naming lines and the POEM line —
  verify by eyeballing `grep -n "Penny\|Alex\|Oscar" docs/architecture.md`: every remaining
  hit sits inside the §6 blockquote).
- **Failure signal:** persona mentions remain outside the §6 note.
- **Counter-move:** each straggler is a site Recon 2 didn't predict — apply the same
  pattern (replace with the Marshall/Swagger equivalent, or fold into the note if it's
  historical narrative). More than 2 unpredicted sites → the doc drifted materially → Fork F1
  Route B judgment; if the drift is a rewrite-in-progress → Abort A3.

### Move 5 — Verify, self-report, commit, push

- **Do:** Run the full Verification battery below. Write the worker self-report to
  `engine/store/results/<this-ticket-filename>.json` in the exact form the orchestrator's task
  prompt demands (include: which of the 5 sites were edited vs already-fixed/skipped, the
  supersession-note hash used, any drift noted). Commit ONLY `docs/architecture.md` plus the
  results file, message
  `docs(architecture): retire Penny/Alex/Oscar — superseded by Marshall/Swagger 2026-06-02 (wg-t8-03)`
  with the standard Co-Authored-By trailer; push.
- **Expect:** every verification command passes; `git log --oneline -1` shows the commit;
  `git status --porcelain` clean apart from Recon 7's pre-existing dirt.
- **Failure signal:** push rejected (non-fast-forward) — another session/machine pushed.
- **Counter-move:** `git pull --rebase` then push. A rebase conflict in architecture.md means a
  concurrent edit to the same doc → inspect: if the other side ALSO retired the personas,
  keep theirs, re-run verification, and report yours as merged; any other conflict shape →
  resolve keeping both intents if trivially compatible, else Abort A3. Second push failure →
  leave committed locally, note it in the results JSON.

## Forks

**F1 — The personas are already gone (someone beat this ticket to it).**
Trigger: Recon 2 returns zero Penny/Alex/Oscar matches in architecture.md.
→ **Route A (a supersession note exists):** `grep -n "Superseded\|Marshall" docs/architecture.md`
shows §6 already carries the note or equivalent → the work is done; write the results JSON
reporting no-op-verified (list what you found), do not edit, do not commit doc changes — the
ticket completes as a verification pass.
→ **Route B (silently deleted — no note anywhere):** the locked default ("note the
supersession") is NOT satisfied by silent deletion. Add ONLY the Move 1 blockquote note to
whatever §6 now is (or the nearest conversational-layer section), header-date bump, commit,
report. If no conversational-layer section exists at all to hang the note on → Abort A3.

**F2 — Recon 1 shows a post-authoring `Last updated` date (doc touched since 2026-07-06).**
Trigger: header date later than 2026-06-01 AND Recon 2 sites partially match.
→ **Route A (sites match ≥4 of 5):** proceed; treat unmatched sites per each move's
counter-move (grep-anchored, skip-and-note when gone).
→ **Route B (sites match ≤3 of 5):** the doc materially drifted — someone is actively
reworking it. Do not race a rewrite → Abort A3.

## Assumptions ledger

1. **Marshall/Swagger (+ Millwright as build-side) is the correct successor mapping for all
   three personas.** Plausible: runtime-model.md (2026-06-02) defines the full runtime;
   chatgpt-brief.md:99 states "Swagger is the daily interface. Not Penny, Alec, or Oscar";
   millwright's SKILL.md self-describes as "Marshall's build-side sibling" (covers
   Alex-the-designer / Oscar-the-mechanic territory). If David objects to the mapping at
   triage/HITL: the note's supersession *fact* stands regardless — adjust only the §6 table
   wording per his correction and continue.
2. **In-place edit of architecture.md is permitted.** Plausible: the doc self-declares "living
   document"; the assessment-mode freeze applies to ratified `canonical/` artifacts, and the
   2026-06-16 doc-drift sweep (commit `6b91d46`) already edited this file in place as routine
   work. If David objects → revert, park to needs-decision/ asking whether architecture.md
   changes need a versioned-copy mechanism.
3. **Other files' persona mentions stay untouched.** `docs/workflow-tool-authoring-notes.md`
   (R14 risk row), `spikes/blackboard-mcp/{README,HANDOVER}.md` (historical spike records),
   `backlog/2026-05-18-elicit-skill-workshop-spec.md` and `mochaccino/briefs/…` (POEM-context),
   `docs/ylo-to-poem-blueprint.md` (parked POEM track), `docs/watchtower/chatgpt-brief.md`
   (already correct). Plausible: the locked default names architecture.md specifically;
   spike/backlog files are historical records where retro-editing would falsify provenance.
   If the executor believes one of these actively misleads → note it in the results JSON as a
   candidate follow-up ticket; do NOT edit it.
4. **The §11 diagram is plain `│`-boxed ASCII whose rows share one width.** Verified at
   authoring. If the diagram was converted to mermaid/image since → apply the same one-node
   rename in whatever format exists; if that's not a trivial text edit → skip the diagram,
   note it, continue (the note in §6 still lands the supersession).

## Abort conditions

**A1 — architecture.md missing or relocated.** Recon 1 fails. Park: write
`engine/store/needs-decision/wg-t8-03-retire-penny-alex-oscar.json` containing
`{"ticket":"wg-t8-03-retire-penny-alex-oscar","question":"docs/architecture.md is missing/moved (expected at authoring 2026-07-06). Where does the architecture statement live now, and does the Penny/Alex/Oscar retirement still apply?","proposed":"git log --follow the old path; apply the war game to the successor doc if one exists","note":"<what was found>"}`.
Leave the ticket in `running/`.

**A2 — Reality inverted under the ticket.** `.claude/agents/` now contains penny/alex/oscar
agents (Recon 3), or the Marshall/Swagger/Millwright skills are gone (Recon 5). The
supersession note's central claims would be false — never write a "truth" note you can't
verify. Park to needs-decision/ (same shape as A1; question: "T8-03 assumes the personas were
never built and Marshall/Swagger exist — recon found the opposite: <finding>. Retire, or is
the persona layer being revived?"). Leave the ticket in `running/`.

**A3 — Concurrent rewrite or unbounded drift.** Fork F2 Route B (doc materially reworked),
Fork F1 Route B with no section to hang the note on, a second Move-1 clobber, or a
non-trivial rebase conflict in Move 5. Park to needs-decision/ with the concrete diff/finding
in `note` (question: "architecture.md is being actively reworked / has drifted beyond T8-03's
anchors: <what changed>. Re-anchor this retirement, or fold it into the rework?"). Leave the
ticket in `running/`. Never race another writer on the same doc.

## Verification

Run from `/Users/davidcruwys/dev/ad/apps/dark-factory`:

```bash
# The five sites are fixed
grep -c "## 6 — The conversational layer: Marshall & Swagger" docs/architecture.md   # 1
grep -c "Superseded" docs/architecture.md                                            # 1
grep -c "Talks to Marshall" docs/architecture.md                                     # 1
grep -c "Marshall, run the code-review factory" docs/architecture.md                 # 1
grep -c "Marshall → Swagger (job-agents)" docs/architecture.md                       # 1
grep -c "Phase E — Shadow Runs (later)" docs/architecture.md                         # 1

# Personas survive ONLY inside the §6 supersession blockquote (every hit is a '> '-prefixed line)
grep -n "Penny\|Alex\|Oscar" docs/architecture.md | grep -vc "^[0-9]*:>"             # 0

# Header date bumped
grep -c "Last updated.*: 2026-06-01" docs/architecture.md                            # 0

# Self-report exists
ls engine/store/results/ | grep -c wg-t8-03                                          # 1
```

Diagram alignment (§11): `grep -B2 -A2 "Marshall → Swagger" docs/architecture.md` — all
trailing `│` characters sit in the same column.

Negative checks (nothing else changed):
```bash
git diff HEAD~1 --stat                                # docs/architecture.md + the results file ONLY
git diff HEAD~1 -- docs/runtime-model.md docs/ylo-to-poem-blueprint.md \
  docs/workflow-tool-authoring-notes.md docs/watchtower/ spikes/ backlog/ \
  .claude/skills/                                     # empty
grep -c "Penny" docs/ylo-to-poem-blueprint.md         # unchanged from recon (≥5) — POEM untouched
```

(Under Fork F1 Route A, the doc checks instead verify the pre-existing state and no new commit
touches architecture.md — the results JSON explains the no-op.)

## Executor notes (sonnet)

- **Scope fence:** edit `docs/architecture.md` ONLY (plus the results/needs-decision store files
  this ticket's lifecycle requires). Do NOT touch: `docs/ylo-to-poem-blueprint.md` or anything
  POEM (Q5: parked), `docs/workflow-tool-authoring-notes.md`, `spikes/`, `backlog/` history
  files, `mochaccino/`, any `.claude/skills/`, `docs/runtime-model.md`.
- **Retire ≠ erase.** The locked default says *note the supersession*. The blockquote in Move 1
  is the deliverable's heart — a reader must be able to see what the doc used to claim, when it
  was superseded, and where the personas still live (POEM).
- **Anchor by grep, never by line number.** Authoring-time line numbers are hints only.
- **Prefer HITL over guessing** on anything that smells like a concurrent rewrite (A3) — a
  needs-decision/ park costs minutes; racing another writer on the architecture doc costs a
  mangled canonical statement.
- **The rabbit hole:** §7's Warehouse-Keeper/Factory-Floor content is ALSO stale (M4 Pro
  "Warehouse Keeper" was likely never set up — that resolution is its own T8 seed), and the
  whole doc has more drift (Phase B/C claims, workflow-runtime framing). You will be tempted to
  do a full truth-reconciliation pass while you're in there. **Skip ALL of it** — this ticket
  changes persona references + the header date, nothing else. The broader doc-truth pass is a
  separate T8 ticket.
