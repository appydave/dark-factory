---
id: ADR-0045
title: Stabilise before drain — declare an engine moratorium after T1-21
status: accepted
scope: internal
date_decided: 2026-07-11
deciders: [David Cruwys]
confidence: confirmed
recurrence_count: 1
provenance:
  sessions: [dark-factory-c2]
  files: ["backlog/2026-07-11-stabilise-before-drain.md", ".claude/skills/factory/SKILL.md"]
  commits: ["a1261a6", "153f42e"]
tags: [engine, moratorium, factory, self-hosting, hitl]
---

# ADR-0045: Stabilise before drain — declare an engine moratorium after T1-21

**Status:** Accepted

## Context

Nearly every ticket in a long 2026-07-11 session was the engine repairing **itself**
(T1-16 ledger, T1-19 worktrees, T1-20 no-spin, T1-21 verify-in-worktree) rather than producing
anything. The only product tickets (T3-03/T3-04, real tools) were **eaten by engine bugs and
hand-rescued**. So each run's "output" was another engine bug discovered — the ground shifted every
run, and the operator's recurring complaint ("it never gives me clear instructions, I don't know
what we're building") was structural, not user error: the run interface changed three times in one
day and `/factory` was built the same morning. The Chaperone (the cross-session outside eye) named
the shape: **the factory is self-hosting — using the machine to fix the machine** — and this has now
been the shape of multiple sessions.

## Decision

After T1-21 lands and one clean pool=1 **product** run confirms the fix, we **freeze the engine**:
no more `T1-xx` engine tickets for a defined stretch. We **freeze one run command** (`./run.sh
<ticket>`) and stop changing the interface. We **drain only product tickets at pool=1** until value
flows end-to-end without an engine bug eating it. If an engine bug surfaces mid-drain, we **ticket
it and keep draining** — we do not drop back into engine-repair mode. Parallelism was a *proof*, not
a need, and waits behind the moratorium.

## Alternatives Considered

- **Keep hardening / keep draining skills.** Rejected: the 1,100-skill drain was premature (research
  is 6 weeks stale, the skills aren't yet in use, and the factory is far bigger than skills — it's
  the micro-apps, comms, and hardening). More engine work keeps the ground shifting.
- **Fix HITL/ratification now** (the next bug found). Rejected as an in-moratorium exception — that
  is exactly the self-hosting trap. Ticket it; rebuild post-moratorium.

## Consequences

- The machine must become *boring* before it's useful; interface stability beats new capability.
- The next real build is a **Factory Map** — a legible view of the pipelines (T1 engine, T2
  producer, T3 ingestion, T5 watchtower, T6 constellation micro-apps, T7 self-learning, T8
  doc-truth, T9 voice, T10 fleet) and their gaps — so "I don't know what we're building" stops being
  true before more building happens.
- Product-first: the next 3–5 tickets are artifacts, not engine.
