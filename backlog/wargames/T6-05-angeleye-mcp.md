# T6-05 — AngelEye MCP wrapper

| field | value |
|---|---|
| ticket | wg-t6-05-angeleye-mcp |
| track / size / priority | T6 Constellation / S / normal |
| executor | sonnet Swagger via engine |
| depends_on | none hard (soft: a bootable AngelEye server — see Abort A2, which points at T6-04) |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

AngelEye (`/Users/davidcruwys/dev/ad/apps/angeleye`, Express API on :5051) has a rich read
API and no MCP surface — it is the first retrofit under the every-app-exposes-both
(API + MCP) doctrine (path-map.md T6). Build a **thin read-only stdio MCP server** at
`server/src/expose/mcp.ts` that proxies the existing HTTP API (never re-implements its
logic), register it user-scope as `angeleye` via the `claude mcp` CLI, and prove it at the
JSON-RPC protocol level. Done looks like: the file exists and typechecks, a piped
initialize→tools/list→tools/call handshake returns real session data, `claude mcp get
angeleye` shows the registration, the surface is documented in the AngelEye repo, and
everything is committed and pushed in the AngelEye repo with a self-report in this repo's
`engine/store/results/`.

## Locked context

- **Q4 (decisions.md):** everything through the engine — written for sonnet Swagger
  dispatch; self-report to `engine/store/results/` per the orchestrator's task prompt.
- **Ticket-first standing rule (`engine/store/queue/.CONVENTION.md`):** the ticket's
  queue/running/done movement + `results/<ticket>.json` is the audit trail.
- **No `-p`/headless/SDK-metered ever; interactive `claude` only** — binds how this ticket
  runs, not what it builds (the `@modelcontextprotocol/sdk` npm package is a library, not
  the metered Agent SDK — it is fine).
- **T6 doctrine seed (path-map.md):** "every-app-exposes-API+MCP doctrine sweep" — this
  ticket is the first single-app retrofit; the constellation-wide sweep is T6-14, NOT this
  ticket.
