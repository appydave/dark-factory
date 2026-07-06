# T6-02 — Migrate sentinel 'a'→'e'

| field | value |
|---|---|
| ticket | wg-t6-02-sentinel-migration |
| track / size / priority | T6 Constellation / M / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

The fleet collector that feeds all liveness data is running out of the legacy typo'd repo
`~/dev/ad/apps/appyradar-sentinal` ('a': launchd daemon `com.appydave.appyradar-sentinal`
runs its `src/main.ts`; the global MCP server named `appyradar-sentinel` points at its
`src/access/bindings/mcp.ts`; 113 files dirty, last commit 2026-04-28). The clean re-scaffold
`~/dev/ad/apps/appyradar-sentinel` ('e') exists (2 commits, built on published
`@appydave/appysentinel-core`) but has never been installed, configured, or run. Done means:
the 'e' repo is installed, configured, smoke-proven (collector writes a fresh snapshot; MCP
answers `tools/list`), the launchd daemon and the global MCP registration both point at 'e',
the 'a' repo is retired in place (daemon stopped, dirty tree committed + pushed with a
RETIRED banner — folder NOT deleted), 'e' is registered in locations.json, and
dark-factory's `docs/constellation-map.md` reflects the new truth. Fixing sentinel's
blind-to-Roamy defect is explicitly NOT this ticket (that is T6-03).

## Locked context

- **Q4 (decisions.md):** everything through the engine — written for sonnet Swagger dispatch;
  no `-p`/headless/SDK ever; interactive-session tooling only (`claude mcp` config CLI is fine,
  spawning sessions is not).
- **Q8 (decisions.md):** fleet work is in scope, but blind-to-Roamy is its own candidate
  (T6-03) — this ticket must not attempt it.
- **Register-every-new-app standing rule:** 'e' gets a locations.json entry at cutover
  (app-registry and constellation-map already carry it).
- **Repo-trap memory (canonical):** `appysentinal→appysentinel` was a RENAME (redirect);
  `appyradar-sentinel` is a NEW re-scaffold, NOT the same lineage as `appyradar-sentinal`.
  Never treat 'e' as a git continuation of 'a' — no merges, no history grafts.
- **Never commit secrets** — the 113-file dirty legacy tree gets a secrets scan before its
  archive commit.
- **Docs-lag-code rule:** every state claim below was disk-verified 2026-07-06; re-verify in
  Recon, months may have passed.

## Recon (verify before any work)

Run all checks first; each replaces doc-trust. Grounded numbers are as-of 2026-07-06.

1. `launchctl list | grep appyradar` → expect exactly one line, label
   `com.appydave.appyradar-sentinal` (the 'a' spelling) with a live PID. If instead you see
   `com.appydave.appyradar-sentinel` (the 'e' spelling) → migration already happened in a race
   → **Abort A1**. If NEITHER is loaded → the collector is already stopped; note it, skip the
   bootout half of Move 8, and continue.
2. `ls /Users/davidcruwys/dev/ad/apps/appyradar-sentinal/snapshots/sentinel-latest.json` and
   check mtime is within ~1 hour (`stat -f '%Sm' <file>`) → confirms 'a' is genuinely
   collecting today. Stale by days → note it (weaker baseline, migration still valid).
3. `git -C /Users/davidcruwys/dev/ad/apps/appyradar-sentinel log --oneline | wc -l` → expect
   ~2 (±3) commits and `git status --porcelain` clean; `ls` shows NO `node_modules`, NO
   `sentinel.config.json`, NO `snapshots/`. If the repo has grown many commits or is already
   configured/running → someone built on it → **Abort A1**.
