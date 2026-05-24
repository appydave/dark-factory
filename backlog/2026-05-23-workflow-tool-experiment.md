# Workflow Tool Experiment — Handover

> **PATH RENAME 2026-05-23**: `experiments/ylo/blackboard/runs/b65-workflow-tool/` was moved to `experiments/ylo/workflow-tool/runs/b65/`. Wherever this file references the old path, mentally substitute the new one. See `backlog/2026-05-25-workflow-tool-run-and-compare.md` for the active handover.

**Date**: 2026-05-23
**Author**: Brain session (PO side), to be picked up by a fresh Claude Code session in `~/dev/ad/apps/dark-factory/`
**Status**: ready-to-build — empirical first moves required
**Priority**: high (strategic-fork decision)

---

## TL;DR for the new session

Open a session in this repo. Set `CLAUDE_CODE_WORKFLOWS=1`. Verify the new native **Workflow Tool** primitive works on this machine. Build one workflow (`title-gen.workflow.js`) that replicates **YLO probe #2** behaviour using the native primitive instead of our bash+jq blackboard conductor. Wire it into the existing EAV store at `experiments/ylo/blackboard/runs/b65/store.jsonl` via `remember()` / `recall()` helpers defined inline. Compare cost, complexity, resumability, and audit-trail against the existing blackboard implementation. Write a comparison report. Do not delete the existing blackboard conductor or store — both must keep working.

---

## Why this exists

We've been building a bespoke "blackboard workflow pattern" for the YLO (YouTube Launch Optimizer) rebuild — 4 probes shipped successfully. As of 2026-05-23, a native Claude Code feature (the **Workflow Tool**, gated behind `CLAUDE_CODE_WORKFLOWS=1`, available in v2.1.147+) ships the orchestration half of what we've been hand-rolling. It does NOT ship the durable-store half. Strategic question: **lean native, stay bespoke, or hybridise.**

Before we make that decision, we need to actually use the native tool against a real YLO scenario.

---

## Context — where we've been

### YLO blackboard experiment (lives in this repo)

- **Substrate spec**: `~/dev/ad/brains/anthropic-claude/claude-code/blackboard-workflow-pattern.md` — the pattern we built. Conductor + store + isolated subagents + EAV append-only log + last-write-wins projection.
- **Skills built and battle-tested in this repo**:
  - `.claude/skills/conductor/` — orchestrator role spec (declarative — Claude reads SKILL.md and walks the loop)
  - `.claude/skills/store/` — bash `remember` / `recall` / `project` over JSONL
  - `.claude/skills/image-gen/` — kie.ai async polling wrapper
- **Workflows declared and tested**: at `experiments/ylo/blackboard/workflow*.json`
- **Test asset**: `experiments/ylo/blackboard/runs/b65/` (b65 = Guy Monroe Marketing Plan, full transcript + bulk-analysis outputs + titles + thumbnails)
- **Probes that passed**: 4 (see plans at `~/dev/ad/brains/plans/plan-ylo-blackboard-*.md`)
  - #1 bulk content analysis (12-parallel)
  - #2 title generation with scripted critique fixture
  - #2.5 title generation with REAL human gate
  - #3 thumbnail workflow (Flux Schnell + Nano Banana 2, fixture-based selection)

### What's new — the native Workflow Tool

A `*.workflow.js` file in `.claude/workflows/` that runs deterministically top-to-bottom as plain JavaScript when invoked by the harness. Six ambient globals: `meta`, `agent`, `phase`, `pipeline`, `parallel`, `log`. Plus `args` (input) and `return` (output). No `import` statements. No filesystem/shell access from the body — every I/O action goes through `agent()` subagent calls.

Reverse-engineered docs at: `~/dev/ad/brains/anthropic-claude/claude-code/workflow-tool.md`

