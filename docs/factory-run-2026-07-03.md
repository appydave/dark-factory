# Factory Run — 2026-07-03 (the first real extension cut)

**What this is**: the wrap report of the factory's first full production day — David directed by voice (OMI) + one "go"; Fable orchestrated; Sonnet workers built; everything shipped same-day. Written so a cold session (post-Fable week) can pick up every thread.

**Status**: complete · all repos pushed · both pulses live.

---

## Shipped (5 of the 6-item cut)

| # | Deliverable | Where | Live? |
|---|---|---|---|
| 1 | **OMI Fetch v1** — pulse: fetch → dedupe → archive → index → events → view | `~/dev/ad/apps/omi-fetch` (`appydave/omi-fetch`) | launchd, every 600s |
| 2 | **App Registry v1** — structure from constellation.json + local liveness probe; `query.py running\|dark\|drift\|app <id>` | `~/dev/ad/apps/app-registry` (`appydave/app-registry`) | launchd, every 1800s |
| 3 | **Project Digest v1** — the §2 MORNING BRIEFING box (daily-operating-model), dark-factory first; the one write = last-briefing ts | `~/dev/ad/apps/project-digest` (`appydave/project-digest`) | read-on-demand |
| 4 | **comms-flow.md** — Switchboard/Watchtower flow pinned; David's OMI action item | `docs/comms-flow.md` | doc |
| 6 | **KDD Viewer v1** — Lisa's window: normalize-first browser over `docs/kdd/` (SupportSignal: 578 learnings/54 patterns/14 decisions) | `~/dev/ad/apps/kdd-viewer` (`appydave/kdd-viewer`) | read-on-demand |
| 5 | AngelEye-sentinel extension | **NOT BUILT** — deliberate: murkiest scope, end-of-budget; candidate unchanged in pipeline | — |

Every app carries `docs/extension-notes.md` — the per-build learning artifact + KBDE promotion mapping. Those five notes files are the survival kit.

## The pattern that emerged (promotion-ready, Lisa-style: 4 recurrences)

**The factory micro-app shape** — converged across builds without being pre-designed, then enforced:
```
<app>/
├── <pulse|probe|digest|scan>.py     one entry point, LLM-FREE v1, stdlib only
├── lib/                             small single-purpose modules
├── store/                           index.jsonl · state.json · events/ · <x>.log
│                                    (one-write rule; volatile files gitignored)
├── view/<x>.html                    static, regenerated per run, warm palette
├── launchd/ + install/uninstall.sh  only if always-on (pulse apps)
├── projects|instances/<id>.json     the generalization seam (config-per-target)
└── README + CONTEXT + docs/extension-notes.md
```
Laws that held: **artifact-is-truth** (verify what landed, not what a worker said) · **idempotent runs** (run twice = no change) · **honest absence** (unknown/unresolved rendered as such, never faked) · **local commits by workers, orchestrator reviews then pushes** · **imperfect-now, document-always**.

## Cross-build learnings (the ones with teeth)

1. **Doc statuses rot in days; only probes tell the truth.** Twice this week a "running/dark" claim in a doc was wrong within 48h. The registry now keeps three status opinions side-by-side (constellation verdict · apps.json · live probe) and surfaces drift instead of arbitrating. Corollary found by build #2: AngelEye has three *disagreeing* statuses across sources.
2. **The orchestrator/worker economics work.** Fable spent tokens only on direction, review, and synthesis; ~7 Sonnet workers (~1M subagent tokens) did the building. Every build was verified by evidence (pulse logs, scan counts, screenshots) before commit.
3. **Real data broke every clean assumption** — constellation paths were prose not paths (30-entry override table); a pre-existing `omi-sync` launchd job nobody remembered (failing, left loaded — David to retire); `promoted_to_pattern` has 3 raw shapes in the wild; living registers (concepts.md/problems.md) poison "in flight" counts. Normalize-first + honest-absence handled all of it.
4. **Events have producers but no consumer.** omi-fetch emits `store/events/*.json`; nothing listens yet. The comms-flow doc (§5) names this as the top missing piece — the daemon/consumer is the natural next brick (and the KBDE ④ Events story).
5. **NEEDS-YOU works when the source is written down.** The digest surfaced David's real open decisions on run 1 — but missed the poster taste-check because it was never a backlog item. Law: *if it needs David, it must exist as a file.*

## Open threads (for the next session/day)

- **constellation.json lags reality** — 3 new apps (omi-fetch, app-registry, kdd-viewer… + project-digest) born today; add them + flows, re-render design 10 (note: the view embeds the JSON inline — update both).
- **Events consumer/daemon** — the missing comms brick (comms-flow §5).
- **#5 AngelEye-sentinel extension** — unbuilt, candidate stands.
- **Cortex KDD scan** — needs MacBook Pro + the staging-vs-ratified schema fix (specced in kdd-viewer's extension-notes).
- **Retire `com.appydave.omi-sync`** — failing + superseded; David's call.
- **Digest project #2** — config seam ready; wire `needs_you.markers` config first (named in its extension-notes).
- **Poster taste-check** — now written down where NEEDS-YOU can see it: this line is that file.

## Provenance
Direction: `raw-intake/omi/2026-07-03-0909-micro-apps-apis-and-extension-planning.md` (+ 07-02 capture) · Cut agreed in-session 2026-07-03 · Builds delegated per `feedback_orchestrator_delegate_cheaper_models` · Candidates: `brains/dark-factory/app-pipeline/` (omi-fetch-extension, app-registry, kdd-viewer all marked shipped).
