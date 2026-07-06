# T1-04 — C4 return leg — "what ran" surfaced to David

| field | value |
|---|---|
| ticket | wg-t1-04-c4-return-leg |
| track / size / priority | T1 Engine / M / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Close C4 of the build spine (`docs/north-star.md`: *"Return leg (#19): every run surfaces a
one-line 'what ran' so nothing is silent"*). Today tickets land in `engine/store/done/` silently:
`orchestrator.py` notifies on HITL and BACKOFF but **not** on completion, and builder-agent
tickets are moved to done/ by hand with no signal at all. Done means two things ship: **(a)** a
done-watcher return leg in `engine/wake.py` — when a ticket lands in `engine/store/done/`, David
gets a macOS notification with a one-line "what ran" summary plus a durable `[return]` line in
`engine/store/wake.log`, fired by the existing launchd WatchPaths job widened to also watch
`store/done/`; **(b)** the morning briefing's SHIPPED field — project-digest's
`lib/shipped.py` gains engine done-tickets as a third source, so `python3 digest.py dark-factory`
reports what the factory shipped, not just git commits and backlog/done files.

## Locked context

- **Q4 (decisions.md):** everything through the engine — this ticket is written for sonnet
  Swagger dispatch; the artifact itself must never call `claude` (wake.py's standing law).
- **No `-p`/headless/SDK ever; interactive `claude` only** — moot for this build (nothing here
  spawns Claude), but preserve wake.py's "never calls claude itself" property verbatim.
- **HALT/BACKOFF respected implicitly** — the return leg is notify-only; it must NOT add any
  dispatch path. Notifying during HALT is correct (David still wants to know what finished).
- **Store is a growing ledger** (orchestrator.py header): never modify or delete real files in
  `done/`. The only exception is the clearly-marked DUMMY test file you create and remove.
- **No YLO/POEM work** — out of scope entirely for this ticket.

## Recon (verify before any work)

Docs lag code in this repo. Run every check; each replaces doc-trust.

1. `ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/done/*.json | wc -l` → expect
   ≥ 17 (count as of 2026-07-06). If the directory is missing or empty → the store layout moved
   → **Abort A1**.
2. `grep -n "done\|return\|\.done-state" engine/wake.py` → expect NO done-scanning leg: as of
   2026-07-06 wake.py (300 lines) scans only `queue/` (`Q = store/queue`), state file
   `.wake-state.json`, functions `run_pass/pending_tickets/notify/log/dispatchable`. If a
   done/return leg already exists → someone landed C4 in a race → **Abort A2**.
3. `launchctl list | grep com.appydave.dark-factory-wake` → expect one line (loaded; leading `-`
   is normal for a WatchPaths job with no live pid). If not loaded, note it — Move 3's
   `install.sh` re-load fixes it; do not treat as a blocker.
4. `grep -A4 WatchPaths ~/Library/LaunchAgents/com.appydave.dark-factory-wake.plist` → expect
   only `.../engine/store/queue` (one `<string>` entry). The repo template is
   `engine/launchd/com.appydave.dark-factory-wake.plist` with `__APP_ROOT__` placeholders;
   `engine/launchd/install.sh` does the sed + unload + load.
5. Confirm the done-outcome duality before writing the summariser:
   `python3 engine/status.py` runs clean, and read `engine/status.py` `done_outcome()`
   (~line 106): outcome lives EITHER in `store/results/<fname>.json` (`status`/`notes`) OR
   embedded in the done ticket itself as `result` (string OR dict with `status`/`notes`) —
   both shapes exist in the real store. Your wake.py summariser must handle all of these.
6. `ls /Users/davidcruwys/dev/ad/apps/project-digest/lib/shipped.py` exists;
   `grep -n "engine" /Users/davidcruwys/dev/ad/apps/project-digest/lib/shipped.py` → expect no
   hits (sources today: git commits via `git_source.shipped_recently` + `backlog_done_in_window`).
   If an engine source already exists → leg (b) landed elsewhere; skip Moves 5–6, verify only.
7. Baseline the digest BEFORE touching it:
   `python3 /Users/davidcruwys/dev/ad/apps/project-digest/digest.py dark-factory --format json --no-write`
   → expect valid JSON with a `shipped_recently` object (`git_count`, `backlog_done_count`,
   `top`). If this baseline run crashes → **Abort A3**.
8. `grep -rn "shipped_recently" /Users/davidcruwys/dev/ad/apps/project-digest/lib/` → expect
   consumers `box.py` (`_fmt_shipped`), `view.py` (~line 61, computes
   `git_count + backlog_done_count`), `render_md.py` (~line 44), `assemble.py` (producer).
   These are the render surfaces Move 5 must extend. Keep all existing keys — additive only.
9. `git -C /Users/davidcruwys/dev/ad/apps/project-digest status --porcelain` → expect clean or
   only `view/dark-factory.html` modified (a generated file, refreshed on every digest run —
   normal churn). Anything else dirty → **Fork F2**.

## Moves

1. **Do:** Add the return leg to `engine/wake.py`, mirroring its existing idioms exactly
   (stdlib only; duplicate-don't-import per the engine's stated convention). Add:
   `DONE_DIR = os.path.join(STORE, "done")`, `DONE_STATE_PATH = os.path.join(STORE, ".done-state.json")`,
   and a `done_pass()` function that: lists `done/*.json`, diffs against the `last_seen` set in
   `.done-state.json`, and for each NEW file builds a one-liner
   `"<title> — <status>"` where title = ticket `title` (fallback: filename) and status comes from
   `store/results/<fname>` `status` if present, else the ticket's embedded `result` (unwrap
   dict → `result["status"]`, accept plain string, else `"unknown"`) — the `done_outcome()`
   duality from `engine/status.py`. **First-run rule:** if `.done-state.json` does not exist,
   record the full current set, append one `[return] baseline: N existing done ticket(s) recorded, no notify`
   line, and do NOT notify (prevents a ~17-notification blast). Otherwise: one `notify()` call
   per pass — `notify("dark-factory", f"{n} ticket(s) done: {first_one_liner[:80]}")` — plus one
   `[return] done: <one-liner> [<fname>]` wake.log line per new ticket. Save state. Call
   `done_pass()` from `main()`'s no-arg path immediately after `run_pass()`. No dispatch logic
   anywhere in the leg.
   **Expect:** `python3 engine/wake.py` (by hand) exits 0; wake.log gains the `[return] baseline:`
   line; `engine/store/.done-state.json` exists and its `last_seen` matches the real done/ set;
   no notification fired on this baseline run.
   **Failure signal:** traceback, or a notification fires on first run, or `.done-state.json`
   missing afterwards.
   **Counter-move:** fix the code (typical culprits: dict-shaped `result`, unparseable done JSON —
   wrap every per-file read in try/except and fall back to filename + "unknown"; never let one bad
   file kill the pass). If a second hand-run still crashes on a specific store file, log-and-skip
   that file; if more than half the done files are unreadable → the store schema has shifted
   under you → **Abort A1**.

2. **Do:** Run `python3 engine/wake.py` a second time, by hand, with nothing changed.
   **Expect:** wake.log gains the queue leg's normal `quiet:` line AND no new `[return]` lines,
   no notification — the done leg debounces exactly like the queue leg.
   **Failure signal:** repeat notification or duplicate `[return]` lines for already-seen files.
   **Counter-move:** the state save/load is broken (compare with `save_state`/`load_state` for
   the queue leg); fix and re-run Move 1's baseline check from scratch (delete
   `.done-state.json` first, expect the baseline line again).