Production reference corpus at: `~/dev/upstream/repos/bun/.claude/workflows/` (53 files from the Bun team's Zig→Rust porting effort) plus `~/dev/upstream/repos/bun/.context/CONTEXT.md` (a deep comprehension doc).

**This is reverse-engineered, not from official Anthropic docs.** The brain note explicitly says "treat signatures as observed-true, expect refinement when docs land."

---

## What this session must verify (the empirical part)

**The literal invocation mechanic is not documented.** The brain note says "see what tool/command surface appears" when the env var is set. So step 1 is empirical discovery.

### Step 1 — Verify the tool surfaces

```bash
# From a fresh terminal
claude --version
# Need ≥ 2.1.147. If lower, update Claude Code via your normal mechanism.

cd ~/dev/ad/apps/dark-factory
CLAUDE_CODE_WORKFLOWS=1 claude
```

Inside the session:
1. Type `/help` — note any new commands
2. Type `/` and tab — see if a `/workflow` or similar appears
3. Ask Claude: "Do you have access to a workflow tool? List any new tools or commands available because CLAUDE_CODE_WORKFLOWS is set."
4. Note the answer — that's the invocation mechanic

### Step 2 — Hello-world workflow

Create `~/dev/ad/apps/dark-factory/.claude/workflows/hello.workflow.js`:

```javascript
export const meta = {
  name: "hello",
  description: "Smallest possible workflow — prove the substrate works",
  phases: [{ title: "Greet" }]
};

const A = typeof args === "string" ? JSON.parse(args) : args || {};

phase("Greet");
const result = await agent(
  `Say hello to ${A.name || "world"} in one short sentence.`,
  { schema: { type: "object", required: ["greeting"],
              properties: { greeting: { type: "string" }}}}
);

return { greeting: result?.greeting ?? "no greeting received" };
```

Invoke it using whatever mechanic step 1 revealed. Expected output: `{ greeting: "Hello, ..." }`.

If this works, the substrate is operational on this machine. If it fails, the failure mode tells us what's wrong (env var not honoured, version mismatch, syntax error, etc.).

### Step 3 — Build `title-gen.workflow.js` (the real probe)

Replicate YLO probe #2 (title generation + scripted critique + refinement) as a native workflow. Wire it into the EAV store at `experiments/ylo/blackboard/runs/b65/store.jsonl` so the audit trail is preserved.

#### Skeleton

```javascript
// .claude/workflows/title-gen.workflow.js
export const meta = {
  name: "title-gen",
  description: "Generate 10 titles, apply critique, refine. Persists to EAV store.",
  phases: [{ title: "Generate" }, { title: "Critique" }, { title: "Refine" }]
};

const A = typeof args === "string" ? JSON.parse(args) : args || {};
if (!A.transcript || !A.storePath || !A.critiqueFixturePath) {
  return { error: "args required: transcript, storePath, critiqueFixturePath" };
}

// === EAV STORE HELPERS — inline because no imports ===
// Format matches existing experiments/ylo/blackboard store.jsonl:
//   { key, group?, index?, value, meta: { step, ts, attempt, source } }

async function remember(key, value, meta = {}) {
  const record = {
    key,
    group: meta.group ?? null,
    index: meta.index ?? null,
    value,
    meta: { ...meta, ts: new Date().toISOString() }
  };
  const r = await agent(
    `Append this exact JSON line (no formatting changes) to file ${A.storePath}:\n${JSON.stringify(record)}\nReturn { ok: true } on success.`,
    { schema: { type: "object", required: ["ok"], properties: { ok: { type: "boolean" }}}}
  );
  if (!r?.ok) throw new Error(`store write failed for key=${key}`);
}

async function recall(key) {
  const r = await agent(
    `Read JSONL file ${A.storePath}. Find the LATEST record where key="${key}". Return its value as { value: ... }. If no such record exists, return { value: null }.`,
    { schema: { type: "object", required: ["value"], properties: { value: {} }}}
  );
  return r?.value ?? null;
}

// === SCHEMAS ===
const TITLES_S = {
  type: "object", required: ["titles"],
  properties: {
    titles: {
      type: "array", minItems: 10, maxItems: 10,
      items: { type: "object", required: ["emotion", "chars", "title"],
               properties: {
                 emotion: { enum: ["CURIOSITY", "DESIRE", "FEAR"] },
                 chars: { type: "integer" },
                 title: { type: "string" }
               }}
    }
  }
};

// === WORKFLOW ===
phase("Generate");
const gen = await agent(
  `Generate 10 YouTube titles using the Three Emotions Framework (CURIOSITY/DESIRE/FEAR), 40-50 char optimal length. Transcript:\n${A.transcript}\nReturn { titles: [{ emotion, chars, title }, ...] }.`,
  { schema: TITLES_S }
);
if (!gen) return { error: "generation failed" };
await remember("generatedTitles", gen.titles, { step: "generate-titles", attempt: 1 });

phase("Critique");
const critique = await agent(
  `Read the critique from file ${A.critiqueFixturePath}, return { critique: "..." }.`,
  { schema: { type: "object", required: ["critique"], properties: { critique: { type: "string" }}}}
);
await remember("titleCritiqueLog", critique.critique, { step: "apply-critique", attempt: 1, source: "fixture" });

phase("Refine");
const refined = await agent(
  `Refine these 10 titles based on the critique. Same Three Emotions Framework + char limits.\nOriginal:\n${gen.titles.map(t => `[${t.emotion} ${t.chars}c] ${t.title}`).join("\n")}\nCritique: ${critique.critique}\nReturn { titles: [{ emotion, chars, title }, ...] }.`,
  { schema: TITLES_S }
);
await remember("generatedTitles", refined.titles, { step: "refine-titles", attempt: 2 });
await remember("selectedTitles", refined.titles, { step: "refine-titles", source: "refined" });

return {
  generated: gen.titles,
  critique: critique.critique,
  refined: refined.titles,
  storePath: A.storePath
};
```

#### Invocation args

```json
{
  "transcript": "<concat of runs/b65/transcript.txt>",
  "storePath": "/Users/davidcruwys/dev/ad/apps/dark-factory/experiments/ylo/blackboard/runs/b65-workflow-tool/store.jsonl",
  "critiqueFixturePath": "/Users/davidcruwys/dev/ad/apps/dark-factory/experiments/ylo/blackboard/runs/b65/critique-fixture.txt"
}
```

Note: use `runs/b65-workflow-tool/` (a NEW directory) so the experiment doesn't pollute the existing `runs/b65/` audit trail. Pre-populate it with a copy of `transcript.txt` and an initial empty `store.jsonl`.

### Step 4 — Compare and report

After the run, write `~/dev/ad/apps/dark-factory/experiments/ylo/blackboard/runs/b65-workflow-tool/comparison.md` covering:

| Dimension | Blackboard (existing) | Workflow Tool (this run) | Notes |
|-----------|----------------------|--------------------------|-------|
| Lines of code authored | conductor SKILL.md + workflow-titles.json + bash | title-gen.workflow.js | Count both |
| Wall-clock time end-to-end | (look up from existing run logs) | (measure) | |
| Total token cost | (sum from existing run) | (sum from this run) | |
| Schema enforcement | DIY post-hoc | Native `agent({schema})` | |
| Resumability if mid-run crash | Yes — replay from store | ? — needs test | Try Ctrl-C mid-run and re-invoke |
| Audit trail completeness | Full event log | Full event log via `remember()` | Should match |
| Subagent isolation verified | Yes — no payload in conductor log | Test the same way — grep title text against the workflow's visible output | Critical: is the workflow body's `gen.titles` variable considered "orchestrator context"? Or only Claude's chat-visible session log? |
| Human gate support | First-class step type | DIY in JS — needs experimentation | Defer to a later probe |
| Authoring difficulty | Two artifacts (JSON + skill) | One artifact (JS file) | Subjective |
| Debuggability | Read JSONL trace | TBD — does the harness emit a workflow trace? | |

The big question: **does the orchestrator JS variable (`gen.titles` etc.) constitute context poisoning?** Our blackboard pattern keeps step payloads out of the orchestrator entirely. The Workflow Tool stores them in JS variables in the main session. If the main session is then prompted later, it sees those variables in scope. **Whether that "leaks" depends on what the harness considers context.** This is the critical empirical question.

---

## Reference reading (in order)

1. **`~/dev/ad/brains/anthropic-claude/claude-code/workflow-tool.md`** — start here. 175 lines, reverse-engineered API reference. Read in full.
2. **`~/dev/upstream/repos/bun/.context/CONTEXT.md`** — 104-line deep comprehension doc for the Bun corpus. Mental model + failure modes.
3. **`~/dev/upstream/repos/bun/.claude/workflows/lifetime-classify.workflow.js`** — one real production workflow. Read to see the idioms.
4. **`~/dev/ad/brains/anthropic-claude/claude-code/blackboard-workflow-pattern.md`** — what we built, the substrate the new tool would replace/complement.
5. **`~/dev/ad/brains/ylo/workflow-candidates.md`** — the 6 YLO sub-workflows we've been planning; test #2 (title gen + refinement) is the chosen comparison point.
6. **`~/dev/ad/apps/dark-factory/.claude/skills/conductor/SKILL.md`** — the existing conductor implementation for direct comparison.

---

## Provenance — what's verified vs. assumed

| Claim | Source | Status |
|-------|--------|--------|
| `.claude/workflows/` is the path | workflow-tool.md + bun corpus | ✅ verified (two sources agree) |
| Filename pattern `*.workflow.js` | both sources | ✅ verified |
| `CLAUDE_CODE_WORKFLOWS=1` env var enables it | workflow-tool.md | ✅ stated; not empirically tested on this machine |
| Need Claude Code ≥ 2.1.147 | workflow-tool.md | ✅ stated; not verified — current `/Users/davidcruwys/.local/share/claude/versions/` may have older version |
| 6 ambient globals + `args`/`return` | both sources | ✅ verified across multiple workflow files |
| Subagent runs in fresh context | workflow-tool.md | ✅ stated; will be empirically verified by step 4 isolation test |
| **Invocation mechanic (slash command? tool? both?)** | NOT in either source | ❌ unknown — discover empirically in step 1 |
| Whether the workflow body's JS variables are visible in the parent Claude Code session's context | not stated | ❌ unknown — critical for isolation question |
| Whether multiple workflow files can share helpers | not stated; no `import` in 53 files suggests NO | ⚠️ likely-no, but unconfirmed |

---

## What NOT to do in this experiment

- Don't delete the existing `.claude/skills/{conductor,store,image-gen}/` — they keep working
- Don't write to `experiments/ylo/blackboard/runs/b65/` — make a new sibling directory
- Don't write to `~/dev/ad/brains/` from this session unless you specifically need to (it's a separate repo with its own discipline)
- Don't attempt human-gated workflows under the new tool yet — that's a later probe once the substrate is proven
- Don't migrate the bash+jq conductor unless this experiment provides strong evidence it should be retired

