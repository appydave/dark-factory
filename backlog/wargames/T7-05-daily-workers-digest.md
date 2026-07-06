# T7-05 — Daily workers' review digest

| field | value |
|---|---|
| ticket | wg-t7-05-daily-workers-digest |
| track / size / priority | T7 Self-learning / S / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

David ends the day asking "what did the workers do today?" and today the answer is
hand-assembled: `engine/status.py` shows a current-state snapshot (queue depth, last-N done,
audit tail) but nothing windows the store by day, joins tickets to their outcomes and their
workers, or reads as a review. Build `engine/workers_digest.py`: a stdlib-only, **read-only**,
day-windowed rollup over `engine/store/` — settled tickets joined with their `results/`
self-reports and `audit.jsonl` attribution (worker + session), needs-decision items opened in
the window ("blocked on you"), still-running tickets, and a queue snapshot — rendered as a
terminal report, `--md`, or `--json`, with `--write` persisting `engine/digests/<date>.md`.
The candidate brief mandates an overlap check against project-digest BEFORE building; that is
Move 1 and it can legitimately end this ticket at an abort. Done looks like: overlap gate
passed, every windowing/join rule fixture-proven, real-store runs green for today and a known
busy past day, `status.py` untouched and still green, the tool documented in
`engine/README.md`, everything committed and pushed.

**Locked design (no taste calls left open):**

- **Name/home:** `engine/workers_digest.py`, sibling of `status.py`. Written digests go to
  `engine/digests/<YYYY-MM-DD>.md` — deliberately OUTSIDE `engine/store/` so the store stays
  lifecycle-only (T1-10's retention war game hard-aborts on unknown `store/` dirs; do not
  trip it).
- **CLI:** `--date YYYY-MM-DD` (default: today, LOCAL calendar day) · `--json` · `--md`
  (print markdown to stdout) · `--write` (also save the markdown to `--out`) · `--out DIR`
  (default `engine/digests/`) · `--store PATH` (fixture override: rebuild every store path
  off PATH, ignore the orchestrator-imported constants). Exit 0 on success **including an
  empty day** (print `no worker activity on <date>` plus the queue snapshot).
- **Window:** the LOCAL calendar day `[00:00, 24:00)` converted to UTC epoch for comparison
  (end-of-day review is a local human ritual; store timestamps are UTC — David is UTC+10
  where UTC days split his evenings). Header shows both: local date + the UTC span.
- **Settle-time basis** (what puts a done ticket "in today"): mtime of `results/<f>.json` if
  it exists (the worker's completion self-report), else `max(st_mtime, st_ctime)` of
  `done/<f>.json` (a pure-rename settle bumps ctime; a hand-reap rewrite bumps mtime —
  verified against the real store 2026-07-06: hand-reaped 07-04 tickets correctly carry
  07-06 file times). Fallback when file times are provably bogus → Fork F1.
- **Attribution join:** scan `audit.jsonl` once; the LAST entry whose `"ticket"` field equals
  the done filename wins (retries log one entry per attempt — latest attempt wins). Fields
  used: `worker`, `session_id` (render first 8 chars), `claimed_at`. No matching entry →
  render `hand-closed / no dispatch record` (external-research and hand-reaped tickets are a
  normal, verified store shape — never an error).
- **Outcome:** reuse `status.py`'s `done_outcome()` verbatim by import — it already handles
  every observed schema generation (results self-report / ticket-embedded result / dict-shaped
  result). Do not reimplement it.
- **Report sections (all three renderers mirror this):** header (date + UTC span + time
  basis) · `SETTLED (n)` — per ticket: `[result]` filename — title, worker, session-8,
  settled-time, notes (first 200 chars in human mode) · `BLOCKED ON YOU (n)` —
  `needs-decision/*.json` with file mtime in the window: filename, `question` field, opened
  time · `STILL RUNNING (n)` — every `running/` ticket: filename, title, claimed_by,
  claimed_at, age · `QUEUE SNAPSHOT` — depth + oldest-age one-liner (run-time snapshot, not
  windowed).
- **`--json` schema:** `{generated_at, window: {local_date, utc_start, utc_end, time_basis},
  settled: [{file, title, result, notes, worker, session_id, settled_at}], blocked:
  [{file, question, opened_at}], running: [{file, title, claimed_by, claimed_at, age_s}],
  queue: {depth, oldest_age_s}}`.

## Locked context

- **Q4 (decisions.md): everything through the engine** — this ticket is written for sonnet
  Swagger dispatch; self-report to `results/` per the orchestrator's task prompt.
- **Q9 (decisions.md): complement, don't replace** — this tool complements `status.py` (a
  now-snapshot) and project-digest (the per-project MORNING briefing). It must not fork,
  wrap, or modify either. The candidate brief's overlap check is a gate, not a formality.
