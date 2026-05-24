# Dark Factory — Architecture

**Status**: living document — first complete statement, will evolve
**Last updated**: 2026-05-25
**Companion docs**: `experiments/ylo/README.md`, `workflow-tool-authoring-notes.md`, `canonical-form-spec.md`, `provenance-spec.md`, `ingestion-workflow.md`

---

## 1 — What Dark Factory is

Dark Factory is **a self-improving capability factory**.

It runs autonomously, observes itself, harvests new capabilities from upstream sources, benchmarks them against the current production line, and promotes the winners. The output is a continuously improving library of skills, agents, workflows, and commands — each one provably the current best version available, with full provenance back to every source it was derived from.

It is *not* a static skill collection that gets updated when someone remembers. It is *not* a hand-rolled methodology library. It is a factory with lights-off operation, a warehouse of raw material, and a watchtower for human insight.

### Three roles, not one

Earlier framings collapsed Dark Factory to "skill library" or "workflow platform." Neither was right. The system has three coexisting roles:

1. **The Library** — `canonical/`. The current production line. One winner per station, with receipts back to every alternative it beat.
2. **The Warehouse** — `research/` + upstream provider repos. All the raw material, all the alternatives, all the not-yet-canonical variants.
3. **The Platform** — `.claude/workflows/` + the runtime. The factory that creates, runs, evaluates, and promotes.

You don't pick between them. They're three layers of the same thing. The Platform reads from the Warehouse, produces the Library, and uses the Library to do the production work.

---

## 2 — Metaphor: Factory, Warehouse, Watchtower

The system is shaped by three named structures, each with a specific job.

### The Factory (autonomous)

The factory floor runs **dark** — lights off, no humans on the floor. Workflows execute as deterministic JavaScript orchestrators that fan work out to fresh-context subagents. The Workflow Tool is the runtime substrate; the workflow file IS the orchestrator.

Inside the factory:
- **Domains** — high-level concerns (YouTube Launch, SDLC, KDD, Brand)
- **Lanes** — sequences within a domain (e.g., YouTube Launch has content-analysis, titles, thumbnails)
- **Stations** — discrete work units within a lane (e.g., title generation, thumbnail rendering)
- **Variants** — interchangeable implementations of a station (e.g., title-gen.osmani.v1, title-gen.gsd.v2)
- **Steps** — the atomic agent calls inside a station

A station can be powered by: a single agent, a multi-agent parallel team, a pipeline stage, a budget-bounded loop, a human-gated sign-off booth, or a hybrid.

### The Warehouse (continuously refreshed)

`research/` holds 1,100+ artifacts from 14 upstream provider repos (BMAD, GSD, SpecKit, Osmani, Claude Superpowers, Compound Engineering, gstack, gbrain, AppyDave Plugins, POEM, Compound Knowledge, Ruflo, matt-pocock-skills, ray-amjad/claude-code-workflow-creator).

Each provider has its own "room" (subdirectory) with:
- A recon report (`research/recon/<provider>.md`) — capability inventory
- Evaluations (`research/evaluations/<artifact>.md`) — quality scorecards
- Distillations (`research/distillations/<cluster>.md`) — merged-write-up per cluster
- Verbatim source copies (preserved, never lost)

The warehouse is refreshed by **Upstream Pulse** — a scheduled workflow that polls each provider's git log, recons new artifacts, and registers them as candidate variants.

### The Watchtower (human insight, no floor control)

The watchtower is glass-walled. You can see everything: which workflows ran, which variants won, which stations are bottlenecks, which agents failed, what each run cost. But you don't reach onto the floor. You don't lift levers. You read the dashboard, tune the rubrics, propose new stations, override the occasional bad promotion.

The watchtower is implemented as:
- The `store.jsonl` per-run logs (already exist)
- Projection scripts that aggregate across runs (to build)
- Live dashboards via AngelEye (to wire up later)

