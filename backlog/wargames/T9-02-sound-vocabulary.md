# T9-02 — Sound-effect vocabulary (done / failed / needs-you chimes)

| field | value |
|---|---|
| ticket | wg-t9-02-sound-vocabulary |
| track / size / priority | T9 Voice / S / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Today `engine/consumer.py` plays ONE sound — Glass.aiff, once per batch, for ANY event — so
David hears "something happened" but not WHAT. Give the factory a three-note vocabulary:
**done** (Glass), **failed** (Basso), **needs-you** (Sosumi), plus **other** (Pop) for
non-factory events like omi-fetch captures. Two halves: (a) consumer.py classifies each
consumed event by its `event` kind and plays at most one cue per class per pass, priority
order needs-you → failed → done → other, plus a `--sounds` demo flag; (b) orchestrator.py
actually EMITS the missing event kinds — it only emits `job.completed` today (verified line
638), so `job.failed` (4 terminal-failure points) and `job.needs_decision` (HITL lock point)
must be added or the failed/needs-you chimes can never fire. Done looks like: both files
edited and compiling, a synthetic end-to-end pass produces the right chime lines from
`consumer.py --once`, engine/README.md documents the vocabulary, everything committed and
pushed to main. No launchd, no TTS, no speech — chimes only.

## Locked context

- **Q7 (decisions.md):** voice/human-comms is IN (audio-out + Samantha front door) — this
  ticket is the cheapest first brick of that track.
- **Q4:** everything through the engine — this ticket ships as a sonnet-Swagger edit job;
  no new runtime services, no daemons.
- **Ticket-first** (`engine/store/queue/.CONVENTION.md`): this work item IS a ticket; its
  movement queue/ → running/ → done/ is the audit trail.
- **No `-p`/headless/SDK ever** (wargame-spec): nothing here invokes `claude` at all.
- **Docs lag code** (wargame-spec): `docs/comms-flow.md` line 139 claims attention alerts
  have "zero implementation" — false since consumer.py shipped its Glass chime. Do NOT fix
  comms-flow.md here; that status line is T8 truth-reconciliation's seam.

## Recon (verify before any work)

All paths relative to `/Users/davidcruwys/dev/ad/apps/dark-factory`. Run every check.

1. `grep -n "def chime" engine/consumer.py` → expect one hit (~line 58), a zero-argument
   `chime()` that plays only Glass.aiff unconditionally; and `grep -c "Basso\|Sosumi\|classify" engine/consumer.py`
   → expect 0. Non-zero → a vocabulary already landed → **Fork F1**.
2. Anchors in `engine/orchestrator.py` (verified 2026-07-06 at lines 502/612/625/629/643/669):
   `grep -n "def emit_event\|notify(f\"engine: ticket\|\"declined\"; settle\|failed(no-decision)\|failed(verify)\"; a\|failed(timeout)\"" engine/orchestrator.py`
   → expect 6 hits, one per anchor. Fewer hits, or `grep -c "job.failed\|job.needs_decision" engine/orchestrator.py`
   already > 0 → the reap block was restructured or the emissions landed → **Fork F1** (if
   landed) / **Abort A2** (if restructured beyond the anchors).
3. Seam is free: `git -C . status --porcelain -- engine/consumer.py engine/orchestrator.py engine/README.md`
   → expect empty; and `ls engine/store/running/ | grep -i "t9\|sound\|consumer"` → expect no
   hits. Dirty file or a running/ sibling on this seam → **Abort A1**.
4. Nothing live is executing the code you're about to edit:
   `pgrep -f orchestrator.py; pgrep -f consumer.py; tmux ls 2>&1 | grep df-worker` → expect
   all empty (verified empty 2026-07-06). Any hit → **Fork F2**.
5. The four sounds exist:
   `ls /System/Library/Sounds/Glass.aiff /System/Library/Sounds/Basso.aiff /System/Library/Sounds/Sosumi.aiff /System/Library/Sounds/Pop.aiff`
   → expect all four (verified 2026-07-06). One missing → substitute any other file from
   `ls /System/Library/Sounds/` (14 exist), keep the class names unchanged, note the swap in
   your result.
