---
generated: 2026-06-16
generator: system-context
status: snapshot
sources:
  - CLAUDE.md
  - CLAUDE.local.md
  - README.md
  - context/CONTEXT.md
  - context/context.globs.json
  - docs/north-star.md
  - docs/dark-factory-constellation.md
  - docs/runtime-model.md
  - docs/architecture.md
  - docs/appyradar.md
  - docs/dark-factory-living-system-spec.md
  - docs/canonical-form-spec.md
  - docs/provenance-spec.md
  - docs/ingestion-workflow.md
  - docs/human-comms.md
  - docs/systemic-fixes.md
  - docs/intake.md
  - docs/sop-lifecycle.md
  - docs/tool-registry.md
  - docs/ylo-to-poem-blueprint.md
  - docs/watchtower/spec.md
  - docs/watchtower/DECISIONS.md
  - docs/watchtower/symphony-spec.md
  - AUDIT-2026-06-12.md
  - experiments/watchtower-engine/README.md
  - experiments/watchtower-engine/failures/register.jsonl
  - experiments/watchtower-engine/failures/record-failure.sh
  - .claude/workflows/level-1-census.workflow.js
  - .claude/skills/marshall/SKILL.md
  - .claude/skills/swagger/SKILL.md
  - .claude/skills/millwright/SKILL.md
  - canonical/INDEX.md
  - research/INDEX.md
  - research/census.jsonl
  - mochaccino/workspace.md
regenerate: "Run /system-context in the repo root"
---

# Dark Factory — System Context

## Purpose
A self-improving capability factory **you direct by talking to it** — you say what you want, it runs the work in interactive sessions (on the Max plan, never cron/API), observes itself, and improves; a lights-off floor under a glass-walled watchtower with David as the director. Its *class* is an **agentic Manufacturing-Execution-System + control plane**: a stateless, replaceable execution floor with all coordination state pushed out into surrounding services.

**The repo has two paths, and the priority order matters.** **Path 1 — build the factory machinery** (PRIORITY NOW): the producer (talk → ticket), the consumer (claim → execute → record → done loop), the in-session trigger, the constellation of supporting services, and the conversational control layer. **Path 2 — run the content** (DEFERRED): the 1,100-artifact canonical-ingestion pipeline (census → eval → distill → ratify into `canonical/`). Path 2 is the *first cargo* the factory carries, not the factory itself — it can run in its own session once the machinery exists. **The older charter docs (`README.md`, `docs/architecture.md`) lead with Path 2 because they predate the reframe; `docs/north-star.md` is the current orienting frame and wins on priority.**

## Core Abstractions