---

## Decision after the experiment

The comparison report should make one of these recommendations:

1. **Adopt and migrate** — Workflow Tool is strictly better; port the 4 existing probes to `*.workflow.js`; retire the bash+jq conductor; keep EAV store via `remember`/`recall` helpers.
2. **Hybrid** — Workflow Tool for fan-out + schema-validated work; existing blackboard pattern for HITL + complex state.
3. **Stay bespoke** — too experimental / undocumented / lacks key feature; revisit when official docs land.

Whichever recommendation: write it as a follow-on backlog item that updates `~/dev/ad/brains/ylo/recommendations.md`.

---

## Open questions to log if encountered

If the new session hits unknowns or surprises during the experiment, log them at the bottom of the comparison.md report so the next iteration knows. Likely candidates:

- How is a workflow actually invoked? (slash command? agent tool? both?)
- Can the same workflow file be invoked concurrently for different videos? (For the 70-video batch)
- Does the harness emit telemetry / a trace log showing which `agent()` calls fired and what they returned?
- Does `isolation: "worktree"` actually create a git worktree on disk, and where?
- Are there rate limits / concurrency caps on `pipeline()` and `parallel()`?
- What happens to args if the workflow file has a syntax error?
- Is there a way to define a helper library shared across workflow files? (If not — should there be?)

