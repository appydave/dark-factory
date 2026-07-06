# T5-02 — Kanban board over the engine store

| field | value |
|---|---|
| ticket | wg-t5-02-kanban-board |
| track / size / priority | T5 Watchtower / M / normal |
| executor | sonnet Swagger via engine |
| depends_on | wg-t5-01-watchtower-charter-scaffold (id confirmed against T5-01's authored war game, same portfolio day; Recon 3 still checks the ARTIFACTS, not the id) |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

Give the Watchtower app (`~/dev/ad/apps/watchtower/`, AppyStack RVETS, client :5060 / server
:5061) its first real view: a **read-only kanban board** over the dark-factory engine store —
`engine/store/queue/`, `running/`, `done/` as three lanes, one card per ticket showing title,
ticket id, kind/priority badges, **age** (queue: since `requested_at`; running: since
`claimed_at`), **claimant** (`claimed_by`, written by `orchestrator.py lease()`), and **verdict**
(done lane: the normalized `result` — "done"/"unknown"/etc — plus notes). The engine seam is
`python3 engine/status.py --json` (the T5-01 charter's seam and the T5-12 doctrine's future API):
the Watchtower server spawns it and serves the report at `GET /api/board`; the client polls every
5s and renders lanes. One small **additive-only** extension to `status.py` puts the missing card
fields (kind, priority, executor, timestamps) into the JSON so the drift-tolerant store parsing
stays in exactly one place. v1 mutates NOTHING: no writes to the store, no POST routes, no
Socket.io push, no needs-decision lane. Done looks like: `/api/board` returns lane data matching
an `ls` of the store, the browser shows three lanes with correct cards, tests/typecheck/lint
green, both repos committed and pushed.

## Locked context

- **Q6 (decisions.md):** Watchtower is a **real web app** — this board lives in
  `~/dev/ad/apps/watchtower/`, NOT a Mochaccino static page and NOT
  `experiments/watchtower-board/`.
- **Q4 (decisions.md):** everything through the engine — written for sonnet Swagger dispatch.
- **No `-p`/headless/SDK ever; interactive `claude` only** — moot here (web app + one Python
  edit; nothing in this ticket spawns Claude).
- **No YLO/POEM work** — out of scope entirely.
- **Docs lag code** (wargame-spec) — e.g. watchtower's own CLAUDE.md says shared imports are
  `@appystack-template/shared` but the real package is `@appydave/shared` (verified in
  `shared/package.json` 2026-07-06). Trust the code; your Recon re-verifies at execution time.
- **ADR-0032:** `~/dev/ad/apps/watchtower/` is the durable Watchtower home;
  `experiments/watchtower-engine/` and `experiments/watchtower-board/` are disposable PoCs.
  Never build there, never port their code wholesale.
- **T5-09 killed** Board v6 Map view — do not resurrect map/graph ideas from the old :7430
  board into this ticket.
- **Watchtower CLAUDE.md dev-server rules:** if a dev server is already LISTENing on 5060/5061,
  it is UP — do not restart it, do not change ports.

## Recon (verify before any work)

Run every check. `WT=/Users/davidcruwys/dev/ad/apps/watchtower`,
`DF=/Users/davidcruwys/dev/ad/apps/dark-factory`.

1. `git -C $WT log --oneline | head -3` and `git -C $WT remote -v` → expect ≥1 commit (at
   authoring: exactly one, `1f4d5e9 Initial commit: Watchtower — human control surface…`) and
   remote `git@github.com:appydave/watchtower.git`. Directory missing or not a git repo →
   **Abort A2** (the T5-01 dependency did not deliver what its done-state claims).
2. Engine baseline, untouched:
   `cd $DF/engine && python3 status.py --json --n-done 3` → exit 0, valid JSON with top-level
   keys `generated_at, halt, backoff, queue, running, done, workers, audit_tail`; `queue.items[]`
   entries have `file, title, age_s`; `running.items[]` have `file, title, claimed_by,
   claimed_at`; `done.recent[]` have `file, title, result, notes` (all verified 2026-07-06).
   Also run plain `python3 status.py > /tmp/status-human-before.txt` and keep the file — Move 2's
   negative check diffs against it. Crash or missing keys → **Abort A1**.
3. T5-01 artifact discovery (this replaces trusting the depends_on id). T5-01's war game
   (authored same day, `backlog/wargames/T5-01-watchtower-charter-scaffold.md`) plans to land
   `server/src/routes/engine.ts` serving `GET /api/engine/status` (a status.py --json
   passthrough) plus a `DARK_FACTORY_ROOT` env var — but plans are not artifacts, so verify:
   `ls $WT/server/src/routes/` and `grep -rln "status.py\|engine\|DARK_FACTORY" $WT/server/src/` →
   - `engine.ts` (or any engine-status route) found: note its exact route path, spawn helper
     location, and env var name → **Fork F1 Route A**.
   - no hits (bare scaffold: only `health.ts`, `info.ts`, as at authoring) → **Fork F1 Route B**.
   Either way also `ls $WT/client/src/pages/` — if T5-01 added navigation/pages beyond
   `LandingPage.tsx`, slot the board into that structure instead of replacing the root (F1
   detail).
4. If a board already renders — `grep -rln "lane\|kanban\|BoardPage" $WT/client/src $WT/server/src`
   returns hits → someone landed this in a race → **Abort A2**.
5. Store ground truth (your later comparison baseline):
   `ls $DF/engine/store/queue/*.json 2>/dev/null | wc -l` /
   same for `running/` and `done/` → note the three numbers (at authoring: 1 / 0 / 17). Also
   confirm schema drift is real: `python3 -c "import json; d=json.load(open('$DF/engine/store/done/20260706T0930Z-orchestrator-kind-filter.json')); print(type(d['result']))"`
   → `<class 'dict'>` (dict-shaped result — the board must NOT assume a string; status.py's
   `done_outcome()` normalizes, which is why the seam is status.py and not raw file reads).
6. Rate limiter trap: `cat $WT/server/src/middleware/rateLimiter.ts` → expect
   `windowMs: 15 * 60 * 1000, limit: 100` (verified 2026-07-06). A 5s poll is 180 req/15min —
   it WILL 429 unless Move 4 mounts the board route before `apiLimiter` (or gives it its own
   limiter). If the limits have been raised past 200/15min, the special-casing is optional —
   note and simplify.
7. Ports: `lsof -i :5060 -i :5061 | grep LISTEN` → at authoring: nothing. If LISTENing, the dev
   server is already up — use it, don't restart (locked context).
8. Trap check: `git -C $DF ls-files apps/` → expect only `apps/watchtower/.gitignore`. The dir
   `$DF/apps/watchtower/` (inside dark-factory: `.env`, `.vscode`, `node_modules`, nothing else)
   is untracked leftover junk, NOT the app. Never build there.
9. `python3 --version` → ≥3.9 on PATH (3.14.5 at authoring; status.py is stdlib-only).
   `node --version` → ≥20 (RVETS needs it). Either missing → **Abort A1**.
10. Dirty-tree check: `git -C $WT status --porcelain` and
    `git -C $DF status --porcelain -- engine/status.py` → expect clean. Watchtower dirt →
    **Fork F2**. `status.py` dirty or mid-edit → **Abort A3**.

## Moves

1. **Do:** Baseline the scaffold. In `$WT`: `npm install` (node_modules is gitignored; a fresh
   clone has none), then `npm run typecheck && npm test && npm run lint`. Then start dev if not
   already up (Recon 7): `npm run dev` in the background (or `./scripts/start.sh` if Overmind is
   installed) and `curl -s http://localhost:5061/health`.
   **Expect:** all three quality gates exit 0 on the untouched scaffold; `/health` returns
   `{"status":"ok",...}` wrapped in the ApiResponse envelope.
   **Failure signal:** scaffold-red tests/typecheck before you changed anything, or the server
   won't boot.
   **Counter-move:** `npm run clean && npm install` once (stale node_modules is the usual
   culprit — the tracked tree is one commit old). Still red → **Abort A1** (broken baseline is
   not yours to fix under a board ticket).

2. **Do:** Additive-only extension to `$DF/engine/status.py` `build_report()` so cards have
   their fields. Exactly this, nothing else:
   - queue items: also emit `kind=data.get("kind")`, `priority=data.get("priority")`,
     `executor=data.get("executor")`, `requested_at=data.get("requested_at")`.
   - running items: same four fields, plus
     `age_s=(now - parse_iso(data.get("claimed_at"))).total_seconds() if parse_iso(data.get("claimed_at")) else None`
     (running age = time since claim; `parse_iso` already exists, line ~61).
   - done recent: also emit `created_at` — reuse
     `ticket_created_at(ticket, fname)` inside `done_outcome()` or compute in the loop by
     loading the ticket (it's already loaded inside `done_outcome`; simplest: have
     `done_outcome` return a 4-tuple adding created_at ISO-string-or-None, update its one call
     site).
   All new keys sit BESIDE existing ones; every existing key keeps its exact name and meaning
   (`--json` may already have consumers — agents per the file's own docstring).
   **Expect:** `python3 status.py --json --n-done 3` shows the new keys with sane values
   (`kind: "instruction"`, running age None-safe on the currently-empty lane);
   `python3 status.py > /tmp/status-human-after.txt && diff /tmp/status-human-before.txt /tmp/status-human-after.txt`
   → differences ONLY in `generated_at` and age numbers (time moved), no structural change to
   the human report.
   **Failure signal:** human diff shows new/changed lines beyond timestamps/ages, or `--json`
   crashes on any real store file.
   **Counter-move:** you renamed or restructured instead of appending — revert
   (`git -C $DF checkout -- engine/status.py`) and redo as pure addition. A store file that
   crashes the new code means you assumed a field: every lookup must be `.get()`-guarded like
   the surrounding code (the file's header documents real schema drift). Second revert-and-fail
   → **Abort A3**.

3. **Do:** Types + shared build. Append to `$WT/shared/src/types.ts` (package `@appydave/shared`
   — NOT the `@appystack-template/shared` the docs claim): interfaces mirroring the report —
   `BoardQueueItem { file: string; title: string; age_s: number | null; kind?: string | null; priority?: string | null; executor?: string | null; requested_at?: string | null }`,
   `BoardRunningItem` (same + `claimed_by`, `claimed_at`, `age_s`), `BoardDoneItem { file; title; result: string; notes?: string | null; created_at?: string | null }`,
   `BoardReport { generated_at: string; halt: Record<string, unknown> | null; backoff: Record<string, unknown> | null; queue: { depth: number; oldest_ticket: string | null; oldest_age_s: number | null; items: BoardQueueItem[] }; running: { count: number; items: BoardRunningItem[] }; done: { total: number; recent: BoardDoneItem[] }; workers: string[] | null }`.
   Keep every field optional/nullable where the store can drift. Then
   `npm run build --workspace shared` (server/client import the built package).
   **Expect:** shared builds clean; `npm run typecheck` still green.
   **Failure signal:** type errors in server/client from the new exports.
   **Counter-move:** new interfaces are additive exports — they cannot break existing imports
   unless you edited existing types; revert any such edit.

4. **Do:** Server seam. Three pieces, following the scaffold's own route idiom
   (`routes/info.ts` + `apiSuccess` helper + Zod env pattern):
   (a) `$WT/server/src/config/env.ts` — if T5-01 already added a dark-factory path var (its
   plan names it `DARK_FACTORY_ROOT` — Recon 3), REUSE it verbatim and skip this sub-move.
   Otherwise add to the Zod schema:
   `DARK_FACTORY_ROOT: z.string().default('/Users/davidcruwys/dev/ad/apps/dark-factory')`, and
   document it in `.env.example` (README "New environment variable" recipe). One var name for
   this seam across the app — never both `_ROOT` and `_DIR`.
   (b) `$WT/server/src/lib/engineStatus.ts` — one exported async function
   `fetchEngineStatus(): Promise<BoardReport>` that runs
   `execFile('python3', [join(env.DARK_FACTORY_ROOT, 'engine/status.py'), '--json', '--n-done', '200', '--n-audit', '0'], { timeout: 15000, maxBuffer: 10 * 1024 * 1024 })`
   (promisified) and `JSON.parse`s stdout (status.py resolves its own imports from its script
   dir — cwd doesn't matter, verified 2026-07-06). Isolated in lib/ so the route test can mock
   it. If T5-01's `engine.ts` already contains this spawn (F1 Route A), extract/reuse its code
   into this one lib function and have BOTH routes call it — one spawn implementation, ever.
   (c) `$WT/server/src/routes/board.ts` — `GET /api/board` calling `fetchEngineStatus()`,
   returning via `apiSuccess(res, report)`; on spawn/parse failure
   `throw new AppError(502, 'engine status unavailable: <message>')` (the scaffold's
   errorHandler formats it). Mount in `server/src/index.ts` **BEFORE**
   `app.use(apiLimiter)` (Recon 6: 100 req/15min would 429 a 5s poll) with a comment saying
   exactly that, and give boardRouter its own
   `rateLimit({ windowMs: 15 * 60 * 1000, limit: 1200 })` inside `board.ts` so it isn't
   unlimited.
   **Expect:** `curl -s http://localhost:5061/api/board | python3 -m json.tool` → ApiResponse
   envelope, `data.queue.depth` / `data.running.count` / `data.done.total` equal to Recon 5's
   three `ls` counts (re-run the `ls` now — the store moves; T2-03 will move the deferred queue
   ticket to done/ this same cycle).
   **Failure signal:** 502 (python3/path wrong), 429 (limiter order wrong), counts mismatch
   (wrong store — you pointed at a copy or the trap dir).
   **Counter-move:** run the exact execFile command by hand in a shell from
   `$DF/engine` to split "spawn broken" from "route broken". If `env.ts` refuses to boot after
   your schema edit, the default is malformed (Zod `.default()` on a `z.string()`, no
   `.coerce`). Persistent 429 → you mounted after the limiter; move the mount line.

5. **Do:** Server tests, scaffold-idiomatic (Vitest + Supertest, see
   `server/src/routes/info.test.ts` for the pattern). In
   `$WT/server/src/routes/board.test.ts`: mock `../lib/engineStatus.js` with
   `vi.mock`; test (a) 200-path — resolve a small fixture `BoardReport` (hand-write one queue
   item, one running item with `claimed_by: "mac-mini-pid123"`, one done item with
   `result: "done"`), assert `status: 'ok'` and the three lanes echo through; (b) 502-path —
   mock rejects, assert status 502 and `status: 'error'`.
   **Expect:** `npm test --workspace server` green, including the untouched scaffold tests.
   **Failure signal:** your route test passes but an existing test broke (you changed middleware
   order in a way that affected `info`/`health` tests).
   **Counter-move:** the board mount must be additive — a line above apiLimiter, no reordering
   of existing lines. Diff `index.ts` against git to confirm only additions.

6. **Do:** Client board. New files, existing Tailwind v4 setup, no new dependencies, no router:
   - `$WT/client/src/hooks/useBoard.ts` — `useEffect` + `setInterval(5000)` polling
     `fetch('/api/board')` (Vite proxy routes `/api` to :5061), storing
     `{ report, error, lastFetched }`; clear the interval on unmount; on fetch error keep the
     last good report and set the error flag (stale board beats blank board).
   - `$WT/client/src/pages/BoardPage.tsx` + small `Lane` and `TicketCard` components (same file
     or `client/src/components/` — follow the scaffold's placement pattern). Layout: header bar
     with app name, `generated_at`, a red `HALTED` badge if `halt != null`, an amber `BACKOFF`
     badge if `backoff != null`, worker count (`workers?.length ?? 'tmux n/a'`); below, a
     3-column grid (`grid grid-cols-1 md:grid-cols-3 gap-4`), one column per lane with heading
     `QUEUE (depth)` / `RUNNING (count)` / `DONE (total)`. Cards: title (2-line clamp), ticket
     `file` in mono small type, badges for `kind` and `priority` when present; queue card shows
     age (format `age_s` with a tiny humanize helper: s/m/h/d — mirror status.py's
     `human_age` thresholds); running card shows `claimed_by` + age-since-claim; done card
     shows a verdict badge (`result` — green for `done`, gray for `unknown`, red otherwise) and
     `notes` behind a native `<details>` (notes run to paragraphs — never inline the full
     text on the card face). Done lane renders `recent` newest-first (reverse the array — the
     store list is oldest-first) and a footer line `showing N of {total}` when `total >
     recent.length`. Error flag → a thin banner "engine unreachable — showing last snapshot
     from <lastFetched>".
   - Wire into `App.tsx`: replace `<LandingPage />` with `<BoardPage />` (keep the LandingPage
     file; keep the `DemoPage` dev-only line untouched) — UNLESS Recon 3 found T5-01 navigation,
     in which case add BoardPage as a page in that structure instead.
   **Expect:** browser at `http://localhost:5060` shows three lanes whose counts match the
   `curl` from Move 4; a card in the done lane shows a green `done` badge; the page updates
   without reload when the store changes (test: it re-fetches within 5s — watch `lastFetched`).
   **Failure signal:** blank page (check browser console — a null-field crash means a missing
   `?.` on a drifted ticket), CORS/proxy errors (you fetched `:5061` absolute instead of the
   relative `/api/board`), interval leak warnings in tests.
   **Counter-move:** every report field access goes through optional chaining with a rendered
   fallback (`'—'`); the fixture-vs-real gap is exactly the schema drift the store is documented
   to have. Proxy issues: use the relative path, the scaffold's `vite.config.ts` already routes
   it.
7. **Do:** Full-gate + live verification. `npm run typecheck && npm test && npm run lint` at the
   workspace root; then with the dev pair up, run the Verification block below end-to-end,
   including the read-only proof (store `ls` before/after several poll cycles → byte-identical
   file lists).
   **Expect:** everything in the Verification block holds.
   **Failure signal:** any check fails.
   **Counter-move:** fix and re-run the block; if a fix requires touching engine files beyond
   the Move-2 diff → **Abort A3**.

8. **Do:** Docs + commit + push, both repos (separate git repos — verified at authoring).
   Watchtower: append a `## The Board` section to `$WT/README.md` (what it shows, the
   `/api/board` route, the `DARK_FACTORY_ROOT` env var, read-only-v1 statement, pointer that
   lanes = `engine/store/{queue,running,done}` in dark-factory) and fill the CLAUDE.md
   "Additional Environment Variables" consumer slot with `DARK_FACTORY_ROOT`. Commit all new/
   changed watchtower files, message:
   `feat(board): read-only kanban over the dark-factory engine store (queue/running/done)`.
   dark-factory: commit ONLY `engine/status.py`, message:
   `feat(engine): status.py --json additive card fields (kind/priority/executor/ages) for Watchtower board`.
   Push both.
   **Expect:** both pushes succeed; `git status --porcelain` clean in watchtower; dark-factory
   clean of YOUR files (stage nothing else).
   **Failure signal:** push rejected (remote ahead).
   **Counter-move:** `git pull --rebase` then push; conflict in a file you touched → resolve
   keeping both intents; conflict in a file you did NOT touch → **Abort A4**.

## Forks

**F1 — what did T5-01 actually leave behind?** (Trigger: Recon 3.)
→ **Route A** (an engine-status route already exists in watchtower — T5-01's plan:
`routes/engine.ts`, `GET /api/engine/status`, env `DARK_FACTORY_ROOT`): do NOT add a parallel
duplicate seam. Refactor its spawn into the single `lib/engineStatus.ts` function (Move 4b),
keep `/api/engine/status` working as-is (its consumers may exist), add `/api/board` calling the
same function with `--n-done 200`, and make sure Move 2's new fields flow through the
passthrough. Moves 4a/4b become "reuse + extract"; Move 4c (limiter ordering for a 5s poll)
still applies — T5-01's route was built for occasional loads, not polling.
→ **Route A′** (T5-01 landed AND its page already renders the raw report): the board replaces
that minimal page as the richer view — keep the raw page reachable if T5-01's charter named it,
otherwise BoardPage supersedes it; say which you did in the result notes.
→ **Route B** (bare scaffold, no engine seam anywhere — the authoring-time state): build Moves
4a–c exactly as written. This war game is deliberately self-sufficient: T5-01's charter/scaffold
matters, its status-serving deliverable is nice-to-reuse but not required.

**F2 — watchtower tree dirty.** (Trigger: Recon 10 shows uncommitted changes.)
→ **Route A** (dirt in files this ticket never touches — e.g. T5-01 charter docs, other pages):
proceed; stage only your files at Move 8; mention the stranger's dirt in the result notes.
→ **Route B** (dirt in `server/src/index.ts`, `env.ts`, `shared/src/types.ts`, or anything
route/board-shaped): someone is mid-change on your exact seam → **Abort A3**.

**F3 — the engine already speaks HTTP.** (Trigger: during Recon you find a live engine API — a
T5-12-style server, e.g. something LISTENing that serves the status report over HTTP, or
`$DF/engine/` has grown an api/server module that documents itself as the stable seam.)
→ **Route A** (no such API — authoring-time state): spawn status.py per Move 4.
→ **Route B** (a real engine HTTP API exists and serves the report): `fetchEngineStatus()`
becomes an HTTP fetch to it instead of an execFile spawn (config: `ENGINE_API_URL` env var
replacing/augmenting `DARK_FACTORY_ROOT`); everything downstream is unchanged. Do not build both
paths; pick by what exists.

## Assumptions ledger

1. **T5-01 will have executed before this ticket dispatches.** Its ticket id
   (`wg-t5-01-watchtower-charter-scaffold`) was confirmed against its authored war game
   (same portfolio day), and depends_on gates dispatch — but a manual run or a promotion-order
   slip could still land this ticket first. **If false** (Recon 3 finds a bare scaffold with no
   T5-01 charter/route artifacts AND no done-ticket for wg-t5-01 in `engine/store/done/`): the
   war game is self-sufficient via F1 Route B — proceed if the scaffold repo itself exists
   (Recon 1); only a missing repo is fatal (**Abort A2**). Note the ordering anomaly in the
   result.
2. **Editing `engine/status.py` is in-scope for a Watchtower ticket.** Plausible: status.py IS
   the declared engine seam (its own docstring: "machine-readable JSON (for agents)"), the
   change is additive-only with a byte-level negative check on human output, and T5-12 later
   promotes this exact seam to a stable API — putting card fields anywhere else would fork the
   store-parsing logic into TypeScript. **If false** (David or a concurrent engine ticket
   objects, or Recon 10 finds status.py mid-edit): fall back to shipping the board with the
   fields status.py already emits (title/age/claimant/verdict all survive; kind/priority badges
   render `—`), note the degradation, and park the status.py extension as a question in
   `engine/store/needs-decision/wg-t5-02-kanban-board.json`.
3. **status.py's BACKOFF auto-clear side effect is acceptable under polling.** `build_report()`
   calls `is_backoff()`, which deletes an EXPIRED `engine/store/BACKOFF` flag file — so the
   "read-only" board indirectly performs the engine's own housekeeping unlink every 5s poll.
   Plausible: that is the engine's designed expiry semantics; the orchestrator does the same;
   an expired flag is semantically already-cleared. **If false** (David wants the board to have
   zero write side effects of any kind): park to needs-decision with the proposal "add
   `--no-side-effects` flag to status.py"; do not hand-roll a side-effect-free parser in
   TypeScript.
4. **Polling (5s fetch) is acceptable for v1; no Socket.io push.** Plausible: the store is plain
   files with no change feed; live push is the Live-bus-view ticket's territory (T5-04), and the
   scaffold's Socket.io stays idle but wired for it. **If false**: the seam (`fetchEngineStatus`
   + `BoardReport` type) is push-agnostic; a later ticket swaps the transport. No action now.
5. **Replacing `<LandingPage />` as the root view is acceptable.** Plausible: LandingPage is
   scaffold TODO-content, and the board is the app's first real feature; F1 handles the case
   where T5-01 built navigation. **If false** (David wants the landing page kept as front door):
   5-minute change — render both or add a trivial toggle; note it, don't park.
6. **The store's lane counts at verification time won't match authoring-time counts** (1/0/17).
   Certain, not just plausible — the store is live and T2-03 explicitly moves the one queued
   ticket to done/. That is why every count check compares board-vs-`ls` at the same moment,
   never board-vs-this-document.

## Abort conditions

- **A1 — broken baseline.** Recon 2's untouched status.py crashes, Recon 9's runtimes are
  missing, or Move 1's untouched scaffold fails its own gates after one clean reinstall. Park:
  write `engine/store/needs-decision/wg-t5-02-kanban-board.json` with
  `{"ticket": "wg-t5-02-kanban-board", "question": "baseline broken before any board work: <which — status.py | scaffold | runtime> — fix under a separate ticket or debug here?", "observed": "<the failing command + output>"}`.
  Leave this ticket in `running/`. Never build a view on a broken seam.
- **A2 — dependency did not deliver, or the work already landed (race).** Recon 1 finds no
  watchtower repo (T5-01 claimed done but the artifact is absent), or Recon 4 finds a board
  already rendering. Park with question: "wg-t5-02 found <missing scaffold | an existing board
  at …> — re-run T5-01 first / verify-and-close against the existing board / redo per the war
  game?" Do not duplicate or overwrite whatever exists.
- **A3 — seam conflict.** Recon 10 or Fork F2 Route B (concurrent edits on status.py or the
  watchtower server seam), Move 2 failing twice to stay additive, or any fix demanding engine
  changes beyond the Move-2 diff (orchestrator.py, wake.py, halt.py, warm_pool.py, the store
  itself). Park with the git evidence and the question "who owns this seam right now?".
- **A4 — rebase conflict in a file this ticket never touched.** Park with the conflicting
  paths; do not resolve other people's conflicts.

## Verification

```bash
WT=/Users/davidcruwys/dev/ad/apps/watchtower
DF=/Users/davidcruwys/dev/ad/apps/dark-factory

# 0. quality gates, whole workspace
cd $WT && npm run typecheck && npm test && npm run lint && echo GATES-OK

# 1. status.py extension is additive and alive
cd $DF/engine && python3 status.py --json --n-done 5 | python3 -c "
import json,sys; r=json.load(sys.stdin)
assert set(['generated_at','halt','backoff','queue','running','done','workers']) <= set(r)
for it in r['queue']['items']: assert 'kind' in it and 'priority' in it and 'requested_at' in it
for it in r['done']['recent']: assert 'result' in it and 'created_at' in it
print('status-json ok — queue', r['queue']['depth'], 'running', r['running']['count'], 'done', r['done']['total'])"
python3 status.py | head -20                                   # human report still renders, same shape as before

# 2. /api/board serves the report (dev server up on :5061)
curl -s http://localhost:5061/api/board | python3 -c "
import json,sys; r=json.load(sys.stdin)
assert r['status']=='ok'; d=r['data']
print('board ok —', d['queue']['depth'], d['running']['count'], d['done']['total'])"

# 3. board counts == store ls counts, same moment
echo "store: $(ls $DF/engine/store/queue/*.json 2>/dev/null | wc -l | tr -d ' ')/$(ls $DF/engine/store/running/*.json 2>/dev/null | wc -l | tr -d ' ')/$(ls $DF/engine/store/done/*.json 2>/dev/null | wc -l | tr -d ' ')"
# ^ must equal the three numbers from check 2 (queue/running/done)

# 4. poll survives the rate limiter: 30 rapid hits, zero 429s
for i in $(seq 1 30); do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5061/api/board; done | sort | uniq -c
# → 30× 200, no 429

# 5. client renders (dev server up on :5060) — title + lanes present in served HTML/JS
curl -s http://localhost:5060/ | grep -ci "watchtower"          # ≥1 (shell smoke; real check is the browser)
# browser check (manual or playwright): three lane headings QUEUE/RUNNING/DONE with counts,
# a done card showing a 'done' verdict badge, ticket ids in mono type

# 6. READ-ONLY proof — polling changes nothing in the store
ls $DF/engine/store/queue $DF/engine/store/running $DF/engine/store/done > /tmp/store-before.txt
sleep 12   # ≥2 poll cycles while the board is open
ls $DF/engine/store/queue $DF/engine/store/running $DF/engine/store/done > /tmp/store-after.txt
diff /tmp/store-before.txt /tmp/store-after.txt && echo STORE-UNTOUCHED   # empty diff (unless the engine itself moved a ticket — re-run to confirm it wasn't the board)

# 7. negative checks — what must NOT have changed
git -C $DF diff --stat HEAD~1 -- engine/ | grep -v status.py | grep -c "\.py"   # → 0 (only status.py touched in engine)
git -C $DF status --porcelain -- engine/store/ | wc -l                          # → 0 store dirt from this ticket
ls $WT/server/src/routes/health.ts $WT/server/src/routes/info.ts               # scaffold routes intact
grep -c "app.use(apiLimiter)" $WT/server/src/index.ts                           # → 1 (limiter still applied, board mounted above it)
grep -rc "POST\|\.post(" $WT/server/src/routes/board.ts                         # → 0 (read-only: GET only)

# 8. both repos committed and pushed
git -C $WT status --porcelain | wc -l            # → 0
git -C $WT log --oneline -1                      # the feat(board) commit
git -C $DF log --oneline -1 -- engine/status.py  # the feat(engine) additive commit
```

## Executor notes (sonnet)

- **Scope fence.** Read-only v1 means: NO POST/PUT/DELETE routes, NO writes into
  `$DF/engine/store/` from watchtower ever, NO needs-decision lane (that's T5-06 HITL inbox),
  NO live agent/tmux view (T5-03), NO bus/events view (T5-04), NO curation actions (T5-05), NO
  Socket.io push wiring (leave the scaffold's socket code untouched and idle). In dark-factory,
  touch `engine/status.py` ONLY — never orchestrator.py, wake.py, halt.py, warm_pool.py, or any
  store file. Never write into `$DF/apps/watchtower/` (untracked junk dir, Recon 8's trap).
- **The rabbit hole: `$DF/docs/watchtower/` + `experiments/watchtower-board/`.** Sixteen spec
  files (symphony-spec, schemas, Board v6 plans) and an old working board from the :7430 era.
  Reading them will tempt you into map views, device panels, and event-log renderers. Skip them
  entirely — ADR-0032 makes them disposable PoC history, T5-09 killed the Map view, and this
  ticket is exactly three lanes over `status.py --json`.
- **Do not run `/mochaccino` or any design-interview skill** despite watchtower's CLAUDE.md
  suggesting it for UI choices: the layout here is fully specified (header + 3-column grid +
  cards), and this run is unattended. Visual taste passes come later via the census loop. Style
  minimally with the existing Tailwind setup; clean/neutral beats branded-and-wrong.
- **Schema drift is the enemy of a pretty demo.** The store's tickets genuinely vary
  (`result` as string vs dict, missing `requested_at`, `question` instead of `title` on
  external-research tickets). status.py normalizes; your client must still `?.` every field and
  render `—` rather than crash. If a real store file breaks the board, the fix is a guard, never
  a store edit.
- **Dev-server discipline (watchtower CLAUDE.md):** if :5060/:5061 are already LISTENing, use
  the running pair; never kill, never change ports.
- **Prefer parking over guessing** on any A2/A3 signal — T5-01, T5-03, T5-06, and T5-12 all
  orbit this same app and seam this cycle; half-landed neighbour work means park, not merge by
  guess.