- **Ticket-first standing rule (`engine/store/queue/.CONVENTION.md`):** the store is the
  single audit trail. This tool is strictly read-only over `engine/store/` — its only writes
  land in `engine/digests/`.
- **No standing cron without an explicit go** (plans/wargames/unknowns-map.md §B): this is a
  manually-invoked tool. No launchd, no `/loop`, no scheduled task.
- **No `-p`/headless/SDK ever; interactive `claude` only** — binds how this ticket runs, not
  the tool itself.

## Recon (verify before any work)

Repo root `/Users/davidcruwys/dev/ad/apps/dark-factory`; paths relative to it unless
absolute. Authoring-time state (2026-07-06) noted; docs lag code — trust these checks.

1. **Engine layout + nobody-got-here-first.** `ls engine/*.py` → authoring: exactly
   `consumer.py halt.py orchestrator.py status.py wake.py warm_pool.py`.
   `ls engine/workers_digest.py engine/digests/ 2>&1` → both "No such file". If
   `workers_digest.py` (or any day-windowed digest module) already exists → **Abort A1**.
   Other NEW engine modules are fine — note them, don't touch them.
2. **Foreign work in flight?** `git status --porcelain engine/ | grep -v '^?? engine/store/'`
   → expect empty (or only store lifecycle movement). Uncommitted edits to any existing
   `engine/*.py` → **Abort A3**.
3. **Path constants.** `grep -n "^Q, RUN, DONE, RES\|^NEEDS, DEC\|^AUDIT\s*=\|^STORE\s*=" engine/orchestrator.py`
   → expect `STORE` (≈line 54), `Q, RUN, DONE, RES` (≈55), `NEEDS, DEC` (≈57), `AUDIT` (≈58).
   These are the single source of truth; import them, never redefine. Missing/renamed →
   **Fork F2** applies to the status.py import too — same recovery.
4. **status.py helper seams.**
   `grep -n "def _list_json\|def parse_fname_ts\|def human_age\|def done_outcome" engine/status.py`
   → all four present (authoring ≈ lines 32/46/82/106). `python3 engine/status.py` → exit 0
   (baseline: the ledger reader is green before you start). Helpers missing → **Fork F2**.
5. **Overlap sweep (the candidate-brief mandate — feeds Move 1).**
   (a) `grep -rn "engine" /Users/davidcruwys/dev/ad/apps/project-digest/lib/*.py` → authoring:
   ZERO hits (project-digest is engine-blind). Hits appearing means T1-04 (`lib/shipped.py`
   done-feed) and/or T2-05 (`lib/needs_you.py` feed) landed — that is per-project MORNING
   briefing enrichment, NOT a factory-wide day rollup: note it, proceed.
   (b) `grep -n "add_argument" engine/status.py` → authoring: only `--json`, `--n-done`,
   `--n-audit` — no date/window mode. A `--date`/`--since` day mode present → **Abort A1**.
   (c) `head -20 /Users/davidcruwys/dev/ad/apps/project-digest/README.md` → confirm its
   charter is still the per-project briefing feed. If it has grown a factory-wide
   "what did the workers do" surface → **Abort A1**.
