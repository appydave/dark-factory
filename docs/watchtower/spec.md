# Spec: Dark Factory Watchtower v0

> **⚠️ PARTIALLY SUPERSEDED (2026-06-06 three-plane model — see [`RE-BUCKETING.md`](RE-BUCKETING.md)).**
> The §5/§12/R7 *"no WebSockets/SSE; poll every 5s"* rule is **reversed** — Switchboard pushes over SSE and the
> Watchtower viewer consumes it; polling survives only at the outward Codex/tracker boundary. The §7
> shell-out-to-workflow trigger is **superseded** by the durable queue + claim + report-back (proven in
> `experiments/watchtower-engine/`; `DECISIONS.md` D1 already moved to file-trigger + watcher). Read this as the
> Control-Plane viewer scope only — the engine lives on the Factory Floor / Switchboard. Physical re-home pending.

**Status**: draft for ratification — 2026-05-28
**Author**: requirements agent (spec-driven-development pass)
**Companion docs**: `chatgpt-brief.md` (strategic input), `context.md` (session state), `../dark-factory-living-system-spec.md` (parent architecture)
**Skill applied**: `agent-skills:spec-driven-development`

---

## Assumptions surfaced before drafting

1. Watchtower v0 is a **local-only web app** scaffolded by `appydave:create-appystack` (RVETS — React + Vite + Express + TypeScript + SQLite-or-files). Not Electron, not CLI.
2. The four record types (`experiment.yml`, `run.json`, `learning.yml`, `promotion.yml`) are **net-new artifacts**. They do not yet exist in `research/` or `.claude/workflows/`. Watchtower v0 introduces them.
3. The existing `research/census.jsonl` is an **input to Watchtower**, not owned by it. Watchtower reads it; the census workflow continues to own writes.
4. `.claude/workflows/level-1-census.workflow.js` continues to be **invoked by the Workflow Tool harness** (`DISABLE_GROWTHBOOK=1 CLAUDE_CODE_WORKFLOWS=1 claude`). Watchtower does not re-implement the harness — it shells out to it and surfaces results.
5. "Local-only" means `localhost`-bound HTTP server. No tunnel, no Tailscale exposure, no external auth.

If any of these is wrong, the spec is wrong. Correct in Open Questions or before implementation begins.

---

## 1. Problem statement

David's articulated overwhelm signal (verbatim from `context.md`):

> *"I look at a screenshot like this, and in its small we've only done five things. From a point of view, it's okay, but this is going to get to overwhelm within two or three iterations. I want to have a series of experiments that we keep testing but probably also promote experiments to proper workflows."*

**Failure mode without Watchtower**: At N≥20 census records (≈3 batches of 5), the Mochaccino dashboard becomes a scrolling list of artifacts with no queue of decisions. The system has output but no foreground. David's attention is spent re-deriving "what do I look at next" every session, and experiments that produced results 3 days ago drift into invisibility without a promotion decision being made.

**Measurable threshold the absence of Watchtower violates**:
- > 5 minutes from session start to "what should I work on right now."
- > 0 completed experiments without an explicit promote/discard/rerun decision.
- > 0 captured learnings not attached to a 9-layer taxonomy entry.

Watchtower v0 succeeds when all three counters can be driven to zero in a single session.

**Dissent against the ChatGPT brief**: The brief proposes thumbnail ideation as the first slice. This is wrong for v0 because (a) census is already running and produces real records *today*, (b) thumbnail ideation would force us to invent a new workflow AND a new control surface in the same v0, doubling risk, and (c) dogfooding requires the v0 to drive a workflow that exists. **First slice is census-batch-1.**

---

## 2. Users and non-users

**User (singular)**: David Cruwys. Local machine. Hands-on technical operator. Writes code, reads JSON, runs CLI tools without UI scaffolding.

**Explicit non-users in v0**:
- No team members. No collaborators. No shared sessions.
- No clients (SupportSignal, voz, Lars, Kiros) — even read-only.
- No mobile or tablet view. Desktop browser only.
- No public/shared URLs. No tunnel to Tailscale fleet.
- No automated agents reading Watchtower's UI (agents read the underlying files directly).
- No future-David from another machine — v0 runs only where the files live.

**Implication**: No auth, no RBAC, no per-user state, no audit log of "who clicked promote." Single-user simplifies everything; deferring multi-user is a hard cut, not a "we'll add later."

---

## 3. Core jobs-to-be-done (4 screens)

