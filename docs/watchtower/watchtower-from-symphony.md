# Watchtower from Symphony — Adaptation Map

**Purpose**: How to build Watchtower by lifting OpenAI's Symphony spec, layer by layer — what we take verbatim, what we re-host for our stack, and what we drop. The companion to [symphony-spec.md](./symphony-spec.md) (the full 2,169-line source).

**For Agents / Builders**:
- Read this before touching the Symphony spec — it tells you which sections are load-bearing for us and which are reference-impl noise
- Use the section map to jump straight to the relevant `symphony-spec.md` chapter
- This is a design map, not a build plan — decisions still open are flagged at the end

**Created**: 2026-06-02
**Last Updated**: 2026-06-02

---

## The premise — two halves of one app

| | Symphony | Watchtower |
|---|---|---|
| Has | A complete spec + Elixir reference impl | An identity + hard constraints, **no body yet** |
| Lacks | A human-attention discipline (it just piles issues into a handoff state) | An implementation |

So we don't *adopt* Symphony and we don't *rename* Watchtower. **Symphony's spec becomes Watchtower's skeleton; Watchtower's identity becomes Symphony's restraint.**

### Correction to earlier framing
The "headless Elixir GenServer polling every 30s" is the **reference implementation's** choice — it is **not** the spec. The SPEC is explicitly language- and host-agnostic (§3.2 "Abstraction Levels"). **We are building a new React app and implement the coordination layer as we see fit.** Nothing below requires Elixir, a daemon, or headless execution.

---

## The host model — Monitor-driven, not `/loop`-driven

Symphony's reference impl drives everything from a timer poll. We don't.

- **Coordination is event-driven via an in-conversation `Monitor`.** A `Monitor` armed `persistent: true` on the `queue/` directory (or on state-change signals) delivers `<task-notification>` events that wake the conversation **the instant** something changes — no timer cadence, no cache-burning short `/loop`. (See brain `anthropic-claude/claude-code/native-automation-loops.md` → "Monitor vs CronCreate".)
- **`/loop` is dropped** as the primary driver. (It remains available as a fallback heartbeat only if a Monitor ever needs a safety net.)
- **30s polling is retained at exactly one boundary**: talking *outward* to the Codex/Symphony agent system (§10 Agent Runner, §11 Tracker reads). Polling an external API on a clock is fine; polling our *own* queue on a clock is what Monitor replaces.

Net: Symphony's **coordination logic** (§7–§8, §16) survives intact; its **runtime host** (daemon + timer) is replaced by *React app + in-conversation Monitor*.

---

## Layer-by-layer verdict (Symphony §3.2 → Watchtower)

| Symphony layer | Verdict | Notes |
|---|---|---|
| **1. Policy** (`WORKFLOW.md`) | ✅ **Lift** | Policy-as-code in the repo is already how we think. Take the front-matter schema (§5.3) near-verbatim. |
| **2. Configuration** (typed getters, defaults, env) | ✅ **Lift** | Re-express in TS; same shape. |
| **3. Coordination** (poll, eligibility, concurrency, retry, reconcile) | 🔧 **Lift logic, re-host** | Keep the state machine (§7) + algorithms (§16). Replace timer poll with Monitor events. |
| **4. Execution** (workspace + agent subprocess) | 🔧 **Adapt** | Workspace model (§9) lifts cleanly. Agent runner (§10) points at Codex — keep as the *outward* integration, the one place 30s polling is fine. |
| **5. Integration** (Linear adapter) | 🔧 **Adapt / make pluggable** | `tracker.kind` is already an abstraction (§5.3.1). Source can be Linear, the `todo` brain, or dark-factory experiment records. |
| **6. Observability** (logs + status surface) | 🔁 **Replace with the React surface** | This is where Watchtower's identity lives — see below. Drop §13.4/§13.7 reference dashboards; build ours. |

---

## Section-by-section map of `symphony-spec.md`

