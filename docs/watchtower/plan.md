# Watchtower v0 — Implementation Plan

**Generated**: 2026-05-28
**Method**: plan-hunter (4 competing drafts → 4-judge scoring → synthesis)
**Status**: opinionated, time-boxed, ready to execute

---

## Plan-Hunter Prelude

**Winning draft**: **Risk-First** (3 of 4 judge votes — Architecture, Velocity, Truth-to-Brief). User-First took the Empathy judge vote.

**Why Risk-First won**: The single most under-specified element in the brief is *how Watchtower triggers a workflow run*. Every other surface (Today screen, file schemas, queue-by-decision view) is essentially CRUD over four YAML/JSON shapes — solvable inside a weekend by any RVETS scaffold. The trigger story is the integration spine; if it's broken or hand-wavy, the rest of the app is a static viewer. Risk-First makes "Watchtower spawns level-1-census batch-1 from a button click and receives the result" the **first** thing built, before any pretty UI. MVP-First was close but deferred this risk to phase 2; Dependency-First over-indexed on schema lock-in before proving the wiring; User-First wrote a beautiful Today screen that couldn't actually *do* anything.

**Best ideas grafted in from runners-up**:
1. **From MVP-First**: back-fill batch-0 census as a synthetic experiment record so the Today screen has real data on day one — no empty-state design problem. (Phase 1.)
2. **From User-First**: the **Decision Queue is the only landing surface**. Not "Today + Experiments + Runs as peer tabs" — Today is the home, and Experiments/Runs are drill-downs. This is the explicit answer to the N=1,150 overwhelm problem.
3. **From Dependency-First**: write the four record schemas as **JSON Schema files** (not just TypeScript types) before any Express route exists. The schema is the contract between Watchtower, workflows, and future tools. Validated reads + validated writes from day one.

**Plan-hunter risk flags**:
- The **trigger mechanism** (shell exec vs. file-write+watcher vs. MCP) is committed in Phase 0 below but is genuinely the architectural decision of the project. The plan picks **shell exec via Express child_process** as the v0 choice and explains why; if that proves wrong, the swap is contained to one server module.
- The **9-layer taxonomy** is asserted in the brief but no examples exist yet for 6 of the 9 layers. Plan assumes the taxonomy is correct and surfaces friction as a Phase 2 learning.
- **No real-time updates** in v0 — polling only. Socket.io is tempting but unnecessary; flagged as a v0.1 candidate if polling feels janky.
- **The workflow harness contract is one-way today**: workflows write JSONL, Watchtower reads them. There is no "workflow completion signals Watchtower" channel except file mtime polling. Acceptable for v0; revisit at N>50 runs.

---

## North Star

A single decision queue over four file-backed records, where David never browses 1,150 artifacts — he answers a small ordered list of "what needs me?" prompts that the system surfaces. The first usable proof is: **click "Run batch 1" → 5 minutes later a decision card appears on Today**.

## Scope (v0)

- One repo: `dark-factory/apps/watchtower/`
- Three screens (Today, Experiments, Runs) — Today is home, the other two are drill-downs
- Four file-backed records under `dark-factory/data/{experiments,runs,learnings,promotions}/`
- One workflow integration: `level-1-census` (already running)
- One trigger path: **Express server shells out to the workflow CLI**
- One concurrency story: only one workflow runs at a time (queued, not parallel)
- Local-only, single-user, no auth, no deployment, no Socket.io

## Out of Scope (v0)

- Thumbnail ideation workflow (mentioned in brief — defer)
- Multiple workflow types — only level-1-census wired up
- SQLite, search index, full-text query (file scan is fast enough at N<50)
- Real-time updates / WebSocket / SSE
- Auth, multi-tenancy, deployment
- Auto-promotion logic (Promoter agent is data-only; David clicks the buttons)
- Mochaccino retirement — runs in parallel until Watchtower replaces design 09
- The Architect / Builder / Evaluator / Learning Miner specialist agents — Swagger orchestration is *modeled* as data (experiment + run + learning + promotion), but the agents themselves are not implemented; the user does Swagger's job in v0

---

## Phase 0 — Decisions Locked Before Code (Day 0, ~2 hours)

Lock the three things that make every later phase faster:

### 0.1 Workflow trigger mechanism: **shell exec from Express**
- Express server exposes `POST /api/workflows/:name/run` with body `{ args }`
- Server `child_process.spawn`s: `DISABLE_GROWTHBOOK=1 CLAUDE_CODE_WORKFLOWS=1 claude --workflow .claude/workflows/<name>.workflow.js --args '<json>'`
- Stdout/stderr captured into `data/runs/<run_id>/log.txt`
- Run record (`run.json`) written by Watchtower *before* spawn (status: `running`); workflow appends to its own JSONL (existing behaviour); Watchtower updates run status from `running` → `complete` when the subprocess exits 0, `failed` if non-zero
- **Why not file-write+watcher**: doubles the contract; workflow doesn't know it was triggered by Watchtower
- **Why not MCP**: requires Claude session to be open; Watchtower must work when David has no Claude window running
- **Concurrency**: server holds an in-memory `currentRun` lock; second request returns 409 with the active run_id

### 0.2 Schema files first: **JSON Schema in `apps/watchtower/schemas/`**
- `experiment.schema.json`, `run.schema.json`, `learning.schema.json`, `promotion.schema.json`
- Validated on both write (server) and read (server, returning `{ data, validationErrors[] }` so the UI can flag bad records without crashing)
- TypeScript types generated from these via `json-schema-to-typescript` (or hand-written — pick whichever's faster, the schemas are small)

### 0.3 File layout: **flat per-record-type, one file per record**
```
dark-factory/data/
  experiments/<exp_id>.yml
  runs/<run_id>/run.json + log.txt
  learnings/<learn_id>.yml
  promotions/<promote_id>.yml
```
- One file per record. Glob to list. No index file (yet — flagged for Phase 4).
- YAML for human-edited shapes (experiment, learning, promotion); JSON for machine-only (run).
- IDs are filename-stem (no separate ID field needs unique constraint logic).

**Exit criteria**: 4 schema files committed, trigger architecture documented in `apps/watchtower/ARCHITECTURE.md`, file layout asserted by a Node script that creates the empty directories.

---

## Phase 1 — Wire End-to-End Trigger (Days 1–2)

Build the spine before the skin. **This is the highest-risk phase; ship it first.**

### 1.1 Scaffold the app
- `appydave:create-appystack apps/watchtower` — accept defaults
- Verify: `pnpm dev` boots client + server, Tailwind works, Express returns from `/api/health`

### 1.2 The single working route
- `POST /api/workflows/level-1-census/run` with body `{ batchStart, batchSize }`
- Server creates `runs/<run_id>/run.json` with `{ status: "running", started_at, experiment_id: "census-ongoing", args }`
- Server spawns the workflow subprocess as in 0.1
- Server returns `{ run_id }` immediately
- On subprocess exit: update `run.json` with `status, ended_at, exit_code`, append last 100 lines of stdout to `run.json.steps`
- Validate: invoke the route via `curl`, watch `data/runs/<run_id>/` appear, watch `research/census.jsonl` grow by 5 rows

### 1.3 The single working button
- Single page, single button: "Run Census Batch 1"
- Click → POST → poll `GET /api/runs/<run_id>` every 2s → show `running` then `complete`
- No styling effort. Tailwind defaults. Just prove the wire.

**Exit criteria**:
- Click button in browser → 5 new rows in `research/census.jsonl` → run status flips to `complete` in UI within polling cycle
- Re-running while a run is active returns a visible 409 error

---

## Phase 2 — The Four Records and the Today Screen (Days 3–4)

Now build the data model and the only screen that matters.

### 2.1 Back-fill census batch-0 as an experiment
- Hand-author `data/experiments/exp-census-level1.yml` covering batch-0 (the 5 records from 2026-05-26)
- Hand-author `data/runs/run-census-2026-05-26/run.json` pointing at the existing 5 census rows
- This gives Today screen real content from minute zero — no empty-state.

### 2.2 Server routes (validated reads)
- `GET /api/experiments` — glob+parse+validate, returns `{ experiments[], invalid[] }`
- `GET /api/experiments/:id` — single + its runs + its learnings + its promotion
- `GET /api/runs?experiment=...&status=...`
- `GET /api/learnings?layer=prompt|agent|...` (queryable by layer — success criterion 5)
- `POST /api/experiments`, `POST /api/learnings`, `POST /api/promotions` (write + validate)
- `PATCH /api/promotions/:id` (the decision verb: discard/rerun/improve/promote)

### 2.3 Today screen — three sections, decision-first

```
TODAY
─────────────────────────────────────────
Needs you (count badge)
  [card] exp-census-level1 / run-batch-1
    Verdicts: 3 adopt, 2 evaluate, 0 skip
    Recommendation: continue to batch 2
    [Accept] [Rerun] [Promote] [Kill] [Defer]

Recently completed (last 5)
  exp-census-level1 batch-1 — 5 assessed — 4m ago

System warnings (errors)
  • 0 schema-invalid records
  • 0 runs without learning attached
─────────────────────────────────────────
```

- Only what needs David. No browsing. No artifact counts. No charts.
- "Needs you" is computed: any promotion with `decision: not_yet` OR any completed run without a promotion record at all.
- Decision buttons write/patch the promotion record and remove the card from the queue.

**Exit criteria**:
- Today renders batch-0 as a back-filled experiment with the 5 census rows summarised (success criterion 2)
- Clicking "Run batch 1" → new decision card appears when run completes (success criterion 4)
- `GET /api/learnings?layer=prompt` returns only prompt-layer learnings (success criterion 5)

---

## Phase 3 — Experiments and Runs Drill-Downs (Day 5)

Now build the two screens you'd open *from* a Today card.

### 3.1 Experiments list
- One row per experiment file
- Columns: id, status, runs count, last run time, decision state
- Filter chips: `proposed | running | completed | promoted | killed`
- Sort: most recent activity first
- This is *not* a dashboard. Plain table. No charts.

### 3.2 Run detail
- One run = one page
- Top: status, started, ended, exit code, cost (if recorded — optional)
- Middle: steps timeline (read from run.json.steps)
- Bottom: log tail (last 500 lines of log.txt)
- Right rail: linked experiment, linked learnings (if any), promotion (if any)

### 3.3 Learning capture form (manual for v0)
- "Capture a learning" button on the run detail page
- Form: layer (dropdown of 9), summary, evidence, applies_to (multi-tag), recommendation, confidence
- Write to `data/learnings/<auto-id>.yml`
- This is how Learnings populate in v0 — David writes them. Learning Miner agent comes later.

**Exit criteria**:
- Can navigate Today → experiment → run → log
- Can capture a learning against any run
- Experiments list filters work

---

## Phase 4 — Anti-Overwhelm Hardening (Day 6)

**This phase exists specifically to answer the N=1,150 question.** The plan must not re-create the overwhelm Mochaccino design 09 hit at N=5. The discipline is enforced here, not assumed earlier.

### 4.1 The decision queue is bounded
- Today shows **at most 5 "needs you" cards** by default. More than 5 → show "+ 12 more" link, never the full list inline.
- Cards are ordered by: (a) explicit `priority` field on the promotion, then (b) age ascending (older first — surface the staleness).

### 4.2 Aggregations replace browsing
- Experiments list shows **stats, not artifacts**: "level-1-census — 4 batches, 20 assessed, 12 adopt / 5 evaluate / 3 skip — last batch 2 days ago".
- The experiment detail page summarises run outputs (e.g., "230 census rows total, +5 since last review") — David never sees a 1,150-row table in this app. The artifact-level detail lives in `census.jsonl` and is reached via shell tools (`jq`), not Watchtower screens.
- **Hard rule**: no screen in Watchtower renders >50 records. If a query returns more, it returns a summary + a "drill in by [filter]" affordance.

### 4.3 The "promote experiment to workflow" path is explicit
- When David clicks `Promote` on a decision card, the app generates a markdown checklist file `data/promotions/<id>-checklist.md` covering the 6 promotion-rule items from the brief (successful run, captured learning, repeatable harness, Watchtower view, named owner, promotion decision).
- The checklist is the human gate — Watchtower won't auto-write to `canonical/`.
- This is the **mechanism** that prevents experiments from accumulating without resolution: an unresolved experiment is a card on Today, every time David opens the app.

### 4.4 Self-instrumentation
- Add `GET /api/system/health`: counts of (experiments by status), (runs by status), (learnings by layer), (orphan runs = run with no experiment), (orphan learnings = learning with no run).
- Health surfaced as the "System warnings" section on Today.
- This is how Watchtower scales: it tells David when its own state is getting messy.

**Exit criteria** (and the explicit anti-overwhelm acceptance test):
- Seed 50 fake experiments + 200 fake runs into `data/`
- Today loads in <500ms
- Today still shows ≤5 decision cards (rest collapsed)
- No screen scrolls beyond one viewport without an explicit "show more" toggle
- Health endpoint surfaces the orphan/invalid counts correctly

---

## Phase 5 — Polish and Verification (Day 7)

### 5.1 Browser-test the happy path
- Invoke `agent-skills:browser-testing-with-devtools` to verify success criteria 1–6 end-to-end
- Capture screenshots of Today (with batch-0 + batch-1), Experiments list, a Run detail page
- These replace the Mochaccino design 09 deliverable

### 5.2 Code review pass
- Invoke `agent-skills:code-review-and-quality` on the diff
- Invoke `agent-skills:code-simplification` on the server module (the trigger spawner is the most likely place to over-engineer)

### 5.3 Documentation
- `apps/watchtower/README.md`: what it is, how to run, where data lives, how to add a workflow
- Update root `CLAUDE.md` to point Watchtower as the operating surface (Mochaccino remains for design exploration)

**Exit criteria**: all 6 success criteria green; PR ready for self-review.

---

## Risk Register (live)

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| `claude --workflow` CLI flags shift in a Claude Code update | medium | high (trigger breaks) | Pin the env-var/flag combo in `ARCHITECTURE.md`; if it shifts, swap to file-write+watcher (already documented as fallback) |
| 9-layer taxonomy doesn't fit a real learning | medium | medium | Allow `layer: other` with a free-text `other_label`; surface as a Phase 2 learning |
| Polling feels janky at N>20 concurrent runs | low (v0 forces N=1) | low | Document Socket.io as v0.1 candidate |
| File scan slows past N=500 records | medium (when census completes) | medium | Add a write-time index (`data/_index.json`) in v0.1 before SQLite |
| The "Run batch 1" button fires while Claude Code is mid-session and conflicts | medium | low | The subprocess runs in its own env; document that workflows are best invoked when no Claude session is editing the same files |
| Watchtower becomes another Mochaccino — pretty but unused | medium | high | The dogfooding loop *requires* it: every batch after batch-0 is run through Watchtower, not the CLI. Make the CLI path inconvenient. |

---

## Scale Argument — How Watchtower Survives N=1,150

The brief makes this the existential question. The plan's answer is structural:

1. **Watchtower never renders an artifact list**. It renders experiment/run aggregates. The 1,150 artifacts live in `census.jsonl`; they are queried with `jq`, summarised in run records, and surfaced as "+5 new rows since last review" — not as rows in the UI.
2. **The unit of attention is the decision, not the record**. A complete census batch produces one decision card ("review batch N, continue to N+1?"). 230 batches of 5 = 230 decision cards over the *life* of the project, not all at once — only the unresolved ones appear on Today, and the queue is capped at 5 visible.
3. **Promotion is the pressure-release valve**. Every promotion either ratifies a workflow (removes it from the experiment list) or kills it (removes it). Experiments cannot accumulate indefinitely — the promotion checklist forces resolution.
4. **System health is self-reported**. The orphan/invalid counts make backlog visible *as a single number*, not as a screen full of warnings. If those numbers grow, that itself becomes a single decision card.

This is the explicit anti-Mochaccino discipline: visualisations were the wrong primitive — they showed *everything*. Watchtower's primitive is a queue — it shows *the next thing*.

---

## Time Budget

| Phase | Estimate | Calendar |
|-------|----------|----------|
| 0 — Decisions locked | 2 hours | Day 0 |
| 1 — Trigger wired end-to-end | 2 days | Days 1–2 |
| 2 — Four records + Today screen | 2 days | Days 3–4 |
| 3 — Experiments + Runs + Learning capture | 1 day | Day 5 |
| 4 — Anti-overwhelm hardening | 1 day | Day 6 |
| 5 — Polish + verification | 1 day | Day 7 |
| **Total** | **~7 working days** | **One week** |

If Phase 1 slips, ship Phase 2 against hand-written runs and treat the trigger as a Phase 1.5 follow-up. The Today screen is still useful as a viewer even without the button working.

---

## Open Questions

These were surfaced by plan-hunter and require David's decision before or during execution:

1. **Workflow CLI invocation form** — The exact `claude --workflow ...` command line: is it stable? Is there a non-interactive flag that suppresses TUI? If not, does `node` invoking the workflow script directly work without the Claude Code harness? (Phase 0 blocker.)
2. **Run subprocess identity** — Should the spawned workflow run as the same shell user with full credentials, or in a sandboxed env? V0 plan says "same user, full creds, single machine, single user" — confirm acceptable.
3. **Should batch-0 back-fill be authored manually or scripted?** — Plan says manual (one experiment, one run, 5 census rows already exist). If David wants a back-fill script that scans `research/census.jsonl` and synthesises experiments retroactively, that's a Phase 2 sub-task.
4. **Promotion file lives where?** — `data/promotions/<id>.yml` is the v0 location. When a promotion ratifies a workflow, does it write to `canonical/workflows/...`? Plan says no — Watchtower writes the checklist; canonical writes are a separate ratification step done by hand. Confirm.
5. **Learning auto-attach** — A learning is captured against a run. Should it also auto-attach to the experiment (parent), or only the run? Plan says auto-attach to both. Confirm.
6. **9-layer taxonomy enforcement** — Should the UI hard-enforce one of the 9 layers, or allow `other` with explanation? Plan says allow `other` as escape hatch. Confirm.
7. **Mochaccino design 09 deprecation** — Once Watchtower's Today screen exists, is design 09 retired, kept as a historical artifact, or kept as a parallel visualisation? Plan-hunter suggests retire (move to `mochaccino/archive/`) — confirm.