### JTBD-1: Today
- **Trigger**: David opens Watchtower at session start.
- **Context**: Has not opened the app in N hours; wants to know what changed and what needs him.
- **Desired outcome**: A single screen answers "what's the highest-leverage thing I can do in the next 30 minutes."
- **Success signal**: David clicks one item on the Today screen and acts on it within 60 seconds of page load.

### JTBD-2: Experiments
- **Trigger**: David wants to see the full portfolio — what's proposed, running, completed, promoted, killed.
- **Context**: Mid-session, after acting on Today; wants the panoramic view.
- **Desired outcome**: Single list grouped by status, sortable by recency. Each row links to its experiment record.
- **Success signal**: David can find a specific experiment by name or status in ≤3 clicks from anywhere in the app.

### JTBD-3: Runs
- **Trigger**: An experiment just executed; David wants to see what happened.
- **Context**: A workflow run produced a `run.json`; David needs step-by-step status, cost, failure point, links to outputs.
- **Desired outcome**: Timeline view of the run's steps, with duration, status, cost rollup, and a link to the produced artifacts.
- **Success signal**: David can answer "did this run succeed and what did it cost" without opening any file in a text editor.

### JTBD-4: Learnings
- **Trigger**: David wants to review what the factory has learned, grouped by where the learning applies.
- **Context**: Reviewing whether enough signal has accumulated to justify a promotion or a prompt patch.
- **Desired outcome**: Learnings grouped by the 9-layer taxonomy (`prompt`, `agent`, `skill`, `workflow`, `harness`, `evaluation`, `data_schema`, `watchtower_ui`, `orchestration`). Each learning shows source run, summary, recommendation, promotion candidacy.
- **Success signal**: David can mark a learning as "applied" or "dismissed" and the system records that decision.

---

## 4. Acceptance criteria (Given/When/Then)

### AC-1: Today screen shows decisions needed
- **Given** at least one experiment has `status: completed` and no promotion decision recorded,
- **When** David loads `/` (the Today screen),
- **Then** that experiment appears in a "Needs decision" section with buttons: `Accept`, `Rerun`, `Promote`, `Kill`.

### AC-2: Today shows recent completions and system warnings
- **Given** at least one experiment completed in the last 7 days AND at least one learning has no taxonomy `layer` field,
- **When** David loads `/`,
- **Then** the recent experiment appears in "Recently completed" AND a "System warnings" count shows the number of learnings missing layer.

### AC-3: Experiments registry shows all experiments by status
- **Given** N experiment records exist in `data/experiments/*.yml`,
- **When** David loads `/experiments`,
- **Then** all N experiments appear, grouped by status (`proposed | running | completed | promoted | killed`), each row linking to the detail view.

### AC-4: Runs viewer shows steps + cost
- **Given** a run record exists at `data/runs/<run_id>.json` with ≥1 step and a `cost` object,
- **When** David navigates to `/runs/<run_id>`,
- **Then** each step's `name`, `status`, `duration_seconds`, and optional `reason` are visible AND the total `cost.tokens` and `cost.usd_estimate` are shown.

### AC-5: Learnings viewer groups by 9-layer taxonomy
- **Given** N learning records exist in `data/learnings/*.yml`, each with a `layer` field from the 9-value enum,
- **When** David loads `/learnings`,
- **Then** learnings appear grouped under exactly 9 layer headings; any learning with a missing or invalid layer appears in a "Malformed" group at the top with a fix link.

### AC-6: Triggering a workflow run writes the correct files and surfaces output
- **Given** an experiment record exists with `workflow.harness: level-1-census` and inputs configured,
- **When** David clicks "Run" on that experiment in Watchtower,
- **Then** Watchtower shells out to the Workflow Tool, writes a `data/runs/<run_id>.json` while the run executes, updates step status as the workflow progresses, and on completion the run appears under `/runs` AND a "Needs decision" row appears on Today.

### AC-7: First vertical slice — census batch-1 end to end
- **Given** Watchtower is freshly scaffolded with seed data including an experiment record `exp-2026-05-28-census-batch-1`,
- **When** David clicks "Run" on that experiment,
- **Then** (a) `.claude/workflows/level-1-census.workflow.js` executes with `batchStart: 5, batchSize: 5`, (b) 5 new records are appended to `research/census.jsonl`, (c) a `run.json` is written under `data/runs/`, (d) a `learning.yml` stub is created (even if blank for David to fill), (e) the experiment now appears in Today's "Needs decision" section, (f) David can click `Promote` and a `promotion.yml` is written.

---

## 5. Out of scope (aggressive cuts)

v0 deliberately does **NOT** do:

- **Multi-user / auth / RBAC** — single user, no login.
- **Real-time push** — no WebSockets, no SSE. Polling every 5s during an active run is acceptable; otherwise on-load refresh.
- **Automatic promotion** — every promotion is HITL. Never auto-promote.
- **Mobile or responsive design** — desktop browser at ≥1280px width only.
- **Public sharing / export** — no "share this experiment" link, no PDF export.
- **Cross-artifact full-text search** — no global search bar. Filter-by-status only.
- **Inline experiment editing** — experiments are authored in YAML files; Watchtower reads but does not write experiment specs. (It writes promotions and run results.)
- **Diagram view auto-generation from workflow scripts** — deferred. v0 shows a flat step list, not a DAG.
- **Cost projections / budget tracking** — show actual cost per run; do not project future cost or warn on budget.
- **Cross-experiment learnings rollup** — learnings are listed flat under their layer; no "which experiments produced the most prompt-layer learnings" analytics.
- **The other 5 specialist roles' UIs** — Architect, Builder, Runner, Evaluator, Learning Miner, Promoter are conceptual roles. v0 surfaces *outputs* of Runner and Evaluator; the others have no dedicated UI.
- **Swagger conversational interface** — v0 has buttons, not chat. The Swagger orchestration model is a future layer; v0 is the substrate it will sit on.
- **Level 0 / Level 2 / Level 3 / Level 4 workflows** — only Level 1 census is wired up in v0.
- **Notifications** — no desktop notifications, no email, no Slack.
- **Undo** — actions (promote, kill) write a record; reversal means writing a new record. No transactional undo.

---

## 6. Non-functional requirements

| Concern | Requirement |
|---|---|
| Deployment | Local only. `localhost:NNNN`. No external binding. |
| Auth | None. Same-origin only. |
| Storage | File-backed: YAML for human-edited specs (`experiment.yml`, `learning.yml`, `promotion.yml`), JSON for machine-written records (`run.json`). Optional SQLite as a derived index, never source of truth. |
| Source of truth | The files in `data/` and `research/`. UI is a projection; deleting the DB is harmless. |
| Concurrency | Single user, single session. No file locking required. |
| Performance bound | Operates correctly up to **500 experiments, 5,000 runs, 5,000 learnings**. Beyond this, paginate or degrade gracefully. v0 is not designed for 50k. |
| Page load | Today screen renders in < 500ms with 50 experiments loaded. |
| Workflow invocation latency | Click-to-run-started ≤ 2s. Run duration itself is bounded by the workflow, not Watchtower. |
| Coexistence | Runs alongside `.claude/workflows/` harness without modification to existing workflow files. Shell-out interface only. |
| Restart | App restart loses no data; all state is on disk. |
| Browser support | Latest Chrome / Safari / Firefox. No IE, no legacy. |

---

## 7. Swagger orchestration interaction model

Walk-through: **David clicks "Run census batch 1"** on the Today screen.

1. **Click handler** (Watchtower frontend) — POST `/api/experiments/exp-2026-05-28-census-batch-1/run`.
2. **API layer** (Watchtower backend Express) —
   - Validates the experiment record exists and is in `status: proposed` or `status: completed` (rerun-able).
   - Generates a `run_id` (`run-<ISO date>-<seq>`).
   - Writes initial `data/runs/<run_id>.json` with `status: starting`, empty `steps[]`.
   - Spawns the workflow harness as a child process:
     ```
     DISABLE_GROWTHBOOK=1 CLAUDE_CODE_WORKFLOWS=1 claude \
       workflow run .claude/workflows/level-1-census.workflow.js \
       --args '{"artifactsPath": "...", "censusPath": "...", "batchStart": 5, "batchSize": 5}'
     ```
   - Returns `{ run_id }` to the client immediately.
3. **Workflow execution** — Workflow Tool runs the existing `level-1-census.workflow.js` unchanged. Watchtower does NOT intercept agent calls.
4. **Step progress** — Watchtower tails the workflow's stdout/log file (or polls a known progress file the workflow writes) and updates `data/runs/<run_id>.json` with each phase transition: `Load → Assess → Store`.
5. **Frontend polling** — The Run detail page polls `GET /api/runs/<run_id>` every 5 seconds while `status !== complete && status !== failed`.
6. **Completion** — When child process exits 0:
   - Watchtower marks `run.json.status: complete`, records `ended_at` and final `cost` (if the workflow emits cost; otherwise `cost: { tokens: null, usd_estimate: null }`).
   - Watchtower creates a stub `data/learnings/learn-<run_id>.yml` with `layer: TODO` and a prompt for David to fill.
   - Watchtower updates the experiment's `status: completed` and marks it `needs_decision: true`.
