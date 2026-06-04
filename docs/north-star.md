# Dark Factory — North Star & Path Hierarchy

**Status**: 2026-06-01 — the orienting frame; read before anything else.

---

## The North Star (the one primary thing)

A capability factory you **direct by talking to it.** You say what you want; it runs the work **in sessions** (on the Max plan — never cron/API), observes itself, and improves. Lights-off floor, glass-walled watchtower, **you as director.**

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
2. **C2 — Producer: talk → a schema-valid ticket in `queue/`.** ← next.
3. **C3 — Trigger (Marshall): one watcher wakes on a ticket and dispatches to a Swagger; Marshall stays lean.**
4. **C4 — Return leg (#19): every run surfaces a one-line "what ran" so nothing is silent.**
5. **C5 — One real `kind:workflow` job carried end-to-end, triggered by talking.**

Scale (N>1 dispatch, Agent Teams, tmux pane pools) is **deferred** until the N=1 spine is proven — the research is parked in `agent-orchestration-capabilities.md`.
