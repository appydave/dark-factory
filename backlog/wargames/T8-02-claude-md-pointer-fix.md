# T8-02 — Fix CLAUDE.md's stale activation pointer

| field | value |
|---|---|
| ticket | wg-t8-02-claude-md-pointer-fix |
| track / size / priority | T8 Doc truth / S / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Every fresh session that follows `CLAUDE.md`'s "First thing to do on activation" is told
`docs/phase-b-next-steps.md` is the **START HERE** — a 2026-05-25 plan whose status line still
reads "thinking / not started" and whose entire content (two `workflow.js` builds, the
"David's voice" open question) was superseded by the engine (`engine/`, shipped) and the
2026-07-06 war-game portfolio (first ingestion = war games T3-01/T3-02, session split locked by
decisions.md Q9). Fix the misroute at all three ends: (1) rewrite the activation section of
`CLAUDE.md` to point at the current spine (README banner → north-star → INDEX) and the live work
surfaces (engine store + war-game portfolio), (2) stamp a supersession banner on
`docs/phase-b-next-steps.md` (repo precedent: `docs/watchtower/spec.md`), (3) correct
`docs/INDEX.md`'s one stale descriptor line for that doc. Done looks like: a fresh session
reading CLAUDE.md lands on today's factory, three files changed, nothing else touched,
committed and pushed to main. This is a surgical pointer fix — the broader
truth-reconciliation pass (harness-evaluation / runtime-model / six-app-eval status lines,
Penny/Alex/Oscar retirement, the CLAUDE.md charter paragraphs themselves) is OTHER T8 tickets'
scope, not this one.

## Locked context

- **Q9 (decisions.md):** "CLAUDE.md phase-b pointer fixed" — an accepted parked default; this
  ticket IS that fix.
- **Q9 also locked** the answers phase-b-next-steps.md left open: first ingestion named
  `review-dimensional`; harvest+draft / voice-review+ratify session split — cite these in the
  banner, don't re-litigate them.
- **Q5:** YLO→POEM parked entirely — do NOT expand scope into rewriting CLAUDE.md's YLO
  "Two threads" paragraph (charter-truth is a different T8 concern); this ticket touches ONLY
  the activation section.
- **Q4:** everything through the engine — the new activation text must route agents at the
  engine store + ticket convention, not at ad-hoc backlog reading alone.
- **Docs lag code** (wargame-spec): the replacement text below was verified against disk on
  2026-07-06; your Recon re-verifies every pointed-at path before you write it into CLAUDE.md.

## Recon (verify before any work)

All paths relative to `/Users/davidcruwys/dev/ad/apps/dark-factory` unless absolute. Run every check.

1. `grep -n "START HERE if Phase B" CLAUDE.md` → expect exactly one hit (line ~24, the
   `phase-b-next-steps.md` bullet inside "## First thing to do on activation", lines ~15–26).
   Zero hits → the fix already landed or the section was rewritten → **Fork F1**.
2. `git -C /Users/davidcruwys/dev/ad/apps/dark-factory status --porcelain -- CLAUDE.md docs/phase-b-next-steps.md docs/INDEX.md`
   → expect empty (all three committed-clean; at authoring the only repo dirt was the untracked
   war-game portfolio itself). Any of the three showing modified → someone is mid-edit on your
   exact seam → **Abort A2**.
3. `ls engine/store/running/ | grep -i "t8\|claude-md\|doc-truth"` and the same grep over
   `ls engine/store/done/` → expect no hits (no sibling T8 ticket currently holds or already did
   this work). A running hit → **Abort A2**. A done hit → **Fork F1** (verify-and-close).
4. Every path the replacement text points at must exist NOW:
   `ls README.md docs/north-star.md docs/INDEX.md docs/daily-operating-model.md engine/README.md engine/store/queue/.CONVENTION.md engine/store/needs-decision plans/wargames/wargame-spec.md plans/wargames/decisions.md backlog/wargames/tickets docs/canonical-form-spec.md docs/provenance-spec.md docs/ingestion-workflow.md docs/david-style-patterns.md docs/phase-b-next-steps.md`
   → expect all present, exit 0 (all verified 2026-07-06). Any missing → adjust the replacement
   text's pointer to the found equivalent if it's a rename you can prove via
   `git log --diff-filter=R --summary -5 -- <old-path>`; if `docs/north-star.md` or `engine/`
   is gone entirely, the repo's shape has shifted under the whole T8 track → **Abort A1**.