---

**End of handover.** Once this experiment is complete, write the comparison report at `~/dev/ad/apps/dark-factory/experiments/ylo/blackboard/runs/b65-workflow-tool/comparison.md` and create a follow-on backlog item with the recommendation.

---

## Status — 2026-05-23 (Developer)

**Partial — blocked at Step 1b, artifacts staged.**

What was done:
- Verified `claude --version` = 2.1.149 (≥ 2.1.147 ✓), `CLAUDE_CODE_WORKFLOWS=1` set in session env, gate logic in binary confirms `env var + tengu_workflows_enabled flag → enabled`.
- Wrote `.claude/workflows/hello.workflow.js` (smoke test) and `.claude/workflows/title-gen.workflow.js` (the real probe, 144 lines, with inline `remember`/`recall`/`loadFile` helpers; format wire-compatible with existing `store.jsonl`).
- Staged `experiments/ylo/blackboard/runs/b65-workflow-tool/` with transcript, critique fixture, empty store.
- Wrote `experiments/ylo/blackboard/runs/b65-workflow-tool/comparison.md` with empirical findings and unfilled comparison cells.

Blocker:
- The `Workflow` tool **did not surface** in this session's tool list (verified via `ToolSearch select:Workflow` and full deferred-tool scan). Binary string inspection shows the invocation shape is `Workflow({name, args})`. Hypothesis: lazy registration — workflow files must exist at session boot. Empirically untested mid-session.

Hand-off: see `backlog/2026-05-24-workflow-tool-followup.md` — restart Claude Code (with workflow files now present), run hello → title-gen, do the isolation test, complete the comparison table, choose a recommendation.
