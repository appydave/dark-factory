STOP — this is a HANDOVER SEED from a previous session, designed to seed a GREENFIELD design charter for Switchboard. Read it fully, then orient and ASK (cold-start protocol) — do not start building. This is a clean-close → fresh-window handover (DF-6 pattern), NOT compaction.

> Produced 2026-06-09 by mining session transcript `2df0e613-…jsonl` with the `abridge` subagent (NOT hand-written from faded memory — that's the thin-handover bug this method fixes). Pairs with `MEMORY.md` (auto-loads) + `backlog/specs/tickets.json`.

## Why a fresh window (read first)
David (tired, end of a long winding session): *"if I do it from here, we have polluted context; if I do it from anywhere else, I don't know what we are building."* This seed is the bridge. **A fresh window is also REQUIRED for a second reason:** the greenfield charter should be authored with Osmani's **`/agent-skills:spec`** (`spec-driven-development`), which was installed user-scope this session but only loads in a **new** `claude` window — the session that wrote this seed could not use it.

## How to resume
1. Close the old window. Open a fresh `claude` in `~/dev/ad/apps/dark-factory` → `/marshall`.
2. Run preflight; read `MEMORY.md` + this seed + `backlog/specs/tickets.json`.
3. **The job:** author a **greenfield Switchboard design charter** — *what Switchboard IS, from the end-state backward*, with the DF-7 state-plane spec as an INPUT (not the thing to build). **Timebox to a CHARTER (a design doc), NOT a rebuild** — the working bus is a real asset.
4. **Author it via `/agent-skills:spec`** (Osmani, greenfield-shaped) — this doubles as the fair "re-test Osmani as author on a greenfield capability" the DF-7 delta explicitly asked for, and optionally generates the second DF-8 comparison data point.
5. DF-7 is **paused at `spec-written`** (all 5 decisions ruled). Do NOT merge the canonical DF-7 or greenlight a build until the charter says the state-plane is still the right next slice.
6. Per cold-start protocol: surface, then **ask David** what he wants — don't auto-dispatch.

## ⚠️ THIS SEED IS NOT THE CHARTER INPUT — it's grounding + a map to the real sources
Mined from ONE session transcript. That transcript only legitimately holds: the **trigger**, the **recent decisions** (DF-7 D1–D5, CRUD-vs-kill), and a **current-state snapshot** of Switchboard (captured only because we read its repo files this session). It does **NOT** contain "what Switchboard should be" — that was never discussed here. **The greenfield charter's real source material is elsewhere — READ THESE before authoring:**
- `backlog/2026-06-06-dark-factory-sentinel.md` — the actual Sentinel design plan (build order; "four problems → one mechanism").
- `docs/watchtower/symphony-spec.md` (**80KB — the richest source**; Switchboard's job/claim/state model derives from it) + `symphony-relook-2026-06-07.md`.
- `docs/watchtower/{DECISIONS,schemas,spec,plan}.md`, `watchtower-from-symphony.md`, `reaper-brief.md`.
- The AppySentinel template: `~/dev/ad/apps/appysentinal/{CONTEXT.md,DEVELOPMENT.md,docs/}` (what the recipe-app substrate is FOR) + Switchboard's own `~/dev/ad/apps/switchboard/{README.md,CLAUDE.md}`.
- Memory `watchtower-sentinel-bus-direction` (the 2026-06-06 design thinking — richer on Switchboard's identity than this whole session).
- **DAVID is the primary source.** Most of "what Switchboard should be" is unwritten — in his head. The charter MUST be **interview-driven** (this is why `/agent-skills:spec` / `spec-driven-development` is the right, interview-first author — it asks the §5 open questions rather than guesses). Do NOT let the spec author fabricate answers from this seed.

### Un-mined session transcripts (BATCH-MINE these as charter prep — this seed was built from only ONE thin session)
A grep across the past week's transcripts found far richer Switchboard material than this session held. Mine via the `abridge` subagent with a "what-is-Switchboard / greenfield-design" lens, in priority order (hit-count = signal density). **Path prefix:** `~/.claude/projects/`
- **`-Users-davidcruwys-dev-ad-apps-switchboard/` cluster (HIGHEST value — design-while-building, NOT in memories):** `b9153637-…` (276) · `992e121b-…` (123) · `0d7ebe05-…` (115) · `5d7e5dfe-…` (93) · `0cc44f83-…` (76) · `6396f590-…` (73) · `74659a99-…` (65). All 06-06/06-07, the construction sessions for the 5 recipes.
- **`-Users-davidcruwys-dev-ad-apps-dark-factory/627e86a2-ecc2-4057-bfa7-619a1c1de676.jsonl`** (15MB, 633 hits) — the **design-origin** session. ⚠️ partly already distilled into the Switchboard memories (it's their `originSessionId`) — mine for the detail the memories compressed away, expect some redundancy.
- Moderate df sessions: `215b9cee-…` (53) · `940816e3-…` (25) · `5a5b5de5-…` (11).
- **Method:** batch the cluster in parallel (one `abridge` per transcript, greenfield lens), dedupe net-new findings against this seed + the memories, merge only the additive material. Watch token cost on the 15MB one.

---

## Switchboard Greenfield Design Charter — Session Seed

### Purpose
Seeds a fresh session to write a greenfield design charter for Switchboard, a Dark Factory constellation app. Mined from session `2df0e613-17f6-489e-9042-d26ddac8315f` (2026-06-09). The session wandered through an orphaned job → a state-plane spec (DF-7) → an Osmani plugin hunt → a delta comparison → and landed on David's directive to step back and think greenfield rather than keep patching.

---

## 1. THE GREENFIELD TRIGGER

**David's exact framing:**
> "we have not even taken time to plan anything around what switch board does? the task we are about to do is reactive based on a fragile system and trying to fix that. Now this may be ok right now and yes we could merge DF7 but I suspect we might want to sit back and think greenfield as well."

**The synthesis David endorsed:** DF-7 as shaped is reactive — "the flat-file engine is fragile → bolt a state plane onto Switchboard." Underneath: **we never designed what Switchboard IS.** Its history is 5 `feat:` commits (registry → SSE → queue → tickets → staleness), each a reaction to the next gap, **no charter**. Grafting a sixth recipe onto a thing that grew by accretion is building on un-surveyed sand.

**Three reasons the step-back is right (not paralysis):**
1. Converges with the Osmani verdict — the delta asked to "re-test Osmani as author on a greenfield capability." The charter IS that re-test. Two birds. ✅
2. A live instance of DF-8 — same task, two task_types: appydave won existing-app; greenfield is the other cell, generating corroboration data. ✅
3. Cost is a design doc, not a rebuild. Greenfield-DESIGN ≠ greenfield-CODE. ✅

**Status at close:** DF-7 paused at `spec-written`. No build greenlighted. Merged canonical DF-7 NOT produced — both pending the charter outcome.

---

## 2. WHAT SWITCHBOARD IS TODAY (starting material)

- Path `~/dev/ad/apps/switchboard/`; launchd `com.appydave.switchboard`; `:5099` HTTP + `:5100` MCP; core `@appydave/appysentinel-core`. ✅verified
- **Scaffolded by `create-appysentinel`** (the AppySentinel template) — **NOT Ralphy** (correction this session). ✅verified
- Built out over 5 `feat:` commits **by a dark-factory Swagger through the loop** (Marshall dispatched a Swagger running `configure-sentinel`), NOT Ralphy: `a3dd0d8` registry+SSE · `c81b219` /jobs queue · `489117c` durable claimable tickets · `08c9ba2` staleness-detector · `d1506ba` topic-selective log. ✅verified

**Recipe inventory** (`appysentinel.json`): input[`poll-command`] · storage[`snapshot-store`] · interface[`mcp-binding`,`api-binding`] · transport[`sse-deliver`] · runtime[`register-as-launchd`] · coordination[`staleness-detector`]. ✅verified
- `api-binding` (Hono): `POST /jobs` persists `queue/<id>.json` durable-first, emits `job.queued`, fans out SSE; `GET /health`. Enqueue surface exists; **no claim-coordination, no ownership** in the service yet.
- `staleness-detector`: timer (30s), scans `swagger-*` tmux windows, emits `session.stale`, **observer-only — detect+tell, never kills.** TODO(v2): query AngelEye `last_active`. **THE MODEL recipe to copy** (`src/coordination/staleness-detector.ts`).
- `snapshot-store`: one overwriting JSON via `atomicWrite` (ephemeral/last-only, not per-job durable).

---

## 2b. WHAT SWITCHBOARD IS *MEANT* TO DO — grounded in Symphony (evaluated 2026-06-09)
The authoritative grounding is **Symphony** (`docs/watchtower/symphony-spec.md`). Symphony is a daemon **scheduler/runner + tracker reader** (§1): poll a tracker → per-issue workspace → run a coding agent → manage lifecycle. The KEYSTONE: §4.1.8 **Orchestrator Runtime State** — *"a single authoritative in-memory state"* = `running`(map) · `claimed`(set) · `retry_attempts`(map) · `completed`(set) · token totals — which Symphony deliberately keeps **in-memory and does NOT persist** (§2.1: "exact in-memory scheduler state is not restored").

➡️ **Switchboard = Symphony's §4.1.8 Orchestrator Runtime State, lifted out of one orchestrator's memory into a DURABLE, SHARED service, + the event/observability bus its runs emit on.** The whole constellation IS Symphony decomposed: **Marshall** = Orchestrator (poll/dispatch/retry/reconcile §3.1.4) · **Switchboard** = the authoritative state (§4.1.8 = DF-7's state plane) + bus · **Swagger** = Agent Runner (§3.1.6/§10) · **AngelEye** = Live Session liveness (§4.1.6, stall §8.5 keys on `last_codex_timestamp`) · **Watchtower/DF-3** = Status Surface + observability (§3.1.7/§13).

⚠️ **THE CHARTER MUST OWN THIS:** Symphony lists *"general-purpose workflow engine or distributed job scheduler"* as an explicit **§2.2 Non-Goal** and keeps state in-memory by design. Dark Factory wants that state **persisted AND shared across N orchestrators on multiple machines** — the opposite. So DF-7/the state plane is a **deliberate extension of Symphony past its own non-goals**, NOT a reactive patch and NOT merely "implement Symphony." Decide this consciously.

✅ evaluated this session: Symphony §1–4 (problem, goals/non-goals, components/layers, full §4.1 domain model). ❓ NEXT DEEP READ for the charter: §7 (orchestration state machine), §8 (polling/scheduling/retry/reconciliation), §10 (agent-runner protocol + §10.4 emitted runtime events = what rides the bus), §13 (observability) — header-skimmed only so far.

## 3. BOUNDED RESPONSIBILITY (lines already drawn — starting constraints)

**Switchboard IS:** the communication layer / broker / durable write-side; owns the queue, routing, messages, and "awareness of communication" (liveness FOR routing). The always-on Sentinel bus other apps emit onto / subscribe to. ✅established
**Switchboard is NOT:** resource/process health (→ AppyRadar (was "AppyCtrl" — corrected 2026-06-10, see docs/appyradar.md)); session telemetry (→ AngelEye); the thing that kills processes / closes windows / mutates the external world (→ Marshall's Monitor — Marshall is the only killer). AppyRadar only observes process/window state and answers/emits; it never kills. ✅established

**The CRUD-vs-kill boundary (D4 — the session's most important correction):** Marshall wrongly framed Switchboard as "observer-only." David corrected: *a switchboard ROUTES — it's where state goes; if a thing dies it becomes unclaimed/pool again.* Rule: Switchboard **MAY** CRUD its own comms/queue/state domain (enqueue, claim, complete, fail, **requeue a dead-claimant's record claimed→pool**); it **NEVER** mutates the external observed system. "Requeue a state record" = broker CRUD = legal. ✅established

---

## 4. THE STATE-PLANE (DF-7) AS AN INPUT, NOT THE CHARTER

**Goal:** move job work-state off flat files (`experiments/watchtower-engine/{queue,running,done,reports}/`) onto a service-backed shared-state plane → Marshall instances become thin stateless clients on one bus. Unlocks **(1) parallel orchestration** (N thin clients on 1 plane; NOT repo-cloning — "a disaster in normal programming") and **(2) factory portability** (state not tied to `dark-factory/` cwd). ✅established

**5 ruled decisions (ALL RESOLVED 2026-06-09):** D1 file-per-job JSON via `atomicWrite` · D2 adopt AngelEye session-id as `claimed_by` · D3 MCP-first for Marshall / HTTP for scripts · D4 coordinator requeues state (broker CRUD, never kills) · D5 coordinator records `attempts`, client owns retry. ✅established — but these are INPUTS; the charter may confirm/reshape/expand them.

**2 recipes DF-7 specifies:** `job-state-store` (durable per-job record, `pool→claimed→running→done|failed`) + `job-coordinator` (atomic claim-by-id + `claimed_by`, complete/fail, AngelEye-keyed reaping, emits lifecycle Signals). **Current gap:** `/jobs` only enqueues; claiming still happens via `rename(2)` on the floor (`bin/claim-next.sh`). DF-7 fills that — the charter decides if it's the RIGHT next gap.

**Spec artifacts:** `df7-switchboard-state-plane-spec.md` (appydave baseline, 5 decisions ruled) · `…osmani.md` (Osmani pass) · `df7-osmani-vs-appydave-delta.md`.

---

## 5. OPEN DESIGN QUESTIONS THE CHARTER MUST ANSWER (the ❓s)

0. **⭐ THE CENTRAL FORK — where does the authoritative orchestrator state live?** TWO unreconciled answers exist: **(a)** the 2026-06-06 *Switchboard-replay hybrid* (memory `symphony-coordination-model` line 28, marked "RESOLVED"): state lives in **Marshall's session**, Switchboard is a durable **event log**, a restarted Marshall **replays** to rebuild — stateful Marshall, no always-on coordinator. **(b)** DF-7 (2026-06-09): authoritative state lives as **durable records IN Switchboard** + a coordinator — **stateless** thin-client Marshall. DF-7 likely *supersedes* (a) because N concurrent Marshalls + portability need shared authoritative state, not per-Marshall replay-rebuild — but this was NEVER reconciled. **The charter MUST pick one and retire the other.** (This is also the Symphony §2.2-non-goal extension: (b) makes Symphony's in-memory §4.1.8 state a distributed store, which Symphony chose not to do.) ❓⭐
1. **Full message-type surface** — only `job.queued`, `session.stale`, `process.snapshot` known. What SHOULD a designed bus emit/route? ❓
2. **Multi-machine / N-Marshall federation** — one Switchboard per machine (Tailscale bridging Roamy ↔ M4 Mini ↔ …) or a single authority? How do clients discover/reach it? ❓
3. **Event-log retention** — should Switchboard BE the DF-3 telemetry store, or emit and let DF-3 consume? prune vs permanent. ❓
4. **Relationship to DF-3 without duplication** — DF-3 = "observe the loop externally via Switchboard"; DF-7 = the state home. Same bus. Articulate exactly what Switchboard emits vs what DF-3 derives. ❓
5. **How much accreted bus fits the target vs needs reshaping** — recipes fine as-is? rename/restructure? different split? Requires designing first. ❓
6. **"Factory builds the apps" doctrine** — memory says constellation apps → Ralphy (AngelEye was). But the factory built Switchboard via Swagger. Live contradiction. The charter pass (Osmani as author) may itself reveal the right build method. ⚠️
7. **Scope of "awareness of communication"** — should Switchboard check a target is alive before routing, or be a dumb bus? ❓

---

## 6. TOOLING CONTEXT

- **Osmani `agent-skills` INSTALLED** (Roamy, user-scope, 2026-06-09): `agent-skills@addy-agent-skills`, `github:addyosmani/agent-skills`, v1.0.0. `/agent-skills:spec` → `spec-driven-development` (greenfield-shaped, interview-first, 6-area: Objective/Commands/Structure/Code-Style/Testing/Boundaries). **Only loads in a fresh window.**
- **Osmani-vs-appydave verdict:** appydave won the DF-7 *existing-app* task (framing, domain-fit, decision-richness, no-interview flow); Osmani won boundaries / gated-tasks / commands / test-pyramid. **Bias caveat:** DF-7 was home turf for appydave; Osmani is greenfield-shaped → **for the greenfield charter, let Osmani author it** (the fair re-test). Posture (not yet confirmed by David): appydave = author for existing-app work; Osmani = rigor/gate overlay.
- **Adversarial-delta technique** = David-endorsed method (memory `adversarial-delta-technique`). **DF-8** = comparison-registry spec born this session (`research/comparisons.jsonl` + `catalog:compare`; `backlog/specs/df8-comparison-registry-spec.md`). The charter delta (Osmani-on-greenfield) = the 2nd row that corroborates/contests the DF-7 result.
- **Memories to load:** `watchtower-sentinel-bus-direction`, `dark-factory-is-a-constellation-of-apps`, `cleanup-is-harness-driven-not-remembered` (CRUD-vs-kill), `constellation-first-placement`, `osmani-agent-skills`, `adversarial-delta-technique`, `requirements-first-store-for-future-ticketing`, `build-reusable-systems-not-one-offs`, `hitl-at-marshall-gates`.

---

## 7. LOOSE ENDS / STATE AT CLOSE

- **DF-7 ticket `build_via` corrected** this turn: was `ralphy` (wrong) → now flags the real history (create-appysentinel + dark-factory Swagger) + that the build method is itself an open charter question.
- **`q-20260609-cortex-proof.json` in `done/`** — NOT dispatched by this session; appears to be another orchestrator's Mochaccino proof run. Unrelated to Switchboard. Flag-not-chase, harmless.
- **No running jobs / no open windows** at close; the `swagger-df7-osmani` reaper auto-closed correctly (arm-on-dispatch fix held). Background hunts (`osmani-hunt`, `m4-agentskills-hunt`, `delta-tracking-eval`) all completed.
- **Tickets:** DF-7 `spec-written` (decisions ruled, build NOT greenlighted, merged-canonical NOT produced) · DF-8 `spec-written` (build-later).
- **Merged canonical DF-7** (appydave baseline + 3 Osmani grafts) — recommended but NOT produced; likely better done AFTER the charter (the charter may reshape whether DF-7 is still the right build spec).

## Key paths
`~/dev/ad/apps/switchboard/{appysentinel.json, src/coordination/staleness-detector.ts}` · `backlog/specs/{df7-switchboard-state-plane-spec.md, …osmani.md, df7-osmani-vs-appydave-delta.md, df8-comparison-registry-spec.md, tickets.json}`
