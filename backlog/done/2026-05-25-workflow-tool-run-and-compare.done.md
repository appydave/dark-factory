# Anthropic Workflow Tool — Run `title-gen` and Complete the Comparison

**Date**: 2026-05-25
**Author**: Follow-on from `backlog/2026-05-24-workflow-tool-followup.md`
**Status**: ready
**Priority**: high

---

## 🎯 Goal

Run the native Anthropic **Workflow Tool** against the same YLO title-generation scenario (probe #2) we already ran with the bespoke blackboard pattern, then write up the side-by-side comparison and pick a recommendation: **adopt / hybrid / stay bespoke**.

The Workflow Tool gate is OPEN on this account (confirmed 2026-05-23 — smoke test passed: `{"result":"WORKFLOW_OK"}` in 2.9s).

---

## 🚀 How to start Claude correctly for this session

In a **fresh terminal**:

```bash
cd ~/dev/ad/apps/dark-factory
DISABLE_GROWTHBOOK=1 CLAUDE_CODE_WORKFLOWS=1 claude
```

**Both env vars are required.** `CLAUDE_CODE_WORKFLOWS=1` enables the feature; `DISABLE_GROWTHBOOK=1` bypasses the GrowthBook gate check (confirmed necessary as of 2026-05-25 — without it the tool does not surface even with the feature flag set). The gate evaluates once at boot and caches — there is **no mid-session way** to enable it; if you forget either var, exit and restart.

---

## 📋 Step-by-step

### 1. Verify the tool surfaces

```
ToolSearch select:Workflow
```

Expected: a `Workflow` tool schema is returned. Stop and report if not.

### 2. Smoke test (sanity)

```
Run the hello workflow with args { "name": "Dark Factory" }
```

Should complete in ~3s with `{"greeting": "..."}`.

### 3. Run the real probe — `title-gen`

```
Workflow({
  name: "title-gen",
  args: {
    transcriptPath:      "/Users/davidcruwys/dev/ad/apps/dark-factory/experiments/ylo/workflow-tool/runs/b65/transcript.txt",
    storePath:           "/Users/davidcruwys/dev/ad/apps/dark-factory/experiments/ylo/workflow-tool/runs/b65/store.jsonl",
    critiqueFixturePath: "/Users/davidcruwys/dev/ad/apps/dark-factory/experiments/ylo/workflow-tool/runs/b65/critique-fixture.txt"
  }
})
```

**Measure during the run:**
- Wall-clock time end-to-end (before/after the call)
- Total tokens (use `/usage` delta, or session telemetry)
- Number of `agent()` calls fired
- Number of records written to `store.jsonl`

### 4. THE CRITICAL ISOLATION TEST

**Immediately after the run finishes**, in the same session, with no other prompts between:

> "Without re-running anything and without reading any files, what were the 10 refined titles from that workflow?"

- **Model recites verbatim** → workflow JS state leaked into parent context. ❌ Major mark against the Workflow Tool for isolation.
- **Model says it needs to read `store.jsonl`** → state stayed in the workflow's VM context. ✅ Major mark for.

This is THE empirical question — it determines whether the Workflow Tool preserves the blackboard's isolation guarantee.

### 5. Fill in `comparison.md`

File: `experiments/ylo/workflow-tool/runs/b65/comparison.md`

TBD cells that need real data:
- Wall-clock time end-to-end (both substrates)
- Total token cost — workflow side from your run; blackboard side from `experiments/ylo/blackboard/runs/b65/conductor-session-titles.log`
- Resumability — try Ctrl-C mid-run + re-invoke with same `scriptPath`
- Subagent isolation — from step 4
- Debuggability — check `~/.claude/projects/.../<session>/` for any workflow trace files post-run

### 6. Commit to a recommendation

At the bottom of `comparison.md`, pick one:

1. **Adopt and migrate** — Workflow tool is strictly better. Port the 4 existing probes to `*.workflow.js`, retire bash+jq conductor.
2. **Hybrid** — Workflow Tool for fan-out + schema-validated work; blackboard for HITL + complex state.
3. **Stay bespoke** — workflow tool has footguns; revisit later.

### 7. Sync the brain

Update `~/dev/ad/brains/ylo/recommendations.md` — the `## 2026-05-24 — Workflow Tool vs Blackboard` section currently says "Stay bespoke (cannot evaluate)". Replace with the real recommendation + evidence pointer to `experiments/ylo/workflow-tool/runs/b65/comparison.md`.

Update `~/dev/ad/brains/anthropic-claude/claude-code/workflow-tool.md`:
- Status: ⚗️ Experimental → ✅ Verified-working
- Add a note about the GrowthBook gate history (was blocked, now open on this account)

---

## ⚠️ What NOT to do

- Don't re-investigate the gate — it's solved. Smoke test passed. If it works for `hello`, it works.
- Don't migrate existing blackboard skills yet — that decision waits on this experiment.
- Don't pollute `experiments/ylo/blackboard/runs/b65/` — that's the blackboard baseline.
- Don't run any OTHER workflow probes in this session. Single-variable test.

---

## 📂 Directory layout (post-restructure)

```
experiments/ylo/blackboard/
├── runs/b65/                                  ← blackboard baseline (probe #2 done — DO NOT MODIFY)
└── runs/b65-2-5/                              ← (other prior blackboard run)

experiments/ylo/workflow-tool/                 ← NEW: Workflow Tool substrate
└── runs/b65/                                  ← this experiment
    ├── transcript.txt                         ← same source as experiments/ylo/blackboard/runs/b65/
    ├── critique-fixture.txt
    ├── store.jsonl                            ← empty; workflow populates
    └── comparison.md                          ← framework ready, TBD cells to fill

.claude/workflows/
├── hello.workflow.js                          ← smoke test (already passed)
└── title-gen.workflow.js                      ← the real probe (144 lines)
```

---

## 🔑 Key context (don't waste cycles re-deriving)

### The gate (history)

The `Workflow` tool is gated by:
1. `CLAUDE_CODE_WORKFLOWS=1` env var at session boot
2. GrowthBook flag `tengu_workflows_enabled` (was off for this account 2026-05-24, opened 2026-05-23)

Binary gate logic:
```js
function bp() {
  if (!mH(process.env.CLAUDE_CODE_WORKFLOWS)) Dw_ = false;
  else Dw_ = k_("tengu_workflows_enabled", true);
  return Dw_;
}
```

`Dw_` is cached at boot; no mid-session re-evaluation. That's why the env var must be set BEFORE `claude` is invoked.

### Filed and closed

GitHub issue **#61637** at `anthropics/claude-code` was opened asking about the gate, then closed when the tool started working.

---

## 📚 Reference reading order

1. **`backlog/2026-05-23-workflow-tool-experiment.md`** — original strategic context (full Read of § "What this session must verify" + § "Reference reading")
2. **`backlog/2026-05-24-workflow-tool-followup.md`** — gate investigation (marked DONE)
3. **`experiments/ylo/workflow-tool/runs/b65/comparison.md`** — the framework + TBD cells you'll fill in
4. **`~/dev/ad/brains/anthropic-claude/claude-code/workflow-tool.md`** — API reference for `agent()`/`phase()`/`pipeline()`/`parallel()`
5. **`~/dev/ad/brains/anthropic-claude/claude-code/blackboard-workflow-pattern.md`** — the pattern being compared

---

## ✅ End-of-session checklist

- [x] `experiments/ylo/workflow-tool/runs/b65/comparison.md` has all TBD cells filled
- [x] One final recommendation committed at the bottom of comparison.md
- [x] `brains/ylo/recommendations.md` § 2026-05-24 updated with the real call
- [x] `brains/anthropic-claude/claude-code/workflow-tool.md` status moved out of ⚗️
- [x] This file renamed to `2026-05-25-workflow-tool-run-and-compare.done.md` with a 5-line summary appended at the bottom

---

## Summary (2026-05-25)

Ran `title-gen` workflow end-to-end against b65 transcript. Workflow Tool completed in ~284s using 9 agents and 196,712 tokens vs blackboard's ~56s and 2 agents — a 5× wall-clock regression driven by store writes requiring a full agent call each (no filesystem access in the workflow VM). Recommendation: **Hybrid** — keep blackboard for sequential HITL + store-heavy flows (#2, #3); adopt Workflow Tool for parallel fan-out work (#1 bulk analysis, #4 thumbnails). `Date.now()` is banned in workflow scripts (pass `ts` via args). Both `DISABLE_GROWTHBOOK=1` and `CLAUDE_CODE_WORKFLOWS=1` are required at startup.