6. `command -v afplay` → expect a path (macOS built-in). Missing → you are not on a Mac →
   **Abort A2** (this ticket is macOS-audio-specific by design).
7. Baseline the store: `ls engine/store/events/*.json | wc -l` and
   `wc -l < engine/store/events-consumed.jsonl` → note both numbers (at authoring: 1 event
   file, ledger present). You'll restore events/ to this file-count after the synthetic test.

## Moves

1. **Do:** Rewrite the sound half of `engine/consumer.py`. Replace the existing
   `def chime():` block (the whole function, ~lines 58–64) with:

   ```python
   SOUNDS = [
       # (class, path) in playback priority order — most attention-worthy first
       ("needs-you", "/System/Library/Sounds/Sosumi.aiff"),
       ("failed",    "/System/Library/Sounds/Basso.aiff"),
       ("done",      "/System/Library/Sounds/Glass.aiff"),
       ("other",     "/System/Library/Sounds/Pop.aiff"),
   ]


   def classify(event):
       """Map an event dict -> sound class. Kind-based, deliberately dumb."""
       kind = str(event.get("event", ""))
       if kind == "job.needs_decision":
           return "needs-you"
       if kind == "job.failed":
           return "failed"
       if kind == "job.completed":
           return "done" if event.get("result", "done") == "done" else "failed"
       return "other"


   def play(path):
       """Best-effort macOS sound cue; silently no-ops elsewhere."""
       try:
           subprocess.run(["afplay", path], capture_output=True, timeout=5)
       except Exception:
           pass


   def chime(classes):
       """Play at most one cue per class present, in priority order."""
       for cls, path in SOUNDS:
           if cls in classes:
               print(f"[chime] {cls} -> {os.path.basename(path)}", flush=True)
               play(path)
   ```

   Then wire `poll_once` to it — inside the consume loop add `cls = classify(event)` after
   the `event = ...` try/except, change the print to
   `print(f"[consumed] {source}: {os.path.basename(f)} ({cls})", flush=True)`, collect
   `classes.add(cls)` into a `classes = set()` initialised at the top of `poll_once`, and
   change the tail to `if consumed_this_pass: chime(classes)`. Add a demo flag as the FIRST
   thing in `main()`:

   ```python
   if "--sounds" in sys.argv:
       print("[consumer] sound vocabulary demo:", flush=True)
       chime({cls for cls, _ in SOUNDS})
       return
   ```

   Finally update the module docstring's Glass.aiff paragraph (lines ~12–15) to describe the
   vocabulary (one cue per class per batch: needs-you=Sosumi, failed=Basso, done=Glass,
   other=Pop) and add `python3 consumer.py --sounds` to the docstring's Usage block. Touch
   nothing else — `load_seen`, sources, the loop, `--once`/`--interval` behaviour all stay.
   **Expect:** `python3 -m py_compile engine/consumer.py` exits 0; `grep -c "def classify" engine/consumer.py` → 1.
   **Failure signal:** compile error, or `chime()` still zero-argument anywhere
   (`grep -n "chime()" engine/consumer.py` → any hit is a missed call-site).
   **Counter-move:** fix the missed call-site (there is exactly one caller, in `poll_once`).
   Second compile failure → `git checkout -- engine/consumer.py` and redo the move from the
   verbatim block. Third failure → **Abort A2**.

