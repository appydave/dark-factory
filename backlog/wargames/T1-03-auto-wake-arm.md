# T1-03 — Arm auto-wake dispatch leg — first live run

| field | value |
|---|---|
| ticket | wg-t1-03-auto-wake-arm |
| track / size / priority | T1 Engine / S / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

The auto-wake watcher (`engine/wake.py` + launchd `com.appydave.dark-factory-wake`) shipped
2026-07-06 with its notification leg live and its dispatch leg deliberately DISARMED. This ticket
arms the dispatch leg for real: write the WAKE-ARMED operating protocol (`docs/wake-armed-protocol.md`),
close the traceability gap that made the 07-06 anomaly untraceable (arm/disarm events currently
leave NO wake.log line), run a bounded forensic pass on that anomaly (WAKE-ARMED found existing at
2026-07-06T08:19:36Z with no agent admitting to creating it), and prove one live
queue-drop → launchd fire → wake.py → orchestrator auto-dispatch → ticket-done cycle with a canary
ticket. Done looks like: protocol doc exists with the anomaly recorded, arm/disarm events append to
wake.log, one canary ticket demonstrably ran end-to-end via auto-wake (or is verifiably staged to,
if this executor is itself engine-dispatched — see Fork F1), and the factory ends ARMED.

## Locked context

- **Interactive `claude` only — no `-p`, no headless, no Agent SDK, ever** (metered billing). wake.py
  never calls claude; only `orchestrator.py` boots workers. Preserve that split exactly.
- **HALT and BACKOFF flags win over everything** (decisions.md via kill-switch idiom). Never arm over
  a HALT; never fight a BACKOFF.
- **Q4: everything through the engine** — this ticket itself is probably being run by a live
  orchestrator. That is why Fork F1 exists; respect it.
- **Ticket-first** (queue/.CONVENTION.md): the canary is a real ticket JSON that moves
  queue/ → running/ → done/ like any other.
- **Docs lag code**: trust only the Recon checks below, not `docs/auto-wake.md`'s status line.

## Recon (verify before any work)

1. `bin/factory-wake status` → expect `DISARMED`, `launchd loaded: yes`, and the last wake.log lines.
   - If `launchd loaded: no` → run `bash engine/launchd/install.sh` (idempotent: sed plist, unload, load), re-check.
   - If `ARMED` → **anomaly recurrence** (nothing should have armed it). Capture `cat engine/store/WAKE-ARMED`
     (has `ts` + `by`), run `bin/factory-wake disarm`, and treat this as first-class evidence for Move 1 / Fork F3.
2. `ls -la engine/store/ | grep -E 'HALT|BACKOFF|wake'` → expect `wake.log` and `.wake-state.json` only;
   `HALT`, `BACKOFF`, `WAKE-ARMED`, `.wake.lock` all absent.
   - `HALT` present → **Abort A1**. `BACKOFF` present → wait for its `until` to pass (it self-clears), re-check.
   - `.wake.lock` present → read the pid, `ps -p <pid> -o command=`; a live orchestrator.py means an engine
     run is in flight (feeds Fork F1); a dead/unrelated pid is stale — leave it, wake.py takes it over safely.
3. `python3 engine/wake.py && tail -3 engine/store/wake.log` → expect a `quiet: no new dispatchable tickets`
   line (as of authoring, queue/ holds exactly one ticket, `20260704T0630Z-project-digest-list-and-project-2.json`,
   skipped as "deferred by David").
   - If the tail shows `wake: N new ticket(s)` → real dispatchable tickets are sitting in queue/. Do NOT arm
     until you know what they are: read each, and route via Fork F2.
4. `grep -o 'ANOMALY[^"]*' engine/store/done/20260706T0932Z-auto-wake-and-notify-watcher.json | head -c 600`
   → expect the anomaly record (WAKE-ARMED found existing, ts 2026-07-06T08:19:36Z, by=davidcruwys, builder
   never called arm, disarmed immediately). Missing → the done ticket moved; find it with
   `grep -rl "ANOMALY" engine/store/done/` before Move 1.
5. `ps aux | grep '[o]rchestrator.py'` and `tmux ls 2>/dev/null | grep df-worker` → record both. A live
   orchestrator.py process almost certainly means YOU are its worker. This determines Fork F1's route at Move 5.