4. `grep -n 'appyradar-sentinel' /Users/davidcruwys/.claude.json | head -5` → expect a global
   `mcpServers.appyradar-sentinel` entry whose args path contains `appyradar-sentinal/src/
   access/bindings/mcp.ts` (the 'e'-NAMED server serving from the 'a' PATH — that mismatch is
   the bug). Confirm precisely:
   `python3 -c "import json; print(json.load(open('/Users/davidcruwys/.claude.json'))['mcpServers']['appyradar-sentinel']['args'])"`.
   If the key is absent, note it — Move 7's counter-move creates it fresh. If the file doesn't
   parse → **Abort A4**.
5. `npm view @appydave/appysentinel-core versions` → expect `0.1.0` present (lockfile pins
   0.1.0; `^0.1.0` will NOT accept 0.2.0). If 0.1.0 is gone from npm → **Fork F1** route B
   territory; treat as install failure.
6. `ls /Users/davidcruwys/.config/appydave/apps.json /Users/davidcruwys/.bun/bin/bun` → both
   exist (config value + plist binary path depend on them). Missing bun → find it with
   `which bun` and substitute that absolute path everywhere below.
7. `python3 -c "import json; d=json.load(open('/Users/davidcruwys/.config/appydave/locations.json')); locs=d['locations']; print(len(locs), any(e.get('key')=='appyradar-sentinel' for e in locs))"`
   → expect `134 False` (±15 on count). If `True` → already registered; skip that half of
   Move 10.
8. Consumer check for the MCP tools that 'e' does NOT carry ('a' has 13 tools incl.
   `pause_collection`, `resume_collection`, `trigger_collection`, `investigate_machine`,
   `add_machine`, `remove_machine`; 'e' has 9: the 7 read tools + `disk_archaeology` +
   `refresh`):
   `grep -rln 'pause_collection\|trigger_collection\|investigate_machine\|add_machine\|remove_machine' /Users/davidcruwys/dev/ad --include='*.md' --include='*.py' --include='*.ts' --include='*.js' --include='*.json' | grep -v 'appyradar-sentin\|node_modules'`
   → expect only `~/dev/ad/brains/cowork/cowork-live-artifact-spec.md` (a doc, not runtime).
   Any OTHER hit → **Fork F3**.

## Moves

1. **Install 'e' dependencies.**
   - **Do:** `cd /Users/davidcruwys/dev/ad/apps/appyradar-sentinel && bun install`
   - **Expect:** exit 0; `node_modules/@appydave/appysentinel-core/package.json` exists with
     `"version": "0.1.0"`.
   - **Failure signal:** non-zero exit; resolution errors for `@appydave/appysentinel-core`.
   - **Counter-move:** retry once (network). Second failure → **Abort A2** (do NOT vendor,
     link, or bump the dependency yourself).

2. **Typecheck + tests on 'e'.**
   - **Do:** `bun run typecheck && bun run test` in the 'e' repo.
   - **Expect:** both exit 0 (vitest suite passes).
   - **Failure signal:** compile errors or failing tests.
   - **Counter-move:** → **Fork F1**.

3. **Create the live config for 'e'.**
   - **Do:** `cp sentinel.config.example.json sentinel.config.json` in the 'e' repo, then set
     the real path:
     `python3 -c "import json,io; p='/Users/davidcruwys/dev/ad/apps/appyradar-sentinel/sentinel.config.json'; d=json.load(open(p)); d['appsJsonPath']='/Users/davidcruwys/.config/appydave/apps.json'; open(p,'w').write(json.dumps(d,indent=2)+'\n')"`
     Leave the 5 machines exactly as the example lists them (they match 'a''s live config
     verbatim: macbook-pro, mac-mini-m4, mac-mini-m2, jan, mary). Do NOT rename hosts for
     Roamy — that is T6-03.
   - **Expect:** `sentinel.config.json` parses; `appsJsonPath` = the davidcruwys path; 5
     machine entries.
   - **Failure signal:** JSON error, or example file missing.
   - **Counter-move:** if the example is missing, reconstruct config is a guess → **Abort A2**.

