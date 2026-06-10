STOP — this is a handover from a previous session. Read everything before doing
anything. When done, summarise what you understand and ask what we should work on
today. Do not start implementing anything until directed.

> Produced with the `capture-context` skill (not hand-written) — 2026-06-08, session 2.
> Pairs with `2026-06-08-session-handover.md` (the prior session's full *work-state* handover). This doc is the *process-correction* layer on top of it.

## Session Context: Marshall startup + handover-mechanism correction — 2026-06-08 (session 2)

## Working On
Fixing Marshall's cold-start behaviour and the broken session-handover *mechanism*. Not feature work — a process-correction session triggered by Marshall mis-starting (it built + dispatched on a bare `/marshall` instead of orienting and asking).

## Current State
- ✅ **Marshall cold-start FIXED** in `.claude/skills/marshall/SKILL.md` (new "Cold start" section + scoped the momentum rules to mid-session).
- ✅ **Prior session's handover REBUILT complete** (`backlog/2026-06-08-session-handover.md`, 11 sections) by mining transcript `627e86a2…jsonl` with the `abridge` subagent.
- ✅ **The inline DF-3 telemetry build was FULLY REVERTED** — engine scripts back at HEAD, new files deleted, the false "DF-3 shipped" memory removed. **DF-3 is spec-only, not built.**
- ✅ **Learnings persisted to memory** (`cold-start-orient-and-ask` new; `session-handover-not-compaction` updated with the root-cause).
- ⏳ **Open:** DF-6 (a proper handover skill) not built; a location-convention tension surfaced (below).

## Key Decisions Made
- **A bare `/marshall` = orient + surface + ASK, never dispatch/build.** Why: a handover records David's *parked decisions*; executing them unasked strips him of the choice. Momentum/"pick-one-and-start" is a *mid-session* rule only.
- **Reverted the DF-3 inline build.** Why: built without David's go, skipped the Swagger protocol, and pre-empted the Switchboard-event-log-as-telemetry fork David was deliberately standing at.
- **Handovers must be produced by a TOOL/skill — ideally transcript-mining — never hand-written from conversation memory.** Why: hand-writing produced a thin handover that dropped half the loose ends.

## Important References
- `.claude/skills/marshall/SKILL.md` → "Cold start — orient, surface, ASK" — the behavioural fix.
- `backlog/2026-06-08-session-handover.md` — the COMPLETE prior-session handover (the completeness bar to match).
- memory `session-handover-not-compaction` — root-cause + the mine-the-transcript fix.
- `appydave:capture-context` skill (this one) — the designated handover tool; `appydave:near-compaction` orchestrates the family (`session-checkpoint` + `capture-context` + `knowledge-capture`).
- Transcript mining: `~/.claude/projects/<proj-slug>/<session-id>.jsonl`, summarised via the `abridge` subagent.

## Active Files
- `.claude/skills/marshall/SKILL.md` — added cold-start section, scoped "Take"/anti-menu rules to mid-session.
- `backlog/2026-06-08-session-handover.md` — rewritten from the transcript (complete).
- memory `cold-start-orient-and-ask.md` (new), `session-handover-not-compaction.md` (edited).

## What We Ruled Out
- **"Compaction caused the thin handover" — FALSE.** The loose-ends survived compaction (David's pasted list *came from* the post-compaction conversation). The info was available; it was never *captured*. Do not repeat this excuse, and do not assert a causal claim without verifying it.
- **Hand-writing handovers from in-conversation memory** — that IS the bug (a `Write` call at end-of-session captures only what you happen to remember).
- **Building DF-3 inline via Marshall** — wrong on protocol; reverted.

## Gotchas / Watch Out For
- **Do not dispatch or build on a bare `/marshall`.** Surface the threads and ask.
- **DF-3 is NOT built** (a deleted memory once wrongly claimed it was).
- **`capture-context` warns repo handover docs "go stale and poison future sessions"** and prefers `~/.claude/sessions/`. But dark-factory's convention + the Marshall cold-start read from `backlog/`. **Unresolved — feed into DF-6 design** (e.g. dated files, never edit-in-place, a "latest" pointer, or relocate handovers out of the repo).
- The deepest pattern here is David's own: **"the trigger is the weak link, not the storage."** The skills existed; they were never fired. DF-6 should make the trigger automatic, not rely on memory.

## Options (for DF-6 — not directives)
1. Build a **transcript-mining handover skill** (the abridge-the-`.jsonl` approach proven this session).
2. **Extend the `capture-context` family** to add transcript-mining + the loose-ends taxonomy (awaiting-eyes / decisions / named-but-unbuilt / hygiene / forks).
3. Defer the build; keep using `capture-context` manually + `abridge` for long/compacted sessions.

## How to Resume
Read this + `2026-06-08-session-handover.md` + `MEMORY.md`. Summarise what you understand, then ask David what to work on today. Do not implement until directed.