6. `ls docs/wake-armed-protocol.md` → expect **absent** (this ticket creates it). If present → a prior run of
   this war game got partway; read it, keep what is correct, APPEND rather than rewrite (assessment-mode rule),
   and skip any move whose artifact already verifiably exists.

## Moves

**Move 1 — Anomaly forensics (hard timebox: 30 minutes).**
- **Do:** Work these leads in order, noting each result: (a) known facts: the anomalous `WAKE-ARMED` carried
  `ts 2026-07-06T08:19:36Z, by=davidcruwys`, and that timestamp matches `.wake-state.json`'s `updated_at` and two
  same-second `quiet` lines in wake.log (the builder's own back-to-back debounce test) — to the second.
  (b) `grep -c 'factory-wake\|wake\.py' ~/.zsh_history 2>/dev/null` then eyeball matches for an `arm` near that time.
  (c) `git log --all --oneline -- engine/store/WAKE-ARMED` (was it ever committed?).
  (d) Transcript sweep: over `~/.claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/*.jsonl`, grep for
  `"command"` entries containing both `wake` and `arm`, and separately for `WAKE-ARMED`, filtered to timestamps
  `2026-07-06T08:1`. (Authoring-time result, 2026-07-06: this sweep found ZERO arm executions — only prose
  mentions in sessions `78dc18bd` and `90b578a0`. Expect the same; a smoking gun would be new information.)
- **Expect:** Either a specific command + timestamp that created the file (→ Fork F3), or — the likely outcome —
  no cause found. Both are acceptable endings for this move.
- **Failure signal:** You are past 30 minutes and still spelunking transcripts.
- **Counter-move:** Stop immediately. Record verdict `UNRESOLVED — mitigated by arm/disarm logging (Move 2)`
  with the evidence table in the protocol doc's Incident log (Move 3). Do not extend the timebox.

**Move 2 — Close the traceability gap in `engine/wake.py`.**
- **Do:** `cmd_arm()` (~line 234) and `cmd_disarm()` (~line 244) currently only `print()`; wake.log never records
  arm/disarm flips — this is exactly why Move 1's anomaly was untraceable. Add one `log(...)` call to each, using
  the module's existing `log()` helper: in `cmd_arm` after writing the flag,
  `log(f"ARMED by {payload['by']} (pid={os.getpid()} ppid={os.getppid()})")`; in `cmd_disarm`,
  `log("DISARMED (flag removed)")` when it existed and `log("disarm no-op (already disarmed)")` when not.
  Touch nothing else in the file. Then test with a single compound command so the armed window is < 1 second:
  `bin/factory-wake arm && bin/factory-wake disarm && tail -4 engine/store/wake.log`.
- **Expect:** wake.log tail shows one `ARMED by davidcruwys (pid=… ppid=…)` line and one `DISARMED (flag removed)`
  line; `bin/factory-wake status` still prints `DISARMED`.
- **Failure signal:** Python traceback from wake.py, or the tail shows no new lines.
- **Counter-move:** Fix once. If a second attempt still errors → `git checkout -- engine/wake.py` and **Abort A3**.
  If the flag file got left behind (`ls engine/store/WAKE-ARMED`) → `bin/factory-wake disarm` before anything else.

**Move 3 — Author `docs/wake-armed-protocol.md`.**
- **Do:** Write the protocol doc with exactly these sections: `## Purpose` (WAKE-ARMED vs HALT — allow-gate vs
  stop-gate, both flag-files per docs/kill-switch-spec.md); `## Preconditions to arm` (the Recon checklist above,
  as a reusable list); `## Arm / disarm` (the bin/factory-wake commands + note that both now log to wake.log);
  `## Concurrency law` (NEVER let a second orchestrator boot while one is live — `engine/warm_pool.py`
  `boot()` runs `tmux kill-session -t df-worker-<n>` before creating, so a second boot kills a live worker's
  session; the `.wake.lock` live-pid check is the guard — pre-write it with a live orchestrator's pid when arming
  during an engine run); `## Supervised live-fire procedure` (both routes from Fork F1, written as runnable steps);
  `## Disarm triggers` (disarm whenever you would HALT; before handing the machine over; before deliberate
  429-saturation runs like T1-02); `## Steady-state policy` (ARMED is the factory's normal state from the date
  this ticket completes — David can veto at triage); `## Incident log` (entry `2026-07-06 — WAKE-ARMED present,
  unexplained` with the known facts + Move 1 verdict, plus an entry template); `## Live-fire log` (empty list
  under an HTML comment `<!-- appended by canary tickets and drills -->` — the exact literal text `- LIVE-FIRE 20`
  must NOT appear anywhere in the doc's prose, because the canary's verify greps for it).
- **Expect:** File exists; `grep -c '^## ' docs/wake-armed-protocol.md` → 9; `grep -c '^- LIVE-FIRE 20' docs/wake-armed-protocol.md` → 0.
- **Failure signal:** Section count wrong, or the live-fire literal appears in prose.
- **Counter-move:** Edit until both greps pass — this is mechanical, no fork.

**Move 4 — Stage the canary ticket (outside queue/).**
- **Do:** `mkdir -p engine/store/.staged` and write `engine/store/.staged/<STAMP>-wake-canary-live-fire.json`
  where `<STAMP>` is `date -u +%Y%m%dT%H%M%SZ`, containing exactly:
  ```json
  {
    "ticket": "<STAMP>-wake-canary-live-fire",
    "kind": "instruction",
    "title": "T1-03 canary: auto-wake live-fire proof",
    "source": "backlog/wargames/T1-03-auto-wake-arm.md",
    "executor": "swagger",
    "priority": "high",
    "requested_at": "<UTC now>",
    "requested_by": "wg-t1-03 executor (auto-wake live-fire)",
    "depends_on": [],
    "prompt": "Append exactly one line to the '## Live-fire log' section of docs/wake-armed-protocol.md in this repo: '- LIVE-FIRE <current UTC ISO-8601 timestamp> — dispatched by auto-wake, executed by an engine worker.' Make no other edits and do not commit.",
    "artifacts": ["docs/wake-armed-protocol.md"],
    "verify_command": "grep -q '^- LIVE-FIRE 20' docs/wake-armed-protocol.md"
  }
  ```
  (The `artifacts` + `verify_command` fields trigger orchestrator.py's `verify_artifacts_fallback` — verified
  present at orchestrator.py ~lines 450–491 — so the engine itself verifies the live-fire.)
- **Expect:** `python3 -c "import json;json.load(open('engine/store/.staged/<STAMP>-wake-canary-live-fire.json'))"`
  exits 0. Nothing appears in queue/ yet; wake.log stays quiet (launchd watches queue/, not .staged/).
- **Failure signal:** JSON parse error, or a wake.log line mentioning the canary (you wrote it into queue/ by mistake).
- **Counter-move:** Fix the JSON. If it landed in queue/ early: it is harmless while DISARMED (notification only) —
  `mv` it back to `.staged/`, and note that `.wake-state.json` now remembers it; that is fine, the later `mv` back
  into queue/ re-adds it as "new" only if it left the pending set in between (it does — claimed/absent files drop
  out of last_seen on the next pass; run `python3 engine/wake.py` once after the mv-back to confirm a fresh quiet line).

**Move 5 — Arm and fire (route chosen by Fork F1).**
- **Do:** Re-run Recon check 5 (`ps aux | grep '[o]rchestrator.py'`). Then → **Fork F1** decides Route A
  (no live orchestrator: synchronous supervised fire) or Route B (live orchestrator — you are its worker:
  deferred fire). Execute the chosen route's steps as written in the fork.
- **Expect:** Route A: within ~10–30s of the `mv` into queue/, wake.log gains
  `wake: 1 new ticket(s) [<STAMP>-wake-canary-live-fire.json] armed=True action=dispatched (pid=<N>)` and
  `.wake.lock` holds that pid. Route B: `.wake.lock` holds the LIVE parent orchestrator's pid, `WAKE-ARMED`
  exists (and wake.log shows the ARMED line), the canary sits in `.staged/`, and the detached drop-watcher
  process is alive.
- **Failure signal:** Route A: 60s pass with no new wake.log line → launchd did not fire → **Fork F2**.
  Route A: line says `skip-dispatch (live lock pid=N)` → something live holds the lock — `ps -p N -o command=`;
  if it is a real orchestrator.py you missed it in Recon 5, switch to Route B; if it is an unrelated process
  that reused the pid, `rm engine/store/.wake.lock` and `python3 engine/wake.py` to retry.
- **Counter-move:** As per failure signal; second consecutive unexplained non-fire → **Abort A4**.

**Move 6 — Observe / hand off the cycle.**
- **Do:** Route A: watch it run — `tmux ls` shows `df-worker-1`; poll until the canary leaves running/:
  `ls engine/store/done/ | grep wake-canary` and `ls engine/store/results/ | grep wake-canary`; then confirm
  `grep '^- LIVE-FIRE 20' docs/wake-armed-protocol.md`. Append the observed timeline (drop→fire→dispatch→done,
  with timestamps from wake.log) to the protocol doc's Live-fire log entry. Route B: you cannot observe (the
  fire happens after your parent exits). Instead: paste the post-flight check block into the protocol doc's
  live-fire section — `grep 'action=dispatched' engine/store/wake.log && ls engine/store/done/ | grep wake-canary
  && grep '^- LIVE-FIRE 20' docs/wake-armed-protocol.md` — and fire a notification David will see:
  `osascript -e 'display notification "auto-wake ARMED — canary will fire after this engine run exits; post-flight check is in docs/wake-armed-protocol.md" with title "dark-factory T1-03"'`.
