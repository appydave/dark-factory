# T1-10 — Engine store retention policy

| field | value |
|---|---|
| ticket | wg-t1-10-store-retention |
| track / size / priority | T1 Engine / S / normal |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

`engine/store/` is a growing ledger by design — `done/`, `results/`, `events/`, `audit.jsonl`
and `events-consumed.jsonl` accumulate forever and nothing prunes them (verified 2026-07-06:
17 done tickets, 4 results, 1 event, 1 audit line — tiny today, unbounded tomorrow). Build
`engine/retention.py`: a stdlib-only, dry-run-by-default tool that ARCHIVES (never deletes)
settled artifacts older than a keep-window into `engine/store/archive/`, keeping done/results
pairs together and never orphaning an unconsumed event. Done looks like: the tool exists, a
synthetic-fixture run proves every policy rule, a real-store dry-run + apply both exit clean,
`status.py` still works afterwards, and the policy is documented in `engine/README.md`.

## Locked context

- **Q4 (decisions.md):** everything through the engine — this ticket is written for sonnet
  Swagger dispatch; the worker self-reports to `results/` per the orchestrator's task prompt.
- **Ticket-first standing rule (`engine/store/queue/.CONVENTION.md`):** the ticket's own
  queue/running/done movement plus `results/<ticket>.json` is the audit trail — retention must
  preserve that trail, which is why the policy is archive-only, never delete.
- **No `-p`/headless/SDK ever; interactive `claude` only** — irrelevant to the tool itself but
  binds how this ticket runs.