- **The constellation (three planes + two read-only sensors)** — Dark Factory is the *whole system*, not one component. **Floor** (this repo) = where agents execute: Marshall dispatches, Swaggers run jobs. **Comms + state plane** (Switchboard, an AppySentinel daemon, sibling repo `apps/switchboard`) = the nervous system: job queue, claims/ownership/lifecycle, SSE bus + durable `Last-Event-ID` replay; never runs `claude`. **Control plane** (Watchtower, AppyStack/React) = the glass wall where the human decides: decision cards (≤5 Today), dashboards, verdict records; reads state, never mutates `canonical/`. **Two read-only sensors**: **AngelEye** answers *session* liveness (Claude Code hook events — "when was session X last active?"); **AppyRadar** answers *machine/fleet* resource + process health (read-only SSH across the 5-Mac network, AppySentinel Pilot 1). **Neither sensor kills** — Marshall is the only actor that reaps. The load-bearing boundary (DF-7 D4): *Switchboard MAY CRUD its own comms/queue/state domain (enqueue, claim, requeue a dead claimant) but NEVER mutates the external observed world (kill a process, close a tmux window).* "Requeue a state record = legal; kill a window = not legal." See `docs/dark-factory-constellation.md` (the canonical map — wins on constellation shape when older docs disagree) and `docs/appyradar.md` (note: the older docs' "AppyCtrl" is a wrong name + wrong role, superseded by AppyRadar).

- **The runtime: Marshall → Swagger → workflow/sub-agent (Conductor / job-agent / execution)** — three layers. **Marshall (the Conductor)** is David's single daily orchestrator, lives in the Watchtower, holds the single Monitor, *routes* problems to jobs and dispatches each to a job-agent — it routes, it does not coordinate (jobs are independent), and it is the **only thing that runs `claude` and the only thing that kills** (`tmux kill-window`). **Swagger (the job-agent, one per job)** owns a single problem with *judgment*: runs a workflow and/or spins up sub-agent panes, listens to results, decides if more is needed; isolated, never coordinates with other Swaggers, reports up. **Workflows & sub-agents** are execution — a workflow is just a longer, more-deterministic version of an agent-in-a-pane, so Swagger chooses per step: deterministic route (workflow) or flexible agent (pane). HITL lives at **Marshall's gates between Swagger jobs**, never inside a Swagger. Skills: `.claude/skills/{marshall,swagger,millwright,conductor,...}/`. See `docs/runtime-model.md`.

- **The Three Roles of the floor (Library / Warehouse / Platform)** — the floor itself has three coexisting roles. **Library** = `canonical/` (one winner per capability station, David's voice, provenance + verbatim sources). **Warehouse** = `research/` + upstream provider repos at `~/dev/upstream/repos/` (raw material, alternatives, history). **Platform** = `.claude/workflows/` + the Workflow Tool runtime + the watchtower-engine trigger loop (the factory that creates/runs/evaluates/promotes). Platform reads Warehouse, produces Library, uses Library to do production work. A fourth area, **Intake** (`backlog/` + `experiments/`), is the open front door where raw ideas/papers/others' work land before a validation gate lets *validated* learning cross into Warehouse/Library — anything can enter, nothing is trusted (`docs/intake.md`). Cutting across all of it: **human communication is first-class, both directions** — audio (talk to steer; events/summaries/sound-cues back) and visual (Mochaccino learnings + Watchtower) — see `docs/human-comms.md`.

- **Canonical artifact (a folder, with variants)** — `canonical/<type>/<name>/` containing `SKILL.md` (current winner, David's voice, **stack-agnostic**), `provenance.json` (rewrite chain + `winner_mechanism` + `version_history`), `_source/` (verbatim copies of every origin file), and an emerging `variants/` subdir (runners-up, demoted-canonicals). `canonical_id` follows `<domain>.<lane>.<station>` (e.g. `software.dev.code-review`); variants append `.<provider>.v<n>`. When a challenger beats canonical via shadow-run evidence, the new variant promotes to top-level `SKILL.md` and the old canonical demotes to `variants/was-canonical-<date>.md`. **No artifact is ever destroyed** — the library is a layered cake of historical winners. A canonical without `provenance.json` + `_source/` is, by spec, a *draft*, not a canonical.

- **The provenance chain + 5 evaluation levels** — assessment is a pipeline, not a one-time pass. **L0 Repo Scorecard** (`research/repos.jsonl`). **L1 Census** (`level-1-census.workflow.js` → `research/census.jsonl`; verdict ∈ {adopt, evaluate, skip, defer}). **L2a Triage** (qualitative scorecard → `research/evals.jsonl` + `research/evaluations/`). **L2b Rollout** (run the skill on held-out tasks, score outputs — *infrastructure not yet built*). **L3 Distillation** (one per cluster, requires complete L2 coverage — the 76 existing distillations are **provisional**, written before L2 was complete). **L4 Ratification** (HITL gate). `provenance.json` records, per origin, the `kept` / `modified` / `set_aside` trichotomy — `set_aside[]` (what was deliberately *not* used) is the highest-signal audit surface. Every `_source/` file must be referenced by ≥1 `origins[i].verbatim_copy`; orphans fail validation.

- **Workflow Tool + in-session execution (the runtime substrate)** — Dark Factory's primary substrate is Anthropic's **Workflow Tool** (deterministic JS orchestrator: `agent()`, `parallel()`, `pipeline()`, `phase()`, `schema`, `budget`), a *code wrapper* that passes state through plain JS variables and spawns fresh-context subagents per `agent()` call. It runs **inside an interactive Claude Code session, never headless** — there is no detached `node` that runs a `.workflow.js`. The **Blackboard** (bash+jq+curl conductor + append-only EAV store, `experiments/ylo/blackboard/`) remains useful for HITL-heavy/store-granular flows where the Workflow Tool's "no filesystem in the VM" penalty dominates (5× slower on store-heavy probes); the **MCP Blackboard pattern** (`spikes/blackboard-mcp/`, R11–R14 PASS) bridges them. Pick substrate by I/O shape, not preference.

- **The watchtower-engine trigger loop (built + proven)** — `experiments/watchtower-engine/` is a directory queue (`queue/ → running/ → done/|failed/`) whose mutex is `rename(2)`: claiming atomically `mv`s the oldest entry from `queue/` to `running/`. **Proven and live** — the reaper ran unattended (2026-06-07) and 35 jobs have flowed through `done/`. A queue entry names `kind` (workflow | skill | instruction), `workflow`/`harness`/`skill`/`prompt`, `experiment_id`, `args`. **⚠️ The README is stale** (says "not yet run") and still describes the dead "4 staggered sessions" model.

- **Backlog item (the PO↔Dev bridge)** — `backlog/YYYY-MM-DD-<slug>.md`, written from a brain conversation (PO side, `~/dev/ad/brains/`), executed in this repo (Dev side). Specs that aren't yet ready to build are stored under `backlog/specs/` (Symphony-shaped) for future ticketing. A dev/Marshall session opens the repo, picks the highest-priority item, executes.

How they compose: David talks to **Marshall**, who turns a problem into a job-ticket and dispatches a **Swagger**, which runs a **workflow or sub-agents** on the **floor** (Library/Warehouse/Platform), with state living in **Switchboard** and the human deciding at **Watchtower**. For Path-2 cargo specifically, a backlog item authorises folding N **origins** (verbatim → `_source/`) into one **canonical** with a full **provenance chain**, gated by L4 ratification. The factory eats its own dog food: its first production work is the workflows that maintain the factory.

## Key Workflows

### Direct the factory by talking to it (the North-Star loop, Path 1 — being built)
1. David talks to **Marshall** (the Conductor session, in the Watchtower).
2. Marshall decides what's a job, writes a schema-valid ticket into the queue (the **Producer**, C2).
3. A watcher (Marshall, holding the single Monitor) wakes on the ticket and **dispatches** a **Swagger** by `tmux new-window "claude '<swagger prompt>'"` (the **Trigger**, C3 — `tmux` is the spawn mechanism because a session can't conjure a new pane).
4. The Swagger owns the job: claims the ticket (`rename(2)` mutex), runs the named workflow inline via the Workflow Tool and/or spins sub-agent panes, writes a **run record**, and writes a **reports/ handback**, then lands the ticket in `done/`.
5. Marshall **verifies the artifact** (never trusts a "done" message), `tmux kill-window`s the Swagger on `done/` landing (the **return leg / reaper**, C4), and surfaces a one-line "what ran" so nothing is silent.
6. **Build spine status (C1→C5):** C1 (consumer runs one job by hand) ✅ done 2026-06-05; C2 producer 🔨 next; C3 Marshall auto-wake ❌ unwired (the Switchboard queue-topic → Monitor synapse was never connected — the #1 blocker per AUDIT-2026-06-12).

### Run a job through the watchtower-engine queue (in-session, on subscription)
1. A queue entry is written into `experiments/watchtower-engine/queue/` (by hand, by Marshall, or eventually by a Switchboard `POST /jobs` / Watchtower "Run" button).
2. In an interactive session, the `run-next-workflow` skill calls `bin/claim-next.sh`, which `rename(2)`-moves the oldest entry to `running/` (the atomic claim). Empty queue → stop.
3. The skill runs the named workflow **inline** via the Workflow Tool (visible in `/workflows`), writes a run record to `runs/`, writes a `reports/` handback, then moves the entry to `done/` (or `failed/` on error — never left in `running/`).
4. The result surfaces; the parent experiment shows on Watchtower's Today screen as "needs decision."

### Level 1 census run (Path 2 cargo — the deferred pipeline's first stage)
1. Read a batch of artifact IDs from `research/artifacts.jsonl` (the 1,150-row discovery output).
2. `level-1-census.workflow.js` fans out via `pipeline()` (5 agents/batch), each producing a schema-validated census record.
3. Append records to `research/census.jsonl`. Live progress at `mochaccino/designs/09-census-progress/`. Batches 0–1 complete (10 records, 4 adopt / 6 evaluate); ~1,140 remaining.

### Ingest one canonical artifact end-to-end (Path 2 cargo — PO authors backlog → Dev produces ratified canonical)
1. PO writes `backlog/<date>-<slug>.md` naming target canonical_id, distillation source, origin list, acceptance criteria.
2. Dev reads referenced distillation + evaluations + `research/insights.md`; copies each origin verbatim to `_source/<repo>--<file>.md`.
3. Dev drafts `provenance.json` (`rewrite_status: draft`); writes `SKILL.md` per `docs/canonical-form-spec.md` (four-field frontmatter, **trigger-only** description, David-pattern body) → flips `in-style`.
4. Dev refines `kept`/`modified`/`set_aside` per origin; runs the ratification checklist; flips `ratified`; appends to `canonical/INDEX.md`; renames backlog item to `backlog/done/` with a `## Result` section. The HITL gate sits between draft and ratify. Two workflows (`prepare-ingestion-brief`, `ingest`) are designed to automate steps 2–4 but **not yet built**.

### Decide the FORM of new machinery (millwright gate)
1. Before building any factory capability — or the moment you catch yourself about to hand-perform a task — invoke the `millwright` skill.
2. It decides the form (skill / `workflow.js` / agent-job / improve-existing / combo) and enforces "build the machine, not the one-off": the spec David gives is the blueprint for the *system*, the test payload is not the deliverable.

### Visual decision-support (Mochaccino)
1. Restart if needed: `cd mochaccino && nohup python3 -m http.server 7420 > .serve.log 2>&1 &`.
2. Open `http://localhost:7420/designs/` — gallery. Designs render from JSON in `mochaccino/data/` (prose → Peter→JSON → Mocha→HTML, MVC); never hand-edit HTML to reflect new data — refresh data and re-render. Mochaccino is David's prose→visual documentation engine (NOT mermaid, NOT in-app).

## Design Decisions

- **Build the machinery first; the content is cargo (Path 1 before Path 2)**: the factory is the durable asset, the 1,100-artifact library is just the first cargo it carries.
  - *Alternative considered*: grind the census/ingestion by hand now (it's "real work" with visible output).
  - *Why rejected*: hand-grinding cargo builds no factory. Building the factory makes the cargo — and everything after — something you can just ask for.

- **Direct-by-talking, in interactive sessions, never headless/metered (the in-session model)**: all execution runs in an interactive `claude` session on the Max subscription. **As of 2026-06-15, `claude -p`/headless/SDK-mode runs on a separate *metered* API credit pool, not the Max plan** (proven on Roamy; the `$x.xx` an interactive session shows is notional, not a charge).
  - *Alternative considered*: headless workflow execution, cron/API scheduling, or shell-exec spawning `node`.
  - *Why rejected*: the Workflow Tool runs *inside* a Claude session (headless was never verified to work); `-p`/SDK silently moves execution onto metered billing; cron is off the table on the Max plan. In-session keeps it free, visible in `/workflows`, and survives crashes because the queue files are the audit trail.

- **One watcher (Marshall) routes to isolated Swaggers — the "4 staggered sessions" model is dead**: a single Monitor on Marshall dispatches each independent job to its own isolated Swagger.
  - *Alternative considered*: a `/loop` + `rename(2)` mutex across up to 4 self-watching sessions draining one queue.
  - *Why rejected (2026-06-05)*: competing self-watchers don't distribute work — one fast session hogs the queue; the mutex gives *correctness*, never *fairness*. The mutex is kept only as a safety net. (The engine README still describes the dead model — known drift.)

- **Stateless replaceable floor + state in services (the constellation split)**: shared coordination state (pool/claims/liveness) lives in Switchboard/AngelEye/AppyRadar; the floor is a stateless client. "Second orchestrator" means N thin clients on one state plane, not repo-cloning.
  - *Alternative considered*: solve coordination, locking, and shared state inside the engine/agent on the floor.
  - *Why rejected*: a floor that owns state can't be replaced or parallelised cleanly. Pushing state to services makes the floor disposable and parallelism an identity-partitioning problem, not a locking problem. This split is green-field — no OSS fleet-orchestrator ships it (closest: CAO / Composio / ccswarm; Ruflo is the inverse, central state).

- **Sensors read and make queryable; control acts elsewhere (read-vs-control); Marshall is the only killer**: AngelEye and AppyRadar observe and answer queries (including emitting *detection* events like `session.stale`); they never kill, delete, or mutate.
  - *Alternative considered*: a "killer sentinel" (the mis-named "AppyCtrl") that reaps dead processes.
  - *Why rejected*: process-tree reaping was proven a dead end (claude reparents to its daemon); and mixing observe + act corrupts a sensor's identity. Acting (`tmux kill-window`) belongs to **Marshall** alone; Switchboard may requeue its *own* state but never touch the external world.

- **Cleanup/wake is harness-driven, not remembered (the one unifying mechanism)**: *Sentinel pushes topic-filtered SSE → an in-session Monitor (`persistent: true`) subscribes → it wakes Marshall/Swagger → the agent acts.* A durable write side + reactive listen side.
  - *Alternative considered*: rely on the agent to remember to poll / clean up stale state.
  - *Why rejected*: the worker skips its own bookkeeping (proven repeatedly — see Failure Modes). One reactive pattern solves four problems at once (external wake #15, Marshall auto-wake C3c, result return #19, process-watch #8).

- **Provenance as schema-validated JSON + verbatim `_source/` + `kept/modified/set_aside`**: every origin is copied byte-for-byte and every choice (including discards) is recorded in a validatable schema.
  - *Alternative considered*: link to upstream commit URLs + free-form prose credits.
  - *Why rejected*: upstream files get force-pushed/deleted/moved (a link is a promise, a copy is an artifact); prose can't be validated or diffed and rots silently; the discarded `set_aside[]` ideas are the highest-signal review surface and vanish without a schema slot.

- **One winner per station + all alternatives kept (canonical + `variants/`); bounded edits on ratified artifacts (SkillOpt)**: name one canonical, retain every variant; iterate ratified artifacts with bounded add/delete/replace edits only, accepted only on held-out improvement.
  - *Alternative considered*: flat variant set with no canonical / free re-authoring on taste shifts.
  - *Why rejected*: a flat set gives agents no default production line; free re-authoring loses the optimisation signal (SkillOpt: text-space optimisation only beats baseline when edits are bounded).

- **Trigger-only descriptions + stack-agnostic bodies in canonical SKILL.md**: the YAML `description` is a routing condition (`"Use when…"`, ≥3 trigger phrases), never a summary; the body never names a language/framework.
  - *Alternative considered*: descriptive paragraph + stack-specific examples for clarity.
  - *Why rejected*: only `name`+`description` enter context at session start under lazy loading — a summary lets the LLM skip the body; stack lock makes a skill un-composable. The mechanism is extracted stack-free; the lift is recorded in `origins[].modified[]`.

- **Fix the class, not the instance; good/bad is a hypothesis**: every fix weighs system cohesion (output is often a workflow/skill/agent), but pick the *smallest* move that fixes the class; David reports feelings, not verdicts, so every good/bad is a claim to validate, not a mandate to ship.
  - *Alternative considered*: patch each instance as it appears / treat David's reaction as a spec.
  - *Why rejected*: instance-patching is whack-a-mole; a sycophant who ships a single situated preference as a universal rule creates ten new problems (recorded failure F-20260608-06). See `docs/systemic-fixes.md`.

## Non-obvious Constraints

- **"Watchtower" means three different things** (the single biggest source of confusion, AUDIT Drift #1): **(a)** the *control surface* concept (decision queue, `rename(2)` engine) described in the brain; **(b)** the *app* `apps/watchtower/` — a one-commit RVETS scaffold that implements none of (a); **(c)** the *engine* `experiments/watchtower-engine/` — where the atomic claim actually lives and works, plus the live board on `:7430`. Docs describe (c) but file it under a name pointing at the empty (b). When someone says "Watchtower," disambiguate which.

- **The system is single-writer by design but nobody enforces it.** A second session doesn't get blocked — it silently corrupts shared files. This is why "two sessions always conflict." Parallelism is an *identity/partition* problem (different lanes, worktrees, then Switchboard), not a locking one.

- **No loop is closed end-to-end yet.** Every sentinel *collects* and *exposes*; nothing *delivers* or *consumes*. The collect/expose half is built and tested in five places; the deliver/consume wire is the blocker every time (Switchboard accepts jobs but nothing reaps the queue; appyradar-sentinel has `transport: []`; the Watchtower app has no persistence). "Self-managing" can't happen until those wires are run.

- **Workflows do NOT run headless.** Watchtower's "Run" button only *writes a queue entry*; an in-session skill is what runs the workflow. Anyone designing "click → workflow runs autonomously" is designing a different app than the one that exists.

- **Never use `claude -p` / Agent SDK for factory execution** — metered billing since 2026-06-15. The entire in-session model exists to stay on the Max subscription. Spawn Swaggers with interactive `claude "<prompt>"`, never `-p`.

- **An entry left in `running/` is stranded.** No session re-claims from `running/`; a crash mid-run leaves it owned-but-dead until a human `mv`s it back to `queue/` or `failed/`.

- **Interactive Claude does not exit after its turn**, so a spawned Swagger window won't self-close — completion = the ticket landing in `done/`, and the watcher (Marshall) `tmux kill-window`s it. Do not "fix" the non-exit with `-p`.

- **Workers skip their own bookkeeping.** Recorded ≥4×: Swaggers wrote no run record and/or no `reports/` handback even when the ticket explicitly forbade the skip. Do not trust the worker to self-instrument; observe the loop externally. Every factory failure is recorded in `experiments/watchtower-engine/failures/register.jsonl` via `record-failure.sh` (investigate a category at 3–4 instances).

- **Headless screenshots / HTTP-200 / tag-counts are NOT visual verification.** F-20260608-04: designs were claimed "verified/love-tier" from headless captures while David's real browser showed broken/blank/stale pages. Visual review means a real browser + console check.

- **Re-rendering a Mochaccino design at the same URL cache-poisons the human reviewer** (F-20260608-05): the Python server sends no cache-control and views fetch data without `?v=hash`, so returning visitors see stale pages while files are correct. A render/lint gate must screenshot the gallery **index** + every linked page, not just ticket-named artifacts (cortex v4 missed the index; David caught it).

- **Two live copies of the Marshall skill** (AUDIT Drift #6): `experiments/watchtower-engine/skills/marshall/` (stale spike) and `.claude/skills/marshall/` (hardened, live — the one that runs). Edit only the latter.

- **`research/` is frozen and externally referenced.** Moving/renaming anything under `research/recon/`, `research/distillations/`, or `research/evaluations/` breaks the catalog SKILL at `~/dev/ad/appydave-plugins/.../dark-factory-catalog/` and the brains-side compat symlink (`~/dev/ad/brains/agentic-factory/dark-factory-catalog/` → `apps/dark-factory/research/`).

- **`canonical/` is staging, not deployment.** Ratifying does not install a skill anywhere; migration to appydave-plugins is a separate deliberate copy step.

- **The 76 distillations are provisional, not authoritative** — written with incomplete L2 coverage; do not ingest from one until its cluster's L2 coverage is complete.

- **The Workflow Tool VM has no filesystem access** (every store op = a full agent round-trip, root of the 5× store-heavy penalty) and **env-var inheritance is fragile** (`CLAUDE_CODE_WORKFLOWS=1` drops across surfaces — persist it in `.claude/settings.local.json`; API keys don't flow to subagents).

- **`origins: []` is forbidden** even for from-scratch canonicals (record what you considered and chose not to use as empty-`kept[]`/populated-`set_aside[]` origins); **no orphan `_source/` files**; **ratified artifacts are immutable in place** (bump `version` + append `version_history[]` or the diff silently lies).

- **AppyRadar ≠ "AppyCtrl".** ~10 older backlog/spec docs say "AppyCtrl" and describe a process-killer; that name and role are both wrong — read AppyRadar (read-only fleet sensor) and discard the killing role. Also: `~/dev/baku/b-appy-radar` is only a UI mock, not the real app. The GitHub repo is `appyradar-sentinal` (missing 'e' — a carried typo).

- **Several READMEs lie about state** (AUDIT): the engine README under-claims ("not yet run" vs 35 jobs in `done/`); Switchboard's README under-claims by an entire build (says "walking skeleton" vs a running service with SSE+replay, queue persister, MCP server); appyradar-sentinel's "proven live 2026-06-11" outruns the evidence (only commit is an `Initial commit — clean re-scaffold` at that timestamp). Verify against code/git, not READMEs.

## Expert Mental Model

- **Dark Factory is an agentic MES, not "an orchestrator."** The expert frame is a Manufacturing-Execution-System + control plane: a *stateless, replaceable floor* with coordination state in services. "Just make the agent smarter" is the beginner's reflex; the expert moves state out of the floor and closes wires between boxes.

- **The blocker is never "better AI" — it's the missing deliver/consume wire.** Read the audit's state map and every row has the same shape: collect ✅, expose ✅, deliver ❌. The expert hunts for the one unrun wire that turns two boxes into a loop, not for a model upgrade.

- **Marshall routes; it does not execute, and it does not coordinate a team.** The novice asks Marshall to do the work inline; the expert has Marshall dispatch a Swagger and then *verify the artifact*. Jobs are independent — there is no cross-job team, only isolated Swaggers reporting up. HITL happens at the gates *between* jobs.

- **Files are the source of truth; apps are disposable projections.** Deleting any Watchtower index is harmless — it rebuilds from the YAML/JSON records + the engine's `runs/`. Never treat app state as authoritative.

- **Observe the loop externally; don't trust the worker's self-report.** The worker skips its own bookkeeping and reports "done" when it isn't. The expert instruments the dispatcher/reaper/AppyRadar → Switchboard log → Watchtower, and verifies in a real browser, not from a screenshot.

- **Build the machine, not the one-off.** The spec David gives is the blueprint for a *system* (skill/workflow/agent); the test payload is not the deliverable. "I should just do this task" is the beginner's reflex; the expert reaches for `millwright` and asks "should this be a dispatched job / a workflow / a skill?"

- **The provenance chain is the product (Path 2).** The audit chain — every choice auditable back to verbatim source — is the only thing that justifies re-authoring 1,100 skills instead of using them in place. The rewrite is incidental; provenance is the moat. `set_aside[]` carries the highest-signal review surface.

- **Canonical is the *current* winner, not the *only* winner; a canonical is a folder, not a file.** "What's the canonical?" has a current answer, not a permanent one — `SKILL.md` + `provenance.json` + `_source/` + `variants/` is one atomic unit.

- **Self-learning is part of every conversation, and the trigger is the weak link.** Persist learnings durably at milestones and before session end (litmus: a cold restart loses nothing). Storage is solved; *remembering to persist* is the failure point — David wants a clean close → handover record → fresh window, NOT compaction.

- **Lead with a recommendation, not a menu.** David hates AskUserQuestion menus; lead with your take, which he approves with "go." One-word replies are trust, not disengagement. Be a conductor, not a waiter — after each step, pick the next move and start; only pause for a real blocker.

- **Good/bad is a hypothesis; don't over-generalize one signal.** David reports feelings; a single situated preference is not a universal rule (recorded failure: promoting "shapes are nice" to an SVG-first engine). HTML is AppyDave's medium; shapes/diagrams are sparing annotation chosen by judgment.

## Scope Limits

- Does NOT run workflows headless or via metered billing — execution is always in an interactive session on David's subscription, never `claude -p`/SDK (metered from 2026-06-15), never cron/API (Max plan).
- Does NOT let sensors act — AngelEye and AppyRadar are read-only (observe-and-tell, including detection events); killing/reaping is Marshall's alone; Switchboard CRUDs only its own queue/state.
- Does NOT let Watchtower write to `canonical/` — it records *decisions* (`promotion.yml`/verdicts); a human performs the library edit.
- Does NOT install canonical skills into Claude Code — migration to appydave-plugins is a separate deliberate copy step, not a consequence of ratification.
- Does NOT auto-generate canonicals from `artifacts.jsonl` — every canonical needs a human-authored backlog item; the 76 distillations are inputs to that decision, not decisions.
- Does NOT manage upstream repos — `~/dev/upstream/repos/<repo>/` are read-only inputs.
- Does NOT own the constellation's sibling services — Switchboard, AppySentinel, AppyRadar, AngelEye live in their own repos (`apps/switchboard`, `apps/appysentinel`, `apps/appyradar-sentinel`, …); `apps/watchtower` is the only app nested here, and it may relocate.
- Does NOT own skill-usage / session telemetry — AngelEye owns session liveness; AppyRadar owns machine/fleet resource intel; this repo consumes, it doesn't collect those.
- Does NOT replace POEM or AWB — they are upstream authoring/runtime; the YLO→POEM blueprint makes dark-factory a `.poem/` consumer, not a reimplementation.
- Does NOT auto-restart the Mochaccino server (`:7420`) — human-managed.
- Does NOT support multi-user/mobile/shared sessions — single-user (David), localhost, desktop browser; hard cuts, not deferred features.

## Failure Modes

- **Bookkeeping skip (DF-3, the recurring one)**: a Swagger lands a ticket in `done/` but wrote no run record and/or no `reports/` handback — even when the ticket flagged it as watched. Recognition: empty `runs/` or `reports/` for a completed `done/` entry. Recorded ≥4× (F-20260608-01/02/03/07). Fix: harness-enforce the handback (not "remember to"); record every instance via `failures/record-failure.sh`.
- **False verification**: a result claimed "verified/love-tier" from headless screenshots + HTTP-200 + tag-counts while the real browser shows broken/blank/stale (F-20260608-04). Recognition: no real-browser open, no console check. Fix: visual review = real browser; a render/lint gate must cover the gallery **index** + every linked page.
- **Stale-cache on re-render**: re-rendering a design at the same URL shows returning visitors old/half-built pages while files are correct (F-20260608-05). Cause: no cache-control headers + no `?v=hash`. Fix: version the fetch or bust the cache; never trust "looks old" without a hard refresh.
- **Over-generalized feedback**: a single situated preference promoted to a universal skill mandate, silently shifting the AppyDave style David never asked to change (F-20260608-06). Recognition: a skill edit that changes the default engine/output from one comment. Fix: treat good/bad as a hypothesis; change the smallest scope.
- **Open wire / unclosed loop**: a component collects and exposes but nothing consumes (Switchboard queue with no reaper; appyradar `transport: []`). Recognition: data flows to a box and stops. Fix: run the deliver/consume wire — this is the system's #1 blocker, not an AI gap.
- **Silent multi-writer corruption**: a second session edits shared files and quietly corrupts them (no block, no error). Recognition: unexplained file drift after parallel sessions. Fix: partition by identity/lane/worktree; route shared state through Switchboard.
- **Stranded `running/` entry**: a ticket sits in `running/` after the skill returned (crash mid-run). Recognition: neither `done/`/`failed/` nor re-runnable. Fix: `mv` back to `queue/` or to `failed/`.
- **Metered-billing trap**: a trigger path uses `claude -p`/SDK. Recognition: silent until billing — runs that "worked" start costing. Fix: route all execution through interactive in-session runs.
- **Spawned window never closes**: a Swagger tmux window sits at the REPL after its job. Recognition: window open with the ticket already in `done/`. Fix: Marshall `tmux kill-window`s on `done/` landing; don't switch to `-p` to force exit.
- **Doc-vs-reality drift**: a README/memory asserts a state git/code contradicts ("not yet run" vs 35 done; "walking skeleton" vs a running daemon; "proven live" vs an initial-commit-only repo). Recognition: claim outruns evidence. Fix: verify against code/git/test counts, not prose; correct the memory/README.
- **Orphan / missing verbatim source**: a `_source/` file with no `origins[i].verbatim_copy`, or an origin referencing a `_source/` file that doesn't exist. Recognition: provenance validation rule 4 / ratification checklist fails. Fix: add the origin entry, or harvest/remove the file.
- **Description-as-summary regression**: `description:` reads like marketing instead of a trigger condition. Recognition: silent — YAML loads but the body never fires. Fix: `"Use when…"` with ≥3 trigger phrases.
- **Stack-named in a canonical body**: `npm test`/`rspec`/`pytest`/framework paths in a canonical (`style-check.py` doesn't exist yet, so it passes ratification by accident). Recognition: silent until composability fails. Fix: project-neutral phrasing; record the lift in `origins[].modified[]`.
- **In-place edit on a ratified artifact**: a ratified `SKILL.md` edited without bumping `version`/appending `version_history[]`. Recognition: `git log` has the diff, `provenance.json` denies it. Fix: bump version, append a history entry, treat as the next version.
- **Workflow Tool gotchas**: env-var drop ("Workflow tool exists but is not enabled") → persist `CLAUDE_CODE_WORKFLOWS=1`; `parallel([agent()])` runs nothing → wrap in thunks `() => agent()`; phase mismatch → `agent({phase})` must exactly match `meta.phases`; mid-run script edits don't apply → the script is snapshotted at launch; `resumeFromRunId` drops args → re-pass them.
- **Mochaccino server stopped**: `http://localhost:7420/designs/` refuses connection. Fix: `cd ~/dev/ad/apps/dark-factory/mochaccino && nohup python3 -m http.server 7420 > .serve.log 2>&1 &`.
- **Research path drift**: a file under `research/recon|distillations|evaluations/` moved/renamed/deleted breaks the external catalog SKILL or the brains symlink. Recognition: "file not found" in an unrelated repo. Fix: restore the path; any genuine move is a coordinated change on both sides + an `INDEX.md` schema-history entry.
