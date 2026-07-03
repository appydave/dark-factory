# Dark Factory — Daily Operating Model (how David directs the factory each day)

**Status**: 2026-06-23 — canonical operating model. Refines [`north-star.md`](./north-star.md) by speccing the **Producer (C2)** enrichment: the morning briefing + BA conversation that turns David's direction into the day's tickets/specs.

**Scope**: the **work** operating model — what the daily-use experience is and what it must satisfy. The *why* (chief-of-staff intent), the **life-OS vision**, and the **absorption principle (a portable law)** live in the brain vision doc and are referenced, not duplicated:
→ `~/dev/ad/brains/dark-factory/using-dark-factory-vision.md`

---

## 1. The daily loop

```
MORNING — David's ~4 hours of high-value human input
  0. BRIEFING — the factory proposes the candidate projects AND delivers
       each one's current state, loaded into context (§2). Happens BEFORE
       David talks — he reacts to a brief, he doesn't assemble it.
  1. BA CONVERSATION — one project at a time, around that state:
       "Where are we up to? What do you want to get out of it today?
        What's the next level of improvement?"
  • Output per project = a requirements / spec / BA document (tickets) for the day
  • Cover 3–4 projects (solo, David can only really do ~2/day well)

REST OF DAY — AI's 8–12 hours, minimal cognitive load from David
  • AI executes the day's specs across the projects (Marshall → Swagger)
  • David is free: exercise / dance / mental + physical health

OVERNIGHT — slower cadence
  • Work: ~2 hours research / admin / investigation / prep for tomorrow
  • Life: the life lane (deferred — §5, §8)
```

The AI must **truly understand where it waits for David** (the morning direction) and where it runs heavy-handed with **minimal involvement** after. The human is the **bottleneck by design at the front of the day, and deliberately absent after**. Overnight work research is **capped** (~2h) — more would just move the overload downstream ("I still have to check it off and I never get to").

## 2. Step 0 — the morning briefing (the gate)

The BA conversation can't open with "here's where we are on this project" without a trustworthy per-project state feed. This is the **gating prerequisite for P1**.

**Two layers of "observability" — the briefing needs the second:**

```
RUNTIME / SESSION layer            PROJECT / MISSION layer
"is a session alive right now?"     "where are we up to on this project?"
──────────────────────────────     ──────────────────────────────────────
AngelEye Observer (status dots)     git history per repo
Switchboard (process snapshot)      tickets / specs / backlog
watchtower-engine (live jobs)       mission.md + records/ (mission-topology)
appyradar (fleet/disk)              north-star / lane goal · delta since last brief
```

Reviving a session-liveness dashboard (AngelEye) does **not** feed the briefing — wrong layer. The briefing source is a **read-on-demand per-project digest** over durable artifacts (git + `mission.md`/`records/` + tickets), so it can't go stale because a service died.

**Briefing-source contract** (per project, a *compressed* digest — see the absorption law in the brain doc):
1. **Goal / DoD** — what this project is for
2. **Where we're up to** — recent commits, shipped, in flight
3. **Blocked / open** — tickets, specs, decisions waiting on David
4. **Delta since last briefing** — the change, not the whole history
5. *(optional)* **Live now** — the one runtime-layer read

