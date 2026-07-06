# T5-06 — HITL inbox UI

| field | value |
|---|---|
| ticket | wg-t5-06-hitl-inbox-ui |
| track / size / priority | T5 Watchtower / M / normal |
| executor | sonnet Swagger via engine |
| depends_on | wg-t5-01-watchtower-app-scaffold · wg-t5-07-decision-queue-reconcile |
| authored | 2026-07-06, Fable war-game portfolio |

## Mission

The engine's mid-task HITL gate already works as files: a gated worker writes
`engine/store/needs-decision/<tid>.json` and blocks; a human answers by writing
`engine/store/decisions/<tid>.json`; the orchestrator resumes the worker
(`engine/orchestrator.py`, gate block ~lines 599–632). Today the only "UI" is a `[HITL]`
log line telling the human to run an `echo` command. Give the gate a surface: a **HITL
Inbox** page in the Watchtower app (`~/dev/ad/apps/watchtower` — the durable home per
ADR-0032) that lists every unanswered needs-decision item as a card with
**approve / decline / redirect** forms, and writes the decision file **atomically**
through a new server API. Done = `GET /api/hitl` + `POST /api/hitl/:ticket/decision`
with tests, a `HitlInbox` client page polling it, one synthetic round-trip proven
against the real store (then cleaned up), and both repos left clean and committed.

## Locked context

- decisions.md Q6: Watchtower is a **real web app** — this ships in the AppyStack RVETS
  app at `~/dev/ad/apps/watchtower`, not a Mochaccino board and not a status.py flag.
- decisions.md Q4: everything through the engine — this ticket itself arrives via
  sonnet-Swagger dispatch; the work is app code, no engine runs required.