4. **Copy snapshot history 'a'→'e' (dated files only).**
   - **Do:** `mkdir -p /Users/davidcruwys/dev/ad/apps/appyradar-sentinel/snapshots && rsync -a --exclude 'sentinel-latest.json' /Users/davidcruwys/dev/ad/apps/appyradar-sentinal/snapshots/ /Users/davidcruwys/dev/ad/apps/appyradar-sentinel/snapshots/`
   - **Expect:** ~70 `sentinel-YYYY-MM-DD.json` files land in 'e' (`ls | wc -l`); NO
     `sentinel-latest.json` copied; 'a''s snapshots dir untouched.
   - **Failure signal:** rsync error / zero files.
   - **Counter-move:** history is nice-to-have, not load-bearing — on failure, skip, note it
     in the done summary, continue. (Old files may not match 'e''s zod schema; they are kept
     for archaeology, never re-parsed by the daemon — do not "fix" them.)

5. **Smoke-run the 'e' collector in the foreground.**
   - **Do:** from the 'e' repo:
     `timeout 150 bun src/main.ts; echo "exit=$?"` (timeout kill is the EXPECTED end state —
     boot pulse runs one full collection, then we cut it off).
   - **Expect:** within the 150s window, `snapshots/sentinel-latest.json` is (re)written with
     a fresh mtime and parses as JSON containing at least the self machine (mac-mini-m4).
     Offline fleet members producing SSH errors in the log output is NORMAL and fine.
   - **Failure signal:** process crashes at boot (module/config error), or 150s elapse with no
     `sentinel-latest.json` written at all.
   - **Counter-move:** → **Fork F2**.

6. **Smoke the 'e' MCP surface (stdio handshake).**
   - **Do:** from the 'e' repo run:
     ```
     python3 - <<'EOF'
     import subprocess, json, time
     p = subprocess.Popen(['bun','src/expose/mcp.ts'],
         cwd='/Users/davidcruwys/dev/ad/apps/appyradar-sentinel',
         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
     def send(m): p.stdin.write(json.dumps(m)+'\n'); p.stdin.flush()
     send({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"wg-t6-02","version":"0"}}})
     print('INIT:', p.stdout.readline()[:200])
     send({"jsonrpc":"2.0","method":"notifications/initialized"})
     send({"jsonrpc":"2.0","id":2,"method":"tools/list"})
     out = p.stdout.readline()
     print('TOOLS_OK:', 'fleet_status' in out and 'refresh' in out)
     p.terminate()
     EOF
     ```
   - **Expect:** `TOOLS_OK: True` (tools/list names include `fleet_status` and `refresh`).
   - **Failure signal:** hang (no line back), crash, or `TOOLS_OK: False`.
   - **Counter-move:** if it hangs, kill and retry once with a 15s read guard. If the
     handshake still won't complete BUT the server process starts and stays alive 5s with no
     module errors on stderr, accept as a weaker pass and record that in the done summary; if
     the server won't even boot → **Abort A2**.

7. **Cut the global MCP registration over to 'e'.**
   - **Do:** `claude mcp remove appyradar-sentinel -s user` then
     `claude mcp add appyradar-sentinel -s user -- bun /Users/davidcruwys/dev/ad/apps/appyradar-sentinel/src/expose/mcp.ts`
   - **Expect:** `claude mcp get appyradar-sentinel` shows the 'e' path
     (`.../appyradar-sentinel/src/expose/mcp.ts`); the grep from Recon 4 no longer matches the
     'a' path under that server name. (Change affects NEW sessions only; do NOT kill the
     already-spawned `bun .../appyradar-sentinal/src/access/bindings/mcp.ts` processes owned
     by other live Claude sessions.)
   - **Failure signal:** `claude mcp` subcommand errors, or `get` still shows the 'a' path.
   - **Counter-move:** fall back to a direct edit — back up first
     (`cp /Users/davidcruwys/.claude.json /Users/davidcruwys/.claude.json.bak-wg-t6-02`), then
     one quick python read-modify-write setting
     `mcpServers['appyradar-sentinel'] = {"type":"stdio","command":"bun","args":["/Users/davidcruwys/dev/ad/apps/appyradar-sentinel/src/expose/mcp.ts"],"env":{}}`
     (create the key if Recon 4 found it absent). Re-verify by grep; if the value reverts
     (another live session rewrote the file), retry once; still reverting → **Abort A4**.