5. `head -8 docs/phase-b-next-steps.md` → expect the H1 then `**Status**: thinking / not started`
   and `**Last updated**: 2026-05-25`, and NO "SUPERSEDED" banner yet. Banner already present →
   skip Move 2, note it in the result, continue.
6. `grep -n "phase-b-next-steps" docs/INDEX.md` → expect one hit (~line 41):
   `- **\`phase-b-next-steps.md\`** — the next build move (first dog-food workflow).` Already
   rewritten to say historical/superseded → skip Move 3, note it, continue.
7. Confirm the banner's factual claims still hold before writing them:
   `grep -n "review-dimensional\|voice-review" plans/wargames/decisions.md` → expect the Q9 row
   naming `review-dimensional` and the harvest+draft / voice-review+ratify split; and
   `ls backlog/wargames/T3-01-first-ingestion-review-dimensional.md backlog/wargames/T3-02-ratify-first-ingestion.md`
   → both exist. Missing → cite only what exists (decisions.md Q9 at minimum); if decisions.md
   itself lacks Q9 → **Abort A1** (you're in the wrong universe).

## Moves

1. **Do:** In `CLAUDE.md`, replace the ENTIRE "## First thing to do on activation" section —
   from the `## First thing to do on activation` heading down to (not including) the
   `## Hard rules` heading — with exactly this (adjusting only pointers Recon 4 forced you to
   correct):

   ```markdown
   ## First thing to do on activation

   1. Read `README.md` for the repo charter — its top banner names the current priority:
      **Path 1, building the factory machinery**; the canonical-ingestion charter is Path 2
      (deferred cargo, not abandoned).
   2. Read `docs/north-star.md` (the orienting frame), then `docs/INDEX.md` for the full
      docs read-order.
   3. Check the live work surfaces, most-recent-first:
      - `engine/store/queue/` — live engine tickets. Ticket-first is a standing rule (every
        unit of work gets a ticket): idiom in `engine/store/queue/.CONVENTION.md`, engine in
        `engine/README.md`.
      - `engine/store/needs-decision/` — parked questions awaiting David.
      - `backlog/wargames/` — the war-game portfolio (2026-07-06): pre-simulated work
        packages with staged engine tickets in `backlog/wargames/tickets/`; governing spec
        `plans/wargames/wargame-spec.md`, locked decisions `plans/wargames/decisions.md`.
      - `backlog/` — PO work items; most-recent-first, pick the highest priority.
   4. Only for canonical-ingestion work, read the governing specs:
      `docs/canonical-form-spec.md`, `docs/provenance-spec.md`, `docs/ingestion-workflow.md`,
      `docs/david-style-patterns.md`. (`docs/phase-b-next-steps.md` is historical — its open
      questions were resolved by `plans/wargames/decisions.md` Q9, and the first ingestion is
      war-gamed as T3-01/T3-02.)
   5. Execute per the spec that governs your work item. Docs lag code in this repo — when a
      strategy doc and the repo disagree, the repo wins; flag the drift.
   ```

   Touch nothing above the section heading and nothing from `## Hard rules` down.
   **Expect:** `grep -c "START HERE if Phase B" CLAUDE.md` → 0;
   `grep -c "north-star" CLAUDE.md` → ≥1; `grep -c "backlog/wargames" CLAUDE.md` → ≥1;
   `git diff -- CLAUDE.md` shows one contiguous hunk inside the activation section only.
   **Failure signal:** the diff bleeds into "## How sessions are organized" or "## Hard rules",
   or any grep above misses.
   **Counter-move:** `git checkout -- CLAUDE.md` and redo the replacement against the exact
   heading boundaries. A second failure means the file no longer matches Recon 1's shape →
   **Fork F1**.

2. **Do:** In `docs/phase-b-next-steps.md`, insert this blockquote banner on a new line
   directly under the `# Phase B — Next Steps` H1 (before the `**Status**` line), leaving every
   existing line intact (repo precedent for the banner shape: `docs/watchtower/spec.md`):

   ```markdown
   > **⚠️ SUPERSEDED (2026-07-06, war-game portfolio).** This 2026-05-25 plan predates the
   > shipped engine (`engine/` — the queue/claim/dispatch/reap kernel) and the war-game
   > portfolio (`backlog/wargames/`). Its open questions were resolved by
   > `plans/wargames/decisions.md` Q9: the first ingestion is named `review-dimensional` and
   > split harvest+draft / voice-review+ratify across two sessions — executed as war games
   > T3-01/T3-02 through the engine, not via the `workflow.js` pair designed below. Kept for
   > the ingestion-brief design detail; this is NOT the activation entry point.
   ```

   **Expect:** `head -12 docs/phase-b-next-steps.md` shows H1 → banner → original Status line;
   `grep -c "SUPERSEDED" docs/phase-b-next-steps.md` → 1; diff is purely additive.
   **Failure signal:** any original line removed or reworded (`git diff` shows `-` lines other
   than context).
   **Counter-move:** `git checkout -- docs/phase-b-next-steps.md`, redo as a pure insert.

3. **Do:** In `docs/INDEX.md`, replace the single stale descriptor line (Recon 6's hit) with:

   ```markdown
   - **`phase-b-next-steps.md`** — historical (superseded 2026-07-06): the pre-engine first-ingestion plan; the first ingestion now runs as war games T3-01/T3-02 through the engine. Supersession banner inside.
   ```

   One line out, one line in; touch nothing else in INDEX.md.
   **Expect:** `grep -n "phase-b-next-steps" docs/INDEX.md` → exactly one hit containing
   "historical"; `git diff --stat -- docs/INDEX.md` → 1 insertion, 1 deletion.
   **Failure signal:** more than one line changed.
   **Counter-move:** `git checkout -- docs/INDEX.md`, redo the single-line swap.

4. **Do:** Run the routing sweep — prove no activation-path doc still routes a fresh session at
   phase-b as current work:
   `grep -rn "START HERE if Phase B" CLAUDE.md README.md docs/INDEX.md` (expect 0 hits) and
   `grep -rn "phase-b-next-steps" CLAUDE.md docs/INDEX.md` (expect hits only in your new
   "historical" phrasings). Then confirm scope held:
   `git status --porcelain` → exactly three modified files (`CLAUDE.md`,
   `docs/INDEX.md`, `docs/phase-b-next-steps.md`) plus whatever untracked war-game-portfolio
   files were already there at Recon 2.
   **Expect:** as stated. Note: `docs/dark-factory-living-system-spec.md` also mentions
   phase-b-next-steps (companion-doc list, line ~6, and a historical aside, line ~323) — those
   are contextual references, not activation routing; verified 2026-07-06 and deliberately LEFT
   ALONE.
   **Failure signal:** a fourth modified file, or a surviving "START HERE if Phase B".
   **Counter-move:** `git checkout` any file you touched beyond the three; re-apply the missed
   edit from its move. If the stray modification isn't yours (appeared mid-run) → **Abort A2**.

5. **Do:** Commit the three files to `main` and push (repo standing practice — war-game
   portfolio precedent commits directly to main; David's global rule: commit and push finished
   work). `git add CLAUDE.md docs/INDEX.md docs/phase-b-next-steps.md` then commit with message:
   `docs: fix stale phase-b activation pointer — CLAUDE.md routes at spine + war-game portfolio (wg-t8-02)`
   then `git push`. Stage ONLY these three — leave the untracked portfolio files and any
   stranger's dirt alone.
   **Expect:** push succeeds; `git log --oneline -1` shows the message;
   `git status --porcelain` no longer lists the three files.
   **Failure signal:** push rejected (remote ahead).
   **Counter-move:** `git pull --rebase` then push. Rebase conflict in one of YOUR three files →
   another session edited the same seam mid-run → **Abort A2** (do not merge truth claims by
   guess). Conflict in a file you never touched → also **Abort A2**, citing the path.

## Forks

**F1 — the fix already landed (race with a sibling doc-truth ticket).**
Trigger: Recon 1 finds zero "START HERE if Phase B" hits, Recon 3 finds a done/ sibling that
claims CLAUDE.md, or Move 1's counter-move fails twice because the section no longer matches.
→ **Route A** (the existing state already does this ticket's job: activation section points at
north-star/INDEX + engine store + `backlog/wargames/`, phase-b demoted to historical): switch to
verify-and-close — run Moves 2–4's Expect checks against what's on disk, patch ONLY genuinely
missing pieces (e.g. banner landed but INDEX.md line didn't), commit whatever you patched per
Move 5, and record in the result that the core fix pre-existed.
→ **Route B** (the section was rewritten but still misroutes — e.g. phase-b still framed as the
entry point, or the new text points at paths that fail Recon 4's existence check): do NOT layer
a second rewrite on top of someone's fresh intent → **Abort A1** with a diff of found-vs-drafted
text.

## Assumptions ledger

1. **No parallel T8 ticket owns CLAUDE.md's activation section.** Plausible: at authoring
   (2026-07-06) no T8 war game or ticket existed yet in `backlog/wargames/`, and the T8
   truth-reconciliation seed (path-map) targets doc STATUS LINES (harness-evaluation,
   runtime-model, six-app-eval), not CLAUDE.md activation. **If false** (Recon 3 or Fork F1
   triggers): follow F1; if genuinely contested (a running/ sibling), park per A2 — never
   two writers on one seam.
2. **The drafted replacement text is still an accurate spine at execution time.** Plausible:
   every pointer was `ls`-verified on 2026-07-06 and these are the repo's most stable docs
   (north-star "read before anything else", INDEX "living index"). **If false** for a single
   pointer (renamed/moved): Recon 4's rename-trace covers it — point at the successor and note
   the substitution in the result. **If false wholesale** (spine restructured): → Abort A1;
   re-authoring the activation section against an unknown new shape is a taste call above a
   sonnet executor's pay grade.
3. **phase-b-next-steps.md should be bannered, not deleted or moved.** Plausible: repo precedent
   is supersession banners in place (`docs/watchtower/spec.md`), INDEX.md's own doctrine is
   "gets a line here or it doesn't exist", and the doc's ingestion-brief design detail is still
   referenced by `docs/dark-factory-living-system-spec.md`. **If false** (David wants it
   archived): that's a one-`git mv` follow-up, not this ticket — note it, don't do it.
4. **Direct commit to main is correct.** Plausible: David's standing global rule ("commit and
   push finished work", "default to main") + every prior war game commits to main. **If false**
   (a branch-protection or workflow change rejects the push in a way `pull --rebase` can't fix):
   park per A2 with the rejection text.

## Abort conditions

- **A1 — truth conflict / spine shifted.** Fork F1 Route B (a post-authoring rewrite that still
  misroutes, where layering edits would fight fresh intent), Recon 4 finding the spine docs
  wholesale gone/renamed, or Recon 7 finding decisions.md lacks Q9. Park: write
  `engine/store/needs-decision/wg-t8-02-claude-md-pointer-fix.json` with
  `{"ticket": "wg-t8-02-claude-md-pointer-fix", "question": "CLAUDE.md activation fix blocked: <found state> conflicts with the war game's drafted replacement. Whose truth wins — re-author against the new shape, or is the drafted text still wanted?", "observed": "<the diff / missing paths>"}`.
  Leave this ticket in `running/`. Never guess a new orientation text for the repo's front door.
- **A2 — concurrent writer on the seam.** Recon 2/3 shows uncommitted edits or a running/
  sibling on any of the three files, Move 4 finds a mid-run stray modification, or Move 5 hits a
  rebase conflict. Park with the same file shape: question
  "wg-t8-02 collided with a concurrent edit on <paths> — who owns this seam right now?",
  observed = the `git status` / conflict evidence. Leave the ticket in `running/`.

## Verification

```bash
DF=/Users/davidcruwys/dev/ad/apps/dark-factory

# 1. The misroute is gone
grep -c "START HERE if Phase B" $DF/CLAUDE.md                       # → 0

# 2. Activation points at the current spine + portfolio + engine store
grep -c "docs/north-star.md" $DF/CLAUDE.md                          # → ≥1
grep -c "backlog/wargames"   $DF/CLAUDE.md                          # → ≥1
grep -c "engine/store/queue" $DF/CLAUDE.md                          # → ≥1
grep -c "needs-decision"     $DF/CLAUDE.md                          # → ≥1

# 3. Every path the new activation text names actually exists
grep -oE '(docs|engine|plans|backlog)[A-Za-z0-9/._-]*' $DF/CLAUDE.md | sort -u | \
  while read p; do test -e "$DF/$p" || echo "BROKEN POINTER: $p"; done   # → no output

# 4. phase-b demoted at all three ends
grep -c "SUPERSEDED" $DF/docs/phase-b-next-steps.md                 # → 1
grep -c "thinking / not started" $DF/docs/phase-b-next-steps.md     # → 1 (original line preserved — banner was additive)
grep -n "phase-b-next-steps" $DF/docs/INDEX.md | grep -c "historical"   # → 1
grep -c "historical" <(grep "phase-b-next-steps" $DF/CLAUDE.md)     # → 1

# 5. Negative checks — what must NOT have changed
grep -c "## Hard rules" $DF/CLAUDE.md                               # → 1 (section intact)
grep -c "Don't do without asking" $DF/CLAUDE.md                     # → 1
grep -c "## Query tools" $DF/CLAUDE.md                              # → 1 (2026-07-06 section survived)
git -C $DF show --stat HEAD | grep -cE "CLAUDE.md|docs/INDEX.md|docs/phase-b-next-steps.md"  # → 3 (and nothing else in the commit)
git -C $DF diff HEAD~1 HEAD -- docs/dark-factory-living-system-spec.md | wc -l               # → 0 (deliberately untouched)

# 6. Committed and pushed
git -C $DF log --oneline -1 | grep -c "wg-t8-02"                    # → 1
git -C $DF status --porcelain -- CLAUDE.md docs/INDEX.md docs/phase-b-next-steps.md | wc -l  # → 0
```

## Executor notes (sonnet)

- **Scope fence.** This is a THREE-FILE ticket: `CLAUDE.md` (one section), `docs/INDEX.md` (one
  line), `docs/phase-b-next-steps.md` (one additive banner). Do NOT touch CLAUDE.md's charter
  paragraphs ("canonical skill library project", the YLO "Two threads" para) even though they
  are also stale — charter-truth is other T8 tickets' scope. Do NOT edit
  `docs/dark-factory-living-system-spec.md`, `README.md`, `research/`, anything in `engine/*.py`,
  or anything under `~/dev/ad/appydave-plugins/`. Do NOT delete, move, or rewrite the body of
  phase-b-next-steps.md.
- **The rabbit hole: fixing all the drift you'll see.** Reading north-star/INDEX/README to
  verify pointers will surface a dozen other stale lines (INDEX's watchtower cluster, spec
  status dates, the CLAUDE.md charter itself). Resist. Each is a one-line note in your result's
  `notes` field at most — the T8 truth-reconciliation ticket exists precisely so you don't
  freelance it here.
- **Style:** the replacement text is given verbatim — use it as written (minus any Recon-4
  forced pointer substitutions, each one noted in the result). Terse, David's register, no
  marketing prose. The banner matches the `docs/watchtower/spec.md` blockquote idiom.
- **Prefer parking over guessing:** this file is the repo's front door and every future session
  eats what you write here. Any conflict about what the activation text SHOULD say (F1 Route B,
  A1) is David's call, not yours.
