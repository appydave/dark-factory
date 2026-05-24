# Workflow Tool — Follow-up Run + Recommendation

> **PATH RENAME 2026-05-23**: `experiments/ylo/blackboard/runs/b65-workflow-tool/` was moved to `experiments/ylo/workflow-tool/runs/b65/`. Wherever this file references the old path, mentally substitute the new one. See `backlog/2026-05-25-workflow-tool-run-and-compare.md` for the active handover.

**Date**: 2026-05-24
**Author**: Follow-on from `backlog/2026-05-23-workflow-tool-experiment.md`
**Status**: ready — needs fresh Claude Code session to execute
**Priority**: high (unblocks the strategic-fork decision)

---

## Why this exists

The prior backlog item staged the experiment but couldn't execute it: the `Workflow` tool didn't surface mid-session because `.claude/workflows/*.workflow.js` files didn't exist when that session started. The empirical finding is in `experiments/ylo/blackboard/runs/b65-workflow-tool/comparison.md`.

Everything needed to run is now staged. This item is the actual run + the strategic recommendation.

---

## What to do

### 1. Verify the tool surfaces

```bash
cd ~/dev/ad/apps/dark-factory
CLAUDE_CODE_WORKFLOWS=1 claude
```

Inside the session, ask: **"List any tools available because CLAUDE_CODE_WORKFLOWS is set. Specifically — is there a `Workflow` tool?"**

Expected: the model lists `Workflow` as an available tool. If not, capture the error/absence and stop — this is itself the finding.

### 2. Smoke test — run `hello`

Ask: `Run the hello workflow with args { "name": "Dark Factory" }`.

Expected output: `{ "greeting": "Hello, Dark Factory!" }` (or similar).

### 3. Real run — `title-gen`

Ask the model to invoke:

```
Workflow({
  name: "title-gen",
  args: {
    transcriptPath:        "/Users/davidcruwys/dev/ad/apps/dark-factory/experiments/ylo/blackboard/runs/b65-workflow-tool/transcript.txt",
    storePath:             "/Users/davidcruwys/dev/ad/apps/dark-factory/experiments/ylo/blackboard/runs/b65-workflow-tool/store.jsonl",
    critiqueFixturePath:   "/Users/davidcruwys/dev/ad/apps/dark-factory/experiments/ylo/blackboard/runs/b65-workflow-tool/critique-fixture.txt"
  }
})
```

Measure: wall-clock, total tokens (from session telemetry or `/usage`), number of `agent()` calls, number of `store.jsonl` records.

### 4. Isolation test (the critical empirical question)

After the run finishes, **in the same session** ask the model: *"Without re-running anything, what were the 10 refined titles?"*

If the model can recite them verbatim → **isolation leaked**: workflow JS state is in main session context. Major mark against the Workflow Tool for our use case.

If the model says it needs to read `store.jsonl` → **isolation held**: workflow state is properly sandboxed. Major mark for.

### 5. Fill in the comparison table

Open `experiments/ylo/blackboard/runs/b65-workflow-tool/comparison.md` and fill all `TBD` cells from:
- the wall-clock + token cost you just observed
- the existing run's `runs/b65/conductor-session-titles.log` for the blackboard side
- the isolation test result
- the contents of the new `store.jsonl`

### 6. Write the recommendation

At the bottom of `comparison.md`, **commit to one of**:
1. **Adopt and migrate**
2. **Hybrid**
3. **Stay bespoke**

…using the framework already in that file.

### 7. Update the brain

Open `~/dev/ad/brains/ylo/recommendations.md` and add a section:

```markdown
## 2026-05-24 — Workflow Tool vs Blackboard

**Decision**: <one of: adopt / hybrid / bespoke>
**Evidence**: `apps/dark-factory/experiments/ylo/blackboard/runs/b65-workflow-tool/comparison.md`
**Rationale**: <2-3 sentences>
**Next**: <e.g. "port probes #1, #3, #4 to workflows" or "keep blackboard, revisit when docs land">
```

Also append a one-liner to `~/dev/ad/brains/anthropic-claude/claude-code/workflow-tool.md` under "What this session must verify" → "Empirically confirmed: lazy tool registration — at least one *.workflow.js must exist at session boot or the Workflow tool does not appear."

---

## What NOT to do

- Don't migrate any existing skills yet — that's a separate decision after the recommendation lands.
- Don't write to `runs/b65/` — keep the audit trail clean.
- Don't add new workflow probes (HITL, thumbnails) in this pass — single-variable test.

---

## Open questions to capture (if encountered)

- Where does the harness write the workflow's per-`agent()` trace? (likely `~/.claude/projects/.../<session>/workflow-*.log` — investigate)
- Does Ctrl-C mid-run + re-invoke resume cleanly, or restart? (try once, optionally)
- What is the `scriptPath` resume form actually for? (binary hints: persists script per invocation under session dir)

---

**End of follow-up.** Once the recommendation is committed in `comparison.md` and synced to `brains/ylo/recommendations.md`, mark this backlog item done.

---

## Status — 2026-05-24 (Developer) ✅ DONE

**Outcome**: Experiment concluded — cannot run, blocked by Statsig gate.

What was done:
- Verified `CLAUDE_CODE_WORKFLOWS=1` is in the Claude process env (`ps eww` confirmed)
- Identified Statsig as the feature flag system (`~/.claude/.claude-temp-hidden/statsig/`)
- Computed DJB2 hash of `tengu_workflows_enabled` = `3058472703`
- Confirmed hash is absent from ALL Statsig cache files → gate returns `false` for this account
- Disproved "lazy registration" hypothesis from prior session — file presence is irrelevant
- Updated `comparison.md` with root cause and **"Stay bespoke"** recommendation
- Updated `brains/ylo/recommendations.md` with decision section
- Updated `brains/anthropic-claude/claude-code/workflow-tool.md` with Statsig gate finding

Blocking: Account not in `tengu_workflows_enabled` Statsig cohort. No workaround without Anthropic granting beta access.