### Sign-Off Booths (HITL, by design)

Some stations *require* a human. Not as an override — as part of the station definition. YouTube title selection is one (you choose the title). Skill ratification is another (you approve the canonical artifact before it lands). Production code merges may be another.

These are inside the factory, not outside it. The factory's design says: "this station has a human gate." It blocks until the gate passes. That's deliberate, not a failure of automation.

---

## 3 — The Library: Canonical with receipts

`canonical/` holds the **current winner** per station — David's voice, stack-agnostic, fully spec-compliant.

But "winner" is dynamic. Each canonical artifact has:

```
canonical/skills/code-review/
├── SKILL.md                       ← the current winner
├── provenance.json                ← full chain: which variants this beat, when, why
├── _source/                       ← verbatim copies of every origin file
│   ├── osmani--code-review.md
│   ├── gsd--reviewer.md
│   └── bmad--qa-agent.md
└── variants/                      ← runners-up, demoted versions, alternatives
    ├── gsd.v2.md
    ├── osmani.v1.md
    └── was-canonical-2026-04-12.md
```

When a new variant arrives (from upstream or self-improvement), it doesn't replace canonical immediately. It enters as a `variants/` entry and waits to be benchmarked. When it beats canonical by enough rubric evidence, the swap happens:
1. Old canonical demoted to `variants/was-canonical-<date>.md`
2. New variant promoted to top-level SKILL.md
3. `provenance.json` updated with the promotion event

**No artifact is ever destroyed.** Every variant stays available. The library is a layered cake of historical winners.

### Naming

The ChatGPT architecture proposes `software.dev.unit-test-generation.osmani.v1`. Dark Factory adopts a similar convention internally:

- **Canonical ID**: `<domain>.<lane>.<station>` (e.g., `software.dev.code-review`)
- **Variant ID**: `<canonical_id>.<provider>.v<n>` (e.g., `software.dev.code-review.osmani.v1`)
- **File path**: `canonical/skills/code-review/` (human-friendly, the ID is in provenance.json)

The dotted notation lives in metadata; the directory tree stays clean.

---

## 4 — The Platform: Workflow Tool as the runtime

Dark Factory builds on Claude Code's **Workflow Tool** — Anthropic's deterministic multi-agent orchestrator. Why this matters:

- **Code wrapper, not model wrapper**: a workflow file passes state through plain JavaScript variables. No Claude orchestrator in the middle re-reading and re-tokenizing every intermediate. This is the central architectural win the YLO experiments validated.
- **Fresh-context subagents**: every `agent()` call spawns a clean Claude. No context pollution, no compaction loss, no "the orchestrator forgot the task."
- **Native primitives**: `agent()`, `parallel()`, `pipeline()`, `phase()`, `log()`, `schema`, `args`, `budget`. Combine in plain JS.
- **Resumability built in**: if a workflow dies halfway, cached agent results replay instantly on resume.
- **Schema enforcement**: agents retry up to 3× to match the declared schema. Saves error-handling code.

The blackboard substrate (conductor + store + image-gen skills) is still useful — for HITL-heavy and store-granular flows where Workflow Tool's I/O overhead dominates. See `experiments/ylo/README.md` for the hybrid decision.

### Workflows we build vs workflows we run

There are two categories of workflow in Dark Factory:

**Production workflows** — what the factory exists to run.
- `ingest.workflow.js` — turn a backlog item into a canonical artifact
- `evaluate.workflow.js` — score a variant against canonical
- `promote.workflow.js` — swap a winner when evidence threshold is met
- `prepare-ingestion-brief.workflow.js` — fan-out read of relevant research material
- Plus all the YLO probes (`content-analysis`, `title-gen`, `titles-human`, `thumbnails`)

