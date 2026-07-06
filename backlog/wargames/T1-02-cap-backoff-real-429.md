# T1-02 — Prove CAP/BACKOFF against a real 429

| field | value |
|---|---|
| ticket | wg-t1-02-cap-backoff-real-429 |
| track / size / priority | T1 Engine / S / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

The engine's 429/usage-limit governor (CAP=3 clamp, pane-sniff signatures, `BACKOFF` flag-file,
cooldown auto-expiry, macOS notify) shipped 2026-07-06 but — per `engine/docs/ENGINE-NOTES.md`,
"Known limitations" — has only ever been tested against a synthetic pane string and a
manually-written flag. This war game runs a controlled saturation to hit a **genuine**
usage-limit wall, captures the real pane text as a durable fixture, proves
`looks_like_usage_limit()` matches it (patching the signature tuple if it doesn't — that gap is
exactly what we're hunting), proves the full BACKOFF lifecycle (flag write → `status.py` banner →
`wake.py` dispatch-gate → cooldown auto-clear) with real-wall data, and — when the execution
context permits — runs the live `orchestrator.py` reap path end-to-end at the wall. Done looks
like: fixture files committed, detector proven (or fixed and proven), ENGINE-NOTES limitation
struck with evidence, store left clean.

**Cost warning, by design:** saturation exhausts the current 5-hour subscription window and
blocks ALL interactive Claude use on this account until it resets — including David's own
sessions. That is why Move 1 is a hard human go-gate.

## Locked context

- decisions.md Q4: everything through the engine — this is a sonnet-Swagger engine ticket.
- Spec globals: **interactive `claude` only — no `-p`, no headless, no Agent SDK, no API key,
  ever** (metered billing). The saturation driver must use tmux-driven interactive REPLs only.
- HALT/BACKOFF flags are respected implicitly: if HALT appears mid-run, stop starting new work.
- No YLO/POEM work (parked) — not touched here.

## Recon (verify before any work)

1. `grep -n "USAGE_LIMIT_SIGNATURES\|def write_backoff\|def looks_like_usage_limit\|^CAP" engine/orchestrator.py`
   → expect all four present; as of authoring the tuple is
   `("usage limit", "rate limit", "429", "out of extended usage")` and `CAP = 3`.
   If missing/renamed → the governor moved since authoring; re-ground every Do line against the
   current code before proceeding, or park (A5) if the governor is gone entirely.
2. `grep -n "REAL 429" engine/docs/ENGINE-NOTES.md` → expect the "Not yet exercised against a
   REAL 429" limitation line still open. If it's already struck AND
   `ls engine/docs/fixtures/real-429-pane-*.txt` shows a fixture → this ticket is moot; park
   (A5) with the question "already proven on <date> — close as no-op?".
3. `ls engine/store/HALT engine/store/BACKOFF engine/store/WAKE-ARMED 2>&1` → expect all three
   absent (as of authoring). HALT present → stop immediately (A4). BACKOFF present → a real
   wall is ALREADY active; skip Moves 2–3, treat the current pane/flag as the specimen, and
   jump to Move 4 evidence capture.
4. `ls engine/store/queue/` → as of authoring exactly one ticket,
   `20260704T0630Z-project-digest-list-and-project-2.json`, carrying `"status": "deferred"` +
   `"priority": "deferred"` (verified — `dispatchable()` skips it). Record its checksum now:
   `md5 -q engine/store/queue/20260704T0630Z-project-digest-list-and-project-2.json` — it must
   be byte-identical at the end. Any OTHER dispatchable ticket present → note it; it disqualifies
   Route A of Fork F3 (a nested engine run would claim it first and could strand it in running/).
5. Execution context: `tmux display-message -p '#S' 2>/dev/null` (own session name, empty if not
   in tmux), `pgrep -f orchestrator.py`, `tmux ls 2>/dev/null | grep df-worker`. Feed the answers
   into Fork F3. Known trap (verified in code): `WarmWorker.boot()` **kills any existing tmux
   session named `df-worker-<n>` before booting** — a nested `orchestrator.py --pool 1` run
   would kill `df-worker-1`, i.e. you, if that's your own session.
