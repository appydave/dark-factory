# T10-01 — Roamy as Swagger worker

| field | value |
|---|---|
| ticket | wg-t10-01-roamy-swagger-worker |
| track / size / priority | T10 Fleet / M / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Prove the cross-machine delegation seam per Q8: one real Family-A ticket **claimed on the Mini**
(rename CAS, queue/ → running/, ownership stamped), **executed on Roamy** (an interactive
`claude` inside a detached tmux session, reached over Tailscale SSH — never `.local`), and the
**artifact verified back** on the Mini (scp'd into `engine/store/results/`, content-checked,
ticket moved to done/, audit line appended). The whole mechanic was **live-proven at authoring
(2026-07-06)**: boot-to-ready ≈ 5 s, one send-keys turn answered in ≈ 5 s, clean teardown — this
war game re-runs that proof against a real payload ticket and leaves committed evidence. Done
looks like: `engine/store/results/wg-t10-01p-roamy-echo.json` on the Mini containing
`"hostname": "Roamy"` (execution provably happened on the other machine), the payload ticket in
done/ with `claimed_by` stamped, an audit.jsonl entry naming the remote worker and its Roamy-side
session transcript, nothing left running on Roamy, and Roamy's working tree clean. Productizing
this seam (pool semantics, CAP, machine-tag routing) is **T10-06's job, not yours**.

**Seed correction (verified live):** the candidate brief says "100.82.235.39" — that IP is
**mac-mini-m4 itself** (this machine). Roamy is `roamy` / **100.89.32.35** on the tailnet. The
delegation target is Roamy; treat the seed's IP as a typo. The "never .local" instruction stands:
use the MagicDNS name `roamy` (or the pinned fallback alias, Fork F4), never `Roamy.local`.

## Locked context

- decisions.md Q8: fleet scope is **+ Roamy** — Tailscale worker delegation is explicitly in scope.
- decisions.md Q4: everything through the engine — this war game is itself a sonnet-Swagger
  engine ticket, and its payload follows the engine's ticket idiom (queue/ → running/ → done/,
  artifact-is-truth, audit.jsonl).
- Spec globals: **no `-p`/headless/SDK ever** (metered billing) — the remote worker is an
  **interactive** `claude` in tmux, same invariant as `engine/warm_pool.py`. HALT/BACKOFF
  respected. No YLO/POEM work.
- `engine/store/queue/.CONVENTION.md`: every unit of work gets a ticket JSON that moves
  queue/ → running/ → done/ — the payload ticket obeys this even though the executor (not
  orchestrator.py) does the moving.

## Recon (verify before any work)

All paths absolute. Authoring-time state noted; docs lag code — trust only what you see.

1. **Engine flags:** `ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/HALT /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/BACKOFF 2>&1`
   → expect both absent ("No such file"). Either present → stop immediately, park per the
   engine's standing HALT/BACKOFF rule (do not begin).
2. **No local engine racing you:** `pgrep -f orchestrator.py; tmux ls 2>&1` → expect no
   orchestrator PID and no `df-worker-*` sessions (authoring: "no server running"). An
   orchestrator IS running → **Fork F2 pre-empt**: skip queue/ in Move 2 and write the payload
   ticket directly into running/ (claim-by-construction), noting it in your report.
3. **Roamy alive on the tailnet:**
   `/Applications/Tailscale.app/Contents/MacOS/Tailscale status | grep -i roamy`
   → expect `100.89.32.35   roamy   david@   macOS` with a `-` or `active…` tail (authoring:
   `active; direct 192.168.1.142:41641`). `offline, last seen …` → **Abort A2**. No `roamy` row
   at all → the machine was renamed again: take the current MagicDNS name of the macOS row that
   is not a mini from the same output and substitute it for `roamy` in every Do line
   (Assumption 2); no such row → **Abort A2**.
4. **SSH proof (MagicDNS, never .local):**
   `ssh -o ConnectTimeout=8 -o BatchMode=yes -o StrictHostKeyChecking=no davidcruwys@roamy 'echo ok; hostname'`
   → expect `ok` then `Roamy`. `Permission denied (publickey)` or "Could not resolve hostname"
   → **Fork F4**. Timeout with Recon 3 green → retry once, then **Abort A2**.