**Infrastructure workflows** — what the factory runs on itself.
- `upstream-pulse.workflow.js` — daily provider repo scan
- `framework-pulse.workflow.js` — daily Anthropic/community workflow pattern scan
- `shadow-scout.workflow.js` — recommend shadow injection points
- `shadowify.workflow.js` — transform a workflow to add shadow execution
- `watchtower-projection.workflow.js` — aggregate run telemetry into dashboards

These are written using the same primitives. The factory eats its own dog food — workflows that maintain workflows.

---

## 5 — Shadow Runs and Upstream Pulse: the self-improvement loop

Two patterns make the factory genuinely self-improving.

### Shadow Runs

When a workflow executes a station that has multiple known variants, it runs the canonical variant for real (its output flows downstream) and runs N challenger variants in parallel as shadows (their outputs are scored against a rubric, not used downstream).

```js
const result = await shadow({
  canonical: () => agent(canonicalPrompt, opts),
  challengers: [
    { name: "gsd.v2",   fn: () => agent(gsdPrompt, opts) },
    { name: "bmad.v1",  fn: () => agent(bmadPrompt, opts) },
  ],
  rubric: rubricSpec,
})
// result.canonical = output flows downstream
// result.shadows = [{ variant, output, score, reasoning }, ...] → logged, not returned
```

Over time, evidence accumulates. When a challenger beats canonical by enough margin over enough runs, the promotion workflow fires.

**Two evaluation modes:**
- *Isolated grade* — rubric scores the challenger's output alone. Cheap. Run often.
- *End-to-end shadow* — run the entire downstream chain on the challenger's output. Expensive. Run when a challenger is a serious promotion candidate.

**Cost discipline**: never shadow every step on every run. Sample (10% of runs), or restrict to high-value stations, or burst-mode when a new variant lands and needs fast evidence.

### Upstream Pulse

A scheduled workflow (cron) that:

1. For each provider repo in registry: `git fetch` + `git log` since last pulse
2. For each new artifact: run mini-recon, decide if it maps to an existing station
3. If existing station → register as new challenger variant in `variants/`
4. If new capability → flag in backlog for human review (might be a new station)
5. Write pulse-report to mochaccino

**Framework Pulse** is the same shape pointed at runtime/framework repos (anthropics/claude-code, ray-amjad/claude-code-workflow-creator, community workflow collections) to catch new primitives and patterns.

### The loop

```
Upstream Pulse → new variant lands in warehouse
              → Shadow Runs accumulate evidence over weeks
              → promotion workflow detects threshold crossed
              → canonical swap; old version demoted to variants/
              → next workflow run uses new canonical
              → Watchtower shows the scoreboard
```

No human in the loop for the routine case. Human only intervenes to approve new *stations* (genuinely new capabilities), override promotions if evidence looks fishy, or tune rubrics.

---

## 6 — The conversational layer: Penny, Alex, Oscar

Dark Factory has infrastructure but needs a human interface. The three POEM personas fit naturally:

| Persona | Role | What you ask |
|---------|------|--------------|
| **Penny** (Prompt Orchestrator) | Floor supervisor | "Run YLO on b65." "What's in flight?" "Why did the title-gen promotion fail?" |
| **Alex** (Prompt Architect) | Factory designer | "Design a workflow for X." "Should this be a workflow or a skill?" |
| **Oscar** (Prompt Engineer) | Mechanic | "The title-gen station is producing weak hooks — fix it." "Why is the recall agent double-nesting?" |