| § | Topic | Verdict | Why |
|---|---|---|---|
| §1–2 | Problem / Goals | 📖 Read | Frames intent; note §1's handoff-state idea (the Watchtower seam). |
| §3 | System overview, **abstraction levels** | ✅ Lift | §3.2 is our layering. |
| §4 | Domain model (Issue, Workspace, RunAttempt, RetryEntry, OrchestratorState) | ✅ Lift | The data shapes — port to TS types. |
| §5 | `WORKFLOW.md` contract + front-matter schema | ✅ Lift | Policy-as-code. Keep `tracker`/`polling`/`workspace`/`hooks`/`agent` objects. |
| §6 | Config resolution + dynamic reload | ✅ Lift | Useful even in React (config hot-reload). |
| §7 | **Orchestration state machine** | ✅ Lift | Claim states, run lifecycle, idempotency — the hard, bug-prone core. Host-agnostic. |
| §8 | Poll / candidate selection / concurrency / backoff / reconciliation | 🔧 Lift logic | Keep selection+concurrency+reconcile rules; the "poll" trigger becomes a Monitor event. |
| §9 | Workspace management + safety invariants | ✅ Lift | Isolation + cleanup rules transfer directly. |
| §10 | **Agent Runner protocol (Codex)** | 🔧 Adapt | The outward boundary. 30s polling lives here. v1.1.0 Kata CLI path = model-agnostic option. |
| §11 | Tracker integration + **§11.5 tracker writes boundary** | 🔧 Adapt | Make pluggable. §11.5 matters: the *agent* writes back to the tracker, not the orchestrator. |
| §12 | Prompt construction + continuation semantics | ✅ Lift | First-turn-full / continuation-minimal is a clean pattern. |
| §13 | Logging + status + **§13.7 HTTP dashboard/REST** | 🔁 Replace | Drop reference dashboards; the React app *is* the status surface. Keep §13.3 snapshot/§13.5 token accounting as data we render. |
| §14 | Failure model + operator intervention points | ✅ Lift | §14.4 operator intervention points ≈ Watchtower decision cards. |
| §15 | Security / filesystem safety / secrets / hook safety | ✅ Lift | Non-negotiable; port the invariants. |
| §16 | **Reference algorithms (language-agnostic)** | ✅ Lift | Pseudocode for startup/tick/reconcile/dispatch/worker — implement in TS. |
| §17 | Test + validation matrix | ✅ Lift | Ready-made test plan. |

---

## What Watchtower adds that Symphony's spec lacks

Symphony is silent on the human surface — it just deposits issues in a handoff state. Watchtower's identity *is* that surface, governed by three non-negotiables:

1. **The cap.** At most 5 cards on the Today screen, oldest-first; no screen renders >50 records. A control surface that shows everything has failed at its one job. Symphony will happily accumulate 50 `Human Review` issues — Watchtower rations them.
2. **Records, never mutates `canonical/` (v0).** Clicking "Promote"/"Approve" writes a verdict record; a human performs the actual edit later. Watchtower has no write access to the source-of-truth library.
3. **Decision queue, not a dashboard.** The surface's job is triage — *"what needs me next?"* — not display.

---

## The seam — where the two halves join

Symphony §1 (and §11.5) already provide the join, by design:

```
  Symphony coordination (§7–§8)                Watchtower surface
  ──────────────────────────────              ───────────────────
  issue runs autonomously  ──▶ ends at a
  workflow-defined handoff   ──▶  handoff/failed state  ──▶  becomes a decision card
  state (e.g. "Human Review")     (§1, §14.4)                (capped, oldest-first)
                                                                  │ human decides
                                                                  ▼
                                                       verdict record written;
                                                       issue returns to the board
```

Symphony's terminal/handoff states **are** Watchtower's queue feed. No glue invented — the spec was built to hand off to humans; Watchtower is the human it hands off to.

---

## Open decisions (resolve before building)

1. **Work source for v1** — Linear (Symphony-native), the `todo` brain, or dark-factory experiment records? The tracker abstraction (§5.3.1) lets us defer, but v1 should pick one.
2. **Agent runtime** — Codex app-server (Symphony-native, §10) vs Claude Code agents. v1.1.0's Kata CLI path makes this swappable; decide what the React app actually launches.
3. **Where the coordination loop lives** — entirely in-conversation (Monitor-driven inside a Claude Code session), or a thin React/Node service that the conversation observes? This is the real architecture fork; the Monitor model assumes the former.
4. **Workspace population** (§9.3) — git clone per issue, or operate in place?

---

## Related

- [symphony-spec.md](./symphony-spec.md) — the full source spec (copied from `openai/symphony`, 2026-06-02)
- [context.md](./context.md), [plan.md](./plan.md), [schemas.md](./schemas.md) — existing Watchtower design docs
- Brain: `anthropic-claude/agent-sdk/symphony-orchestration.md` — Symphony summary + v1.1.0 model-agnostic update
- Brain: `anthropic-claude/claude-code/native-automation-loops.md` — Monitor vs /loop vs cron
- Brain: `dark-factory/watchtower-control-surface.md` — the identity this spec gives a body
