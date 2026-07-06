# T6-03 — Fix sentinel blind-to-Roamy

| field | value |
|---|---|
| ticket | wg-t6-03-sentinel-roamy-liveness |
| track / size / priority | T6 Constellation / M / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

The fleet sentinel reports the MacBook Pro **offline while it is alive**, and that lie is
quietly consumed (MCP `fleet_status`, daily snapshots, anything reading
`snapshots/sentinel-latest.json`). Root cause was **verified live at authoring
(2026-07-06)**: the machine was renamed to **Roamy** on 2026-07-03; its Tailscale MagicDNS name
is `roamy` (100.89.32.35), but the running sentinel's `sentinel.config.json` still says
`"host": "macbook-pro"`, and `ssh macbook-pro` now fails with *"Could not resolve hostname"* —
which `sshStatus()` maps to `unreachable` → snapshot status `offline`. Meanwhile
`ssh davidcruwys@roamy 'echo ok; hostname'` returns `ok` / `Roamy` from this machine. The fix
is a config rename + daemon restart in the RUNNING deployment
(`~/dev/ad/apps/appyradar-sentinal` — the **'a'** spelling), plus the same rename in the clean
re-scaffold's example config (`~/dev/ad/apps/appyradar-sentinel` — the **'e'** spelling) so a
future migration doesn't reintroduce the blindness. Done looks like: a fresh
`sentinel-latest.json` shows Roamy **online**, before/after evidence is stored in
`engine/store/results/`, and the 'e'-repo example config is committed and pushed.

## Locked context

- decisions.md Q8: fleet scope is **+ Roamy** — fixing sentinel blind-to-Roamy is explicitly
  in scope.
- decisions.md Q4: everything through the engine — this is a sonnet-Swagger engine ticket.
- Spec globals: no `-p`/headless/SDK ever; HALT/BACKOFF respected implicitly; no YLO/POEM work.
- Standing preference (auto-memory, "David's naming over dev-speak"): the machine is **Roamy**,
  so the logical `name` field renames too — unless Fork F1 Route B forces host-only.

## Recon (verify before any work)

All paths absolute. Authoring-time expectations noted; docs lag code — trust only what you see.

1. **Daemon running?** `launchctl list | grep appyradar-sentinal` → expect one line: a PID,
   status `0`, label `com.appydave.appyradar-sentinal` (plist at
   `~/Library/LaunchAgents/com.appydave.appyradar-sentinal.plist`, `KeepAlive: true`, runs
   `bun run /Users/davidcruwys/dev/ad/apps/appyradar-sentinal/src/main.ts`). Not listed →
   **Fork F2**.
2. **Blindness still present?**
   ```bash
   python3 -c "
   import json
   d=json.load(open('/Users/davidcruwys/dev/ad/apps/appyradar-sentinal/snapshots/sentinel-latest.json'))
   print('generated_at:', d['generated_at'])
   print('offline_machines:', d['summary']['offline_machines'])
   for m in d['machines']: print(m['machine'],'|',m['host'],'|',m['status'])
   "
   ```
   → expect `macbook-pro | macbook-pro | offline` (authoring state: offline_machines =
   `["macbook-pro","mac-mini-m2","mary"]`). If a `roamy` or `macbook-pro` entry already reads
   `online` → **Fork F3**.
