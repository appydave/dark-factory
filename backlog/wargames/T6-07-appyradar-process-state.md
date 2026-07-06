# T6-07 — AppyRadar owns tmux/process state

| field | value |
|---|---|
| ticket | wg-t6-07-appyradar-process-state |
| track / size / priority | T6 Constellation / M / normal |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

The reaper's stuck-case (hung Swagger, no handback) has no signal source: process-tree
detection is a proven dead end (claude reparents to its daemon), and the deferred design
question "who owns the process/tmux liveness signal — AngelEye or AppyRadar?" has sat open in
`docs/appyradar.md` §5.2/§6 since 2026-06-10. This ticket builds the AppyRadar half for real:
a `tmux` collector + parser + typed snapshot field in **appyradar-sentinel** (the canonical
'e' successor repo at `/Users/davidcruwys/dev/ad/apps/appyradar-sentinel` — NOT the running
'a' repo `appyradar-sentinal`), exposed two ways — a one-shot CLI (`bun src/expose/process-state.ts`)
and an MCP tool (`process_state`) — reporting tmux sessions/panes with activity ages,
`df-worker-*` engine workers flagged with their last pane lines, and the claude process list.
Done looks like: tests green, a live one-shot run against mac-mini-m4 shows a probe
`df-worker-99` session flagged as an engine worker, and dark-factory's `docs/appyradar.md`
records the resolution — AppyRadar owns the queryable process/tmux source (built); which
sensor(s) the reaper *consumes* stays T6-08's fork. Verified 2026-07-06: neither sentinel repo
has any tmux-state collection today (only a tmux *version* string in the tools collector).

## Locked context

- **Q4 (decisions.md):** everything through the engine — written for sonnet Swagger dispatch;
  self-report to `engine/store/results/` per the orchestrator's task prompt.
- **decisions.md assumptions ledger:** "Reaper stuck-case ownership (AngelEye vs AppyRadar)
  not asked → war-gamed as fork inside T6-08." This ticket builds AppyRadar's branch of that
  fork; it must NOT claim to decide what the reaper consumes.
- **docs/appyradar.md §4 (David, 2026-06-10):** "AppyRadar owns reading machine / process /
  tmux / machine observations, and making that data queryable." Sensors observe and answer;
  they never kill — the kill is Marshall's. This ticket is read-only observation, no actions.
- **docs/appyradar.md §5.1:** Switchboard's accreted process-polling (`ps -Ao …`, tmux,
  `pgrep claude`) "should migrate to AppyRadar — or Switchboard hosts it only until
  AppyRadar's Sentinel rebuild lands." This ticket IS that landing (build fresh in the
  sentinel; do NOT port Switchboard code).
- **Process-tree detection is a DEAD END** (`docs/watchtower/reaper-brief.md`, live-fire
  2026-06-06): never attempt pane-PID → claude-PID tree mapping. Report tmux state and the
  claude process list as two independent surfaces.
- **Q8 (decisions.md):** fleet = +Roamy, but Roamy liveness is a SEPARATE ticket
  (sentinel-blind-to-Roamy). This ticket configures self-machine collection only.
- **No `-p`/headless/SDK ever; interactive `claude` only** — binds how this ticket runs, not
  what it builds.
- **No standing service/cron without an explicit go:** do not install launchd, do not start
  an always-on daemon, do not register/edit MCP servers in `~/.claude.json`.

## Recon (verify before any work)

Docs lag code — trust nothing above until these pass. Two repos are involved:
`DF=/Users/davidcruwys/dev/ad/apps/dark-factory` (worker cwd) and
`SEN=/Users/davidcruwys/dev/ad/apps/appyradar-sentinel`. Use absolute paths for $SEN.

1. `ls $SEN/src/collectors/orchestrator.ts $SEN/src/collectors/bash-scripts.ts
   $SEN/src/collectors/parsers.ts $SEN/src/collect.ts $SEN/src/expose/mcp.ts $SEN/src/types.ts`
   → all six exist. Missing repo or missing files → **Abort A1**.
2. `grep -n "CONCERN_TO_COLLECTOR\|resolveCollectors\|export type Collector" $SEN/src/collectors/orchestrator.ts`
   → expect the `Collector` union (≈line 67), `CONCERN_TO_COLLECTOR` map (≈line 83), and
   `resolveCollectors()` (≈line 94). This is the extension seam. Renamed/gone → **Abort A1**.