- **Adjacent tickets are fenced off:** sentinel 'a'→'e' migration is T6-02; AngelEye
  revival (hook compat, daemonize) is T6-04; port-drift doc fix (:5501 vs :5051 in
  AngelEye's CLAUDE.md) is T6-06. Touch none of that here.

## Recon (verify before any work)

Docs lag code — trust nothing above until these pass. Two repos are involved:
`DF=/Users/davidcruwys/dev/ad/apps/dark-factory` (this repo, self-report only) and
`AE=/Users/davidcruwys/dev/ad/apps/angeleye` (where all code lands). Use absolute paths;
your cwd resets between bash calls.

1. `ls $AE/server/src/routes/` → expect `sessions.ts health.ts projects.ts diagnostics.ts
   stats.ts hooks.ts ...` (verified 2026-07-06). Missing dir or a fundamentally different
   layout → **Abort A1**.
2. `grep '^PORT=' $AE/.env` → expect `PORT=5051` (verified 2026-07-06; AngelEye's own
   CLAUDE.md says 5500/5501 — that is the KNOWN doc drift, T6-06's job, do not fix it).
   No `.env` → `cp $AE/.env.example $AE/.env` won't have the right ports; **Abort A1**
   instead (the app's runtime identity is ambiguous). If PORT is some other value, use that
   value everywhere this war game says 5051 and note the drift in the results JSON.
3. `lsof -i :5051 2>/dev/null | grep LISTEN` → either a `node` listener (server already
   up → **Fork F1 Route A**) or nothing (→ **Fork F1 Route B**). Record which for Move 6's
   negative check.
4. `ls $AE/server/src/expose/ 2>&1` → expect "No such file or directory", AND
   `grep -r modelcontextprotocol $AE/package.json $AE/server/package.json` → expect no
   match (verified 2026-07-06: AngelEye has zero MCP code and no SDK dep). If either
   exists, someone got here first → **Abort A3**.
5. `claude mcp list 2>&1 | head -20` → expect a working list (e.g. `appyradar-sentinel`,
   `playwright`, …) and NO `angeleye` entry. `angeleye` already present → **Abort A3**.
   Command itself errors → note it; you will hit **Fork F3** at Move 5.
6. Reference implementation: `sed -n '88,180p'
   /Users/davidcruwys/dev/ad/apps/appyradar-sentinel/src/expose/mcp.ts` → expect the
   sentinel MCP pattern (SDK `Server` + `StdioServerTransport` +
   `ListToolsRequestSchema`/`CallToolRequestSchema` handlers). If the file is gone, proceed
   anyway — Move 3 specifies everything you need inline. ⚠️ The *registered* sentinel in
   `~/.claude.json` points at the LEGACY repo (`appyradar-sentinal/src/access/bindings/mcp.ts`
   — 'a' spelling); that is T6-02's mess. Read-only precedent; never edit it.
7. Toolchain: `command -v overmind; command -v claude; ls $AE/node_modules/.bin/tsx` → all
   three resolve (verified 2026-07-06: `/opt/homebrew/bin/overmind`,
   `~/.local/bin/claude`, repo-local tsx). tsx missing → `npm install` in `$AE` first;
   still missing → **Abort A1**.
8. Baseline: `git -C $AE status --porcelain | head -20` → note pre-existing dirt (this repo
   is often dirty — e.g. `x.md`, `UPGRADE_TODO.md`) so Move 6 commits only files this
   ticket created. Also `cp ~/.claude.json /tmp/t6-05-claude-json.bak` — insurance for
   Fork F3 Route B, taken now while nothing is modified.

## Moves

### Move 1 — Bring the API up and pin the tool surface with curl

- **Do:** Resolve **Fork F1** (server up vs down) so :5051 answers. Then curl-pin every
  endpoint the MCP will wrap (this replaces doc-trust with observed truth):
  ```bash
  curl -sf http://localhost:5051/health                                    # 1
  curl -sf "http://localhost:5051/api/sessions?limit=2"                    # 2
  curl -sf "http://localhost:5051/api/search?q=swagger&limit=2"            # 3
  SID=$(curl -s "http://localhost:5051/api/sessions?limit=1" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['sessions'][0]['session_id'])")
  curl -sf "http://localhost:5051/api/sessions/$SID/events"                # 4
  curl -sf "http://localhost:5051/api/sessions/$SID/enrichments"           # 5
  curl -sf http://localhost:5051/api/projects                              # 6
  curl -sf http://localhost:5051/api/diagnostics                           # 7
  ```
  Endpoints 1–6 are verified in source (2026-07-06: `health.ts:7`, `sessions.ts:100`,
  `sessions.ts:147`, `sessions.ts:289`, `sessions.ts:299`, `projects.ts:10`). Endpoint 7's
  router is mounted at `/api/diagnostics` (`index.ts:87`) but its internal path was not
  source-verified — if it 404s, try `curl -sf http://localhost:5051/api/diagnostics/` and
  `grep -n "router.get" $AE/server/src/routes/diagnostics.ts` to find the real path.
- **Expect:** endpoints 1–6 return HTTP 200 with a JSON body shaped
  `{"success":true,"data":...}` (or `{"status":"ok"...}` for /health); 7 resolves to
  SOME working path. The `$SID` extraction yields a UUID-ish id (the registry has weeks of
  real session data).
- **Failure signal:** 1 or 2 fail (the core surface is gone), or the sessions list is empty
  so `$SID` extraction dies.
- **Counter-move:** /health or /api/sessions failing → **Abort A1**. Empty sessions list →
  keep tools 1/2/3/6/7, mark the two per-session tools as wired-but-unproven in the results
  JSON, and skip their tools/call checks in Move 4. Any OTHER single endpoint 404s after
  the grep hunt → drop that one tool from the surface, note it, continue (**Fork F2**).

### Move 2 — Install the MCP SDK into the server workspace

- **Do:** `cd $AE && npm install @modelcontextprotocol/sdk --workspace server`
- **Expect:** exit 0; `grep modelcontextprotocol $AE/server/package.json` shows the dep;
  `ls $AE/node_modules/@modelcontextprotocol/sdk` exists. If the dev server is running
  under nodemon, it may restart once — harmless.
- **Failure signal:** npm errors (peer conflicts, network, workspace flag rejected).
- **Counter-move:** retry as `cd $AE/server && npm install @modelcontextprotocol/sdk`. If
  npm cannot install at all (offline/registry down) → stop and leave the ticket in
  running/ with a `## Status` note; this is transient, not a decision — do NOT park to
  needs-decision for a network blip.

### Move 3 — Write `server/src/expose/mcp.ts` (thin read-only HTTP proxy)

- **Do:** Create `$AE/server/src/expose/mcp.ts`. Contract (each row = one MCP tool; drop
  rows Move 1 eliminated):

  | tool | inputSchema properties | proxies |
  |---|---|---|
  | `health` | — | `GET /health` |
  | `sessions` | `limit` (number, default 20, server clamps 1–200), `project` (string), `kind` (string), `since` (string ISO) — all optional | `GET /api/sessions?...` |
  | `search` | `q` (string, REQUIRED — regex), `fields` (string, optional csv), `limit` (number, optional, server clamps 1–100) | `GET /api/search?...` |
  | `session_events` | `session_id` (string, REQUIRED) | `GET /api/sessions/:id/events` |
  | `session_enrichments` | `session_id` (string, REQUIRED) | `GET /api/sessions/:id/enrichments` |
  | `projects` | — | `GET /api/projects` |
  | `diagnostics` | — | Move 1's verified diagnostics path |

  Implementation constraints (all load-bearing):
  - Follow the sentinel pattern from Recon 6: `Server` + `StdioServerTransport`,
    `ListToolsRequestSchema` / `CallToolRequestSchema` handlers, every result returned as
    `{ content: [{ type: 'text', text: JSON.stringify(v, null, 2) }] }`. Server identity:
    `{ name: 'angeleye', version: '0.1.0' }`, capabilities `{ tools: {} }`.
  - **Base URL resolution:** `process.env.ANGELEYE_MCP_BASE_URL` if set; else read `PORT`
    from the repo's `.env` resolved OFF THE MODULE PATH (sentinel precedent:
    `dirname(fileURLToPath(import.meta.url))` then `../../..` to repo root — the process
    can be launched from any cwd), falling back to `5051`. Use Node's global `fetch`.
  - **Graceful-down:** wrap every fetch; on connection failure return (as tool text, not a
    thrown error) `{ error: "AngelEye server not reachable at <baseUrl>. Start it: cd
    /Users/davidcruwys/dev/ad/apps/angeleye && ./scripts/start.sh" }`.
  - **stdout is protocol-only.** No `console.log`, no pino, no banner — anything diagnostic
    goes to `console.error` (stderr). One stray stdout byte corrupts the MCP stream.
  - Read-only: no POST endpoints wrapped, ever (backfill/registry/sync POSTs exist —
    excluded by design, see Assumptions #1).
  - Standalone module: import ONLY from `@modelcontextprotocol/sdk` and `node:` builtins —
    no imports from the rest of the server codebase (keeps the wrapper decoupled from the
    Express app's lifecycle and avoids pino/env side effects).
- **Expect:** `cd $AE && npm run typecheck -w server` exits 0, and
  `npm run build -w server` exits 0 (the file compiles into the normal build).
- **Failure signal:** type errors from SDK import paths (the SDK's deep-import style is
  `@modelcontextprotocol/sdk/server/index.js` — note the `.js` suffixes, required under
  ESM), or nodemon crash-looping because the express server accidentally imports the new
  file.
- **Counter-move:** fix import suffixes per the sentinel file (Recon 6 shows the exact
  working import lines). If typecheck still fails after two attempts on SDK typing issues,
  pin the SDK to the major version the sentinel repo uses
  (`grep modelcontextprotocol /Users/davidcruwys/dev/ad/apps/appyradar-sentinel/package.json`)
  and retry; still failing → **Abort A2** is wrong here (server boots fine) — leave in
  running/ with a `## Status` note describing the compile error. Never ship a non-compiling
  file.

### Move 4 — Prove it at the JSON-RPC protocol level (no session restart needed)

- **Do:** A new MCP registration is only visible to NEW Claude sessions, so prove the
  server at the protocol level instead. Run the piped handshake:
  ```bash
  ( printf '%s\n' \
    '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"wg-t6-05","version":"0"}}}' \
    '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
    '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
    '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"health","arguments":{}}}' \
    '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"sessions","arguments":{"limit":2}}}' \
    '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"search","arguments":{"q":"swagger","limit":2}}}' ; \
    sleep 3 ) | $AE/node_modules/.bin/tsx $AE/server/src/expose/mcp.ts > /tmp/t6-05-handshake.out 2>/tmp/t6-05-handshake.err
  grep -c '"jsonrpc"' /tmp/t6-05-handshake.out
  python3 -c "
  import json
  ok = set()
  for line in open('/tmp/t6-05-handshake.out'):
      line = line.strip()
      if not line:
          continue
      m = json.loads(line)
      if m.get('id') == 2:
          assert len(m['result']['tools']) >= 5, 'tool list too small'
          ok.add(2)
      if m.get('id') in (3, 4, 5):
          assert 'result' in m, f'id {m[\"id\"]} returned no result'
          body = json.loads(m['result']['content'][0]['text'])
          assert 'error' not in body, f'id {m[\"id\"]} tool returned error: {body}'
          ok.add(m['id'])
  assert {2, 3, 4, 5} <= ok, f'missing responses: { {2,3,4,5} - ok }'
  print('handshake OK')
  "
  ```
  Then the graceful-down negative (dead port, NOT killing the real server):
  ```bash
  ( printf '%s\n' \
    '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"wg","version":"0"}}}' \
    '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
    '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"health","arguments":{}}}' ; \
    sleep 3 ) | ANGELEYE_MCP_BASE_URL=http://localhost:59999 \
    $AE/node_modules/.bin/tsx $AE/server/src/expose/mcp.ts 2>/dev/null | grep -o 'not reachable'
  ```
- **Expect:** first block prints `handshake OK`; the id:4 sessions result contains real
  session objects; second block prints `not reachable` (a clean tool-text error, not a
  crash). The tsx process exits when the pipe closes (the `sleep 3` gives it time to
  answer).
- **Failure signal:** zero jsonrpc lines in the .out file (stdout polluted or the process
  crashed — read `/tmp/t6-05-handshake.err`); the python assert fails; the process hangs
  past ~15s.
- **Counter-move:** hang → `pkill -f 'expose/mcp.ts'`, then inspect
  `/tmp/t6-05-handshake.out` — the responses may already be captured (the SDK sometimes
  outlives stdin-close); if all four ids are present, treat as pass and note the
  no-exit-on-stdin-close quirk in the results JSON. Stdout pollution → find the stray
  write, route it to stderr, re-run. Any assert failing twice after fixes → leave in
  running/ with a `## Status` note; a wrapper that fails its own handshake must not be
  registered (skip Moves 5–6 except the self-report).

### Move 5 — Register user-scope as `angeleye`

- **Do:**
  ```bash
  claude mcp add --scope user angeleye -- \
    /Users/davidcruwys/dev/ad/apps/angeleye/node_modules/.bin/tsx \
    /Users/davidcruwys/dev/ad/apps/angeleye/server/src/expose/mcp.ts
  claude mcp get angeleye
  ```
  (Absolute paths mandatory — MCP launch cwd is undefined. Repo-local tsx binary is the
  cortex-parity registration precedent already in `~/.claude.json`.)
- **Expect:** `claude mcp get angeleye` prints the entry with exactly that command/args;
  `claude mcp list` now contains `angeleye`.
- **Failure signal:** `claude mcp add` errors, or the flag syntax is rejected (CLI versions
  drift).
- **Counter-move:** → **Fork F3**. If F3's Route B also fails → restore the Recon 8 backup
  (`cp /tmp/t6-05-claude-json.bak ~/.claude.json`), verify sentinel still listed via
  `claude mcp list`, and park per **Abort A4**.

### Move 6 — Document, commit, self-report

- **Do:** (a) Write `$AE/docs/mcp-surface.md`: the tool table from Move 3 (as-built, minus
  dropped tools), the registration one-liner, the base-URL/env-override rule, the
  graceful-down behaviour, and "read-only by design; write tools are a future decision".
  (b) Append a short `## MCP surface` section to `$AE/CLAUDE.md` (3–5 lines, pointing at
  docs/mcp-surface.md; do NOT touch the stale 5500/5501 port prose — T6-06).
  (c) Commit in the AngelEye repo ONLY the files this ticket created/changed
  (`server/src/expose/mcp.ts`, `server/package.json`, `package-lock.json`,
  `docs/mcp-surface.md`, `CLAUDE.md`) — nothing from Recon 8's pre-existing dirt. Message:
  `feat(server): MCP wrapper over the read API — expose/mcp.ts, user-scope 'angeleye' (wg-t6-05)`
  with the standard Co-Authored-By trailer; push.
  (d) Write the worker self-report to
  `$DF/engine/store/results/<this-ticket-filename>.json` in the exact form the
  orchestrator's task prompt demands, including: final tool list, any dropped endpoints
  (F2), the Recon 3 server-state finding, and the note "new MCP visible only to sessions
  started after registration".
- **Expect:** `git -C $AE log --oneline -1` shows the commit; `git -C $AE status
  --porcelain` shows only Recon 8's pre-existing dirt; push accepted.
- **Failure signal:** push rejected (non-fast-forward).
- **Counter-move:** `git -C $AE pull --rebase` then push; conflicts in files this ticket
  didn't create → abort the rebase, leave committed locally, note it in the results JSON
  `notes`. Never resolve someone else's conflict in this repo.

## Forks

**F1 — AngelEye server already running vs down.**
Trigger: Recon 3's lsof on :5051.
→ **Route A (listener present):** the server is UP — do not restart it, do not touch
Overmind, proceed straight to the curls (AngelEye CLAUDE.md hard rule: never kill or
restart a running dev server).
→ **Route B (no listener):** start it the sanctioned way — `cd $AE && ./scripts/start.sh`
(Overmind; NEVER `npm run dev` from the Bash tool — AngelEye CLAUDE.md documents the env
leak). Wait ~15s, re-check `lsof -i :5051 | grep LISTEN` and `curl -sf
http://localhost:5051/health`. If start.sh fails or /health never answers after one retry
→ **Abort A2**. If you started it, leave it running at the end (a live AngelEye is the
desired end state; T6-04 owns daemonizing it properly).

**F2 — Endpoint drift on the non-core surface.**
Trigger: a Move 1 curl 404s/errors for anything OTHER than `/health` or `/api/sessions`
after the diagnostics grep-hunt.
→ **Route A (one or two peripheral endpoints dead):** drop those tools from the Move 3
table, list them under `dropped` in the results JSON, continue — a 5-tool surface still
satisfies the doctrine.
→ **Route B (three or more dead, or the response envelope isn't
`{"success":true,"data":...}` anywhere):** the API has drifted beyond this war game's map
→ **Abort A1**.

**F3 — `claude mcp add` unavailable or syntax-drifted.**
Trigger: Move 5's command errors.
→ **Route A (syntax drift):** `claude mcp add --help` and adapt flags (scope flag may have
moved); retry once with corrected syntax.
→ **Route B (CLI subcommand gone/broken):** edit `~/.claude.json` directly — Recon 8's
backup already exists. `python3` round-trip: load the JSON, add
`mcpServers.angeleye = {"command": "<abs tsx>", "args": ["<abs mcp.ts>"]}` matching the
existing entries' shape exactly, dump with `indent=2`, then re-verify the file still
parses AND `claude mcp list` still shows the pre-existing servers. Any parse failure →
restore the backup immediately, then **Abort A4**.

## Assumptions ledger

1. **Read-only surface is the doctrine's bar for a first retrofit.** AngelEye has write
   endpoints (registry backfills, sync, hooks ingest) — deliberately excluded: an MCP that
   can mutate the session registry from any Claude session is a decision, not a default.
   If execution-time context shows David wants write tools → note it in the results JSON
   as a follow-on ticket; do not add them here.
2. **Proxy-over-HTTP is the right wrapper shape** (vs sentinel's read-the-snapshot-file
   style). Plausible: AngelEye's business logic lives in `server/src/services/` behind the
   API, and the ticket's own brief says "API exists, MCP surface doesn't" — wrap, don't
   re-implement. Consequence: data tools need the server up (graceful error when down). If
   David objects to the running-server requirement at triage/HITL → park to
   needs-decision/ (switching to direct file reads is a different architecture, not a
   tweak).
3. **Name `angeleye`, user scope.** No collision found in `claude mcp list` on 2026-07-06
   and no `mcp__angeleye__*` tools exist. If a collision appears at execution time →
   **Abort A3** — naming is David's (standing preference: his naming over dev-speak).
4. **tsx-based launch is acceptable** (no compile step in the registration): precedent is
   the `cortex-parity` entry in `~/.claude.json` which launches a repo-local `tsx`
   directly. If David wants a compiled `node dist/...` entrypoint, that's a one-line
   registration change later — don't build it speculatively.
5. **The session registry is non-empty** (weeks of ingested data existed under
   `~/.claude/angeleye/` on 2026-07-06), so `sessions`/`search` return real rows. If it's
   empty at execution time, Move 1's counter-move already covers it (wire but mark
   unproven) — that emptiness itself is a T6-04 signal worth a line in the results JSON.

## Abort conditions

**A1 — AngelEye has drifted beyond this map.** Core routes missing (Recon 1, Move 1),
`.env` absent (Recon 2), toolchain unrecoverable (Recon 7), or F2 Route B. Park: write
`engine/store/needs-decision/wg-t6-05-angeleye-mcp.json` containing
`{"ticket":"wg-t6-05-angeleye-mcp","question":"AngelEye's API/layout differs from the T6-05 war game (authored 2026-07-06): <what differs>. Re-scope the MCP surface, or re-author after T6-04 lands?","proposed":"<one line>","note":"<observed state>"}`.
Leave the ticket in `running/`. Never invent a tool surface against an API you can't see.

**A2 — AngelEye server won't boot.** F1 Route B fails (start.sh errors or /health never
answers). This is exactly the territory T6-04 (AngelEye revival) exists to fix. Park to
needs-decision/ (same JSON shape, question: "AngelEye server fails to boot: <error>.
Should T6-04 (revival) land before T6-05 (MCP wrapper)?", proposed: "sequence T6-04 first").
Leave in `running/`. Do not debug the Express app's boot — that's scope theft from T6-04.

**A3 — Someone got here first.** `server/src/expose/` or an SDK dep already exists
(Recon 4), or `angeleye` is already registered (Recon 5 / Move 5). Park to needs-decision/
(question: "an AngelEye MCP surface already exists at <where>: extend it, supersede it, or
close this ticket as done?"). Leave in `running/`. Never overwrite or shadow an existing
registration.

**A4 — Registration path unusable.** Both F3 routes failed and the backup is restored.
The code half of the ticket may be complete and committed; the registration half is not.
Park to needs-decision/ (question: "MCP wrapper built and protocol-verified but `claude
mcp add` and manual ~/.claude.json edit both failed: <errors>. How should registration
happen?"), leave in `running/`, and say in the results JSON exactly which half is done.

## Verification

Run with `AE=/Users/davidcruwys/dev/ad/apps/angeleye`:

```bash
ls $AE/server/src/expose/mcp.ts                                    # exists
cd $AE && npm run typecheck -w server                              # exit 0
grep -c modelcontextprotocol $AE/server/package.json               # ≥1
# protocol-level proof (server must be reachable):
#   re-run Move 4's first block → prints "handshake OK"
claude mcp get angeleye                                            # shows abs-path tsx + mcp.ts
grep -n "MCP surface" $AE/CLAUDE.md                                # section present
ls $AE/docs/mcp-surface.md                                         # exists
git -C $AE log --oneline -1 | grep wg-t6-05                        # committed
ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/results/ | grep -c wg-t6-05   # 1
```

Move 4's graceful-down block must have printed `not reachable` at least once (dead-port
negative), and the handshake's `sessions` call must have returned real session objects
(or been explicitly marked unproven under Move 1's empty-registry counter-move).

Negative checks (what must NOT have changed):

```bash
grep -c "appyradar-sentinal/src/access/bindings/mcp.ts" ~/.claude.json   # 1 — legacy sentinel entry untouched (T6-02's job)
git -C $AE diff --stat HEAD~1 -- server/src/index.ts server/src/routes/ .env   # empty — no Express/env changes
lsof -i :5051 | grep -c LISTEN                                            # ≥1 — server alive (never killed; if Recon 3 found it down and F1-B started it, it stays up)
```

And no other MCP entry in `~/.claude.json` was added, removed, or edited (compare against
`/tmp/t6-05-claude-json.bak`: `python3 -c "import json; a=json.load(open('/tmp/t6-05-claude-json.bak'))['mcpServers']; b=json.load(open('$HOME/.claude.json'))['mcpServers']; assert {k:v for k,v in b.items() if k!='angeleye'}==a, 'other entries changed'; print('mcpServers clean')"`).

## Executor notes (sonnet)

- **Scope fence:** create `$AE/server/src/expose/mcp.ts` + `$AE/docs/mcp-surface.md`,
  append one section to `$AE/CLAUDE.md`, add one npm dep to the server workspace, add ONE
  entry (`angeleye`) to the user MCP config, write one results JSON in dark-factory —
  NOTHING else. No edits to `server/src/index.ts`, routes, services, `.env`, the client,
  or anything in the appyradar-sentinel/sentinal repos.
- **Never restart or kill a running AngelEye server**, and never launch it via `npm run
  dev` from Bash — `./scripts/start.sh` (Overmind) is the only sanctioned start
  (AngelEye CLAUDE.md documents the PORT env-leak failure mode).
- **stdout discipline is the whole game** for stdio MCP: if Move 4 shows garbage before
  the first `{`, hunt the stray write — do not "work around" it with output filtering.
- **Prefer HITL over guessing** on anything naming- or scope-shaped (tool names, a write
  tool "while you're in there", a different registration scope): needs-decision/ costs
  minutes; a wrong doctrine precedent gets copied by every later retrofit (T6-14 sweeps
  the whole constellation with whatever shape this ticket sets).
- **The rabbit hole:** AngelEye's ingestion problems (hook compat, subagent detection,
  empty/stale registry rows) will be visible in the data the moment you curl
  `/api/sessions`. All of it is T6-04's problem. You are wrapping the API, not fixing the
  app — if the API answers HTTP 200, it is good enough to wrap. Skip every temptation to
  clean the data.