Penny knows the catalog and can sequence workflow runs. Alex helps design new workflows (uses ray-amjad's workflow-creator as a tool internally). Oscar maintains existing workflows — reads run logs, suggests prompt edits, tunes rubrics.

These are agents (`.claude/agents/`) that live in dark-factory and become the conversational interface. You talk to Penny in plain English; she calls the right workflows. You don't have to remember which `Workflow({name: "..."})` to invoke.

---

## 7 — Multi-machine architecture

Two machines, two specializations:

### M4 Pro = Warehouse Keeper

Runs continuously in the background.
- **Upstream Pulse** daily — git fetch + log on the 14 provider repos
- **Framework Pulse** daily — Anthropic claude-code, workflow-creator, community
- Recon/discover/distill on new artifacts
- Maintains `canonical/` as source of truth (writes the layered cake)
- Has Tailscale + SSH access from this machine

### This machine = Factory Floor

Runs on-demand for project work.
- Executes production workflows on real projects
- Reads latest `canonical/` from shared store
- Writes telemetry back to shared run-store
- Runs Shadow Runs when triggered
- Talks to Penny/Alex/Oscar

### Sync mechanism (v1)

Shared git repo via Tailscale. Warehouse Keeper pushes warehouse updates; Factory Floor pulls when it starts a workflow. No new infrastructure. When this gets unwieldy (likely a year out), evolve to a coordination service.

### Why this matters

The warehouse runs while you sleep. When you start a workflow at 9am, the canonical/ it reads is fresh as of last night's pulse. Self-improvement happens whether you're at the keyboard or not. The factory floor stays responsive because it isn't competing with continuous research for resources.

---

## 8 — Multi-project execution: CWD pattern, evolve to plugin

Dark Factory hosts the workflows centrally. Other projects use them by setting CWD.

**v1 (CWD pattern):**
```
cd ~/dev/ad/apps/some-app
claude
> Penny, run the code-review factory on this branch.
```

Workflows live in `~/dev/ad/apps/dark-factory/.claude/workflows/`. They use `process.cwd()` to know which project they're operating on. Workflows are project-agnostic; project context comes from where you launch.

**v2 (plugin pattern, later):**
Dark Factory becomes a Claude Code plugin. Other projects install it. Workflows are discoverable globally. More infrastructure, cleaner isolation. Adopt when v1 gets unwieldy (10+ workflows across 5+ projects).

**Never:** per-project copy. Workflows duplicate, drift, become unmaintainable.

---

## 9 — Telemetry: keep it boring

The Watchtower v1 reads `store.jsonl` files across all runs and projects a dashboard. No new infrastructure.

Every workflow already calls `remember()` for structured events. Every record has `meta.ts`, `meta.step`, `meta.attempt`, `meta.status`, `meta.by`. That's already telemetry — it just needs aggregation.

**v1 Watchtower projection**:
- Per-station: success rate, mean wall-clock, mean agent count, mean cost
- Per-workflow: run count, success rate, last run, top failure modes
- Per-variant: head-to-head scoreboards from shadow runs
- Cost report: tokens per day/week/month by workflow

**v2**: pipe into AngelEye for live dashboards.

What we don't build: a new logging infrastructure, a custom database, a metrics protocol. The JSONL store IS the metrics store. We project from it.

---

## 10 — Convergence with the ChatGPT architecture document

The architecture David drafted in ChatGPT (Universal Self-Improving Workflow Factory — Factory / Warehouse / Watchtower / Transpiler / Provider Model / Improvement Loop) is **this document's parent**. They describe the same system at different abstraction levels.

| ChatGPT concept | Dark Factory implementation |
|-----------------|------------------------------|
| Factory | `.claude/workflows/` + Workflow Tool runtime |
| Warehouse | `research/` + provider repos + Upstream Pulse |
| Watchtower | `store.jsonl` projections + AngelEye (later) |
| Transpiler | `ingest.workflow.js` (to build) — automates the 11-step procedure |
| Provider Manifest | `research/recon/<provider>.md` |
| Station Variant Registry | `canonical/<type>/<name>/variants/` |
| Improvement Loop | Shadow Runs + promotion workflow |
| Domain / Lane / Station | Same terminology, adopted |
| Data Model entities | Map to JSONL store keys (variant, run, evaluation, recommendation) |

Two divergences worth noting:

1. **The ChatGPT doc says "keep all variants, never collapse."** Dark Factory agrees, but reframes: keep one *canonical* (current winner) + N *alternatives* (in `variants/`). The library has a clear production line, but no historical variant is destroyed. Best of both.

2. **The ChatGPT doc treats the transpiler as automated.** Dark Factory's 11-step ingestion procedure is currently human-executed. The first dog-food workflow is the transpiler itself: `ingest.workflow.js` turns the procedure into a runnable workflow.

---

## 11 — What runs where: the system map

```
┌──────────────────────── M4 Pro (Warehouse Keeper) ────────────────────────┐
│                                                                            │
│  Scheduled (cron):                                                         │
│    upstream-pulse.workflow.js   ← daily provider git scan                 │
│    framework-pulse.workflow.js  ← daily Anthropic/community scan          │
│    promote.workflow.js          ← weekly evidence review + canonical swap │
│    watchtower-projection.workflow.js ← hourly dashboard refresh           │
│                                                                            │
│  Maintains: research/, canonical/                                          │
│  Pushes to: shared git (Tailscale)                                         │
└────────────────────────────────────┬───────────────────────────────────────┘
                                     │
                                     │ git pull on workflow start
                                     ▼
┌─────────────────── This Machine (Factory Floor) ──────────────────────────┐
│                                                                            │
│  On-demand (you invoke):                                                   │
│    Penny / Alex / Oscar (agents)                                           │
│       ↓ call                                                               │
│    Production workflows (ingest, evaluate, YLO probes, etc.)              │
│       ↓ uses                                                               │
│    canonical/<type>/<name>/SKILL.md  (current winner)                     │
│       ↓ writes                                                             │
│    store.jsonl  (per-run telemetry)                                        │
│                                                                            │
│  Pushes telemetry to: shared git                                           │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 12 — The road from here

Architecture is the destination. Sequence to get there:

**Phase A — Codify (this week)**
- ✅ Write this document
- Update `workflow-tool-authoring-notes.md` with video learnings (budget, pipeline streaming, 3× retry, model-per-phase, code-vs-model wrapper framing)
- Add ray-amjad/claude-code-workflow-creator as upstream provider #14
- Mark restructure backlog item done

**Phase B — First dog-food (next week)**
- Build `.claude/workflows/prepare-ingestion-brief.workflow.js` (small, validates the pattern)
- Build `.claude/workflows/ingest.workflow.js` (the transpiler)
- Run it on `code-review` → first canonical artifact + first proof the platform works

**Phase C — Separate the machines (week after)**
- Set up M4 Pro as Warehouse Keeper
- Move Upstream Pulse there
- This machine focuses on factory runs

**Phase D — Watchtower projections (later)**
- Write the projection scripts
- Wire into mochaccino

**Phase E — Shadow Runs + Penny/Alex/Oscar (later)**
- Build shadow-scout, shadowify, promote workflows
- Build the three persona agents
- First shadow run with two variants of `code-review`

Each phase produces something usable; you don't have to wait for the whole architecture to be built.

---

## 13 — Key design principles

- **Harvest, don't author.** Don't build skills from scratch. Mine upstream, transpile, benchmark, promote.
- **Evidence over vibes.** Promotions are driven by shadow-run scoreboards, not opinions.
- **Lights off by default.** The factory runs without human attention. Watchtower observes; sign-off booths gate where needed.
- **Workflows for workflows.** The factory eats its own dog food. Ingestion is a workflow. Evaluation is a workflow. The factory creates the workflows that create the factory.
- **Provenance is non-negotiable.** No canonical artifact without `provenance.json` and verbatim `_source/` copies. Every promotion preserves the chain.
- **One winner per station, all alternatives kept.** Canonical is the production line; variants/ is the bench. Nothing is destroyed.
- **Code wrapper over model wrapper.** Use Workflow Tool primitives. Pass state through JS variables, not through Claude.
- **Stack-agnostic skills.** Stack specifics live in consuming projects, not in canonical artifacts.

These principles are stable. Implementation evolves. Architecture is the contract.