3. `grep -rn "tmux" $SEN/src/ /Users/davidcruwys/dev/ad/apps/appyradar-sentinal/src/ | grep -v test | grep -v "_tool_version\|tmux:.*str\|tmux: string"`
   → expect NO hits (as of 2026-07-06 the only tmux references are tool-version plumbing). Any
   real tmux-state collector found → **Fork F3**.
4. `cd $SEN && git status --porcelain | head` → expect clean (2-commit scaffold:
   `104c191` initial, `4771401` docs). Pre-existing dirt → note it; a large diff touching
   `src/` → **Fork F3** (someone is mid-build).
5. `ls $SEN/node_modules 2>&1; ls $SEN/sentinel.config.json 2>&1` → expect BOTH missing
   ("No such file") — the 'e' repo has never been installed or run. Both are gitignored
   (`node_modules/`, `sentinel.config.json`, `snapshots/` all in `$SEN/.gitignore` — verified),
   so create them locally, never commit them.
6. Which repo is LIVE: `grep -n "appyradar" ~/.claude.json | grep -i "sentin" | head -5` and
   `launchctl list | grep -i "sentin"` → as of authoring, the registered MCP server named
   `appyradar-sentinel` points at the OLD 'a' repo
   (`/Users/davidcruwys/dev/ad/apps/appyradar-sentinal/src/access/bindings/mcp.ts`) and launchd
   runs `com.appydave.appyradar-sentinal`. Record which repo is live → drives **Fork F1**.
7. `ssh -o BatchMode=yes -o ConnectTimeout=3 mac-mini-m4 'echo SSH_OK'` → `SSH_OK` (verified
   2026-07-06 — the sentinel collects over SSH even for the local machine). Fails →
   counter-move: try `ssh localhost 'echo SSH_OK'`; if that also fails, `ssh-copy-id` to self
   is a one-time fix; if keys can't be provisioned → **Abort A3**.
8. `grep -n "df-worker" $DF/engine/warm_pool.py | head -3` → expect worker tmux sessions named
   `df-worker-<n>` (≈line 12 and `self.name = f"df-worker-{index}"` ≈line 64). This is the
   engine-worker naming contract the collector flags. Renamed → use the new pattern everywhere
   this war game says `df-worker`.
9. `sed -n '55,65p' $DF/docs/appyradar.md` → expect §5.2 still calling stuck-case ownership
   "an open design decision (deferred)". If a landed edit already assigns process/tmux state
   to something OTHER than AppyRadar → **Abort A2**.
10. `tmux -V` → expect tmux 3.x (3.6a at authoring; all format variables used below exist
    from tmux ≥2.1). Also `tmux ls 2>&1` — likely "no server running" (true at authoring);
    that's fine, Move 7 creates probe sessions.

## Moves

### Move 1 — Install and baseline the 'e' repo

- **Do:** `cd $SEN && bun install`, then `bun run typecheck` and `bun run test`.
- **Expect:** install resolves `@appydave/appysentinel-core@0.1.0` (it is lockfile-pinned with
  an integrity hash — a registry package, not a local link); typecheck exit 0; vitest suite
  fully green.
- **Failure signal:** install cannot resolve the `@appydave/*` packages, or the baseline suite
  is red before you changed anything.
- **Counter-move:** install failure → **Fork F2**. Pre-existing red tests → **Abort A3** (do
  not build on a broken base; that contradicts the "clean re-scaffold" premise).

### Move 2 — `tmuxStateScript()` in bash-scripts.ts