2. **Do:** Add the missing emissions to `engine/orchestrator.py`. Five single-line inserts,
   each anchored to a line verified 2026-07-06 (`emit_event` itself already exists, line 502
   — do not touch it). Match surrounding indentation exactly:

   a. HITL lock (~line 612) — insert ABOVE the line
      `notify(f"engine: ticket {tid} needs you", req.get("question", "A worker is waiting."))`:
      `emit_event("job.needs_decision", dict(ticket=tid, question=req.get("question", "awaiting decision")))`

   b. Decline (~line 625) — the block reads
      `if act == "decline":` / `results[tid] = "declined"; settle(tid, a)`. Insert below the
      results line, inside the if-block:
      `emit_event("job.failed", dict(ticket=tid, result="declined"))`

   c. HITL timeout (~line 629) — insert directly below
      `results[tid] = "failed(no-decision)"` at the same indent:
      `emit_event("job.failed", dict(ticket=tid, result="failed(no-decision)"))`

   d. Verify-fail (~line 643) — insert directly below
      `results[tid] = "failed(verify)"; a["verify_findings"] = findings; settle(tid, a)`:
      `emit_event("job.failed", dict(ticket=tid, result="failed(verify)", findings=findings))`

   e. Timeout, retries exhausted (~line 669) — insert directly below
      `results[tid] = "failed(timeout)"`:
      `emit_event("job.failed", dict(ticket=tid, result="failed(timeout)"))`

   Deliberately NOT emitted: the retry re-queue path (`re-queue (retry n)`) — it is not
   terminal; and HITL resume — resuming is silence, only the lock chirps.
   **Expect:** `python3 -m py_compile engine/orchestrator.py` exits 0;
   `grep -c 'emit_event("job.failed"' engine/orchestrator.py` → 4;
   `grep -c 'emit_event("job.needs_decision"' engine/orchestrator.py` → 1.
   **Failure signal:** counts off, compile error, or an anchor line not found verbatim.
   **Counter-move:** `git checkout -- engine/orchestrator.py`, re-find each anchor by the
   grep in Recon 2, redo. If an anchor genuinely no longer exists → **Abort A2** — never
   invent a new emission point.

3. **Do:** Static checks of the classifier, no audio needed. From `engine/`:
   ```bash
   cd engine && python3 - <<'EOF'
   from consumer import classify
   assert classify({"event": "job.completed", "result": "done"}) == "done"
   assert classify({"event": "job.completed", "result": "failed(verify)"}) == "failed"
   assert classify({"event": "job.failed", "result": "failed(timeout)"}) == "failed"
   assert classify({"event": "job.needs_decision", "question": "?"}) == "needs-you"
   assert classify({"event": "new-capture"}) == "other"
   assert classify({"parse_error": "boom"}) == "other"
   print("classify OK")
   EOF
   ```
   **Expect:** `classify OK`, exit 0.
   **Failure signal:** AssertionError or ImportError.
   **Counter-move:** the classifier must match the verbatim block in Move 1 — diff yours
   against it and fix. Second failure → **Abort A2**.

4. **Do:** Synthetic end-to-end — prove an emitted event reaches a classified chime. First
   `cd engine && python3 consumer.py --once` to drain any real pending events (baseline).
   Then write two synthetic event files (shapes mirror orchestrator's `emit_event` output):
   ```bash
   TS=$(date -u +%Y%m%dT%H%M%SZ)
   cat > engine/store/events/${TS}-job.failed-wgt9test1.json <<'EOF'
   {"event": "job.failed", "ts": "TEST", "ticket": "WG-T9-02-TEST", "result": "failed(verify)"}
   EOF
   cat > engine/store/events/${TS}-job.needs_decision-wgt9test2.json <<'EOF'
   {"event": "job.needs_decision", "ts": "TEST", "ticket": "WG-T9-02-TEST", "question": "synthetic"}
   EOF
   cd engine && python3 consumer.py --once
   ```
   Then clean up: delete both `*wgt9test*.json` files from `engine/store/events/` and prune
   their two ledger lines:
   `grep -v "wgt9test" engine/store/events-consumed.jsonl > /tmp/ec.$$ && mv /tmp/ec.$$ engine/store/events-consumed.jsonl`.
   Also run `python3 consumer.py --sounds` once — David's ear-training demo must print all
   four `[chime]` lines in priority order.
   **Expect:** the `--once` run prints two `[consumed] engine: ... (failed)` / `(needs-you)`
   lines and exactly two `[chime]` lines — `needs-you -> Sosumi.aiff` FIRST, then
   `failed -> Basso.aiff` (priority order); audible on the Mac's speaker. After cleanup,
   `ls engine/store/events/*.json | wc -l` equals Recon 7's baseline and
   `grep -c wgt9test engine/store/events-consumed.jsonl` → 0.
   **Failure signal:** wrong class in a `[consumed]` line, chimes out of order, more than one
   `[chime]` line per class, or leftover wgt9test artifacts.
   **Counter-move:** re-check `poll_once`'s classes-set wiring against Move 1 and rerun (the
   ledger prune makes reruns re-consume the synthetic files — re-create them if deleted).
   Second failure → **Abort A2**. (No audio audible but lines correct is NOT a failure —
   afplay is best-effort by design; note speaker/mute state in the result.)
