# Watchtower docs — re-bucketing map

**Date**: 2026-06-06 · **Status**: map (ratified model; physical moves pending David's nod)

`docs/watchtower/` was written before the Sentinel/three-plane model existed, so it conflates three planes' worth of thinking under one "watchtower" name. This map re-homes each concern. The model (ratified 2026-06-06):

| Plane | What it is | Instance of | Name |
|---|---|---|---|
| **Factory Floor** | where work happens — Marshall (conductor) + Swaggers (job-agents); coordination = Symphony's state machine, ported | — (this repo) | `dark-factory` |
| **Communication Bus** | always-on durable broker: queue + event log + SSE pub/sub + `Last-Event-ID` replay + registry/reaper; **never runs `claude`** | AppySentinel | **Switchboard** |
| **Control Plane** | glass-wall viz + control: capped decision queue, records-never-mutates | AppyStack | **Watchtower** |

Cross-cutting: a **shared data contract** (the record/Signal envelope) all three planes speak.

## Per-doc disposition

| Doc | Today it's about | Plane | Disposition |
|---|---|---|---|
| `build-state.md` | the C-spine coordination engine (C1→C3d) | **Factory Floor** | **move** → `docs/factory-floor/`; living doc, keep |
| `watchtower-from-symphony.md` | adapting Symphony's coordination | **Factory Floor** | **move** → `docs/factory-floor/coordination-from-symphony.md` |
| `symphony-spec.md` | OpenAI Symphony (external reference) | **Factory Floor** (ref) | **move** → `docs/factory-floor/reference/` |
| `schemas.md` | record envelope + 4 record types | **Cross-cutting contract** | **move** → `docs/contracts/record-schemas.md`; reconcile envelope with AppySentinel Signal |
| `spec.md` | v0 4-screen viewer | **Control Plane** | **keep** in `watchtower/`; **update**: SSE-ban lifted (viewer consumes Switchboard SSE/socket); the §7 shell-out trigger is superseded by Switchboard's queue+events |
| `plan.md` | v0 viewer build plan | **Control Plane** | keep in `watchtower/` |
| `DECISIONS.md` | v0 locked decisions (mixed) | **split/annotate** | D1 trigger→**Switchboard**; D2 run-id→**Factory Floor** convention; D3 records-never-mutates→**Watchtower** doctrine; D4 buttons→**Control Plane**. All still valid; annotate per-plane |
| `context.md` | v0 drafting orientation | process/history | **archive** → `watchtower/_archive/` |
| `chatgpt-brief.md` | strategic origin brief | process/history | **archive** |
| `HANDOVER.md` | PO↔dev handover | process/history | **archive** |
| `REVIEW.md` | critique pass of the 3 drafts | process/history | **archive** |

## What the new architecture SUPERSEDES

- **`spec.md` "no WebSockets/SSE; poll every 5s"** (§5, §12, R7) — reversed. Switchboard pushes over SSE; the Watchtower viewer consumes it (AppyStack `file-crud` socket). Polling survives only at the outward Codex/tracker boundary.
- **`spec.md` §7 shell-out-to-workflow trigger** — superseded by the durable queue + claim + report-back (already proven in `experiments/watchtower-engine/`, and `DECISIONS.md` D1 already moved to file-trigger+watcher). The engine lives on the Factory Floor / Switchboard, not in the viewer's Express backend.
- **`context.md` "Watchtower lives at `apps/watchtower/`"** — superseded: three separate instances (factory floor here; Switchboard + Watchtower as their own AppySentinel/AppyStack instances), not one colocated web app.
- **OrchestratorState location** — RESOLVED: Switchboard-replay hybrid (live state in Marshall's session; rebuild from Switchboard's durable log on restart).

## What STAYS true (doctrine, plane-independent)

The cap (≤5 Today cards / ≤50 records), **records-never-mutates `canonical/`**, decision-queue-not-dashboard, census-batch-1 as first real job, the 9-layer learning taxonomy, the Marshall→Swagger model.

## Proposed target tree

```
docs/
  three-planes.md                      (NEW — the model + names; or fold into architecture.md)
  contracts/record-schemas.md          (← schemas.md)
  factory-floor/
    build-state.md                     (← build-state.md)
    coordination-from-symphony.md      (← watchtower-from-symphony.md)
    reference/symphony-spec.md         (← symphony-spec.md)
  switchboard/
    switchboard-spec.md                (NEW — queue, event log, SSE, replay, registry/reaper)
  watchtower/
    spec.md  plan.md  decisions.md     (control-plane viewer; spec.md updated)
    _archive/  (context.md, chatgpt-brief.md, HANDOVER.md, REVIEW.md)
```

Physical moves not yet executed — see chat for the go/no-go. (Moving touches `CLAUDE.md`'s `docs/watchtower/` references; do it as one deliberate pass.)