- **No standing cron without an explicit go** (plans/wargames/unknowns-map.md §B: "a live cron
  is a standing commitment — needs explicit go"): retention is a manually-invoked tool in this
  ticket. Scheduling it is a separate future decision.

## Recon (verify before any work)

Docs lag code — trust none of the above until these pass. Repo root is
`/Users/davidcruwys/dev/ad/apps/dark-factory`; all paths below relative to it.

1. `ls engine/store/` → expect exactly these lifecycle dirs: `queue/ running/ done/ results/
   events/ needs-decision/ decisions/`, plus root files `audit.jsonl`,
   `events-consumed.jsonl`, `wake.log`, `.wake-state.json` (and possibly transient `HALT` /
   `BACKOFF` flag files). If a lifecycle dir is missing/renamed or a NEW lifecycle dir exists
   that this war game doesn't name → **Abort A1** (the policy below would be guessing).
2. `grep -n "Q, RUN, DONE, RES\|EVENTS\s*=\|AUDIT\s*=\|NEEDS\|DEC" engine/orchestrator.py |
   head` → expect path constants `Q, RUN, DONE, RES` (≈line 55), `EVENTS`, `AUDIT`, and
   `NEEDS`/`DEC` all defined off a `STORE` root. These are the single source of truth for
   store paths; retention.py must import them, not redefine them. Missing/renamed → **Fork F3**.
3. `grep -n "from orchestrator import" engine/status.py` → expect status.py already imports
   `Q, RUN, DONE, RES, AUDIT` from orchestrator (≈line 25). This is the precedent pattern
   retention.py copies. Also note `done_outcome()` (≈line 106) reads `done/<fname>` AND
   `results/<fname>` as a PAIR — this is why pairs must archive together.
4. `sed -n '40,56p' engine/consumer.py` → expect `load_seen()` rebuilding the consumer's
   seen-set from `events-consumed.jsonl`, keyed on `(source, path)` where `path` is the
   **absolute path** of the event file. Consequence (drives Move 2 rules): dropping a
   consumed-log line whose event file still exists on disk causes re-consumption (duplicate
   chime + duplicate record); archiving a not-yet-consumed event file loses the signal
   forever. Both must be impossible under the policy.
5. `ls engine/retention.py engine/store/archive/ 2>&1` → expect both missing ("No such
   file"). If retention.py or archive/ already exists, someone got here first → **Abort A1**
   (park with the question "extend or supersede the existing implementation?").
6. Baseline snapshot: `python3 engine/status.py --json > /tmp/t1-10-baseline.json; echo $?` →
   exit 0. Then `for d in queue running done results events needs-decision decisions; do
   echo "$d: $(ls engine/store/$d/*.json 2>/dev/null | wc -l)"; done; wc -l
   engine/store/audit.jsonl engine/store/events-consumed.jsonl` → record all counts. And
   `git status --porcelain engine/store/ | head` → note any pre-existing dirt so Move 5's
   negative check doesn't blame retention for it.

## Moves

### Move 1 — Pin the policy contract before writing code

- **Do:** Write the policy table below into `engine/retention.py`'s module docstring verbatim
  (it is the spec; the code implements it):

  | target | eligible when | action |
  |---|---|---|
  | `done/<f>.json` | file mtime older than `--keep-days` AND not among the `--keep-min` newest (by filename sort) | move to `archive/done/<f>.json`; if `results/<f>.json` exists, move it to `archive/results/<f>.json` in the same pass |
  | `results/<f>.json` with NO `done/<f>.json` counterpart | never auto-archived | report as `orphan-result` anomaly, leave in place |
  | `events/<f>.json` | mtime older than `--keep-days` AND its absolute path appears in `events-consumed.jsonl` | move to `archive/events/<f>.json` |
  | `events/<f>.json` unconsumed | never | → Fork F2 |
  | `audit.jsonl` line | its `claimed_at` parses and is older than `--keep-days` | append line to `archive/audit.jsonl`, rewrite live file without it (tmp-file + `os.rename`, atomic) |
  | `events-consumed.jsonl` line | its recorded `path` no longer exists on disk | append to `archive/events-consumed.jsonl`, rewrite live file without it |
  | any undated/unparseable jsonl line | never | keep in live file, count as `undated-kept` |
  | `queue/ running/ needs-decision/ decisions/`, store-root files (`HALT`, `BACKOFF`, `.wake-state.json`, `wake.log`), dotfiles, `.gitkeep`, `.CONVENTION.md` | never touched | out of scope, hard-fenced in code |

  Ordering rule (crash-safety, from Recon 4): an event FILE moves before its consumed-log
  LINE is eligible — a crash between the two leaves a dangling log line (harmless; glob won't
  find the moved file) rather than a re-consumable file.
- **Expect:** the table transcribed into the docstring; no code yet.
- **Failure signal:** you find yourself wanting a rule the table doesn't cover.
- **Counter-move:** if it's a genuinely new store shape → Abort A1; if it's an edge inside a
  covered target (e.g. a done ticket that is a directory, not a file) → skip the file, report
  it as an anomaly, continue.

### Move 2 — Write `engine/retention.py`

- **Do:** Implement the docstring policy. Constraints: stdlib only (`os, sys, json, shutil,
  argparse, datetime` — matches every other engine module); import path constants
  `from orchestrator import Q, RUN, DONE, RES, EVENTS, AUDIT, STORE` (status.py precedent,
  Recon 2/3); derive `CONSUMED_LOG = os.path.join(STORE, "events-consumed.jsonl")` and
  `ARCHIVE = os.path.join(STORE, "archive")`. CLI: `--keep-days N` (default 30), `--keep-min
  N` (default 20), `--apply` (without it, DRY-RUN: print the exact move/rewrite plan, mutate
  nothing), `--store PATH` (override the store root entirely — for fixture testing; when set,
  ignore the orchestrator-imported constants and rebuild all paths off PATH), `--json`
  (machine-readable plan/report). Exit 0 on success including a no-op plan; nonzero on any
  anomaly of class `scope-violation` (a planned move touching a fenced path — should be
  unreachable, it's a self-check). Age basis: `os.path.getmtime` (filename timestamps are
  request-time, not settle-time; mtime ≈ claim/settle-write time — see Assumptions #4).
  Archive dirs created on demand with `os.makedirs(..., exist_ok=True)`. Never overwrite: if
  an archive destination already exists → **Abort A3**.
- **Expect:** `python3 engine/retention.py --help` prints usage, exit 0. `python3 -c "import
  ast; ast.parse(open('engine/retention.py').read())"` exit 0.
- **Failure signal:** import of orchestrator constants raises (module-level side effects or
  renamed constants).
- **Counter-move:** → Fork F3. If the fork's Route A adaptation also fails → Abort A1.

### Move 3 — Prove every rule against a synthetic fixture

- **Do:** In the scratchpad (NOT the repo), build a fake store and run the tool against it
  with `--store`:
  ```bash
  FIX=$(mktemp -d)/store   # or scratchpad dir if mktemp unavailable
  mkdir -p $FIX/{queue,running,done,results,events,needs-decision,decisions}
  # old done+result pair (eligible)
  echo '{"ticket":"old-a"}' > $FIX/done/20260101T0000Z-old-a.json
  echo '{"ticket":"old-a","status":"done"}' > $FIX/results/20260101T0000Z-old-a.json
  # old done WITHOUT result (eligible, archives alone — hand-closed precedent)
  echo '{"ticket":"old-b"}' > $FIX/done/20260101T0001Z-old-b.json
  # orphan result (kept + anomaly)
  echo '{"ticket":"orphan"}' > $FIX/results/20260101T0002Z-orphan.json
  # fresh done (kept by window)
  echo '{"ticket":"new-c"}' > $FIX/done/$(date -u +%Y%m%dT%H%MZ)-new-c.json
  # consumed old event + matching consumed-log line; unconsumed old event
  echo '{"event":"job.completed"}' > $FIX/events/20260101T0003Z-consumed.json
  echo '{"event":"job.completed"}' > $FIX/events/20260101T0004Z-unconsumed.json
  echo "{\"source\":\"engine\",\"path\":\"$FIX/events/20260101T0003Z-consumed.json\",\"ts_consumed\":\"2026-01-01T00:05:00Z\"}" > $FIX/events-consumed.jsonl
  # audit: one old line, one fresh line, one undated line
  printf '%s\n' '{"ticket":"old-a","claimed_at":"2026-01-01T00:00:30Z"}' \
    "{\"ticket\":\"new-c\",\"claimed_at\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" \
    '{"note":"no timestamp here"}' > $FIX/audit.jsonl
  # backdate mtimes of everything named 202601* so the mtime-based window fires
  touch -t 202601010000 $FIX/done/202601* $FIX/results/202601* $FIX/events/202601*
  python3 engine/retention.py --store $FIX --keep-days 30 --keep-min 1          # dry-run
  python3 engine/retention.py --store $FIX --keep-days 30 --keep-min 1 --apply
  ```
  Then assert ALL of: (a) `archive/done/` holds old-a + old-b and `archive/results/` holds
  old-a's result; (b) orphan result still in live `results/`, reported as anomaly; (c) fresh
  done still live; (d) consumed event in `archive/events/`, unconsumed event still live and
  reported; (e) live `audit.jsonl` = fresh line + undated line, `archive/audit.jsonl` = old
  line; (f) consumed-log line for the now-archived event moved to
  `archive/events-consumed.jsonl` (its path no longer exists live) — or, if your
  implementation defers log-line pruning to the NEXT run (legal under the ordering rule), run
  `--apply` a second time and then assert it; (g) `queue/ running/ needs-decision/ decisions/`
  untouched; (h) dry-run had printed exactly the moves apply performed.
- **Expect:** every assertion true; both invocations exit 0.
- **Failure signal:** any assertion false, or dry-run/apply plans differ.
- **Counter-move:** it's a code bug — fix retention.py and re-run the fixture from scratch
  (delete and rebuild `$FIX`). If the same assertion fails after two fix attempts → Abort A2.

### Move 4 — Dry-run against the real store

- **Do:** `python3 engine/retention.py` (defaults: keep-days 30, keep-min 20, dry-run) from
  the repo root, and `python3 engine/retention.py --json` once more.
- **Expect:** exit 0; a plan consistent with the Recon 6 counts (months from now the store
  may be large — the plan may legitimately list many files; that is Fork F1 Route B, not an
  error). `git status --porcelain engine/store/` unchanged from the Recon 6 snapshot —
  dry-run mutated nothing.
- **Failure signal:** nonzero exit; a planned move naming `queue/`, `running/`,
  `needs-decision/`, `decisions/`, or a store-root flag/state file; git status shows new dirt.
- **Counter-move:** a fenced-path plan entry or any dry-run mutation is a scope violation →
  fix the bug, re-run Move 3's fixture FIRST, then retry this move. Second occurrence →
  Abort A2.

### Move 5 — Apply against the real store

- **Do:** `python3 engine/retention.py --apply`, then `python3 engine/status.py` and
  `python3 engine/status.py --json > /tmp/t1-10-after.json`.
- **Expect:** exit 0; files moved exactly per Move 4's plan (→ Fork F1 for the two legitimate
  shapes this takes); status.py exits 0 and its DONE section still renders (keep-min
  guarantees ≥20 done files remain, or all of them if fewer exist); `done.total` in the after
  JSON = baseline total minus archived count; `queue`/`running` sections byte-identical in
  meaning to baseline (same files).
- **Failure signal:** status.py crashes or shows an empty DONE section; counts don't
  reconcile; anything moved that Move 4 didn't plan.
- **Counter-move:** if status.py crashes, the pairing invariant likely broke — restore by
  moving the affected archive files back (exact inverse `mv`, filenames unchanged by design),
  fix, redo Moves 3→5. If files moved that weren't in the plan → Abort A2 (restore first,
  then park).

### Move 6 — Document, self-report, commit

- **Do:** Add a `## Store retention` section to `engine/README.md`: what retention.py does,
  the policy table (reference the docstring rather than duplicating it), the two invocations
  (dry-run default / `--apply`), the defaults (30/20), the archive-not-delete rationale
  (audit-trail standing rule), and the explicit note "not scheduled — manual invocation only;
  scheduling needs David's go". Write the worker self-report to
  `engine/store/results/<this-ticket-filename>.json` in the exact form the orchestrator's
  task prompt demands. Commit everything (retention.py, README section, any archived-file
  moves from Move 5) in one commit, message
  `feat(engine): store retention — archive-only keep-window tool (wg-t1-10)` with the
  standard Co-Authored-By trailer; push.
- **Expect:** `git log --oneline -1` shows the commit; `git status --porcelain` clean apart
  from pre-existing dirt noted in Recon 6.
- **Failure signal:** push rejected (non-fast-forward).
- **Counter-move:** `git pull --rebase` then push; if rebase conflicts inside
  `engine/store/` (another session moved tickets), resolve by preferring the OTHER side for
  ticket lifecycle files and re-running `python3 engine/status.py` before pushing. Second
  push failure → leave committed locally and note it in the results JSON `notes`.

## Forks

**F1 — Real store young vs aged at execution time.**
Trigger: Move 4's dry-run plan on the real store.
→ **Route A (plan is empty — nothing outside the window yet):** legitimate; the fixture run
(Move 3) is the proof the policy works. Run `--apply` anyway (verified no-op), note
"no-op on real store, fixture-proven" in the results JSON.
→ **Route B (plan lists files):** proceed through Move 5 and verify counts reconcile; spot-
check ONE archived done/results pair opens as valid JSON in its archive location.

**F2 — Old event never consumed.**
Trigger: dry-run reports an `events/` file older than the window absent from
`events-consumed.jsonl`.
→ **Route A (consumer runnable):** `python3 engine/consumer.py --once` (exit 0 expected — it
records + chimes), then re-run retention; the event is now consumed and archivable.
→ **Route B (consumer errors or the event file is unparseable):** leave the event live,
report it as an anomaly in the results JSON. Never archive unconsumed signal.

**F3 — Orchestrator constants moved/renamed since authoring.**
Trigger: Move 2's `from orchestrator import ...` raises ImportError/AttributeError.
→ **Route A (constants renamed but `engine/store/` layout matches Recon 1):** find the new
names (`grep -n "store" engine/orchestrator.py | head -30`), adapt the import, note the drift
in the results JSON.
→ **Route B (store layout itself changed):** Abort A1.

## Assumptions ledger

1. **Defaults `--keep-days 30` / `--keep-min 20` are Fable's numbers, not David's** — the
   interview never asked. Plausible: 30d ≫ any observed queue latency; keep-min keeps
   status.py's DONE history meaningful even after an aggressive window. If David pushes back
   at triage or via HITL: the numbers are flags, change nothing structural — apply his values
   and re-run Move 5. If he questions archive-vs-delete itself → park to needs-decision/
   (that contradicts the audit-trail standing rule and is not the executor's call).
2. **`archive/` stays git-tracked.** The store is tracked today (verified: `git ls-files
   engine/store` lists done/results/events/audit); archiving via plain `mv` + `git add -A`
   preserves the provenance chain, which is the repo's value proposition. If David wants
   archive/ gitignored (files leave the index) → needs-decision/, don't guess.
3. **No scheduling in this ticket.** Retention is manual. If execution-time context shows
   David asked for a cron → that's a separate ticket; note it in results JSON, don't build it.
4. **mtime is a sound age basis on this machine.** Renames preserve mtime; a fresh `git
   clone` resets mtimes to checkout-time, which makes everything look NEW — i.e. the failure
   direction is conservative (archives too little, never too much). Accepted. If the
   executor observes mtimes obviously bogus (e.g. all identical), fall back to the filename
   timestamp (`status.py:parse_fname_ts` shows the two observed precisions) and note it.

## Abort conditions

**A1 — Store layout drift.** A Recon-1 lifecycle dir is missing/renamed, an unknown lifecycle
dir exists, or retention.py/archive/ already exist. Park: write
`engine/store/needs-decision/wg-t1-10-store-retention.json` containing
`{"ticket":"wg-t1-10-store-retention","question":"Store layout differs from the T1-10 war game (authored 2026-07-06): <what differs>. Extend the policy to cover it, or re-author?","proposed":"<one line>","note":"<observed layout>"}`.
Leave the ticket in `running/`. Never guess a policy for a directory this war game didn't name.

**A2 — Tool cannot be trusted.** The same fixture assertion fails after two fix attempts, OR
apply diverges from its own dry-run plan on the real store, OR anything moves out of a fenced
path. Restore any real-store moves (inverse `mv`), then park to needs-decision/ (same shape
as A1, question: "retention.py failed its own contract: <how>") and leave the ticket in
`running/`. A retention tool that is even slightly untrustworthy is worse than none.

**A3 — Archive destination collision.** An archive target filename already exists (should be
impossible — timestamp-prefixed names — so it means a previous partial run or a re-run over
history). Do not overwrite. Park to needs-decision/ with the colliding paths listed.

## Verification

Run from `/Users/davidcruwys/dev/ad/apps/dark-factory`:

```bash
python3 -c "import ast; ast.parse(open('engine/retention.py').read())"   # exit 0
python3 engine/retention.py --help                                       # usage, exit 0
python3 engine/retention.py                                              # real-store dry-run, exit 0
python3 engine/retention.py --apply                                      # exit 0 (no-op OK per F1-A)
python3 engine/status.py                                                 # exit 0, DONE section non-empty
grep -n "Store retention" engine/README.md                               # section present
ls engine/store/results/ | grep -c wg-t1-10                              # 1 — worker self-report exists
```

Fixture evidence (Move 3) must have demonstrated, at least once: pair-archiving, orphan-result
kept, unconsumed-event kept, jsonl split with undated-line kept, fenced dirs untouched,
dry-run/apply parity.

Negative checks:
```bash
git status --porcelain engine/store/queue engine/store/running \
  engine/store/needs-decision engine/store/decisions   # empty (vs Recon 6 baseline)
ls engine/store/HALT engine/store/BACKOFF 2>&1          # both absent (unless pre-existing per Recon 6)
```
And: no crontab/launchd entry was added (`crontab -l 2>&1; ls engine/launchd/` unchanged vs
Recon), and `orchestrator.py`, `status.py`, `consumer.py`, `halt.py`, `wake.py`,
`warm_pool.py` have no diff (`git diff --stat engine/*.py` names only retention.py as new).

## Executor notes (sonnet)

- **Scope fence:** create `engine/retention.py`, extend `engine/README.md`, move files under
  `engine/store/{done,results,events}/` + rewrite the two jsonl files — NOTHING else. Do not
  edit any existing `.py` in `engine/`. Do not touch `queue/`, `running/`,
  `needs-decision/`, `decisions/`, flag files, or anything outside `engine/`.
- **Archive-only, ever.** If you are about to call `os.remove`/`shutil.rmtree` on store data,
  you have left the war game — stop.
- **No scheduling.** No cron, no launchd plist, no `/loop` suggestion. Manual tool only.
- **Prefer HITL over guessing** on anything policy-shaped (a file kind the table doesn't
  cover, a David objection mid-run): needs-decision/ costs minutes, a wrong archive policy
  costs the audit trail.
- **The rabbit hole:** you will be tempted to build rollup/compression/SQLite/summary-index
  for the archive, or to "improve" status.py to also read archive/. Skip all of it — flat
  `mv` into mirrored dirs is the whole job. Archive-aware reporting is a future ticket if
  David ever asks.
