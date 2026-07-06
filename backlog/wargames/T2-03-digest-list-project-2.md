# T2-03 — digest.py --list + onboard project #2

| field | value |
|---|---|
| ticket | wg-t2-03-digest-list-project-2 |
| track / size / priority | T2 Producer/BA / S / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Give project-digest (`~/dev/ad/apps/project-digest/`) its two missing generalization proofs so
the T2 morning-briefing chain can loop over more than one project. **(a)** a `--list` flag on
`digest.py` that wraps the already-built `lib/config.list_project_ids()` (today used only inside
an error message, config.py:73) — "what projects can I even ask about" gets a real answer.
**(b)** onboard project #2 — default **omi-fetch** (`~/dev/ad/apps/omi-fetch/`, the most
actively-worked constellation sibling as of authoring) — per the README's own "Adding a project"
recipe, wiring the one piece of real code `docs/extension-notes.md` ranks #1 (the
`needs_you.markers` config key exists in the schema but `lib/needs_you.py` never reads it), and
honestly documenting which of the three ranked generalization items needed code vs worked out of
the box. Done also closes the deferred engine ticket
`engine/store/queue/20260704T0630Z-project-digest-list-and-project-2.json` (this war game IS that
work) by moving it to `done/` with a superseded-by result. This ticket does NOT build the
universal activity registry, the `--all` loop, or the BA agent — those are separate T2 tickets.

## Locked context

- **Q4 (decisions.md):** everything through the engine — written for sonnet Swagger dispatch.
- **No `-p`/headless/SDK ever; interactive `claude` only** — moot here (pure Python CLI work;
  nothing in this ticket spawns Claude or touches dispatch).
- **No YLO/POEM work** — out of scope entirely.
- **Docs lag code** (wargame-spec) — extension-notes' claims about needs_you.py were re-verified
  on disk at authoring (2026-07-06); your Recon re-verifies at execution time.
- **Store is a growing ledger** — the deferred queue ticket gets MOVED to done/ with a result
  appended, never deleted; its original `deferred_reason` text stays intact (history).

## Recon (verify before any work)

Run every check. All paths absolute; project-digest root = `/Users/davidcruwys/dev/ad/apps/project-digest`.

1. `grep -n "add_argument" /Users/davidcruwys/dev/ad/apps/project-digest/digest.py` → expect
   exactly three: positional `project`, `--format`, `--no-write` (digest.py:31–33) and NO
   `--list`/`--projects`. If a list flag already exists → someone landed this in a race →
   **Abort A2**.
2. `grep -n "def list_project_ids" /Users/davidcruwys/dev/ad/apps/project-digest/lib/config.py`
   → expect one hit (~line 42: `sorted(p.stem for p in PROJECTS_DIR.glob("*.json"))`). Missing →
   the lib was refactored under you → **Abort A2** (same park question, different observed state).
3. `ls /Users/davidcruwys/dev/ad/apps/project-digest/projects/` → expect exactly
   `dark-factory.json`. If ≥2 configs already exist → project #2 landed in a race → **Abort A2**.
4. Baseline BEFORE any edit:
   `cd /Users/davidcruwys/dev/ad/apps/project-digest && python3 digest.py dark-factory --format json --no-write`
   → expect exit 0 and valid JSON with keys `goal`, `needs_you`, `in_flight`, `shipped_recently`,
   `live_now` (verified working 2026-07-06, `needs_you.total_found` was 7). Crashes → **Abort A1**.
5. `grep -n "markers" /Users/davidcruwys/dev/ad/apps/project-digest/lib/needs_you.py` → expect
   hits only on the hardcoded `MARKERS`/`TITLE_MARKERS` lists (~lines 24–35) and NONE reading
   `cfg` — the scan reads only `needs_you.backlog_glob` from config (~line 82). If the config
   `markers` key is already wired → skip Move 2, verify its behaviour instead, and say so in the
   result notes.
6. Project #2 candidate health: `ls /Users/davidcruwys/dev/ad/apps/omi-fetch/README.md` exists;
   `git -C /Users/davidcruwys/dev/ad/apps/omi-fetch rev-parse --show-toplevel` prints the
   omi-fetch path itself (own repo — needed for the git-sourced digest fields);
   `head -10 /Users/davidcruwys/dev/ad/apps/omi-fetch/README.md` → first paragraph after the
   `# OMI Fetch` H1 is prose starting "David Cruwys drives dark-factory partly by voice…"
   (feeds `first-paragraph` goal mode). Also expect NO `backlog/` dir and NO tickets.json there —
   that absence is the point (graceful-degradation exercise). Candidate missing/unusable →
   **Fork F1**.