- **Expect:** Route A: canary in done/, LIVE-FIRE line present, worker torn down (wake dispatch uses
  `--teardown`), `.wake.lock` pid now dead. Route B: doc contains the post-flight block; notification call exited 0.
- **Failure signal:** Route A: canary bounces back to queue/ (worker timeout re-queue) or lands as
  `failed(verify)` in the orchestrator report; or a `BACKOFF` file appears (usage-limit hit).
- **Counter-move:** One re-queue/retry is normal engine behaviour — let MAX_RETRY play out. BACKOFF: wait out
  ONE cooldown (it self-clears, ~15 min) while staying disarm-ready; a second BACKOFF → **Abort A2**. Verify-fail
  twice → read the worker's result notes in `engine/store/results/`, fix the doc section header mismatch if that
  is the cause (most likely), re-stage once; third failure → **Abort A4**.

**Move 7 — End state, cross-links, commit.**
- **Do:** Confirm end state ARMED: `bin/factory-wake status` → `ARMED` (this is the deliverable; leave it armed
  unless an abort or Fork F3-Route-B fired). Update `docs/auto-wake.md`: change the `**Status**` line to note the
  dispatch leg was armed on this date and add a pointer to `docs/wake-armed-protocol.md` in §5 and §8. Then commit
  and push everything (wake.py, both docs, this war game's status, store files that changed):
  `git add -A && git commit -m "feat(engine): T1-03 auto-wake dispatch leg armed — protocol doc + arm/disarm logging + live-fire" && git push`.
- **Expect:** Clean push; `git status` clean; `bin/factory-wake status` shows ARMED with the ARMED line visible in
  its wake.log tail.
- **Failure signal:** Push rejected (remote moved).
- **Counter-move:** `git pull --rebase` then push (standing preference: own the rebases). Conflicts in files this
  ticket did not touch → stop rebasing that file, `git rebase --abort`, and **Abort A5**.

## Forks

**F1 — Live orchestrator present at fire time?** *Trigger:* Recon 5 / Move 5's `ps` check.
- **Route A (no orchestrator.py process live):** You can fire synchronously and watch. Steps: (1) if a stale
  `.wake.lock` exists leave it (wake.py takes over dead pids); (2) `bin/factory-wake arm`; (3)
  `mv engine/store/.staged/<STAMP>-wake-canary-live-fire.json engine/store/queue/`; (4) proceed to Move 6 Route A.
- **Route B (an orchestrator.py is live — you are almost certainly its worker):** A synchronous fire is FORBIDDEN:
  wake.py sees no live `.wake.lock`, dispatches a second orchestrator, whose warm-pool boot `tmux kill-session`s
  `df-worker-1` — killing YOU mid-ticket. Steps: (1) write the live orchestrator's pid into the lock:
  `ps aux | grep '[o]rchestrator.py'` → `echo <pid> > engine/store/.wake.lock` (this makes wake.py skip-dispatch
  while it lives, and treat it as stale takeover the moment it dies — exactly the intended semantics);
  (2) `bin/factory-wake arm`; (3) start the detached drop-watcher:
  `nohup bash -c 'while ps -p <pid> >/dev/null 2>&1; do sleep 5; done; sleep 15; mv "$PWD/engine/store/.staged/<STAMP>-wake-canary-live-fire.json" "$PWD/engine/store/queue/"' >/dev/null 2>&1 &`
  run from the repo root (verify it is alive: `ps aux | grep '[w]ake-canary'` or by its bash pid); (4) proceed to
  Move 6 Route B. The fire then happens unattended after your parent exits: lock goes stale, launchd fires on the
  mv, wake.py takes over and dispatches — which is itself the truest possible test of the mechanism.

**F2 — launchd does not fire (Route A only).** *Trigger:* canary in queue/ 60s, no new wake.log line, but a manual
`python3 engine/wake.py` DOES produce the expected `wake: 1 new ticket(s) … action=dispatched` line (prove the
manual path before concluding launchd is at fault — but only run it manually if you intend the dispatch to happen).
- **Route A (first occurrence):** `bash engine/launchd/install.sh` (reload), re-stage a fresh canary filename
  (the state file now remembers the old one), retry once.
- **Route B (still dead after reinstall):** macOS launchd/TCC environment problem — out of scope to debug. Record
  diagnostics (`launchctl list | grep dark-factory`, plist contents, wake.log), leave the system ARMED only if the
  manual dispatch completed the canary cleanly (the mechanism works; the trigger is broken), and → **Abort A4**
  park with the question "launchd WatchPaths not firing — debug env or accept manual/cron trigger?".

**F3 — Anomaly forensics finds a smoking gun (Move 1).** *Trigger:* a command/agent/timestamp is identified that
created WAKE-ARMED on 07-06.
- **Route A (one-off):** e.g. a sibling agent's test invocation — record cause + evidence in the Incident log,
  no further action (Move 2's logging already prevents recurrence-invisibility). Continue the war game normally.
- **Route B (repeatable mechanism):** something arms the gate programmatically (a script, hook, or scheduled job
  that can re-create WAKE-ARMED unprompted). Do NOT proceed to arming: disarm, document, and → **Abort A6**.

## Assumptions ledger

1. **End-state ARMED is the deliverable.** Inferred from the ticket title ("Arm auto-wake dispatch leg") and
  David's portfolio triage; David never separately ratified "leave it armed permanently". If anything during the
  run makes permanent arming feel wrong (anomaly recurrence, flaky launchd, F3-B), do not guess — disarm and park
  to needs-decision with the evidence. The protocol doc + logging land regardless.
2. **The anomaly is probably unresolvable.** Authoring-time forensics (2026-07-06) already swept every dark-factory
  transcript for arm executions and WAKE-ARMED-touching commands in the 08:1x window: nothing. If Move 1 also finds
  nothing, `UNRESOLVED + logging mitigation` is an acceptable closure — that is the planned outcome, not a failure.
3. **launchd job still loaded months from now.** Verified loaded at authoring (`launchctl list` → `- 0
  com.appydave.dark-factory-wake`; plist in ~/Library/LaunchAgents with correct absolute paths). Recon 1 re-verifies;
  install.sh is the counter.
4. **queue/ still holds only the deferred project-digest ticket.** True at authoring. Recon 3 re-verifies; if real
  dispatchable tickets have accumulated (e.g. the war-game promotion script has started draining), arming will run
  them — that is by design (they were queued to run), but confirm they are wargame tickets before arming; anything
  unrecognizable → park to needs-decision rather than auto-running it.
5. **macOS notification popups cannot be machine-verified.** Call-path verification (osascript exits 0) is the
  accepted bar — precedent set by the auto-wake builder ticket's own verify transcript.
6. **This machine only.** Auto-wake v1 is a local launchd WatchPaths trigger; Roamy/fleet (decisions Q8) is
  explicitly not this ticket's problem.

## Abort conditions

All aborts: write `engine/store/needs-decision/wg-t1-03-auto-wake-arm.json` with
`{"ticket":"wg-t1-03-auto-wake-arm","question":"<the specific question>","proposed":"<your best route>","note":"<evidence one-liner>"}`,
leave the ticket in running/, ensure the factory is DISARMED (`bin/factory-wake disarm`) unless the abort text
says otherwise, and stop. Never guess past an abort.

- **A1 — HALT present** at any point. Question: "Factory is HALTed (<reason from HALT file>) — arm auto-wake after resume, or re-triage?"
- **A2 — Second BACKOFF during live-fire.** Usage limits are actively biting. Disarm. Question: "Two BACKOFFs during T1-03 live-fire — retry in a quieter window, or park arming until after T1-02 (429 proof)?"
- **A3 — wake.py edit cannot be made safe in two attempts.** Revert via `git checkout -- engine/wake.py` first. Question: "arm/disarm logging edit failing — proceed to arm without the traceability fix, or fix wake.py in a dedicated ticket first?"
- **A4 — Dispatch mechanism misbehaves** (unexplained repeated non-fire, canary fails verify 3×, launchd dead after reinstall, or any second orchestrator boots while one is live / a df-worker session dies unexpectedly — in that last case run `bin/factory-halt` FIRST, then disarm, then park). Question: specific to what broke, with the wake.log excerpt inlined.
- **A5 — Rebase conflict in files this ticket never touched.** The repo moved underneath the run. Question: "T1-03 work committed locally but push blocked by conflicting upstream changes in <files> — reconcile how?"
- **A6 — F3 Route B: a repeatable external armer exists.** Disarm. Question: "Found <mechanism> able to create WAKE-ARMED unprompted — kill it, or accept and log?"

## Verification

Run from the repo root. Route A = all checks now; Route B = pre-flight checks now, post-flight checks after the
engine run exits (the block is also pasted in the protocol doc).

```bash
# 1. Protocol doc exists with all 9 sections and no verify-literal leakage in prose
test -f docs/wake-armed-protocol.md && grep -c '^## ' docs/wake-armed-protocol.md   # → 9

# 2. Incident log carries the 07-06 anomaly with a verdict
grep -A2 '2026-07-06' docs/wake-armed-protocol.md | grep -Ei 'UNRESOLVED|cause'     # → 1+ line

# 3. arm/disarm now log (traceability gap closed)
grep -E 'ARMED by .*pid=' engine/store/wake.log                                     # → 1+ line
grep -n 'log(' engine/wake.py | grep -iE 'armed|disarm'                             # → 2+ hits

# 4. Live-fire happened (post-flight for Route B)
grep 'action=dispatched' engine/store/wake.log                                      # → 1+ line
ls engine/store/done/ | grep wake-canary                                            # → 1 file
ls engine/store/results/ | grep wake-canary                                         # → 1 file
grep '^- LIVE-FIRE 20' docs/wake-armed-protocol.md                                  # → 1 line

# 5. End state: ARMED, gates clean
bin/factory-wake status | head -1                                                   # → ARMED
ls engine/store/HALT engine/store/BACKOFF 2>&1 | grep -c 'No such'                  # → 2

# 6. Negative checks — what must NOT have changed
git log --oneline -1 -- engine/orchestrator.py engine/warm_pool.py engine/halt.py   # → predates this ticket
ls engine/store/queue/ | grep project-digest                                        # → deferred ticket untouched
tmux ls 2>/dev/null | grep -c df-worker                                             # → 0 (teardown ran; Route A)

# 7. Committed and pushed
git status --porcelain | wc -l                                                      # → 0
```

## Executor notes (sonnet)

- **Scope fence:** the ONLY code file you may edit is `engine/wake.py`, and only the two logging lines of Move 2.
  Do not touch `orchestrator.py`, `warm_pool.py`, `halt.py`, `status.py`, or the launchd plist (install.sh reload
  in F2-A is allowed). Do not add wake-awareness to status.py (real gap, different ticket). Do not build anything
  SSE/Switchboard-shaped — that is DF-7, explicitly deferred in docs/auto-wake.md §7.
- **Never run `claude` yourself in any form** — not to "simulate the worker", not `-p`, not anything. The
  orchestrator boots workers; you observe files, logs, and tmux from the outside.
- **The rabbit hole is Move 1.** Transcript archaeology is bottomless and the answer is probably not in there
  (authoring-time sweep came up empty). 30 minutes, hard stop, `UNRESOLVED` is a fine verdict — the logging fix
  is the real deliverable.
- **When in doubt about arming policy, park.** Arming an unattended dispatch loop is the one genuinely
  consequential action here; every abort path deliberately ends DISARMED. A needs-decision file costs David one
  minute; a wrongly-armed factory costs trust.
- **Style:** protocol doc in David's voice — terse, tables and checklists over prose, no marketing language
  (docs/david-style-patterns.md).
