# T5-01 — Watchtower app charter + scaffold

| field | value |
|---|---|
| ticket | wg-t5-01-watchtower-charter-scaffold |
| track / size / priority | T5 Watchtower / M / high |
| executor | sonnet Swagger via engine |
| depends_on | none |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Turn Watchtower from a design-doc pile + 1-commit stub into a chartered, running web app whose
first deploy serves the engine's own truth. Three deliverables: **(a)** a charter doc
(`docs/watchtower/charter-2026-07.md` in dark-factory) that specs the app per Q6 — the four
views (kanban, live agent, bus, curation queue), the API seams, and exactly what it reads —
superseding the census-era v0 spec; **(b)** the scaffold finished, not re-created — authoring
recon found `~/dev/ad/apps/watchtower/` ALREADY scaffolded on AppyStack RVETS (1 commit,
2026-06-11: React 19 + Vite on the client, Express 5 + Socket.io on the server, shared TS,
Zod, Pino) but never installed, never ported correctly (scaffold defaults 5060/5061, which
Chrome blocks as ERR_UNSAFE_PORT; apps.json allocated 5080/5081), and never registered;
**(c)** first deploy: `GET /api/engine/status` shells out to dark-factory's
`engine/status.py --json` and returns it, a minimal client page renders it, both proven live
with curl, then shut down cleanly. Done looks like: charter committed, app boots on 5080/5081,
the status endpoint returns real queue/running/done/halt/backoff data, the app is registered
(apps.json fixed, locations.json + ad/CLAUDE.md entries added), both repos pushed. This ticket
does NOT build the kanban/bus/curation views — the charter specs them as follow-on T5 tickets.

## Locked context

- **Q6 (decisions.md):** Watchtower is a **real web app** — kanban, live agent view, bus view,
  curation queue. Not terminal + static Mochaccino boards.
- **Q4 (decisions.md):** everything through the engine — this ticket is written for sonnet
  Swagger dispatch.
- **No `-p`/headless/SDK ever; interactive `claude` only** — Watchtower never spawns Claude in
  any form; it shells out to *Python* (status.py), which is fine. The charter must state this.
- **No YLO/POEM work** — out of scope entirely.
- **Docs lag code** (wargame-spec) — `docs/watchtower/` is 16 files of mostly-superseded v0
  thinking (census-era 4-screen app, shell-out-to-workflow trigger). The charter supersedes;
  the Recon below re-verifies disk state at execution time.
- **Watchtower doctrine (RE-BUCKETING.md, ratified 2026-06-06, still binding):** Watchtower is
  the Control Plane of a three-plane model (Factory Floor = dark-factory engine, Communication
  Bus = Switchboard, Control Plane = Watchtower); records-never-mutates; decision-queue-not-
  dashboard; ≤5 Today cards; no screen renders >50 records.
- **Standing rule (register-every-new-app):** apps register at birth — locations.json,
  ad/CLAUDE.md, app-registry, constellation. Watchtower is in the registry/constellation but
  NOT in locations.json or ad/CLAUDE.md; this ticket closes that gap.

## Recon (verify before any work)

All paths absolute. Repos: dark-factory = `/Users/davidcruwys/dev/ad/apps/dark-factory` (DF),
watchtower = `/Users/davidcruwys/dev/ad/apps/watchtower` (WT).

1. `git -C /Users/davidcruwys/dev/ad/apps/watchtower log --oneline | wc -l` → expect `1`
   (commit `1f4d5e9` "Initial commit: Watchtower — human control surface over Dark Factory").
   More commits → **Fork F1**. Directory missing entirely → **Abort A2** (the stub was
   moved/deleted under you — do NOT re-scaffold on your own authority).
2. `git -C /Users/davidcruwys/dev/ad/apps/watchtower status --porcelain` → expect empty.
   Dirty → **Fork F1**.
3. `ls /Users/davidcruwys/dev/ad/apps/watchtower/node_modules 2>/dev/null | head -1; ls /Users/davidcruwys/dev/ad/apps/watchtower/.env 2>/dev/null`
   → expect BOTH absent (never installed, never configured — verified 2026-07-06). Either
   present → someone worked here since → **Fork F1**.