**Output shape** (absorption-ranked: what needs David floats to the top; if he reads only `NEEDS YOU`, he's caught everything that requires him):

```
┌─ MORNING BRIEFING ──────────────────────────────────────────────┐
│ <project>            as of <ts>        ·   briefing #N           │
│ <autonomy stage>          health: <derived flag>                 │
├──────────────────────────────────────────────────────────────────┤
│ GOAL  <one line from mission.md / north-star>                    │
│ ⬤ NEEDS YOU (≤3)   <open decisions · waiting:david · needs-dec>  │
│ ▸ SINCE YOU LAST LOOKED   <git log since last-briefing ts>       │
│ ▸ IN FLIGHT   <tickets in-progress · specs not built>            │
│ ✓ SHIPPED RECENTLY   <collapsed to a count>                      │
│ ◦ LIVE NOW   <runtime read — renders "dark" gracefully>          │
├──────────────────────────────────────────────────────────────────┤
│ →  What do you want to get out of <project> today?               │
│    My take: <recommended focus>                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Field → source** (all durable, read-on-demand): header stage/health ← `mission.md` + derived flag · GOAL ← `mission.md`/north-star · NEEDS YOU ← open decisions in docs + tickets `waiting:david` + `needs-decision/*.json` · SINCE ← `git log --since=<last-briefing-ts>` · IN FLIGHT ← tickets `in-progress` · SHIPPED ← `git log` merged/done, collapsed · LIVE NOW ← AngelEye/Switchboard/`tmux ls` (optional).

**The one write.** "briefing #N / since you last looked" needs one piece of persisted state: a **last-briefing timestamp per project**. That's the only thing the digest writes — the deliberate seam where it stops being purely read-only.

**Smallest gate-opener for P1:** a read-only project-digest generator for **one** project (start with `dark-factory` itself — already mission-topology-instrumented) emitting the shape above from git + `mission.md` + tickets. Generalises by pointing at another repo; if it's not useful for one, it cost an hour, not a sprint.

## 3. The BA agent = the Producer (C2)

The morning interview is **not net-new** — it is north-star's planned **Producer (C2)** build step: *"talk → a schema-valid ticket."* Run once per project, that step *is* the morning BA conversation.

**It is a proper, distinct BA agent — NOT a `goal-plan` variant** (David corrected this, session 7683bd09):

> *"I don't agree that a goal plan skill interviews… It's not the same as what I'm talking about with a proper BA agent. Once you have a BA agent, if you wanted to set something as a goal, then the goal plan would kick in."*

- **`goal-plan` is a downstream *compressor*** — it packs a full context window into a ~4,000-char `/goal` condition. It kicks in *after* a BA conversation has produced something worth setting as a goal. **It is not the morning engine.**
- The BA agent's **internals stay an OPEN design question** (how the interview runs, how state is summarised). Only its **contract** is pinned:
  - in = current project state (§2) · process = deep one-project-at-a-time conversation · out = tickets / specs / requirements.

## 4. Roles & pipeline

None is truly net-new — the **BA agent maps to Producer (C2)**, and the last three already exist on the floor.

```
  Briefing source → BA agent (Producer/C2) → Marshall → Swagger → goal-plan*
   WHERE we are       WHAT today              dispatch   delegate   *if a spec
   (§2 digest)        (talk → ticket)         + reap     the work    becomes a goal
```

- **Briefing source** — per-project state (§2). The P1 gate.
- **BA agent / Producer (C2)** — turns state + David's direction into the day's tickets.
- **Marshall** — Watchtower conductor; wakes on queued work, dispatches, reaps (Dev thread — C3 auto-wake, DF-10; see `runtime-model.md`).
- **Swagger** — understands the daily ticket, delegates the pieces.
- **`goal-plan`** — downstream compressor, only when a spec is set as a goal. Not the interviewer.

## 5. Two lanes, one engine

The factory runs **two lanes through one engine** — work and life — differing in **cadence** and **privacy**, not machinery.

| | **Work lane** (this doc) | **Life lane** (deferred — §8) |
|---|---|---|
| **Daytime** | Heavy execution on the morning specs | (David lives his life) |
| **Overnight** | Capped (~2h) research / admin / prep | Slow-cadence chipping across life areas |
| **Cadence** | Fast, ticket-driven | Slow, check-in-driven |
| **Privacy** | Project state, mostly shareable — **commits/syncs to the work repos** | Touches personal/private data — **must NOT live in a work repo** |

**Privacy boundary (a build constraint):** the work lane must never absorb life data. The work-app repos commit and sync; the life lane touches `dtv`/PII and so its state lives in a **private store**, never here. (Rationale + the fuller privacy model: the brain vision doc, §7.)

## 6. Phasing

```
P1 — THE WORK LOOP  ← start here
     • §2 per-project digest alive + consumable (the gate)
     • BA agent / Producer (C2), one project at a time
     • day's specs → Marshall → Swagger execution · capped overnight research
     Done = a real day run start-to-finish.
P2 — THE LIFE SOFTWARE   (life lane, life-area registry — see brain doc §6; private store)
P3 — THE HARDWARE        (physical-health telemetry: Aura ring, doctor tests — deferred)
```

## 7. Build decisions

| # | Decision | State |
|---|----------|-------|
| BA agent shape | distinct BA agent = Producer (C2); internals OPEN; `goal-plan` downstream-only | **Resolved** (§3) |
| Briefing source | read-on-demand per-project digest (not a liveness dashboard); gate-opener = one-project generator | **BUILT 2026-07-03** — `~/dev/ad/apps/project-digest/` (build #3 of the cut); emits the §2 box for dark-factory from git+backlog+tickets+app-registry; the one write = `store/last-briefing/` |
| First project for the digest | — | **RESOLVED: dark-factory** (shipped); generalization seam = `projects/<id>.json` config |
| Acceptance test | every feature scored against the absorption principle (uptake over output) | see brain doc §8 |

## 8. Life-OS — the deferred third arc

The vision expands beyond work into a life-OS (relationships, health, brain function, DTV/visa, friendship circles), measured by David's wellbeing and actual uptake rather than output. **It is deliberately deferred (P2) and out of scope for this work doc**, named here only to mark the boundary:

- It is a **genuine third arc**, not a work project.
- Its real spec, when built, lives in a **private store** (it touches `dtv` + PII) — **never this work repo** (§5 privacy boundary).
- The full life-OS vision (the life-area registry, the friendship-circles candour, the absorption principle as acceptance criteria) is captured in the brain vision doc — start there when P2 begins.

## References

- **The why + life-OS vision + the absorption law (canonical):** `~/dev/ad/brains/dark-factory/using-dark-factory-vision.md`
- North star + the C1→C5 build spine: [`north-star.md`](./north-star.md)
- Marshall→Swagger runtime: [`runtime-model.md`](./runtime-model.md)
- C3/Marshall auto-wake (DF-10): `../backlog/specs/c3-marshall-auto-wake-spec.md`
- Observability surface ground-truth: `~/dev/ad/brains/dark-factory/observability-surface-audit.md`
- Per-lane state architecture: `~/dev/ad/brains/dark-factory/mission-topology.md`
