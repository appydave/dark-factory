# T5-03 — Live agent view

| field | value |
|---|---|
| ticket | wg-t5-03-live-agent-view |
| track / size / priority | T5 Watchtower / M / normal |
| executor | sonnet Swagger via engine |
| depends_on | wg-t5-01-watchtower-charter-scaffold (id assumed — see Assumption 1; Recon gates on ARTIFACTS, not the id) |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Give Watchtower the "what are the agents doing right now" surface (one of the four views David
named in decisions.md Q6). Ship, in `~/dev/ad/apps/watchtower`: **(a)** `GET /api/agents` — a
read-only Express route that composes `python3 engine/status.py --json --n-audit 200` (the
engine's authoritative aggregator) with per-worker `tmux capture-pane` tails and a
timeout-guarded AngelEye availability probe; **(b)** a worker state machine — each `df-worker-*`
is `working` (tmux session live + a `running/` ticket attributed to it via `audit_tail`),
`idle` (live, no ticket), or `stale` (ticket claims running but the worker session is gone —
the stuck-case smell, surfaced not hidden); **(c)** an **Agents** client view polling the route
every 5s: HALT/BACKOFF banners, worker cards (state chip, ticket title + age, short session id,
pane tail), an unattributed-running lane, an honest "AngelEye dark — revival is T6-04" badge,
and a "factory cold" empty state. Done means the route and view demonstrably track a worker
session appearing and disappearing (Move 8's fake-worker proof), all scaffold quality gates
pass, and the engine store has not been written to.

## Locked context

- **Q6 (decisions.md):** Watchtower is a **real web app** — this view lands in the
  `~/dev/ad/apps/watchtower` repo (AppyStack/RVETS scaffold), not a Mochaccino board.
- **Q4:** everything through the engine — written for sonnet Swagger dispatch, cwd =
  dark-factory repo root; the watchtower work is cross-repo by absolute path (T2-05 precedent).
- **Q9 (complement, don't replace):** `status.py` stays the single aggregator over the store.
  The Watchtower server shells out to `status.py --json` and NEVER reads
  `engine/store/queue|running|done|audit.jsonl` directly. The only engine-adjacent reads this
  ticket adds beyond status.py are `tmux capture-pane` (pane tails — not store data) and an
  HTTP probe of AngelEye.
- **Read-only over the factory:** no writes into `engine/store/` (executor park files in
  `needs-decision/` per aborts excepted), no dispatch path, and **never `tmux send-keys`** to
  any session — `capture-pane` only.
- **No `-p`/headless/SDK ever; interactive `claude` only:** nothing in this build spawns
  Claude. Move 8's fake worker is a `sleep` shell, never a `claude` process.
- **AngelEye revival is T6-04, not this ticket.** Probe-and-degrade only; no hook fixes, no
  daemonizing, no session-feed integration (extension point recorded, nothing built).
- **No YLO/POEM work.**

## Recon (verify before any work)

Docs lag code. Run every check. Repo roots: `DF=/Users/davidcruwys/dev/ad/apps/dark-factory`,
`WT=/Users/davidcruwys/dev/ad/apps/watchtower`.

1. **Dependency gate — did T5-01 land?** `git -C $WT log --oneline | head` and
   `grep -rn "status.py\|DARK_FACTORY\|engine" $WT/server/src $WT/docs 2>/dev/null`.
   As of authoring $WT is a **1-commit virgin scaffold** (`1f4d5e9 Initial commit: Watchtower —
   human control surface over Dark Factory`) with ZERO engine references — T5-01 (charter +
   scaffold + first deploy serving status.py --json) is expected to have added commits and an
   engine-state seam before you run. Repo missing entirely, or still exactly the virgin
   1-commit scaffold with no engine seam and no charter doc → **Abort A1**. Seam found →
   record its shape (route path, env var name, service file) → **Fork F1**.
2. **Engine aggregator healthy:**
   `cd $DF/engine && python3 status.py --json | python3 -m json.tool > /dev/null; echo $?` → `0`.
   Then confirm top-level keys are (at least) `generated_at, halt, backoff, queue, running,
   done, workers, audit_tail` (verified exact set at authoring). Crash or missing keys →
   **Abort A2**.
3. **Worker naming + pane primitive still hold:**
   `grep -n "df-worker\|capture-pane" $DF/engine/warm_pool.py` → expect session names
   `df-worker-<index>` (line ~64) and `capture-pane` as the read primitive (line ~74–75).
   `status.py` `tmux_workers()` (~line 94) returns `None` (tmux not on PATH) / `[]` (no tmux
   server, or none matching) / list of `"df-worker-N: ..."` `tmux list-sessions` lines. Naming
   scheme gone → **Abort A2**.
4. **Audit shape carries the ticket→worker mapping:** `tail -1 $DF/engine/store/audit.jsonl`
   → expect fields `ticket` (the queue filename), `worker` (`df-worker-N`), `session_id`,
   `transcript`, `claimed_by`, `claimed_at`, `attempt` (verified at authoring). Fields
   renamed/gone → **Abort A2**.
5. **Scaffold seams (your extension points):** confirm in `$WT/server/src/index.ts` that
   routers mount root-level via `app.use(healthRouter)` / `app.use(infoRouter)` with the rate
   limiter before routes; `routes/health.ts` (`GET /health`) + `routes/info.ts`
   (`GET /api/info`) use `apiSuccess`/`apiFailure` from `helpers/response.ts`
   (`{status:'ok', data, timestamp}` envelope); env is zod-parsed in `config/env.ts`
   (PORT default 5061, CLIENT_URL 5060). All verified at authoring; T5-01 may have moved
   things — adapt to what's there, keep the idioms.
6. **Client shell:** at authoring `$WT/client/src/App.tsx` renders `<LandingPage />` +
   dev-only `<DemoPage />`; no react-router in `client/package.json`. If T5-01 added a nav
   shell or router → **Fork F1 Route A** for the client too (add your view its way).
7. **AngelEye state:** `curl -s -m 2 http://127.0.0.1:5051/health || echo DARK` → authoring
   state: `DARK` (AngelEye's scaffold default port 5051 per
   `~/dev/ad/apps/angeleye/server/src/config/env.ts`). Either result is fine — it only picks
   your **Fork F2** route at Move 5 verification time.
8. **Is Watchtower already running?** `lsof -nP -i :5061 -i :5060 | grep LISTEN` → authoring
   state: nothing. Something listening → **Fork F3 Route B** (do NOT kill it — David or T5-01's
   deploy owns it).
9. **Tools:** `command -v tmux python3 node npm jq` → all present (verified: tmux + jq at
   `/opt/homebrew/bin/`). npm workspace installs: `ls $WT/node_modules > /dev/null 2>&1 || (cd $WT && npm install)`
   — a failed install gets ONE fix cycle, then **Abort A4**.
10. **Seam cleanliness:** `git -C $WT status --porcelain` → expect clean. Dirt in files this
    ticket touches (`server/src/index.ts`, `server/src/config/env.ts`, `client/src/App.tsx`,
    anything under `server/src/routes/` or `server/src/services/`) → **Abort A3**; dirt
    elsewhere → proceed, stage only your files, name the strangers in result notes.

## Moves

1. **Do:** Env seam. If F1-A found T5-01's dark-factory-root env var, REUSE it verbatim.
   Otherwise add to `$WT/server/src/config/env.ts` (zod schema, matching existing style):
   `DARK_FACTORY_ROOT` (string, default `/Users/davidcruwys/dev/ad/apps/dark-factory`) and
   `ANGELEYE_URL` (string, default `http://127.0.0.1:5051`); mirror both into `.env.example`
   with one-line comments.
   **Expect:** `cd $WT && npm run typecheck` exits 0; `server/src/config/env.test.ts` still
   green (extend it additively if it asserts the full key set).
   **Failure signal:** typecheck or env test failure.
   **Counter-move:** fix the schema addition (zod default syntax mismatch is the usual
   culprit). Second failure → you're fighting T5-01's restructure → re-read its env.ts and
   conform to it; if the file is unrecognizable vs Recon 5 → **Abort A3**.

2. **Do:** Engine adapter, `$WT/server/src/services/engineStatus.ts`: one exported async
   `fetchEngineStatus(root: string)` using `execFile` from `node:child_process` (promisified)
   — `execFile('python3', [join(root,'engine','status.py'), '--json', '--n-audit', '200'],
   { timeout: 15000, maxBuffer: 10 * 1024 * 1024 })`, JSON-parse stdout. Any error (spawn,
   timeout, non-zero exit, parse) → return `{ ok: false, error: <one-line string> }`; success
   → `{ ok: true, status: <parsed> }`. Never throw. Plus
   `services/engineStatus.test.ts` (vitest, mock `node:child_process` per the scaffold's
   existing mocking style) covering: happy parse, non-zero exit, garbage stdout.
   **Expect:** `cd $WT && npm test --workspace=@appydave/server` (or the scaffold's server
   test script) green including the 3 new cases.
   **Failure signal:** tests red, or the real call
   (`node -e` spike against the real `status.py`) returns `ok:false`.
   **Counter-move:** if the REAL status.py call fails while mocked tests pass, run Recon 2's
   command again and read stderr — status.py drift → **Abort A2**; a PATH problem (python3
   resolvable in your shell but not node's spawn env) → use `process.env.PATH` as-is and
   report absolute `python3` path fallback (`/usr/bin/env python3` style) in one retry.

3. **Do:** Pane tails, `$WT/server/src/services/tmuxPanes.ts`:
   `capturePaneTail(session: string, lines = 15)` — `execFile('tmux',
   ['capture-pane', '-p', '-t', session], { timeout: 5000 })`, split stdout, drop trailing
   blank lines, return last `lines`; ANY error (tmux gone, session vanished mid-poll) →
   `null`. Also `parseWorkerName(listLine: string)` → `listLine.split(':')[0].trim()` (the
   `workers[]` entries are raw `tmux list-sessions` lines like
   `"df-worker-1: 1 windows (created ...)"`). **capture-pane only — this module must contain
   no `send-keys` string at all.**
   **Expect:** unit tests green (mocked); grep guard passes:
   `grep -c "send-keys" $WT/server/src/services/tmuxPanes.ts` → `0`.
   **Failure signal:** any send-keys usage, or capture errors bubbling as thrown exceptions.
   **Counter-move:** wrap-and-null the errors; remove any interactive tmux verb. This is a
   hard rule, not a style call.

4. **Do:** Composer + state machine, `$WT/server/src/services/agents.ts`:
   `buildAgentsView(status, paneTails)` — pure function (no I/O; I/O stays in the route so
   this is trivially testable) producing exactly:
   ```json
   {
     "generated_at": "<status.generated_at>",
     "factory": {
       "halt": null, "backoff": null,
       "queue_depth": 0, "running_count": 0,
       "tmux": "ok | none | absent"
     },
     "workers": [
       { "name": "df-worker-1", "live": true, "state": "working | idle | stale",
         "ticket": { "file": "…", "title": "…", "claimed_at": "…", "attempt": 1 },
         "session_id": "…", "pane_tail": ["…"] }
     ],
     "unattributed_running": [ { "file": "…", "title": "…", "claimed_at": "…" } ],
     "angeleye": { "available": false, "url": "…", "hint": "…" }
   }
   ```
   Rules: `factory.halt`/`backoff` pass through status.py's objects (null when absent);
   `queue_depth` = `status.queue.depth`; `running_count` = `status.running.count`; `tmux` =
   `"absent"` when `status.workers === null`, `"none"` when `[]`, else `"ok"`. Attribution:
   for each `status.running.items[i]`, scan `status.audit_tail` from the END for the first
   entry whose `ticket === item.file` → that entry's `worker` + `session_id`; no match →
   the item goes to `unattributed_running`. Workers list = union of live tmux names (parsed
   from `status.workers`) and audit-attributed workers of running tickets; states: live +
   attributed ticket → `working`; live, none → `idle`; not live + attributed ticket →
   `stale` (`live:false`, `pane_tail:null`). `ticket.title` comes from the running item's
   `title` (status.py already computes the fallback chain — don't re-derive).
   Vitest fixtures for all four cases: working, idle, stale, unattributed.
   **Expect:** 4+ new tests green; `npm run typecheck` clean (type the response in
   `$WT/shared/src/types.ts` if F1-A shows T5-01 putting API types there, else co-locate).
   **Failure signal:** fixture disagreement — usually the audit scan direction (must be
   newest-first) or union logic double-listing a worker.
   **Counter-move:** fix against the fixture; the fixtures ARE the contract. A second red
   cycle on the same fixture → simplify: drop the union nicety, list live workers +
   stale-from-audit separately, and note it.

5. **Do:** AngelEye probe, `$WT/server/src/services/angeleye.ts`:
   `probeAngeleye(url: string)` — `fetch(url + '/health', { signal: AbortSignal.timeout(1500) })`;
   HTTP 200 → `{ available: true, url, hint: 'availability only — session feed is a T6-04
   extension point' }`; anything else (non-200, timeout, refused) →
   `{ available: false, url, hint: 'dark — revival is T6-04' }`. Never throws. **Fork F2**
   only changes which value you'll SEE at verify time — code is identical on both routes.
   **Expect:** mocked tests for 200 / refused / timeout green; live spike matches Recon 7's
   recorded state.
   **Failure signal:** unhandled rejection crashing the route when AngelEye is dark (the
   authoring-time state — this is the case that must be bulletproof).
   **Counter-move:** wrap in try/catch returning the dark shape; re-run the refused-case test.

6. **Do:** Route + wiring: `$WT/server/src/routes/agents.ts` — `GET /api/agents` calls
   `fetchEngineStatus(env.DARK_FACTORY_ROOT)`; on `ok:false` → `apiFailure(res,
   'engine unreachable: ' + error, 503)`; on success → capture pane tails for each live
   `df-worker-*` (Move 3), `probeAngeleye(env.ANGELEYE_URL)`, respond
   `apiSuccess(res, buildAgentsView(...))`. Mount in `index.ts` beside `infoRouter`
   (F1-A: beside T5-01's engine route instead). Route test per `routes/info.test.ts`'s
   pattern (mock the services).
   **Expect:** with the dev server up (Fork F3 decides how — Route A: `cd $WT && npm run dev`
   in background; Route B: the already-running instance):
   `curl -s http://127.0.0.1:5061/api/agents | jq '.status, (.data | keys)'` →
   `"ok"` + `["angeleye","factory","generated_at","unattributed_running","workers"]`.
   **Failure signal:** 404 (router not mounted / mounted after the 404 catch-all), 503, or
   rate-limiter 429s during rapid manual curls.
   **Counter-move:** 404 → mount order (must precede the catch-all); 503 → read the error
   field, it names the failing layer (Move 2 vs 3 vs 5); 429 → slow down, the limiter is
   scaffold-standard, do NOT weaken it. Second unexplained failure cycle → **Abort A4**.

7. **Do:** Client view. `$WT/client/src/pages/AgentsPage.tsx` (or T5-01's pages/views dir per
   F1-A): a `useAgents()` hook — `fetch('/api/agents')` (Vite dev proxy handles the origin;
   verified proxy config in scaffold README) on mount + `setInterval` 5000ms, cleared on
   unmount; state `{ data, error, lastUpdated }`. Render, Tailwind-only, **no new client
   dependencies**: (i) full-width banners when `factory.halt` (red, reason + since) or
   `factory.backoff` (amber, until) — mirrors status.py's banner precedent; (ii) worker
   cards: name, state chip (`working` green / `idle` neutral / `stale` red), ticket title +
   `claimed_at`, `session_id` first 8 chars, `pane_tail` in a scrollable `<pre>`;
   (iii) unattributed-running lane when non-empty; (iv) AngelEye badge from `hint`;
   (v) empty state when `workers` is `[]`: "Factory cold — no df-worker sessions" +
   `queue_depth` so the page still informs; (vi) error state "engine unreachable" +
   `lastUpdated`. Wire into the app per **Fork F1** (A: T5-01's nav; B: minimal two-tab strip
   in `App.tsx` — Landing | Agents — do NOT delete LandingPage/DemoPage). One component test
   (render with a fixture, assert a worker card + empty state).
   **Expect:** `npm run typecheck && npm test` green; browser (or `curl -s
   http://127.0.0.1:5060` in dev) serves the app; the Agents view shows the cold-factory
   empty state (authoring-truth: no workers exist between engine runs — empty is the COMMON
   state and must look intentional).
   **Failure signal:** CORS/proxy errors in dev (fetching absolute `:5061` instead of
   relative path), interval leak (multiple polls after navigation).
   **Counter-move:** use the relative `/api/agents` path (proxy contract); return the
   cleanup function from `useEffect`. UI polish beyond the listed elements is out of scope —
   ship the working view.

8. **Do:** Live end-to-end proof with a fake worker (never `claude`):
   `tmux new-session -d -s df-worker-9 'echo WG-T5-03-PANE-PROOF; exec sleep 300'` →
   within one poll cycle `curl -s http://127.0.0.1:5061/api/agents | jq
   '.data.workers[] | select(.name=="df-worker-9") | {state, pane: (.pane_tail|join(" "))}'`
   → `state == "idle"` and pane contains `WG-T5-03-PANE-PROOF`; confirm the client view shows
   the card. Then **mandatory cleanup, same move:** `tmux kill-session -t df-worker-9` →
   next curl shows `df-worker-9` gone → `tmux ls 2>/dev/null | grep -c df-worker` → `0`
   (leftover df-worker sessions trip `warm_pool.py`'s safety/leftover checks and would block
   the next real engine run — this cleanup is non-negotiable).
   **Expect:** appear → observed → disappear, all three curls as stated.
   **Failure signal:** worker never appears (status.py `workers` didn't pick it up — tmux
   server namespace mismatch) or pane_tail null while live.
   **Counter-move:** run `tmux list-sessions` and Recon 2's status.py call side-by-side; if
   status.py sees it and your route doesn't, the bug is Move 3/4 (fix, re-run); if status.py
   itself doesn't see it → **Abort A2**. NEVER leave df-worker-9 alive while debugging —
   kill and respawn per attempt.
9. **Do:** Quality gates + ship: `cd $WT && npm run lint && npm run typecheck && npm test &&
   npm run build` all clean; stop any dev server YOU started (F3-A); commit watchtower —
   stage only your files (Recon 10 discipline) — message:
   `feat(agents): live agent view — GET /api/agents + Agents page (dark-factory wg-t5-03)`;
   `git push`. dark-factory repo: nothing to commit on the happy path (this ticket writes no
   DF files; abort/park files excepted).
   **Expect:** all four gates exit 0; push succeeds; `git -C $WT status --porcelain` empty
   (or only Recon-10 strangers, named in result notes).
   **Failure signal:** husky pre-commit rejects (lint/format), or push rejected (remote
   ahead — T5-01 follow-ups landing in parallel).
   **Counter-move:** `npm run format` then re-stage; push rejection → `git pull --rebase`
   and push; conflict in a file you touched → resolve keeping both intents; conflict in a
   file you did NOT touch → **Abort A3**.

## Forks

**F1 — Shape of T5-01's landing.**
Trigger: Recon 1/5/6 — what the charter+scaffold ticket actually built.
→ **Route A** (T5-01 established an engine seam and/or nav shell — a status route, a
`DARK_FACTORY_ROOT`-style env var, a pages/nav pattern): REUSE all of it — extend its service
with `--n-audit 200` if needed, mount `/api/agents` beside its route, add the Agents view as
its nav pattern dictates. Do not create parallel duplicates of anything it owns.
→ **Route B** (T5-01 landed charter/deploy but only a thin seam — no env var, or a
differently-shaped route): build Moves 1–7 exactly as written, conforming to the scaffold
idioms verified in Recon 5, and note the seam divergence in result notes.
(T5-01 not landed AT ALL is not a fork — that's **Abort A1**.)

**F2 — AngelEye alive vs dark at verify time.**
Trigger: Recon 7 / Move 5's live spike.
→ **Route A** (dark — the authoring-time state): `angeleye.available == false`, badge renders
"dark — revival is T6-04". This is the expected, fully-passing outcome.
→ **Route B** (alive — T6-04 landed first): `available == true`; v1 still reports
availability ONLY. Do not integrate its session feed — record "extension point: map audit
`session_id` → AngelEye session view once T6-04's API is ratified" in result notes.

**F3 — A Watchtower process is already listening.**
Trigger: Recon 8 finds a LISTEN on :5061/:5060.
→ **Route A** (nothing running — authoring state): start `npm run dev` yourself for Moves
6–8 verification; stop it in Move 9.
→ **Route B** (already running): do NOT kill or restart it (David/T5-01's deploy owns it).
Dev-mode instance → hot reload serves your changes, verify against it. Production-style
instance that won't pick up new code → verify on a temporary port
(`PORT=5071 CLIENT_URL=http://localhost:5070 npm run dev --workspace` equivalents per the
scaffold), note in results that the deployed instance needs a restart to expose
`/api/agents`, and leave that restart to David.

## Assumptions ledger

1. **T5-01's ticket id is `wg-t5-01-watchtower-charter-scaffold`.** The T5-01 war game was
   authored in parallel — the exact slug was not verifiable from this seat. Plausible: it is
   the spec-mandated `wg-<id>-<slug>` over the candidate title "Watchtower app charter +
   scaffold". If false: harmless — Recon 1 gates on T5-01's ARTIFACTS on disk, never on the
   ticket id; the promotion operator should reconcile the `depends_on` string when staging.
2. **AngelEye answers `GET /health` on `http://127.0.0.1:5051` when revived.** Verified in
   its scaffold source (`env.ts` PORT default 5051; AppyStack health route) but unverifiable
   live — it is dark at authoring. If a revived AngelEye answers differently (moved port,
   socket-only): the probe's availability-only contract makes this harmless — set
   `ANGELEYE_URL` in `.env` when known, note the drift in result notes. No park needed.
3. **5s polling (not socket.io push) is acceptable for v1.** Plausible: read-only view,
   matches the kanban (T5-02) idiom, and the scaffold's socket layer stays available for a
   later upgrade. Presentation-only; if David wants push at triage → one hook swap later.
4. **A 200-line `--n-audit` window suffices to attribute every `running/` ticket.** Plausible:
   `running/` holds 0–2 tickets in practice and each dispatch appends exactly one audit line.
   If a running ticket predates the window it lands in `unattributed_running` — honest
   degradation, not an error. No action needed beyond the lane existing.
5. **Free-standing park files in `engine/store/needs-decision/` are inert to the engine** —
   verified for this portfolio by T2-05's authoring recon (orchestrator only inspects tids of
   its own live agents). Same contract applies to this ticket's abort parks.

## Abort conditions

Every abort: write the park file, leave the ticket in `running/`, stop — never guess past it.

- **A1 — dependency not landed.** Recon 1 finds no watchtower repo, or the untouched 1-commit
  scaffold with no T5-01 artifacts. Park
  `$DF/engine/store/needs-decision/wg-t5-03-live-agent-view.json`:
  `{"ticket":"wg-t5-03-live-agent-view","question":"T5-03 dispatched but T5-01 (Watchtower charter+scaffold+first-deploy) has not landed — the repo is still the virgin scaffold. Build the agents view directly on the raw scaffold anyway, or hold for T5-01?","observed":"<git log line + grep result>","requested_by":"wg-t5-03 executor"}`.
- **A2 — engine contract shifted.** status.py `--json` crashes / lost `workers`, `running`,
  or `audit_tail` keys (Recon 2/4, Move 2), or `df-worker-*` naming is gone (Recon 3), or
  status.py cannot see a live tmux session (Move 8). Park with the exact command + output
  observed; the fix belongs in an engine ticket, not here.
- **A3 — seam conflict.** Recon 10 dirt in files this ticket touches, an env.ts
  unrecognizable vs Recon 5 after one conform attempt (Move 1), or a rebase conflict in a
  file you never touched (Move 9). Park with `git status`/conflict paths and the question
  "who owns this seam right now?".
- **A4 — cannot obtain a verifiable server.** `npm install` broken beyond one fix cycle
  (Recon 9), or Move 6's route failing for a second unexplained cycle. Park with the error
  output. Do NOT brew-install tooling, switch node versions, or bypass the scaffold to
  "just serve something".

## Verification

`DF=/Users/davidcruwys/dev/ad/apps/dark-factory`, `WT=/Users/davidcruwys/dev/ad/apps/watchtower`.
Requires a running dev server per Fork F3's route.

```bash
# 1. Route exists and the envelope + shape are exact
curl -s http://127.0.0.1:5061/api/agents | python3 -c "
import json,sys; r=json.load(sys.stdin)
assert r['status']=='ok', r
d=r['data']
assert sorted(d.keys())==['angeleye','factory','generated_at','unattributed_running','workers'], d.keys()
f=d['factory']
assert isinstance(f['queue_depth'],int) and isinstance(f['running_count'],int)
assert f['tmux'] in ('ok','none','absent')
assert isinstance(d['angeleye']['available'], bool)
print('shape-ok; tmux =', f['tmux'], '; angeleye =', d['angeleye']['available'])"

# 2. Counts agree with the authoritative aggregator (dynamic — no fixed numbers)
python3 - <<'EOF'
import json, subprocess
eng = json.loads(subprocess.run(["python3","/Users/davidcruwys/dev/ad/apps/dark-factory/engine/status.py","--json"],
                                capture_output=True, text=True).stdout)
api = json.loads(subprocess.run(["curl","-s","http://127.0.0.1:5061/api/agents"],
                                capture_output=True, text=True).stdout)["data"]
assert api["factory"]["queue_depth"]   == eng["queue"]["depth"],   "queue mismatch"
assert api["factory"]["running_count"] == eng["running"]["count"], "running mismatch"
print("counts-in-sync")
EOF

# 3. Live-worker round trip (the Move 8 proof, re-runnable) — WITH cleanup
tmux new-session -d -s df-worker-9 'echo WG-T5-03-PANE-PROOF; exec sleep 120'
sleep 2
curl -s http://127.0.0.1:5061/api/agents | python3 -c "
import json,sys; ws={w['name']:w for w in json.load(sys.stdin)['data']['workers']}
w=ws['df-worker-9']; assert w['live'] and w['state']=='idle', w
assert any('WG-T5-03-PANE-PROOF' in l for l in (w['pane_tail'] or [])), w['pane_tail']
print('live-worker-ok')"
tmux kill-session -t df-worker-9
sleep 2
curl -s http://127.0.0.1:5061/api/agents | python3 -c "
import json,sys; names=[w['name'] for w in json.load(sys.stdin)['data']['workers']]
assert 'df-worker-9' not in names, names; print('worker-gone-ok')"
tmux ls 2>/dev/null | grep -c df-worker            # → 0 (nothing left behind)

# 4. Fork-dependent AngelEye check — run the branch that applies:
#    F2-A (dark, expected): available == false and the badge text ships
curl -s http://127.0.0.1:5061/api/agents | jq -e '.data.angeleye.available == false' # F2-A
grep -rn "T6-04" $WT/client/src | head -1                                            # badge wired
#    F2-B (alive): jq -e '.data.angeleye.available == true' and result notes carry the
#    session-feed extension point.

# 5. Quality gates
cd $WT && npm run lint && npm run typecheck && npm test && npm run build

# 6. Negative checks — what must NOT have changed
grep -rc "send-keys" $WT/server/src | grep -v ":0" | wc -l          # → 0 (capture only)
git -C $DF status --porcelain | grep -v needs-decision | wc -l      # → 0 (no DF writes)
python3 $DF/engine/status.py > /dev/null && echo engine-status-ok   # engine untouched
curl -s http://127.0.0.1:5061/health | jq -r .status                # → ok (scaffold intact)
curl -s http://127.0.0.1:5061/api/info > /dev/null && echo info-ok  # T5-01/scaffold route intact
git -C $WT diff HEAD~1 --name-only | grep -c "client/package.json"  # → 0 (no new client deps)

# 7. Shipped
git -C $WT log --oneline -1        # the feat(agents) commit
git -C $WT status --porcelain      # empty (or named strangers per Recon 10)
```

## Executor notes (sonnet)

- **Scope fence.** Do NOT edit any `$DF/engine/*.py` file or anything under
  `$DF/engine/store/` (abort park files excepted). Do NOT build the kanban (T5-02), bus view
  (T5-04), curation queue (T5-05), HITL inbox (T5-06), or the API/MCP promotion (T5-12) —
  if you find yourself generalizing `/api/agents` into "the engine API layer", stop: that is
  T5-12's ticket. Do NOT attempt AngelEye revival (T6-04). Do NOT register Watchtower in
  locations.json/app-registry — that is T5-01's charter obligation.
- **The rabbit hole: live-streaming pane output.** The scaffold ships socket.io and the
  temptation is a websocket firehose of tmux panes. Poll-every-5s with a 15-line tail IS the
  v1 contract — resist. Same for xterm.js, ANSI-parsing pane content, or attach-in-browser
  ideas: out of scope, note them if you must, build none.
- **Second rabbit hole: re-deriving store logic in TypeScript.** If a number seems missing
  from `status.py --json`, the answer is NEVER "read audit.jsonl/queue/ from Node" — either
  compose what status.py already gives (it gives a lot — `--n-audit` is tunable) or note the
  gap as a status.py enhancement for an engine ticket. Q9: complement, don't replace.
- **tmux is read-only from this app, forever.** `capture-pane` and `list-sessions` only.
  A `send-keys` anywhere in Watchtower's server is a defect even if "convenient" — the
  engine's HITL gate owns worker input.
- **Style:** follow the scaffold's own idioms verified in Recon 5 (apiSuccess envelope, zod
  env, route/service/test triads, Tailwind utility classes); no new dependencies in either
  workspace; services are pure/mockable with I/O at the edges.
- **Prefer parking over guessing** on anything that smells like engine-contract drift (A2)
  or T5-01 seam ambiguity you can't resolve from disk in one read (A3). The empty cold
  factory is the common render state — if verification day has no workers running, that is
  a PASS with the fake-worker proof, not a reason to spawn real engine work.
