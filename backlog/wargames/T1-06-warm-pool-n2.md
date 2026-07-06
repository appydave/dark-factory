# T1-06 — Warm pool N>1 under CAP

| field | value |
|---|---|
| ticket | wg-t1-06-warm-pool-n2 |
| track / size / priority | T1 Engine / M / normal |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

The engine's warm pool has only ever run at N=1 (the 2026-07-03 constellation proof ticket). This
war game proves the pool at N=3 under the CAP=3 governor: (1) `lease()`'s rename-CAS claim is safe
under real multi-process contention — zero double-claims across a 200-ticket × 8-claimant race;
(2) a live `--pool 5` run is loudly clamped to 3, boots `df-worker-1..3`, drains 6 no-op test
tickets with peak concurrency 3, records ownership + audit entries per dispatch, and leaves the
deferred queue resident untouched. Done looks like: a committed reusable race harness at
`engine/tests/lease_race.py` that exits 0, a live-run log at `engine/tests/wg-t1-06/live-run.log`
containing the `[cap]` clamp line and a clean REPORT, 6 `wg-t1-06-noop` tickets in `done/`, and
one recorded limitation finding (two simultaneous orchestrator processes collide on worker names).

## Locked context

- Q4: everything through the engine — this ticket is itself written for sonnet Swagger dispatch.
- Portfolio rule: **no `-p` / headless / Agent SDK ever** (metered billing) — interactive `claude`
  only; `ANTHROPIC_API_KEY` must be unset (orchestrator's `safety_check()` enforces this).
- Kill switch discipline: HALT/BACKOFF flags are respected implicitly — never clear either flag
  yourself; HALT parks this ticket.
- Store is a growing ledger (no wipes): test tickets stay in `done/` after the run, prefixed
  `wg-t1-06-noop` so a future retention pass (T1-10) can find them.

## Recon (verify before any work)

All paths repo-relative to `~/dev/ad/apps/dark-factory/` unless absolute. Docs lag code — these
checks replace doc-trust. Authoring-time state (2026-07-06) noted where useful.

1. `grep -n "^CAP" engine/orchestrator.py` → expect a line like `CAP            = 3` (was ~line 64).
   Not found or value ≠ 3 → the governor changed since authoring → re-read `orchestrator.py` fully;
   if `CAP`, `lease`, or the `--pool` clamp in `main()` no longer exist → **Abort A1**.
2. `grep -n "df-worker" engine/warm_pool.py` → expect the hardcoded name template
   `self.name = f"df-worker-{index}"` (was line 64) and `kill-session` inside `boot()` (was line
   80 — `boot()` kills its own session name before creating it; this is why Fork F1 exists).
   Missing → **Abort A1**.
3. `cd engine && python3 -c "import orchestrator; print(orchestrator.CAP, orchestrator.CLAIMANT)"`
   → expect `3 <hostname>-pid<NNN>`. ImportError/traceback → **Abort A1**.
4. `python3 engine/halt.py status` → expect `RUNNING -- no HALT file present.`; also
   `ls engine/store/BACKOFF 2>/dev/null` → expect no such file. HALT present → **Abort A2**.
   BACKOFF present: read its `until` field; if < 20 min away, sleep past it (it self-clears) and
   re-check; otherwise **Abort A2** (someone hit a usage limit recently — don't pile on).
5. `env | grep -E "ANTHROPIC_API_KEY|ANTHROPIC_AUTH_TOKEN"` → expect empty. If set, prefix every
   orchestrator/harness invocation with `env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN` (the
   engine exits hard otherwise — that exit is correct behaviour, not a bug).
6. `ls engine/store/queue/` → expect exactly one file,
   `20260704T0630Z-project-digest-list-and-project-2.json`, and
   `grep '"status": "deferred"' engine/store/queue/20260704T0630Z-*.json` → match (verified
   2026-07-06: it carries both `"priority": "deferred"` and `"status": "deferred"`, so
   `dispatchable()` skips it). Other live tickets present → **Fork F2**. Record
   `ls engine/store/done/ | wc -l` as the done-count baseline.
7. Execution context self-check: `echo ${TMUX:-none}`; if inside tmux,
   `tmux display-message -p '#S'`. Session name matches `df-worker-*` → **Fork F1 Route B**.
   Also `pgrep -fl orchestrator.py` — a live orchestrator process means an engine run is managing
   you or the store right now → **Fork F1 Route B** regardless of session name.
8. `tmux -V && command -v claude && claude --version` → all succeed. tmux missing → **Abort A1**
   (the engine cannot run here). Note: `tmux ls` saying `no server running` is FINE — the
   orchestrator's first `new-session` starts the server.

## Moves

1. **Build the lease-race harness.**
   - **Do:** `mkdir -p engine/tests/wg-t1-06` then write `engine/tests/lease_race.py` with this
     exact contract — CLI: `python3 engine/tests/lease_race.py --tickets N --claimants M`
     (defaults 200/8). Behaviour: (a) `sys.path.insert(0, <engine dir>)` (parent of the tests
     dir), `import orchestrator`; (b) create scratch dirs
     `engine/tests/.lease-race-scratch/queue` and `.../running` (delete any prior scratch first);
     (c) write N minimal ticket JSONs (`{"ticket": "<name>"}`) into the scratch queue; (d) spawn M
     OS processes via `multiprocessing.get_context("spawn")` — each child re-imports
     `orchestrator`, sets `orchestrator.Q = <scratch queue>` and `orchestrator.RUN = <scratch
     running>` (module globals; `lease()` reads them at call time), shuffles the full ticket-file
     list with a per-process seed, calls `orchestrator.lease(fname)` on every name, and returns
     the list of names it won; (e) parent asserts: total wins == N, no name in two win-lists,
     scratch queue empty, scratch running has N files, and every file in running parses as JSON
     with non-empty `claimed_by` and `claimed_at` (ownership survives the race); (f) on success
     print `LEASE RACE OK: <N> tickets, <M> claimants, <N> unique wins, 0 double-claims`, remove
     the scratch dir, exit 0; on any assertion failure print the offending ticket names, LEAVE the
     scratch dir in place as evidence, exit 1. Smoke it:
     `python3 engine/tests/lease_race.py --tickets 20 --claimants 4`.
   - **Expect:** smoke run prints `LEASE RACE OK: 20 tickets, 4 claimants, 20 unique wins, 0
     double-claims`, exit 0, and `engine/tests/.lease-race-scratch` is gone.
   - **Failure signal:** traceback about pickling / spawn importing the child function, or
     `orchestrator` import errors inside children.
   - **Counter-move:** keep the child function at module top level (spawn requires importability)
     and pass all paths as plain-string args. If spawn still fights you after one fix attempt,
     switch to `multiprocessing.get_context("fork")` (fine for this workload on macOS). If BOTH
     contexts fail, fall back to `threading` with M threads (os.rename releases the GIL; still a
     genuine race). A failure of the ASSERTIONS (not the plumbing) is not a harness bug → treat as
     Move 2's failure signal.

2. **Run the full contention race.**
   - **Do:** `python3 engine/tests/lease_race.py --tickets 200 --claimants 8 2>&1 | tee engine/tests/wg-t1-06/lease-race.log`
   - **Expect:** `LEASE RACE OK: 200 tickets, 8 claimants, 200 unique wins, 0 double-claims`,
     exit 0. (This replays dark-factory's historical 200×8 claim-next.sh stress bar against the
     CURRENT `lease()` implementation, which added the post-rename ownership write.)
   - **Failure signal:** any double-claim, wins ≠ 200, or a running-dir file missing
     `claimed_by`/`claimed_at`.
   - **Counter-move:** re-run once (rule out a harness race in the parent's bookkeeping). If the
     failure reproduces, the CAS mutex the whole engine rests on is broken → **Abort A3** with
     both logs and the preserved scratch dir listed as evidence. Do NOT patch `orchestrator.py`.

3. **Fork checkpoint — execution context.**
   - **Do:** apply Recon check 7's result: inside a `df-worker-*` session or a live
     `orchestrator.py` process exists → take **Fork F1 Route B** (which ends this run via
     **Abort A4** after committing Moves 1–2 work). Otherwise proceed to Move 4.
   - **Expect:** a plain terminal / non-worker tmux session and no live orchestrator process.
   - **Failure signal:** you are `df-worker-N` — running Move 5 would `kill-session` your own
     session and a managing parent would reap-timeout and reboot workers mid-test.
   - **Counter-move:** → Fork F1 Route B (never "just try it").

4. **Stage 6 no-op test tickets.**
   - **Do:** `STAMP=$(date -u +%Y%m%dT%H%M%SZ)`; for n in 1..6 write
     `engine/store/queue/${STAMP}-wg-t1-06-noop-${n}.json` containing exactly:
     `{"ticket": "<filename minus .json>", "kind": "instruction", "title": "T1-06 warm-pool no-op probe <n>", "source": "backlog/wargames/T1-06-warm-pool-n2.md", "executor": "swagger", "priority": "normal", "requested_at": "<date -u +%Y-%m-%dT%H:%M:%SZ>", "requested_by": "wg-t1-06 executor", "prompt": "Warm-pool plumbing probe (war game T1-06). Make NO edits to any repository file and do NOT run git. Your dispatch wrapper already instructs you to write a JSON status report to engine/store/results/<your ticket id>.json — write exactly that file with status done and files_changed [] and nothing else, then reply ACK as instructed."}`
     No `verify_kind`, no `artifacts`, no `verify_command` — the orchestrator's `verify()`
     passes such tickets on `artifact_ok()` alone (verified in code 2026-07-06).
   - **Expect:** `ls engine/store/queue/*.json | wc -l` → 7 (6 probes + 1 deferred); all 6 parse
     (`python3 -c "import json,glob; [json.load(open(f)) for f in glob.glob('engine/store/queue/*wg-t1-06-noop*')]"`).
   - **Failure signal:** JSON parse error (the orchestrator would skip-and-warn unparseable
     tickets, silently gutting the concurrency test).
   - **Counter-move:** fix the file in place before launching; re-run the parse check.

5. **Launch the live N=3 run (requesting 5 to prove the clamp).**
   - **Do:** from the repo root, launch in the BACKGROUND (the run can take 5–20 min — do not
     block a foreground Bash call on it):
     `nohup python3 engine/orchestrator.py --pool 5 --model sonnet --max-wall 1800 --teardown > engine/tests/wg-t1-06/live-run.log 2>&1 &`
     Then poll every ~30 s: `grep -c "=== REPORT ===" engine/tests/wg-t1-06/live-run.log`
     (0 = still running) and `tail -5` the log.
   - **Expect (early lines, within ~2 min):** a `[cap]` line — `requested --pool 5 exceeds hard
     CAP=3 ... clamping to 3`; the banner showing `pool=3`; `[pool] 3 warm worker(s) booted`;
     one `[skip]` line for the deferred project-digest ticket; three `[dispatch]` lines naming
     `df-worker-1`, `df-worker-2`, `df-worker-3`.
   - **Failure signal:** (a) no `[cap]` line but the banner says `pool=5` → governor regressed
     → **Abort A3**. (b) `TimeoutError: worker df-worker-N REPL never became ready` → **Fork F3**.
     (c) `[backoff]` / `[halt]` lines appear → see counter-move.
   - **Counter-move:** for (c): the run degrades gracefully by design — let the process exit on
     its own, never delete `engine/store/BACKOFF` or `HALT`; then **Abort A5** (BACKOFF) or
     **Abort A2** (HALT). If the process dies with a Python traceback, save the log and → **Abort A3**.

6. **Mid-run observation (while Move 5 is still running).**
   - **Do:** once 3 `[dispatch]` lines have appeared: `tmux ls` and `ls engine/store/running/`
     and `grep wg-t1-06-noop engine/store/audit.jsonl`.
   - **Expect:** `tmux ls` lists exactly `df-worker-1`, `df-worker-2`, `df-worker-3` and NO
     `df-worker-4`/`df-worker-5` (the clamp is physical, not just printed); `running/` holds up to
     3 probe tickets, each containing `claimed_by` equal to one orchestrator identity
     (`<host>-pid<orchestrator pid>`) and a `claimed_at`; audit lines carry worker + session_id.
   - **Failure signal:** a 4th df-worker session exists → clamp print lied → **Abort A3**.
     A running probe ticket with missing/empty `claimed_by` → ownership write regressed → record
     it; if ALL are missing it → **Abort A3**.
   - **Counter-move:** none beyond the aborts — this move is observation only; do not touch
     running tickets or workers.

7. **Reap the run and sweep the evidence.**
   - **Do:** wait for `=== REPORT ===` in the log, then run, in order:
     `grep -A10 "=== REPORT ===" engine/tests/wg-t1-06/live-run.log`;
     `ls engine/store/done/ | grep -c wg-t1-06-noop`;
     `ls engine/store/results/ | grep -c wg-t1-06-noop`;
     `ls engine/store/queue/`;
     `grep -c wg-t1-06-noop engine/store/audit.jsonl`;
     `python3 -c "import json; ws={json.loads(l)['worker'] for l in open('engine/store/audit.jsonl') if 'wg-t1-06-noop' in l}; print(sorted(ws))"`;
     `tmux ls 2>&1`.
   - **Expect:** REPORT shows all 6 probes `done` and `peak concurrency 3/3`; done-grep → 6;
     results-grep → 6; queue/ contains ONLY the deferred project-digest ticket (byte-identical —
     re-run Recon 6's grep); audit count ≥ 6 with ≥ 2 distinct workers in the set; `tmux ls` shows
     no `df-worker-*` (teardown ran).
   - **Failure signal:** peak `2/3` with all 6 done — acceptable but note it in the results file
     (dispatch raced a fast finish). Peak `1/3` → the pool never went parallel → **Abort A3**.
     Probes `failed(timeout)` or re-queued → check the log's `[reboot]`/`[reap]` lines.
   - **Counter-move:** for re-queued/failed probes: one full re-run of Moves 5–7 with the SAME
     ticket files (they're back in queue/) is allowed. A second failure → **Abort A3** with both
     logs. Leftover `df-worker-*` sessions despite `--teardown`: kill them by name
     (`tmux kill-session -t df-worker-N`) and note it — that IS a finding.

8. **Record findings, commit, and finish.**
   - **Do:** (a) append one line to `backlog/2026-07-04-loose-ends-ledger.md`:
     `- [wg-t1-06] two simultaneous orchestrator.py processes are UNSAFE: WarmWorker names are hardcoded df-worker-<n> and boot() kill-sessions its own name, so a second process destroys the first's live workers. Lease() itself is contention-safe (200x8 race clean). Needs worker-name namespacing before any multi-orchestrator future.`
     (b) `git status --short` — confirm the ONLY changes are: `engine/tests/lease_race.py`, the
     two logs under `engine/tests/wg-t1-06/`, the ledger line, and the engine-store ticket
     movements (queue→done, results, audit). Any OTHER modified repo file means a probe worker
     disobeyed its no-edit prompt → `git diff` it, revert if trivial whitespace, otherwise
     **Abort A3** (a no-op ticket editing the repo is a containment failure worth a human look).
     (c) commit everything above with message
     `feat(engine): T1-06 warm pool N=3 proven — lease race 200x8 clean, CAP clamp live, peak 3/3`
     and push. (d) if this run was dispatched via the engine, the dispatch wrapper's results-file
     instruction stands — write your own ticket's results JSON with `status: done`, the commit
     sha, and a one-line note including the peak-concurrency figure.
   - **Expect:** clean `git status` afterwards; commit visible in `git log --oneline -1`.
   - **Failure signal:** push rejected (remote moved).
   - **Counter-move:** `git pull --rebase` then push; on conflict in any file you did not author
     this session, stop rebasing and **Abort A4** with the conflict description.

## Forks

**F1 — Execution context (the self-hosting hazard).**
**Trigger:** Recon 7 — executor is inside a tmux session named `df-worker-*`, or `pgrep -fl
orchestrator.py` shows a live orchestrator.
**Route A** (plain terminal / non-worker session, no live orchestrator): run all moves 1–8.
**Route B** (inside a worker or a live orchestrator exists): the live-pool leg is structurally
unsafe here — Move 5 would kill your own session, and a managing parent (WORKER_TIMEOUT 240 s)
would reap-timeout this long ticket and reboot workers mid-test. Execute Moves 1–2 only (the race
harness needs no tmux), commit that work (Move 8a/8c minus the live-run claims, commit message
`feat(engine): T1-06 partial — lease race 200x8 clean; live N=3 leg parked`), then **Abort A4**
to park the live leg. Never attempt session-renaming tricks to dodge the collision.

**F2 — Unexpected live tickets in queue/ at Recon 6.**
**Trigger:** queue/ contains dispatchable tickets other than the deferred project-digest one.
**Route A** (1–2 extra tickets, and their `title`/`prompt` read as small bounded work): proceed —
they were queued to be executed and will be co-drained by your sonnet pool; list them in your
results note and exclude them from every probe count (all Move 7 greps already filter on
`wg-t1-06-noop`).
**Route B** (3+ extra tickets, or any that looks expensive/long-running — a build, a campaign, a
migration): do not burn a surprise batch inside a plumbing test → **Abort A4**, naming the
tickets and asking whether to co-drain or wait.

**F3 — Worker boot failure at Move 5.**
**Trigger:** `TimeoutError: worker df-worker-N REPL never became ready`.
**Route A** (pane shows a usage-limit signature — check `tmux capture-pane -t df-worker-N -p`
for `usage limit` / `rate limit` / `429`): the account is limited; write nothing, wait 15 min,
retry Move 5 once; second limit hit → **Abort A5**.
**Route B** (pane shows anything else — login prompt, model error, shell error): capture the pane
text to `engine/tests/wg-t1-06/boot-failure.txt`, retry Move 5 once; second failure → **Abort A3**
with the pane capture as evidence.

## Assumptions ledger

- **A sonnet REPL boots within warm_pool's 90 s timeout on this machine.** Plausible: proven at
  N=1 on 2026-07-03 (constellation ticket); 3 sequential boots are unproven. False → Fork F3.
- **3 worker sessions + the executor's own session (~4 concurrent) stays under the account's
  429 wall.** Plausible: CAP=3 was chosen precisely as "well under the ~5–7 per-account wall"
  (orchestrator.py comment). False → the BACKOFF governor engages, which is itself a useful
  observation → Abort A5 records it.
- **The queue still holds only the deferred project-digest ticket at execution time.** Plausible
  today (verified 2026-07-06); this war game may run weeks later. False → Fork F2.
- **`multiprocessing` spawn (or fork) works in this python3.** Plausible: stock macOS
  python3 supports both. False → Move 1's counter-move degrades to threads; note the degradation
  in the results file (threads still race `os.rename` genuinely).
- **Leaving 6 probe tickets in `done/` forever is acceptable.** Plausible: the store is a growing
  ledger by convention and retention is ticket T1-10's job; the `wg-t1-06-noop` prefix makes them
  trivially greppable for a future prune. If David objects at review → a one-line cleanup
  (`git mv` them to a quarantine dir) is a follow-up note, not a redo.

## Abort conditions

Every abort: write `engine/store/needs-decision/wg-t1-06-warm-pool-n2.json` as
`{"ticket": "wg-t1-06-warm-pool-n2", "question": "<one sentence>", "proposed": "<your recommended answer>", "note": "<evidence paths>"}`,
leave this ticket in `running/` if engine-dispatched, and stop. Never guess past an abort.

- **A1 — engine drifted.** Recon 1–3/8 fail (symbols gone, import broken, tmux absent). Question:
  "Engine refactored since 2026-07-06 authoring — re-author T1-06 against current engine/?"
- **A2 — HALT present (at recon or appearing mid-run), or BACKOFF present and > 20 min out.**
  Question: "Factory halted/backing off (<reason from flag payload>) — clear and re-run T1-06,
  or hold?" Never remove either flag yourself.
- **A3 — stop-the-line engine finding.** Any of: reproducible double-claim (Move 2), missing
  `[cap]` clamp (Move 5), a 4th worker session (Move 6), peak 1/3 (Move 7), second live-run
  failure, Python traceback in the orchestrator, or a no-op probe editing the repo (Move 8b).
  Question: "T1-06 found a real engine defect: <one-line finding> — evidence at
  engine/tests/wg-t1-06/. Fix under a new ticket before re-running?" Do not hot-fix engine code.
- **A4 — needs David's call, no defect.** F1 Route B (question: "T1-06's live N=3 leg cannot run
  from inside a df-worker session — run it from a plain terminal, or dispatch it as a solo
  engine run with nothing else active?"), F2 Route B, or Move 8's foreign rebase conflict.
- **A5 — usage limit.** BACKOFF written during the run, or F3 Route A's second hit. Question:
  "T1-06 hit the 429/usage wall with N=3+self — resume after cooldown, or schedule this run
  off-peak?" Note in the payload that any re-queued probe tickets are harmless no-ops and will
  drain on the next engine run.

## Verification

Run from the repo root. All must pass for "done":

```bash
# 1. Harness exists and the full race is green (re-runnable any time):
python3 engine/tests/lease_race.py --tickets 200 --claimants 8
# → prints "LEASE RACE OK: 200 tickets, 8 claimants, 200 unique wins, 0 double-claims", exit 0

# 2. Live run evidence — clamp, pool size, completion, concurrency:
grep "exceeds hard CAP=3" engine/tests/wg-t1-06/live-run.log        # → 1 line ([cap] clamp)
grep "3 warm worker(s) booted" engine/tests/wg-t1-06/live-run.log   # → 1 line
grep -c "wg-t1-06-noop.*: done" engine/tests/wg-t1-06/live-run.log  # → 6
grep "peak concurrency" engine/tests/wg-t1-06/live-run.log          # → "peak concurrency 3/3"
                                                                    #   (2/3 = pass-with-note)

# 3. Store evidence:
ls engine/store/done/ | grep -c wg-t1-06-noop                       # → 6
ls engine/store/results/ | grep -c wg-t1-06-noop                    # → 6
python3 -c "import json; ws={json.loads(l)['worker'] for l in open('engine/store/audit.jsonl') if 'wg-t1-06-noop' in l}; print(len(ws))"  # → 2 or 3

# 4. Negative checks — what must NOT have changed:
grep '"status": "deferred"' engine/store/queue/20260704T0630Z-project-digest-list-and-project-2.json  # → still there, still deferred
tmux ls 2>&1 | grep -c df-worker                                    # → 0 (teardown ran)
git status --short | grep -vE "engine/(tests|store)|backlog/2026-07-04-loose-ends" | wc -l  # → 0
grep -c "wg-t1-06" backlog/2026-07-04-loose-ends-ledger.md          # → 1 (the namespacing finding)
```

Partial pass (F1 Route B): check 1 green + the Moves 1–2 commit + `needs-decision/` entry for the
parked live leg. That is a legitimate exit, not a failure.

## Executor notes (sonnet)

- **Scope fence:** do NOT edit `engine/orchestrator.py`, `engine/warm_pool.py`, or
  `engine/halt.py` — this is a *proving* ticket; every defect found routes to Abort A3, never to a
  hot-fix. Do not touch the deferred project-digest ticket, any `done/` ledger entry, or the
  `wake.py`/launchd machinery. Never delete `HALT` or `BACKOFF`.
- New files allowed: `engine/tests/**` and the six probe tickets only. Probe prompts must stay
  single-line JSON strings (tmux `send-keys -l` cannot inject real newlines — SPK-D1).
- Interactive `claude` only, always. If any instinct says "just use `claude -p` for the probes,
  it's cheaper" — that instinct is banned (metered billing).
- Prefer HITL over guessing: every genuinely ambiguous situation in this game already has an
  abort lane. Use it. A parked half-result with clean evidence beats an improvised full result.
- **The most likely rabbit hole:** making concurrent orchestrator processes safe (worker-name
  namespacing, per-process session prefixes, store locks). Do not build any of it. The war game
  only requires the one-line ledger finding in Move 8a. A close second: polishing the race
  harness into a pytest suite — a plain script with asserts is the deliverable; stop there.