6. **Store shapes to code against.** `head -1 engine/store/audit.jsonl | python3 -m json.tool`
   → keys include `ticket` (a done FILENAME), `worker`, `session_id`, `claimed_at`.
   `ls engine/store/done/*.json | wc -l` (authoring: 17) and
   `ls engine/store/results/*.json | wc -l` (authoring: 4) — most done tickets have NO
   results file (hand-closed shape); `done_outcome()` exists precisely for this.
   `ls engine/store/needs-decision/` (authoring: empty — the BLOCKED section must render
   cleanly on zero). Record all counts plus `git status --porcelain engine/store/ | head`
   as the Move-5 negative-check baseline.

## Moves

### Move 1 — Overlap gate (build / don't-build decision)

- **Do:** Evaluate Recon 5 against this rule: BUILD only if (i) no day-windowed rollup mode
  exists in `engine/` and (ii) project-digest's surface remains per-project briefing (engine
  feeds inside its five fields are fine and expected once T1-04/T2-05 land). Write the
  decision as one short paragraph (what you checked, what you found, why it's complementary)
  — you will paste it into your results JSON `notes` in Move 6.
- **Expect:** BUILD, with the paragraph citing Recon 5a/5b/5c findings.
- **Failure signal:** an equivalent day-windowed factory rollup already exists anywhere
  (engine module, a status.py mode, or a project-digest surface).
- **Counter-move:** → Abort A1. Do not "build it anyway but better".

### Move 2 — Write `engine/workers_digest.py`

- **Do:** Implement the Locked design verbatim. Constraints: stdlib only (`os, sys, json,
  argparse, datetime` — matches every engine module); paste the Locked-design bullet list
  into the module docstring as the contract; import
  `from orchestrator import Q, RUN, DONE, RES, AUDIT, NEEDS` and
  `from status import done_outcome, parse_fname_ts, _list_json, human_age` (status.py's own
  import-from-orchestrator precedent — script-dir imports work from any cwd because Python
  adds the script's directory to `sys.path`). When `--store PATH` is set, rebuild all six
  store paths off PATH and ignore the imports' values. Window math: build local-midnight
  datetimes via `datetime.now().astimezone()`, convert to UTC epoch, compare against the
  settle-time basis. Open every JSON defensively (a `_load`-style try/except returning `{}`
  — same posture as status.py). No writes anywhere except the `--write` path
  (`os.makedirs(out_dir, exist_ok=True)` + write `<date>.md`).
- **Expect:** `python3 engine/workers_digest.py --help` prints usage, exit 0;
  `python3 -c "import ast; ast.parse(open('engine/workers_digest.py').read())"` exit 0.
- **Failure signal:** the `from status import ...` / `from orchestrator import ...` line
  raises ImportError/AttributeError.
- **Counter-move:** → Fork F2. If the fork's Route A adaptation also fails → Abort A1.

### Move 3 — Prove every rule on a synthetic fixture

- **Do:** In the scratchpad (NOT the repo), build a fake store spanning two days and run
  with `--store`/`--out`:
  ```bash
  FIX=$(mktemp -d)/store
  mkdir -p $FIX/{queue,running,done,results,events,needs-decision,decisions}
  # day-1 (2026-01-01): dispatched settle — done + results + audit entry
  echo '{"ticket":"alpha","title":"Alpha job"}' > $FIX/done/20260101T0100Z-alpha.json
  echo '{"status":"done","notes":"alpha shipped, sha abc1234"}' > $FIX/results/20260101T0100Z-alpha.json
  # day-1: hand-closed settle — result embedded in ticket, NO results file, NO audit entry
  echo '{"ticket":"bravo","title":"Bravo job","result":"done","note":"hand-reaped"}' > $FIX/done/20260101T0200Z-bravo.json
  # day-2 (2026-01-02): one settle — must NOT appear in day-1's digest
  echo '{"ticket":"charlie","title":"Charlie job"}' > $FIX/done/20260102T0100Z-charlie.json
  echo '{"status":"done","notes":"charlie done"}' > $FIX/results/20260102T0100Z-charlie.json
  # audit: two attempts for alpha (retry — LAST must win), none for bravo/charlie
  printf '%s\n' \
    '{"ticket":"20260101T0100Z-alpha.json","attempt":1,"worker":"df-worker-1","session_id":"aaaaaaaa-0000","claimed_at":"2026-01-01T01:05:00Z"}' \
    '{"ticket":"20260101T0100Z-alpha.json","attempt":2,"worker":"df-worker-2","session_id":"bbbbbbbb-0000","claimed_at":"2026-01-01T01:20:00Z"}' \
    > $FIX/audit.jsonl
  # blocked-on-you opened day-1; a running ticket; a queued ticket
  echo '{"ticket":"delta","question":"pick a name"}' > $FIX/needs-decision/20260101T0300Z-delta.json
  echo '{"ticket":"echo","title":"Echo job","claimed_by":"w","claimed_at":"2026-01-01T04:00:00Z"}' > $FIX/running/20260101T0400Z-echo.json
  echo '{"ticket":"foxtrot","title":"Foxtrot queued"}' > $FIX/queue/20260101T0500Z-foxtrot.json
  # orphan result (results file with no done counterpart) — must be ignored, not crash
  echo '{"status":"done"}' > $FIX/results/20260101T0600Z-orphan.json
  # stamp file times to the intended days (LOCAL time — the window is local)
  touch -t 202601011200 $FIX/done/20260101T0100Z-alpha.json $FIX/results/20260101T0100Z-alpha.json \
    $FIX/done/20260101T0200Z-bravo.json $FIX/needs-decision/20260101T0300Z-delta.json
  touch -t 202601021200 $FIX/done/20260102T0100Z-charlie.json $FIX/results/20260102T0100Z-charlie.json
  python3 engine/workers_digest.py --store $FIX --date 2026-01-01
  python3 engine/workers_digest.py --store $FIX --date 2026-01-01 --json
  python3 engine/workers_digest.py --store $FIX --date 2026-01-01 --md --write --out $FIX-digests
  python3 engine/workers_digest.py --store $FIX --date 2025-12-25          # empty day
  ```
  Assert ALL of: (a) day-1 digest SETTLED = alpha + bravo only — charlie excluded;
  (b) alpha attributed `worker=df-worker-2` / session `bbbbbbbb` (LAST audit entry won) with
  notes from its results file; (c) bravo renders result `done` with
  `hand-closed / no dispatch record`; (d) BLOCKED ON YOU lists delta with its `question`;
  (e) STILL RUNNING lists echo; (f) QUEUE SNAPSHOT depth 1; (g) the orphan result crashes
  nothing and appears nowhere; (h) `--json` parses (`python3 -m json.tool`) and matches the
  locked schema keys; (i) `$FIX-digests/2026-01-01.md` exists and contains a `SETTLED`
  section; (j) the empty-day run prints `no worker activity` and exits 0;
  (k) `ls $FIX/done $FIX/results $FIX/queue $FIX/running $FIX/needs-decision` — file set
  byte-identical to before the runs (read-only proven).
- **Expect:** every assertion true; all four invocations exit 0.
- **Failure signal:** any assertion false.
- **Counter-move:** code bug — fix and re-run the fixture from scratch (delete and rebuild
  `$FIX`). Same assertion failing after two fix attempts → Abort A2.

### Move 4 — Real-store runs

- **Do:** From the repo root: `python3 engine/workers_digest.py` (today, local), then
  `python3 engine/workers_digest.py --date 2026-07-04` (a busy day at authoring: 5+ tickets
  settled), then `python3 engine/workers_digest.py --json | python3 -m json.tool > /dev/null`,
  then `python3 engine/status.py`.
- **Expect:** all exit 0. Today's digest reflects whatever actually settled today (zero is
  legal → the empty-day line). The 2026-07-04 run renders a well-formed report — do NOT pin
  exact counts: months from now T1-10's retention may have archived that day's files (a
  sparse/empty historical day is correct behavior, not a bug). Every SETTLED entry shows
  either a worker attribution or `hand-closed / no dispatch record` — never a raw `None`.
  If the window's membership looks wrong (e.g. every done ticket ever lands in "today") →
  that is the time-basis failure → **Fork F1**. `status.py` exit 0, output unchanged in
  meaning from Recon 4.
- **Failure signal:** nonzero exit, a traceback on any real store shape (schema drift the
  fixture didn't cover), or `git status --porcelain engine/store/` showing NEW dirt vs the
  Recon 6 baseline (the tool wrote into the store — read-only violation).
- **Counter-move:** traceback on a real shape → make the loader defensive for that shape,
  re-run Move 3's fixture FIRST, then retry. A store write → revert the dirt
  (`git checkout -- engine/store/` for tracked changes, delete untracked files the tool
  created), fix, redo Moves 3–4. Second store-write occurrence → Abort A2.

### Move 5 — Persist a real digest

- **Do:** `python3 engine/workers_digest.py --write` then
  `ls engine/digests/$(date +%Y-%m-%d).md` and
  `git status --porcelain engine/ | grep -v store/`.
- **Expect:** the file exists; git shows ONLY the two new paths (`engine/workers_digest.py`,
  `engine/digests/…`) — no modification to any existing `engine/*.py`.
- **Failure signal:** the digest file lands under `engine/store/` (wrong home — breaks the
  T1-10 fence), or an existing module shows as modified.
- **Counter-move:** wrong home → fix the `--out` default, delete the misplaced file, re-run.
  An existing module modified → you left the scope fence; `git checkout --` it, and if the
  tool genuinely needed that edit to work → Abort A2 (the read-only/additive contract is
  the ticket).

### Move 6 — Document, self-report, commit, push

- **Do:** Add a `## Workers' digest (end-of-day review)` section to `engine/README.md`: what
  it answers ("what did the workers do today"), the invocations (`workers_digest.py`,
  `--date`, `--json`, `--md`, `--write`), the local-day window semantics, the
  settle-time basis one-liner, where written digests live (`engine/digests/` — deliberately
  outside `store/`), how it complements `status.py` (day-windowed review vs now-snapshot),
  and the explicit note "not scheduled — manual invocation only; scheduling needs David's
  go". Write the worker self-report to `engine/store/results/<this-ticket-filename>.json`
  in the exact form the orchestrator's task prompt demands, including the Move-1 overlap
  paragraph in `notes`. Commit `engine/workers_digest.py`, `engine/digests/<today>.md`, and
  the README section in one commit:
  `feat(engine): workers' digest — day-windowed end-of-day rollup over the store (wg-t7-05)`
  with the standard Co-Authored-By trailer; push.
- **Expect:** `git log --oneline -1` shows the commit; `git status --porcelain` clean apart
  from pre-existing dirt noted in Recon 6.
- **Failure signal:** push rejected (non-fast-forward).
- **Counter-move:** `git pull --rebase` then push; rebase conflicts inside `engine/store/`
  (another session moved tickets) → prefer the OTHER side for ticket lifecycle files,
  re-run `python3 engine/status.py`, push again. Second push failure → leave committed
  locally and say so in the results JSON `notes`.

## Forks

**F1 — File times unreliable (fresh clone / bulk-touched store).**
**Trigger:** Move 3 or 4 — window membership is provably wrong: >80% of `done/` files share
one file-time day that contradicts their filename timestamps (a fresh `git clone` resets
every mtime/ctime to checkout time, so ALL history lands in "today").
→ **Route A (times sane — the authoring-time verified case):** keep the stat basis; no action.
→ **Route B (times bogus):** switch the settle basis to parsed ticket fields — `claimed_at`,
else `requested_at`, else `parse_fname_ts(filename)` — and print a
`time basis: ticket fields (file times unreliable)` note in the header + `--json`'s
`window.time_basis`. Document the degraded mode in the README section. Never mix bases in
one run.

**F2 — status.py / orchestrator import seams drifted.**
**Trigger:** Move 2 — `from status import done_outcome, ...` or
`from orchestrator import Q, ...` raises, or Recon 3/4 finds the names moved.
→ **Route A (renamed/moved but logic present):** locate the new names
(`grep -n "def done\|^Q\|^STORE" engine/*.py`), adapt the import, note the drift in the
results JSON.
→ **Route B (status.py gone or rewritten beyond recognition):** inline minimal local copies
of `done_outcome` + `parse_fname_ts` (≤40 lines total, comment naming the drift and the
source they were copied from), keep the orchestrator constants if those survive, and flag
the drift prominently in the results JSON — do NOT refactor status.py's remains.

## Assumptions ledger

1. **Name (`workers_digest.py`) and flag names are Fable's choice** — the interview never
   asked. Plausible: mirrors the candidate title, avoids colliding with project-digest's
   "digest" vocabulary. If David pushes back: renaming is a one-file `git mv` + README
   touch-up — apply his name, never park over naming.
2. **Local calendar day, not UTC.** Plausible: end-of-day review is a local ritual and David
   is UTC+10, where UTC days split his evenings mid-session. If David wants UTC windows:
   flip the window math to UTC midnights (one function), note in README — a flag, not a
   parking matter.
3. **`engine/digests/` (outside `store/`) is the right write home.** Deliberate: keeps
   `store/` lifecycle-only and avoids tripping T1-10's retention war game, which hard-aborts
   on unknown `store/` dirs. If David prefers digests inside the store → **needs-decision/**
   (it forces a T1-10 policy edit too; not the executor's call).
4. **No scheduling in this ticket.** Manual tool only. If execution-time context shows David
   asked for an automatic end-of-day run → separate ticket (unknowns-map §B: a live cron is
   a standing commitment); note it in the results JSON, don't build it.
5. **T1-04/T2-05 may have landed by execution time** (engine feeds inside project-digest's
   briefing fields, done-watcher notifications in wake.py). Assumed complementary: those are
   per-project morning-briefing enrichment and per-ticket signals; this is the factory-wide
   end-of-day rollup. If their landing actually produced a day-windowed factory-wide rollup
   → the assumption is false → Abort A1.
6. **decisions/ resolutions stay out of scope.** The digest reports needs-decision items
   OPENED in the window, not decisions answered. Plausible: keeps S-size; answered decisions
   already leave the needs-decision/ dir. If David wants a "you unblocked N workers" line →
   future one-move extension, note only.

## Abort conditions

Every abort: write `engine/store/needs-decision/wg-t7-05-daily-workers-digest.json` as
`{"ticket": "wg-t7-05-daily-workers-digest", "question": "<one sentence>", "proposed": "<your recommended answer>", "note": "<evidence: paths/commands/output>"}`,
leave this ticket in `running/` if engine-dispatched, and stop. Never guess past an abort.

- **A1 — an equivalent tool already exists.** Recon 1/5 or Move 1/2: `workers_digest.py`
  present, `status.py` grew a day-window mode, or a factory-wide day rollup surfaced
  elsewhere. Question: "A day-windowed workers rollup already exists at <path> (found via
  <check>). Extend it, supersede it, or drop T7-05?" Complement-don't-replace (Q9) makes
  this David's call, not the executor's.
- **A2 — tool cannot be trusted.** The same fixture assertion fails after two fix attempts,
  OR the tool writes into `engine/store/` on a real run (twice), OR it needs an edit to an
  existing engine module to function. Revert all real-store/module dirt FIRST, then park.
  Question: "workers_digest.py failed its own contract: <how>." A review tool that mutates
  the ledger it reviews is worse than none.
- **A3 — foreign work in the way.** Recon 2's uncommitted edits to existing `engine/*.py`,
  or Move 6's rebase conflict in a file you didn't author. Question: "engine/ has in-flight
  foreign changes (<files>) — rebase over them, or hold T7-05?" Do not build on an unknown
  diff.

## Verification

Run from `/Users/davidcruwys/dev/ad/apps/dark-factory`:

```bash
python3 -c "import ast; ast.parse(open('engine/workers_digest.py').read())"        # exit 0
python3 engine/workers_digest.py --help                                            # usage, exit 0
python3 engine/workers_digest.py                                                    # today, exit 0 (empty day legal)
python3 engine/workers_digest.py --date 2026-07-04                                  # exit 0, well-formed report
python3 engine/workers_digest.py --json | python3 -m json.tool | grep -c '"settled"'   # → 1
python3 engine/workers_digest.py --write && ls engine/digests/$(date +%Y-%m-%d).md  # file exists
python3 engine/status.py                                                            # exit 0 — snapshot tool untouched
grep -n "Workers' digest" engine/README.md                                          # section present
ls engine/store/results/ | grep -c wg-t7-05                                         # 1 — worker self-report exists
```

Fixture evidence (Move 3) must have demonstrated, at least once: day-window exclusion
(charlie out), last-audit-entry attribution (df-worker-2 wins), hand-closed rendering,
blocked/running/queue sections, orphan-result tolerance, empty-day exit 0, `--write` output,
and read-only behavior over every store dir.

Negative checks:
```bash
git status --porcelain engine/store/            # unchanged vs the Recon 6 baseline
git diff --stat HEAD~1 -- engine/orchestrator.py engine/status.py engine/consumer.py \
  engine/halt.py engine/wake.py engine/warm_pool.py                          # empty — no existing module touched
ls engine/store/digests 2>&1                     # "No such file" — nothing written under store/
crontab -l 2>&1; ls engine/launchd/              # unchanged vs Recon — no scheduling added
```
And project-digest untouched: `git -C /Users/davidcruwys/dev/ad/apps/project-digest status --porcelain`
shows nothing attributable to this ticket (a pre-existing modified `view/*.html` is known
noise there, not yours).

Partial pass (Abort A1/A3): NO code committed, plus
`needs-decision/wg-t7-05-daily-workers-digest.json` naming the exact overlap or foreign work
found. That is a legitimate exit — the candidate brief made the overlap check a first-class
outcome.

## Executor notes (sonnet)

- **Scope fence:** create `engine/workers_digest.py` + `engine/digests/<date>.md`, extend
  `engine/README.md` — NOTHING else. Never edit any existing `engine/*.py`. Never write
  under `engine/store/` (your results self-report JSON is the single sanctioned exception,
  per the dispatch wrapper). Never touch `~/dev/ad/apps/project-digest/` — it is a
  read-only overlap-check target in this ticket.
- **Read-only is the contract.** If you are about to open any store file in write mode or
  move/rename anything under `store/`, you have left the war game — stop.
- **No scheduling.** No cron, no launchd plist, no `/loop` suggestion. Manual tool only.
- **Prefer HITL over guessing** on anything overlap-shaped: a parked ticket with a crisp
  "extend or supersede?" question costs minutes; a duplicate review surface costs a
  consolidation ticket later.
- **The rabbit hole:** the `audit.jsonl` entries carry `transcript` paths to full session
  JSONLs — you will be tempted to mine them for a richer narrative ("what the worker
  actually did"), or to add an HTML view, or LLM summarization. Skip all of it. Ticket
  titles + results notes + attribution ARE the day's story; the terminal/md/json renderers
  are the whole deliverable. Transcript mining is T7's Chronicle seed — a different ticket.