4. Engine baseline:
   `python3 /Users/davidcruwys/dev/ad/apps/dark-factory/engine/status.py --json | python3 -c "import json,sys; d=json.load(sys.stdin); print(sorted(d.keys()))"`
   → expect exit 0 and keys including `generated_at`, `halt`, `backoff`, `queue`, `running`,
   `done` (verified working from an arbitrary cwd 2026-07-06 — status.py resolves its own
   paths via `from orchestrator import Q, RUN, DONE...`). Crash/non-zero → **Abort A1**.
5. Ports: `lsof -nP -iTCP:5080 -iTCP:5081 -sTCP:LISTEN` → expect no output (free, verified
   2026-07-06). Occupied → **Fork F2**. Also confirm the allocation is still watchtower's:
   `python3 -c "import json; print(json.load(open('/Users/davidcruwys/.config/appydave/apps.json'))['apps']['watchtower']['ports'])"`
   → expect `{'client': 5080, 'server': 5081}`. Different ports listed → use THOSE instead of
   5080/5081 everywhere below (the registry is authoritative); key missing → **Abort A4**.
6. Toolchain: `node --version && npm --version` → expect node ≥ 20 (v25.8.0 at authoring),
   npm ≥ 10 (11.11.0 at authoring). Missing → **Abort A2**.
7. Charter home: `ls /Users/davidcruwys/dev/ad/apps/dark-factory/docs/watchtower/` → expect
   ~16 files incl. `plan.md`, `spec.md`, `RE-BUCKETING.md`. If the dir is gone or emptied to
   an `_archive/` shape, the RE-BUCKETING physical moves were executed since authoring —
   write the charter to the surviving `docs/watchtower/` (or its renamed successor named in
   `docs/INDEX.md`) instead; same filename.
8. Registration state:
   `python3 /Users/davidcruwys/dev/ad/apps/app-registry/query.py app watchtower` → expect a
   record with `"verdict_status": "stub"`, `"locations_key": null`, `"apps_json_key": "watchtower"`.
   `grep -c watchtower /Users/davidcruwys/.config/appydave/locations.json` → expect `0`.
   If locations.json already has a watchtower entry → skip that half of Move 7, note it.
9. Race check: `ls /Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/running/` → expect
   no other ticket mentioning watchtower. If one exists → **Abort A3**.
10. Stale-record confirmation (feeds Move 7):
   `python3 -c "import json; a=json.load(open('/Users/davidcruwys/.config/appydave/apps.json'))['apps']['watchtower']; print(a['path'], a['url'])"`
   → expect the KNOWN-STALE values `~/dev/ad/apps/dark-factory/apps/watchtower` and
   `http://localhost:5060` (both wrong as of 2026-07-06 — the repo lives at
   `~/dev/ad/apps/watchtower` and 5060 is Chrome-unsafe). If already fixed, skip that half of
   Move 7.

## Moves

