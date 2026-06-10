# Backlog lanes — stability · self-learning · quality (2026-06-08)

Captured from the North Star "what else should we build" review. Weighted to platform **stability**, **self-learning**, **quality**. (Lanes C/E got a recent sprint; A/B/D are jagged — this rebalances.)

## The lanes
- **A · Dispatch loop (engine)** — Marshall→Swagger→queue/done/failed. Proven serial+local; reliability gaps.
- **B · Constellation (observability)** — Switchboard ● · AngelEye (manual, needs the Sentinel/control-plane split) · board v5 · AppyRadar (was "AppyCtrl" — corrected 2026-06-10, see docs/appyradar.md) ✗.
- **C · Comprehend→Visualise** — built (Millwright + skill + workflow.js + Mochaccino); cortex live.
- **D · Self-learning & memory** — auto-memory ●; the *trigger* is weak; telemetry + reassessment unbuilt.
- **E · Workflows & vendored specs** — reference-contracts ●.
- **F · Symphony / coordination** — claim-states + reconcile (mostly spec).
- **G · Chronicle / build documentary** — capture stage.

## Prioritised work

### #1 — INSTRUMENT-then-harden the dispatch loop  [STABILITY+OBSERVABILITY · ON DECK]
**Reframed (David, 2026-06-08):** measure before fixing. Verified: today's 3 Swaggers wrote NO run record AND NO handback — only `done/` is reliable. **Telemetry must OBSERVE the loop externally** (dispatcher/reaper/AppyRadar emit lifecycle events → Switchboard log → Watchtower viz/queries), NOT trust the worker to self-report (the worker is the unreliable part). Then harden with evidence. See `factory-operations-telemetry`. Original notes below:

Swaggers still **botch bookkeeping** (live again on the cortex job: moved to `done/` but `reports/` handback came back empty). PARAMOUNT per `dispatch-loop-robustness`.
- A **Swagger self-check** it must pass before reporting done (handback written, no `running/` stray, one `done/` entry).
- A **consolidated reconcile** loop that unifies reaper + retry + `running∩done` + stuck-case (Symphony §8.5) — one sweep, not four monitors.
- Monitor hygiene: arm-on-dispatch / stop-on-done, tracked IDs (monitors survive compaction — `monitors-survive-compaction`).
→ Dispatch this as the next job once the cortex **render** completes.

### #2 — Make self-learning ACTIVE machinery  [SELF-LEARNING]
The trigger is the weak link, not storage — proven this session (memories that didn't fire: my-take rule 3-4×, AngelEye-manual rule). Apply the Millwright lesson to learning itself: a **learning-sweep guardrail** (skill/hook) that fires at milestones + compaction, not when Marshall happens to remember.

### #3 — Tool-usage telemetry → lives IN AngelEye  [SELF-LEARNING + QUALITY]
**Reconciled (David, 2026-06-08):** NOT a standalone tool. AngelEye's **Sentinel** already ingests tool-calls + skill-calls via hooks → tool-usage telemetry is a **Sentinel capability**, not a new build. Measure which skills/workflows actually get used → optimise heavy, deprecate dead (skill-flood mgmt; feeds reassessment). Folds into the AngelEye spec below.

## AngelEye lane (B) — the two-product split + new spec  [STABILITY · David, 2026-06-08]
AngelEye is really **two products**:
1. **Visualisation Control Plane** — the dashboard/UI. Stays "AngelEye" (the eye you look through).
2. **The Sentinel** — always-on, always-present, **absorbs the hooks** (session reading + hook ingestion). Currently works; the code could take a big refactor. This is what gets **daemonized**, and the natural home for **tool-usage telemetry** (it already understands tool/skill calls).

**The spec job (research + design, read-only, local):**
- Understand **AppySentinel** (`~/dev/ad/apps/appysentinal` + the template/pattern — `appystack-vs-sentinel`).
- **Identify all of AngelEye's code and where it is** — map it into the two products (control-plane vs hook-absorbing sentinel).
- Draft the **split spec**: what moves to the Sentinel, what stays in the Control Plane, the always-on/daemonized Sentinel, + the tool-usage-telemetry capability. (Built later via Ralphy — app owns its features.)

**Naming the Sentinel (David wants options; angelic welcome):** candidates — `AngelEyeSentinel` / `AngelSentinel` (his) · **Ophan / Ophanim** (the many-eyed angel — all-seeing observer) · `Watcher` (Grigori — angels who watch) · `Vigil` · `Seraph`. (See chat for my take.)

## Naming decided
- The AngelEye Sentinel half = **AngelSentinel** (David, 2026-06-08). Control Plane stays "AngelEye".

## Discussion topics for when the work comes back (David, 2026-06-08)
1. **How can we improve the way we do visualisations** — and any problems *purely for cortex* (David anticipates problems with the "how does a brain work?" render).
2. **Structure for hundreds of presentations in Mochaccino** — the scaling/organisation problem FliDeck had to solve (gallery, tabs/groups, index, nav at scale). How does the Mochaccino side deal with many presentations, not just a handful?

## Parallel-dispatch learning (live, 2026-06-08)
- Two Swaggers run concurrently ✅ — but correct window↔ticket binding required **staggered** dispatch (claim ticket 1, wait for claim, release ticket 2). Confirms **claim-by-id** is the real fix (= stability #1): with multiple tickets in queue, "claim oldest" can't bind a window to a specific job, and the reaper would then close the wrong window.

## Done this round
- cortex shape: David chose **A+B+C** ("how does a brain work?") — rendering in swagger-cortex-render.
