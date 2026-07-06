# T2-05 — Feed layer into the briefing

| field | value |
|---|---|
| ticket | wg-t2-05-briefing-feed-layer |
| track / size / priority | T2 Producer/BA / M / normal |
| executor | sonnet Swagger via engine |
| depends_on | wg-t1-04-c4-return-leg (file-collision serialization — see Fork F3) |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Fold the factory's live ticket state into the morning briefing (feed layer — step 3 of the
dependency chain in `docs/morning-briefing-vision.md`, field table in
`docs/daily-operating-model.md` §2 line ~78: *NEEDS YOU ← … + needs-decision/*.json · IN FLIGHT
← tickets in-progress*). Today `~/dev/ad/apps/project-digest` computes NEEDS-YOU only from
backlog markers + tickets.json `open` fields, and IN-FLIGHT only from backlog files +
tickets.json states — the engine store (`dark-factory/engine/store/`) and Linear are invisible
to it. Done means: **(a)** unanswered `engine/store/needs-decision/*.json` files (no matching
`decisions/<same-name>.json`) surface as top-ranked NEEDS-YOU candidates; **(b)** engine
`queue/` + `running/` tickets appear as an `engine` sub-block of IN-FLIGHT; **(c)** a Linear
source module exists that feeds assigned issues into both fields when an API key is available
and degrades to an honest "not configured" state when it isn't (no key exists on this machine
as of authoring — Fork F1); all three digest formats (json/md/box) plus the HTML twin render
the new data, additively, with zero changes to existing keys.

## Locked context

- **Q4 (decisions.md):** everything through the engine — this ticket is written for sonnet
  Swagger dispatch.
- **No `-p`/headless/SDK ever; interactive `claude` only** — moot here (nothing in this build
  spawns Claude); the digest stays LLM-free plain Python (its own v1 design law, see
  `project-digest/lib/needs_you.py` header).
- **HALT/BACKOFF respected implicitly** — this ticket adds READ-ONLY consumers of the engine
  store; it must not add any dispatch, write, or mutation path into `queue/`, `running/`,
  `done/`, or `decisions/`. The one permitted engine-store write is the executor (not the
  digest code) parking a question file in `needs-decision/` per Fork F1-B / the abort protocol.
- **Store is a growing ledger** — never modify or delete real files in the engine store. The
  only exception is the clearly-marked DUMMY file you create and remove in Move 4.
- **No YLO/POEM work** — out of scope entirely.

## Recon (verify before any work)

Docs lag code. Run every check; each replaces doc-trust. Repo roots:
`DF=/Users/davidcruwys/dev/ad/apps/dark-factory`, `PD=/Users/davidcruwys/dev/ad/apps/project-digest`.

1. Baseline the digest untouched:
   `python3 $PD/digest.py dark-factory --format json --no-write` → expect valid JSON whose
   top-level keys include `needs_you` (with `items` + `total_found`) and `in_flight` (with
   `backlog` + `tickets` sub-dicts). As of authoring: `total_found` = 7, top item score 100 =
   the design-lint placement OPEN QUESTION; `in_flight` = backlog 35 / tickets 0. Numbers may
   have drifted — the SHAPE is the bar. If this run crashes → **Abort A1**.
2. `ls $DF/engine/store/queue $DF/engine/store/running $DF/engine/store/needs-decision $DF/engine/store/decisions`
   → expect all four directories to exist (as of authoring: queue holds exactly 1 deferred
   ticket `20260704T0630Z-project-digest-list-and-project-2.json`; running/ empty;
   needs-decision/ + decisions/ hold only `.gitkeep`). Any directory missing → **Abort A2**.
3. Confirm the HITL answered/unanswered pairing before you encode it: read
   `$DF/engine/store/queue/.CONVENTION.md` and grep `$DF/engine/orchestrator.py` around lines
   ~57 and ~601–630 → expect `NEEDS, DEC = …("needs-decision", "decisions")` and the loop that
   treats `decisions/<tid>.json` as the answer to `needs-decision/<tid>.json`. If that pairing
   is gone → the HITL contract moved → **Abort A2**.
4. `grep -n "engine\|linear" $PD/lib/needs_you.py $PD/lib/in_flight.py $PD/lib/assemble.py`
   → expect NO hits (neither feed exists yet). If an engine or Linear feed already exists →
   someone landed T2-05 in a race → **Abort A3**.
5. T1-04 landing check (it shares your exact files):
   `grep -n "engine_done_in_window" $PD/lib/shipped.py` and
   `grep -n "engine_done_dir" $PD/projects/dark-factory.json` → **Fork F3** routes on the
   result. Expected (depends_on honoured): both present. Either way, note the result — it
   changes nothing except where you add your config key and how careful Move 3's renderer
   edits must be.
6. `git -C $PD status --porcelain` → expect clean or only `view/dark-factory.html` modified
   (generated on every digest run — normal churn). Dirt in `lib/needs_you.py`,
   `lib/in_flight.py`, `lib/assemble.py`, `lib/box.py`, `lib/view.py`, `lib/render_md.py`, or
   `projects/dark-factory.json` → **Fork F2**.
7. Linear credential hunt (decides Fork F1): `printenv LINEAR_API_KEY`;
   `cat ~/.config/appydave/linear.json 2>/dev/null`; `grep -i linear $DF/.env 2>/dev/null`;
   `grep -rn "LINEAR_API_KEY" $PD/ 2>/dev/null` → as of authoring ALL come back empty (Linear
   exists on this machine only as a claude.ai OAuth MCP in `~/.claude.json` — unusable from
   plain Python). Empty → F1 Route B. Any hit → F1 Route A; record where the key lives.
8. Renderer surface map: `grep -n "in_flight\|needs_you" $PD/lib/box.py $PD/lib/view.py $PD/lib/render_md.py`
   → expect `box.py` `_fmt_needs_you`/`_fmt_in_flight` (~lines 18–45), `render_md.py` NEEDS
   YOU + IN FLIGHT sections (~lines 16–41), `view.py` `_needs_you_html` + `in_flight_html`
   (~lines 23–59). These are the exact seams Move 3 extends — additive only.

## Moves

1. **Do:** Build the engine feed. (i) Add `"engine_store": "/Users/davidcruwys/dev/ad/apps/dark-factory/engine/store"`
   to `$PD/projects/dark-factory.json` (absolute path, sitting beside the existing keys — and
   beside `engine_done_dir` if F3 found it; note `engine_done_dir` is project-relative while
   this key is absolute by design: the engine store is the factory's, not necessarily inside
   the digested project). (ii) Create `$PD/lib/engine_feed.py`, stdlib-only, mirroring the
   defensive idioms of `in_flight.py`/`needs_you.py`, with two functions:
   `needs_decision_candidates(cfg)` — returns `[]` when `engine_store` absent from cfg or the
   dir missing; else lists `needs-decision/*.json` (skip `.gitkeep`), drops any file whose
   same-named twin exists in `decisions/`, and for each survivor emits a NEEDS-YOU candidate
   dict in the established shape: `title` = ticket `question`[:80] or `title` or `ticket` or
   filename stem (per-file `try/except json` → filename stem), `file` =
   `"engine/store/needs-decision/<fname>"`, `score` = **110** (a blocked/parked worker
   outranks every doc marker — design ruling, see Assumption 3), `reason` =
   `"unanswered engine decision (HITL/parked)"`, `snippet` = `question`[:200] if present.
   `in_flight(cfg, top_n=5)` — returns `{"configured": False, "queue_count": 0, "running_count": 0, "top": [], "error": None}`
   when unconfigured; else counts `queue/*.json` and `running/*.json` (skip `.gitkeep`,
   per-file try/except) and fills `top` with up to `top_n` titles (same title fallback chain),
   queue first then running, `configured: True`. Missing dir with key set → `configured: True`
   + `error` string + zeros.
   **Expect:** `python3 -c "import sys; sys.path.insert(0,'$PD'); from lib import engine_feed, config; cfg=config.load_config('dark-factory'); print(engine_feed.in_flight(cfg)); print(len(engine_feed.needs_decision_candidates(cfg)))"`
   prints a configured=True dict whose `queue_count` equals `ls $DF/engine/store/queue/*.json | wc -l`
   and candidate count 0 (needs-decision/ empty as of authoring — if war-game promotion has
   since parked real items there, a matching non-zero count is equally a pass).
   **Failure signal:** traceback, or counts disagree with `ls`.
   **Counter-move:** fix the module (usual culprit: counting `.gitkeep` or forgetting the
   decisions/ twin-check). If counts still disagree after a fix because the store layout
   itself differs from Recon 2's finding → **Abort A2**.

2. **Do:** Wire the feed in. (i) In `$PD/lib/needs_you.py` `collect()`: add
   `from lib import engine_feed` (top of file, matching existing import style) and extend the
   candidate pool — `candidates = scan_backlog_files(cfg) + scan_tickets(cfg) + engine_feed.needs_decision_candidates(cfg)`.
   Touch nothing else in the file (cap-3, dedup-by-file, sort all stay). (ii) In
   `$PD/lib/assemble.py` `build()`: add `"engine": engine_feed.in_flight(cfg)` as a third key
   inside the existing `in_flight` dict (after `tickets`). Do NOT touch `recommend_focus`
   (it reads `backlog`/`tickets` keys, which are unchanged).
   **Expect:** `python3 $PD/digest.py dark-factory --format json --no-write` runs clean;
   `in_flight.engine.configured` is `true`; `needs_you.total_found` ≥ Recon 1's baseline;
   every baseline top-level key still present.
   **Failure signal:** KeyError/ImportError, or a baseline key vanished.
   **Counter-move:** circular-import is the likely trap (engine_feed must import nothing from
   needs_you/assemble); flatten the import. If `recommend_focus` broke, you touched keys you
   were told not to — revert `assemble.py` and redo additively.

3. **Do:** Render it, additive only, uniform rule: **a sub-line renders iff its sub-dict has
   `configured: True`** (projects without the config key see zero change). (i) `box.py`
   `_fmt_in_flight`: when engine configured, append line
   `f"{e['queue_count']} queued + {e['running_count']} running in engine"` (append
   `f" — {'; '.join(e['top'][:2])}"` when top non-empty; on `error`, render
   `f"engine feed error: {e['error']}"` instead). (ii) `render_md.py` IN FLIGHT section: same
   content as a third `- Engine: …` bullet. (iii) `view.py` `in_flight_html`: a third `<div>`
   with the same text. NEEDS-YOU needs no renderer work (engine candidates already flow
   through the generic item shape). Do not touch `_fmt_shipped`/shipped HTML (T1-04's seam).
   **Expect:** `--format box`, `--format md` both render the engine line;
   `view/dark-factory.html` regenerates containing "running in engine"; `--format json`
   unchanged from Move 2.
   **Failure signal:** box border misalignment (see extension-notes: don't "fix" unicode width
   by counting bytes), or a crash in any format.
   **Counter-move:** keep the engine line pure-ASCII (no new glyphs) and let `_append_field`
   do the wrapping — the box arithmetic is already solved for plain text. Fix the renderer,
   never the data shape.

4. **Do:** Dogfood-prove the NEEDS-YOU engine path end-to-end with a marked dummy. Create
   `$DF/engine/store/needs-decision/wg-DUMMY-t2-05-feed-verify.json` containing
   `{"ticket":"wg-DUMMY-t2-05-feed-verify","question":"DUMMY — feed-layer verification, ignore and delete","requested_by":"wg-t2-05 executor"}`.
   Run `python3 $PD/digest.py dark-factory --format json --no-write`.
   **Expect:** `needs_you.items[0].file` == `"engine/store/needs-decision/wg-DUMMY-t2-05-feed-verify.json"`
   (score 110 beats the standing 100-score backlog item — deterministic top-1) and
   `total_found` = baseline + 1.
   **Failure signal:** dummy absent from items, or present but not ranked first.
   **Counter-move:** absent → the twin-check or glob in Move 1 is wrong, fix and re-run;
   present-but-not-first → the sort or score constant is wrong, fix and re-run. If it still
   fails after one fix cycle → **Abort A3** (something structural you don't understand is
   intercepting the pipeline — park, don't thrash).
   **Cleanup (mandatory, same move):** `rm $DF/engine/store/needs-decision/wg-DUMMY-*.json`,
   re-run the digest, confirm the dummy is gone from output and
   `ls $DF/engine/store/needs-decision/ | grep -c DUMMY` → 0.

5. **Do:** Build the Linear source, `$PD/lib/linear_source.py`, stdlib-only (`urllib.request`,
   `json`, `os`). Key lookup order: `os.environ.get("LINEAR_API_KEY")`, then
   `~/.config/appydave/linear.json` field `api_key` (try/except missing/bad file). No key →
   `{"configured": False, "count": 0, "top": [], "needs_you_candidates": [], "error": "no LINEAR_API_KEY env var or ~/.config/appydave/linear.json"}`.
   With a key: POST to `https://api.linear.app/graphql`, header `Authorization: <key>`,
   `Content-Type: application/json`, timeout 10s, query
   `{"query": "{ viewer { assignedIssues(first: 25, filter: { state: { type: { in: [\"triage\", \"unstarted\", \"started\"] } } }) { nodes { identifier title priority url state { name type } } } }"}`.
   Split the nodes: `state.type == "started"` → IN-FLIGHT (`count`, `top` =
   `"<identifier> — <title>"`, cap 5); `priority == 1` (Urgent) and not started → NEEDS-YOU
   candidates (`title` = `"<identifier> — <title>"`, `file` = the issue `url`, `score` = 85,
   `reason` = `"urgent Linear issue assigned to David"`, `snippet` = state name). ANY network,
   HTTP, or schema error → `configured: True`, zeros, `error` = one-line string — the digest
   must brief fine offline, never crash. Wire it: `needs_you.collect()` gains
   `+ linear_source.needs_you_candidates(cfg)` (make that a thin accessor returning the
   candidates list) and `assemble.build()` gains `"linear": linear_source.in_flight(cfg)`
   inside `in_flight` (thin accessor over the same single fetch — fetch once per build, not
   twice: memoize on the cfg dict or return both shapes from one `collect(cfg)` and split in
   the accessors). Renderers: same configured-gated third/fourth line as Move 3
   (`f"{n} Linear issue(s) in progress: …"`).
   **Expect:** digest runs clean in all formats; with no key (authoring state)
   `in_flight.linear.configured` == `false` and NO Linear line appears in box/md/html.
   **Failure signal:** digest hangs (missing timeout), crashes, or a "not configured" Linear
   line leaks into the rendered output.
   **Counter-move:** enforce the 10s timeout and the configured-gate in renderers. Do NOT
   attempt to reach Linear through the claude.ai MCP, OAuth flows, or any browser automation —
   key-or-degrade is the whole v1 contract (see Executor notes).

6. **Do:** Route on **Fork F1** (Recon 7's result). **Route B (expected — no key):** park the
   provisioning question so the factory's own front door surfaces it: write
   `$DF/engine/store/needs-decision/wg-t2-05-linear-key.json` containing
   `{"ticket":"wg-t2-05-linear-key","question":"Feed layer (T2-05) shipped with the Linear source degraded: no LINEAR_API_KEY on this machine (Linear is claude.ai-MCP OAuth only). Provision a personal API key (env LINEAR_API_KEY or ~/.config/appydave/linear.json {\"api_key\":\"...\"}) to activate it, or rule Linear as MCP-lane-only and I'll strip the module. Which?","requested_by":"wg-t2-05 executor (2026-07-06 war game)","context":"lib/linear_source.py in project-digest is built and wired; it activates on next digest run once a key exists. No code change needed."}`.
   This is **park-and-proceed, not an abort** — the ticket still completes; the file is a
   decision request that the feature you just built will itself surface. Re-run the digest.
   **Route A (key found):** no park file; instead live-verify —
   `in_flight.linear.configured` == `true`, `error` == `null`, and counts are plausible
   against a manual spot-check of David's Linear (list the fetched identifiers in your result
   notes).
   **Expect (B):** `needs_you.items[0].file` == `"engine/store/needs-decision/wg-t2-05-linear-key.json"`
   — the dogfood loop closed: the briefing's newest source is announcing its own missing
   credential. **Expect (A):** the assertions above.
   **Failure signal (B):** the park file doesn't surface top-1. **(A):** HTTP 400/schema error
   from the GraphQL query.
   **Counter-move (B):** same as Move 4's counter-move. **(A):** the query shape drifted —
   adapt using Linear's error message (their GraphQL errors name valid fields); two failed
   adaptations → fall back to Route B behaviour (degrade + park a file noting the schema
   mismatch instead of the missing key) and continue; never burn hours on API archaeology.

7. **Do:** Full-format regression pass:
   `python3 $PD/digest.py dark-factory --format json --no-write | python3 -c "import json,sys; d=json.load(sys.stdin); s=d['in_flight']; assert s['engine']['configured'] is True; assert 'linear' in s; assert {'backlog','tickets'} <= set(s); assert d['needs_you']['total_found'] >= 1; print('json-ok')"`
   then `--format md --no-write | grep -c "engine"` (≥1), `--format box --no-write` (renders,
   engine line present), and confirm `view/dark-factory.html` contains "running in engine".
   **Expect:** all four pass.
   **Failure signal:** any assertion trips.
   **Counter-move:** the failing surface names the move to revisit (json → Moves 1–2/5;
   md/box/html → Move 3/5 renderers). One fix cycle each; a second failure on the same
   surface → **Abort A3**.

8. **Do:** Documentation, tightly fenced: (i) append a `## Feed layer (engine + Linear)`
   section to `$PD/README.md` — the two config keys (`engine_store` absolute,
   Linear key locations), the three sub-dict shapes, the configured-gate render rule, the
   110/85 score rationale, and the degradation contract; (ii) in
   `$DF/docs/morning-briefing-vision.md`, on dependency-chain item 3 ("**Feed layer**…",
   line ~17), append a one-line status suffix only:
   `— ✅ engine tickets + needs-decision live, Linear built-but-degraded pending key, 2026-07-06 (wg-t2-05)`.
   Annotate ONLY the dark-factory copy (it is canonical; project-digest's
   `docs/morning-briefing-vision.md` is the pre-move duplicate — leave it).
   **Expect:** two files changed, small diffs.
   **Failure signal:** you restructured either doc.
   **Counter-move:** `git checkout` the file and redo as pure addition/suffix.

9. **Do:** Commit and push BOTH repos (separate git repos — verified at authoring).
   project-digest: `lib/engine_feed.py`, `lib/linear_source.py`, `lib/needs_you.py`,
   `lib/in_flight.py` (only if touched — Move 2 puts the engine key in assemble, so likely
   untouched), `lib/assemble.py`, `lib/box.py`, `lib/render_md.py`, `lib/view.py`,
   `projects/dark-factory.json`, `README.md`, `view/dark-factory.html` (generated, tracked —
   fine). Message: `feat(feeds): engine tickets + needs-decision + Linear into NEEDS-YOU/IN-FLIGHT (dark-factory T2-05)`.
   dark-factory: `docs/morning-briefing-vision.md` + (Route B only)
   `engine/store/needs-decision/wg-t2-05-linear-key.json` (the store is git-tracked — commit
   the park file; it is part of the ledger). Message:
   `feat(briefing): feed layer live — engine store folded into morning briefing (wg-t2-05)`.
   Stage only your files; check `git status` for strangers first (Fork F2 discipline).
   **Expect:** both `git push` succeed; nothing of yours left in `git status --porcelain`.
   **Failure signal:** push rejected (remote ahead).
   **Counter-move:** `git pull --rebase` then push; conflict in a file you touched → resolve
   keeping both intents; conflict in a file you did NOT touch → **Abort A4**.

## Forks

**F1 — Linear credential present vs absent.**
Trigger: Recon 7's credential hunt.
→ **Route A** (key found anywhere): build + live-verify against the real API (Move 6-A);
no park file.
→ **Route B** (nothing found — the authoring-time state): build degraded, park the
provisioning question in `needs-decision/`, and let the new feed surface it (Move 6-B). The
ticket completes either way.

**F2 — project-digest tree dirty beyond the generated view file.**
Trigger: Recon 6 shows modifications other than `view/dark-factory.html`.
→ **Route A** (dirt in files you won't touch): proceed; stage only your files at Move 9;
mention the stranger's changes in your result notes.
→ **Route B** (dirt in `lib/needs_you.py`, `lib/in_flight.py`, `lib/assemble.py`, a renderer,
or `projects/dark-factory.json`): someone is mid-change on your exact seam → **Abort A3**.

**F3 — T1-04 (C4 return leg) landed or not.**
Trigger: Recon 5's greps.
→ **Route A** (both hits — expected, since depends_on should have serialized it): your config
key sits beside `engine_done_dir`; renderer files already carry T1-04's shipped lines — your
Move 3 edits are additive next to them; zero interaction otherwise (T1-04 reads `done/`, you
read `queue/`/`running/`/`needs-decision/`).
→ **Route B** (no hits — T1-04 cancelled or reordered): proceed exactly per the moves; do NOT
touch `lib/shipped.py` or add any `done/` reading (that is T1-04's seam, whenever it runs);
note in your result that dispatch order diverged from depends_on.

## Assumptions ledger

1. **No Linear API key exists on this machine.** Verified at authoring (env,
   `~/.config/appydave/` — only apps/bank/locations/etc. JSONs, no linear.json —
   `dark-factory/.env`, project-digest tree all empty; Linear appears only as a claude.ai
   OAuth MCP entry in `~/.claude.json`, unreachable from plain Python). If false → Fork F1
   Route A, live-verify instead of parking.
2. **Free-standing question files in `engine/store/needs-decision/` are inert to the engine.**
   Verified at authoring by reading the code: `orchestrator.py` (~601–630) inspects
   `needs-decision/<tid>.json` only for tids in its own live `agents` dict; `status.py` never
   reads the dir; `wake.py` scans `queue/` only. It is also the spec-blessed abort-park
   location for every war game in this portfolio. If a future engine change starts choking on
   the file → remove `wg-t2-05-linear-key.json`, put the same question in a
   `backlog/` note instead, and record the incompatibility in your result notes.
3. **Score 110 for engine needs-decision (above the 100 title-marker ceiling) and 85 for
   urgent Linear issues is the right default ranking.** Plausible: an unanswered HITL file
   means a worker is (or was) literally blocked mid-task — more urgent than a standing doc
   marker; Linear urgency sits between tickets.json `open` (80) and `Decision owner:` (90).
   David has not ratified the ordering; it is presentation-only (the cap-3 and all sources
   are unchanged). If David objects at triage → each is a one-line constant; note where.
4. **Viewer-assigned issues are the right v1 Linear slice.** No team/project scoping for
   dark-factory exists anywhere on disk, and the briefing is David-personal by design. If
   David wants team-wide or per-project filters → a `linear` config block extension later;
   note the request in `needs-decision/` only if he raises it.
5. **Phase 5 promotion honours depends_on** (T1-04 dispatches before this ticket). If not →
   Fork F3 Route B covers the out-of-order case without loss.

## Abort conditions

- **A1 — digest baseline broken.** Recon 1's untouched run crashes. Park: write
  `engine/store/needs-decision/wg-t2-05-briefing-feed-layer.json` with
  `{"ticket":"wg-t2-05-briefing-feed-layer","question":"project-digest baseline is broken before any T2-05 edit (traceback attached). Fix digest first (separate ticket) or proceed differently?","observed":"<traceback>"}`.
  Leave the ticket in `running/`.
- **A2 — engine store layout or HITL contract shifted.** Recon 2/3 finds directories missing
  or the needs-decision/decisions pairing gone, or Move 1's counts irreconcilably disagree
  with `ls`. Park with what you found; never guess a new store schema.
- **A3 — seam conflict or unexplained pipeline failure.** Fork F2 Route B (concurrent edits on
  the exact files), Recon 4 (feed already exists — a race landed T2-05), or a second failed
  fix cycle in Moves 4/7. Park with `git status` output / the failing observation and the
  question "who owns this seam right now?".
- **A4 — rebase conflict in a file this ticket never touched.** Park with the conflicting
  paths; do not resolve other people's conflicts.

## Verification

All paths absolute; `DF=/Users/davidcruwys/dev/ad/apps/dark-factory`,
`PD=/Users/davidcruwys/dev/ad/apps/project-digest`.

```bash
# 1. Modules exist, digest healthy, additive shape intact
ls $PD/lib/engine_feed.py $PD/lib/linear_source.py
python3 $PD/digest.py dark-factory --format json --no-write | python3 -c "
import json,sys; d=json.load(sys.stdin)
f=d['in_flight']; assert f['engine']['configured'] is True, f
assert 'linear' in f and 'backlog' in f and 'tickets' in f
assert isinstance(f['engine']['queue_count'], int) and isinstance(f['engine']['running_count'], int)
assert all(k in d for k in ('goal','needs_you','since_last_looked','shipped_recently','live_now'))
print('shape-ok; engine queue/running =', f['engine']['queue_count'], f['engine']['running_count'])"

# 2. Engine counts agree with the store on disk (dynamic — no fixed numbers)
python3 - <<'EOF'
import json, subprocess, os, glob
out = subprocess.run(["python3","/Users/davidcruwys/dev/ad/apps/project-digest/digest.py",
                      "dark-factory","--format","json","--no-write"], capture_output=True, text=True)
e = json.loads(out.stdout)["in_flight"]["engine"]
S = "/Users/davidcruwys/dev/ad/apps/dark-factory/engine/store"
assert e["queue_count"]   == len(glob.glob(S+"/queue/*.json")),   "queue mismatch"
assert e["running_count"] == len(glob.glob(S+"/running/*.json")), "running mismatch"
print("counts-in-sync")
EOF

# 3. All render surfaces carry the feed
python3 $PD/digest.py dark-factory --format md  --no-write | grep -ci "engine"        # ≥ 1
python3 $PD/digest.py dark-factory --format box --no-write | grep -c  "in engine"     # ≥ 1
grep -c "running in engine" $PD/view/dark-factory.html                                 # ≥ 1

# 4. Fork-dependent Linear check — run the branch that applied:
#    Route B (no key): the parked question is the top NEEDS-YOU item (dogfood closed)
python3 $PD/digest.py dark-factory --format json --no-write | python3 -c "
import json,sys; d=json.load(sys.stdin)
items=d['needs_you']['items']
assert any('wg-t2-05-linear-key' in i['file'] for i in items[:1]), items[:1]
assert d['in_flight']['linear']['configured'] is False
print('routeB-ok')"
#    Route A (key): configured true, no error, park file absent
#    -> in_flight.linear.configured == true and error == null; ls of needs-decision/ has no wg-t2-05-linear-key.json

# 5. Negative checks — what must NOT have changed
ls $DF/engine/store/needs-decision/ | grep -ci DUMMY                                   # → 0
grep -rn "claude\b" $PD/lib/engine_feed.py $PD/lib/linear_source.py | grep -cv "^$"    # → 0 (digest stays LLM-free)
grep -c "def collect" $PD/lib/needs_you.py                                             # → 1 (cap-3 collect intact)
git -C $DF diff HEAD~2 --name-only -- engine/store/queue engine/store/running engine/store/done | grep -cv needs-decision # → 0 real store files touched by your commits
python3 $DF/engine/status.py > /dev/null && echo engine-status-ok                      # engine tooling unbothered

# 6. Both repos committed and pushed
git -C $PD log --oneline -1     # shows the feat(feeds) commit
git -C $DF log --oneline -1     # shows the feat(briefing) commit
git -C $PD status --porcelain   # empty (or untouched stranger files per F2-A, named in result notes)
```

## Executor notes (sonnet)

- **Scope fence.** In project-digest do NOT touch `lib/shipped.py`, `lib/goal.py`,
  `lib/git_source.py`, `lib/store.py`, `lib/live.py`, or `assemble.py`'s windowing/briefing_n
  logic. In dark-factory do NOT edit ANY `engine/*.py` file — this ticket only READS the
  store — and never modify/delete real store files (the DUMMY and, Route B, the one park file
  are the only writes). Do not add a second project config, `--list`, or activity-registry
  work (T2-02/T2-03/T2-04's seams).
- **The rabbit hole: bridging to Linear via MCP/OAuth.** The Linear MCP in `~/.claude.json`
  is claude.ai-session plumbing — a plain-Python digest cannot and must not use it. Do not
  build OAuth flows, browser automation, or token extraction. Key-or-degrade is the entire v1
  contract; the park file is the designed outcome, not a failure.
- **Second rabbit hole: LLM re-ranking of NEEDS-YOU.** extension-notes.md names LLM triage as
  stage-2 and says resist fattening the digest into the BA agent. The 110/85 constants are
  the whole ranking story here.
- **Style:** stdlib only, defensive per-file try/except, graceful zeros for missing config —
  copy the shapes of `in_flight.py`/`needs_you.py` line-for-line where possible. Renderer
  additions are plain ASCII text lines through the existing helpers; never re-derive box
  widths.
- **Prefer parking over guessing** on anything that smells like store-schema drift (A2), seam
  contention (A3), or Linear API archaeology beyond two query adaptations (Move 6-A's
  counter-move). A parked question costs minutes; a guessed schema costs the morning briefing
  its credibility — the one thing this ticket exists to build.