3. **Roamy alive on the tailnet?**
   `/Applications/Tailscale.app/Contents/MacOS/Tailscale status | grep -i roamy`
   (fall back to `tailscale status` if that path is gone) → expect a line like
   `100.89.32.35   roamy   david@   macOS   -` (a `-` or `active` tail means up; `offline,
   last seen …` means down → **Abort A2** after Moves 1–3 — the config fix is correct
   regardless, but the end-to-end proof can't complete). If no `roamy` row exists at all, the
   machine was renamed AGAIN: take the current MagicDNS name of 100.89.32.35 from the status
   output and substitute it for `roamy` in every Do line below (Assumption 1).
4. **SSH proof from your shell:**
   `ssh -o ConnectTimeout=8 -o BatchMode=yes -o StrictHostKeyChecking=no davidcruwys@roamy 'echo ok; hostname'`
   → expect `ok` then `Roamy`. `Permission denied (publickey)` → **Fork F4**. Timeout with
   Recon 3 green → retry once, then **Abort A2**.
5. **Config state:** `cat /Users/davidcruwys/dev/ad/apps/appyradar-sentinal/sentinel.config.json`
   → expect a `machines` array of 5 (`macbook-pro`, `mac-mini-m4`, `mac-mini-m2`, `jan`,
   `mary`) with the first entry `{"name": "macbook-pro", "host": "macbook-pro"}`, plus
   `collectIntervalMinutes: 10`. Also confirm it is per-deployment (not tracked):
   `git -C /Users/davidcruwys/dev/ad/apps/appyradar-sentinal check-ignore sentinel.config.json`
   → prints the filename (verified at authoring: `.gitignore` line 4). If it is now TRACKED,
   commit it in Move 7 alongside the 'e'-repo change.
6. **Consumer sweep — does anything key on the logical name `"macbook-pro"`?**
   ```bash
   grep -rln '"macbook-pro"' /Users/davidcruwys/dev/ad/apps /Users/davidcruwys/dev/ad/apps/dark-factory/engine 2>/dev/null \
     | grep -v node_modules | grep -v appyradar-sentin | grep -v /snapshots/ | grep -v backlog/wargames
   ```
   → expect **empty** (authoring sweep: the only non-sentinel hits are app-registry's
   `"macbook-pro-2"` — a *different* string naming Switchboard's machine, not a
   sentinel-snapshot consumer). Any hit that actually READS sentinel snapshots and matches on
   the machine name → **Fork F1**.
7. **Engine flags:** `ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/HALT 2>&1` →
   expect absent. Present → stop immediately, park per the engine's standing HALT rule.

## Moves

1. **Capture before-evidence (snapshot + config backup).**
   - **Do:**
     ```bash
     cp /Users/davidcruwys/dev/ad/apps/appyradar-sentinal/snapshots/sentinel-latest.json \
        /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/results/wg-t6-03-before.json
     cp /Users/davidcruwys/dev/ad/apps/appyradar-sentinal/sentinel.config.json \
        /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/results/wg-t6-03-config-before.json
     ```
   - **Expect:** both files exist and are non-empty; the before-snapshot contains the
     `offline` verdict from Recon 2.
   - **Failure signal:** source file missing.
   - **Counter-move:** snapshot missing → the daemon never wrote one; treat as Fork F2.
     Config missing → deployment changed → Abort A1.

2. **Edit the live config: `macbook-pro`/`macbook-pro` → `roamy`/`roamy`.**
   - **Do:**
     ```bash
     python3 - <<'EOF'
     import json
     p = '/Users/davidcruwys/dev/ad/apps/appyradar-sentinal/sentinel.config.json'
     cfg = json.load(open(p))
     hit = False
     for m in cfg['machines']:
         if m['name'] == 'macbook-pro':
             m['name'] = 'roamy'   # skip this line ONLY under Fork F1 Route B
             m['host'] = 'roamy'
             hit = True
     assert hit, 'no macbook-pro entry found'
     open(p, 'w').write(json.dumps(cfg, indent=2) + '\n')
     print('ok:', [ (m['name'], m['host']) for m in cfg['machines'] ])
     EOF
     ```
   - **Expect:** prints `ok:` with 5 machines, `('roamy', 'roamy')` first, the other 4
     entries byte-identical to before.
   - **Failure signal:** assertion error (no `macbook-pro` entry) or JSON decode error.
   - **Counter-move:** no-entry → re-read the config; if a `roamy` entry already exists this
     is Fork F3 territory — go there. Decode error → restore from
     `wg-t6-03-config-before.json` and retry once; second failure → Abort A3.

3. **Restart the daemon (config is loaded once at startup — a restart is mandatory).**
   - **Do:** record the moment first, then kick:
     ```bash
     RESTART_TS=$(date -u +%Y-%m-%dT%H:%M:%SZ); echo "$RESTART_TS"
     launchctl kickstart -k gui/$(id -u)/com.appydave.appyradar-sentinal
     sleep 3; launchctl list | grep appyradar-sentinal
     ```
   - **Expect:** the grep shows a PID (new process) with status `0`. On start the daemon runs
     a collection cycle immediately (verified in `src/main.ts`: `await runCollection()` before
     the `setInterval`), so a fresh snapshot lands within minutes — no 10-minute wait.
   - **Failure signal:** kickstart errors, or no PID in the list.
   - **Counter-move:**
     `launchctl unload ~/Library/LaunchAgents/com.appydave.appyradar-sentinal.plist && launchctl load ~/Library/LaunchAgents/com.appydave.appyradar-sentinal.plist`,
     re-check, and read the last 30 lines of
     `/Users/davidcruwys/dev/ad/apps/appyradar-sentinal/logs/stderr.log` +
     `logs/stdout.log`. Still no PID after one retry → Abort A3.

4. **Wait for the post-restart cycle and confirm Roamy reads online.**
   - **Do:** poll up to 12 × 30 s (a full cycle SSHes 5 machines in series; genuinely-offline
     ones each burn an 8 s ConnectTimeout — expect 1–4 min total):
     ```bash
     python3 - <<EOF
     import json, time, sys
     p = '/Users/davidcruwys/dev/ad/apps/appyradar-sentinal/snapshots/sentinel-latest.json'
     restart = "$RESTART_TS"
     for i in range(12):
         d = json.load(open(p))
         if d['generated_at'] > restart:
             row = [m for m in d['machines'] if m['machine'] in ('roamy', 'macbook-pro')]
             print('generated_at:', d['generated_at'])
             print('row:', row[0]['machine'], row[0]['status'])
             print('offline_machines:', d['summary']['offline_machines'])
             sys.exit(0 if row and row[0]['status'] == 'online' else 1)
         time.sleep(30)
     print('no fresh snapshot after 6 min'); sys.exit(2)
     EOF
     ```
   - **Expect:** exit 0 — `row: roamy online`, and `roamy` absent from `offline_machines`.
   - **Failure signal:** exit 1 (fresh snapshot, Roamy still offline) or exit 2 (no fresh
     snapshot at all).
   - **Counter-move:** exit 2 → the daemon is wedged: check `launchctl list` + the two logs,
     redo Move 3's counter-move once. Exit 1 with Recon 4 green → the daemon's ssh resolves
     differently from your shell: append a pinned block to `~/.ssh/config` —
     ```
     Host roamy
         HostName 100.89.32.35
         User davidcruwys
     ```
     — then repeat Moves 3–4 once. Second failure of either kind → Abort A3.

5. **Confirm the consumed surface (MCP) sees the truth.**
   - **Do:** if your session has `mcp__appyradar-sentinel__fleet_status`, call it. Otherwise
     this is equivalent and sufficient (verified: the MCP binding at
     `appyradar-sentinal/src/access/bindings/mcp.ts` reads
     `snapshots/sentinel-latest.json` per call — no MCP restart needed):
     ```bash
     python3 -c "
     import json
     d=json.load(open('/Users/davidcruwys/dev/ad/apps/appyradar-sentinal/snapshots/sentinel-latest.json'))
     print(d['summary'])"
     ```
   - **Expect:** online count is one higher than the before-evidence; `roamy` not in
     `offline_machines`.
   - **Failure signal:** MCP tool returns a stale/different summary than the file.
   - **Counter-move:** a second snapshot writer exists → Abort A1 (deployment ambiguity is
     David's call). File-only path can't fail independently of Move 4; if it somehow does,
     re-run Move 4's poll.

6. **Future-proof the re-scaffold ('e' repo) example config.**
   - **Do:** in `/Users/davidcruwys/dev/ad/apps/appyradar-sentinel/sentinel.config.example.json`
     replace the line `{ "name": "macbook-pro", "host": "macbook-pro" },` with
     `{ "name": "roamy",       "host": "roamy" },` (line 3 at authoring; keep the file's
     column-aligned style).
   - **Expect:** `git -C /Users/davidcruwys/dev/ad/apps/appyradar-sentinel diff --stat` shows
     exactly `sentinel.config.example.json | 2 +-` (one line changed).
   - **Failure signal:** the line isn't there (example already updated, or file moved).
   - **Counter-move:** already says `roamy` → skip, note "e-repo already correct". File
     gone → note it and move on; do NOT hunt for a new home (that's the migration ticket's
     job).

7. **Commit + push the 'e' repo change.**
   - **Do:** (repo verified clean, branch `main`, remote
     `git@github.com:appydave/appyradar-sentinel.git`)
     ```bash
     cd /Users/davidcruwys/dev/ad/apps/appyradar-sentinel
     git add sentinel.config.example.json
     git commit -m "fix(config): macbook-pro -> roamy — machine renamed 2026-07-03, old host never resolved (wg-t6-03)"
     git push origin main
     ```
   - **Expect:** push accepted; `git log --oneline -1` shows the commit.
   - **Failure signal:** push rejected (remote moved ahead).
   - **Counter-move:** `git pull --rebase origin main && git push origin main`; if that also
     fails, leave the commit local and record "push pending — remote diverged" in the results
     note. Do not force-push.

8. **Capture after-evidence and commit it in dark-factory.**
   - **Do:**
     ```bash
     cp /Users/davidcruwys/dev/ad/apps/appyradar-sentinal/snapshots/sentinel-latest.json \
        /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/results/wg-t6-03-after.json
     cd /Users/davidcruwys/dev/ad/apps/dark-factory
     git add engine/store/results/wg-t6-03-before.json \
             engine/store/results/wg-t6-03-config-before.json \
             engine/store/results/wg-t6-03-after.json
     git commit -m "proof(constellation): sentinel sees Roamy — before/after evidence (wg-t6-03)"
     git push
     ```
     Then write the results self-report JSON to the exact path your dispatch prompt gave you.
     If any fork/counter-move fired, say which and why in the report.
   - **Expect:** commit lands; `wg-t6-03-after.json` contains `"roamy"` with
     `"status": "online"`.
   - **Failure signal:** after-file still shows offline (you skipped a failed Move 4).
   - **Counter-move:** never commit an after-file that doesn't prove the fix — go back to
     Move 4's counter-move or Abort A3.

## Forks

**F1 — the consumer sweep (Recon 6) finds something keying on the logical name
`"macbook-pro"` in sentinel snapshots.**
Trigger: a non-sentinel file both reads sentinel snapshot data and matches the machine name
literally. (`"macbook-pro-2"` hits are NOT this — different string, Switchboard's machine
field in app-registry, not a snapshot consumer.)
→ **Route A** (the consumer's fix is a ≤2-line literal rename, same semantics): update it in
the same pass, include it in the evidence commit, name it in the results report.
→ **Route B** (non-trivial, ambiguous, or in a repo you shouldn't touch): keep
`"name": "macbook-pro"` and change ONLY `"host"` to `"roamy"` in Move 2 (liveness is fixed;
naming continuity preserved). Record "logical-name rename deferred — consumer at <path>" in
the results report. Verification then expects machine `macbook-pro` online.

**F2 — the launchd daemon is not running at recon.**
Trigger: Recon 1 grep is empty.
→ **Route A** (`~/Library/LaunchAgents/com.appydave.appyradar-sentinal.plist` exists and the
'a' repo is intact): `launchctl load` the plist, re-run Recon 1; a PID appears → proceed from
Recon 2.
→ **Route B** (plist gone, or the 'a' repo path is missing/empty): the deployment world has
changed since authoring — most likely the appyradar-sentinal→sentinel migration landed →
**Abort A1**.

**F3 — the blindness is already fixed at recon.**
Trigger: Recon 2 shows a `roamy` (or `macbook-pro`) row with `status: online`.
→ **Route A** (config already carries a resolvable host — `roamy` or equivalent): someone got
here first. Run the Verification block only, skip Moves 1–4; still do Moves 6–7 if the 'e'
example config is stale, then report "no-op: already fixed, verified".
→ **Route B** (snapshot says online but the config still says `host: macbook-pro`): a
contradiction — the snapshot has another writer. Re-read once after 60 s; if it persists →
**Abort A1**.

**F4 — SSH to Roamy denied (publickey) from your shell.**
Trigger: Recon 4 returns `Permission denied (publickey)`.
→ **Route A** (`ssh -o BatchMode=yes macbook-pro-m4 'echo ok'` succeeds — that alias pins
`100.89.32.35` + `User davidcruwys` in `~/.ssh/config`, verified working at authoring): use
`"host": "macbook-pro-m4"` in Move 2 instead of `roamy` (keep `"name": "roamy"` unless F1-B).
Record "host uses ssh-config alias; MagicDNS path denied" as naming debt in the report.
→ **Route B** (both routes denied): no key reaches Roamy from this machine → **Abort A2**.

## Assumptions ledger

1. **Tailscale identity stays `roamy` / 100.82.x.x-net 100.89.32.35.** Renamed 2026-07-03,
   stable since. If false, Recon 3 derives the machine's CURRENT MagicDNS name from
   `tailscale status` (the macOS row that isn't a mini) and substitutes it for `roamy`
   throughout; if no such row exists → Abort A2.
2. **No consumer keys on the logical name `"macbook-pro"`.** Authoring sweep found none
   (app-registry's `"macbook-pro-2"` is a different concept). If false → Fork F1.
3. **The 'a'→'e' repo migration has not landed.** It's a sibling T6 seed with no war game in
   `backlog/wargames/` at authoring. If false → Fork F2 Route B / Abort A1: ask which
   deployment is authoritative rather than fixing a corpse. This ticket deliberately has no
   depends_on — it fixes the RUNNING deployment either way, and Move 6 pre-fixes the successor.
4. **Executor's shell has David's SSH keys/agent.** BatchMode key auth to the fleet worked from
   a subagent shell at authoring. If false → Fork F4.
5. **Historical snapshot discontinuity is accepted.** Daily snapshot files before 2026-07-06
   say `macbook-pro`; after, `roamy`. No tool joins across days on machine name (per the same
   sweep). If such a tool appears later, this file records the rename date.

## Abort conditions

- **A1 — deployment world changed / ambiguous authority.** (F2-B, F3-B, Move 5's second-writer
  case, or the 'a' repo missing.) Park: write
  `engine/store/needs-decision/<your ticket filename>.json` with
  `{"ticket":"wg-t6-03-sentinel-roamy-liveness","question":"Sentinel deployment has changed since authoring: <observed state, verbatim>. Which deployment is authoritative for fleet liveness — appyradar-sentinal (a, launchd com.appydave.appyradar-sentinal) or appyradar-sentinel (e, re-scaffold)? Apply the Roamy host fix (host: roamy) there.","proposed":"fix whichever config the running collector actually loads, then restart it","note":"per war game T6-03 A1"}`.
  Leave the ticket in `running/`. Never guess which system is real.
- **A2 — Roamy not provably alive from this machine.** (Recon 3 shows offline / no row, or
  F4-B.) Still complete Moves 1–3 IF hostname resolution itself works (`ssh roamy` failing
  with a timeout is correct-config-unreachable-machine; failing with "Could not resolve
  hostname" means MagicDNS is broken — then also A1-style park). Then park with:
  question `"Roamy is asleep/unreachable (or its SSH key is missing) so the end-to-end
  liveness proof cannot complete. Wake Roamy (or run: ssh-copy-id davidcruwys@roamy) and say
  go — the config fix is already applied and the next collection cycle will prove it."`
  Leave the ticket in `running/`.
- **A3 — the daemon won't start, or still reports Roamy offline after all counter-moves.**
  FIRST restore the live config —
  `cp engine/store/results/wg-t6-03-config-before.json /Users/davidcruwys/dev/ad/apps/appyradar-sentinal/sentinel.config.json`
  — and re-run Move 3 so fleet collection is never left dead. Then park with the exact error
  output (stderr.log tail, poll exit code) quoted verbatim in the question. Leave the ticket
  in `running/`.

## Verification

Executable acceptance (mirrors the ticket's `verify` field). Under F1-B substitute
`macbook-pro` for `roamy` in checks 1–2; under F4-A the host check expects `macbook-pro-m4`.

```bash
# 1. Live config carries a resolvable host for Roamy
python3 -c "
import json
cfg=json.load(open('/Users/davidcruwys/dev/ad/apps/appyradar-sentinal/sentinel.config.json'))
row=[m for m in cfg['machines'] if m['name'] in ('roamy','macbook-pro')][0]
assert row['host'] != 'macbook-pro', 'host still unresolvable'
assert len(cfg['machines']) == 5, 'machine list mutated'
print('config OK:', row)"

# 2. Fresh snapshot (≤ 2 collection intervals old) shows Roamy online
python3 -c "
import json, datetime
d=json.load(open('/Users/davidcruwys/dev/ad/apps/appyradar-sentinal/snapshots/sentinel-latest.json'))
age=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(d['generated_at'].replace('Z','+00:00'))).total_seconds()
assert age < 1200, f'snapshot stale ({age:.0f}s) — daemon not cycling'
row=[m for m in d['machines'] if m['machine'] in ('roamy','macbook-pro')][0]
assert row['status']=='online', f'still blind: {row}'
assert row['machine'] not in d['summary']['offline_machines']
print('snapshot OK:', row['machine'], row['status'], d['generated_at'])"

# 3. Daemon alive
launchctl list | grep -q appyradar-sentinal && echo daemon OK

# 4. Evidence pair exists and tells the before/after story
test -s /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/results/wg-t6-03-before.json
test -s /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/results/wg-t6-03-after.json
grep -q '"offline"' /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/results/wg-t6-03-before.json && echo evidence OK

# 5. 'e' repo example fixed and committed
grep -q '"roamy"' /Users/davidcruwys/dev/ad/apps/appyradar-sentinel/sentinel.config.example.json
git -C /Users/davidcruwys/dev/ad/apps/appyradar-sentinel log --oneline -3 | grep -qi "wg-t6-03" && echo e-repo OK
```

Negative checks (what must NOT have changed):

```bash
# No source-code edits in the running 'a' repo (config is gitignored; src must stay untouched)
test -z "$(git -C /Users/davidcruwys/dev/ad/apps/appyradar-sentinal status --short -- src/)" && echo src untouched

# The other 4 machine entries are intact
python3 -c "
import json
cfg=json.load(open('/Users/davidcruwys/dev/ad/apps/appyradar-sentinal/sentinel.config.json'))
names=sorted(m['name'] for m in cfg['machines'])
assert names==sorted(['roamy','mac-mini-m4','mac-mini-m2','jan','mary']) or names==sorted(['macbook-pro','mac-mini-m4','mac-mini-m2','jan','mary']), names
print('fleet list intact')"

# launchd label and MCP wiring untouched
grep -q "appyradar-sentinal/src/main.ts" ~/Library/LaunchAgents/com.appydave.appyradar-sentinal.plist
python3 -c "
import json
d=json.load(open('$HOME/.claude.json'))
assert 'appyradar-sentinal/src/access/bindings/mcp.ts' in json.dumps(d.get('mcpServers',{}).get('appyradar-sentinel',{})); print('mcp wiring intact')"
```

## Executor notes (sonnet)

- **Scope fence:** touch exactly three files — the 'a' repo's `sentinel.config.json`
  (gitignored, live), the 'e' repo's `sentinel.config.example.json`, and evidence under
  dark-factory `engine/store/results/`. Never edit collector source (`src/**`) in either repo.
  Never rename the launchd label, the MCP server key, or the 'a'/'e' folder spellings — the
  `appyradar-sentinel` MCP name being backed by the `appyradar-sentinal` repo is a KNOWN trap,
  not yours to fix. The 'a' repo has pre-existing dirty files (README, docs, .mochaccino,
  node_modules) — never stage or commit them.
- **Adjacent false-offline, do NOT chase:** `mac-mini-m2` also reads offline while Tailscale
  shows it up — its ssh alias resolves via `mac-mini-m2.local` (mDNS), likely the same class
  of bug. One sentence in your results report ("mac-mini-m2 probable false-offline via stale
  .local host — follow-up candidate"), nothing more. Same for `mary` (genuinely offline at
  authoring) and app-registry's third name `"macbook-pro-2"` for this same machine (naming
  debt, out of scope).
- **HITL over guessing:** any ambiguity about WHICH sentinel deployment is live → A1. A parked
  ticket with a sharp question beats a fix applied to a corpse.
- **The rabbit hole:** the appyradar-sentinal→appyradar-sentinel migration (repo consolidation,
  launchd re-point, spelling cleanup). It is a separate T6 seed. This ticket fixes liveness in
  the running system and pre-fixes the successor's example config — nothing else. Skip it.
