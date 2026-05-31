# Problem Register

**Status**: living register — 2026-06-01
The place to note anything that feels wrong: a defect, friction, a missing capability, "I can't see X."

**Rules** (from `docs/systemic-fixes.md`):
- Capture is cheap — log freely, let nothing fall through.
- A register is **not a graveyard**. Logging ≠ progress.
- Every fix asks: *what workflow/skill/agent fixes the class, not just this instance?* — then picks the **smallest** move that does it.
- "Good/bad" is a hypothesis to validate, not an order to obey.

Upgrade path: this is a markdown register for v1. When the factory processes problems programmatically, promote to `problems.jsonl`.

---

| # | Problem (felt) | Class-level fix to consider | Smallest move | Status |
|---|----------------|------------------------------|---------------|--------|
| 1 | Design thinking accumulates as scattered docs with no index | A doc-organisation discipline (light Lexi-spirit, not Lexi machinery) | `docs/INDEX.md` — one line per doc, mandatory | ✅ done 2026-06-01 |
| 2 | `architecture.md` and `spec.md` overlap; read as competing | **Keep separate** — they ARE two BMAD concepts (architecture = how it's built; spec = what we're building). Don't merge. | Trim spec's three-roles recap to point at architecture; maybe rename spec | open (Task #2) |
| 13 | Claude buries decisions in docs David doesn't open → they get lost | A "Decisions & Actions for David" surface (Watchtower long-term) | Interim: surface in-conversation + as visible tasks; never bury | in progress (Task #1) |
| 14 | David gets too much per turn; no breakdown into actionable items | Decompose every request into small visible items | Use the task list; short turns | in progress |
| 3 | No teaching/presentation surface (Mochaccino = design, Watchtower = ops) | A presentation/education system | TBD — note as gap, don't build yet | open |
| 4 | No index of available tools (platform + repo); tool knowledge rots | Tool registry + automated freshness | `docs/tool-registry.md` (seeded); schedule a refresh | in progress |
| 5 | Claude Code platform tools (Workflow, /loop, /simplify, ultracode…) not tracked or kept current | Reuse existing `refresh-claude-brain` skill + planned `framework-pulse`; schedule it | Don't build new — schedule the existing refresher | open |
| 6 | Problem register itself didn't exist | This register | This file | ✅ done 2026-06-01 |
| 7 | Cool workflow paths auto-lock-in; spikes never deliberately promoted | Extend `canonical/variants` promotion to **workflows/SOPs** | doc'd `sop-lifecycle.md` | open |
| 8 | No decision lineage — ideas & where they diverge are untracked | Lightweight lineage log tied to workflows (not heavy ADR) | open |
| 9 | Old workflows & state docs sit idle, unnoticed | Idle/stale detection via an **inward pulse** | open |
| 10 | No end-of-day review of "what did the workers do today" | Daily review digest (ties to `human-comms` audio summary) | open |
| 11 | No inward-pointing pulse watching the factory's own SOPs | Internal pulse — same shape as upstream/framework pulse, aimed inward | open |
| 12 | These governance concepts can't be visualised in the Watchtower | Watchtower views for drift / idle / lineage | open |