- Two decision queues, one name (the T5-07 problem): this ticket is the **mid-task HITL
  gate** surface (`engine/store/needs-decision/` ↔ `decisions/`). It is NOT the curation
  queue (canonical promotion → promotion.yml, `docs/watchtower/spec.md` — that's T5-05).
  Do not blend them.
- Write discipline: the UI writes **only** `engine/store/decisions/<tid>.json` — never
  queue/, running/, done/, results/, needs-decision/, never engine code, and it never
  spawns sessions (intake law). Reading is unrestricted.
- Assessment-mode: engine defects observed along the way (e.g. corrupt-decision =>
  silent approve) are findings to note in the commit message / report line, not patches.
- Interactive `claude` only, no `-p`/SDK/API-key anywhere (standing law; not exercised
  here anyway — this ticket runs no engine).

## Recon (verify before any work)

Paths repo-relative to `~/dev/ad/apps/dark-factory` unless absolute. All facts below
were true at authoring (2026-07-06); re-verify each.

1. **The app home.** `ls ~/dev/ad/apps/watchtower/package.json server client shared`
   (from that dir) → AppyStack workspace app, name `@appydave/watchtower`, "Human control
   surface over Dark Factory workflows — a decision queue", remote
   `git@github.com:appydave/watchtower.git`. **Missing or not this shape** → Abort A1.
   ⚠️ Trap: `~/dev/ad/apps/dark-factory/apps/watchtower/` also exists but is a husk
   (node_modules + .env only, gitignored). Never build there — ADR-0032
   (`docs/kdd/decisions/0032-*.md`) names the standalone repo as the durable home.
2. **T5-01's landed shape.** `git -C ~/dev/ad/apps/watchtower log --oneline` → at
   authoring only `1f4d5e9 Initial commit`. If T5-01 landed since (expected — it's a
   dependency): look for an engine-store reader (`grep -ril "engine/store\|DF_ENGINE_STORE\|status.py" ~/dev/ad/apps/watchtower/server/src/`)
   and client navigation (`grep -n "router\|Route" ~/dev/ad/apps/watchtower/client/src/App.tsx`).
   Findings drive Fork F1 (reader) and Fork F2 (navigation).
3. **The gate contract is unchanged.** In `engine/orchestrator.py`:
   `grep -n 'needs-decision\|resume_prompt\|HITL_TIMEOUT' engine/orchestrator.py` →
   NEEDS/DEC dirs (~line 57), gated task_prompt writing
   `{"ticket","question","proposed","note"}` (~248–255), decision consumption
   (~615–626) reading `{"action","note","choice"}` where corrupt JSON **silently
   defaults to approve** (~617–619), `resume_prompt` (~263–274: `decline` → ABORTED;
   any other action resumes, `choice` passed as the specific direction),
   `HITL_TIMEOUT=1800` (~line 70). **Idiom renamed/removed** → Abort A2. Line drift
   without semantic change → adjust and proceed.
4. **The pending/answered convention.** `ls engine/store/needs-decision/ engine/store/decisions/`
   → at authoring both empty (.gitkeep only). Convention (already used by T2-05's
   briefing feed and the T1-01 abort protocol): an item is **pending** iff
   `needs-decision/<name>.json` exists with **no same-named twin** in `decisions/`;
   answered iff both exist; the engine never deletes either. Also: not every
   needs-decision file is a live gate — war-game aborts park free-standing questions
   here (name = war-game ticket id, no twin in `running/`). The UI must render both.
5. **status.py has no HITL section.** `python3 engine/status.py --json | grep -c decision`
   → 0 at authoring (verified by running it). If a `needs_decision`/`hitl` block now
   exists, prefer consuming shapes consistent with it, but the API in M4 is still built
   (Watchtower reads the store, not status.py, for this seam — unless F1 Route A says
   otherwise).
6. **T5-07's vocabulary note.** Search for it:
   `grep -ril "curation\|HITL" docs/watchtower/ backlog/wargames/proof/T5-07/ 2>/dev/null`
   and check `backlog/wargames/T5-07-*.md` for its declared output path. If the note
   exists, adopt its names for the page title / labels verbatim. If it contradicts this
   war game's split (mid-task gate ≠ curation queue) → Abort A4. Not found → proceed
   with the names used here (dependency may have been reordered; note it in the commit).
7. **Ports.** `lsof -nP -i :5060 -i :5061 | head` → free at authoring. Occupied → the
   M7 proof uses `PORT=5911` (and client proxy is irrelevant — proof is curl-only).
8. **Real pending items right now?** `ls engine/store/needs-decision/*.json 2>/dev/null`
   minus same-named files in `decisions/` → drives Fork F3. **Never** POST a decision
   for any real pending ticket during this build.

## Moves

### M1 — Baseline the app

- **Do:** `cd ~/dev/ad/apps/watchtower && npm install && npm run typecheck && npm test`.
- **Expect:** install completes; typecheck clean; vitest suites (server + client) pass —
  the scaffold shipped green.
- **Failure signal:** install/typecheck/test failures before you've changed anything.
- **Counter-move:** one retry after `npm run clean && npm install` (clean script exists
  in root package.json). Still failing → the baseline is broken upstream of this ticket
  → Abort A3. Never "fix forward" scaffold breakage inside this ticket.

### M2 — Pin the gate contract as shared types

- **Do:** in `~/dev/ad/apps/watchtower/shared/src/types.ts` add (and export from
  `shared/src/index.ts`, mirroring how `ServerInfo` is exported):

  ```ts
  /** Worker-written request: engine/store/needs-decision/<ticket>. Shape set by
   *  orchestrator.py task_prompt (gated) — do not add required fields. */
  export interface HitlRequest {
    ticket: string;        // exact filename incl. .json — the join key across dirs
    question: string;
    proposed?: string;
    note?: string;
  }
  /** Human decision: engine/store/decisions/<ticket>. action 'decline' aborts the
   *  worker; any other action resumes it, with 'choice' as the direction. */
  export interface HitlDecision {
    action: 'approve' | 'decline' | 'redirect';
    note?: string;
    choice?: string;       // required when action === 'redirect'
    decided_at?: string;   // extra fields are safe: the engine reads only action/note/choice
    decided_via?: string;
  }
  export interface HitlItem {
    ticket: string;
    kind: 'gate' | 'parked';         // gate: same-named ticket file in running/; parked: free-standing question
    request: HitlRequest;
    requestedAt: string;             // needs-decision file mtime, ISO-8601
    ageSeconds: number;
    decision?: HitlDecision;         // present iff answered
  }
  export interface HitlInboxResponse { pending: HitlItem[]; answered: HitlItem[] }
  ```
- **Expect:** `npm run typecheck` still clean; `npm run build -w shared` succeeds.
- **Failure signal:** type errors or export collisions.
- **Counter-move:** rename only your additions to avoid collisions (e.g. an existing
  `HitlItem` from T5-01 — if one exists, reuse it instead per Fork F1 Route A).

### M3 — Server: store path env + reader module

- **Do:**
  1. Add `DF_ENGINE_STORE` to the Zod schema in
     `~/dev/ad/apps/watchtower/server/src/config/env.ts`:
     `DF_ENGINE_STORE: z.string().default('/Users/davidcruwys/dev/ad/apps/dark-factory/engine/store')`
     and add the same line (with the default value) to the root `.env.example` (and
     `.env` if present).
  2. Fork F1 decides Route A (reuse T5-01's reader) or Route B (build one). Route B:
     create `~/dev/ad/apps/watchtower/server/src/lib/hitlStore.ts` — pure Node `fs`
     functions, **read path resolved at call time** (`process.env.DF_ENGINE_STORE ?? env.DF_ENGINE_STORE`)
     so tests can point it at a fixture dir:
     - `listInbox(): HitlInboxResponse` — read `needs-decision/*.json`; for each, parse
       (unparseable → include with `question: '<unparseable JSON>'`, never throw), stat
       mtime → `requestedAt`/`ageSeconds`, `kind = 'gate'` iff `running/<same name>`
       exists else `'parked'`, `decision` = parsed `decisions/<same name>` if present.
       Pending sorted oldest-first.
     - `writeDecision(ticket, decision): void` — **atomic**: write to
       `decisions/.tmp-<ticket>` in the SAME directory, then `fs.renameSync` to
       `decisions/<ticket>`. Non-negotiable: the engine polls every 3s and a
       half-written file parses as corrupt JSON, which silently APPROVES
       (orchestrator.py ~617–619, Recon 3).
- **Expect:** `npm run typecheck` clean.
- **Failure signal:** module resolution errors (workspace import paths).
- **Counter-move:** mirror the import style of `server/src/routes/info.ts`
  (`@appydave/shared` for types, relative `.js`-suffixed paths for local modules).

### M4 — Server: GET /api/hitl (+ tests)

- **Do:** create `~/dev/ad/apps/watchtower/server/src/routes/hitl.ts` mirroring
  `routes/info.ts` (Router, `apiSuccess` from `helpers/response.js`, `AppError` for
  errors): `GET /api/hitl` → `apiSuccess(res, listInbox())`. Mount in
  `server/src/index.ts` beside the existing routers: `app.use(hitlRouter);`.
  Tests in `server/src/routes/hitl.test.ts` mirroring `info.test.ts`'s harness: build a
  fixture store in a temp dir (`fs.mkdtempSync`) with `needs-decision/`, `decisions/`,
  `running/` subdirs; set `process.env.DF_ENGINE_STORE` to it in `beforeEach`. Cases:
  (a) empty store → `{pending: [], answered: []}`; (b) request without twin → pending,
  `kind: 'parked'`; (c) request + same-named running/ file → `kind: 'gate'`;
  (d) request + decision twin → answered with the decision embedded; (e) unparseable
  request file → still listed, never a 500.
- **Expect:** `npm test -w server` green including the new cases.
- **Failure signal:** env var read at import time (tests see the default path, not the
  fixture) — the classic trap.
- **Counter-move:** confirm `hitlStore.ts` resolves the path per-call (M3 requirement),
  not at module top level; fix there, not in the tests.

### M5 — Server: POST /api/hitl/:ticket/decision (+ guards + tests)

- **Do:** in the same router. Order of guards, each its own failing test:
  1. **Name guard** (400): `:ticket` must match `/^[A-Za-z0-9._@-]+\.json$/` AND
     `path.basename(ticket) === ticket` — no traversal, no writing outside `decisions/`.
  2. **Body guard** (400): Zod — `action` ∈ approve|decline|redirect; `note` optional
     string; `choice` required non-empty iff `action === 'redirect'` (a redirect
     without a direction resumes the worker with nothing — the engine treats any
     non-decline action as "proceed", Recon 3).
  3. **Exists guard** (404): `needs-decision/<ticket>` must exist — you can only answer
     a question that was asked.
  4. **Immutability guard** (409): `decisions/<ticket>` must NOT already exist —
     decisions are write-once from this surface; never overwrite (a second writer may
     be the CLI `echo` the engine's own log line suggests). 409 body says who wins:
     "decision already recorded".
  5. Pass → `writeDecision(ticket, {...body, decided_at: new Date().toISOString(), decided_via: 'watchtower-hitl-inbox'})`,
     respond with the written `HitlDecision`.
- **Expect:** `npm test -w server` green: one test per guard + happy-path tests for all
  three actions asserting the file lands in the fixture `decisions/` with exact content
  and that no `.tmp-*` file remains.
- **Failure signal:** any guard test passes vacuously (route not mounted → 404 for the
  wrong reason).
- **Counter-move:** assert response bodies, not just status codes; check the mount line
  in `index.ts` landed (M4).

### M6 — Client: HitlInbox page

- **Do:** create `~/dev/ad/apps/watchtower/client/src/pages/HitlInbox.tsx`. Data: poll
  `GET /api/hitl` every 5s — copy the fetch/poll pattern from
  `client/src/hooks/useServerStatus.ts` into a `useHitlInbox` hook (same file or
  `client/src/hooks/useHitlInbox.ts`). Render:
  - **Pending** (oldest first): one card per item — `question` prominent, `proposed`
    and `note` beneath, ticket filename + `kind` badge (gate/parked) + age. Three
    buttons: Approve / Redirect / Decline. Redirect expands a **required** textarea
    ("direction the worker must follow" → `choice`); all three expose an optional note
    field. Decline requires a confirm click ("Decline aborts the waiting worker —
    confirm") — it is the only destructive action. Submit → POST; on 409 show
    "already answered elsewhere" and refresh; on 400 show the validation message.
  - **Answered**: read-only list — ticket, action taken, `decided_at`, note/choice.
  - **Empty state**: "No decisions waiting."
  - Age honesty: a `gate` item older than 30 min has outlived the engine's
    HITL_TIMEOUT (1800s, Recon 3) — badge it "worker likely timed out; answer may go
    unread" rather than pretending the resume is guaranteed.
  Mounting: Fork F2 — Route A (T5-01 landed a router/nav): add a `/hitl` route + nav
  entry "HITL Inbox". Route B (no router — authoring-time state: `App.tsx` renders
  `<LandingPage />` directly): render `<HitlInbox />` in `App.tsx` below
  `<LandingPage />`. Client tests: one render test with mocked fetch covering pending
  card + empty state (mirror `App.test.tsx`'s harness).
- **Expect:** `npm test` (both workspaces) green; `npm run typecheck` clean.
- **Failure signal:** proxy misses (client dev server proxies `/api` to :5061 — only in
  dev; tests must mock fetch, never hit the network).
- **Counter-move:** if the poll hook is flaky under vitest fake timers, drop timer
  testing — assert a single fetch+render cycle only. Do not build Socket.io push, an
  fs.watcher, or optimistic UI to "fix" a test (rabbit hole — see Executor notes).

### M7 — Live synthetic round-trip against the real store

- **Do:** Fork F3 first (real pending items → Route B). Then:
  1. Start the server only:
     `cd ~/dev/ad/apps/watchtower && npm run build -w shared && nohup npm run dev -w server > /tmp/wg-t5-06-server.log 2>&1 &`
     (add `PORT=5911` before `npm` if Recon 7 found :5061 busy; use that port in the
     curls below). Poll `curl -s localhost:5061/health` until ok (≤60s).
  2. Plant a synthetic request (unique name — never a real ticket's):
     `printf '%s\n' '{"ticket":"wg-t5-06-demo-gate.json","question":"Approve this approach?","proposed":"demo plan — synthetic","note":"planted by wg-t5-06 M7; safe to delete"}' > ~/dev/ad/apps/dark-factory/engine/store/needs-decision/wg-t5-06-demo-gate.json`
  3. `curl -s localhost:5061/api/hitl` → the item appears in `pending`, `kind:"parked"`
     (no running/ twin), correct question.
  4. Negative probes: POST with `action:"redirect"` and no `choice` → 400. POST to a
     name with `../` in it → 400. POST to `wg-t5-06-never-asked.json` → 404.
  5. `curl -s -X POST localhost:5061/api/hitl/wg-t5-06-demo-gate.json/decision -H 'Content-Type: application/json' -d '{"action":"approve","note":"wg-t5-06 M7 round-trip"}'`
     → 200; `cat ~/dev/ad/apps/dark-factory/engine/store/decisions/wg-t5-06-demo-gate.json`
     → valid JSON containing action/note/decided_at/decided_via; repeat the same POST →
     409; GET → item now in `answered`, gone from `pending`.
  6. Clean up: kill the background server;
     `rm ~/dev/ad/apps/dark-factory/engine/store/needs-decision/wg-t5-06-demo-gate.json ~/dev/ad/apps/dark-factory/engine/store/decisions/wg-t5-06-demo-gate.json`;
     `git -C ~/dev/ad/apps/dark-factory status --short engine/store/` → no wg-t5-06
     entries (files were untracked; removal restores clean).
- **Expect:** every curl above returns exactly the listed status; store clean after.
- **Failure signal:** server boots but GET 404s (mount missed), or the decision file is
  written somewhere else (path resolution bug — check `DF_ENGINE_STORE` in the root
  `.env` didn't override to the fixture path).
- **Counter-move:** fix, re-run M7 from step 2 (idempotent: the planted file is recreated).
  If the same step fails twice for a different reason each time, stop → Abort A3.
  Whatever happens, step 6's cleanup ALWAYS runs before leaving this move.

### M8 — Commit both sides, report findings

- **Do:**
  1. Watchtower repo: `git add` the new/changed files; commit
     `feat(hitl): HITL inbox — approve/decline/redirect surface over the engine's mid-task gate (wg-t5-06)`;
     `git push origin main` (remote `origin` verified at authoring; if push is rejected,
     commit locally and note it — never force-push).
  2. Update `~/dev/ad/apps/watchtower/README.md`: add the two endpoints to an "API"
     line/section and one sentence on what the HITL inbox is (mid-task gate, NOT the
     curation queue).
  3. Findings line (in the commit body, not a patch): "engine treats a corrupt
     decisions/ file as approve (orchestrator.py ~617–619) — this surface mitigates via
     atomic rename; CLI echo writers remain exposed."
  4. Dark-factory repo: confirm untouched — `git -C ~/dev/ad/apps/dark-factory status --short`
     shows nothing from this ticket (the results self-report to `engine/store/results/`
     is written by the engine-protocol wrapper, not by these moves).
- **Expect:** watchtower `git status` clean, commit on origin/main; dark-factory clean.
- **Failure signal:** stray files (fixture temp dirs, `/tmp` logs are fine; anything
  inside either repo is not).
- **Counter-move:** `git status --short` both repos, remove strays you created; anything
  you did NOT create → leave it, mention it in the results notes.

## Forks

**F1 — Did T5-01 land an engine-store reader / API seam?**
Trigger: Recon 2's grep of `server/src/` for an existing store reader.
→ **Route A** (reader or `/api/state`-style seam exists): reuse it — extend, don't
duplicate: add the hitl listing to the existing module/route family, keep this war
game's response shapes. If it already exposes needs-decision data, M4 becomes "extend +
conform" rather than "create".
→ **Route B** (bare scaffold, authoring-time state): build `hitlStore.ts` per M3,
scoped to the three dirs this ticket needs (needs-decision/, decisions/, running/) —
do NOT build a general store-reader framework on T5-01's behalf.

**F2 — Client navigation.**
Trigger: Recon 2's grep of `App.tsx` for a router.
→ **Route A** (router/nav exists): register `/hitl` + nav entry, follow the existing
page-registration pattern exactly.
→ **Route B** (no router): mount `<HitlInbox />` directly in `App.tsx`. Do not add
react-router yourself — that's T5-01/T5-02 surface architecture, not yours.

**F3 — Real pending HITL items exist at proof time.**
Trigger: Recon 8 finds unanswered real items (a live gated worker, or parked war-game
questions from other tickets).
→ **Route A** (store quiet): run M7 in full.
→ **Route B** (real items present): M7 still runs — the synthetic name
`wg-t5-06-demo-gate.json` collides with nothing and a decisions/ file is only ever
consumed by an orchestrator gating that exact tid, so planting/answering it is inert.
But: verify the GET response ALSO lists the real items correctly (free live-data
check), and never POST to any ticket name you didn't plant. If a real item's name ever
equals the demo name (inconceivable but checkable): pick `wg-t5-06-demo-gate-2.json`.

## Assumptions ledger

1. **Gate schema/line-numbers unchanged since the 2026-07-06 code read** (refs in Recon
   3). Plausible: the engine hardened 07-04→06 and T1 tickets prove, not rewrite. False
   in detail → adjust greps; false in kind (idiom gone) → Abort A2.
2. **depends_on ticket ids are authoring-time guesses** (`wg-t5-01-watchtower-app-scaffold`,
   `wg-t5-07-decision-queue-reconcile` — those war games were authored in parallel and
   may carry different slugs). If the promotion script flags an unknown dependency,
   resolve by T-id (T5-01, T5-07) against `backlog/wargames/tickets/`. If T5-07 was
   dropped entirely: proceed (Recon 6 already covers the missing-note branch).
3. **Same-machine file access is the sanctioned seam** — Watchtower reads/writes the
   store via path, not via an engine HTTP API (T5-12 builds that later; this UI can be
   re-pointed at it then). If T5-01's charter mandates API-only access and such an API
   exists → F1 Route A through it; if it mandates API-only and none exists → Abort A4.
4. **Writing decisions/ from the app is sanctioned.** The candidate brief says so
   explicitly, and the engine's own `[HITL]` log instructs humans to write that exact
   file. If any charter/doc found in recon declares Watchtower read-only-v1 → Abort A4.
5. **No auth for v1.** The scaffold has none wired (verified: socket auth is commented
   out) and this is a localhost operator tool. Flag in the README sentence that the
   decision endpoint is unauthenticated; hardening is a follow-on, not scope creep here.

## Abort conditions

Park action for ALL aborts: write
`/Users/davidcruwys/dev/ad/apps/dark-factory/engine/store/needs-decision/wg-t5-06-hitl-inbox-ui.json`
containing `{"ticket":"wg-t5-06-hitl-inbox-ui","question":"<one line>","note":"<observed, with paths>"}`,
leave this ticket in `running/`, stop. Never guess past an abort. (Yes — an abort here
files into the very inbox this ticket builds; keep the park file well-formed.)

- **A1 — App home missing/ambiguous.** `~/dev/ad/apps/watchtower` absent, or not the
  AppyStack app (Recon 1). Question: "T5-06 expects the Watchtower app at
  ~/dev/ad/apps/watchtower (ADR-0032). It's <missing/moved/replaced by X>. Where do I build?"
- **A2 — Gate idiom gone.** orchestrator.py no longer implements
  needs-decision/→decisions/ (Recon 3). Question: "The mid-task gate this UI surfaces
  no longer exists in that shape. Re-scope T5-06 against the current mechanism?"
- **A3 — Baseline or build irrecoverable.** Scaffold red before changes (M1), or M7
  fails twice for shifting reasons. Question: "T5-06 blocked: <symptom + log path>.
  Fix upstream first, or waive?"
- **A4 — Doctrine conflict.** T5-07's note contradicts the gate/curation split, a
  charter declares Watchtower read-only, or API-only access is mandated with no API
  (Recon 6, Assumptions 3–4). Question: "T5-06's design conflicts with <doc, path,
  quote>. Which wins?"

## Verification

Positive — all must pass:

```bash
test -f ~/dev/ad/apps/watchtower/server/src/routes/hitl.ts            && echo PASS-1
test -f ~/dev/ad/apps/watchtower/server/src/routes/hitl.test.ts       && echo PASS-2
test -f ~/dev/ad/apps/watchtower/client/src/pages/HitlInbox.tsx       && echo PASS-3
grep -q  hitl ~/dev/ad/apps/watchtower/server/src/index.ts            && echo PASS-4   # route mounted
grep -q  HitlDecision ~/dev/ad/apps/watchtower/shared/src/types.ts    && echo PASS-5
cd ~/dev/ad/apps/watchtower && npm run typecheck && npm test          && echo PASS-6
git -C ~/dev/ad/apps/watchtower log --oneline -n 10 | grep -qi 'wg-t5-06' && echo PASS-7
```

Behavioural (repeatable M7 core — server up, then):

```bash
curl -s localhost:5061/api/hitl | grep -q '"pending"'                              # GET shape
# plant → appears pending → approve → 200 → twin file exists → repeat POST → 409
# (full sequence in M7; it must have been demonstrated once and cleaned up)
```

Negative — must ALSO hold:

```bash
ls ~/dev/ad/apps/dark-factory/engine/store/needs-decision/ | grep -c wg-t5-06-demo | grep -qx 0 && echo NEG-1
ls ~/dev/ad/apps/dark-factory/engine/store/decisions/      | grep -c wg-t5-06-demo | grep -qx 0 && echo NEG-2
git -C ~/dev/ad/apps/dark-factory diff --quiet engine/orchestrator.py engine/warm_pool.py engine/status.py && echo NEG-3
git -C ~/dev/ad/apps/dark-factory status --short | grep -cv '^$' | grep -qx 0 && echo NEG-4  # dark-factory untouched
```

(NEG-4 relaxes only for the abort park file, or files another process changed —
name them in the results notes.)

## Executor notes (sonnet)

- **Scope fence:** all code lands in `~/dev/ad/apps/watchtower`. In dark-factory you
  may READ anything and WRITE only: the M7 demo pair (removed before you finish) and an
  abort park file. Never touch `engine/*.py`, `queue/`, `running/`, `done/`,
  `research/`, or any real needs-decision/decisions file.
- The join key across the three store dirs is the **exact filename including `.json`**.
  Every bug in this seam historically comes from trimming that extension.
- Decision writes are temp-file-then-rename, same directory, always — a torn write is
  a silent APPROVE on the engine side.
- Decisions are write-once from this surface: 409 on conflict, never overwrite. The
  human can always fall back to the CLI echo the engine prints.
- Prefer HITL over guessing: charter conflicts, vocabulary conflicts, surprising T5-01
  shapes → park (A4) rather than inventing architecture. A parked question costs
  minutes; a wrong seam bakes into every later T5 view.
- **The rabbit hole:** real-time push. You will want Socket.io events, fs.watch, and
  live-updating cards — the scaffold makes it seductively easy. Don't. A 5s poll is the
  whole v1; push is a later ticket once T5-03/T5-04 define the app's event story.