5. **Do:** Document the vocabulary in `engine/README.md`. Replace the two-line consumer.py
   entry (lines ~23–24: `consumer.py        the events consumer ... logs + chimes`) with:
   ```
   consumer.py        the events consumer (the missing brick, comms-flow.md §5) — polls
                       engine/store/events/ + omi-fetch/store/events/, logs + chimes a
                       sound VOCABULARY (one cue per class per batch, priority order):
                       needs-you=Sosumi · failed=Basso · done=Glass · other=Pop
   ```
   and in the "## Run it" block add one line under the two existing consumer.py lines:
   `python3 consumer.py --sounds    # play the 4-cue vocabulary once (ear training)`.
   Touch nothing else in the README.
   **Expect:** `grep -c "Sosumi" engine/README.md` → ≥1; `git diff --stat -- engine/README.md`
   shows only this file's small hunk.
   **Failure signal:** diff bleeds into other README sections.
   **Counter-move:** `git checkout -- engine/README.md`, redo as the two surgical edits.

6. **Do:** Commit and push to main (repo standing practice; stage ONLY the three files):
   `git add engine/consumer.py engine/orchestrator.py engine/README.md` then commit with
   message `feat(engine): sound vocabulary — done/failed/needs-you chimes in consumer + job.failed/needs_decision emissions (wg-t9-02)`
   then `git push`.
   **Expect:** push succeeds; `git status --porcelain` no longer lists the three files;
   `git show --stat HEAD` lists exactly those three.
   **Failure signal:** push rejected (remote ahead), or a fourth file staged.
   **Counter-move:** `git pull --rebase` then push. Rebase conflict in one of YOUR three
   files → a concurrent writer on the seam → **Abort A1**. A fourth file staged → reset it
   out (`git restore --staged <path>`) and recommit.

## Forks

**F1 — the vocabulary (or the emissions) already landed.**
Trigger: Recon 1 finds `classify`/Basso in consumer.py, or Recon 2 finds `job.failed` /
`job.needs_decision` emissions already in orchestrator.py.
→ **Route A** (the landed scheme matches this war game's semantics: kind-based classes done /
failed / needs-you / other, one cue per class per batch, all five orchestrator emission points
present): switch to verify-and-close — run Moves 3–4's checks against what's on disk, patch
only genuinely missing pieces (e.g. consumer landed but orchestrator emissions didn't — do
Move 2 only), commit per Move 6, record that the rest pre-existed.
→ **Route B** (a DIFFERENT scheme landed — different classes, per-event chime storms, config
files, TTS calls): do not layer this design on top of someone's fresh intent → **Abort A1**
with a summary of found-vs-specified.

**F2 — the engine is live at execution time.**
Trigger: Recon 4 finds a running orchestrator.py / df-worker tmux session / consumer.py loop.
→ **Route A** (pool run in progress, no HITL block — likely a sibling T1 ticket draining):
wait, re-checking every 5 minutes up to 30 minutes; when Recon 4 comes back empty, proceed
from Move 1. Editing the .py files mid-run would not crash the running process (Python loads
code at start) but committing behaviour claims against a moving engine muddies both tickets'
audit trails.
→ **Route B** (still live after 30 minutes, or a gated `--hitl` run is blocked awaiting
David — could hold for hours): → **Abort A1**, naming the live tmux sessions/PIDs in the
question. Special case: if ONLY a `consumer.py` loop is running (no orchestrator), kill it
(`pkill -f consumer.py`), proceed, and note in the result that whoever ran it must restart
it to pick up the vocabulary — the durable ledger guarantees no replayed chimes on restart.