7. **Surfacing on Today** — Next Today screen load (or current page's polled refresh) shows the experiment in "Needs decision" with `Accept / Rerun / Promote / Kill` buttons.
8. **David's decision** — Clicking `Promote` POSTs to `/api/experiments/<id>/promote`, which writes `data/promotions/promote-<id>.yml` and updates experiment `status: promoted`.

**Key constraint**: Watchtower never modifies `.claude/workflows/*.js`. The workflow is a black box that takes JSON args and writes to known paths.

---

## 8. First vertical slice — census-batch-1

**The runnable scenario**, end to end:

**Precondition**:
- `apps/watchtower/` scaffolded via `appydave:create-appystack`.
- Seed file `data/experiments/exp-2026-05-28-census-batch-1.yml` exists with:
  ```yaml
  id: exp-2026-05-28-census-batch-1
  status: proposed
  intent:
    user_goal: "Continue Level 1 census — assess artifacts 5–9"
    domain: dark-factory
    lane: research
    station: census
  hypothesis:
    claim: "Batch 1 of 5 artifacts can be censused with same quality as batch 0"
    success_signal: "All 5 records validate against census schema and David accepts verdicts"
  inputs:
    artifactsPath: research/artifacts.jsonl
    censusPath: research/census.jsonl
    batchStart: 5
    batchSize: 5
  workflow:
    type: experiment
    harness: level-1-census
  outputs:
    expected:
      - research/census.jsonl (5 appended lines)
      - data/runs/<run_id>.json
      - data/learnings/learn-<run_id>.yml
  decision:
    options: [discard, rerun, improve, promote_to_workflow]
  ```
- Watchtower running at `localhost:NNNN`.

**The scenario**:
1. David opens `localhost:NNNN/`. Today screen shows the seed experiment under "Proposed."
2. David clicks the experiment, opens the detail view, clicks **Run**.
3. Watchtower API spawns the workflow, returns `run_id`. UI redirects to `/runs/<run_id>`.
4. David watches phases tick: Load → Assess → Store. Each phase updates within 5s of actual transition.
5. Workflow completes. `research/census.jsonl` has 10 records (5 original + 5 new). `data/runs/<run_id>.json` shows 3 steps, all pass.
6. David returns to Today. Experiment is now under "Needs decision."
7. David clicks **Promote**. `data/promotions/promote-exp-2026-05-28-census-batch-1.yml` is written. Experiment moves to "Promoted."
8. David clicks the learning stub at `/learnings`. Fills in:
   ```yaml
   layer: workflow
   learning:
     summary: "Batch-of-5 sizing works; assessment quality stable across batches."
   ```
9. Save. Learning appears under "workflow" group. System-warnings counter on Today decrements by 1.

**This is the v0 demo.** Anything that doesn't serve this scenario is out of scope.

---

## 9. Open questions for David

Framed as binary or small-N choices. Resolve before implementation.

| # | Question | Options |
|---|----------|---------|
| Q1 | Storage backend for the index | (a) Pure files, scan on every request; (b) Files as source-of-truth + SQLite index rebuilt on file change |
| Q2 | Workflow invocation mechanism | (a) Shell out to `claude workflow run` child process; (b) MCP call to a Workflow Tool MCP server; (c) Direct Node import of the workflow JS |
| Q3 | Where do experiments live | (a) `apps/watchtower/data/experiments/`; (b) `dark-factory/experiments/` (sibling to `canonical/`); (c) `dark-factory/data/experiments/` (matches brief's diagram) |
| Q4 | Is `research/census.jsonl` writable by Watchtower? | (a) No — workflow writes, Watchtower reads; (b) Yes — Watchtower writes on user actions (verdict overrides) |
| Q5 | Workflow progress reporting | (a) Workflow writes to a known progress file Watchtower polls; (b) Workflow emits structured stdout Watchtower parses; (c) Workflow writes directly to `run.json` and Watchtower polls that |
| Q6 | Port number for the local server | (a) Random/AppyStack default; (b) Fixed (e.g. 7421 — adjacent to mochaccino's 7420) |
| Q7 | Is the seed experiment hand-authored or generated | (a) Hand-author the first `experiment.yml`; (b) Build a "New experiment" form in v0 (adds scope) |
| Q8 | What happens to existing 5 census records | (a) Treat as orphan-no-experiment (no parent record); (b) Retroactively create `exp-2026-05-26-census-batch-0.yml` to wrap them |
| Q9 | Promotion writes to `canonical/` or only to `data/promotions/` | (a) Promotion is a *decision record* only; canonical materialization is a separate explicit step; (b) Promotion auto-materializes the workflow under `canonical/` |

**My recommendations** (mark dissent):
- Q1: (a) pure files for v0. SQLite is a v0.1 optimization.
- Q2: (a) shell out. MCP is over-engineered for v0.
- Q3: (c) `dark-factory/data/` matches the brief's diagram and keeps Watchtower a pure projection.
- Q4: (a) workflow owns writes. Strict separation.
- Q5: (a) progress file. Stdout parsing is fragile.
- Q6: (b) fixed 7421 — predictable.
- Q7: (a) hand-author. Form is v0.1.
- Q8: (b) retroactively wrap. Cleaner mental model.
- Q9: (a) decision-only. Auto-materialization is dangerous in v0.

---

## 10. Risks

| # | Risk | Likelihood | Mitigation |
|---|------|-----------|------------|
| R1 | Workflow Tool harness changes break the shell-out contract | Medium | Pin the env var invocation in a single helper module; integration test the spawn |
| R2 | File-backed storage doesn't scale past 500 experiments | Low (v0) | Acceptance: v0 is sized for ≤500; explicit out-of-scope above |
| R3 | David hand-authors malformed YAML | High | Schema-validate on read; "Malformed" group on Experiments page with line/column |
| R4 | The 9-layer taxonomy is wrong and needs to evolve | Medium | Store layer as a string with enum validation in code, not DB constraint; renaming a layer is a code change + migration script |
| R5 | "Run" button blocks if a previous run is still executing | Medium | Per-experiment lock file; UI shows "running, started Xs ago"; disable Run button until prior completes |
| R6 | David never actually opens Watchtower because he's used to Mochaccino | High | Forcing function: first slice must produce something Mochaccino can't — a captured promotion decision. If after week 1 David hasn't clicked Promote once, v0 has failed |
| R7 | Run progress polling at 5s feels laggy | Low | Acceptable for v0; if it bites, drop to 2s; SSE only if 2s is still wrong |
| R8 | The "stub learning" auto-created post-run becomes noise | Medium | If David never fills it, it becomes a system warning. Acceptable forcing function; reconsider if >50% of stubs go unfilled after week 2 |
| R9 | Scope creep into Swagger conversational layer | High | Hard cut in Out of Scope. Any chat-shaped feature is rejected in v0 review |
| R10 | The brief's `cost` object isn't actually produced by the current Workflow Tool | High | Verify before AC-4 is testable; if cost isn't emitted, AC-4 accepts `null` and a TODO badge appears |

---

## 11. Success criteria (testable)

v0 is **done** when:

1. All 7 acceptance criteria (AC-1 through AC-7) pass on the operator's machine.
2. The census-batch-1 scenario (Section 8) executes end-to-end without manual file editing.
3. David can answer "what's next" in < 60 seconds from a cold session start.
4. Zero experiments exist in `status: completed` with no promotion decision (after at least one full session of use).
5. Zero learnings exist with a missing or invalid `layer` (after at least one full session of use).
6. The Mochaccino design 09 is no longer the primary surface David checks at session start.

v0 has **failed** if, after one week of availability:
- David is still opening Mochaccino design 09 first.
- No promotion decision has been recorded.
- The Today screen still feels like "another dashboard" rather than a queue.

---

## 12. Boundaries

**Always**:
- Validate YAML/JSON on read with explicit schema; reject malformed records into a "Malformed" group.
- Treat files as source of truth; any derived state must be rebuildable from files alone.
- Shell out to the Workflow Tool; never re-implement workflow execution inside Watchtower.
- Append, never overwrite, run records and promotion decisions.
- Use ISO-8601 timestamps everywhere.

**Ask first**:
- Adding any new field to the four record schemas.
- Changing the 9-layer taxonomy.
- Adding a new screen beyond the four.
- Changing the shell-out invocation contract.
- Writing to `research/` (only `level-1-census.workflow.js` writes there in v0).

**Never**:
- No auth, no users table, no sessions.
- No automatic promotion.
- No editing of ratified canonical artifacts from Watchtower.
- No real-time push protocols (WebSocket/SSE) in v0.
- No deletion of run records or learnings — only mark `dismissed: true`.
- No global search, no full-text indexing.
- No mobile/responsive work.

---

**End of spec. ~470 lines.**