7. `python3 /Users/davidcruwys/dev/ad/apps/app-registry/query.py app omi-fetch` → expect JSON
   with `"id": "omi-fetch"` (verdict was `running` at authoring). Non-zero exit / unknown id →
   not fatal: LIVE NOW will render `unknown` gracefully; note it and continue (that IS the
   documented degradation path, lib/live.py).
8. The deferred ticket:
   `cat /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/queue/20260704T0630Z-project-digest-list-and-project-2.json`
   → expect `"status": "deferred"` + `"deferred_reason"` quoting David 2026-07-04 ("premature —
   needs universal activity registry first"). Also confirm the orchestrator skips it:
   `grep -n "deferred" /Users/davidcruwys/dev/ad/apps/dark-factory/engine/orchestrator.py` →
   expect the dispatchable() filter (~line 197). If the ticket is GONE from queue/ → check
   `engine/store/done/` and `engine/store/running/` for it; if in done/ → someone closed it →
   **Abort A2**; if in running/ → someone claimed it → **Abort A2**.
9. `git -C /Users/davidcruwys/dev/ad/apps/project-digest status --porcelain` → expect clean or
   only `view/*.html` modified (the view regenerates on every run, even `--no-write` — normal
   churn). Anything else dirty → **Fork F2**.

## Moves

1. **Do:** Add `--list` to `/Users/davidcruwys/dev/ad/apps/project-digest/digest.py`. Concretely:
   change the positional to `parser.add_argument("project", nargs="?", default=None, help=...)`,
   add `parser.add_argument("--list", action="store_true", help="print configured project ids and exit")`.
   At the top of `main()` after `parse_args()`: if `args.list` → for each id from
   `config.list_project_ids()`, load its config via `config.load_config(id)` and print one line
   `"{id}\t{name}\t{path}"` (plain text default); if `--format json` was also passed, instead
   print `json.dumps([{"id":…,"name":…,"path":…}, …], indent=2)`; then `sys.exit(0)`. If
   `args.list` is false and `args.project` is None → `parser.error("project is required unless --list is given")`
   (argparse exits 2 with usage). Touch nothing else in the file — the existing digest path must
   run byte-identical when a project IS given.
   **Expect:** `python3 digest.py --list` exits 0 printing one line containing `dark-factory`;
   `python3 digest.py --list --format json` prints a JSON array parseable by `json.loads`;
   `python3 digest.py` (no args) exits 2 with a usage message; `python3 digest.py dark-factory --no-write`
   still produces the box exactly as in Recon 4.
   **Failure signal:** traceback on any of the four invocations, or the no-args case silently
   does nothing (exit 0).
   **Counter-move:** fix the flag logic (the classic slip: `nargs="?"` makes `args.project` None
   and the old code passes None into `load_config` → guard order matters — handle `--list`, then
   the None-project error, then the normal path). If a second attempt still breaks the normal
   digest path, `git -C /Users/davidcruwys/dev/ad/apps/project-digest checkout -- digest.py` and
   retry from scratch; a third failure → **Abort A1** (the baseline was lying).

2. **Do:** Wire the `needs_you.markers` config override — extension-notes' #1 ranked item
   ("wire that first"). In `lib/needs_you.py`, inside `scan_backlog_files()`: read
   `cfg_markers = cfg.get("needs_you", {}).get("markers")` and use
   `markers = [m.lower() for m in cfg_markers] if cfg_markers else MARKERS` in place of the
   module-level `MARKERS` in the body scan (~line 102). Leave `TITLE_MARKERS` and the
   `## Status`-blocked scan untouched (they are structural conventions, not vocabulary).
   THEN sync `/Users/davidcruwys/dev/ad/apps/project-digest/projects/dark-factory.json`'s
   existing `needs_you.markers` list (5 entries, currently ignored) to the full built-in
   8-entry list from needs_you.py:24–33 — so wiring the key does NOT silently shrink
   dark-factory's recall.
   **Expect:** `python3 digest.py dark-factory --format json --no-write` → `needs_you.total_found`
   equals Recon 4's baseline number (behaviour unchanged for dark-factory); a config WITHOUT a
   `markers` key (omi-fetch's, Move 3) falls back to built-ins.
   **Failure signal:** total_found drops versus baseline, or a traceback in the scan.
   **Counter-move:** diff the config list against needs_you.py's MARKERS (case! the scan
   lower-cases text, so markers must be stored/compared lowercase); fix and re-run. If
   total_found differs for a reason you can prove is legitimate (a backlog file changed under you
   mid-run — check `git -C /Users/davidcruwys/dev/ad/apps/dark-factory log --oneline -3` for
   fresh backlog commits), re-baseline once and proceed; otherwise revert needs_you.py and
   → **Abort A3**.

3. **Do:** Create `/Users/davidcruwys/dev/ad/apps/project-digest/projects/omi-fetch.json`
   (project #2, per README "Adding a project" + Fork F1's default) with exactly:
   ```json
   {
     "id": "omi-fetch",
     "name": "OMI Fetch",
     "path": "/Users/davidcruwys/dev/ad/apps/omi-fetch",
     "registry_id": "omi-fetch",
     "autonomy_stage": "pulse-live",
     "goal_source": {
       "file": "README.md",
       "mode": "first-paragraph"
     }
   }
   ```
   Deliberately OMIT `tickets_json`, `backlog_dir`, `backlog_done_dir`, `needs_you` — omi-fetch
   has none of those conventions (Recon 6); each absent field must report honestly rather than
   error (the README's stated contract, and exactly what this onboarding is meant to prove).
   **Expect:** file exists; `python3 digest.py --list` now prints TWO lines (dark-factory,
   omi-fetch).
   **Failure signal:** --list still shows one project (wrong dir? typo in filename — must be
   `projects/omi-fetch.json`).
   **Counter-move:** fix path/name; `list_project_ids()` is a plain glob of `projects/*.json`,
   there is nothing else to configure.

4. **Do:** Run project #2 end-to-end, all three formats, dry-run:
   `python3 digest.py omi-fetch --no-write` (box), then `--format json --no-write`, then
   `--format md --no-write`. Eyeball each section against reality.
   **Expect:** exit 0 on all three. GOAL = a sentence starting "David Cruwys drives dark-factory
   partly by voice…" (README first paragraph, first sentence, ≤160 chars). NEEDS YOU = 0 items
   (no backlog to scan — honest zero, not an error). SINCE/SHIPPED = real git buckets (omi-fetch
   had 14 commits since 2026-06-20 at authoring; first run uses the 7-day fallback window).
   IN FLIGHT = 0/empty (no backlog, no tickets.json). LIVE NOW = `running` via app-registry (or
   graceful `unknown` per Recon 7). `view/omi-fetch.html` now exists (the HTML twin regenerates
   regardless of format).
   **Failure signal:** traceback in ANY field module (`goal.py`, `needs_you.py`, `in_flight.py`,
   `shipped.py`, `live.py`) on the absent-convention project.
   **Counter-move:** this is the generalization bug the onboarding exists to find — fix the
   crashing lib module to degrade to an honest zero/None for a missing config key (mirror how
   `scan_tickets()` returns `[]` when `tickets_json` is absent), keeping dark-factory's output
   identical (re-run Recon 4's command after every such fix). If a fix would require touching
   `assemble.py`'s windowing or `store.py` → that's a design change, not a degradation fix →
   **Abort A3**.

5. **Do:** Record the honest generalization report — the original ticket's explicit ask. Append
   a short dated section `## Project #2 verdict (omi-fetch, <today's date>)` to
   `/Users/davidcruwys/dev/ad/apps/project-digest/docs/extension-notes.md` stating, for each of
   the three ranked items: **(1) marker-vocabulary override** — wired in Move 2 (real code:
   needs_you.py + config sync) even though omi-fetch itself has no backlog to exercise it;
   **(2) goal-extraction mode** — needed a new mode or not (at authoring, `first-paragraph`
   worked out of the box for omi-fetch's README — confirm from Move 4's actual output);
   **(3) done-convention abstraction** — needed or not (omi-fetch has no done convention; the
   honest-zero path sufficed or it didn't). Plus any Move-4 counter-move fixes you had to make.
   Update the README `## Usage` block with the `--list` line
   (`python3 digest.py --list        # configured projects (add --format json for machine-readable)`).
   **Expect:** two docs touched, additive diffs only.
   **Failure signal:** you're rewriting sections rather than appending.
   **Counter-move:** `git checkout` the file and redo as a pure append/insert.

6. **Do:** Close the deferred engine ticket as superseded. In
   `/Users/davidcruwys/dev/ad/apps/dark-factory/`: edit
   `engine/store/queue/20260704T0630Z-project-digest-list-and-project-2.json` — change
   `"status": "deferred"` to `"status": "done"`, leave `deferred_reason` untouched, and add
   `"result": {"status": "done", "notes": "superseded by wg-t2-03-digest-list-project-2 (war-game portfolio 2026-07-06): --list shipped, omi-fetch onboarded as project #2, needs_you.markers wired. The deferred_reason's larger vision (universal activity registry) remains a separate T2 ticket — this was its groundwork."}`.
   Then `git mv` (or `mv`) the file from `engine/store/queue/` to `engine/store/done/`. First
   verify the old ticket's OWN verify line passes — it demands: `--list` prints ≥2 project ids
   (Move 3's Expect) and project #2 produces a sensible box or documented degradations (Moves
   4–5). Do not close it before both hold.
   **Expect:** queue/ no longer contains `20260704T0630Z-project-digest-*`; done/ does; the JSON
   in done/ parses (`python3 -m json.tool` on it exits 0).
   **Failure signal:** JSON parse error after your edit, or the file exists in both places.
   **Counter-move:** fix the JSON by hand (trailing comma is the usual culprit); a move is
   `mv` + confirm — there is no partial state that can't be re-checked with `ls`.

7. **Do:** Commit and push BOTH repos (separate git repos — verified at authoring).
   project-digest: `digest.py`, `lib/needs_you.py`, `projects/dark-factory.json`,
   `projects/omi-fetch.json`, `view/omi-fetch.html` (+ `view/dark-factory.html` if churned),
   `README.md`, `docs/extension-notes.md`. Message:
   `feat(cli): --list + project #2 (omi-fetch) — markers config wired, degradations documented`.
   dark-factory: the moved queue→done ticket only. Message:
   `chore(engine): close deferred project-digest ticket — superseded by wg-t2-03`.
   Stage ONLY these files; leave any stranger's dirt (Fork F2 Route A) uncommitted.
   **Expect:** both `git push` succeed; `git status --porcelain` in each repo shows none of YOUR
   files left.
   **Failure signal:** push rejected (remote ahead).
   **Counter-move:** `git pull --rebase` then push; on a conflict in a file you touched, resolve
   keeping both intents; on a conflict in a file you did NOT touch → **Abort A4**.

## Forks

**F1 — project #2 candidate.**
Trigger: Recon 6 finds omi-fetch missing, not a git repo, or its README first paragraph no
longer yields a usable goal line — OR David's triage note on this ticket names a different
project.
→ **Route A** (default, no signal to the contrary): **omi-fetch** — it is the "next most
actively-worked repo" the original deferred ticket's own text designates as the default
(14 commits in the prior fortnight at authoring, live in app-registry, and its
no-backlog/no-tickets shape genuinely exercises graceful degradation).
→ **Route B** (trigger fired): fall back to **app-registry**
(`/Users/davidcruwys/dev/ad/apps/app-registry`) — same sibling family, own repo, tracked in its
own registry under id `app-registry`; re-run Recon 6's checks against it first (README
first-paragraph shape UNVERIFIED at authoring — if its README opens with a blockquote or status
line, use `heading-paragraph` mode against its first `##` heading instead). If David named a
specific project, that overrides both routes; re-run Recon 6 against his pick and apply the same
config recipe.

**F2 — project-digest tree dirty beyond generated view files.**
Trigger: Recon 9 shows modifications other than `view/*.html`.
→ **Route A** (dirt in files this ticket never touches): proceed; stage only your files at
Move 7; mention the stranger's dirt in the result notes.
→ **Route B** (dirt in `digest.py`, `lib/config.py`, `lib/needs_you.py`, or `projects/*.json`):
someone is mid-change on your exact seam → **Abort A3**.

## Assumptions ledger

1. **Closing the deferred ticket does not defy David's 2026-07-04 deferral.** He deferred it as
   "premature — needs universal activity registry first", but the 2026-07-06 war-game interview
   (decisions.md Q1/Q4) ratified the T2 track whose path-map seed explicitly includes
   "digest.py --list + project #2 onboarding (unblocks the deferred queue ticket)". The
   supersede note (Move 6) preserves his reasoning and re-points the larger vision at its own
   T2 ticket. **If false** (you find a post-2026-07-06 edit to the queue ticket re-asserting the
   deferral — check `git -C /Users/davidcruwys/dev/ad/apps/dark-factory log --oneline -- engine/store/queue/20260704T0630Z-project-digest-list-and-project-2.json`
   for commits after 07-06): do Moves 1–5 and 7 anyway (the code work stands alone), SKIP Move 6,
   and park the closure question to
   `engine/store/needs-decision/wg-t2-03-digest-list-project-2.json`.
2. **omi-fetch as project #2 is acceptable without David's explicit pick.** The original ticket
   says "David's call which one, default to the next most actively-worked repo if not specified"
   — omi-fetch is that repo and no pick was recorded anywhere authoring-time recon looked.
   **If false** (David objects at triage or in the result review): swapping is a 5-minute
   config-file change; note in the result that `projects/omi-fetch.json` can be deleted and the
   recipe re-applied — no park needed, no code depends on which project #2 is.
3. **Wiring `needs_you.markers` is in-scope for "onboard project #2"** even though omi-fetch has
   no backlog to exercise it. Plausible: the original ticket's prompt explicitly says to follow
   extension-notes' ranked list, whose #1 says "wire that first when adding project #2".
   **If false** (the wiring turns out to fight other in-flight work on needs_you.py): drop
   Move 2, note the skip in extension-notes, continue — `--list` + onboarding stand alone.
4. **`--format json` doubling as `--list`'s output switch won't confuse the existing CLI.**
   Plausible: `--format` already exists and `--list` exits before the digest path runs.
   **If false** (a consumer emerges that parses `--list` plain text and breaks): the plain-text
   default is the compatibility surface; JSON is additive. No action beyond noting it.

## Abort conditions

- **A1 — baseline broken.** Recon 4's untouched dark-factory run crashes, or Move 1's
  counter-move fails three times. Park: write
  `engine/store/needs-decision/wg-t2-03-digest-list-project-2.json` (in the dark-factory repo)
  with `{"ticket": "wg-t2-03-digest-list-project-2", "question": "project-digest baseline is broken before/despite minimal edits — digest.py dark-factory crashes. Fix digest first (separate ticket) or debug here?", "observed": "<the traceback>"}`.
  Leave this war game's engine ticket in `running/`. Never build on a broken baseline.
- **A2 — the work already landed (race).** A `--list` flag exists (Recon 1), ≥2 project configs
  exist (Recon 3), `list_project_ids` is gone (Recon 2), or the deferred ticket already moved out
  of queue/ (Recon 8). Park with question: "wg-t2-03's target state partially/fully exists
  (found: <what and where>). Verify-and-close against the existing implementation, or redo per
  the war game?" Do not duplicate or rewrite whatever landed.
- **A3 — seam conflict or design-change pressure.** Fork F2 Route B (concurrent edits on
  digest.py/config.py/needs_you.py), Move 2's unexplained recall change, or Move 4 demanding
  changes beyond honest-zero degradation (assemble.py windowing / store.py). Park with the
  `git status` / diff evidence and the question "who owns this seam right now / is this
  degradation actually a redesign?".
- **A4 — rebase conflict in a file this ticket never touched.** Park with the conflicting paths;
  do not resolve other people's conflicts.

## Verification

```bash
PD=/Users/davidcruwys/dev/ad/apps/project-digest
DF=/Users/davidcruwys/dev/ad/apps/dark-factory

# 1. --list works, both formats, and no-args errors cleanly
python3 $PD/digest.py --list                                  # exit 0, ≥2 lines, contains dark-factory AND the project-#2 id
python3 $PD/digest.py --list | wc -l                          # → ≥ 2
python3 $PD/digest.py --list --format json | python3 -c "import json,sys; a=json.load(sys.stdin); assert len(a)>=2 and all('id' in p and 'path' in p for p in a); print('list-json ok', [p['id'] for p in a])"
python3 $PD/digest.py >/dev/null 2>&1; test $? -eq 2 && echo "no-args errors correctly"

# 2. Project #2 digests in all three formats, dry-run
python3 $PD/digest.py omi-fetch --no-write            > /dev/null && echo box-ok
python3 $PD/digest.py omi-fetch --format md --no-write > /dev/null && echo md-ok
python3 $PD/digest.py omi-fetch --format json --no-write | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['project_id']=='omi-fetch' and d['goal']['text']; print('goal:', d['goal']['text'][:60])"
ls $PD/view/omi-fetch.html                                    # exists (HTML twin)

# 3. markers config wired, dark-factory recall preserved
grep -c 'needs_you.*markers\|cfg_markers' $PD/lib/needs_you.py            # → ≥ 1 (the cfg read)
python3 $PD/digest.py dark-factory --format json --no-write | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['needs_you']['total_found'] >= 1; print('needs_you', d['needs_you']['total_found'])"

# 4. Deferred ticket closed as superseded
ls $DF/engine/store/queue/  | grep -c "20260704T0630Z-project-digest"     # → 0
ls $DF/engine/store/done/   | grep -c "20260704T0630Z-project-digest"     # → 1
python3 -m json.tool $DF/engine/store/done/20260704T0630Z-project-digest-list-and-project-2.json > /dev/null && echo done-ticket-json-ok
grep -c "superseded by wg-t2-03" $DF/engine/store/done/20260704T0630Z-project-digest-list-and-project-2.json  # → 1
grep -c "deferred_reason" $DF/engine/store/done/20260704T0630Z-project-digest-list-and-project-2.json         # → 1 (history preserved)

# 5. Honest report + README landed
grep -c "Project #2 verdict" $PD/docs/extension-notes.md      # → 1
grep -c "\-\-list" $PD/README.md                              # → ≥ 1

# 6. Negative checks — what must NOT have changed
git -C /Users/davidcruwys/dev/ad/apps/omi-fetch status --porcelain | wc -l   # → 0 new dirt from this ticket (digest is read-only on targets; compare against Recon 6 if it was already dirty)
python3 $PD/digest.py dark-factory --no-write > /dev/null && echo df-still-ok # original project untouched behaviourally
ls $PD/store/last-briefing/ | grep -c omi-fetch               # → 0 (every project-#2 run used --no-write; dark-factory.json may exist from before)

# 7. Both repos committed and pushed
git -C $PD status --porcelain | grep -v "^ M view/" | wc -l   # → 0 (only view churn tolerated)
git -C $PD log --oneline -1                                   # shows the --list/project-#2 commit
git -C $DF log --oneline -- engine/store/done/20260704T0630Z-project-digest-list-and-project-2.json | head -1   # shows the close commit
```

## Executor notes (sonnet)

- **Scope fence.** Do NOT build `--all` / a multi-project briefing loop (explicit v1 non-goal in
  project-digest's README; the loop is the BA agent's job — a different T2 ticket). Do NOT build
  the universal activity registry (the deferred_reason's vision — its own T2 ticket). Do NOT add
  any LLM call anywhere (v1 is LLM-free by design). Do NOT write into
  `/Users/davidcruwys/dev/ad/apps/omi-fetch/` — the digest reads target projects strictly
  read-only. Do NOT touch `lib/assemble.py`, `lib/store.py`, or any engine/*.py in dark-factory.
  Do NOT onboard a third project.
- **The rabbit hole: `docs/morning-briefing-vision.md`.** It's a pointer to the big
  activity-across-everything vision (canonical copy in dark-factory/docs/). Reading it will
  tempt you to "just start" the activity registry or a cross-project loop. Skip it entirely —
  this ticket is deliberately the 2-hour groundwork slice, and the deferral you're closing was
  ABOUT not conflating the two.
- **Style:** project-digest is stdlib-only, small pure functions, honest degradation over clever
  inference ("a config with a badly-worded source doc will read badly here too, on purpose" —
  goal.py's own header). Match that: absent config key → honest zero, never a guess. Markers
  compare lowercase (the scan lower-cases file text).
- **Prefer parking over guessing** on any race signal (A2) — five other war-game tickets touch
  project-digest's neighbourhood this cycle (T1-04 extends `lib/shipped.py`; it is compatible
  with this ticket but if you find half-landed edits, park, don't merge by guess).
- **The honest-report move (5) is not optional garnish** — "note honestly which of those three
  actually needed real code vs worked out of the box" is a named deliverable of the original
  ticket, and extension-notes.md is the repo's designated learning artifact.