## Assumptions ledger

1. **The specific sound mapping (Sosumi/Basso/Glass/Pop) is Fable's authoring-time pick, not
   David-ratified.** Plausible: Q7 locked voice IN but named no sounds; Glass-for-done
   preserves the existing cue's meaning; Basso is macOS's conventional error sound. **If
   false** (David dislikes a cue at triage): it's a one-line change in the `SOUNDS` list —
   note it, don't park.
2. **"Declined" chimes as failed.** Plausible: it is a non-success terminal outcome and the
   events store doubles as an audit surface; a decline David just typed produces one soft
   Basso he expects. **If false:** reclassify in `classify()` later; note in result, don't
   park.
3. **Reclassifying omi-fetch `new-capture` events from Glass to Pop is an acceptable
   behaviour change.** Plausible: the whole point is distinguishing "factory verdict" from
   "something arrived"; omi-fetch events are the only current `other` producer. **If false:**
   swap `other` back to Glass.aiff — one dict line.
4. **No persistent consumer.py service exists.** Verified 2026-07-06: no consumer launchd
   job in `engine/launchd/` or `~/Library/LaunchAgents/` (only dark-factory-wake), no live
   process. **If false at execution:** Fork F2's special case — restart it after the edit.
5. **Live-fire proof of the orchestrator emissions belongs to the next real engine run, not
   this ticket.** Plausible: booting a warm pool costs real subscription usage for an S-sized
   audio ticket, and sibling war game T1-01 will exercise the HITL path live (its run will
   emit the first real `job.needs_decision`). Move 4's synthetic events prove the
   emit-shape → classify → chime chain end-to-end. **If false** (David wants live-fire
   here): that's a triage note on this ticket, not an executor improvisation.

## Abort conditions

- **A1 — seam conflict / concurrent writer / conflicting design.** Recon 3 dirt, a running/
  sibling on this seam, Fork F1 Route B (a different landed scheme), Fork F2 Route B (engine
  live and staying live), or Move 6 rebase conflict in your files. Park: write
  `engine/store/needs-decision/wg-t9-02-sound-vocabulary.json` with
  `{"ticket": "wg-t9-02-sound-vocabulary", "question": "Sound-vocabulary blocked: <what you found — dirty seam / live run / conflicting landed scheme>. Who owns this seam right now, and does the war game's mapping (needs-you=Sosumi, failed=Basso, done=Glass, other=Pop) still stand?", "observed": "<git status / pgrep / tmux / diff evidence>"}`.
  Leave the ticket in `running/`. Never edit around a live engine or someone else's design.
- **A2 — code shape diverged beyond the anchors.** Recon 2's anchors missing without the
  emissions having landed, Recon 6's afplay missing (non-macOS host), or a Move's
  counter-move failing twice. Park with the same file shape: question "wg-t9-02: engine code
  no longer matches the war game's verified anchors (<which>) — re-author against the new
  shape?", observed = the failing grep/compile output. Leave the ticket in `running/`.
  Never guess where an emission belongs in a reap loop you don't recognise.

## Verification