1. **Do:** Write the charter: `/Users/davidcruwys/dev/ad/apps/dark-factory/docs/watchtower/charter-2026-07.md`
   (location per Recon 7). Terse, tables over prose, David's voice. Required sections, in order:
   - **Header block**: date, "supersedes `spec.md`/`plan.md` v0 (census-era); doctrine from
     `RE-BUCKETING.md` carried forward"; ruling Q6 quoted from `plans/wargames/decisions.md`.
   - **Identity**: the three-plane table (Factory Floor = dark-factory engine · Communication
     Bus = Switchboard, an AppySentinel instance at `~/dev/ad/apps/switchboard` · Control
     Plane = Watchtower, this AppyStack app at `~/dev/ad/apps/watchtower`).
   - **What it reads** (all read-only): `engine/store/queue/`, `running/`, `done/`,
     `results/`, `needs-decision/`, `audit.jsonl`, HALT/BACKOFF flags, `engine/store/events/`
     — today aggregated by `engine/status.py --json`, later pushed by Switchboard.
   - **The four views (Q6)**, one row each — purpose / data source / seam / ships in:
     **Kanban** (tickets queue→running→done→needs-decision; seam 1; ticket T5-03) ·
     **Live agent view** (which tmux workers are running what, from audit.jsonl + running/;
     seam 1 extended or seam 2; T5-03) · **Bus view** (event stream; engine/store/events/ now,
     Switchboard SSE when live; seam 3; T5-04) · **Curation queue** (needs-decision/ cards
     with promote/reject; seam 4, the ONLY write seam, HITL-gated; T5-02).
   - **API seams**: 1 = shell-out `python3 <DF>/engine/status.py --json` (built this ticket);
     2 = direct read-only JSON reads of `engine/store/**` (when a view needs more than
     status.py aggregates); 3 = Switchboard SSE/socket subscribe (future — do not build);
     4 = decision write-back, LIMITED to answering `needs-decision/` items (future — do not
     build).
   - **Doctrine**: read-only v1; never mutates `engine/store/` or `canonical/`; ≤5 decision
     cards on the landing surface; no screen renders >50 records; NEVER spawns `claude` in any
     form (no `-p`, no SDK — it is a window, not a worker).
   - **v0.1 slice (this ticket)**: one status page over seam 1.
   - **Run**: ports 5080 (client) / 5081 (server) — 5060/5061 are Chrome ERR_UNSAFE_PORT,
     which is why apps.json moved the allocation; `npm run dev` from the repo root.
   - **Non-goals**: auth, multi-user, deployment beyond localhost, spawning work, Mochaccino
     replacement (design exploration stays in Mochaccino).
   - **Open questions**: (i) reconcile the two decision-queue concepts — curation-at-rest
     (needs-decision/) vs mid-task HITL — flagged, NOT resolved here; (ii) constellation marks
     watchtower `build_target: kbde-extension` — recorded as "standalone AppyStack app now,
     KBDE mount later; not a contradiction"; (iii) Switchboard SSE availability gates T5-04.
   - **Follow-on tickets**: T5-02 curation queue · T5-03 kanban + live agent views · T5-04 bus
     view / SSE · decision-queue reconciliation.
   **Expect:** file exists; contains all section headings above;
   `grep -c "5080" <charter>` ≥ 1; `grep -ci "read-only" <charter>` ≥ 1.
   **Failure signal:** you are copying screens/phases from the old `spec.md`/`plan.md`
   (Today/Experiments/Runs, census batches, shell-out-to-workflow trigger) — those are the
   superseded v0.
   **Counter-move:** re-read only `RE-BUCKETING.md`'s "What STAYS true" + "SUPERSEDES" lists;
   rewrite the offending section from Q6 + the seams above, not from the legacy docs.

2. **Do:** Install + baseline the scaffold:
   `cd /Users/davidcruwys/dev/ad/apps/watchtower && npm install && npm run typecheck && npm test`.
   **Expect:** all three exit 0 (npm workspaces: shared, server, client; tests are Vitest and
   pass out of the box on the untouched scaffold).
   **Failure signal:** install errors (peer deps, husky `prepare` hook, network) or red tests
   on the UNTOUCHED scaffold.
   **Counter-move:** retry `npm install` once (transient network); if the `prepare`/husky hook
   is the failure, `npm install --ignore-scripts` then proceed (hooks are lint garnish, not
   build). If typecheck/test still fail on the untouched scaffold after that → **Abort A2**.