5. **Remote claude present and subscription-safe (metered-billing gate):**
   ```bash
   ssh -o BatchMode=yes davidcruwys@roamy 'zsh -lc "which claude; claude --version; env | grep -ci anthropic"'
   ```
   → expect `/Users/davidcruwys/.local/bin/claude`, a version line (authoring: `2.1.201
   (Claude Code)`), and `0` on the env grep count. **Any ANTHROPIC_API_KEY/AUTH_TOKEN hit
   (count ≥ 1 naming those vars) → Abort A1 — never boot a worker that could bill metered.**
   `claude not found` under `zsh -lc` → **Fork F3 Route B**. NOTE the path fact: `claude` is
   NOT on the non-interactive SSH PATH (verified at authoring) — every remote invocation below
   uses the absolute `~/.local/bin/claude` and `/opt/homebrew/bin/tmux` for the same reason.
6. **Remote claude is subscription-authed:**
   ```bash
   ssh -o BatchMode=yes davidcruwys@roamy 'python3 -c "
   import json,os
   d=json.load(open(os.path.expanduser(\"~/.claude.json\")))
   print(d.get(\"oauthAccount\",{}).get(\"emailAddress\"), d.get(\"hasAvailableSubscription\"))"'
   ```
   → expect `david@appydave.com True` (authoring state). `None`/missing oauthAccount → **Abort A1**.
7. **Remote repo state:**
   `ssh -o BatchMode=yes davidcruwys@roamy 'git -C ~/dev/ad/apps/dark-factory rev-parse --abbrev-ref HEAD; git -C ~/dev/ad/apps/dark-factory status --short | head -5; git -C ~/dev/ad/apps/dark-factory log --oneline -1'`
   → expect `main`, empty status, some HEAD (authoring: `2eae942`, a clean ancestor 13 commits
   behind the Mini). Dirty or non-main → **Fork F1**.
8. **Mini's main is pushed (so Roamy can sync):**
   `git -C /Users/davidcruwys/dev/ad/apps/dark-factory rev-list --count origin/main..main`
   → expect `0` (authoring: 0, remote `git@github.com:appydave/dark-factory.git`). Non-zero →
   push first in Move 1.
9. **Payload not already run:** `ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/results/wg-t10-01p-roamy-echo.json /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/done/wg-t10-01p-roamy-echo.json 2>&1`
   → expect both absent. Both present with `"hostname": "Roamy"` inside the results file →
   someone got here first: run the Verification block only and report "no-op: already proven".

## Moves

