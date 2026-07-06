# T9-01 — Audio-out engine decision + build

| field | value |
|---|---|
| ticket | wg-t9-01-audio-out-engine |
| track / size / priority | T9 Voice / M / normal |
| executor | sonnet Swagger via engine |
| depends_on | wg-t1-04-c4-return-leg |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Close the "Audio-out engine — ElevenLabs? system TTS?" open decision (`docs/human-comms.md` §Open
decisions) and ship the ONE spoken-output pathway for factory events. **The decision is made in
this war game, not left to the executor**: kokoro-tts (David's own local/free/offline skill,
already named as the voice-out piece in the canonical `docs/comms-flow.md` triad) is the primary
voice, macOS `say` is the guaranteed zero-install fallback, and ElevenLabs is REJECTED for
ambient factory events (metered API cost for always-on chatter, network dependency, key lives in
another repo, and the `elevenlabs-agents` skill human-comms.md cites does not exist on this
machine — see Assumptions 1). Done means: `engine/speak.py` exists (stdlib-only, MUTE flag,
serialization lock, kokoro→say auto-fallback, `speak.log` ledger), both engine `notify()` seams
(`orchestrator.py`, `wake.py`) additionally speak their line fire-and-forget, a dummy done-ticket
drop produces a spoken line via the live launchd wire, and the decision is recorded in
`docs/audio-out.md` with measured latencies and re-open triggers.

## Locked context

- **Q7 (decisions.md):** voice/human-comms is IN — audio-out is portfolio work, not speculative.
- **Q4 (decisions.md):** everything through the engine — this ticket is written for sonnet
  Swagger dispatch.
- **No `-p`/headless/SDK ever; interactive `claude` only** — moot here (nothing spawns Claude),
  but `speak.py` must never invoke `claude`, and wake.py's "never calls claude itself" law stays
  intact after your edit.
- **HALT/BACKOFF respected implicitly** — speech is notify-layer only; it must NOT add any
  dispatch path. Speaking during HALT is correct (same ruling as T1-04: David still wants to know).
- **Voice law (`docs/comms-flow.md` §8):** voice surfaces are read-only. Audio-OUT is pure
  output; `speak.py` must never mutate factory state (queue/running/done/decisions) — its only
  writes are `speak.log` and its own lock file.
- **No YLO/POEM work** — out of scope entirely.
- **T9-02 (sound-effect vocabulary → consumer.py chimes) and T9-07 (one notify library) are
  SEPARATE tickets** — build neither here (see Executor notes).

## Recon (verify before any work)

Docs lag code in this repo. Run every check; each replaces doc-trust. All paths from
`/Users/davidcruwys/dev/ad/apps/dark-factory` unless absolute.

