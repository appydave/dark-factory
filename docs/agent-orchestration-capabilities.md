# Agent Orchestration Capabilities — what Claude Code gives the factory

**Status**: education note / capability reference — 2026-06-01
**Why this exists**: The Dark Factory runs work through Claude Code. This doc tells the factory *what coordination primitives Claude Code actually has* (subagents, Agent Teams, the Workflow tool, tmux visibility) and *which to reach for*, so design decisions (especially the Watchtower runtime) are grounded in real capability, not guesses. Sourced from official Anthropic docs + community field reports + a Watchtower design session (2026-06-01).
**Related**: `watchtower/spec.md`, `watchtower/DECISIONS.md`, `workflow-tool-authoring-notes.md`, `sop-lifecycle.md`. Reusable Claude-Code-level detail lives in the brain: `~/dev/ad/brains/anthropic-claude/claude-code/{claude-code-swarm-teams,workflow-tool,native-automation-loops}.md`.

---

## 0. TL;DR — four layers, four jobs

| Layer | What it is | Use for | Coordination held by |
|-------|-----------|---------|----------------------|
| **Subagents** | helper agents spawned in-session; report back to caller only; never talk to each other | quick focused fan-out where only the *result* matters | the calling agent |
| **Agent Teams** | independent Claude Code sessions, shared task list, peer messaging | evolving multi-role work, discovered mid-run, needs Q&A / human gates | the lead **model**, turn-by-turn (emergent) |
| **Workflow tool** | deterministic `*.workflow.js` orchestrating agents with code-controlled flow | fixed pipelines, serial phases → handoff, audits, migrations | the **script** (deterministic) |
| **External queue** (Watchtower) | durable `queue/→running/→done/` job store wrapping any of the above | between-job gates, fix-loops, persistence, restart safety | the **filesystem** + a dispatcher |

**The factory's core insight**: these are *complementary halves*, not competitors. **Workflows handle within-job serial phases; the queue handles between-job gates, fix-loops, and persistence.** Teams handle the negotiated, human-gated middle. Pick by *who should hold the plan*.

---

## 1. Subagents vs Agent Teams (the first fork)

|  | Subagents | Agent Teams |
|--|-----------|-------------|
| Context | own window; result returns to caller | own window; fully independent |
| Communication | report back to caller only | teammates message each other directly (`SendMessage`) |
| Coordination | caller manages all | shared task list + self-coordination |
| Token cost | lower (summarised back) | higher (each teammate = a full Claude instance) |
| Best for | focused tasks, result-only | discussion, challenge, cross-layer ownership |

**Rule**: use subagents when workers don't need to talk; use teams when they do. For the factory, most *production* work is result-only → subagents or workflows. Teams are for *design/review/debate* phases.

---

## 2. Agent Teams — the mechanics

Enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` (v2.1.32+). **Experimental.**

**Architecture**: a fixed **lead** (the session that creates the team) + **teammates** (independent sessions) + a **shared task list** (`~/.claude/tasks/{team}/`, file-locked claims) + a **mailbox** (auto-delivered messages, no polling).

- **Dispatch is dual-mode**: the lead can **assign** tasks explicitly, *or* teammates **self-claim** the next unblocked task. File locking prevents claim races on both paths.
- **`TeammateIdle` hook**: fires when a teammate is about to go idle → the lead learns who's free (the key to round-robin assignment). Exit code 2 keeps it working.
- **Quality-gate hooks**: `TaskCompleted` / `TaskCreated` can block (exit 2) to enforce rules.
- **Plan approval**: teammates can be forced into read-only plan mode until the lead approves — a built-in gate.

**Sizing (official guidance)**: start **3–5** teammates; *"three focused teammates often outperform five scattered ones."* ~5–6 tasks per teammate. Scale only when work genuinely parallelises.

**Limitations to design around**:
- **One team per session**; **no nested teams** (teammates can't spawn teammates); **lead is fixed** for the team's life.
- **No `/resume` for in-process teammates** — after resume, the lead may message teammates that no longer exist (respawn them). tmux-mode sessions survive a lead crash (re-attach with `tmux -CC attach`).
- **Task status can lag** — teammates sometimes don't mark tasks complete, blocking dependents. **Verify the artifact, don't trust the status.**
- Plain-text teammate output is **invisible** to the lead/user — agents *must* use `SendMessage`.
- Permissions are set at spawn (inherit the lead's mode).

---

## 3. tmux Teammate Mode — seeing the work

`teammateMode` (in `~/.claude/settings.json` or `--teammate-mode`) controls visibility:

| Mode | What you see |
|------|--------------|
| **`tmux`** | **each teammate gets its own iTerm2 pane/tab**, auto-labelled with the agent name (1:1). Watch all of them live. This is the mode David uses. |
| `in-process` | teammates run inside the main terminal; cycle with **Shift+Down**, Enter to view, Esc to interrupt. Works in any terminal. |
| `auto` (default) | split panes if already inside tmux, else in-process. |

**Setup**: `tmux -CC` in iTerm2 (control mode → real iTerm2 tabs per pane), then `claude --teammate-mode tmux`. Requires tmux **or** iTerm2 + the `it2` CLI. **Not supported** in VS Code terminal, Windows Terminal, or Ghostty.

**Visibility caveat (the #19 lesson)**: the agent view *shows* activity but provides **no interruption mechanism** — a destructive action can run unimpeded in `auto`/`bypass` mode. So: (a) run factory workers in **`defaultMode`, never auto/bypass**; (b) build a deliberate monitoring surface. The proven pattern (from `claude_code_agent_farm`) is a **controller dashboard** showing per-agent status, context %, and **heartbeat age** — this is exactly what the Watchtower's return-leg should surface.

---

## 4. Dispatch patterns — distributing queued work

This is the heart of the Watchtower runtime. Two shapes; one is a trap.

### ❌ The trap — competing-consumers + event wake = thundering herd
N listeners each watch `queue/` (e.g. each arms a `Monitor`) and race to claim. An atomic `rename(2)` / file-lock claim guarantees **correctness** (one winner) but **not** fairness, distribution, or within-thread serialization:
- same listener can win every time (no round-robin);
- a fast winner loop-drains a burst before others finish one claim → no parallelism;
- a persistent `Monitor` can re-fire while a worker is still recording the previous job.

> Staggered *timers* (offset 1-min `/loop`s) give round-robin + serialization **by accident** — emergent timing side effects that vanish the instant a worker switches to an event `Monitor`. Don't depend on them.

### ✅ The fix — one lead dispatcher, push to idle
Put the **single** `Monitor` on **one lead**; workers never watch the queue. The lead claims a specific ticket and hands it to the **next idle worker** (tracked via `TeammateIdle`).

| Property | How it's restored |
|----------|-------------------|
| No herd | one watcher, not N |
| True round-robin | lead assigns to next idle worker in rotation |
| Finish-before-next | lead only messages an **idle** worker; a busy one can't get a 2nd job |
| Burst (2 events in 5s) | lead reads the **whole** queue per wake, fans across idle workers in one pass; rest wait for next `TeammateIdle` (backpressure) |

The file-lock claim becomes **belt-and-suspenders**, not the primary distribution mechanism.

> **Correction (2026-06-02, grounded against `~/dev/ad/brains/anthropic-claude/claude-code/native-automation-loops.md`):** This "lead dispatcher" framing implicitly borrows **Agent Teams** machinery (`TeammateIdle`, peer messaging) — which is for *coordinated* work. The Dark Factory's jobs are **independent** (different clients/projects). The authoritative doc is explicit: the native primitive for *independent* fan-out is **`/batch`**, whose workers *"are independent and don't talk to each other"* (`native-automation-loops.md:134`); Agent Teams is the *coordinated/messaging* family (`native-automation-loops.md:163`). So for our independent jobs, use the **independent family** (`/batch` / subagents / isolated sessions) — the lead+`Monitor` dispatch *shape* is fine, but don't import team-coordination semantics. See `runtime-model.md`.

### Operational facts that bound the design
- **~5–7 simultaneous sessions is a concurrency wall** on consumer plans (a dispatch cap, not quota). A lead + 4 workers = 5 sessions — at the edge. Don't plan to scale workers much past this.
- **The reaper is load-bearing**: stale `running/` entries (dead listener) must requeue. Field pools use adaptive timeouts (≈ 3× median cycle); the spike uses a fixed 10-min sweep. **The lead must verify the file landed in `done/`** — status/"done" messages lag and lie.
- **Adaptive staggering** (halve-on-success / double-on-failure, capped) + per-agent random seeds beat fixed offsets for distribution.
- **Async coordination is the hard frontier** — Anthropic's own research system is synchronous *on purpose* (they defer async over "result coordination, state consistency, error propagation"). A queue-pull pool is the async version, so reaper + dedup-log + verify-file discipline is *safety*, not polish.

---

## 5. The Workflow tool — serial phases → handoff

`*.workflow.js` in `.claude/workflows/` runs **deterministically, top-to-bottom, as plain JS** in the main session (research preview, v2.1.154+, paid plans). It owns control flow but **cannot touch fs/shell** — only `agent()` can. Eight injected globals: `agent, pipeline, parallel, phase, log, workflow, args, budget`.

| Construct | Does | Barrier? |
|-----------|------|----------|
| `agent(prompt,{schema?})` | spawns one fresh-context child; `{schema}` → validated object (retries), else text; `null` if skipped | — |
| `phase(label)` | **cosmetic** progress label only — does NOT sequence | no |
| `pipeline(items,...stages)` | per-item multi-stage chain, items flow **independently** | **no** |
| `parallel(thunks)` | `()=>agent(...)` thunks; awaits **all** | **yes** |

**Serial-phases-then-handoff mapping** (the thing the factory wants):
- **Fixed role chain** (analyst→builder→verifier) = single-item `pipeline()` or chained `await agent()`.
- **One role's serial sub-steps** (share context) = **one** `agent()`.
- **Deliberate context reset between sub-steps** = **split** into separate `agent()` calls.
- **The handoff** = plain JS variable passing: `const spec = await agent(A,{schema}); const impl = await agent(buildFrom(spec),{schema});`. Agents never talk; state flows through return values + files they write.
- **Fan-out (later)** = multi-item `pipeline()` (no barrier). **Fan-out + converge** = `parallel()` then plain-JS consensus. *When in doubt, `pipeline()`.*

**The two limits dissolve against the queue** (why Watchtower + workflows are complementary):
- **No mid-run human gate** → make each gated stage its **own `kind:workflow` job**; the gate is a job boundary (`done/` → human → enqueue next).
- **Forward-only (no fix-loop back-edges)** → a verify-REJECT lands in `failed/`/`needs_repair` and **enqueues a repair job**; the queue is the re-entry.
- **No cross-session memory** → each phase writes its artifact to disk (the *baton*); the workflow's final `return` emits a run summary the harness records. **Design for restart-fresh** — the run record is the only durable thing.

**Key gotchas**: `Date.now()`/`Math.random()`/argless `new Date()` **throw** (pass `args.ts`); plain JS not TS; `parallel()` needs thunks not promises; always `.filter(Boolean)`; un-allowlisted shell/web/MCP **still prompts mid-run** (pre-allowlist for unattended runs); concurrency cap `min(16, cores-2)`, lifetime cap **1000 agents/run**; **cost blows up** (a 5-hr Max allocation burned in 18 min by 62 Opus subagents) — route cheap stages to a smaller `model`. Full craft notes: `workflow-tool-authoring-notes.md`.

---

## 6. How it all maps to the Watchtower

The Watchtower (`experiments/watchtower-engine/`) is the **external queue layer**. It already has the right bones: `queue/→running/→done/|failed/`, atomic `rename(2)` claim, `runs/` records, kind-dispatch (`workflow|skill|instruction`), reaper, Monitor.

**Decisions this capability map points to** (not yet locked in `DECISIONS.md`):
1. **Runtime now = sequential, 1 leader + 1 child.** That's the natural shape of a single-item pipeline / chained `await agent()`. Not a limitation — the right default.
2. **When concurrency is wanted → lead-dispatcher, push-to-idle**, *not* N competing-consumers on one queue. Reuse the atomic claim as a safety net. **But (grounded):** for *independent* jobs (our case) this is the `/batch`/independent family, **not** Agent Teams coordination (`native-automation-loops.md:134`) — `TeammateIdle`/peer-messaging are coordination features we don't need.
3. **`kind:workflow` jobs = `.workflow.js` pipelines** for fixed role chains; serial sub-steps inside one `agent()` unless a reset is wanted.
4. **Gates & fix-loops = job boundaries**, not in-workflow constructs. The queue is the gate seam and the re-entry.
5. **Visibility (#19) = a heartbeat-age dashboard** fed by the lead; workers run in `defaultMode`.
6. **The reaper must verify `done/`**, never trust a worker's word.

**Topologies, in build order**: (1) single sequential pipeline [now] → (2) multi-item `pipeline()` fan-out → (3) lead-dispatcher worker pool with `TeammateIdle` round-robin → (4) Agent Team for negotiated/human-gated design phases. Each is a strict superset of capability over the last; the queue underlies all four.

---

## Sources
- [Anthropic — Orchestrate teams of Claude Code sessions (official docs)](https://code.claude.com/docs/en/agent-teams)
- [Anthropic Engineering — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Anthropic — Introducing dynamic workflows in Claude Code](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code) · [Workflows docs](https://code.claude.com/docs/en/workflows)
- [GitHub — Multi-agent workflows often fail; how to engineer ones that don't](https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont/)
- [Claude Code at 10 Parallel Agents: Week 1 Failure Modes](https://findskill.ai/blog/claude-code-10-parallel-agents-week-1/)
- [claude_code_agent_farm — lock-based coordination for 20+ parallel agents](https://github.com/Dicklesworthstone/claude_code_agent_farm)
- Brain: `~/dev/ad/brains/anthropic-claude/claude-code/{claude-code-swarm-teams,workflow-tool,native-automation-loops}.md`