```bash
DF=/Users/davidcruwys/dev/ad/apps/dark-factory

# 1. Both files compile
python3 -m py_compile $DF/engine/consumer.py $DF/engine/orchestrator.py && echo COMPILE-OK

# 2. The vocabulary exists and is complete
grep -c "def classify" $DF/engine/consumer.py                          # → 1
grep -c "Sosumi.aiff\|Basso.aiff\|Glass.aiff\|Pop.aiff" $DF/engine/consumer.py | \
  awk '{print ($1>=4) ? "SOUNDS-OK" : "SOUNDS-MISSING"}'               # → SOUNDS-OK

# 3. Classifier behaves (pure functions, no audio required)
cd $DF/engine && python3 -c "
from consumer import classify
assert classify({'event':'job.completed','result':'done'})=='done'
assert classify({'event':'job.completed','result':'failed(x)'})=='failed'
assert classify({'event':'job.failed'})=='failed'
assert classify({'event':'job.needs_decision'})=='needs-you'
assert classify({'event':'new-capture'})=='other'
print('CLASSIFY-OK')"

# 4. Orchestrator emits the full vocabulary
grep -c 'emit_event("job.failed"' $DF/engine/orchestrator.py           # → 4
grep -c 'emit_event("job.needs_decision"' $DF/engine/orchestrator.py   # → 1
grep -c 'emit_event("job.completed"' $DF/engine/orchestrator.py        # → 1 (pre-existing, untouched)

# 5. Demo flag works and prints priority order
cd $DF/engine && python3 consumer.py --sounds | grep "\[chime\]" | head -1 | grep -c "needs-you"  # → 1
cd $DF/engine && python3 consumer.py --sounds | grep -c "\[chime\]"    # → 4

# 6. Negative checks — what must NOT have changed
grep -c "def load_seen" $DF/engine/consumer.py                         # → 1 (durable ledger intact)
grep -c "re-queue (retry" $DF/engine/orchestrator.py                   # → 1 (retry path exists, and…)
awk '/re-queue \(retry/{found=1} found&&/emit_event\("job.failed"/{print "BAD"; exit}' \
  $DF/engine/orchestrator.py | grep -c BAD || true                     # → 0 (…no emission on retry)
grep -c wgt9test $DF/engine/store/events-consumed.jsonl || true        # → 0 (synthetic test cleaned)
ls $DF/engine/store/events/ | grep -c wgt9test || true                 # → 0
git -C $DF diff HEAD~1 HEAD --stat -- engine/wake.py engine/warm_pool.py engine/status.py docs/comms-flow.md | wc -l  # → 0

# 7. Committed and pushed
git -C $DF log --oneline -1 | grep -c "wg-t9-02"                       # → 1
git -C $DF status --porcelain -- engine/consumer.py engine/orchestrator.py engine/README.md | wc -l  # → 0
```

## Executor notes (sonnet)

- **Scope fence.** THREE files: `engine/consumer.py`, `engine/orchestrator.py` (five one-line
  inserts, nothing else — not `emit_event` itself, not `notify()`, not the retry path),
  `engine/README.md` (two surgical edits). Do NOT touch `engine/wake.py`, `warm_pool.py`,
  `status.py`, `halt.py`, anything under `engine/launchd/`, `docs/comms-flow.md`, or the
  omi-fetch repo. Do NOT boot the warm pool or run `orchestrator.py` to test — synthetic
  event files are the test rig (Move 4).
- **This is chimes, not speech.** The audio-out engine decision (ElevenLabs vs system TTS)
  is T9-01's seam; Samantha is another ticket entirely. If you feel the urge to add `say`,
  a config file for sound choices, per-ticket custom sounds, or a volume flag — that's the
  rabbit hole. Four hardcoded .aiff paths in one list is the whole design; skip anything
  fancier.
- **Chime-per-class, not per-event.** A 10-ticket batch completing must produce ONE Glass,
  not ten — the storm-avoidance semantic is the point of the `classes` set. Don't "improve"
  it into per-event playback.
- **Audio is best-effort.** `play()` swallows everything, like today's `chime()`. Correct
  `[chime]` stdout lines are the acceptance signal; actual audibility depends on the Mac's
  mute state and is noted, never asserted.
- **Prefer parking over guessing:** if the orchestrator's reap loop doesn't match the five
  anchors, or another scheme already landed, that's David's call (A1/A2) — a wrong emission
  point in the engine kernel is worse than a parked ticket.
