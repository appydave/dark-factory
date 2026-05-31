# Dark Factory — Workflows as SOPs: State, Lifecycle & Drift

**Status**: new — 2026-06-01
**Companion docs**: `architecture.md` §3 (canonical + variants), §5 (pulses), §9 (telemetry); `human-comms.md` (daily summary); `systemic-fixes.md`; `watchtower/`

---

## A workflow is an SOP

A workflow is a **Standard Operating Procedure encoded as data** — a defined piece of machinery. Not flexible; that's the point. It does the same job the same way, every time. The factory *is* largely its SOPs.

## State lives at levels

The data files that track state aren't one thing:

- **Per-run** — `store.jsonl` for a single workflow run. The normal case. ✓ exists.
- **Cross-workflow** — state shared across runs/workflows (blackboard, shared records). Partly exists.
- **Cross-time / aggregate** — "what is the factory's overall state of play." Mostly missing.

## The drift problem (the real gap)

Two workers show up to the factory. Worker A builds something cool, uses it a while. Worker B arrives — doesn't know A's work, or just has a different opinion — and goes a different direction. **Nothing wrong with B's work. But it's different, and it dropped steps and ideas A had captured.**

Today the factory has **no way to notice this.** Specifically, no:

- **Decision lineage / ADR** — a record of *what was decided, why, and where ideas diverged.* (Scattered "Why rejected" notes in `CONTEXT.md` and `watchtower/DECISIONS.md` are not a system.)
- **Idle / stale detection** — the old workflow, or its state docs, may now be sitting unused. Nobody flags it.
- **Daily review** — nothing arrives at end of day saying *"here's what these smart-but-non-communicative workers did today; this needs review."*
- **Spike-vs-main-flow discipline for workflows** — a cool path is not automatically the way. It could be *"great spike — pull these ideas back to the main flow,"* or *"move the main flow,"* or *"keep it as a variant."* That decision isn't tracked.

## Fix the class — extend what exists, don't invent

Most of this is **one existing pattern pointed at a new target**, not new machinery:

| Felt gap | Pattern that already solves it | What's actually missing |
|----------|-------------------------------|--------------------------|
| Cool path auto-locks in | `canonical/` + `variants/` promotion (skills) — "one winner, all alternatives kept, nothing destroyed" | The same model applied to **workflows/SOPs**, not just skills |
| Nobody watches for drift/idle | Upstream/Framework **Pulse** (`architecture.md §5`) — scheduled scans | An **inward-pointing pulse** that scans the factory's *own* SOPs + state |
| No end-of-day digest | **human-comms** daily summary + Watchtower projections (`§9` already tracks "last run") | The review *content* + the trigger |
| No decision record | `watchtower/DECISIONS.md` (ad hoc) | A **lightweight decision-lineage** log tied to workflows |

So the class-level move is: **(1) an internal pulse** that produces **(2) a daily review** and feeds **(3) a Watchtower view**, reusing **(4) canonical/variants semantics for workflows** and writing **(5) decision records** for divergence. Five facets, one loop — not five mechanisms.

## Caution: lineage, not ceremony

A decision log is worth building **only if it's consulted.** A heavy ADR process becomes the same graveyard the problem register warns about. Prefer *lightweight lineage* (one line: decided X, diverged from Y, because Z) over formal ADR ritual. The value is "Worker B can see what Worker A decided," not the paperwork.

## The missing automation (named, not built)

- No workflow/agent/event/cron looking at drift, idle, or divergence.
- No way to *create* these "automation overview" concepts.
- No way to *visualise* them in the Watchtower.

Logged in `backlog/problems.md`. Build order is a David decision — don't auto-build.