1. `grep -n "def notify" engine/orchestrator.py engine/wake.py` → expect exactly one hit in each
   (orchestrator.py ~line 162, wake.py ~line 59, both osascript + `sound name "Glass"`, both
   documented as duplicate-don't-import). If either is missing or the signature changed →
   **Abort A1**.
2. `grep -rni "speak\|tts\|kokoro" engine/*.py` and `ls engine/speak.py` → expect ZERO hits and
   no file (verified 2026-07-06: engine has no speech pathway; the only audio anywhere is
   consumer.py's `afplay Glass.aiff` chime, which greps as neither). Any hit or an existing
   `engine/speak.py` → someone landed audio-out in a race → **Abort A2**.
3. `grep -c "def done_pass" engine/wake.py` → expect `1` (the depends_on ticket
   wg-t1-04-c4-return-leg landed its done-watcher). If `0` → **Fork F2**.
4. `which say` → expect `/usr/bin/say` (verified at authoring). Then `say -o /tmp/say-check.aiff
   "dark factory audio check" && rm /tmp/say-check.aiff` → exit 0. If `say` is missing or
   errors AND Move 2's kokoro install also fails → **Abort A3**.
5. `ls /Users/davidcruwys/dev/ad/appydave-plugins/appydave/skills/kokoro-tts/scripts/` → expect
   `setup.sh`, `speak`, `speak_engine.py` (verified at authoring). Then
   `ls ~/.kokoro-tts/venv/bin/python` → EITHER missing (state at authoring on this M4 Mini —
   Move 2 installs it) OR present (someone installed it since — skip the install half of Move 2,
   keep the latency measurement). If the skill directory itself is gone → **Fork F1 Route B**
   (say-only) — do not go hunting for a relocated skill.
6. Flag-file idiom baseline: `ls engine/store/ | grep -c "^MUTE$"` → expect `0` (MUTE is new,
   this ticket creates its meaning; HALT/BACKOFF/WAKE-ARMED are the existing all-caps flag
   convention per wake.py header + kill-switch-spec). If MUTE already exists → treat as Abort A2
   evidence (someone is mid-build on this seam).
7. Import-safety of the wiring test: `grep -n "__main__" engine/orchestrator.py engine/wake.py`
   → expect guards (~line 698 and ~line 299 respectively), and eyeball that both modules'
   top-level is imports/constants/defs only (true at authoring) so
   `python3 -c "from wake import notify; ..."` is side-effect-free. If top-level now executes
   work on import → skip import-call tests, rely on Move 5's live test only, and note it.
8. `launchctl list | grep com.appydave.dark-factory-wake` → expect one line (loaded), and
   `grep -c "store/done" ~/Library/LaunchAgents/com.appydave.dark-factory-wake.plist` → ≥ 1
   (T1-04 widened WatchPaths to done/). If the job isn't loaded or done/ isn't watched, Move 5's
   launchd leg won't fire — fall back to hand-running `python3 engine/wake.py` for the live test
   and say so in the result notes; do NOT re-plumb launchd here (that's T1-04's seam).
9. Decision-record context (non-blocking, feeds Move 6):
   `grep -c "ELEVENLABS_API_KEY" /Users/davidcruwys/dev/ad/flivideo/fligen/server/.env` → ≥ 1
   (key exists, but in fligen — verified at authoring);
   `grep -ci eleven /Users/davidcruwys/dev/ad/apps/dark-factory/.env` → 0 (no key here — keep it
   that way); `find /Users/davidcruwys/dev/ad/appydave-plugins /Users/davidcruwys/.claude -maxdepth 6 -iname "*elevenlabs*" 2>/dev/null`
   → expect empty (the `elevenlabs-agents` skill is a phantom — Assumptions 1). Record whatever
   you actually find; if the skill DOES exist now, see Assumptions 1 (still don't wire it).
10. `git -C /Users/davidcruwys/dev/ad/apps/dark-factory status --porcelain` → expect clean or
    only unrelated files. If `engine/wake.py`, `engine/orchestrator.py`, or `engine/speak.py`
    is dirty → someone is mid-change on your exact seam → **Abort A5**.

## Moves

1. **Do:** Bake-off leg 1 — measure `say`. Run
   `time say -o /tmp/bakeoff-say.aiff "Three tickets done. First: canonical ingestion review dimensional."`
   then `afplay /tmp/bakeoff-say.aiff` and `rm /tmp/bakeoff-say.aiff`. Record the synth wall
   time (expect well under 1s) for the Move 6 decision table.
   **Expect:** exit 0 on all three; synth time recorded.
   **Failure signal:** `say` errors or hangs.
   **Counter-move:** retry once with the default voice explicitly (`say -v Samantha ...` — the
   macOS default US voice); if it still fails, `say` is broken on this machine — kokoro becomes
   the only engine; if Move 2 then also fails → **Abort A3**.

2. **Do:** Bake-off leg 2 — install + measure kokoro. If Recon 5 found the venv missing, run
   `bash /Users/davidcruwys/dev/ad/appydave-plugins/appydave/skills/kokoro-tts/scripts/setup.sh`
   (idempotent per its own header; installs brew espeak-ng + ffmpeg, uv-pinned Python 3.13 venv
   at `~/.kokoro-tts/`, ~330MB model — one-time, sanctioned by this ticket, see Assumptions 2).
   Then measure synth-only latency:
   `time /Users/davidcruwys/dev/ad/appydave-plugins/appydave/skills/kokoro-tts/scripts/speak "Three tickets done. First: canonical ingestion review dimensional." -o /tmp/bakeoff-kokoro.wav`
   then `afplay /tmp/bakeoff-kokoro.wav && rm /tmp/bakeoff-kokoro.wav`. Record the wall time.
   **Expect:** setup.sh completes without sudo prompts; the timed synth exits 0 in ≤ 10s wall
   time (cold model load included — each `scripts/speak` call is a fresh process).
   **Failure signal:** setup.sh errors, asks for sudo/anything beyond its documented brew+uv
   path, or the timed synth exceeds 10s or crashes.
   **Counter-move:** re-run setup.sh once (it self-skips completed steps). Second failure, or
   latency still > 10s → **Fork F1**. Never edit the kokoro skill itself to make it work
   (appydave-plugins is out of scope — note the failure in the result instead).

3. **Do:** Write `engine/speak.py` — stdlib only, mirroring wake.py's constants idiom
   (`ENGINE = os.path.dirname(os.path.abspath(__file__))`, `STORE = os.path.join(ENGINE, "store")`).
   Spec, exactly:
   - **Constants:** `MUTE_PATH = STORE/MUTE` · `LOCK_PATH = STORE/.speak.lock` ·
     `SPEAK_LOG_PATH = STORE/speak.log` ·
     `KOKORO_SHIM = "/Users/davidcruwys/dev/ad/appydave-plugins/appydave/skills/kokoro-tts/scripts/speak"` ·
     `KOKORO_VENV = os.path.expanduser("~/.kokoro-tts/venv/bin/python")` · `MAX_CHARS = 300`.
   - **CLI:** `python3 engine/speak.py "text..." [--engine say|kokoro|auto]` (default `auto`).
     Joins all positional args into one utterance; truncates to `MAX_CHARS`.
   - **MUTE:** if `MUTE_PATH` exists → append `[muted] <text>` to speak.log, exit 0, speak nothing.
   - **Engine selection (`auto`):** kokoro iff `KOKORO_VENV` and `KOKORO_SHIM` both exist, else
     `/usr/bin/say`. (If Fork F1 fired, `auto` correctly lands on say with zero code change —
     that IS the fallback design; do not special-case it.)
   - **Lock (serialize, never overlap audio):** create `LOCK_PATH` with
     `os.open(..., os.O_CREAT | os.O_EXCL)` writing the pid; if it exists, poll every 0.5s up to
     20s; a lock older than 90s (mtime) is stale — remove and take over; on timeout append
     `[dropped] <text>` to speak.log and exit 0. Always remove the lock in a `finally`.
   - **Speak:** kokoro → `subprocess.run([KOKORO_SHIM, text], timeout=60)`; say →
     `subprocess.run(["/usr/bin/say", text], timeout=30)`. If the kokoro call fails or times
     out, fall back to `say` in the same invocation and log `[fallback]` before the spoken line.
   - **Ledger:** every outcome appends one timestamped line to speak.log —
     `[spoken engine=say|kokoro]`, `[muted]`, `[dropped]`, `[fallback]`, `[error <summary>]` —
     mirroring wake.log's `log()` style.
   - **Exit 0 in every path** (a broken voice must never break a caller); errors go to the
     ledger, not stderr-with-nonzero.
   Then hand-test all four behaviours: (a) `python3 engine/speak.py "speak module check"` →
   audible + `[spoken engine=kokoro]` (or `say` if F1); (b) `touch engine/store/MUTE`, repeat →
   silent + `[muted]`, then `rm engine/store/MUTE`; (c) `python3 engine/speak.py "engine pinned check" --engine say`
   → `[spoken engine=say]`; (d) two concurrent calls
   (`python3 engine/speak.py "first long line about the factory finishing work" & python3 engine/speak.py "second line"; wait`)
   → both `[spoken]` lines in speak.log, no traceback, no leftover `.speak.lock`.
   **Expect:** all four tests pass; `ls engine/store/.speak.lock` → No such file afterwards.
   **Failure signal:** traceback, nonzero exit, leftover lock, or a `[muted]` test that speaks.
   **Counter-move:** fix and re-run the failing case (usual culprits: lock not released in
   `finally`, truncation applied after the log line so ledger and speech disagree). If (d)
   deadlocks twice, simplify: on lock contention just `[dropped]` immediately (no wait loop) —
   events are ambient, dropping the overlap is acceptable v1 behaviour; note it in Move 6.

4. **Do:** Wire the two notify() seams. In BOTH `engine/wake.py` `notify()` and
   `engine/orchestrator.py` `notify()`, after the existing osascript block and inside the same
   defensive posture, add (duplicated per the engine's stated duplicate-don't-import convention):
   ```python
   try:
       subprocess.Popen(
           [sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "speak.py"),
            f"{title}. {msg}"],
           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
           start_new_session=True)
   except Exception:
       pass
   ```
   (`start_new_session=True` detaches the child from the launchd job's process group so speech
   survives wake.py's quick exit.) Touch NOTHING else in either function. Then import-call test
   both (Recon 7 confirmed this is side-effect-free):
   `cd engine && python3 -c "from wake import notify; notify('dark-factory','wake audio wiring check')"` and
   `python3 -c "from orchestrator import notify; notify('dark-factory','orchestrator audio wiring check')"`.
   **Expect:** each prints nothing, exits 0, fires a macOS notification, AND within ~15s
   speak.log gains a `[spoken ...]` line containing the check text (audible if you could hear —
   the log line is your bar).
   **Failure signal:** ImportError/traceback, or no speak.log line within 30s.
   **Counter-move:** a traceback in the snippet usually means module top-level changed since
   Recon 7 — fall back to verifying via Move 5 only and note it. A missing speak.log line with a
   clean exit means the Popen path is wrong — check the speak.py path resolution from each
   file's location (both live in engine/, so `dirname(abspath(__file__))` is engine/ for both);
   fix and re-test. If the second attempt still produces no ledger line → **Abort A1** (the
   notify seam is not what recon believed).

5. **Do:** Live end-to-end via the launchd wire (T1-04's proven dummy procedure). Create
   `engine/store/done/20260706T9998Z-DUMMY-t9-audio-verify.json` containing
   `{"ticket":"20260706T9998Z-DUMMY-t9-audio-verify","kind":"instruction","title":"DUMMY t9 audio-out verify — ignore","result":{"status":"done","notes":"dummy"}}`.
   Wait 25s (launchd ThrottleInterval is 10s), then check `tail -5 engine/store/wake.log` and
   `tail -5 engine/store/speak.log`.
   **Expect:** wake.log gains a `[return] done: DUMMY t9 audio-out verify ...` line WITHOUT you
   running wake.py (launchd fired it — T1-04's leg), and speak.log gains a matching
   `[spoken ...]` line — the full chain done-file → wake → notify → speak just ran dark.
   Also `ps aux | grep '[p]ython3.*orchestrator.py'` → empty (no dispatch happened).
   **Failure signal:** no new wake.log `[return]` line within 60s, or a `[return]` line with no
   speak.log line.
   **Counter-move:** no `[return]` at all → run `python3 engine/wake.py` by hand; if the lines
   appear now, launchd is the gap — accept the hand-run as the live test (Recon 8 predicted
   this) and note it; do not re-plumb launchd. A `[return]` without `[spoken]` → your Move 4
   wake.py edit isn't on the code path launchd runs (stale pyc? wrong branch of notify?) —
   re-read your diff, fix, redo this move.
   **Cleanup (mandatory, same move):** `rm engine/store/done/20260706T9998Z-DUMMY-*.json`, run
   `python3 engine/wake.py` once to re-baseline, confirm `engine/store/.done-state.json` no
   longer lists the dummy and `ls engine/store/done/ | grep -ci dummy` → 0.

6. **Do:** Write the decision record `docs/audio-out.md` (new file, this is the ticket's paper
   trail). Sections, in order: **The decision** (kokoro primary / say fallback / ElevenLabs
   rejected — one paragraph, with the three-way rationale: local+free+offline+David's-own-skill
   vs zero-install vs metered+network+key-in-fligen+phantom-skill); **Measured** (the Move 1/2
   latency table, plus which engine `auto` resolves to on this machine today); **The pathway**
   (wire diagram: `notify() [orchestrator.py | wake.py] → Popen speak.py → MUTE gate → lock →
   kokoro|say → speak.log`, plus the four ledger line types); **Ops** (`touch engine/store/MUTE`
   to silence / `rm` to restore; speak.log is the audit trail; the dummy-done test procedure
   from Move 5; known risk: if David reports cut-off speech under launchd, flip wake.py's call
   site from Popen to `subprocess.run(..., timeout=90)`); **Re-open triggers** (revisit
   ElevenLabs only if: Samantha T9-04 needs conversational quality, or a real `elevenlabs-agents`
   skill lands with a costed always-on plan; revisit engine choice if kokoro latency degrades or
   the venv breaks — `auto` already degrades gracefully to say); **Out of scope, owned
   elsewhere** (chime vocabulary = T9-02 · notify-library consolidation = T9-07 · summary-on-
   return = T9-03 · fleet-wide audio = T10).
   **Expect:** one new doc, self-contained, every claim in it something you measured or did.
   **Failure signal:** the doc asserts anything you didn't verify (e.g. ElevenLabs pricing
   specifics — leave dollar figures out, the structural rationale suffices).
   **Counter-move:** cut the unverified claim; this record must not seed the next docs-lag-code
   problem.

7. **Do:** Annotate the two upstream docs, line-level only. (i) `docs/human-comms.md` — on the
   "Audio-out engine" bullet under `## Open decisions`, append
   ` — ✅ decided 2026-07-06: kokoro primary / say fallback, ElevenLabs rejected for ambient
   events; the elevenlabs-agents skill referenced here was not found on this machine. See
   docs/audio-out.md.` (ii) `docs/comms-flow.md` — in the §5 gaps table row `**Voice-out**`
   (~line 138), update the gap cell to `Wired: notify() → engine/speak.py (kokoro/say) — see
   docs/audio-out.md` and, in the §1 triad diagram, change `(kokoro-tts, unwired)` to
   `(kokoro-tts, wired)`. No other edits to either doc.
   **Expect:** two files, diffs of ≤ 4 lines total.
   **Failure signal:** the diff shows structural rewrites of either doc.
   **Counter-move:** `git checkout -- <doc>` and redo as pure line-level annotation.

8. **Do:** Commit and push dark-factory only. Stage: `engine/speak.py`, `engine/wake.py`,
   `engine/orchestrator.py`, `docs/audio-out.md`, `docs/human-comms.md`, `docs/comms-flow.md`.
   `engine/store/speak.log` follows whatever the store's tracking convention is — check
   `git check-ignore engine/store/speak.log`; if the store logs are tracked (wake.log is), stage
   it too. Message: `feat(engine): audio-out — speak.py (kokoro/say) wired into both notify() seams`.
   Do NOT commit anything in appydave-plugins (Recon/Move 2 must have left it untouched —
   `git -C /Users/davidcruwys/dev/ad/appydave-plugins status --porcelain` shows nothing under
   `appydave/skills/kokoro-tts/`).
   **Expect:** `git push` succeeds; `git status --porcelain` shows nothing of yours left.
   **Failure signal:** push rejected (remote ahead).
   **Counter-move:** `git pull --rebase` then push; on a real conflict in a file you touched,
   resolve keeping both sides' intent; on a conflict in a file you did NOT touch → **Abort A4**.

## Forks

**F1 — kokoro unavailable or too slow (say-only v1).**
Trigger: Move 2's setup.sh fails twice, demands anything beyond its documented brew+uv path
(e.g. sudo), the skill directory is gone (Recon 5), or measured synth latency of the test line
exceeds 10s.
→ **Route A** (first, only for a setup failure): re-run setup.sh once — it is idempotent and
self-skips completed steps; a transient brew/network hiccup is the common cause.
→ **Route B** (Route A exhausted, or latency/missing-skill trigger): ship say-only v1. No code
change needed — speak.py's `auto` already resolves to say when the venv is absent; if the venv
exists but is slow/broken, delete nothing — instead pin the default by changing `auto`'s kokoro
condition to `False` with a one-line comment naming this fork. Move 6's decision record then
states: v1 default = say, kokoro = documented upgrade path (install/repair the venv and `auto`
takes over), measured numbers included. ElevenLabs stays rejected either way.

**F2 — T1-04's done_pass never landed (Recon 3 = 0 despite depends_on).**
Trigger: `grep -c "def done_pass" engine/wake.py` → 0.
→ **Route A** (a done-watcher exists in a DIFFERENT shape — grep wake.py for `done\|return` and
check wake.log for `[return]` lines): adapt Move 5 to whatever the real leg is (same dummy-file
idea, expect its log idiom instead), and proceed — the notify() seam you wire is unchanged.
→ **Route B** (no done leg at all): the dependency was reordered or parked. Do NOT build the
done-watcher here (that is T1-04's ticket). Wire Move 4 as written, replace Move 5's live test
with the two import-call tests as the accepted bar (call-path-verified — precedent: the 0932
auto-wake ticket and T1-04 itself), and state in the result notes that the launchd-live spoken
return leg activates automatically the day T1-04 lands, because it rides the same notify().

## Assumptions ledger

1. **The `elevenlabs-agents` skill is a phantom.** `docs/human-comms.md` (2026-06-01) says it
   exists; authoring-time recon (2026-07-06) searched `appydave-plugins` skills,
   `~/.claude/skills`, and the plugin caches/repos — no such skill anywhere on this machine, and
   the newer canonical `docs/comms-flow.md` (2026-07-03) names kokoro-tts as the voice-out piece
   without mentioning ElevenLabs at all. If the executor's Recon 9 DOES find it (added since):
   still do not wire it — the rejection rationale (metered cost for always-on ambient events,
   network dependency, key lives in fligen) stands regardless; record its location in
   docs/audio-out.md's re-open triggers instead. Not a park.
2. **One-time kokoro install is within ticket scope.** ~330MB model + venv to `~/.kokoro-tts/`,
   brew espeak-ng + ffmpeg, uv — no sudo (verified against setup.sh's source at authoring).
   Plausible because Q7 locked voice IN and David triaged this ticket into the portfolio; the
   skill is David's own. If setup.sh's behaviour has changed and it wants more than that →
   Fork F1 Route B, never force an install.
3. **Spoken audio on this M4 Mini's default output device reaches David.** He works at this
   desk; the engine, launchd wire, and store all live here. Fleet-wide audio (Roamy, other
   minis) is T10 territory. If David flags at triage that events must speak on a different
   machine → that is a new ticket, not a rework of this one.
4. **Call-path-verified is the accepted bar for "it spoke".** The executor cannot hear;
   exit 0 + a `[spoken]` speak.log line + the macOS notification is the proof standard
   (precedent: T1-04 Move 4 and the 0932 auto-wake ticket's accepted verify). David's ear at
   triage is the true test; if he reports silence-with-clean-logs, the documented known-risk fix
   (blocking `subprocess.run` in wake.py's call site) is the first thing to try.
5. **The 10s latency threshold is an authoring call, not a measurement.** Kokoro cold-load on
   this machine was unmeasured at authoring (venv not installed). 0–10s: kokoro is the default
   (ambient events tolerate a short lag); > 10s: F1 Route B. If David later wants a different
   threshold, the decision record is where it changes.
6. **No concurrent editor on the notify() seams.** T9-02 targets consumer.py (chimes), T1-04
   has landed (depends_on), T9-07 (notify consolidation) is bucket-later. Recon 10 catches a
   live race → Abort A5 rather than merge-by-guess.

## Abort conditions

- **A1 — the notify seam is not what recon believed.** `def notify` missing/renamed in either
  engine file, or Move 4's wiring produces no ledger line after the counter-move retry. Park:
  write `engine/store/needs-decision/wg-t9-01-audio-out-engine.json` with
  `{"ticket":"wg-t9-01-audio-out-engine","question":"engine notify() seam has changed since authoring (2026-07-06: orchestrator.py ~162, wake.py ~59, osascript+Glass, duplicate-don't-import). Audio-out wiring needs a re-recon against the new shape. Proceed how?","observed":"<what you found>"}`.
  Leave the ticket in `running/`. Never guess a new seam.
- **A2 — a speech pathway already exists** (Recon 2 hits, engine/speak.py present, or a MUTE
  flag already in the store). Park with question: "engine already contains an audio/speech
  pathway (found: <lines/files>). Verify-and-close this ticket against the existing
  implementation, or rebuild per the war game?" Do not duplicate or rewrite what's there.
- **A3 — no working engine at all.** `say` fails (Move 1 counter-move exhausted) AND kokoro
  fails (Move 2 counter-move exhausted). Park with both failure outputs and the question:
  "M4 Mini has no working TTS (say: <error>, kokoro: <error>). Fix the machine's audio stack
  first, or re-scope audio-out to another surface?"
- **A4 — rebase conflict in a file this ticket never touched.** Park with the conflicting
  paths; do not resolve other people's conflicts.
- **A5 — concurrent edits on the exact seam** (Recon 10: wake.py / orchestrator.py / speak.py
  dirty before you start). Park with the `git status` output and the question "who owns the
  notify() seam right now?".

## Verification

All from `/Users/davidcruwys/dev/ad/apps/dark-factory` unless pathed:

```bash
# 1. speak.py exists, speaks, and ledgers — all four behaviours
ls engine/speak.py
python3 engine/speak.py "verification pass" --engine say && echo say-ok        # exit 0
python3 engine/speak.py "auto verification pass" && echo auto-ok               # exit 0, engine per machine state
touch engine/store/MUTE && python3 engine/speak.py "must not speak"; rm engine/store/MUTE
tail -5 engine/store/speak.log | grep -c "\[muted\]"                           # → ≥ 1
grep -c "\[spoken engine=" engine/store/speak.log                              # → ≥ 3
ls engine/store/.speak.lock 2>&1 | grep -c "No such"                           # → 1 (no leftover lock)

# 2. Both notify() seams wired and callable
grep -c "speak.py" engine/wake.py                                              # → ≥ 1
grep -c "speak.py" engine/orchestrator.py                                      # → ≥ 1
cd engine && python3 -c "from wake import notify; notify('dark-factory','verify wake leg')" && cd ..
cd engine && python3 -c "from orchestrator import notify; notify('dark-factory','verify orch leg')" && cd ..
sleep 15 && tail -5 engine/store/speak.log | grep -c "verify"                  # → ≥ 1 (≥ 2 if not lock-dropped)

# 3. Decision record + doc annotations
grep -c "kokoro" docs/audio-out.md                                             # → ≥ 1 (file exists, decision named)
grep -ci "re-open" docs/audio-out.md                                           # → ≥ 1
grep -c "audio-out.md" docs/human-comms.md docs/comms-flow.md | grep -vc ":0"  # → 2 (both annotated)

# 4. Negative checks — what must NOT have changed
git diff HEAD~1 --name-only | grep -c "consumer.py"                            # → 0 (T9-02's seam untouched)
grep -ci eleven .env 2>/dev/null; echo "(expect 0 or no file)"                 # no key imported here
grep -c "claude" engine/speak.py                                               # → 0 (never calls claude)
git -C /Users/davidcruwys/dev/ad/appydave-plugins status --porcelain | grep -c kokoro   # → 0 (skill untouched)
ls engine/store/done/ | grep -ci dummy                                         # → 0
ls engine/store/MUTE 2>&1 | grep -c "No such"                                  # → 1 (not left muted)
ls engine/store/WAKE-ARMED 2>&1 | grep -c "No such"                            # → 1 unless armed BEFORE this ticket

# 5. Committed and pushed
git log --oneline -1                                                           # shows the audio-out commit
git status --porcelain | wc -l                                                 # nothing of yours left
```

## Executor notes (sonnet)

- **Scope fence.** Do NOT touch `engine/consumer.py` (its Glass chime is T9-02's seam — the
  chime vocabulary ticket), `engine/halt.py`, `engine/warm_pool.py`, `engine/status.py`, the
  launchd plists (T1-04 owns that wire), anything under `experiments/`, any real file in
  `engine/store/done|queue|running/` (dummies only, removed same-move), or ANYTHING in
  `/Users/davidcruwys/dev/ad/appydave-plugins/` — you consume the kokoro skill, you never edit it.
- **The rabbit hole: building the notify library.** Wiring the same 6-line Popen block into two
  files will itch — "extract a shared notify module" is T9-07, a separate later ticket, and the
  engine's duplicate-don't-import convention is documented in wake.py's own notify() docstring.
  Duplicate the block, move on. Equally out of scope: chime vocabularies (T9-02), spoken
  digests/summaries (T9-03), Samantha (T9-04), quiet-hours scheduling (note it as a re-open
  trigger in docs/audio-out.md if you feel strongly; do not build it).
- **The decision is already made** — kokoro primary, say fallback, ElevenLabs rejected. Your job
  is to measure, build, wire, and record it, not to re-litigate it. The only decision-shaped
  latitude you have is Fork F1's latency trigger, and its threshold is fixed at 10s.
- **Style:** speak.py is stdlib-only, small functions, wake.py's constants idiom, one timestamped
  ledger line per outcome (mirror wake.log's format). Exit 0 in every path — a voice failure
  must never propagate into notify() or the orchestrator.
- **Do not call the ElevenLabs API** at any point — not even "just to compare quality". It is
  metered, the key lives in another repo's .env, and the comparison is structural, not auditory.
- **Prefer parking over guessing** on any schema/seam drift (A1/A2/A5). A parked question costs
  minutes; a guessed merge into the factory's live notification path costs David his one
  ambient-awareness channel.