3. **Do:** Widen the launchd trigger: in the repo template
   `engine/launchd/com.appydave.dark-factory-wake.plist`, add a second WatchPaths entry
   `<string>__APP_ROOT__/engine/store/done</string>` after the queue entry, then run
   `bash engine/launchd/install.sh` (it seds `__APP_ROOT__`, unloads, loads). Do this ONLY after
   Moves 1–2 pass (the baseline must exist before launchd can fire the leg).
   **Expect:** install.sh prints its "Loaded com.appydave.dark-factory-wake" line;
   `grep done ~/Library/LaunchAgents/com.appydave.dark-factory-wake.plist` shows the real
   absolute done path; `launchctl list | grep dark-factory-wake` shows it loaded.
   **Failure signal:** launchctl load error, or the installed plist lacks the done path.
   **Counter-move:** re-run install.sh once (unload/load races are transient). If the job loads
   but Move 4 shows done/-changes never fire it → **Fork F1**.

4. **Do:** Live-verify the return leg end-to-end. Create
   `engine/store/done/20260706T9999Z-DUMMY-c4-return-verify.json` containing
   `{"ticket":"20260706T9999Z-DUMMY-c4-return-verify","kind":"instruction","title":"DUMMY c4 return-leg verify — ignore","result":{"status":"done","notes":"dummy"}}`.
   Wait 20s (ThrottleInterval is 10s), then check `tail -5 engine/store/wake.log`.
   **Expect:** a `[return] done: DUMMY c4 return-leg verify — ignore — done [...]` line appears
   WITHOUT you invoking wake.py (launchd fired it), and the notify() call path ran (osascript;
   call-path-verified is the accepted bar — precedent: the 0932 auto-wake ticket's verify).
   Also confirm NO orchestrator was launched: `ps aux | grep '[p]ython3.*orchestrator.py'` empty
   (use exactly this bracketed pattern — a loose pgrep has false-matched sibling shells before).
   **Failure signal:** no `[return]` line within 60s of the file landing.
   **Counter-move:** run `python3 engine/wake.py` by hand — if the line appears now, the code is
   fine and launchd is the problem → **Fork F1**. If it doesn't appear even by hand, the diff
   logic missed the file → back to Move 1's counter-move.
   **Cleanup (mandatory, same move):** `rm engine/store/done/20260706T9999Z-DUMMY-*.json`, run
   `python3 engine/wake.py` once to re-baseline, and confirm `.done-state.json` no longer lists
   the dummy. The ledger must hold zero dummy files at the end.

5. **Do:** Leg (b) — extend project-digest. In
   `/Users/davidcruwys/dev/ad/apps/project-digest/`: (i) add
   `"engine_done_dir": "engine/store/done"` to `projects/dark-factory.json`; (ii) in
   `lib/shipped.py` add `engine_done_in_window(cfg, since_ts, top_n=3)` modelled line-for-line
   on the existing `backlog_done_in_window` (missing config key or missing dir → zeros, no
   error; glob `*.json`; window by file mtime against `since_ts`; title = the ticket JSON's
   `title` field via a try/except json load, fallback filename stem); (iii) in `collect()`,
   call it and add `"engine_done_count"` to the returned dict, merging its titles into `top`
   after git titles (keep `top_n` cap); (iv) fold the new count into the three renderers found
   in Recon 8: `view.py`'s `total_shipped` sum, `box.py`'s `_fmt_shipped`, and `render_md.py`'s
   SHIPPED line — additive presentation, e.g. `· N engine tickets`. Do NOT rename or remove any
   existing key (Recon 8's consumers depend on them).
   **Expect:** files edited; no other lib file touched.
   **Failure signal:** you find yourself editing `assemble.py`'s windowing or `store.py` —
   that's out of scope; the since_ts window arrives in `collect()` already computed.
   **Counter-move:** revert the overreach; the entire leg lives in shipped.py + config + the
   three render lines.

6. **Do:** Verify leg (b):
   `python3 /Users/davidcruwys/dev/ad/apps/project-digest/digest.py dark-factory --format json --no-write | python3 -c "import json,sys; s=json.load(sys.stdin)['shipped_recently']; assert 'engine_done_count' in s, s; print('engine_done_count =', s['engine_done_count'])"`
   then run once more with `--format md --no-write` and eyeball the SHIPPED line.
   **Expect:** assertion passes; `engine_done_count` ≥ 1 (the last-briefing ts was
   2026-07-03T03:17Z as of authoring and 14+ done tickets landed 07-04→07-06 — if David has run
   a briefing since, the window may legitimately be smaller; ≥ 0 with the key present is the
   hard bar, ≥ 1 the expected one). The md SHIPPED line mentions engine tickets. `--format box`
   also renders without crashing.
   **Failure signal:** KeyError/traceback in any of the three formats.
   **Counter-move:** the usual culprit is a renderer assuming the old two-term sum; fix the
   renderer, not the data shape. If mtime windowing yields 0 while done/ clearly has recent
   files, print the mtimes (`ls -lT` on macOS) and check the `since_ts` actually in play
   (`store/last-briefing/dark-factory.json`) before touching code — 0 may be correct.

7. **Do:** Documentation, tightly fenced: (i) append a short `## Return leg (C4)` section to
   `docs/auto-wake.md` — the wire (done/ WatchPaths → wake.py `done_pass()` → notify +
   `[return]` log), the first-run silent-baseline rule, the dummy-file test procedure, and the
   note that the digest SHIPPED field is the second surface; (ii) in `docs/north-star.md`, on
   the C4 line of the build spine (line ~81), append a one-line status annotation only —
   `✅ DONE 2026-07-06 (wake.py return leg + digest SHIPPED — see docs/auto-wake.md)` — matching
   the C1 line's existing style. No other north-star edits.
   **Expect:** two files changed, diffs of a few lines each.
   **Failure signal:** the north-star spine reads structurally different from before (you
   rewrote rather than annotated).
   **Counter-move:** `git checkout -- docs/north-star.md` and redo as a pure suffix on the C4
   bullet.

8. **Do:** Commit and push BOTH repos (they are separate git repos — verified at authoring).
   dark-factory: `engine/wake.py`, `engine/launchd/com.appydave.dark-factory-wake.plist`,
   `docs/auto-wake.md`, `docs/north-star.md`, plus this war game's own state files are NOT
   committed if gitignored — check `git status` and stage only your intended files. Message:
   `feat(engine): C4 return leg — done-ticket notify + digest SHIPPED source`.
   project-digest: `lib/shipped.py`, `projects/dark-factory.json`, the three renderer files
   (`view/dark-factory.html` regenerates on every run — committing it is fine if already
   tracked-dirty, per Recon 9). Message:
   `feat(shipped): engine done-tickets as third SHIPPED source (dark-factory C4)`.
   **Expect:** both `git push` succeed; `git status --porcelain` shows nothing of yours left.
   **Failure signal:** push rejected (remote ahead).
   **Counter-move:** `git pull --rebase` then push; on a real conflict in a file you touched,
   resolve keeping both sides' intent; on a conflict in a file you did NOT touch → **Abort A4**.

## Forks

**F1 — launchd won't fire on done/ (single job, two WatchPaths).**
Trigger: Move 4's dummy file produces no `[return]` line via launchd within 60s, but a by-hand
`python3 engine/wake.py` run summarises it correctly (code proven, trigger broken).
→ **Route A** (first): re-check the installed plist has BOTH absolute paths (sed ran on the
edited template — a stale `~/Library/LaunchAgents` copy from before Move 3 is the common miss);
`launchctl unload` + `load` once more; retry the dummy.
→ **Route B** (if A fails once): ship a second launchd job — copy the plist to
`engine/launchd/com.appydave.dark-factory-return.plist` with label
`com.appydave.dark-factory-return`, WatchPaths = done/ only, same ProgramArguments; extend
install.sh/uninstall.sh to handle both labels; revert the original plist to queue-only. Verify
Move 4 again. Note the split in `docs/auto-wake.md`.

**F2 — project-digest tree dirty beyond the generated view file.**
Trigger: Recon 9 shows modifications other than `view/dark-factory.html`.
→ **Route A** (dirt is in files you won't touch): proceed; stage ONLY your files at Move 8;
leave the stranger's changes uncommitted and mention them in the ticket result notes.
→ **Route B** (dirt is in `lib/shipped.py`, `lib/assemble.py`, `projects/dark-factory.json`, or
a renderer you must edit): someone is mid-change on your exact seam → **Abort A5**.

## Assumptions ledger

1. **A macOS `osascript` notification counts as "reaches David" for C4 v1.** Plausible: it is
   the established engine idiom (orchestrator.py `notify()`, wake.py, the 0932 ticket's accepted
   verify), and richer channels (audio-out, Samantha) are Q7/T9 portfolio work, not this ticket.
   If David rejects this bar at triage → park to `needs-decision/` asking which channel
   (T9 audio-out / webhook / other) before building more.
2. **launchd accepts two WatchPaths entries on one job and fires the same throttled program.**
   Standard documented launchd behaviour; not yet exercised in this repo. If false in practice
   → Fork F1 Route B (second job) — already planned, no decision needed.
3. **File mtime is an acceptable proxy for "landed in done/" for the digest window.**
   Plausible: orchestrator's `commit()` is an `os.rename` (mtime preserved = last result write),
   and builder-agent tickets get their embedded `result` written at completion. Known imprecision;
   if a windowing dispute surfaces, the upgrade path is `results/*.json` timestamps or
   `audit.jsonl` — note it in the result, do not build it now.
4. **`shipped_recently` has no consumers outside project-digest's own three renderers.**
   Recon 8 greps the lib; authoring-time recon found none elsewhere. Keys stay additive anyway;
   if an external consumer surfaces post-landing, additive keys can't have broken it.
5. **No other war-game ticket edits wake.py concurrently.** T1-siblings (auto-wake arming,
   CAP/429 proving) exercise but don't rewrite wake.py. Recon 2 catches the race; if it fires
   → Abort A2 rather than merge-by-guess.

## Abort conditions

- **A1 — store layout shifted.** `engine/store/done/` missing, or >50% of done files unreadable
  by the Move-1 summariser. Park: write `engine/store/needs-decision/wg-t1-04-c4-return-leg.json`
  with `{"ticket":"wg-t1-04-c4-return-leg","question":"store/done layout or ticket schema has changed since authoring (2026-07-06, 17 tickets, results-or-embedded-result duality). Return leg needs a re-recon against the new shape. Proceed how?","observed":"<what you found>"}`.
  Leave the ticket in `running/`. Never guess a new schema.
- **A2 — return leg already exists in wake.py.** Someone landed C4 in a race. Park with
  question: "wake.py already contains a done-watcher (found: <lines>). Verify-and-close this
  ticket against the existing implementation, or rebuild per the war game?" Do not duplicate or
  rewrite the existing leg.
- **A3 — digest baseline broken.** Recon 7's untouched `digest.py` run crashes. Park with the
  traceback and question: "project-digest baseline is broken before any C4 edit; leg (b) is
  blocked. Fix digest first (separate ticket) or land leg (a) alone?" Record in the park file
  which moves (1–4) already landed.
- **A4 — rebase conflict in a file this ticket never touched.** Park with the conflicting
  paths; do not resolve other people's conflicts.
- **A5 — concurrent edits on the exact digest seam** (Fork F2 Route B). Park with
  `git status` output and the question "who owns lib/shipped.py right now?".

## Verification

All from `/Users/davidcruwys/dev/ad/apps/dark-factory` unless pathed:

```bash
# 1. Return leg exists and is debounced
grep -c "def done_pass" engine/wake.py                      # → 1
grep -c "\[return\]" engine/store/wake.log                  # → ≥ 2 (baseline + dummy test)
python3 engine/wake.py && python3 engine/wake.py            # exit 0 twice, no crash
python3 - <<'EOF'                                           # state matches the real done/ set
import json, os
state = set(json.load(open("engine/store/.done-state.json"))["last_seen"])
real  = set(f for f in os.listdir("engine/store/done") if f.endswith(".json"))
assert state == real, (state ^ real)
print("done-state in sync:", len(real))
EOF

# 2. launchd trigger widened and live
grep -c "store/done" ~/Library/LaunchAgents/com.appydave.dark-factory-wake.plist   # → ≥1 (or the F1-B second plist)
launchctl list | grep -c "com.appydave.dark-factory"        # → ≥ 1

# 3. Digest SHIPPED includes engine tickets, all three formats render
cd /Users/davidcruwys/dev/ad/apps/project-digest
python3 digest.py dark-factory --format json --no-write | \
  python3 -c "import json,sys; s=json.load(sys.stdin)['shipped_recently']; assert 'engine_done_count' in s; print('engine_done_count', s['engine_done_count'])"
python3 digest.py dark-factory --format md  --no-write | grep -i "SHIPPED"
python3 digest.py dark-factory --format box --no-write > /dev/null && echo box-ok

# 4. Negative checks — what must NOT have changed
ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/done/ | grep -ci dummy   # → 0
grep -c "subprocess.*claude\|\"claude\"" /Users/davidcruwys/dev/ad/apps/dark-factory/engine/wake.py  # → 0 (wake.py still never calls claude)
ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/WAKE-ARMED 2>&1 | grep -c "No such"      # → 1 unless it was armed BEFORE this ticket
tail -20 /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/wake.log | grep -c "quiet\|wake:"  # queue leg still alive

# 5. Both repos committed and pushed
git -C /Users/davidcruwys/dev/ad/apps/dark-factory   log --oneline -1   # shows the C4 commit
git -C /Users/davidcruwys/dev/ad/apps/project-digest log --oneline -1   # shows the shipped commit
```

## Executor notes (sonnet)

- **Scope fence.** Do NOT touch `engine/orchestrator.py` (its `commit()` already emits
  `job.completed` events — leave that path alone; the done/-watcher covers orchestrator AND
  builder-agent landings, which is exactly why the leg lives on the directory, not in the
  orchestrator). Do NOT touch `engine/consumer.py`, `engine/halt.py`, `engine/warm_pool.py`,
  anything under `experiments/`, or any real file in `engine/store/done/`.
- **The rabbit hole: folding this into `consumer.py`.** consumer.py already reads events and
  chimes — it looks like the natural home. Skip it: consumer.py is a run-forever polling loop
  nobody keeps running, it only sees `job.completed` events (orchestrator path — builder-agent
  tickets emit none), and C4 needs the event-driven launchd wire. The seam is the done/
  directory via wake.py. Do not unify the two; note the overlap in docs/auto-wake.md if you
  must, in one sentence.
- **Style:** wake.py is stdlib-only, small functions, duplicate-don't-import (its own header
  explains why); keep `done_pass()` symmetrical with `run_pass()`'s state/log/notify idioms.
  project-digest changes mirror `backlog_done_in_window` — same defensive zeros, same shape.
- **Notifications:** one per pass, not one per ticket (a 5-ticket batch = 1 notification naming
  the first + count); per-ticket detail goes to wake.log lines. Nobody wants 17 popups.
- **Prefer parking over guessing** on anything that smells like schema drift in the store, and
  on any concurrent-edit signal (A2/A5). A parked question costs minutes; a guessed merge of
  someone's half-landed watcher costs a debugging day.