3. **Do:** Align ports to the registered allocation (5080 client / 5081 server, per Recon 5):
   (a) `client/vite.config.ts`: `port: 5060` → `5080`; all three proxy targets
   `http://localhost:5061` → `http://localhost:5081`.
   (b) Create `.env` at the WT repo root (env.ts loads `../.env` relative to `server/`, i.e.
   the repo root — verified) by copying `.env.example` and setting `PORT=5081`,
   `CLIENT_URL=http://localhost:5080`, `VITE_SOCKET_URL=http://localhost:5081`.
   (c) Update `.env.example` to the same three values (the example must stop advertising
   Chrome-unsafe ports).
   (d) Sweep the rest: `grep -rn "506[01]" /Users/davidcruwys/dev/ad/apps/watchtower --exclude-dir=node_modules --exclude=package-lock.json`
   and update every live config/doc hit (README port table + quick-start, `server/src/config/env.ts`
   zod defaults, docker-compose/Procfile/CLAUDE.md if they name ports).
   **Expect:** the grep in (d) returns zero hits afterwards (excluding package-lock.json);
   `npm run typecheck` still exits 0.
   **Failure signal:** leftover 5060/5061 references, or the client later boots on 5060 anyway.
   **Counter-move:** re-run the sweep grep and fix stragglers; `strictPort: true` is already
   set in vite.config.ts, so a wrong port fails loudly rather than sliding — read the boot log.

4. **Do:** Build seam 1 on the server.
   (a) `server/src/config/env.ts`: add to the zod schema
   `DARK_FACTORY_ROOT: z.string().default('/Users/davidcruwys/dev/ad/apps/dark-factory')`
   and add `DARK_FACTORY_ROOT=/Users/davidcruwys/dev/ad/apps/dark-factory` to `.env` +
   `.env.example`.
   (b) New file `server/src/routes/engine.ts` (mirror the shape of `routes/info.ts`): router
   with `GET /api/engine/status` → `execFile('python3', [join(env.DARK_FACTORY_ROOT, 'engine/status.py'), '--json'], { timeout: 15000 })`
   (promisified) → `JSON.parse(stdout)` → `apiSuccess(res, parsed)` (the standard helper wraps
   it as `{status:'ok', data, timestamp}`). Pass the engine JSON through VERBATIM as `data` —
   do NOT re-shape or cherry-pick fields; status.py's shape has drifted before and the
   passthrough must survive that. On spawn/parse failure: `apiFailure(res, 'engine status unavailable: <message>', 502)`.
   (c) Register in `server/src/index.ts`: `import engineRouter from './routes/engine.js';` +
   `app.use(engineRouter);` next to `infoRouter`.
   (d) Test file `server/src/routes/engine.test.ts` mirroring `health.test.ts` / `info.test.ts`
   (supertest against the exported app) — but **mock `node:child_process`'s execFile**
   (`vi.mock`) to return a canned `{"queue":{"depth":0}}` payload: the GitHub CI workflow
   (`.github/workflows/ci.yml`) runs `npm test` on a runner that has NO dark-factory checkout,
   so a real-spawn test would break CI. Assert 200 + `body.data.queue` present, and the 502
   path when the mock errors.
   **Expect:** `npm run typecheck` and `npm test` exit 0 including the new test.
   **Failure signal:** ESM mocking friction (`vi.mock` of node builtins) or type errors on the
   promisified execFile.
   **Counter-move:** follow the existing test files' import style exactly (this scaffold is
   ESM, `type: module`, imports end `.js`); for the mock, `vi.mock('node:child_process')` with
   a factory, or refactor the route to accept an injectable runner function (default = real
   execFile) and unit-test via injection — the injectable-runner refactor is the reliable path
   if `vi.mock` fights you for more than two attempts.

