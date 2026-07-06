# T6-04 — AngelEye revival

| field | value |
|---|---|
| ticket | wg-t6-04-angeleye-revival |
| track / size / priority | T6 Constellation / M / normal |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Bring AngelEye (`~/dev/ad/apps/angeleye` — Claude Code session/work telemetry sentinel, dark
since ~2026-06-29) back to life as an always-on daemon with live hook ingestion against the
CURRENT Claude Code version. Concretely: **(a)** rebuild the stale workspaces and verify the
server's hook contract still stands; **(b)** daemonize via a launchd LaunchAgent
(`com.appydave.angeleye`, KeepAlive, production mode serving API + built client UI on :5051 —
"a Sentinel you have to remember to start isn't a Sentinel"); **(c)** re-install the Claude
Code hooks into `~/.claude/settings.json` from the server's own source-of-truth endpoint
(`GET /api/hooks/supported` `register` list — NEVER the stale 24-event install skill, which
still registers the worktree-breaking `WorktreeCreate`); **(d)** prove live ingestion with a
throwaway interactive-claude tmux probe; **(e)** force a resync of the ~980MB store and update
the stale install skill. Done means the daemon answers `/health` without anyone starting it,
a session started after install lands in AngelEye within seconds, and the two non-AngelEye
hooks in settings.json survive byte-for-byte. This unblocks T5-03's Fork F2-B (Watchtower's
AngelEye badge flips to alive) and is the prerequisite for usage telemetry (T7-06).

## Locked context

- **Q4 (decisions.md):** everything through the engine — written for sonnet Swagger dispatch,
  cwd = dark-factory repo root; AngelEye work is cross-repo by absolute path (T5-03/T2-05
  precedent).
