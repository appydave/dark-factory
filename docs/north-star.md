# Dark Factory — North Star & Path Hierarchy

**Status**: 2026-06-01 — the orienting frame; read before anything else.

---

## The North Star (the one primary thing)

A capability factory you **direct by talking to it.** You say what you want; it runs the work **in sessions** (on the Max plan — never cron/API), observes itself, and improves. Lights-off floor, glass-walled watchtower, **you as director.**

## Self-learning is non-negotiable — part of EVERY conversation

The factory that "improves" only does so if learning is **persisted**. This is a first-class North Star requirement, not a nicety (David, 2026-06-06):

1. **Learn from every conversation** — corrections, decisions, dead-ends, proven mechanisms.
2. **Persist it durably** — into the right bucket so a cold restart loses nothing:
   - **auto-memory** (`~/.claude/projects/.../memory/` + `MEMORY.md`) — cross-session facts/decisions/feedback (the primary store, loaded every session).
   - **`build-state.md` / `backlog/`** — project state + open work.
   - **brains** (`~/dev/ad/brains/`) — reusable, cross-project knowledge (e.g. Claude Code platform rules).
3. **Check in on a cadence, not just at the end** — at every milestone (a decision ratified, a probe proven, a correction received) AND before session end / compaction, run the sweep: *what did we learn → is it durable → where does it persist?* The trigger is the weak link, not the storage; the discipline lives in the `marshall` skill's Self-learning step and should be reinforced by a SessionEnd/PreCompact hook.

**Litmus test:** if David shut this session down right now and started fresh, would the next session have everything it needs? If not, persist before moving on.

## Get it done — lean on the full toolbox, and parallelize

When something needs doing, **reach for a tool; don't grind it by hand in one chat.** The toolbox (be aware of all of it):
- **Claude Code built-ins** — Bash, Edit, the Agent/Task tool, **Monitor**, **/loop**, and **Workflows** (the newest — orchestrated parallel sub-agent fan-out; ⚠️ verify Max-vs-metered billing before relying on it).
- **MCP servers, skills, and Python scripts you build** for the job.
- **The Marshall→Swagger dispatch loop** for build/execution work.

**Before doing a task, propose the next 3-4 useful tasks** — so we can parallelize instead of going serial:
- **Local fan-out:** multiple Swaggers on this machine (bounded ~4 by the session wall).
- **Distributed:** delegate to the **M4 Mini** (Tailscale `100.82.235.39`) once it has the latest dark-factory + **Switchboard** + **Watchtower** — via SSH + tmux + interactive `claude` (never `-p`; Max plan). Tailscale, not `.local` (Roamy is a travel machine).
- **Read/research fan-out:** background agents (already in use) or the Workflow tool.

The point: **get results back faster by running independent work in parallel**, and always leave David a menu of the next few moves so he can choose what to fan out.

## Constant research — you can't lean on a tool you don't understand

The toolbox principle is empty without this. **Continuously research how the tools actually work and what new ones exist** — research is a first-class, ongoing activity, not a one-off. Before leaning on a tool for real work, understand its mechanics, limits, and **costs** (e.g. Max-vs-metered billing). The newest example: **Workflows** — we flagged we don't yet know its billing/mechanics, so we research it before relying on it. Sources: the **brains** (`~/dev/ad/brains/`), the Claude Code brain docs, **meetups/events** (e.g. the 2026-06-06 Anthropic CNX Chiang Mai write-ups now in the `ai-meetups` brain — deep dives on Workflows, lossless context/memory, and Claude-Code/Codex orchestration over MCP), and **dispatched research agents**. Capture findings to brains (reusable) + memory (project). Research feeds the toolbox; the toolbox gets the work done; self-learning persists what we learn — the three reinforce.

## Observability & telemetry — measure, don't trust hearsay

**Verify with instrumentation; don't take anyone's word** — not a text model's, not a meetup's. When a claim matters (e.g. "Claude Code leaks to ~60GB and crashes the box"), build the **observability to measure it ourselves** before acting on it. Telemetry/observability is a **standing investment area**, funded regularly — not bolted on after a fire. (Switchboard already polls `ps -Ao …pcpu,pmem…`, so the substrate exists — extend it to track Claude Code/Swagger RAM over time, and let Watchtower visualise it.)

## Grow the capability wheel evenly

Picture a skills radar — harness engineering, tools, research, observability, the dispatch loop, the bus, the control plane, the content pipeline. We want the circle **ever-expanding but smooth**: invest across all spokes regularly, keep balance. Don't spike one (e.g. harness engineering) while another (tools, observability) sits at zero — that's a jagged wheel that rolls badly. Even, continuous growth across capabilities.

## Two major paths (different work — both serve the North Star)

1. **Build the factory — the machinery.**
   Producer (talk → ticket) · Consumer (the loop) · Trigger (in-session firing, problem #15) · Watchtower · conversational layer.
   **← PRIORITY NOW.**

2. **Run the content — the 1,100-artifact pipeline.**
   Census → eval → distill → ratify. This is **cargo**, not the factory. It can run in its **own independent session** once the workflow exists.
   **Deferred.**

## Why Path 1 first

The factory is the **durable asset**; the content is just the **first cargo** it carries. Grinding the cargo by hand builds no factory. Building the factory makes the cargo — and everything after it — something you can **just ask for.**

## Current frontier (Path 1)

| Part | Status (2026-06-05) |
|------|--------|
| Consumer — claim → execute → record → done | ✅ **C1 proven** — first real end-to-end run, by hand (`experiments/watchtower-engine/proof/c1-first-real-run.md`). The earlier "✅ proven" referred only to the atomic-claim **mutex** (200×8); the *job path itself* had never run until C1. |
| Producer — talk → ticket | 🔨 **next (C2)** |
| Trigger — in-session autonomous firing (#15) | ❌ unsolved — target shape is **Marshall → Swagger**, see `runtime-model.md` |

> **Correction (2026-06-05):** the old "Consumer = a `/loop` + mutex across 4 staggered sessions" model is **dead**. Competing self-watchers don't distribute work — one fast session hogs the queue; the mutex gives *correctness*, never *fairness*. The runtime is now **one watcher (Marshall) routing to isolated job-agents (Swaggers)** — see `runtime-model.md`. The mutex is kept only as a safety net.

## The build spine (C1 → C5) — prove one mechanism per session

Linear, N=1, **do** not theorise. Each session ends in a tangible artifact.

1. **C1 — Consumer runs one job by hand.** ✅ **DONE 2026-06-05** — queue→running→done, real run record + artifact, no loop/mutex/monitor.
2. **C2 — Producer: talk → a schema-valid ticket in `queue/`.** ← next. *(The daily-use form of C2 — the morning briefing + BA conversation — is specced in [`daily-operating-model.md`](./daily-operating-model.md).)*
3. **C3 — Trigger (Marshall): one watcher wakes on a ticket and dispatches to a Swagger; Marshall stays lean.**
4. **C4 — Return leg (#19): every run surfaces a one-line "what ran" so nothing is silent.**
5. **C5 — One real `kind:workflow` job carried end-to-end, triggered by talking.**

Scale (N>1 dispatch, Agent Teams, tmux pane pools) is **deferred** until the N=1 spine is proven — the research is parked in `agent-orchestration-capabilities.md`.