6. `env | grep -c '^ANTHROPIC_API_KEY\|^ANTHROPIC_AUTH_TOKEN'` → expect 0 (`safety_check()`
   aborts otherwise; also the billing law).

## Moves

1. **Go-gate (human approval of the burn window).**
   - **Do:** read `engine/store/decisions/wg-t1-02-go.json`. Proceed only if it exists and
     parses with `{"action": "approve"}` (optional `"window_note"`).
   - **Expect:** file present, action approve.
   - **Failure signal:** file absent, unparseable, or action ≠ approve.
   - **Counter-move:** → Abort A1 (park with the timing question — never start saturation
     without this file).

2. **Build the saturation driver `engine/tools/saturate_429.py`.**
   - **Do:** create the file (new `engine/tools/` dir is fine). Requirements, all grounded in
     existing code: (a) `sys.path.insert` the `engine/` dir and import `WarmWorker`,
     `safety_check` from `warm_pool`, `is_halted` from `halt`, `looks_like_usage_limit` from
     `orchestrator`; (b) call `safety_check()` first; (c) boot exactly TWO workers via
     `WarmWorker(91, "sonnet", <repo root>)` and `WarmWorker(92, ...)` — indices 91/92 give tmux
     names `df-worker-91/92`, no collision with the engine pool's 1..3 and total live sessions
     stay ≤ CAP=3 alongside the executor's own; (d) wrap each `boot()` in
     `try/except TimeoutError`: on timeout, capture the pane, scan it, and if limit-ish text is
     present treat it as the wall (fixture + exit 0) else exit 3; (e) loop alternating workers,
     max 40 total turns or 50 min wall, checking `is_halted()` each turn (halt → exit 4):
     `send()` a heavy no-tool prompt ("Without using any tools, write an exhaustive ~2000-word
     technical essay comparing event-driven and polling architectures. Do not read or write any
     files."), poll `idle()` up to 180s, then capture scrollback with
     `tmux capture-pane -t df-worker-9N -p -S -400`; (f) after every turn overwrite
     `engine/store/results/wg-t1-02-last-pane.txt` with the capture (evidence survives even a
     no-wall exit); (g) if `looks_like_usage_limit(capture)` is True OR the capture matches the
     looser heuristic `re.search(r"(limit reached|usage limit|rate limit|resets at|try again later)", capture, re.I)`,
     write the full capture to `engine/docs/fixtures/real-429-pane-<YYYYMMDD>.txt` (mkdir -p the
     fixtures dir), print the matched line, **leave the tmux sessions alive** (Move 6 needs a
     probe), and exit 0; (h) caps exhausted → exit 2. Keep it ≤ ~120 lines, stdlib only.
     Then `python3 -m py_compile engine/tools/saturate_429.py`.
   - **Expect:** file exists; py_compile exits 0.
   - **Failure signal:** import errors at runtime (module path).
   - **Counter-move:** run from repo root and verify the `sys.path` insert points at `engine/`
     (where `warm_pool.py`/`orchestrator.py`/`halt.py` live — verified). If imports still fail
     after one fix attempt → A5.

3. **Run the saturation.**
   - **Do:** `python3 engine/tools/saturate_429.py 2>&1 | tee engine/store/results/wg-t1-02-saturation.log`
   - **Expect:** exit 0 and a non-empty `engine/docs/fixtures/real-429-pane-<YYYYMMDD>.txt`
     containing the genuine wall text; log names the worker + turn that hit it.
   - **Failure signal:** exit 2 (caps exhausted, no wall) · exit 3 (boot timeout, no limit text)
     · exit 4 (HALT appeared).
   - **Counter-move:** exit 2 → Fork F1. Exit 3 → inspect
     `engine/store/results/wg-t1-02-last-pane.txt` by eye; genuine-but-unmatched wall text →
     treat as fixture and go to Move 4 (F2 will catch the gap); truly no signal → F1. Exit 4 →
     Abort A4.

4. **Detector proof against the real pane text.**
   - **Do:**
     `python3 -c "import sys; sys.path.insert(0,'engine'); from orchestrator import looks_like_usage_limit as f; import glob; p=glob.glob('engine/docs/fixtures/real-429-pane-*.txt')[0]; print(f(open(p).read()))"`
     (run from repo root).
   - **Expect:** `True`.
   - **Failure signal:** `False` — the shipped signature tuple does not match reality. This is
     the single most valuable possible finding of this war game.
   - **Counter-move:** → Fork F2.

5. **BACKOFF lifecycle proof with real-wall data.**
   - **Do:** (a) drop a canary ticket `engine/store/queue/<UTC ts>-wg-t1-02-canary.json` —
     `{"ticket":"wg-t1-02-canary","kind":"instruction","title":"canary: trivial no-op for the 429 proof","executor":"swagger","priority":"normal","requested_at":"<now>","requested_by":"wg-t1-02","prompt":"Write the single word ok to your results file per the dispatch instructions. Change nothing else.","verify":"results file exists"}`;
     (b) write a real-reason flag:
     `python3 -c "import sys; sys.path.insert(0,'engine'); from orchestrator import write_backoff; print(write_backoff(\"usage-limit signature '<matched sig>' on df-worker-91 (wg-t1-02 live proof)\", 'df-worker-91', cooldown=90))"`;
     (c) `python3 engine/status.py` and `python3 engine/status.py --json`;
     (d) one watcher pass: `python3 engine/wake.py`, then `tail -3 engine/store/wake.log`;
     (e) sleep 100, then
     `python3 -c "import sys; sys.path.insert(0,'engine'); from orchestrator import is_backoff; print(is_backoff())"`
     and `ls engine/store/BACKOFF`.
   - **Expect:** (b) `engine/store/BACKOFF` exists with ts/until/reason/worker; (c) human output
     shows the `FACTORY IN BACKOFF (429 wall)` banner, `--json` has a non-null `backoff` key;
     (d) newest wake.log line shows the canary in the new-ticket set and
     `action=skip-dispatch (disarmed, BACKOFF present)`; (e) prints `False` with a
     `cooldown expired` line, and the flag file is gone (auto-clear proven).
   - **Failure signal:** banner missing, `backoff` null, wake.log says `quiet` or omits
     `BACKOFF present`, or the flag survives expiry.
   - **Counter-move:** wake.log `quiet` means the debounce state already saw the canary — accept
     the status.py evidence and record the wake check as inconclusive (do NOT delete
     `.wake-state.json`; it's the watcher's live state). Banner/JSON/expiry failures are real
     defects → record the exact output in the results notes and → A5 (a governor that lies
     about its own state needs David before anything trusts it).

6. **End-to-end orchestrator reap at the wall (→ Fork F3 decides the route).**
   - **Do (Route A only — all F3 conditions green):** first re-probe the wall:
     `tmux send-keys -t df-worker-91 -l "Reply with one word: ping"`, Enter, wait 30s,
     capture — limit text must still appear (the window may have reset). Then:
     `cd engine && python3 orchestrator.py --pool 1 --max-wall 420 --teardown 2>&1 | tee store/results/wg-t1-02-e2e.log`
   - **Expect:** log shows `[dispatch] ticket <canary>`; ~240s later (WORKER_TIMEOUT)
     `[backoff]  ticket ... -> BACKOFF written (cooldown 900s)` + `[reboot]`; a later pass shows
     `[backoff]  factory in backoff ... skipping claim/dispatch`; `[wall]` at 420s;
     `engine/store/BACKOFF` exists with `"worker": "df-worker-1"`; a macOS notification
     "engine: entering BACKOFF" fired (best-effort — note it, can't assert it); the canary is
     back in `queue/` (re-queued on retry), NOT stranded in `running/`.
   - **Failure signal:** worker completes the canary normally (wall reset mid-run — no backoff
     path exercised) · `TimeoutError` from `boot_all()` (REPL won't boot at the wall — the
     engine CRASHES instead of backing off) · canary left in `running/`.
   - **Counter-move:** wall-reset → record "window expired before E2E" and → A3 (park the leg,
     everything else stands). Boot crash → that is a REAL finding: capture the traceback into
     the e2e log, capture the boot pane, record in ENGINE-NOTES as "engine cannot boot a worker
     at the wall — governor never engages" — the leg is then complete (it proved a defect), carry
     on to Move 7. Stranded canary → `mv engine/store/running/<canary> engine/store/queue/` then
     delete it in Move 7.
   - **Do (Route B):** skip the live run entirely. The park happens in A3 AFTER Move 7 commits
     the evidence.

7. **Cleanup, document, commit.**
   - **Do:** (a) `tmux kill-session -t df-worker-91; tmux kill-session -t df-worker-92`;
     (b) delete the canary wherever it landed (`queue/`, `running/`, or `done/` + its results
     file) — it's scratch; (c) if `engine/store/BACKOFF` exists (Route A), preserve it first —
     `cp engine/store/BACKOFF engine/docs/fixtures/real-backoff-<YYYYMMDD>.json` — then clear:
     `python3 -c "import sys; sys.path.insert(0,'engine'); from orchestrator import clear_backoff; print(clear_backoff())"`;
     (d) confirm the deferred project-digest ticket's md5 matches Recon #4; (e) edit
     `engine/docs/ENGINE-NOTES.md`: strike the "Not yet exercised against a REAL 429" clause the
     same way the file's other closed items are struck (`~~...~~ **Closed <date>**`), citing the
     fixture path(s), which signature matched, any signature added via F2, and any boot-at-wall
     finding; (f) write the results self-report JSON to the exact path the dispatch prompt gave
     you; (g) `git add` the driver, fixtures, logs under store/results/, ENGINE-NOTES, and (if
     F2 fired) orchestrator.py; commit
     (`proof(engine): CAP/BACKOFF exercised against a real 429 — wg-t1-02`) and push.
   - **Expect:** `git status` clean for everything this ticket touched; both negative checks in
     Verification pass.
   - **Failure signal:** md5 mismatch on the deferred ticket, or leftover df-worker-9x sessions.
   - **Counter-move:** md5 mismatch → `git checkout -- engine/store/queue/20260704T0630Z-project-digest-list-and-project-2.json`
     and state in the results notes that it was restored. Leftover sessions → kill again by
     exact name from `tmux ls`.

## Forks

**F1 — saturation caps exhausted without hitting the wall** (driver exit 2).
Trigger: 40 turns / 50 min burned, no limit text in any capture.
→ **Route A** (the go-file's `window_note` said the window was near-spent AND less than ~60 min
elapsed since approval): run Move 3 exactly once more — the wall may be one burst away.
→ **Route B** (no such note, or the second run also exits 2): the window was too fresh —
park via A1's action with the question "saturation burned 40 turns without reaching the wall;
re-approve at a moment when /usage shows ≥70% consumed?" Do not run a third time.

**F2 — detector returns False on the real fixture** (signature gap — the hunted defect).
Trigger: Move 4 prints `False`.
→ **Route A** (the fixture contains an identifiable limit phrase a human can point at): add ONE
minimal lowercase substring of that phrase (prefer stable words, e.g. `"limit reached"`, never a
timestamp or reset-time fragment) to `USAGE_LIMIT_SIGNATURES` in `engine/orchestrator.py` — a
one-line tuple edit, nothing else in the file — re-run Move 4 until `True`, and record the
before/after in ENGINE-NOTES at Move 7.
→ **Route B** (the wall manifests with NO stable text at all — blank pane, spinner forever,
or purely visual state): → Abort A2. Pane-sniffing itself is the wrong strategy and that is
David's call, not yours.

**F3 — can the end-to-end orchestrator leg run safely here?**
Trigger: Move 6 reached; evaluate with Recon #4/#5 data.
→ **Route A** (ALL true: own tmux session is NOT `df-worker-1` — not in tmux at all also
qualifies; `pgrep -f orchestrator.py` is empty; no dispatchable ticket in `queue/` other than
the canary; wall re-probe still shows limit text): run Move 6 live.
→ **Route B** (anything false — the expected case when this ticket is engine-dispatched, since
the executor IS `df-worker-1` and a nested run's `boot()` would kill it): skip the live run,
complete Move 7, then → Abort A3 with the paste-ready command for an attended run.

## Assumptions ledger

1. **The wall renders as visible pane text.** Plausible — the shipped signatures were chosen
   from observed strings, and the TUI is a text UI. Candidate real-world phrasings (unverified,
   hints only): "usage limit reached", "5-hour limit reached ∙ resets <time>". If text exists
   but mismatches → F2 Route A. If no text at all → A2.
2. **The TUI still boots at the wall** (the limit surfaces per-message, not at startup). If
   false, Move 6 finds the boot-crash defect — file it per the counter-move; that outcome still
   completes the leg.
3. **A 5-hour usage-limit wall and a burst HTTP-429 present the same pane-sniff surface.** This
   run proves whichever arrives first (almost certainly the usage limit — CAP=3 exists precisely
   to prevent burst 429s). If David specifically wants a burst-429 proof, that requires >CAP
   concurrent sessions and is deliberately NOT this ticket → park a note, don't do it.
4. **Execution context:** engine-dispatched inside `df-worker-1` with the parent orchestrator
   live → F3 Route B is the expected path. If David runs this attended from a plain terminal,
   Route A opens up.
5. **Parent reap hazard:** this war game takes far longer than `WORKER_TIMEOUT=240s`; assumed
   the portfolio's promotion phase dispatches war-game tickets with an attended/lengthened
   timeout. If your own ticket file vanishes from `engine/store/running/` mid-work, you've been
   reaped-and-requeued → stop immediately and park (A4-style) rather than racing a second copy
   of yourself.
6. **Burn size:** David's go-approval implies the window is already near-spent, so the
   saturation cost is small. If the driver is clearly grinding through a fresh window (F1),
   stop rather than burn it down from zero.

## Abort conditions

- **A1 — no approved burn window.** `decisions/wg-t1-02-go.json` absent/declined (Move 1), or
  F1 Route B. Park: write `engine/store/needs-decision/<your ticket filename>.json` with
  `{"ticket":"<tid>","question":"Approve a saturation window for the real-429 proof? This exhausts the current 5-hour window and blocks ALL interactive Claude use until reset. When /usage shows >=70% consumed and you don't need Claude for ~1h, write engine/store/decisions/wg-t1-02-go.json {\"action\":\"approve\",\"window_note\":\"...\"}","proposed":"run saturation driver (2 workers, <=40 turns) at David's chosen moment","note":"go-gate per war game T1-02 Move 1"}`.
  Leave the ticket in `running/`. Never guess past this.
- **A2 — wall reached but no detectable pane text.** Park with the fixture/last-pane path in the
  note; the question: "pane-sniff cannot see this wall — redesign detection (exit-code sniff?
  transcript sniff?) or accept blind timeout+reboot?" Leave ticket in `running/`.
- **A3 — E2E leg unrunnable here** (F3 Route B, or wall reset first). ONLY after Move 7 has
  committed all other evidence: park with the question "run the attended E2E leg, or waive it?"
  and include the exact command block:
  `cd ~/dev/ad/apps/dark-factory/engine && python3 orchestrator.py --pool 1 --max-wall 420 --teardown 2>&1 | tee store/results/wg-t1-02-e2e.log`
  plus the precondition "account at the wall, no other engine running, canary ticket in queue/".
  Leave ticket in `running/`.
- **A4 — HALT appears, or your own ticket vanishes from running/.** Stop starting anything new
  immediately. Write a needs-decision noting exactly which move you stopped at and what state
  (tmux sessions, flags, canary) is live. Leave everything else untouched.
- **A5 — ground truth shifted or the governor misbehaves** (Recon #1/#2 mismatch, Move 5 defects,
  unfixable driver). Park with the specific observation quoted verbatim. Never "fix" status.py /
  wake.py / halt.py under this ticket.

## Verification

Executable acceptance (run from repo root; mirrors the ticket's `verify` field):

```bash
# 1. Real-wall fixture exists and is non-trivial
test -s engine/docs/fixtures/real-429-pane-$(date -u +%Y%m%d).txt || ls engine/docs/fixtures/real-429-pane-*.txt

# 2. The shipped detector matches the REAL pane text (post-F2 if it fired)
python3 -c "import sys; sys.path.insert(0,'engine'); from orchestrator import looks_like_usage_limit as f; import glob; p=sorted(glob.glob('engine/docs/fixtures/real-429-pane-*.txt'))[-1]; assert f(open(p).read()), 'detector MISSES real wall text'; print('detector OK on', p)"

# 3. Lifecycle evidence on disk
test -s engine/store/results/wg-t1-02-saturation.log
grep -q "FACTORY IN BACKOFF" engine/store/results/*.log 2>/dev/null || true   # banner captured in session log if teed
# Route A only: e2e log shows the live governor engaging
grep -q "BACKOFF written" engine/store/results/wg-t1-02-e2e.log 2>/dev/null || test -f engine/store/needs-decision/*wg-t1-02* 2>/dev/null

# 4. ENGINE-NOTES limitation closed with evidence
grep -q "real-429-pane" engine/docs/ENGINE-NOTES.md

# 5. Commit landed
git log --oneline -5 | grep -qi "wg-t1-02"
```

Negative checks (what must NOT have changed):

```bash
test ! -f engine/store/HALT && test ! -f engine/store/BACKOFF && test ! -f engine/store/WAKE-ARMED
tmux ls 2>/dev/null | grep -c "df-worker-9" | grep -q "^0$" || ! tmux ls 2>/dev/null | grep -q "df-worker-9"
ls engine/store/queue/ | grep -q "20260704T0630Z-project-digest"   # deferred ticket untouched, still queued
git diff HEAD~1 --stat -- engine/orchestrator.py | grep -q "1 file" && git diff HEAD~1 -- engine/orchestrator.py | grep -c "^[+-][^+-]" | grep -qE "^[24]$" || true
# (if F2 fired: the orchestrator.py diff is the ONE signature-tuple line; otherwise no diff at all)
```

## Executor notes (sonnet)

- **Scope fence:** the ONLY permitted edit to `engine/orchestrator.py` is the one-line
  `USAGE_LIMIT_SIGNATURES` addition under F2 Route A. Never touch `warm_pool.py`, `halt.py`,
  `wake.py`, `status.py`, the deferred queue ticket, or `.wake-state.json`. Never create
  `WAKE-ARMED`. Never set `ANTHROPIC_API_KEY` or use `claude -p` — the driver works exclusively
  through tmux-driven interactive REPLs, same as the engine.
- **Style:** the driver is a single-purpose proof tool, ≤ ~120 lines, stdlib only, comment-light.
  ENGINE-NOTES edits follow the file's existing strike-through closure idiom.
- **HITL over guessing:** anything ambiguous about spend, timing, or a governor defect → park.
  A parked ticket with a sharp question is a success; a guessed saturation run is not.
- **The rabbit hole:** trying to force a burst HTTP-429 by booting more than 3 concurrent
  workers "to be thorough". Don't — CAP=3 exists precisely to prevent that, exceeding it risks
  account-level throttling beyond the test window, and the usage-limit wall exercises the exact
  same detection/flag/notify path. Skip it.