- **No `-p`/headless/SDK ever; interactive `claude` only.** Move 7's probe is a plain
  interactive `claude` in a detached tmux session (the engine's own dispatch idiom) — never
  `claude -p`, never the Agent SDK.
- **Curl transport is the ratified hook transport.** HTTP-typed hooks were live-tested and
  REJECTED 2026-05-13 (SessionStart drops — `docs/architecture/hook-transport.md` in the
  AngelEye repo). Do not re-litigate this; install `type:"command"` curl hooks only.
- **`WorktreeCreate` must NEVER be registered as a hook.** It replaces git's worktree
  workflow — a passthrough curl hook feeds the response body in as the worktree path (ENOENT)
  and breaks background-isolated sessions. Verified 2026-05-19; hard-excluded in
  `hooks.ts` `HOOK_REGISTRATION_EXCLUSIONS`. This is the reason the old install skill is
  dangerous.
- **Don't touch working systems beyond the ask** (global preference): the two non-AngelEye
  hooks in `~/.claude/settings.json` (playwright-screenshot PostToolUse, buggered
  UserPromptSubmit) must be preserved untouched, and no process David started manually may be
  killed (→ Abort A2).
- **Complement, don't replace (Q9):** revival = refresh items 1+2 of
  `backlog/2026-06-06-angeleye-refresh.md`. The overlay (item 3), pruning (item 4), MCP
  surface (item 5), and Watchtower feed (item 6) are explicitly OUT of this ticket.
- **No YLO/POEM work.**

## Recon (verify before any work)

Docs lag code. Run every check. Roots: `DF=/Users/davidcruwys/dev/ad/apps/dark-factory`,
`AE=/Users/davidcruwys/dev/ad/apps/angeleye`, data home `~/.claude/angeleye`.

1. **AngelEye is dark and nothing owns :5051:** `lsof -nP -iTCP:5051 -sTCP:LISTEN` → authoring
   state: empty (and `curl -s -m 2 http://127.0.0.1:5051/health` fails). ANY listener found →
   **Abort A2** (don't kill it — David or another ticket owns it).
2. **Repo baseline:** `git -C $AE status --porcelain` → authoring state: three untracked
   strangers (`.claude/settings.json`, `docs/planning/worktree-hook-passthrough-fix.md`,
   `memory/`) and branch `main` at `cca1fc64`. Leave the strangers alone; stage only your
   files. Tracked-file dirt in files this ticket touches (`server/src/config/env.ts`,
   `.env.example`, anything under `scripts/`) → **Abort A5**.
3. **Hook contract still stands in source:** in `$AE/server/src/routes/hooks.ts` confirm
   (i) `EVENT_MAP` exists with 30 events (comment "v2.1.167 canonical reconcile"),
   (ii) `HOOK_REGISTRATION_EXCLUSIONS` hard-excludes `WorktreeCreate` (`optional: false`)
   and soft-excludes `MessageDisplay`, (iii) `router.get('/api/hooks/supported', …)` returns
   `{ events, count, register, excluded }`. All verified at authoring. Endpoint or exclusion
   gone → **Abort A1**.
4. **settings.json shape:** `python3 -c "import json; d=json.load(open('/Users/davidcruwys/.claude/settings.json')); print(list(d.get('hooks',{}).keys()))"`
   → authoring state: `['PostToolUse', 'UserPromptSubmit']`, both NON-AngelEye
   (`grep -c "localhost:5051" ~/.claude/settings.json` → `0`). Record the exact current
   content of both entries — they must survive verbatim. JSON parse failure → **Abort A3**.
5. **Data home + staleness:** `du -sh ~/.claude/angeleye` → ~980M at authoring;
   `ls -lt ~/.claude/angeleye/sessions | head -3` → newest 2026-06-29 (last time the server
   ran). Missing dir entirely is fine (server creates it) — just note it.
6. **Stale install skill is what recon says it is:**
   `grep -c "WorktreeCreate" ~/.claude/skills/angeleye-install/SKILL.md` → `1` (it registers
   it — the defect), and the skill lists 24 events (dated Mar 25, plain file, no symlink).
   Skill missing → skip Move 8's rewrite, note it, everything else proceeds.
7. **Version drift bounds:** `claude --version` → authoring: `2.1.201`; EVENT_MAP was
   reconciled at v2.1.167. Also confirm the brain pointer exists:
   `ls ~/dev/ad/brains/anthropic-claude/claude-code/hooks/configuration-reference.md`
   (reference, NOT authority — see Move 6's drift check).
8. **Daemon prerequisites:** `command -v node tmux jq` → `/opt/homebrew/bin/node` (v25.8.0),
   tmux + jq present at authoring; `claude` at `~/.local/bin/claude`. Use the ABSOLUTE node
   path you find in the plist. `ls ~/Library/LaunchAgents/ | grep angeleye` → authoring:
   nothing (label `com.appydave.angeleye` is free). An existing angeleye plist → adopt/replace
   it in Move 4 rather than duplicating, and say so in results.
9. **Workspace installs + stale builds:** `ls $AE/node_modules > /dev/null && echo ok` →
   installed at authoring. Dist dirs exist but are 3+ months stale (server Mar 15, client
   Mar 27). `npm install` needed and failing gets ONE fix cycle, then **Abort A4**.
10. **cwd contract (why the plist's WorkingDirectory matters):** confirm these three still
    resolve relative to `process.cwd()` = `server/`: `env.ts` line ~6
    (`dotenv.config({ path: path.resolve(process.cwd(), '../.env'), override: true })`),
    `workflow-type.service.ts` / `project-config.service.ts` (`process.cwd()/src/config/…`),
    `git-sync.service.ts` (`REPO_ROOT = process.cwd()/..`). All verified at authoring. If this
    idiom changed, re-derive the correct WorkingDirectory before Move 3 and note it.

## Moves

1. **Do:** Rebuild + baseline. `cd $AE && npm install && npm run build` (builds shared →
   server → client per root package.json), then baseline the gates:
   `npm run typecheck && npm test` — record pass/fail per workspace BEFORE touching anything.
   **Expect:** build exits 0; fresh `shared/dist`, `server/dist`, `client/dist` timestamps;
   gates ideally green.
   **Failure signal:** build fails, or tests red out of the box.
   **Counter-move:** build failure → one fix cycle (usual culprit: node version vs lockfile —
   do NOT switch node versions; `rm -rf node_modules && npm install` is the one allowed
   retry), second failure → **Abort A4**. Pre-existing red tests → **Fork F3** (revival is
   not a test-fixing campaign).

2. **Do:** NODE_ENV seam for the daemon. `$AE/.env` (machine-local, untracked) currently
   pins `NODE_ENV=development`, and `env.ts` uses dotenv `override: true`, so a
   launchd-supplied `NODE_ENV=production` would be clobbered. Remove (or comment out) the
   `NODE_ENV=development` line in `$AE/.env`; the zod schema defaults to `development`, so
   `npm run dev` behaviour is unchanged, while launchd's `NODE_ENV=production` now survives
   and switches on the production static-client serving in `server/src/index.ts`
   (`if (env.isProduction) { … express.static(clientDist) … }` — verified at authoring).
   Document the contract in `$AE/.env.example` with a comment: "leave NODE_ENV unset —
   dev defaults to development; the launchd daemon injects production".
   **Expect:** `cd $AE/server && node -e "process.env.NODE_ENV='production'; import('./dist/config/env.js').then(m=>console.log(m.env.NODE_ENV))"`
   prints `production` (run from `server/` so `../.env` resolves).
   **Failure signal:** prints `development` (something still overrides) or the import crashes.
   **Counter-move:** re-read `.env` for a duplicate NODE_ENV line and `env.ts` for drift from
   Recon 10. If a second attempt still can't get `production` through cleanly → **Fork F1
   Route B** (code seam) — do not ship a daemon that silently runs dev mode.

3. **Do:** Author the LaunchAgent. Write `$AE/scripts/launchd/com.appydave.angeleye.plist`
   (tracked in the repo — the machine copy is installed in Move 4), modelled on the working
   `com.appydave.app-registry.plist` pattern:
   - `Label` = `com.appydave.angeleye`
   - `ProgramArguments` = [`<absolute node path from Recon 8>`, `dist/index.js`]
   - `WorkingDirectory` = `/Users/davidcruwys/dev/ad/apps/angeleye/server` (the Recon 10
     contract: `../.env`, `src/config/…`, git-sync all hang off this)
   - `EnvironmentVariables`: `NODE_ENV=production`,
     `PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin` (git-sync shells out to `git`)
   - `KeepAlive` true, `RunAtLoad` true
   - `StandardOutPath`/`StandardErrorPath` →
     `/Users/davidcruwys/.claude/angeleye/logs/launchd.out.log` / `launchd.err.log`
     (create `~/.claude/angeleye/logs/` first — launchd won't mkdir).
   **Expect:** `plutil -lint $AE/scripts/launchd/com.appydave.angeleye.plist` → `OK`.
   **Failure signal:** plutil rejects the XML.
   **Counter-move:** fix the XML against the app-registry plist as the literal template;
   plutil must pass before Move 4 — no loading unlinted plists.

4. **Do:** Install + start the daemon. `mkdir -p ~/.claude/angeleye/logs`, copy the plist to
   `~/Library/LaunchAgents/com.appydave.angeleye.plist`, then
   `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.appydave.angeleye.plist`
   (if `bootstrap` reports it's already loaded, `launchctl bootout gui/$(id -u)/com.appydave.angeleye`
   first, then bootstrap again). Startup runs a backfill over ~980MB of data — give it time.
   **Expect:** within 120s, `curl -s http://127.0.0.1:5051/health` returns the
   `{"status":"ok",…}` envelope AND `curl -s http://127.0.0.1:5051/` returns the client
   index.html (production static serving proves NODE_ENV landed);
   `launchctl print gui/$(id -u)/com.appydave.angeleye | grep -m1 state` → `state = running`.
   **Failure signal:** no listener after 120s, or `launchd.err.log` shows a crash loop
   (repeated startup banners / "Invalid environment variables" / EADDRINUSE).
   **Counter-move:** read the err log — it names the layer. `Invalid environment variables`
   → Move 2 regressed; EADDRINUSE → someone grabbed :5051 since Recon 1 → **Abort A2**;
   module-not-found → Move 1's build is stale, rebuild. ONE fix cycle then re-bootstrap;
   a second crash loop → `launchctl bootout` (leave the machine clean) → **Abort A4**.
   UI serving dev-mode fallback (health ok, `/` 404s) → **Fork F1**.

5. **Do:** Re-install hooks from the server's source of truth. First back up:
   `cp ~/.claude/settings.json ~/.claude/settings.json.wg-t6-04.bak`. Then fetch
   `curl -s http://127.0.0.1:5051/api/hooks/supported` and use its `register` array (expect
   28 events = 30 − WorktreeCreate − MessageDisplay) — NOT the stale skill's 24-event list,
   NOT EVENT_MAP raw. Read-modify-write `~/.claude/settings.json` with a python3 script:
   for each register event, remove any existing entries whose command contains
   `localhost:5051`, then append
   `{"matcher": "", "hooks": [{"type": "command", "command": "curl -s -X POST -H 'Content-Type: application/json' -d @- http://localhost:5051/hooks/<EventName> || true"}]}`
   to that event's array. Never touch entries that don't contain `localhost:5051`; never
   create a `WorktreeCreate` key; preserve every other top-level settings key.
   **Expect:** `python3 -m json.tool ~/.claude/settings.json > /dev/null` exits 0;
   `grep -c "localhost:5051" ~/.claude/settings.json` → `28`;
   `grep -c "WorktreeCreate" ~/.claude/settings.json` → `0`; the buggered-detect and
   playwright-screenshot hook commands still present byte-for-byte (diff against Recon 4's
   record).
   **Failure signal:** any of those four checks off, or the script throws mid-write.
   **Counter-move:** `cp ~/.claude/settings.json.wg-t6-04.bak ~/.claude/settings.json`
   (restore FIRST, always), fix the script, retry once. Second failure → restore backup →
   **Abort A3**. A corrupted settings.json breaks every future session on this machine —
   the backup-restore step is non-negotiable.

6. **Do:** Version-drift check (the "compat" in the ticket title). Diff the server's
   `register`+`excluded` event names against what current Claude Code (Recon 7's version)
   actually fires: consult the official hooks docs (docs.claude.com — primary source) via
   WebFetch/WebSearch if network is available, with
   `~/dev/ad/brains/anthropic-claude/claude-code/hooks/configuration-reference.md` as the
   local pointer (reference, not authority). Classify: events Claude Code no longer fires
   (dead weight — harmless, note them) vs NEW events absent from `EVENT_MAP` (data gaps —
   list them). Do NOT extend EVENT_MAP or the server in this ticket; write findings into the
   results note and, if new events exist, add one line to
   `$AE/docs/architecture/hook-transport.md` §"When to revisit" naming them.
   **Expect:** a short written diff (possibly "no drift found"); no code changes.
   **Failure signal:** no network and the brain file is stale/ambiguous — the diff can't be
   grounded.
   **Counter-move:** degrade honestly: state "drift check deferred — no primary source
   reachable; Move 7's live probe plus the server's schema auditor (non-blocking, logs drift
   per event) are the operative compat evidence". Not abort-worthy.

7. **Do:** Live end-to-end proof with a throwaway interactive claude (hooks only bind to
   sessions started AFTER Move 5). Record the marker
   `BEFORE=$(ls ~/.claude/angeleye/sessions | wc -l)`, then
   `tmux new-session -d -s angeleye-wg-probe -c $DF '~/.local/bin/claude'` (interactive,
   trusted cwd, NEVER `-p`). Wait ~30s (SessionStart fires at startup, no prompt needed),
   then check a new `session-*.jsonl` appeared in `~/.claude/angeleye/sessions/` with mtime
   after Move 5, and `grep -l '"hook_event":"session_start"\|session_start' <that file>`
   (exact field name per what the file shows — read it). Then **mandatory cleanup, same
   move:** `tmux kill-session -t angeleye-wg-probe` and confirm
   `tmux ls 2>/dev/null | grep -c angeleye-wg-probe` → `0`.
   **Expect:** new session file appears within ~30s of the probe starting; probe session
   killed and gone.
   **Failure signal:** no new file after 60s.
   **Counter-move:** triage the pipe in order: (i) `tmux capture-pane -p -t angeleye-wg-probe`
   — is claude actually up (trust prompt? crash?); (ii)
   `curl -s -X POST -H 'Content-Type: application/json' -d '{"session_id":"wg-t6-04-synthetic","hook_event_name":"SessionStart","cwd":"'$DF'"}' http://127.0.0.1:5051/hooks/SessionStart`
   — server-side ingestion works? (iii) re-grep settings.json for the SessionStart entry.
   Fix the failing layer once and re-probe (kill the old probe first — never two probes).
   If the synthetic curl ingests but a real session still doesn't emit → **Fork F2** (record
   the degradation, don't spin). NEVER leave angeleye-wg-probe alive while debugging.

8. **Do:** Resync the stale store + fix the stale skill. (a)
   `curl -s -X POST 'http://127.0.0.1:5051/api/sync?force=true'` then poll
   `curl -s http://127.0.0.1:5051/api/sync/status` until it reports complete (980MB — allow
   minutes; poll, don't hammer: the scaffold rate-limiter is live). (b) Rewrite
   `~/.claude/skills/angeleye-install/SKILL.md` (machine file, Recon 6): the event list must
   be FETCHED live from `GET /api/hooks/supported` (`register` field) instead of hardcoded;
   keep the safety rules (identify AngelEye entries solely by `localhost:5051`, preserve
   other tools' hooks, idempotent); add a red warning that `WorktreeCreate` is never to be
   registered (breaks worktree creation — cite `docs/architecture/hook-transport.md`) and
   that the server must be running before install.
   **Expect:** sync status reaches its terminal/complete state; updated SKILL.md contains
   `api/hooks/supported` and a WorktreeCreate warning, and no longer contains a hardcoded
   24-event list.
   **Failure signal:** sync errors out, or status never terminates after 10 minutes.
   **Counter-move:** read `launchd.err.log` for the sync failure; one retry. Still failing →
   note "force-resync failed: <error>" in results and proceed — the resync is a data-refresh
   nicety, NOT the acceptance bar (live ingestion is). Skill rewrite has no failure mode
   worth a cycle; if the file is missing (Recon 6), skip with a note.

9. **Do:** Ship + close the loop. In `$AE`: stage ONLY your files
   (`scripts/launchd/com.appydave.angeleye.plist`, `.env.example`, any
   `docs/architecture/hook-transport.md` line from Move 6) — Recon 2's strangers stay
   untracked — commit
   `feat(daemon): launchd LaunchAgent + production serving — AngelEye revival (dark-factory wg-t6-04)`
   and `git push`. In `$DF`: append to `backlog/2026-06-06-angeleye-refresh.md` a `## Status
   2026-07-XX (wg-t6-04)` section stating items 1+2 are done (daemon label, hook count,
   probe result), items 3–6 still open; commit
   `chore(backlog): angeleye-refresh items 1+2 done via wg-t6-04` and push. Optionally run
   `python3 /Users/davidcruwys/dev/ad/apps/app-registry/probe.py` once so the app registry
   flips angeleye dark→running (it also runs itself every 30min — skip if it errors).
   **Expect:** both pushes succeed; `git -C $AE status --porcelain` shows only the Recon 2
   strangers.
   **Failure signal:** husky pre-commit rejects, or push rejected (remote ahead).
   **Counter-move:** lint/format fix then re-stage; `git pull --rebase` and re-push; a rebase
   conflict in a file you never touched → **Abort A5**.

## Forks

**F1 — Production mode won't switch on via .env line removal.**
Trigger: Move 2's expect prints `development` twice, or Move 4 health is ok but `/` doesn't
serve the client.
→ **Route A** (default, no trigger): the `.env` edit works — config-only, zero code change.
→ **Route B** (triggered): add a minimal code seam in `$AE/server/src/config/env.ts` — after
`dotenv.config(…)`, honour `process.env.ANGELEYE_ENV` (a key never present in `.env`, so
`override:true` can't clobber it) as the NODE_ENV source when set; plist sets
`ANGELEYE_ENV=production` instead. Extend `env.test.ts` additively; typecheck + server tests
must stay green; mention the seam in the commit body. Do NOT flip `override:true` to false —
that reintroduces the shell-PORT bug `scripts/start.sh` warns about.

**F2 — Server ingests synthetic events but a real session's hooks don't fire.**
Trigger: Move 7 counter-move step (ii) succeeds while a correctly-registered real probe still
produces nothing.
→ **Route A** (transient/environmental — probe's claude never fully started, trust prompt,
PATH): fix the probe environment and retry once; success → back on the happy path.
→ **Route B** (structural — Claude Code at the current version genuinely no longer fires
command hooks as configured): this is the real version-compat break the ticket exists for.
Do NOT patch guesswork into settings.json shapes. Park →
`$DF/engine/store/needs-decision/wg-t6-04-angeleye-revival.json` with the evidence trio
(settings.json entry, synthetic-curl 200, absent server log line) and the question "hook
config schema appears changed in CC <version> — investigate transport or pin?". The daemon,
resync, and skill-fix still count as delivered; say so in the park file.

**F3 — Pre-existing red tests at baseline.**
Trigger: Move 1's baseline `npm test`/`typecheck` fails before any edit.
→ **Route A** (green): full gates (`lint`, `typecheck`, `test`) must pass at Move 9.
→ **Route B** (red at baseline): do NOT fix unrelated tests (scope fence). Gate Move 9 on
"not worse": the workspaces/files you touched typecheck clean and any test file adjacent to
your edits passes; name the pre-existing failures in the commit body and results note.

## Assumptions ledger

1. **Production static serving is the right daemon mode** (UI + API on :5051, one process).
   Plausible: `index.ts` ships the `isProduction` static+SPA block for exactly this, and the
   client build bakes `VITE_SOCKET_URL=http://localhost:5051`. If David objects at triage
   (wants dev-mode daemon + on-demand Vite), the plist's env var flips — one-line change, no
   park needed.
2. **`GET /api/hooks/supported` `register` = 28 events** (30 − 2 exclusions, counted in
   source at authoring). If the live endpoint returns a different count, TRUST THE ENDPOINT
   (it is the source of truth by design) and adjust Move 5's `grep -c` expectation to
   `length(register)`; note the delta.
3. **A session file in `~/.claude/angeleye/sessions/` is the observable proof of ingestion.**
   Plausible: `sessions.service.ts` writes `session-<id>.jsonl` per event at authoring. If
   storage moved, fall back to `launchd.out.log` request lines (`POST /hooks/SessionStart`
   200) as the proof; either observation satisfies Move 7.
4. **Spawning ONE short-lived interactive `claude` in tmux is permitted.** Plausible: it is
   the engine's own dispatch mechanism (interactive-only rule bans `-p`/headless/SDK, not
   interactive tmux sessions), and the probe does no work — starts, fires SessionStart, dies.
   If the operator regards even this as engine-only privilege: run Move 7 through synthetic
   curl only and mark the live proof "deferred to David's next real session" in results —
   degradation, not park.
5. **The stale machine skill (`~/.claude/skills/angeleye-install/`) is this machine's only
   install skill copy** — no repo-tracked or plugin twin found at authoring (searched
   angeleye repo and plugins). If a twin surfaces, update it identically and name both in
   results.
6. **Free-standing park files in `engine/store/needs-decision/` are inert to the engine** —
   same contract as the rest of the portfolio (T2-05 authoring recon).
7. **Last-run evidence (data written 2026-06-29 with no hooks in settings.json at authoring)
   means someone ran the server manually since the hooks were removed.** Immaterial to the
   moves; recorded so the executor isn't confused by "fresh-ish" data in a dark app.

## Abort conditions

Every abort: write the park file, leave the ticket in `running/`, stop — never guess past it.

- **A1 — hook contract drifted in source.** Recon 3 fails: `/api/hooks/supported` gone,
  `WorktreeCreate` no longer excluded, or `EVENT_MAP` unrecognizable. Park
  `$DF/engine/store/needs-decision/wg-t6-04-angeleye-revival.json`:
  `{"ticket":"wg-t6-04-angeleye-revival","question":"AngelEye's hooks.ts no longer matches the authored contract (source-of-truth endpoint / WorktreeCreate exclusion) — was there an intervening refactor? Safe hook-install path unclear.","observed":"<grep output>","requested_by":"wg-t6-04 executor"}`.
- **A2 — :5051 is owned.** Recon 1 (or Move 4's EADDRINUSE) finds a listener. Never kill it
  (David's manual process or an unknown tenant). Park with `lsof` output and the question
  "manual AngelEye instance or port squatter — replace with daemon, or move the daemon?".
- **A3 — settings.json cannot be edited safely.** Recon 4 parse failure, or Move 5 failing
  twice. Restore `~/.claude/settings.json.wg-t6-04.bak` FIRST, verify
  `python3 -m json.tool` passes on the restored file, then park with the diff that failed.
  Machine-wide session config outranks this ticket.
- **A4 — cannot obtain a healthy daemon.** Move 1's build broken after the one retry, or
  Move 4 crash-looping after one fix cycle. `launchctl bootout gui/$(id -u)/com.appydave.angeleye`
  and remove the LaunchAgents copy (leave the machine as found), park with the last 30 lines
  of `launchd.err.log`. Do NOT brew-install anything or switch node versions.
- **A5 — seam conflict.** Recon 2 tracked-dirt in files this ticket touches, or a Move 9
  rebase conflict in a file you never edited. Park with `git status` and "who owns this seam
  right now?".

## Verification

`DF=/Users/davidcruwys/dev/ad/apps/dark-factory`, `AE=/Users/davidcruwys/dev/ad/apps/angeleye`.

```bash
# 1. Daemon is alive, launchd-owned, in production mode
launchctl print gui/$(id -u)/com.appydave.angeleye | grep -m1 "state" # → state = running
curl -s http://127.0.0.1:5051/health | jq -r .status                  # → ok
curl -s http://127.0.0.1:5051/ | grep -ci "<title>"                   # → 1 (client served ⇒ production mode)
plutil -lint $AE/scripts/launchd/com.appydave.angeleye.plist          # → OK (tracked copy)

# 2. Hooks installed from the source of truth, dangerous event absent, strangers preserved
python3 - <<'EOF'
import json, subprocess, urllib.request
reg = json.load(urllib.request.urlopen('http://127.0.0.1:5051/api/hooks/supported'))['register']
s   = json.load(open('/Users/davidcruwys/.claude/settings.json'))
hooks = s['hooks']
wired = [e for e in reg if any('localhost:5051' in h['command']
         for grp in hooks.get(e, []) for h in grp.get('hooks', []))]
assert sorted(wired) == sorted(reg), f"missing: {set(reg)-set(wired)}"
assert 'WorktreeCreate' not in hooks, "FATAL: WorktreeCreate registered"
buggered = any('buggered-detect' in h.get('command','')
               for grp in hooks['UserPromptSubmit'] for h in grp.get('hooks', []))
screenshot = any('browser_take_screenshot' == grp.get('matcher')
                 for grp in hooks['PostToolUse'])
assert buggered and screenshot, "non-AngelEye hooks lost"
print(f"hooks-ok: {len(wired)} wired, WorktreeCreate absent, strangers intact")
EOF

# 3. Live ingestion round trip (re-runnable; interactive claude, never -p) — WITH cleanup
BEFORE=$(ls ~/.claude/angeleye/sessions | wc -l)
tmux new-session -d -s angeleye-wg-probe -c $DF '~/.local/bin/claude'
sleep 30
AFTER=$(ls ~/.claude/angeleye/sessions | wc -l)
tmux kill-session -t angeleye-wg-probe
[ "$AFTER" -gt "$BEFORE" ] && echo live-ingestion-ok || echo "PROBE-FAIL (see Fork F2)"
tmux ls 2>/dev/null | grep -c angeleye-wg-probe                       # → 0 (nothing left behind)

# 4. Install skill fixed (skip if Recon 6 found it missing)
grep -c "api/hooks/supported" ~/.claude/skills/angeleye-install/SKILL.md  # → ≥1
grep -ci "never.*WorktreeCreate\|WorktreeCreate.*never" ~/.claude/skills/angeleye-install/SKILL.md # → ≥1

# 5. Shipped
git -C $AE log --oneline -1        # the feat(daemon) commit, pushed
grep -c "wg-t6-04" $DF/backlog/2026-06-06-angeleye-refresh.md         # → ≥1 (status appended)

# 6. Negative checks — what must NOT have changed
python3 -m json.tool ~/.claude/settings.json > /dev/null && echo settings-valid
grep "^PORT=" $AE/.env                                                # → PORT=5051 (untouched)
git -C $AE status --porcelain | grep -v "^??" | wc -l                 # → 0 (only Recon-2 strangers remain)
git -C $DF status --porcelain | grep -v "needs-decision" | wc -l      # → 0 (DF clean post-commit)
tmux ls 2>/dev/null | grep -c "df-worker"                             # → 0 unchanged (engine pool untouched)
ls ~/.claude/settings.json.wg-t6-04.bak                               # backup exists (keep it — David deletes)
```

## Executor notes (sonnet)

- **Scope fence.** Items 3–6 of the refresh backlog are OUT: no dark-factory classification
  overlay, no pruning of the 980MB store, no MCP surface, no Watchtower feed. No engine
  (`$DF/engine/*.py`) edits, no `engine/store/` writes (park files excepted), no Watchtower
  repo edits (its F2-B route reacts to you by itself), no locations.json/app-registry schema
  work (one optional `probe.py` run only). Do not "fix" AngelEye client UI issues you notice
  while verifying — note them.
- **The rabbit hole: extending hook coverage.** Move 6 WILL likely find events Claude Code
  2.1.201 fires that EVENT_MAP lacks. Adding them means server code + schema + tests — a
  different ticket. List them, add the one doc line, walk away.
- **Second rabbit hole: the 980MB store.** Backfill slowness, oversized registry.json
  (24MB), pruning ideas — all noted-not-built (refresh item 4). If the resync is slow, let
  it run; if it fails, report and move on.
- **settings.json is machine-blast-radius.** Backup before writing, restore-first on any
  failure, read-modify-write in one quick script (other sessions write this file too). The
  two non-AngelEye hooks surviving verbatim is as important as the 28 new ones landing.
- **WorktreeCreate is the one non-negotiable.** If ANY list you consume proposes registering
  it, the list is wrong — the `register` field from a healthy server never includes it
  (Recon 3 gates this). A registered WorktreeCreate breaks every future worktree on this
  machine.
- **Prefer parking over guessing** on port ownership (A2), settings-edit failures (A3), and
  structural hook-firing breaks (F2-B). A daemon that runs + hooks that fire is the bar;
  everything else in this ticket degrades gracefully and says so in results.
