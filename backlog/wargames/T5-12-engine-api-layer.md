# T5-12 — Engine API layer (API+MCP doctrine)

| field | value |
|---|---|
| ticket | wg-t5-12-engine-api-layer |
| track / size / priority | T5 Watchtower / M / normal |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Promote `engine/status.py --json` from a CLI you must shell into a **stable, always-on seam**:
a read-only HTTP API over the engine store plus an MCP wrapper over that API, per the standing
doctrine in `backlog/concepts.md` ("Every app = API + MCP-over-API — API for harnesses/Monitors
(curl); MCP for skills/agents (conversational)"). Done means: `engine/api.py` serves the
status report + store sections over HTTP on :7430, kept alive by launchd; `engine/mcp/server.mjs`
exposes 3 read-only MCP tools that call that API (never the store directly); the server is
registered in the repo's `.mcp.json`; and the JSON contract is written down in
`engine/docs/API.md` with an additive-only change rule — so Watchtower (T5-01/02/06), the
Cardputer front desk (T5-10/11), and any agent all read ONE seam instead of each growing its
own store-reading path.

## Locked context

- **Q4 (decisions.md):** everything through the engine — this ticket is executed by sonnet
  Swagger dispatch; nothing built here ever calls `claude`.
- **Q6 (decisions.md):** Watchtower is a real web app — this API is the seam it will consume;
  do NOT build any UI here.
- **No `-p`/headless/SDK ever; interactive `claude` only** — moot for this build (nothing here
  spawns Claude), but the API must not add any dispatch path either. **Read-only surface.**
- **HALT/BACKOFF respected implicitly** — the API only *reports* halt/backoff state (it's in
  the status report already); it must never write, clear, or set those flags itself. (One known
  indirect exception documented in Move 1.)
- **Store is a growing ledger** — the API never writes to `engine/store/` (no POST/PUT/DELETE,
  405 everything non-GET).
- **No YLO/POEM work** — out of scope entirely.

## Recon (verify before any work)

Docs lag code in this repo. Run every check; each replaces doc-trust. All paths relative to
`/Users/davidcruwys/dev/ad/apps/dark-factory` unless absolute.

1. `python3 engine/status.py --json | python3 -m json.tool > /dev/null; echo $?` → expect `0`.
   The report's top-level keys as of 2026-07-06: `generated_at, halt, backoff, queue, running,
   done, workers, audit_tail` (from `build_report()` in `engine/status.py`, ~line 141). If the
   command fails or the store layout has moved → **Abort A1**.
2. `grep -rn "HTTPServer\|http.server" engine/*.py` → expect **no hits** (as of 2026-07-06 no
   HTTP server exists anywhere in `engine/`). If an engine HTTP API already exists → someone
   raced this ticket → **Abort A2**.
3. `lsof -iTCP:7430 -sTCP:LISTEN` → expect empty (`:7430` is earmarked "DF job queue + board"
   in `docs/constellation-map.md` line 72 but the old `experiments/watchtower-board` is dark;
   port was free at authoring). If occupied → **Fork F1**.
4. `/usr/bin/python3 --version` → expect ≥ 3.9. The launchd house pattern
   (`engine/launchd/com.appydave.dark-factory-wake.plist`) runs `/usr/bin/python3`, which is
   the Xcode CLT python, NOT the brew 3.14 on PATH. Your `api.py` must run under BOTH — write
   for the older one (no 3.10+ syntax: no `match`, no `X | Y` type unions). If
   `/usr/bin/python3` is missing → use `$(which python3)` in the plist instead and note it in
   the commit message.
5. `node --version` → expect ≥ 18 (v25.8.0 at authoring; the MCP wrapper uses global `fetch`,
   available since node 18). If node is missing → **Abort A3**.
6. House MCP pattern files exist: `ls /Users/davidcruwys/dev/ad/apps/kdd-bridge/server.mjs
   spikes/blackboard-mcp/server.mjs` → both present. These are the zero-dependency
   JSON-RPC-over-stdio pattern you copy in Move 4. If both are gone → **Abort A3**.
7. `cat .mcp.json` → expect `mcpServers` containing `blackboard` (relative path) and
   `kdd-bridge` (absolute path), and **no** `df-engine` key. If `df-engine` already exists →
   **Abort A2**. If `.mcp.json` itself is missing → create it fresh in Move 6 with just
   `{"mcpServers": {}}` plus your entry; don't hunt for a lost one.
8. `grep -rn "engine/store\|status.py\|:7430" /Users/davidcruwys/dev/ad/apps/watchtower/server
   /Users/davidcruwys/dev/ad/apps/watchtower/shared 2>/dev/null` → expect **empty** (Watchtower
   was a 1-commit AppyStack scaffold with zero engine references at authoring). If it now reads
   engine state → **Fork F2**.
9. `ls engine/launchd/` → expect `com.appydave.dark-factory-wake.plist`, `install.sh`,
   `uninstall.sh` — the `__APP_ROOT__`-sed launchd house pattern you mirror in Move 3. If the
   dir is gone → skip Move 3, deliver foreground-run instructions in `API.md` instead, and note
   the skip in the commit message.

## Moves

### Move 1 — write `engine/api.py`

- **Do:** Create `engine/api.py`: a stdlib-only (no pip installs) HTTP server. Requirements:
  - `from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler` — threading because
    `build_report()` shells `tmux list-sessions` with a 5s timeout and must not serialize
    requests behind it.
  - Import the existing report builder, don't reimplement it:
    `from status import build_report` and `from orchestrator import Q, RUN, DONE, RES` (python
    puts the script's own dir on `sys.path`, so `python3 engine/api.py` works from any cwd —
    same mechanics `status.py` relies on). Also
    `NEEDS = os.path.join(os.path.dirname(Q), "needs-decision")` — `orchestrator.py` defines
    `NEEDS` at module level (line 57) but as part of a tuple-unpack; import it directly if
    `from orchestrator import NEEDS` works, else derive it as above.
  - GET-only. Any other method → `405` with body `{"error": "read-only API"}`. Unknown path →
    `404`. Every response `Content-Type: application/json`.
  - Endpoints:
    - `GET /api/health` → `{"ok": true, "service": "df-engine-api", "api_version": 1,
      "generated_at": "<UTC ISO>"}` — must NOT call `build_report()` (cheap enough for a
      hardware poller every few seconds).
    - `GET /api/status?n_done=5&n_audit=5` → `{"api_version": 1, **build_report(n_done,
      n_audit)}`. Clamp both params to 1..50, default 5, ignore garbage values.
    - `GET /api/queue` / `GET /api/running` / `GET /api/done` → the matching subsection of
      `build_report()` (same envelope: `{"api_version": 1, "queue": {...}}` etc.).
    - `GET /api/needs-decision` → `{"api_version": 1, "count": N, "items": [{"file": f,
      **<parsed JSON>}...]}` for every `*.json` in `engine/store/needs-decision/` (worker-written
      shape is `{ticket, question, proposed, note}` per `orchestrator.py task_prompt(gated=True)`,
      but serve whatever the file contains — no schema enforcement). `status.py` doesn't expose
      this; it's the one additive section, and T5-06's HITL inbox needs it.
  - Bind `0.0.0.0`, port `int(os.environ.get("DF_API_PORT", "7430"))`.
  - One-line access log per request to stdout (launchd redirects it to a file in Move 3).
  - Top-of-file docstring stating: read-only; the ONE known indirect write is that
    `build_report()` calls `is_backoff()`, which auto-clears an *expired* BACKOFF flag file —
    identical behavior to running `status.py` by hand, by design (governor idiom, see
    `engine/docs/ENGINE-NOTES.md` CAP row); the API adds no new writes.
- **Expect:** `python3 -c "import ast; ast.parse(open('engine/api.py').read())"` exits 0, and
  `/usr/bin/python3 -c "import ast; ast.parse(open('engine/api.py').read())"` also exits 0
  (syntax valid on the older interpreter).
- **Failure signal:** either parse fails, or `from orchestrator import NEEDS` errors at runtime
  in Move 2.
- **Counter-move:** fix syntax for the lower version (recon 4 listed the forbidden constructs);
  for `NEEDS`, fall back to the `os.path.join(os.path.dirname(Q), "needs-decision")` derivation.
  If imports from `status`/`orchestrator` fail for a *structural* reason (module reshaped) →
  **Abort A1**.

### Move 2 — foreground smoke test

- **Do:** From the repo root: `python3 engine/api.py > /tmp/df-api-smoke.log 2>&1 & sleep 1`,
  then:
  1. `curl -s http://localhost:7430/api/health` → parse with `python3 -m json.tool`.
  2. `curl -s "http://localhost:7430/api/status?n_done=3&n_audit=3"` → parse clean.
  3. Contract equivalence: `curl -s http://localhost:7430/api/status | python3 -c "import
     json,sys; d=json.load(sys.stdin); d.pop('api_version'); print(sorted(d.keys()))"` must
     equal `python3 engine/status.py --json | python3 -c "import json,sys;
     print(sorted(json.load(sys.stdin).keys()))"`.
  4. `curl -s http://localhost:7430/api/needs-decision`, `/api/queue`, `/api/running`,
     `/api/done` → each parses clean.
  5. `curl -s -X POST http://localhost:7430/api/status -o /dev/null -w "%{http_code}"` → `405`.
  6. `curl -s http://localhost:7430/api/nope -o /dev/null -w "%{http_code}"` → `404`.
  Then `kill %1`.
- **Expect:** all six checks pass; the keys lists in check 3 are identical.
- **Failure signal:** curl connection refused (server died — read `/tmp/df-api-smoke.log`),
  JSON parse error, mismatched keys, or wrong status codes.
- **Counter-move:** fix `api.py` and re-run this move. If the *same* check fails twice in a row
  for a reason you cannot see in the smoke log → **Abort A4** (don't loop blind).

### Move 3 — launchd persistence

- **Do:** Mirror the wake watcher's house pattern (recon 9):
  1. Write `engine/launchd/com.appydave.dark-factory-api.plist` — copy the wake plist's
     structure but: `Label` `com.appydave.dark-factory-api`; `ProgramArguments`
     `/usr/bin/python3 __APP_ROOT__/engine/api.py`; NO `WatchPaths`; add
     `<key>KeepAlive</key><true/>` and `<key>RunAtLoad</key><true/>`; keep
     `ThrottleInterval 10`; `StandardOutPath`/`StandardErrorPath` →
     `__APP_ROOT__/engine/store/api.log`.
  2. Write `engine/launchd/install-api.sh` — copy `install.sh` verbatim, change only LABEL and
     the two echo lines. Do NOT edit the existing `install.sh`/`uninstall.sh` (wake's). Add the
     matching `uninstall-api.sh` (unload + rm the LaunchAgents plist).
  3. `chmod +x` both scripts, run `engine/launchd/install-api.sh`.
- **Expect:** `launchctl list | grep com.appydave.dark-factory-api` shows the job with a live
  PID (KeepAlive job, unlike wake's `-`), and `curl -s http://localhost:7430/api/health` returns
  `"ok": true` within ~5s of loading.
- **Failure signal:** job loaded but no PID / curl refused → read `engine/store/api.log`.
  Classic cause: `/usr/bin/python3` missing (recon 4) or port already bound by your own Move-2
  process you forgot to kill.
- **Counter-move:** kill stray `api.py` processes (`pkill -f "engine/api.py"`), fix per the log,
  `install-api.sh` again. If macOS blocks the listener with a firewall prompt that can't be
  accepted unattended → bind `127.0.0.1` instead (one-line change), note it in `API.md` under
  "Cardputer caveat", and continue — see Assumptions ledger #1.

### Move 4 — write `engine/mcp/server.mjs` (MCP-over-API)

- **Do:** Create `engine/mcp/server.mjs`: zero-dependency JSON-RPC-over-stdio MCP server,
  copying the protocol scaffolding (initialize / tools/list / tools/call loop, stdin line
  reader, response writer) from `/Users/davidcruwys/dev/ad/apps/kdd-bridge/server.mjs` — same
  house pattern as `spikes/blackboard-mcp/server.mjs`. No `package.json` needed (no deps); if
  node complains about module type, name it `.mjs` (it is) and nothing more. Server name
  `df-engine`. Base URL `process.env.DF_API_URL || "http://127.0.0.1:7430"`. Exactly 3 tools,
  all read-only, all implemented as `fetch(BASE + path)` — **never** read `engine/store/`
  directly (that's the doctrine: MCP wraps the API, so there is one seam, not two):
  - `engine_status` — args `{n_done?: number, n_audit?: number}` → `/api/status?...`.
    Description in David's voice, trigger-only: "Use when you need the dark-factory engine's
    current state — queue depth/age, running tickets, recent done verdicts, workers, HALT/BACKOFF."
  - `engine_health` — no args → `/api/health`. "Use when checking whether the engine API is up
    before relying on it."
  - `engine_needs_decision` — no args → `/api/needs-decision`. "Use when checking whether any
    ticket is parked mid-task waiting on a human decision (HITL gate)."
  On fetch failure every tool returns an MCP error result whose message says the API is down
  and how to restart it: `bash /Users/davidcruwys/dev/ad/apps/dark-factory/engine/launchd/install-api.sh`
  (or foreground: `python3 engine/api.py`). No fallback to shelling `status.py` — a dead API
  must be visible, not papered over.
- **Expect:** `node --check engine/mcp/server.mjs` exits 0.
- **Failure signal:** syntax error, or the borrowed scaffolding references kdd-bridge lib files.
- **Counter-move:** strip the borrowed code down to the protocol loop only (it has no lib
  dependency in its protocol section); re-check.

### Move 5 — MCP smoke test

- **Do:** With the launchd API up (Move 3), run the kdd-bridge-style pipe test from the repo
  root:
  ```bash
  (printf '%s\n' \
    '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
    '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
    '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"engine_health","arguments":{}}}' \
    '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"engine_status","arguments":{"n_done":2}}}' \
    ; sleep 0.3) | node engine/mcp/server.mjs
  ```
  Then stop the API (`launchctl unload ~/Library/LaunchAgents/com.appydave.dark-factory-api.plist`),
  re-run just the `engine_health` call, confirm the error message contains the restart command,
  then `launchctl load` it back.
- **Expect:** `tools/list` returns exactly 3 tools with schemas; `engine_health` returns
  `"ok": true`; `engine_status` returns the report; the API-down call returns the
  restart-command error; after re-load, health passes again.
- **Failure signal:** missing tools, hung pipe (server not exiting on stdin close), fetch error
  while the API is demonstrably up (`curl` works).
- **Counter-move:** if fetch fails while curl works, check the base URL (must be `127.0.0.1`,
  not `localhost`, if IPv6 resolution bites — node's fetch can resolve `localhost` to `::1`
  where the server listens v4-only). Fix and re-run. Second consecutive unexplained failure →
  **Abort A4**.

### Move 6 — register in `.mcp.json`

- **Do:** Add to the repo-root `.mcp.json` `mcpServers` (preserving the existing `blackboard`
  and `kdd-bridge` entries byte-for-byte):
  ```json
  "df-engine": {
    "type": "stdio",
    "command": "node",
    "args": ["engine/mcp/server.mjs"]
  }
  ```
  Relative path — same convention as the `blackboard` entry (project-scoped, resolved from repo
  root).
- **Expect:** `python3 -m json.tool .mcp.json` parses clean and shows 3 servers.
- **Failure signal:** parse error, or a `df-engine` key was already there (recon 7 missed a
  race).
- **Counter-move:** fix JSON by hand; if a conflicting `df-engine` with a *different* shape
  appeared since recon → **Abort A2**.

### Move 7 — write the contract: `engine/docs/API.md` + README pointer

- **Do:**
  1. Write `engine/docs/API.md`: purpose (the one seam, doctrine quote + pointer to
     `backlog/concepts.md` "Every app = API + MCP-over-API" row); base URL + port (:7430,
     `DF_API_PORT` override); every endpoint with its exact JSON shape (paste real sanitized
     responses from Move 2); the params and their clamps; **the stability rule: the contract is
     additive-only — existing keys never change meaning or disappear; new keys may appear;
     consumers must ignore unknown keys**; the `api_version` bump rule (only on a breaking
     change, which requires a David decision); the known BACKOFF auto-clear side effect; the
     named consumers (Watchtower T5-01/02/06, Cardputer T5-10/11, agents via the `df-engine`
     MCP server); run/install/uninstall commands.
  2. Append a short "HTTP API + MCP" section to `engine/README.md` (3–6 lines) pointing at
     `engine/docs/API.md` — don't restate the contract there.
- **Expect:** both files render sensibly; `API.md` shapes match what Move 2 actually observed
  (not what this war game predicted).
- **Failure signal:** you're documenting a shape you didn't observe.
- **Counter-move:** re-run the Move-2 curls and paste reality.

### Move 8 — commit + push

- **Do:** `git add engine/api.py engine/mcp/server.mjs engine/launchd/com.appydave.dark-factory-api.plist
  engine/launchd/install-api.sh engine/launchd/uninstall-api.sh engine/docs/API.md
  engine/README.md .mcp.json` — then commit
  (`feat(engine): read-only HTTP API :7430 + df-engine MCP wrapper — one seam for Watchtower/Cardputer/agents (T5-12)`)
  and push to main. Do NOT commit `engine/store/api.log` (it's runtime output; add to
  `.gitignore` if the store isn't already ignored — check `git status` first).
- **Expect:** `git status` clean for the listed files; push succeeds.
- **Failure signal:** push rejected (remote moved ahead).
- **Counter-move:** `git pull --rebase` then push; on conflict in `.mcp.json`, re-apply your
  entry on top of the incoming version.

## Forks

**F1 — port :7430 occupied at recon/run time.**
Trigger: recon 3 shows a listener, or Move 2/3 gets "address in use" not caused by your own
stray process. → **Route A** (occupant is a stray/transient — e.g. an old
`experiments/watchtower-board` server someone hand-started): do NOT kill it (David may be using
it); take **:7431**, set it via `DF_API_PORT` in the plist (`EnvironmentVariables` dict) and as
the default in `API.md`/`server.mjs`, and note the deviation in the commit message. → **Route B**
(occupant IS already an engine-store HTTP API): that's a race with another ticket → **Abort A2**.

**F2 — Watchtower grew its own engine-reading path since authoring.**
Trigger: recon 8 finds `engine/store`/`status.py` references in `apps/watchtower`. → **Route A**
(it shells `status.py --json` or reads store files directly): proceed with this build unchanged
— the API is still the right seam — but append a follow-up note to this war-game file's Status
section: "Watchtower reads the store directly at <files>; converge onto :7430 in T5-01/T5-02."
Do NOT edit the Watchtower repo. → **Route B** (Watchtower already *serves* its own HTTP API
over the engine store): two competing seams is a David call → **Abort A2**.

## Assumptions ledger

1. **Bind `0.0.0.0`, not loopback.** Plausible because the candidate names Cardputer (an
   M5Stack on the LAN) and fleet workers (Tailscale, Q8) as consumers, and the data is
   read-only status. If macOS firewall interference or David objects at triage → flip the
   one-line bind to `127.0.0.1`, note the Cardputer caveat in `API.md` (Move 3 counter-move
   already covers the unattended case). Not park-worthy either way.
2. **A standing launchd service is acceptable.** Plausible because the engine already ships a
   launchd agent (wake watcher, installed via the same pattern) and unknowns-map's "standing
   commitment needs explicit go" concern was about *acting* crons — this one only serves reads.
   If David objects → `uninstall-api.sh` exists precisely so the whole persistence layer is
   one command to remove; the API still works foreground. Note in triage, don't park.
3. **Claiming :7430 honors, not squats, the constellation-map earmark.** The map's line 72
   assigns :7430 to the dark "Watchtower-engine/-board (exp)" — superseded by the real-app
   decision (Q6) and the T5-09 kill verdict. This API is that row's successor. If wrong →
   F1 Route A's :7431 fallback is the escape.
4. **`needs-decision/` files stay worker-shaped** (`{ticket, question, proposed, note}`).
   The endpoint serves file content verbatim, so a shape change degrades gracefully — no
   action needed if false, the contract only promises `file` + passthrough.
5. **No other war-game ticket ships an engine HTTP server.** Checked the staged portfolio at
   authoring (T1-*, T2-*, T3-* tickets; none do). If one landed anyway → recon 2 / Abort A2
   catches it.

## Abort conditions

**A1 — engine reshaped.** `status.py --json` fails, or `build_report`/path constants no longer
import (recon 1, Move 1). Park: write `engine/store/needs-decision/wg-t5-12-engine-api-layer.json`
with `{"ticket":"wg-t5-12-engine-api-layer","question":"engine/status.py or orchestrator.py has
been reshaped since 2026-07-06 — the API layer's import seam is gone. Rebase this war game on
the new engine shape?","proposed":"<what you found>","note":"T5-12 recon/Move-1 failure"}`.
Leave the ticket in running/. Never reimplement `build_report` yourself.

**A2 — competing seam exists.** An engine-store HTTP API already exists (recon 2, F1-B, F2-B),
or a conflicting `df-engine` MCP registration appeared (recon 7, Move 6). Park to
needs-decision/ (same JSON shape) with the question "Two seams over the engine store — which
one wins?" and the paths of both. Never ship a second parallel API.

**A3 — toolchain missing.** No node ≥ 18, or both house-pattern MCP servers gone (recon 5, 6).
Park to needs-decision/ with what's missing. Don't `brew install` anything — installs are an
explicit-go action.

**A4 — twice-failed smoke with no visible cause.** The same Move-2 or Move-5 check fails twice
consecutively with logs that don't explain it. Park to needs-decision/ with the failing check,
both logs, and your best hypothesis. Never loop a third time.

## Verification

Run from `/Users/davidcruwys/dev/ad/apps/dark-factory`:

```bash
# 1. API up under launchd
launchctl list | grep com.appydave.dark-factory-api            # job present, live PID
curl -s http://localhost:7430/api/health | python3 -m json.tool # "ok": true, api_version 1

# 2. Contract equivalence with status.py (keys, not values — values are time-sensitive)
curl -s http://localhost:7430/api/status | python3 -c "import json,sys; d=json.load(sys.stdin); d.pop('api_version'); print(sorted(d.keys()))"
python3 engine/status.py --json | python3 -c "import json,sys; print(sorted(json.load(sys.stdin).keys()))"
# → identical lists

# 3. Read-only enforced
curl -s -X POST http://localhost:7430/api/status -o /dev/null -w "%{http_code}"   # 405
curl -s -X DELETE http://localhost:7430/api/queue -o /dev/null -w "%{http_code}"  # 405

# 4. MCP wrapper: tools/list shows exactly engine_status, engine_health,
#    engine_needs_decision; engine_health round-trips through the HTTP API
(printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
  '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"engine_health","arguments":{}}}' \
  ; sleep 0.3) | node engine/mcp/server.mjs

# 5. Registration + contract doc exist
python3 -m json.tool .mcp.json | grep df-engine
ls engine/docs/API.md engine/launchd/com.appydave.dark-factory-api.plist engine/launchd/install-api.sh engine/launchd/uninstall-api.sh
```

Negative checks (what must NOT have changed):

```bash
git log --oneline -1 -- engine/status.py engine/orchestrator.py engine/wake.py engine/halt.py
# → no commit from this ticket touches these four (API wraps, never modifies)
grep -c "readFileSync\|readdirSync" engine/mcp/server.mjs
# → 0 store reads in the MCP server (MCP-over-API, not MCP-over-files)
launchctl list | grep com.appydave.dark-factory-wake
# → wake watcher still loaded (Move 3 didn't disturb it)
ls engine/store/queue/*.json 2>/dev/null; ls engine/store/done/*.json | wc -l
# → queue/done untouched by this ticket (counts consistent with normal factory traffic)
```

Both files committed and pushed to main.

## Executor notes (sonnet)

- **Scope fence:** touch ONLY `engine/api.py`, `engine/mcp/server.mjs`, the two new launchd
  files (+uninstall), `engine/docs/API.md`, `engine/README.md` (append-only), `.mcp.json`
  (add-one-key). Never edit `status.py`, `orchestrator.py`, `wake.py`, `halt.py`, anything in
  `engine/store/`, the Watchtower repo, or `docs/constellation-map.md`.
- **Stdlib/zero-dep is a hard style constraint** — no pip, no npm install, no `package.json`
  under `engine/mcp/`. If you feel you need a dependency, you've overbuilt.
- **Python compatibility:** must parse and run under `/usr/bin/python3` (older) AND brew 3.14.
  No `match`, no `X | Y` unions, no `tomllib`.
- **HITL over guessing:** any situation where two systems could both claim to be "the seam"
  (F1-B, F2-B, duplicate `df-engine`) is a park, not a judgment call. The whole point of this
  ticket is ONE seam; guessing defeats it.
- **The rabbit hole to skip:** do NOT add write endpoints (ticket submission, HALT toggling,
  decision answering) "while you're in there" — Cardputer Stage 2 (T5-11) and the HITL inbox
  (T5-06) will design their write paths deliberately, with their own war games. This ticket is
  read-only by charter; a write path added casually here becomes an unguarded actuator on the
  factory floor. Equally: no caching layer, no websockets/SSE, no auth — the report builds in
  well under a second and the consumers poll.