8. **Cut the launchd daemon over to 'e'.**
   - **Do:** in order:
     1. `launchctl bootout gui/$(id -u)/com.appydave.appyradar-sentinal` (skip if Recon 1
        found nothing loaded; "No such process" output is equivalent to success here).
     2. `ps aux | grep 'appyradar-sentinal/src/main.ts' | grep -v grep` → must be empty.
     3. Archive the old plist INTO the legacy repo (picked up by Move 9's commit):
        `mkdir -p /Users/davidcruwys/dev/ad/apps/appyradar-sentinal/docs/retired-launchd && mv /Users/davidcruwys/Library/LaunchAgents/com.appydave.appyradar-sentinal.plist /Users/davidcruwys/dev/ad/apps/appyradar-sentinal/docs/retired-launchd/`
     4. `mkdir -p /Users/davidcruwys/dev/ad/apps/appyradar-sentinel/logs`
     5. Write `/Users/davidcruwys/Library/LaunchAgents/com.appydave.appyradar-sentinel.plist`
        — an exact copy of the retired plist's structure with every occurrence of
        `appyradar-sentinal` replaced by `appyradar-sentinel` (Label, ProgramArguments script
        path, WorkingDirectory, both log paths), keeping `/Users/davidcruwys/.bun/bin/bun run`
        + `RunAtLoad` + `KeepAlive` + the `HOME` env var.
     6. `launchctl bootstrap gui/$(id -u) /Users/davidcruwys/Library/LaunchAgents/com.appydave.appyradar-sentinel.plist`
   - **Expect:** `launchctl list | grep appyradar` shows exactly one entry,
     `com.appydave.appyradar-sentinel`, with a live PID; within ~10 min
     `/Users/davidcruwys/dev/ad/apps/appyradar-sentinel/snapshots/sentinel-latest.json` mtime
     refreshes (boot pulse); `logs/stdout.log` accumulating.
   - **Failure signal:** bootstrap error 5 (bad plist), no PID, daemon crash-looping
     (`logs/stderr.log` repeating boot errors).
   - **Counter-move:** `plutil -lint` the new plist and fix XML; one retry of
     bootout+bootstrap. If 'e' still won't stay up, ROLL BACK: bootout 'e', move the retired
     'a' plist back to `~/Library/LaunchAgents/`, bootstrap it, confirm the 'a' collector
     runs again, revert Move 7 (point MCP back at the 'a' path) → then **Abort A2** with the
     rollback recorded.

9. **Retire the 'a' repo in place (no deletion).**
   - **Do:** in order, in `/Users/davidcruwys/dev/ad/apps/appyradar-sentinal`:
     1. Secrets scan the dirty tree:
        `git status --porcelain | awk '{print $NF}' | grep -iE '\.env|secret|credential|token|pem|key$'`
        and `git diff | grep -cE 'sk-[A-Za-z0-9]{20}|AKIA[0-9A-Z]{16}|api[_-]?key.{0,4}[:=]'`
        → both must come back empty / `0`.
     2. Prepend to `README.md`:
        `> **RETIRED 2026-07-06** — superseded by `~/dev/ad/apps/appyradar-sentinel` ('e'). launchd + MCP + collection migrated (wg-t6-02). Kept for history; do not restart this daemon.`
     3. `git add -A && git commit -m "chore: retire appyradar-sentinal — collection migrated to appyradar-sentinel (wg-t6-02)"`
        (standard Co-Authored-By trailer), then `git push`.
   - **Expect:** scan empty; `git status --porcelain` empty after commit; push accepted by
     `github.com:appydave/appyradar-sentinal.git`.
   - **Failure signal:** scan hits (→ **Abort A3**); push rejected (auth/diverged remote).
   - **Counter-move:** on push rejection only: `git pull --rebase` once and re-push; if still
     failing, keep the local commit, note "push pending" in the done summary, continue —
     retirement is effective locally (daemon already stopped).

10. **Register 'e' + update the constellation doc, then commit dark-factory.**
    - **Do:**
      1. Back up: `cp /Users/davidcruwys/.config/appydave/locations.json /Users/davidcruwys/.config/appydave/locations.json.bak-wg-t6-02`.
      2. Append this entry to the `locations` list via a python json round-trip
         (`json.dumps(d, indent=2)`), inserted immediately after the entry with key
         `appysentinel`:
         ```json
         {
           "key": "appyradar-sentinel",
           "path": "/Users/davidcruwys/dev/ad/apps/appyradar-sentinel",
           "jump": "japp-radar-sentinel",
           "brand": "appydave",
           "type": "product",
           "tags": ["sentinel", "fleet", "collector", "mcp"],
           "description": "AppyRadar Sentinel - fleet collector daemon + MCP surface (re-scaffold; replaced retired appyradar-sentinal 2026-07-06)",
           "git_remote": "git@github.com:appydave/appyradar-sentinel.git"
         }
         ```
      3. In `/Users/davidcruwys/dev/ad/apps/dark-factory/docs/constellation-map.md`, update
         every row/line that `grep -n sentin` surfaces to the new truth: the 'e' row becomes
         the RUNNING collector (launchd `com.appydave.appyradar-sentinel`, migrated
         2026-07-06); the 'a' row becomes RETIRED 2026-07-06; the "Migrate the running
         sentinel" numbered step gets a "— DONE 2026-07-06 (wg-t6-02)" suffix.
      4. Commit + push dark-factory:
         `chore(constellation): sentinel a→e migration landed — map updated (wg-t6-02)`.
    - **Expect:** locations.json re-parses with count = Recon-7 count + 1 and the new key
      present; constellation-map.md greps show no line still calling 'a' RUNNING;
      dark-factory `git status` clean after push.
    - **Failure signal:** locations.json fails to parse after edit; constellation-map.md
      strings from 2026-07-06 no longer exist (doc rewritten since authoring).
    - **Counter-move:** locations.json breakage → restore from the .bak and retry once; a
      second parse failure → restore the .bak, skip registration, record it in the done
      summary. Constellation-map drift → make the smallest semantically-equivalent edits the
      current text allows; if the file is gone entirely, skip and note. Do NOT hand-edit
      `app-registry/store/registry.json` — its `probe.py` re-detects live status on its own.

## Forks

**F1 — 'e' tests fail (from Move 2).**
- **Trigger:** `bun run test` or `bun run typecheck` non-zero.
- **Route A (environmental):** failures ONLY in SSH/hostname-dependent tests (fleet members
  unreachable from this machine, e.g. `ssh/client` or collector integration cases) →
  re-run the pure-unit remainder (`bash-scripts`, `parsers`, `disk-usage` suites); if those
  pass, proceed with the failure list recorded in the done summary.
- **Route B (source defect):** compile errors or pure-unit failures → the re-scaffold itself
  is broken; do NOT start fixing its source (that's a different ticket) → **Abort A2**.

**F2 — smoke run produces a degraded snapshot (from Move 5).**
- **Trigger:** `sentinel-latest.json` was written but is thin, OR the run errored after
  partial collection.
- **Route A (partial fleet):** the snapshot parses and contains at least mac-mini-m4 (self) —
  offline peers are expected (Roamy blindness is a KNOWN pre-existing defect, T6-03) →
  proceed; the migration must not be blocked by fleet members being asleep.
- **Route B (no usable data):** snapshot missing, empty, or unparseable after a second
  attempt → the collector core doesn't work on this machine → **Abort A2** (leave 'a'
  running; nothing has been cut over yet at this move).

**F3 — a runtime consumer of the 6 command tools 'e' lacks (from Recon 8).**
- **Trigger:** the grep finds `pause_collection`/`trigger_collection`/`investigate_machine`/
  `add_machine`/`remove_machine` referenced in executable code (`.py`/`.ts`/`.js`) or an
  active skill outside the two sentinel repos — not just the known cowork spec doc.
- **Route A (doc/spec-only hit):** markdown that merely describes the surface → proceed;
  list the file(s) in the done summary so docs can catch up.
- **Route B (executable consumer):** something would break at cutover → **Abort A5** (the
  choice between porting the command tools to 'e' vs migrating the consumer is David's).

## Assumptions ledger

- **The 9-tool 'e' MCP surface is an acceptable replacement for the 13-tool 'a' surface**
  (`refresh` ≈ `trigger_collection`; pause/resume/add/remove/investigate go away; gains
  `disk_archaeology`). Plausible: authoring recon found zero runtime consumers of the removed
  six (only a cowork spec doc mentions them). If Recon 8 proves otherwise → F3/Abort A5.
- **Old dated snapshots need not parse under 'e''s schema.** Plausible: the daemon and MCP
  read only `sentinel-latest.json`; history is archaeology. If some future 'e' feature chokes
  on them, they can be deleted from 'e' — never edit them to fit.
- **`appyradar-sentinal-safe/` (the non-git backup copy) stays untouched.** Its deletion is
  David's call; flag it in the done summary as a follow-up candidate, do not act.
- **The 5-machine fleet list is still correct** (matches 'a''s live config verbatim as of
  2026-07-06). Host renames (Roamy) are T6-03's problem; if the executor finds the example
  config's machine list diverged from 'a''s live config, copy the LIVE 'a' values across and
  note the divergence — do not invent hosts.
- **`bun` lives at `/Users/davidcruwys/.bun/bin/bun`** (verified in the old plist + running
  processes). If Recon 6 finds it moved, substitute `which bun` output everywhere, including
  the new plist.

## Abort conditions

Park action for every abort: write
`engine/store/needs-decision/wg-t6-02-sentinel-migration.json` containing `{ticket, question,
evidence (commands + outputs), state_so_far (which moves completed, any rollback performed)}`;
leave the ticket in `running/`; never guess past an abort.

- **A1 — race/pre-emption:** Recon finds the migration already done ('e' daemon loaded, or
  'e' repo substantially built beyond ~2 commits). Question for David: "T6-02 appears already
  executed or in progress elsewhere — confirm state and close or re-scope."
- **A2 — the 'e' re-scaffold doesn't work** (install, boot, collection, or MCP boot fails
  beyond the counter-moves; includes F1-B and F2-B). If reached AFTER Move 8, perform the
  Move-8 rollback first so 'a' keeps collecting. Question: "Re-scaffold is not runnable —
  fix-forward in 'e', or keep 'a' as the collector for now?"
- **A3 — secrets in the legacy dirty tree** (Move 9 scan hits). Do NOT commit anything.
  Question: "appyradar-sentinal dirty tree contains candidate secrets at <paths> — scrub
  strategy before archive commit?"
- **A4 — `~/.claude.json` unmanageable** (unparseable, or the MCP edit keeps being reverted
  by concurrent sessions after retries). Question: "MCP registration for appyradar-sentinel
  contested/corrupt — safe window to edit?"
- **A5 — runtime consumer of removed MCP command tools found** (F3-B). Question: "Port
  pause/resume/trigger/add/remove/investigate to 'e', or migrate consumer <path>?"

## Verification

All from a fresh shell:

```bash
# 1. Daemon cutover — exactly one sentinel loaded, the 'e' one, with a PID
launchctl list | grep appyradar
# → single line: com.appydave.appyradar-sentinel, PID column numeric

# 2. Old collector fully stopped (session-spawned mcp.ts stdio servers may linger — allowed)
ps aux | grep 'appyradar-sentinal/src/main.ts' | grep -v grep   # → empty

# 3. 'e' is collecting — snapshot fresh (within 2× vital interval ≈ 10 min of a pulse)
stat -f '%Sm %N' /Users/davidcruwys/dev/ad/apps/appyradar-sentinel/snapshots/sentinel-latest.json
python3 -c "import json; d=json.load(open('/Users/davidcruwys/dev/ad/apps/appyradar-sentinel/snapshots/sentinel-latest.json')); print('parses OK')"

# 4. MCP registration points at 'e'
claude mcp get appyradar-sentinel | grep 'appyradar-sentinel/src/expose/mcp.ts'

# 5. Legacy retired: clean, pushed, banner present, old plist archived in-repo
git -C /Users/davidcruwys/dev/ad/apps/appyradar-sentinal status --porcelain   # → empty
head -1 /Users/davidcruwys/dev/ad/apps/appyradar-sentinal/README.md | grep RETIRED
ls /Users/davidcruwys/dev/ad/apps/appyradar-sentinal/docs/retired-launchd/com.appydave.appyradar-sentinal.plist

# 6. No 'a' plist left where launchd loads from
ls /Users/davidcruwys/Library/LaunchAgents/ | grep appyradar   # → only ...sentinel.plist ('e')

# 7. Registration + docs
python3 -c "import json; locs=json.load(open('/Users/davidcruwys/.config/appydave/locations.json'))['locations']; print(any(e['key']=='appyradar-sentinel' for e in locs))"   # → True
grep -c "RETIRED 2026-07-06" /Users/davidcruwys/dev/ad/apps/dark-factory/docs/constellation-map.md   # → ≥1

# NEGATIVE checks — what must NOT have changed
ls -d /Users/davidcruwys/dev/ad/apps/appyradar-sentinal /Users/davidcruwys/dev/ad/apps/appyradar-sentinal-safe   # both still exist
ls /Users/davidcruwys/dev/ad/apps/appyradar-sentinal/snapshots/ | wc -l   # ≥70 — history intact at source
grep -n 'supportsignal-sentinel' /Users/davidcruwys/.claude.json | head -1   # SS sentinel MCP untouched
```

Behaviour to demonstrate: a NEW interactive Claude session lists the `appyradar-sentinel`
MCP server with 9 tools including `refresh` and `disk_archaeology` (the executor cannot see
this from inside its own already-spawned session — verify via check 4 + Move 6's handshake
result instead, and say so in the done summary).

## Executor notes (sonnet)

- **Scope fence.** Do not touch: `appysentinel/` (the boilerplate — different app),
  `supportsignal-*sentinal*` (client world), `appyradar/` (the dashboard),
  `appyradar-sentinal-safe/` (backup copy — read-only), `app-registry/store/registry.json`
  (self-refreshing), `ad/CLAUDE.md` (AppyRadar already listed; the sentinel is its collector,
  not a new top-level app), and the blind-to-Roamy defect (T6-03).
- **Do not kill lingering `bun .../appyradar-sentinal/src/access/bindings/mcp.ts` processes**
  — each belongs to a live Claude session on this machine; they die with their sessions.
- **No source changes to 'e' beyond config + plist.** If 'e' needs code fixes to run, that's
  Abort A2, not a coding session.
- **HITL over guessing:** any secrets-scan ambiguity (Move 9) → A3; any doubt whether a Recon-8
  grep hit is "runtime" → treat as F3-B and abort A5. Cheap question > wrong cutover.
- **The rabbit hole:** reconciling the old snapshots' schema with 'e''s zod schema (70 files,
  two generations). Skip it entirely — copy them, never parse them, never migrate them.