5. **Do:** Build the client status page. Replace the demo content of `client/src/App.tsx` with
   a single status view: `fetch('/api/engine/status')` on mount + every 5s (setInterval,
   cleared on unmount); render from `data`: (i) a banner row — red if `halt` non-null, amber if
   `backoff` non-null, green "ENGINE OK" otherwise; (ii) `generated_at`; (iii) QUEUE section:
   `queue.depth` + one line per `queue.items[]` (title, age); (iv) RUNNING section:
   `running.count` + items; (v) DONE section: `done.total` + up to 5 of `done.recent[]`
   (title, result); (vi) a plain error state when the fetch or the API fails ("engine
   unreachable — is dark-factory at DARK_FACTORY_ROOT?"). Defensive access throughout
   (`data?.queue?.items ?? []`) — the passthrough contract means shape can drift. Tailwind
   utility classes only, no new deps, no chart libs, one file (plus updating
   `client/src/App.test.tsx` so `npm test` stays green — mock fetch, assert the QUEUE heading
   renders).
   **Expect:** `npm run typecheck` + `npm test` exit 0; `npm run build` exits 0.
   **Failure signal:** App.test.tsx still asserting the old demo content; build errors.
   **Counter-move:** update the test to the new markup (it is scaffold garnish, not sacred);
   if the Tailwind v4 setup fights a class, drop to inline style — this page's job is truth,
   not beauty.

6. **Do:** First deploy — boot, prove, shut down:
   `cd /Users/davidcruwys/dev/ad/apps/watchtower && nohup npm run dev > /tmp/watchtower-dev.log 2>&1 &`
   then poll up to 60s for readiness (`curl -sf http://localhost:5081/health`). Prove all four:
   (i) `curl -s http://localhost:5081/health` → `{"status":"ok",...}`;
   (ii) `curl -s http://localhost:5081/api/engine/status | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['status']=='ok' and 'queue' in d['data'] and 'depth' in d['data']['queue']; print('seam1 ok, queue depth', d['data']['queue']['depth'])"`;
   (iii) `curl -s http://localhost:5080/ | grep -ci "<div id=\"root\"" ` → ≥1 (client up);
   (iv) `curl -s http://localhost:5080/api/engine/status | grep -c '"queue"'` → ≥1 (Vite proxy
   path works — this is the URL the page actually uses).
   Then STOP it: `lsof -ti:5080,5081 | xargs kill` and confirm
   `lsof -nP -iTCP:5080 -iTCP:5081 -sTCP:LISTEN` is empty. The app is started on demand by
   David (`npm run dev`), not left running and not daemonized — record the start command in
   the README, leave nothing listening.
   **Expect:** all four curls pass; ports quiet afterwards; `/tmp/watchtower-dev.log` free of
   stack traces.
   **Failure signal:** readiness never comes (read the log: EADDRINUSE → **Fork F2**; zod env
   validation exit → your `.env` edit broke parsing; `python3: not found` or ENOENT from the
   route → PATH issue in the spawned env).
   **Counter-move:** for the python ENOENT case, change the route to spawn
   `/usr/bin/env python3 …` or the absolute interpreter (`which python3` to find it), re-test,
   keep the fix. For zod failures, diff `.env` against env.ts's schema keys. Two consecutive
   failed boot cycles after fixes → **Abort A2**, attaching the log tail.

7. **Do:** Register the app (standing rule; Recon 8/10 found the gaps):
   (a) `~/.config/appydave/apps.json` → `apps.watchtower`: `path` →
   `"~/dev/ad/apps/watchtower"`, `url` → `"http://localhost:5080"`, `status` →
   `"building"`; keep ports/notes as-is (append to notes: "repo moved to sibling apps/watchtower;
   first deploy 2026-07 (wg-t5-01)"). Preserve every other key byte-identical.
   (b) `~/.config/appydave/locations.json` → append to the `locations` array (list schema —
   match the sibling entries' shape exactly):
   `{"key": "watchtower", "path": "/Users/davidcruwys/dev/ad/apps/watchtower", "jump": "japp-watchtower", "brand": "appydave", "type": "product", "tags": ["dark-factory", "control-plane", "decision-queue", "dashboard"], "description": "Watchtower - Dark Factory control plane (kanban, agents, bus, curation)"}`.
   Validate both files after editing: `python3 -m json.tool <file> > /dev/null`.
   (c) `~/dev/ad/CLAUDE.md`: add `/apps/watchtower/          → Watchtower — Dark Factory control plane (AppyStack)`
   to the Micro Apps block, and `japp-watchtower` to the shell-alias line that lists
   `japp-angeleye/deckhand/...`. Additive edits only.
   (d) Refresh the registry: `python3 /Users/davidcruwys/dev/ad/apps/app-registry/probe.py`
   then `python3 /Users/davidcruwys/dev/ad/apps/app-registry/query.py app watchtower` — if
   probe.py errors, do NOT debug it; its launchd pulse refreshes on schedule — note the skip.
   **Expect:** both JSON files parse; query.py (post-probe) shows `locations_key` non-null;
   CLAUDE.md diff is 2 added lines.
   **Failure signal:** JSON parse error, or probe output shows watchtower duplicated.
   **Counter-move:** fix the JSON by hand (trailing comma is the usual culprit); duplication
   means locations key ≠ registry id — set the location `key` to exactly `watchtower`.

8. **Do:** Docs + commit + push, three repos, each scoped to its own files:
   (a) WT `README.md`: add an "Engine status seam" section (what `/api/engine/status` does,
   `DARK_FACTORY_ROOT` env var, pointer to the charter at
   `~/dev/ad/apps/dark-factory/docs/watchtower/charter-2026-07.md`) — port table already
   updated in Move 3. Commit ALL watchtower changes:
   `feat(app): first deploy — engine status seam on 5080/5081, charter pointer` → push.
   (b) dark-factory: commit the charter (+ this war game's ticket movement is the engine's
   job, not yours): `docs(watchtower): charter 2026-07 — Q6 real web app, four views, seams` →
   push.
   (c) `~/dev/ad` (the monorepo, a separate repo that CONTAINS both as embedded repos): commit
   ONLY `CLAUDE.md`: `docs: register watchtower in micro-apps + jump aliases` → push.
   (d) `~/.config/appydave`: check `git -C ~/.config/appydave rev-parse --git-dir 2>/dev/null`
   — if it IS a repo, commit the two JSON edits; if not, the file edits stand alone (note
   which in the result).
   **Expect:** `git status --porcelain` clean in WT; dark-factory shows only expected
   war-game/engine churn from other tickets; all pushes exit 0.
   **Failure signal:** push rejected (remote ahead), or you are about to commit files you
   never touched.
   **Counter-move:** `git pull --rebase` then push; a conflict in a file you touched →
   resolve keeping both intents; a conflict in a file you did NOT touch → **Abort A5**.

## Forks

**F1 — the scaffold moved since authoring (2026-07-06).**
Trigger: Recon 1–3 finds extra commits, a dirty tree, node_modules, or a `.env` already
present.
→ **Route A** (drift is additive/unrelated — docs, renames, config not on this ticket's seam):
proceed; adapt file paths/line references to what you find; note the drift in the result.
→ **Route B** (the seam itself landed — `grep -rn "engine/status" WT/server/src/` hits, or a
status page already renders): do NOT duplicate. Run this war game's **Verification** block
against the existing implementation; if it passes, skip Moves 2–6, do only Moves 1, 7, 8
(charter + registration + docs are still owed) and report "seam pre-existed, verified". If it
half-passes → **Abort A3**.

**F2 — ports 5080/5081 occupied at execution time.**
Trigger: Recon 5's lsof shows a listener, or Move 6 hits EADDRINUSE.
→ **Route A** (the holder is a stale watchtower/node process — `lsof -nP -iTCP:5080 -iTCP:5081 -sTCP:LISTEN`
shows node with cwd under apps/watchtower, e.g. a crashed earlier dev run): kill those PIDs,
confirm ports free, proceed.
→ **Route B** (another app holds them, or apps.json now assigns 5080/5081 to something else):
do NOT squat and do NOT pick your own ports — port allocation is David's registry decision →
**Abort A4**.

## Assumptions ledger

1. **The existing 2026-06-11 scaffold IS the "scaffold RVETS/AppyStack" deliverable** — finish
   it, never run `create-appystack` again over it. Plausible: it is a faithful AppyStack
   output, matches the stack Q6 implies, and context.md's fixed input #2 mandated exactly this
   scaffold. **If false** (David's triage note demands a fresh scaffold or different stack):
   park to `needs-decision/` before Move 2 — re-scaffolding destroys a committed repo.
2. **apps.json's 5080/5081 allocation is authoritative** (its own note records the move off
   Chrome-unsafe 5060/5061). **If false** (allocation changed/removed at execution): Recon 5
   already routes this — use the registry's current ports or **Abort A4**.
3. **Q6 "real web app" coexists with constellation's `build_target: kbde-extension`** —
   standalone AppyStack app now, mountable in the KBDE iframe harness later; the charter
   records this reading rather than resolving it. **If false** (David rules KBDE-first):
   charter edit + note; no code in this ticket is invalidated (a web app is what KBDE mounts).
4. **The charter lives in dark-factory (`docs/watchtower/`), not the app repo** — the factory
   owns specs, the app gets a pointer; consistent with RE-BUCKETING keeping control-plane docs
   there. **If false**: it is one `git mv` later; note the open question in the result.
5. **"First deploy" = proven-live-then-stopped on localhost**, started on demand by David; no
   launchd/daemon/always-on. Plausible: global rule "don't spin up a server he means to run
   himself"; nothing in Q6 asks for always-on. **If false** (David wants it resident): that is
   a follow-on ops ticket, not a reopen of this one — say so in the result notes.
6. **`japp-watchtower` as the jump alias** (matches the `japp-*` micro-app pattern in
   ad/CLAUDE.md). **If false**: rename is a 2-line edit; David's naming wins.

## Abort conditions

Park action for ALL aborts: write
`/Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/needs-decision/wg-t5-01-watchtower-charter-scaffold.json`
containing `{"ticket": "wg-t5-01-watchtower-charter-scaffold", "question": "<the specific question>", "observed": "<evidence: command + output>"}`;
leave the engine ticket in `running/`; never guess past an abort.

- **A1 — engine baseline broken.** Recon 4's untouched `status.py --json` crashes. Question:
  "status.py is broken before Watchtower touches anything — fix the engine first (own ticket)
  or proceed with the charter-only subset?" Never build a window onto a broken wall.
- **A2 — scaffold or toolchain broken beyond counter-moves.** Recon 1's missing directory,
  Recon 6's missing node/npm, Move 2's persistent install/test failures, or Move 6's two
  failed boot cycles. Question: "watchtower scaffold unbuildable as found — re-scaffold
  (destructive), repair (which?), or park the app?" + the log tail.
- **A3 — race on the seam.** Recon 9's concurrent watchtower ticket, or Fork F1 Route B's
  half-working pre-existing implementation. Question: "someone else is mid-build on
  watchtower's status seam — who owns it; verify-and-close or redo?"
- **A4 — port allocation conflict.** Recon 5 / Fork F2 Route B. Question: "5080/5081 no longer
  cleanly watchtower's — which ports does Watchtower own?" (Include the lsof/apps.json
  evidence.)
- **A5 — rebase conflict in a file this ticket never touched.** Park with the conflicting
  paths; do not resolve other people's conflicts.

## Verification

```bash
DF=/Users/davidcruwys/dev/ad/apps/dark-factory
WT=/Users/davidcruwys/dev/ad/apps/watchtower

# 1. Charter exists with the required spine
ls $DF/docs/watchtower/charter-2026-07.md
grep -c  "## "            $DF/docs/watchtower/charter-2026-07.md   # → ≥ 8 (sections)
grep -ci "kanban"         $DF/docs/watchtower/charter-2026-07.md   # → ≥ 1
grep -ci "curation"       $DF/docs/watchtower/charter-2026-07.md   # → ≥ 1
grep -ci "read-only"      $DF/docs/watchtower/charter-2026-07.md   # → ≥ 1
grep -c  "5080"           $DF/docs/watchtower/charter-2026-07.md   # → ≥ 1

# 2. Scaffold healthy, ports aligned, seam code present
cd $WT && npm run typecheck && npm test && npm run build            # all exit 0
grep -rn "506[01]" $WT --exclude-dir=node_modules --exclude=package-lock.json | wc -l   # → 0
grep -c "DARK_FACTORY_ROOT" $WT/server/src/config/env.ts            # → ≥ 1
ls $WT/server/src/routes/engine.ts $WT/server/src/routes/engine.test.ts

# 3. First deploy proves live, then leaves nothing running
cd $WT && nohup npm run dev > /tmp/wt-verify.log 2>&1 &
for i in $(seq 1 30); do curl -sf http://localhost:5081/health >/dev/null && break; sleep 2; done
curl -s http://localhost:5081/health | grep -c '"status":"ok"'      # → 1
curl -s http://localhost:5081/api/engine/status | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['status']=='ok' and 'depth' in d['data']['queue']; print('seam1 ok, depth', d['data']['queue']['depth'])"
curl -s http://localhost:5080/ | grep -c 'id="root"'                 # → ≥ 1
curl -s http://localhost:5080/api/engine/status | grep -c '"queue"'  # → ≥ 1 (proxy path)
lsof -ti:5080,5081 | xargs kill; sleep 1
lsof -nP -iTCP:5080 -iTCP:5081 -sTCP:LISTEN | wc -l                  # → 0 (nothing left running)

# 4. Registered
python3 -c "import json; a=json.load(open('/Users/davidcruwys/.config/appydave/apps.json'))['apps']['watchtower']; assert 'dark-factory' not in a['path'] and a['url'].endswith(':5080'); print('apps.json ok')"
python3 -c "import json; L=json.load(open('/Users/davidcruwys/.config/appydave/locations.json'))['locations']; w=[l for l in L if l.get('key')=='watchtower']; assert len(w)==1; print('locations ok', w[0]['jump'])"
grep -c "apps/watchtower" /Users/davidcruwys/dev/ad/CLAUDE.md        # → ≥ 1

# 5. Committed and pushed
git -C $WT status --porcelain | wc -l                                # → 0
git -C $WT log --oneline -1                                          # the first-deploy commit
git -C $DF log --oneline -- docs/watchtower/charter-2026-07.md | head -1   # the charter commit

# 6. Negative checks — what must NOT have changed
git -C $DF status --porcelain -- engine/ | wc -l    # → 0 (engine code + store untouched by this ticket)
ls $DF/engine/store/needs-decision/ | wc -l          # → 0 on success (no park written)
git -C $DF status --porcelain -- research/ | wc -l   # → 0 (frozen corpus untouched)
pgrep -fl "claude .*-p" | grep -v grep | wc -l       # → 0 (nothing headless was ever spawned)
```

## Executor notes (sonnet)

- **Scope fence.** Build ONLY the status slice (seam 1 + one page). Do NOT build the kanban,
  live-agent, bus, or curation views — the charter specs them; T5-02/03/04 build them. Do NOT
  write to `engine/store/` anything except a needs-decision park on abort. Do NOT touch
  `~/dev/ad/apps/switchboard/`, `engine/*.py`, or `research/`. Do NOT execute
  RE-BUCKETING.md's physical doc moves (a separate T8-flavoured decision). Do NOT run
  `create-appystack`, add auth, add Socket.io features, set up launchd, or leave any process
  listening when you finish. No `claude -p`, no headless, no SDK — anywhere, ever.
- **The rabbit hole: `docs/watchtower/`'s 16 legacy files.** `spec.md`, `plan.md`,
  `schemas.md`, `symphony-spec.md` etc. describe the census-era v0 app (Today/Experiments/Runs
  screens, experiment/run/learning/promotion records, shell-out-to-workflow triggers). Reading
  them will tempt you to implement four record schemas and a trigger button. Do not. Read only
  `RE-BUCKETING.md` (the supersession map) for the charter; the engine store IS the data
  model now.
- **Passthrough is the contract.** The server route and the client page treat status.py's JSON
  as opaque-but-shaped: pass it through, access defensively. status.py's own header says the
  ticket schema has drifted across the store's lifetime — hard-coding today's shape is how
  this app dies in a month.
- **Style:** charter in David's voice — terse, tables, trigger-only phrasing, no marketing
  prose. Client page: truth over beauty, Tailwind utilities, zero new dependencies. Server:
  mirror the scaffold's existing route/test idiom exactly (ESM, `.js` import suffixes,
  `apiSuccess`/`apiFailure` helpers).
- **Prefer parking over guessing** on anything touching David's registries (ports, apps.json,
  locations.json keys) — those are his naming/allocation decisions; the war game gives you the
  recorded values, and any divergence you find is a question, not an invitation.
