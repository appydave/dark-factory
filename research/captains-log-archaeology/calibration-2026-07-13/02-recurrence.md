# Recurrence Analysis — What David Kept Saying (2026-06-29 → 2026-07-13)

**Purpose**: Cluster the 102 mined records on `fingerprint` (semantic near-duplicates merged) to surface ideas David raised repeatedly — "said X times over N days" — ranked by repetition.

**For Agents**:
- Repetition is David's implicit priority signal: things said 3+ times without resolution are the real backlog.
- Note the confound: 07-06 onward David deliberately dual-recorded on OMI + Plaud (transcription bake-off), so some pairs are device duplicates, not re-raisings. These are flagged.

---

## Ranked Recurrence Table

| Rank | Idea (merged fingerprints) | Mentions | Span | Dates |
|------|---------------------------|----------|------|-------|
| 1 | **Captain's Log unified capture pipeline** (unify OMI+Plaud → controller → extension → intelligence hub) | **15** | 9 days | 07-05 (×2), 07-06 (×3), 07-09, 07-11, 07-12 (×3), 07-13 (×5) |
| 2 | **Dark Factory autonomy & governance** (sprint → harness feedback → governance breakdown → roadmap reset) | **8** | 12 days | 07-02, 07-03 (×3, incl. 1 dup capture), 07-09 (×2), 07-10, 07-13 |
| 3 | **Extension architecture / SDK gaps** (iframe, repo-per-extension, own web server, host cron + chat access) | **7** | 11 days | 06-29, 07-03 (×2), 07-05, 07-07, 07-13 (×2) |
| 4 | **KDD/Lisa scope & guardrails** ("factory writes knowledge but nothing reads it"; Lisa mis-routing; KDD-folder-only) | **5** | 5 days | 07-03, 07-04 (×2), 07-07 (×2 incl. refresh-context gripe) |
| 5 | **Challenge DV / Linda FDE retainer** (price walked $5k → $3,300 → $2,750) | **4** | 7 days | 07-07 (×2 device dup), 07-13 (×2) |
| 6 | **Kybernesis doc-watcher / first-agent pilot on Roamy** | **3** | 8 days | 07-06 (×2 — device dup), 07-13 |
| 7 | **Talk to / control KyberAgent from Claude Code** | **3** | 8 days | 07-06 (×2 — device dup), 07-09 (control-surfaces mandate) |
| 8 | **Gling automation** (replace → inject MCP into Electron app) | **3** | 8 days | 07-04, 07-11 (×2) |
| 9 | **OMI extension was built wrong** (half-assed fork; bypassed skills; must be superseded) | **3** | 2 days | 07-05 (×2), 07-06 |
| 10 | **Thumbnail generation tooling** (generator extension + prompt-pacing TUI + shortlisting matrix) | **3** | 4 days | 06-30 (×2), 07-03 (as an explicit carve-out: David keeps it manual) |
| 11 | **Temporal/thematic linkage between captures** (compare micro-conversations; quest/side-quest threading) | **2** | 8 days | 07-06, 07-13 |
| 12 | **Plaud refresh-token brittleness → automate daily refresh** | **2** | 2 days | 07-12, 07-13 (escalated to "highest priority") |
| 13 | **Angela / Achieve NDIS engagement** | **2** | 3 days | 07-07, 07-09 |
| 14 | **Smart contracts as agent work-verification** (rubrics at end of unit of work) | **2–3** | 3 days | 07-07 (×2), 07-09 |
| 15 | **Recipes as product** (recipe skill; sell recipes; extension recipe regenerates app) | **2–3** | 2 days | 06-29, 06-30 (×2) — then silent |
| 16 | **Affiliate email triage (AITLDR)** | **2** | 2 days | 07-12, 07-13 (deferred to Jan + Mary) |
| 17 | **Extensions must serve humans AND agents / discovery metadata** | **2** | 1 day | 07-04 (×2) |
| 18 | **refresh-context misuse on documented repos** | **1 capture, self-reported "a few times"** | — | 07-07 (recurring gripe by David's own account) |

---

## Reading the table

**The pipeline itself is the obsession.** The #1 idea (15 mentions over 9 days) is the tool for managing the very captures being analyzed. David returned to Captain's Log on 6 of the 9 days after conceiving it, with the densest day (07-13, 5 captures) being the most recent — accelerating, not fading.

**Three-mention items are the silent backlog.** Ranks 6–10 are all things said ~3 times and still not done: the Roamy pilot agent (planned twice, 7 days apart, never started), Claude Code ↔ KyberAgent control (asked as a question twice, then mandated), and Gling (deadline missed, plan mutated).

**Device-duplicate caveat.** Ranks 5, 6, 7 each contain one OMI/Plaud dual-recording pair (07-06 and 07-07). Counting unique *utterance events*, they are 3, 2, and 2 respectively — still recurrent, but the bake-off inflates raw counts. Any production recurrence detector needs same-day cross-device dedup before counting.

**One-day bursts vs slow burns.** Skill-registry (rank 17) and recipes (rank 15) are single-burst ideas that never re-surfaced — candidates for "was this abandoned or just parked?" prompts. By contrast, Dark Factory governance (rank 2) is a slow burn spread across the whole fortnight — a persistent worry, not a passing thought.

**Escalation signal.** The Plaud token item (rank 12) went from "idea" (07-12) to "highest-priority item" (07-13) in one day — recency + explicit priority language should outrank raw count for actioning.