1. **Sync Roamy's repo to current main (fast-forward only — never merge/rebase from here).**
   - **Do:**
     ```bash
     git -C /Users/davidcruwys/dev/ad/apps/dark-factory push origin main   # no-op if Recon 8 was 0
     ssh -o BatchMode=yes davidcruwys@roamy 'git -C ~/dev/ad/apps/dark-factory pull --ff-only origin main && git -C ~/dev/ad/apps/dark-factory log --oneline -1'
     ```
   - **Expect:** pull fast-forwards (or reports up to date); the printed HEAD equals the Mini's
     `git log --oneline -1`.
   - **Failure signal:** `fatal: Not possible to fast-forward` / non-empty status / auth failure
     fetching from GitHub on Roamy.
   - **Counter-move:** → **Fork F1**. (The payload does not depend on repo freshness — F1's
     routes proceed with a stale repo rather than mutating Roamy's git state.)

2. **Author the payload ticket into queue/ and claim it immediately (rename CAS + ownership stamp).**
   - **Do:**
     ```bash
     python3 - <<'EOF'
     import json, os
     from datetime import datetime, timezone
     ROOT = '/Users/davidcruwys/dev/ad/apps/dark-factory/engine/store'
     now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
     tid = 'wg-t10-01p-roamy-echo.json'
     ticket = {
       "ticket": tid,
       "kind": "instruction",
       "title": "T10 Fleet: remote-echo payload — proof job executed on Roamy",
       "source": "backlog/wargames/T10-01-roamy-swagger-worker.md (Move 2)",
       "executor": "roamy-swagger",
       "priority": "high",
       "requested_at": now,
       "requested_by": "wg-t10-01 delegation proof",
       "depends_on": [],
       "prompt": ("You are running on the machine this ticket was delegated TO. "
         "Run these commands with your Bash tool and capture their exact output: "
         "(1) hostname  "
         "(2) git -C /Users/davidcruwys/dev/ad/apps/dark-factory rev-parse --short HEAD  "
         "(3) whoami  "
         "(4) /Applications/Tailscale.app/Contents/MacOS/Tailscale ip -4 2>/dev/null | head -1 "
         "(use an empty string if this one fails). "
         "Then use the Write tool to save EXACTLY this JSON (valid JSON, no prose) to "
         "/Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/remote/wg-t10-01p-roamy-echo.result.json : "
         '{"ticket":"wg-t10-01p-roamy-echo.json","status":"done","hostname":"<output 1>",'
         '"head_sha":"<output 2>","whoami":"<output 3>","tailscale_ip":"<output 4 or empty>",'
         '"notes":"executed remotely for wg-t10-01"} . '
         "Make no edits, no commits, and touch no other files. "
         "Then reply with exactly: ACK wg-t10-01p-roamy-echo.json")
     }
     qp = os.path.join(ROOT, 'queue', tid)
     rp = os.path.join(ROOT, 'running', tid)
     with open(qp, 'w') as f: json.dump(ticket, f, indent=2); f.write('\n')
     os.rename(qp, rp)                     # the engine's proven CAS claim primitive
     t = json.load(open(rp))
     t['claimed_by'] = 'mac-mini-m4-wg-t10-01-dispatch'
     t['claimed_at'] = now
     with open(rp, 'w') as f: json.dump(t, f, indent=2); f.write('\n')
     print('claimed:', rp)
     EOF
     ```
   - **Expect:** prints `claimed: …/engine/store/running/wg-t10-01p-roamy-echo.json`; the file
     exists in running/ with `claimed_by` set; queue/ does not contain it.
   - **Failure signal:** `FileNotFoundError` on the rename (something claimed it between write
     and rename), or the file appears in neither directory.
   - **Counter-move:** → **Fork F2**.

3. **Stage the remote workspace and copy the ticket to Roamy.**
   - **Do:**
     ```bash
     ssh -o BatchMode=yes davidcruwys@roamy 'mkdir -p ~/dev/ad/apps/dark-factory/engine/store/remote'
     scp -o BatchMode=yes /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/running/wg-t10-01p-roamy-echo.json \
         davidcruwys@roamy:'~/dev/ad/apps/dark-factory/engine/store/remote/'
     ssh -o BatchMode=yes davidcruwys@roamy 'python3 -c "import json; print(json.load(open(\"/Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/remote/wg-t10-01p-roamy-echo.json\"))[\"ticket\"])"'
     ```
   - **Expect:** scp completes; the remote parse prints `wg-t10-01p-roamy-echo.json`.
     (`engine/store/remote/` is deliberately a NEW, untracked directory — `engine/store/` is
     git-tracked (35 files at authoring), so remote working files must not land in
     queue/running/results/ on Roamy's copy, and the whole directory is removed in Move 8.)
   - **Failure signal:** scp error, or remote JSON parse fails (truncated copy).
   - **Counter-move:** retry the scp once; a second failure with Recon 4 previously green →
     **Abort A2** (connectivity degraded mid-run).

4. **Boot the remote worker: detached tmux + interactive claude on Roamy.**
   - **Do:** (absolute binary paths are mandatory — Recon 5's PATH fact)
     ```bash
     ssh -o BatchMode=yes davidcruwys@roamy '/opt/homebrew/bin/tmux kill-session -t df-roamy-1 2>/dev/null; /opt/homebrew/bin/tmux new-session -d -s df-roamy-1 -x 220 -y 50'
     ssh -o BatchMode=yes davidcruwys@roamy '/opt/homebrew/bin/tmux send-keys -t df-roamy-1 -l "cd ~/dev/ad/apps/dark-factory && ~/.local/bin/claude --model sonnet --dangerously-skip-permissions --strict-mcp-config"'
     ssh -o BatchMode=yes davidcruwys@roamy '/opt/homebrew/bin/tmux send-keys -t df-roamy-1 Enter'
     # poll for the ready signature (live-proven ~5 s; allow 90 s)
     for i in $(seq 1 18); do
       sleep 5
       PANE=$(ssh -o BatchMode=yes davidcruwys@roamy '/opt/homebrew/bin/tmux capture-pane -t df-roamy-1 -p')
       echo "$PANE" | grep -q "bypass permissions on\|for shortcuts" && { echo "READY after ~$((i*5))s"; break; }
     done
     ```
   - **Expect:** `READY after ~5s` (up to ~15 s is normal). The pane footer shows
     `⏵⏵ bypass permissions on` and the repo path `~/dev/ad/apps/dark-factory (main)`.
   - **Failure signal:** 90 s elapse with no signature; pane shows a login/trust prompt, a
     shell error (`command not found`), or an update screen.
   - **Counter-move:** → **Fork F3**.

5. **Dispatch the pointer turn (single line, zero quote characters — the SPK-D1 idiom over SSH).**
   - **Do:**
     ```bash
     ssh -o BatchMode=yes davidcruwys@roamy "/opt/homebrew/bin/tmux send-keys -t df-roamy-1 -l 'Your ticket id is wg-t10-01p-roamy-echo.json. Read the JSON file at /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/remote/wg-t10-01p-roamy-echo.json and execute its prompt field exactly. Then reply with exactly: ACK wg-t10-01p-roamy-echo.json'"
     sleep 1
     ssh -o BatchMode=yes davidcruwys@roamy '/opt/homebrew/bin/tmux send-keys -t df-roamy-1 Enter'
     ```
     Do NOT reword the pointer prompt: it is deliberately free of apostrophes and double quotes
     so it survives ssh + `tmux send-keys -l` without escaping (the full multi-line instructions
     live in the ticket file the worker reads — never inline them into send-keys).
   - **Expect:** a follow-up `capture-pane` within ~10 s shows the prompt was accepted (the
     text echoed into the input area and a spinner/tool activity, or already the ACK).
   - **Failure signal:** the pane still shows an empty prompt (send-keys landed nowhere) or the
     literal text sitting unsubmitted.
   - **Counter-move:** unsubmitted text → send the Enter keypress again. Empty prompt/no echo →
     the session died between Moves 4 and 5: redo Move 4 once; second failure → **Abort A3**.

6. **Poll for the remote artifact (artifact-is-truth — never trust the chat reply).**
   - **Do:** (live-proven turn time ≈ 5–30 s; budget 300 s, matching the engine's
     WORKER_TIMEOUT=240 plus SSH slack)
     ```bash
     RESULT_REMOTE='/Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/remote/wg-t10-01p-roamy-echo.result.json'
     for i in $(seq 1 20); do
       sleep 15
       ssh -o BatchMode=yes davidcruwys@roamy "test -s $RESULT_REMOTE" && { echo "ARTIFACT after ~$((i*15))s"; break; }
     done
     ```
   - **Expect:** `ARTIFACT after ~15s` (any value ≤ 300 s passes).
   - **Failure signal:** 300 s elapse with no file.
   - **Counter-move:** capture the pane
     (`ssh … '/opt/homebrew/bin/tmux capture-pane -t df-roamy-1 -p' | tail -30`).
     (a) Pane contains a usage-limit signature (`usage limit`, `rate limit`, `429`,
     `out of extended usage`, case-insensitive) → write the engine's BACKOFF flag on the Mini —
     ```bash
     python3 -c "
     import json, datetime
     until=(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=900)).strftime('%Y-%m-%dT%H:%M:%SZ')
     now=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
     json.dump({'ts':now,'until':until,'reason':'usage-limit on remote worker df-roamy-1 (wg-t10-01)','worker':'df-roamy-1'},open('/Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/BACKOFF','w'),indent=2)"
     ```
     — then **Abort A3** (quote the pane in the park file). (b) Pane shows the worker waiting on
     a question → it is confused: send one nudge turn (same no-quote discipline):
     `Continue with the ticket instructions and write the result JSON file now.` + Enter, then
     re-run the poll once. (c) Second poll also empty → **Abort A3**.

7. **Retrieve, verify content, move to done/, append the audit line.**
   - **Do:**
     ```bash
     scp -o BatchMode=yes davidcruwys@roamy:'~/dev/ad/apps/dark-factory/engine/store/remote/wg-t10-01p-roamy-echo.result.json' \
         /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/results/wg-t10-01p-roamy-echo.json
     REMOTE_SHA=$(ssh -o BatchMode=yes davidcruwys@roamy 'git -C ~/dev/ad/apps/dark-factory rev-parse --short HEAD')
     python3 -c "
     import json
     d=json.load(open('/Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/results/wg-t10-01p-roamy-echo.json'))
     assert d['status']=='done', d
     assert d['hostname'].strip()=='Roamy', 'DID NOT run on Roamy: '+repr(d['hostname'])
     assert d['head_sha'].strip()=='$REMOTE_SHA', ('sha mismatch', d['head_sha'], '$REMOTE_SHA')
     print('remote execution PROVEN:', d['hostname'], d['head_sha'], d.get('tailscale_ip'))"
     # session-id evidence: resolve the Roamy-side transcript by content (warm_pool find_session idiom, remoted)
     SESS=$(ssh -o BatchMode=yes davidcruwys@roamy 'grep -l "ticket id is wg-t10-01p-roamy-echo" ~/.claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/*.jsonl 2>/dev/null | head -1')
     echo "remote transcript: ${SESS:-unresolved}"
     mv /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/running/wg-t10-01p-roamy-echo.json \
        /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/done/wg-t10-01p-roamy-echo.json
     python3 -c "
     import json
     entry={'ticket':'wg-t10-01p-roamy-echo.json','attempt':1,'worker':'df-roamy-1(remote:roamy)',
            'session_id':'${SESS##*/}'.replace('.jsonl','') or None,
            'transcript':('roamy:${SESS}' if '${SESS}' else None),
            'claimed_by':'mac-mini-m4-wg-t10-01-dispatch','claimed_at':None}
     open('/Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/audit.jsonl','a').write(json.dumps(entry)+'\n')
     print('audit appended')"
     ```
   - **Expect:** `remote execution PROVEN: Roamy <sha> 100.89.32.35` (tailscale_ip may be
     empty — it is best-effort), `remote transcript: /Users/davidcruwys/.claude/projects/…jsonl`,
     ticket now in done/, `audit appended`.
   - **Failure signal:** hostname assertion fails (artifact says `mac-mini-m4` or anything else)
     — the job ran on the WRONG machine.
   - **Counter-move:** hostname wrong → this is Fork F2's stolen-ticket symptom surfacing late:
     delete the bad results file, go to **Fork F2 Route A**. Transcript unresolved (`SESS` empty)
     → not fatal: record `session_id: null` in the audit line and note it in the report; the
     artifact + pane are sufficient evidence. sha mismatch only → re-read `REMOTE_SHA` once
     (a push/pull may have raced); persists → note the discrepancy in the report, do not fail
     the proof (hostname is the load-bearing assertion).

8. **Teardown: nothing left running or dirty on Roamy.**
   - **Do:**
     ```bash
     ssh -o BatchMode=yes davidcruwys@roamy '/opt/homebrew/bin/tmux kill-session -t df-roamy-1'
     ssh -o BatchMode=yes davidcruwys@roamy 'rm -rf ~/dev/ad/apps/dark-factory/engine/store/remote'
     ssh -o BatchMode=yes davidcruwys@roamy '/opt/homebrew/bin/tmux ls 2>&1; git -C ~/dev/ad/apps/dark-factory status --short'
     ```
   - **Expect:** kill succeeds; final line shows no `df-roamy-*` session (other sessions, e.g.
     overmind ones, are NOT yours to touch) and an empty git status.
   - **Failure signal:** session survives the kill, or git status shows residue under
     `engine/store/`.
   - **Counter-move:** re-run the kill with the exact session name; residue → remove ONLY files
     you created (`engine/store/remote/`); any OTHER dirty path you did not create → leave it,
     quote it in your report (Roamy carries its own KDD work — never clean up files that are
     not yours).

9. **Commit + push the evidence on the Mini; write your self-report.**
   - **Do:**
     ```bash
     cd /Users/davidcruwys/dev/ad/apps/dark-factory
     git add engine/store/results/wg-t10-01p-roamy-echo.json \
             engine/store/done/wg-t10-01p-roamy-echo.json \
             engine/store/audit.jsonl
     git commit -m "proof(fleet): first cross-machine Swagger ticket — claimed on Mini, executed on Roamy, artifact verified back (wg-t10-01)"
     git push
     ```
     Then write the results self-report JSON to the exact path your dispatch prompt gave you.
     If any fork/counter-move fired, say which and why; include the boot/turn timings you
     observed and the Roamy transcript path.
   - **Expect:** commit lands and pushes; `git log --oneline -1` shows the message.
   - **Failure signal:** push rejected (remote moved ahead).
   - **Counter-move:** `git pull --rebase origin main && git push`; if that also fails, leave
     the commit local and record "push pending — remote diverged" in the report. Do not
     force-push.

## Forks

**F1 — Roamy's repo won't fast-forward (dirty tree, diverged, or GitHub auth fails remotely).**
Trigger: Move 1's pull errors, or Recon 7 shows a dirty/non-main state.
→ **Route A** (behind-only but pull fails for auth/network, or dirty with paths unrelated to
`engine/store/`): proceed with the stale repo — the payload only reads `hostname`/`rev-parse`
and writes one new file; repo freshness is not load-bearing. Record "Roamy repo stale/dirty:
<one-line detail>" in the report.
→ **Route B** (diverged — Roamy has local commits not on origin): NEVER merge, rebase, or reset
Roamy's repo from here (Roamy carries its own KDD-stream commits; reconciliation is a
David-side concern). Proceed as Route A and additionally flag "Roamy main diverged from origin
— needs reconciliation" prominently in the report.

**F2 — the payload ticket is claimed by something else (rename fails or hostname proves wrong).**
Trigger: Move 2's rename throws FileNotFoundError, or Move 7's artifact says the job ran on
`mac-mini-m4` — a concurrently-running local engine (Recon 2 missed it or one started mid-run)
swallowed a ticket whose executor tag it does not filter (verified: `dispatchable()` only skips
external-research/deferred).
→ **Route A**: check `running/` and `done/` for the ticket; if a local worker has it or finished
it, let it settle, delete any wrong-machine results file, then re-author the payload with the
same content **directly into running/** (skip queue/ entirely — claim-by-construction) and
continue from Move 3. Record "local engine raced the queue; payload re-authored direct-to-running".
→ **Route B**: the ticket is in neither queue/, running/, nor done/ — filesystem anomaly, not a
race → **Abort A3** with the `ls` output of all three directories quoted.

**F3 — the remote claude never reaches the ready signature.**
Trigger: Move 4's 90 s poll expires.
→ **Route A** (pane shows a login/onboarding/trust prompt — the worker is not authenticated or
needs first-run consent): kill the session, → **Abort A1** (David must log in / accept on Roamy;
never type credentials or accept trust dialogs on his behalf).
→ **Route B** (pane shows `command not found` or a shell error — the claude binary moved):
re-derive the path via `ssh … 'zsh -lc "which claude"'`, substitute it, redo Move 4 once. Pane
shows an update/migration screen or second failure → **Abort A3** with the pane quoted.

**F4 — SSH via the MagicDNS name `roamy` fails from this machine.**
Trigger: Recon 4 returns "Could not resolve hostname" or `Permission denied (publickey)`.
→ **Route A**: try the pinned alias — `ssh -o BatchMode=yes davidcruwys@macbook-pro-m4 'echo ok; hostname'`
(verified at authoring: `~/.ssh/config` pins `macbook-pro-m4` → `100.89.32.35`, User
`davidcruwys`). Succeeds → substitute `macbook-pro-m4` for `roamy` in every ssh/scp Do line and
record "MagicDNS path failed; used pinned alias" in the report. (This satisfies "never .local" —
the alias resolves to the Tailscale IP, not mDNS.)
→ **Route B**: both names fail → no key/route reaches Roamy → **Abort A2**.

## Assumptions ledger

1. **The seed's IP `100.82.235.39` is a typo for Roamy's `100.89.32.35`.** Verified live:
   `tailscale status` shows `100.82.235.39` is `mac-mini-m4` (this machine) and `roamy` is
   `100.89.32.35`; the brief's direction ("claimed on the Mini, executed on Roamy") is
   unambiguous, so the target is Roamy. If David meant a different topology (e.g. Roamy pulling
   FROM the Mini), that is a different ticket → park via **Abort A4** only if an instruction
   arrives mid-run contradicting this; otherwise proceed.
2. **Tailscale identity stays `roamy` / 100.89.32.35.** Renamed 2026-07-03, stable since. If
   false, Recon 3 derives the current MagicDNS name and substitutes it throughout; no candidate
   row → Abort A2.
3. **Roamy stays subscription-authed (david@appydave.com) with no ANTHROPIC env vars.** Verified
   at authoring (Recon 5/6 re-verify). If false → Abort A1 — this is the one non-negotiable gate.
4. **The claude TUI ready signature (`bypass permissions on` / `for shortcuts`) and idle
   behaviour are stable.** True for 2.1.201 (Roamy) at authoring, same strings
   `engine/warm_pool.py` keys on. If a future version changes them, Move 4's poll times out →
   Fork F3 (the pane quote in the park file will show the new UI for re-grounding).
5. **No always-on local engine claims queue tickets during the run.** Verified at authoring
   (no orchestrator process, no tmux server) and re-checked in Recon 2. If the factory later
   runs a persistent pool, this procedure's queue-hop should be replaced by direct-to-running
   authoring (Fork F2 Route A's mechanism) — note it for T10-06.
6. **~5 s boot / ~5–30 s turn timings hold.** Live-measured at authoring over an active direct
   Tailscale connection. A relayed (DERP) connection may be slower — the budgets (90 s boot,
   300 s artifact) absorb that; do not tighten them.

## Abort conditions

- **A1 — metered-billing or auth risk on the remote worker.** (Recon 5 finds ANTHROPIC_API_KEY/
  AUTH_TOKEN on Roamy, Recon 6 shows no subscription auth, or F3-A hits a login prompt.) NEVER
  boot (or immediately kill) the remote claude. Park: write
  `engine/store/needs-decision/wg-t10-01-roamy-swagger-worker.json` with
  `{"ticket":"wg-t10-01-roamy-swagger-worker","question":"Roamy's claude cannot be used subscription-safely: <observed state, verbatim — env var name or auth screen text>. Fix on Roamy (unset the env var in the shell profile / log claude in as the subscription account), then say go.","proposed":"re-run this war game from Recon once Roamy's claude is subscription-safe","note":"per war game T10-01 A1 — no -p, no SDK, no metered billing, ever"}`.
  Leave the ticket in `running/`.
- **A2 — Roamy not reachable/alive from this machine.** (Recon 3 offline / no row, Recon 4 or
  mid-run SSH failures after retry, F4-B.) If the failure happens mid-run, first attempt Move 8's
  teardown (best-effort — skip what times out). Park with question:
  `"Roamy is asleep/unreachable (or no SSH key reaches it) so the cross-machine proof cannot run. Wake Roamy / check Tailscale on both ends (expected: roamy = 100.89.32.35 active) and say go. Nothing was left running remotely: <teardown outcome>."`
  Leave the ticket in `running/`.
- **A3 — the remote worker never lands the artifact (or a filesystem anomaly) after all
  counter-moves.** FIRST tear down: kill `df-roamy-1`, but LEAVE
  `~/dev/ad/apps/dark-factory/engine/store/remote/` on Roamy intact (forensics). Move the payload
  ticket back from `running/` to `queue/` is WRONG here — leave it in `running/` (it is evidence
  of the attempt). Park with the last 30 pane lines quoted verbatim in the question, plus the
  BACKOFF note if a usage-limit signature fired.
- **A4 — direction/topology contradiction.** (Only reachable via Assumption 1's false branch —
  an explicit David instruction mid-run that the delegation direction is wrong.) Stop, park with
  both readings stated and which recon facts support each.

## Verification

Executable acceptance (mirrors the ticket's `verify` field). Run on the Mini.

```bash
# 1. The artifact came back and proves remote execution
python3 -c "
import json
d=json.load(open('/Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/results/wg-t10-01p-roamy-echo.json'))
assert d['status']=='done'
assert d['hostname'].strip()=='Roamy', d
assert len(d['head_sha'].strip())>=7
print('artifact OK:', d['hostname'], d['head_sha'], d.get('tailscale_ip'))"

# 2. The payload ticket completed the full lifecycle with ownership recorded
python3 -c "
import json, os
p='/Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/done/wg-t10-01p-roamy-echo.json'
t=json.load(open(p))
assert t['claimed_by']=='mac-mini-m4-wg-t10-01-dispatch', t.get('claimed_by')
assert not os.path.exists(p.replace('/done/','/queue/')) and not os.path.exists(p.replace('/done/','/running/'))
print('lifecycle OK: queue->running->done, claimed_by stamped')"

# 3. Audit trail names the remote worker
tail -3 /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/audit.jsonl | grep -q 'wg-t10-01p-roamy-echo' && echo audit OK

# 4. Evidence is committed
git -C /Users/davidcruwys/dev/ad/apps/dark-factory log --oneline -5 | grep -qi 'wg-t10-01' && echo commit OK

# 5. Nothing left running on Roamy; its tree is clean; remote workspace removed
ssh -o BatchMode=yes davidcruwys@roamy '/opt/homebrew/bin/tmux ls 2>&1 | grep df-roamy && echo LEFTOVER || echo no leftover session'
ssh -o BatchMode=yes davidcruwys@roamy 'test -d ~/dev/ad/apps/dark-factory/engine/store/remote && echo LEFTOVER-DIR || echo remote dir gone'
ssh -o BatchMode=yes davidcruwys@roamy 'git -C ~/dev/ad/apps/dark-factory status --short | grep "engine/store" && echo DIRTY || echo store clean'
```

Negative checks (what must NOT have changed):

```bash
# Engine source untouched — this was a proof, not a build
test -z "$(git -C /Users/davidcruwys/dev/ad/apps/dark-factory status --short -- engine/orchestrator.py engine/warm_pool.py engine/halt.py)" && echo engine src untouched

# The pre-existing deferred ticket still sits in queue/ unmolested
ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/queue/ | grep -q 'project-digest-list-and-project-2' && echo queue undisturbed

# No HALT/BACKOFF left behind (BACKOFF acceptable ONLY if A3's usage-limit branch fired — then it self-expires)
ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/HALT 2>/dev/null && echo UNEXPECTED-HALT || echo no HALT

# No git mutation on Roamy (no new commits, no branch change)
ssh -o BatchMode=yes davidcruwys@roamy 'git -C ~/dev/ad/apps/dark-factory rev-parse --abbrev-ref HEAD'   # expect: main
```

## Executor notes (sonnet)

- **Scope fence:** you may create exactly these Mini-side files — the payload ticket (queue/ →
  running/ → done/), `engine/store/results/wg-t10-01p-roamy-echo.json`, one audit.jsonl line,
  and your self-report. On Roamy you may create only `~/dev/ad/apps/dark-factory/engine/store/remote/`
  (removed in Move 8) and the tmux session `df-roamy-1` (killed in Move 8). Do NOT edit
  `engine/orchestrator.py`, `engine/warm_pool.py`, or any engine source on either machine. Do
  NOT install anything on Roamy. Do NOT touch Roamy's other tmux sessions (an overmind session
  existed at authoring), its launchd agents, or its git state beyond the ff-only pull.
- **The metered-billing gate is absolute.** Recon 5/6 exist because a single `-p` call or an
  API-key-authed worker bills real money. If anything about Roamy's claude auth looks unusual,
  A1 — a parked question costs nothing.
- **Quoting discipline:** every string that passes through `ssh … tmux send-keys -l` must
  contain no apostrophes or double quotes. Both dispatch prompts in this war game are
  pre-sanitized — reuse them verbatim; if you must compose a new nudge, strip all quote
  characters first.
- **HITL over guessing:** ambiguity about which machine the seed meant, Roamy auth state, or a
  diverged Roamy repo → park (A1/A4) or flag (F1-B). Never "fix" Roamy's world to make the
  proof pass.
- **The rabbit hole:** generalizing this into a reusable dispatch script, a Roamy warm pool,
  CAP accounting, machine-tag routing, or a fleet HALT relay. All of that is T10-06 / T10-02
  territory. This ticket is ONE ticket across the seam with evidence — the moment your proof
  commit lands, you are done. Skip the generalization.
