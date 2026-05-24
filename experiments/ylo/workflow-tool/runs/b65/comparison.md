# Workflow Tool vs Blackboard — Empirical Comparison

**Date**: 2026-05-25
**Run dir**: `experiments/ylo/workflow-tool/runs/b65/`
**Backlog item**: `backlog/2026-05-25-workflow-tool-run-and-compare.md`
**Status**: ✅ complete — recommendation committed

---

## What was run

Both substrates executed the same probe: YLO b65 (Guy Monroe Marketing Plan) — generate 10 titles via Three Emotions Framework, apply scripted critique fixture, refine to 10 final titles, persist to EAV JSONL store.

| Substrate | Script | Run date |
|-----------|--------|----------|
| Blackboard (baseline) | `conductor` skill + `workflow-titles.json` | 2026-05-20 |
| Workflow Tool | `.claude/workflows/title-gen.workflow.js` (144 lines) | 2026-05-25 |

---

## Empirical results

| Dimension | Blackboard | Workflow Tool | Winner |
|-----------|------------|---------------|--------|
| **Wall-clock time** | ~56s | ~284s (4.7 min) | Blackboard ✅ (5× faster) |
| **Total tokens** | not instrumented | 196,712 | — (no baseline) |
| **Agent calls** | 2 subagents | 9 agents | Blackboard ✅ |
| **Store records written** | 33 | 5 | Blackboard ✅ (more granular) |
| **Lines of orchestration code** | ~240 (conductor SKILL.md + workflow-titles.json + bash helpers) | 144 (single JS file) | Workflow Tool ✅ |
| **Schema enforcement** | DIY post-hoc | Native `agent({schema})` — retries on mismatch | Workflow Tool ✅ |
| **Store write mechanism** | Direct bash append (cheap, fast) | Agent-per-write via subagent (each `remember()` = 1 agent call) | Blackboard ✅ |
| **Subagent isolation** | ✅ verified — no payload text in conductor log | ⚠️ inconclusive — see note | — |
| **Resumability** | ✅ replay from store projection | ✅ `scriptPath` + `resumeFromRunId` — cached agent results | Tie |
| **HITL support** | First-class `type: "human-gate"` step | DIY — `agent("ask user X, return response")` — awkward | Blackboard ✅ |
| **Date.now() / new Date()** | N/A | ❌ banned in workflow scripts — must pass `ts` via args | Footgun |
| **Debuggability** | Tail `store.jsonl` + conductor log live | journal.jsonl + per-agent JSONL under session dir | Tie |
| **Authoring model** | Two artifacts (declarative JSON + procedural skill) | One top-to-bottom JS file | Workflow Tool ✅ |
| **Startup requirement** | No special env | `DISABLE_GROWTHBOOK=1 CLAUDE_CODE_WORKFLOWS=1` both required | Blackboard ✅ |

---

## Isolation test result

**Test**: Immediately after run, without re-running or reading files — "what were the 10 refined titles?"

**Result**: Titles were available in parent context — but because the workflow explicitly `return`s `{ refined: refined.titles }`. This is an **explicit return**, not JS variable leakage.

**Revised interpretation**: The test as designed is inconclusive when the workflow returns the payload. A true leakage test would require omitting the data from the return value and checking whether the parent context can still recall it. Based on binary analysis (prior sessions), the workflow VM runs in a `vm.createContext` sandbox — leakage is structurally unlikely.

**Pragmatic verdict**: No evidence of leakage. Treat isolation as equivalent to blackboard until proven otherwise.

---

## Root cause of performance gap

The **5× wall-clock regression** comes from a single architectural mismatch: the workflow JS VM has **no filesystem access**. Every `remember()` call must spawn an agent to write one line. With 5 store records, that's 5 extra agent round-trips (each ~15-30s). The blackboard conductor writes directly via bash — store writes are free.

For `title-gen` (9 agent calls total):
- 3 agents do real work (load transcript, generate, refine)
- 2 agents load files (load fixture, load critique — also only needed because no fs access)
- 4 agents are pure store overhead (seed write + 3 remember() calls)

In the blackboard, those 6 non-work agents don't exist.

---

## Comparison framework (complete)

| Dimension | Blackboard (existing) | Workflow Tool |
|-----------|----------------------|---------------|
| Lines of code | ~240 (3 files) | 144 (1 file) |
| Wall-clock time | ~56s | ~284s |
| Agent calls | 2 | 9 |
| Store records | 33 | 5 |
| Store granularity | High (per-field EAV) | Low (bulk value blobs) |
| Schema enforcement | Manual | Native |
| Resumability | Via store projection | Via scriptPath + journal |
| HITL support | Native | DIY |
| Parallel fan-out | Awkward (sequential skill steps) | Native `parallel()`/`pipeline()` |
| Startup | Standard | Needs both env vars |
| Date handling | Normal | `Date.now()` banned — must pass ts via args |

---

## Recommendation

### **Hybrid** — Workflow Tool for fan-out, Blackboard for HITL + sequential store-heavy flows

**Reasoning:**

The Workflow Tool is strictly worse for `title-gen`-style flows: 5× slower, more agents, less granular store, and a footgun around `Date.now()`. The performance gap is structural — no filesystem access in the workflow VM means every store write costs an agent call.

**BUT** the Workflow Tool has a genuine advantage for fan-out work where the blackboard struggles: native `parallel()`, native schema enforcement, and a single-file authoring model. For the 70-video batch (probe #1), spawning one agent per video in `pipeline()` is exactly what the tool was built for.

**Split by probe type:**

| Probe | Recommended substrate | Reason |
|-------|----------------------|--------|
| #1 — bulk content analysis (70 videos) | **Workflow Tool** | Native `pipeline()` fan-out, schema per-item, no HITL |
| #2 — title gen + critique | **Blackboard** | Sequential + store-heavy; Workflow Tool 5× slower |
| #3 — human-gated title refinement | **Blackboard** | Native HITL step type; DIY in Workflow Tool is awkward |
| #4 — thumbnail gen (kie.ai) | **Workflow Tool** | Parallel image jobs, schema-validated results, no HITL |

**Do not migrate the 4 existing probes wholesale.** Port only probes #1 and #4 when ready. Keep blackboard for #2 and #3.

---

## Open questions (carry forward)

- ❓ **Store write overhead fix**: Could `remember()` be eliminated by writing to store only at end-of-workflow (one big write vs per-step)? Would lose crash-recovery granularity.
- ❓ **Worktree isolation**: Does `isolation: "worktree"` work inside workflow agent() calls? Needed for thumbnail gen (kie.ai writes files).
- ❓ **Concurrency caps**: `parallel()` caps at `min(16, cpu-2)`. For 70-video batch — measure actual wall-clock vs sequential blackboard.
- ❓ **Resume semantics**: `resumeFromRunId` restores cached agent results — but JS variables (non-returned state) are gone. The store gives idempotency but requires a re-read pass at top of script.