- **Do:** Append to `$SEN/src/collectors/bash-scripts.ts`, following the file's own design
  rules (returns a string, section markers `--- name ---`, `2>/dev/null`, PATH fallbacks —
  non-interactive SSH PATH lacks `/opt/homebrew/bin` where brew installs tmux):

  ```bash
  export PATH="$PATH:/opt/homebrew/bin:/usr/local/bin"
  echo "--- server ---"
  if tmux ls >/dev/null 2>&1; then echo "server_running:true"; else echo "server_running:false"; fi
  echo "--- sessions ---"
  tmux list-sessions -F '#{session_name}|#{session_created}|#{session_attached}|#{session_activity}|#{session_windows}' 2>/dev/null
  echo "--- panes ---"
  tmux list-panes -a -F '#{session_name}|#{window_index}|#{window_name}|#{pane_index}|#{pane_pid}|#{pane_current_command}|#{pane_current_path}' 2>/dev/null
  echo "--- worker_tails ---"
  for s in $(tmux list-sessions -F '#{session_name}' 2>/dev/null | grep -E '^df-worker-[0-9]+$'); do
    echo "tail_session:$s"
    tmux capture-pane -p -t "$s" 2>/dev/null | grep -v '^[[:space:]]*$' | tail -3 | sed 's/^/tail_line:/'
  done
  echo "--- claude_procs ---"
  ps -Ao pid,ppid,pcpu,pmem,etime,command 2>/dev/null | grep -i '[c]laude' | head -40
  ```

  (`session_created`/`session_activity` are unix epoch seconds; the `[c]laude` grep excludes
  the grep itself; capture-pane tails are df-worker-only by design — see Assumptions #4.)
- **Expect:** function exported; `bun run typecheck` still exit 0.
- **Failure signal:** —
- **Counter-move:** n/a (pure string template; failures surface in Moves 5/7).

### Move 3 — Types + parser

- **Do:** In `$SEN/src/types.ts` add `TmuxSessionInfo` (`name`, `created_at` ISO, `attached`
  boolean, `activity_at` ISO, `activity_age_seconds` number|null, `windows` number,
  `is_engine_worker` boolean — true iff name matches `^df-worker-\d+$`), `TmuxPaneInfo`
  (`session`, `window_index`, `window_name`, `pane_index`, `pane_pid`, `current_command`,
  `current_path`), `ClaudeProcInfo` (`pid`, `ppid`, `cpu_pct`, `mem_pct`, `etime`, `command`),
  and `TmuxStatePayload` (`server_running` boolean, `sessions[]`, `panes[]`, `worker_tails`
  Record<string, string[]>, `claude_processes[]`, `collected_at` ISO). Add optional
  `tmux?: TmuxStatePayload` to `MachineSnapshot` (≈line 194) and bump the `FleetSnapshot`
  `schema_version` literal `'1.3'` → `'1.4'` in BOTH `types.ts` (≈line 221) and `collect.ts`
  (the snapshot assembly, ≈line 237). In `$SEN/src/collectors/parsers.ts` add
  `parseTmux(raw: string): TmuxStatePayload`: split on the `--- name ---` section markers
  (same idiom the file already uses via its split helpers), pipe-split sessions/panes rows,
  compute `activity_age_seconds` from `session_activity` vs now (null if unparseable), parse
  `claude_procs` rows as 5 whitespace fields + remainder-as-command, and tolerate every
  malformed/missing line (skip, never throw — a sensor must degrade, not crash).
- **Expect:** `bun run typecheck` exit 0.
- **Failure signal:** typecheck errors in files you did NOT touch (schema-version literal is
  referenced somewhere this war game didn't list).
- **Counter-move:** `grep -rn "'1.3'" $SEN/src/` and update every literal; if the version is
  pinned OUTSIDE this repo's src (a consumer package), revert the bump to `'1.3'` and note the
  skipped bump in the results JSON — the optional field is additive either way.

### Move 4 — Wire the collector + config

- **Do:** In `$SEN/src/collectors/orchestrator.ts`: add `'tmux'` to the `Collector` union
  with a doc line (`tmux — tmux sessions/panes + claude procs (1 SSH). Cheap, high-volatility —
  the reaper's stuck-case source.`); add `tmux: 'tmux', process: 'tmux'` to
  `CONCERN_TO_COLLECTOR`; add `'tmux'` to `DEFAULT_COLLECTORS`; add a `want('tmux')` block in
  `collectMachine()` mirroring the `angeleye` block (`snapshot.tmux =
  parseTmux(track('tmux', sshScript(machine.host, tmuxStateScript())))` — then set
  `collected_at` from `new Date().toISOString()` if the parser doesn't). In `$SEN/src/collect.ts`
  add `tmux: 'tmux', process: 'tmux'` to `CONCERN_FIELD`. In
  `$SEN/sentinel.config.example.json` add `"tmux"` to the `vital` tier's `collect[]`. Create
  local (gitignored, per Recon 5) `$SEN/sentinel.config.json`:

  ```json
  {
    "machines": [{ "name": "mac-mini-m4", "host": "mac-mini-m4" }],
    "appsJsonPath": "/Users/davidcruwys/.config/appydave/apps.json",
    "pulses": { "vital": { "intervalMinutes": 5, "collect": ["system", "apps", "tmux"] } },
    "onDemand": ["git", "disk_archaeology"],
    "thresholds": {},
    "perMachine": {}
  }
  ```
- **Expect:** `bun run typecheck` exit 0.
- **Failure signal:** the substrate's config schema rejects the file at runtime (Move 7).
- **Counter-move:** `SentinelConfigSchema` in collect.ts is the authority — shape the file to
  it; second failure → **Abort A1**.

### Move 5 — Tests

- **Do:** Extend `$SEN/src/__tests__/bash-scripts.test.ts` (marker assertions: script contains
  `--- server ---`, `--- sessions ---`, `--- panes ---`, `--- worker_tails ---`,
  `--- claude_procs ---`, the `df-worker-[0-9]+` grep, the PATH fallback, and `2>/dev/null`).
  Add parser tests in the existing test dir with a literal fixture — at minimum: (a) a full
  raw sample with 2 sessions (one `df-worker-1`, one `main`), 2 panes, one worker tail of 2
  lines, one claude proc row → assert `server_running`, `is_engine_worker` true/false split,
  numeric `activity_age_seconds`, tail lines keyed by session, proc command containing spaces
  survives; (b) the empty case (`server_running:false`, no rows) → empty arrays, no throw;
  (c) a garbage line inside each section → skipped, no throw. Run `bun run test`.
- **Expect:** whole suite green (baseline count from Move 1 + your new tests).
- **Failure signal:** any red test.
- **Counter-move:** fix parser/script and re-run; same assertion red after two fix attempts →
  **Abort A3**.

### Move 6 — Expose: one-shot CLI + MCP tool

- **Do:** (a) Create `$SEN/src/expose/process-state.ts`: shebang `#!/usr/bin/env bun`; loads
  config via `createSentinelConfigLoader()`, runs
  `runFleetCollection({ config, concerns: ['tmux'], machines: argv[2] ? [argv[2]] : undefined })`
  (fresh collection — a kill decision must never rest on a stale snapshot), prints
  `{ generated_at, machines: [{ machine, status, tmux }] }` as pretty JSON to stdout, exit 0;
  exit 1 with a one-line error on config-load failure. Add package.json script
  `"process-state": "bun src/expose/process-state.ts"`. (b) In `$SEN/src/expose/mcp.ts`
  register tool `process_state` (schema: optional `machine` string, "Specific machine, or
  omit for all.") whose handler does the same fresh scoped collection and returns the same
  shape — mirroring how the existing on-demand tools call `runFleetCollection`; on collection
  throw, fall back to the latest snapshot's `tmux` fields with the standard `data_age_minutes`
  so the tool degrades instead of erroring.
- **Expect:** `bun run typecheck` exit 0; `bun run test` still green.
- **Failure signal:** mcp.ts's tool-registration shape differs from the ListTools/CallTool
  pattern read at authoring (≈lines 97–140).
- **Counter-move:** copy whatever pattern the file's OTHER on-demand tool (`refresh` or
  `disk_archaeology`) uses verbatim; if the whole MCP file was restructured → ship the CLI
  (the load-bearing surface), skip the MCP tool, and record the skip in the results JSON as a
  follow-up for the migration ticket.

### Move 7 — Live proof against mac-mini-m4

- **Do:** Create probe state, run the CLI, assert, clean up:

  ```bash
  tmux new-session -d -s df-worker-99 -x 120 -y 30   # fake engine worker
  tmux new-session -d -s wg-t6-07-plain              # non-worker control
  tmux send-keys -t df-worker-99 -l "echo probe-line-t6-07" ; tmux send-keys -t df-worker-99 Enter
  sleep 2
  cd $SEN && bun run process-state mac-mini-m4 > /tmp/t6-07-proof.json; echo "exit:$?"
  python3 - <<'PY'
  import json; d=json.load(open('/tmp/t6-07-proof.json'))
  m=[x for x in d['machines'] if x['machine']=='mac-mini-m4'][0]; t=m['tmux']
  assert t['server_running'] is True
  s={x['name']:x for x in t['sessions']}
  assert s['df-worker-99']['is_engine_worker'] is True
  assert s['wg-t6-07-plain']['is_engine_worker'] is False
  assert isinstance(s['df-worker-99']['activity_age_seconds'], (int,float))
  assert any('probe-line-t6-07' in l for l in t['worker_tails'].get('df-worker-99',[]))
  assert isinstance(t['claude_processes'], list)   # may be empty — presence not required
  print('T6-07 LIVE PROOF OK')
  PY
  tmux kill-session -t df-worker-99; tmux kill-session -t wg-t6-07-plain
  ```

  Then confirm the snapshot landed: `python3 -c "import json; s=json.load(open('$SEN/snapshots/sentinel-latest.json')); print(s['schema_version'], bool(s['machines'][0].get('tmux')))"`
  → `1.4 True` (or `1.3 True` if Move 3's counter-move reverted the bump). Optional MCP smoke
  test — attempt once, do not debug it: pipe an `initialize` + `tools/list` JSON-RPC pair into
  `bun run src/expose/mcp.ts` and grep the output for `process_state`; if stdio framing is
  fiddly, skip — the CLI proof above is the acceptance surface, note the skip in results.
- **Expect:** `exit:0`, `T6-07 LIVE PROOF OK`, snapshot check prints as above.
- **Failure signal:** empty `sessions` despite the probe existing (almost always SSH PATH —
  the remote shell can't find tmux), assertion error, or CLI exit 1.
- **Counter-move:** debug the SCRIPT first (run its raw text via
  `ssh mac-mini-m4 'bash -s' < <(bun -e 'import{tmuxStateScript}from"./src/collectors/bash-scripts.js";console.log(tmuxStateScript())')`
  and eyeball the sections), fix, re-run Move 5's tests, retry. ALWAYS kill both probe
  sessions before retrying or aborting (never leave fake df-worker sessions — the engine's
  own tooling greps that name). Two full failed retry cycles → **Abort A3**.

### Move 8 — Record the resolution, commit both repos, self-report

- **Do:** (a) In `$DF/docs/appyradar.md`: §5.2 — after the existing "ownership TBD" sentence,
  append: *"Update 2026-07-06 (wg-t6-07): the AppyRadar half is now BUILT — appyradar-sentinel
  collects tmux/process state (concern `tmux`) and answers via `bun run process-state` and the
  `process_state` MCP tool. AppyRadar owns the process/tmux source; AngelEye still owns
  session last-active; which signal(s) the reaper consumes remains the open fork (T6-08)."*
  §6 — reword the first bullet to *"Reaper stuck-case consumption — AngelEye vs AppyRadar vs
  both (see §5.2). AppyRadar's queryable source is built (wg-t6-07); the consumption choice is
  deferred to the reaper ticket."* Touch nothing else in the file. (b) Commit + push the
  sentinel repo: `cd $SEN && git add -A && git status --porcelain` — confirm ONLY `src/`,
  `sentinel.config.example.json`, `package.json` (and test files) are staged; gitignored
  config/snapshots/node_modules must not appear; commit
  `feat(collect): tmux/process-state collector + process_state surface (wg-t6-07)` with the
  standard Co-Authored-By trailer; push. (c) Commit + push dark-factory:
  `docs(appyradar): process/tmux source built in sentinel — ownership half resolved (wg-t6-07)`.
  (d) Write the worker self-report to `engine/store/results/<this-ticket-filename>.json` in
  the exact form the orchestrator's task prompt demands, listing both commit SHAs and any
  F/skip notes accumulated above.
- **Expect:** `git log --oneline -1` in each repo shows its commit; both pushes clean;
  `git status --porcelain` clean in both (apart from pre-existing dirt noted in Recon 4).
- **Failure signal:** push rejected (non-fast-forward), or a gitignored file staged.
- **Counter-move:** gitignored file staged → unstage it, re-check `.gitignore` intact. Push
  rejected → `git pull --rebase` then push; second failure → leave committed locally, note in
  results JSON `notes`.

## Forks

**F1 — Which sentinel repo is live at execution time.**
Trigger: Recon 6's `~/.claude.json` grep + `launchctl list`.
→ **Route A ('a' repo live — the authoring-time state):** build and verify entirely in 'e' via
one-shot runs (this war game as written). Do NOT touch the running 'a' service, its launchd
plist, or `~/.claude.json` — live exposure of the new tool arrives with the sibling
sentinal→sentinel migration ticket. State in the results JSON: "tool is repo-ready, not
live-registered; blocked on migration."
→ **Route B ('e' repo live — the migration already landed):** a real `sentinel.config.json`
and `snapshots/` will already exist. Do NOT create the Move 4 config; instead add `"tmux"` to
the LIVE config's `vital` tier, and after Move 7 also verify the always-on service picks it up
(wait one vital interval or use the service's refresh path; expect `tmux` in the next
`sentinel-latest.json`). The registered MCP server gains `process_state` on its next restart —
do not force-restart anything; note it.

**F2 — `@appydave/appysentinel-*` packages fail to install.**
Trigger: Move 1's `bun install` cannot resolve the substrate packages.
→ **Route A (transient/registry-auth):** retry once with default npm registry
(`npm_config_registry=https://registry.npmjs.org bun install`).
→ **Route B (packages genuinely unavailable):** the substrate monorepo exists locally at
`/Users/davidcruwys/dev/ad/apps/appysentinel/packages/` — point the two `@appydave/*` deps at
it via `file:` paths in package.json as a LOCAL-ONLY change: build proceeds, but **revert
package.json/bun.lock before the Move 8 commit** (commit must not carry the file: rewiring)
and record the registry problem in the results JSON. Both routes fail → **Abort A3**.

**F3 — A tmux/process collector already exists.**
Trigger: Recon 3 finds real tmux-state collection, or Recon 4 finds a mid-build diff.
→ **Route A (it landed in 'e' and works):** switch from build to verify+extend — run this war
game's Verification section against it; add ONLY what's missing (typically the CLI/MCP surface
or the `df-worker` flagging), then do Move 8 unchanged.
→ **Route B (it landed somewhere else — 'a' repo, Switchboard, or AngelEye):** do not build a
duplicate → **Abort A2** (ownership contradiction; David decides).

## Assumptions ledger

1. **The sentinal('a')→sentinel('e') migration is a sibling portfolio ticket whose id was
   unknown at authoring; assumed NOT landed.** Plausible: 'e' is a 2-commit scaffold with no
   install as of 2026-07-06. Fork F1 handles either state, so there is no hard depends_on. If
   the migration landed with a restructure that breaks the Recon 1/2 seams → Abort A1.
2. **Names are Fable's, not David's:** concern `tmux`, MCP tool `process_state`, CLI
   `process-state`, vital-tier (5 min) placement. Plausible per the repo's existing naming
   (`disk_archaeology`, `running_apps`) and the concern's high volatility. If David objects at
   triage/HITL: pure renames + a config edit, nothing structural — apply and continue.
3. **Resolving ownership "toward AppyRadar" means building the source there, not deciding the
   reaper's diet.** Grounded in the candidate brief + docs/appyradar.md §4's own charter. The
   consumption fork (AngelEye vs AppyRadar vs both) explicitly stays open for the reaper
   ticket (T6-08 per decisions.md). If executor-time context shows David expects THIS ticket
   to close the whole fork → park to needs-decision/ rather than guess his answer.
4. **df-worker-only pane tails are sufficient for the stuck heuristic.** The engine's own
   detector (orchestrator.py ≈line 93) greps captured pane text of its workers; nothing today
   needs tails of arbitrary sessions, and capturing every pane over SSH is noisy and slow. If
   the reaper ticket later needs more, widening the loop's grep is a one-line change — note,
   don't build.
5. **SSH-to-self stays the collection path** (no localhost fast-path special-casing), matching
   every existing collector. Verified working 2026-07-06. If SSH-to-self is broken at
   execution and unfixable → Abort A3, don't invent a non-SSH collector variant.

## Abort conditions

Park action for all aborts: write
`engine/store/needs-decision/wg-t6-07-appyradar-process-state.json` as
`{"ticket":"wg-t6-07-appyradar-process-state","question":"<one sentence>","proposed":"<one line>","note":"<what was observed, incl. paths>"}`,
leave the ticket in `running/`, kill any probe tmux sessions you created, and stop. Never
guess past an abort.

**A1 — Extension seam gone.** The 'e' repo is missing, or the
Collector/CONCERN_TO_COLLECTOR/collectMachine pattern no longer exists in recognizable form
(Recon 1/2), or the substrate's config schema rejects a conforming config twice (Move 4).
Question: "appyradar-sentinel's collector seam has changed since the T6-07 war game
(2026-07-06) — re-author against the new shape, or build elsewhere?"

**A2 — Ownership contradiction.** docs/appyradar.md (Recon 9) or a landed artifact (Fork F3
Route B) assigns process/tmux state to a home other than AppyRadar. Question: "T6-07 assumes
process/tmux state lands in appyradar-sentinel; found <observed> instead — proceed toward
AppyRadar or follow the new assignment?"

**A3 — Cannot build or cannot prove.** Dependencies unobtainable (F2 exhausted), baseline
tests red before any change (Move 1), the same test assertion red after two fix cycles
(Move 5), SSH-to-self unfixable (Recon 7 / Assumption 5), or two full live-proof retry cycles
fail (Move 7). Question: "T6-07 blocked at <move>: <symptom> — investigate infra or re-scope?"

## Verification

`SEN=/Users/davidcruwys/dev/ad/apps/appyradar-sentinel`, dark-factory as cwd:

```bash
cd $SEN && bun run typecheck                          # exit 0
cd $SEN && bun run test                               # exit 0, suite green incl. new tmux tests
grep -n "tmuxStateScript" $SEN/src/collectors/bash-scripts.ts   # exported
grep -n "tmux: 'tmux'" $SEN/src/collectors/orchestrator.ts      # concern wired
grep -n "process_state" $SEN/src/expose/mcp.ts                  # MCP tool registered
tmux new-session -d -s df-worker-99 && sleep 1 && \
  cd $SEN && bun run process-state mac-mini-m4 | \
  python3 -c "import json,sys; t=[m for m in json.load(sys.stdin)['machines'] if m['machine']=='mac-mini-m4'][0]['tmux']; assert any(s['name']=='df-worker-99' and s['is_engine_worker'] for s in t['sessions']); print('OK')" ; \
  tmux kill-session -t df-worker-99                   # prints OK
grep -n "wg-t6-07" /Users/davidcruwys/dev/ad/apps/dark-factory/docs/appyradar.md   # ≥2 hits (§5.2 + §6)
cd $SEN && git log --oneline -1 | grep "wg-t6-07"     # sentinel commit landed
cd /Users/davidcruwys/dev/ad/apps/dark-factory && git log --oneline -3 | grep "wg-t6-07"  # docs commit landed
ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/results/ | grep -c wg-t6-07   # 1 — self-report
```

Negative checks (what must NOT have changed):

```bash
tmux ls 2>&1 | grep -c "df-worker-99\|wg-t6-07"                    # 0 — probes cleaned up
grep -c "appyradar-sentinal/src/access" ~/.claude.json             # unchanged vs Recon 6 (MCP registration untouched)
launchctl list | grep -i sentin                                     # unchanged vs Recon 6
cd /Users/davidcruwys/dev/ad/apps/appyradar-sentinal && git status --porcelain | head   # 'a' repo: no NEW dirt vs Recon
git -C /Users/davidcruwys/dev/ad/apps/dark-factory diff --stat HEAD -- engine/          # empty — no engine code touched
git -C $SEN check-ignore sentinel.config.json snapshots/ node_modules/ >/dev/null && echo IGNORED-OK
```

## Executor notes (sonnet)

- **Scope fence:** create/edit ONLY `$SEN/src/**`, `$SEN/src/__tests__/**`,
  `$SEN/sentinel.config.example.json`, `$SEN/package.json`, local gitignored
  `sentinel.config.json`, and the two dark-factory files named in Move 8
  (`docs/appyradar.md`, the results self-report). Do NOT touch the 'a' repo
  (`appyradar-sentinal`), `~/.claude.json`, launchd, Switchboard, AngelEye, or any
  `engine/*.py`.
- **Read-only sensor, forever.** No kill, no restart, no cleanup actions in the collector or
  tools. If you find yourself adding a `kill_session` capability "while you're in there", you
  have left the war game — the kill is Marshall's (docs/appyradar.md §4).
- **No process-tree mapping.** Do not correlate pane PIDs to claude PIDs; report the two
  surfaces independently. This was live-fire-proven a dead end; rediscovering it is the #1
  time sink available here.
- **The rabbit hole:** the 'a' repo's richer MCP surface (investigate_machine,
  pause/resume_collection, add/remove_machine…) will tempt you to port it across, or to fix
  sentinel-blind-to-Roamy, or to install the 'e' service properly. All three are OTHER
  tickets. Build the tmux source, expose it twice, prove it once, stop.
- **Prefer HITL over guessing** on anything ownership-shaped (A2 territory) — a needs-decision
  park costs minutes; a duplicated or wrongly-homed sensor pollutes the constellation map.
