# Handover — Run the Workflow Tool spikes

**Previous session**: `df-2-workflow-factory-convergence`
**Last commit**: `7ff7d6a` ("Add MCP Blackboard pattern + spike artifacts")
**You are here to**: execute Spikes 1 and 2 and record the results.

---

## Pre-flight (do this first, before anything else)

1. **Exit any running Claude Code session entirely** (`/exit`). The env-var fix only takes effect on a fresh launch.

2. **Relaunch Claude in this project**:
   ```bash
   cd /Users/davidcruwys/dev/ad/apps/dark-factory
   claude
   ```

3. **Verify the Workflow tool is enabled** — paste this prompt:
   ```
   Run: env | grep CLAUDE_CODE_WORKFLOWS
   Then confirm the Workflow tool is in your available tools.
   ```
   - Should print `CLAUDE_CODE_WORKFLOWS=1`
   - Claude should confirm Workflow is available
   - If not: `.claude/settings.local.json` may not have been read. Check it has `"env": { "CLAUDE_CODE_WORKFLOWS": "1" }` at top level.

4. **Verify the blackboard MCP server is connected** — paste:
   ```
   Run /mcp and report which servers are connected.
   ```
   - Should show `blackboard` with status `connected`
   - If not: check `server.mjs` is executable, check the path in `settings.local.json` is correct.

---

## Spike sequence (run in this order)

### Spike 1a — Programmatic invocation (sanity check)

**Paste this prompt:**
```
Use the Workflow tool to run the "hello" workflow with args { name: "Spike1a" }.
Report what it returned.
```

**Expected**: returns `{ greeting: "Hello, Spike1a!" }` or similar one-sentence greeting.
**If it fails**: stop. Workflow tool isn't fully working yet. Debug before continuing.

### Spike 1b — Slash command (R13)

**Type directly in the TUI** (this is a slash command, not a Claude prompt):
```
/hello {"name":"Spike1b"}
```

Watch `/workflows` for the run.

**Expected**: a workflow run completes. The greeting should mention "Spike1b" (if args parsed) or "world" (if args came through as raw string and our parse guard fell back).
**Record**: which name appears in the greeting — this tells us how slash args land.

### Spike 2 — MCP Blackboard (the big one — R11 + R12)

**Paste this prompt:**
```
Use the Workflow tool to run the "hello-blackboard" workflow with args { runId: "spike2-first" }.
Report what it returned in full — I need to see the `ok`, `bbKey`, `producerSaid`, `consumerSaw`,
and `notes` fields.

Also after it completes, run: cat ~/.claude/blackboard/store.json
so I can verify the data persisted.
```

**Expected**: returns `{ ok: true, ... notes: "R11 + R12 verified..." }`. The store should contain the key `hello-blackboard.spike2-first.titles` with 3 titles in its value.

**Possible failures and what they mean** (full table is in `spikes/blackboard-mcp/README.md`):
- Producer says "I don't have access to mcp__blackboard__bb_set" → **R12 = no** (workflow subagents can't call MCP tools — major architectural finding)
- MCP call returns connection error → server isn't running, check `/mcp`
- Round-trip succeeds but `consumerSaw.count !== 3` → workflow works but data integrity issue

### Spike 1c — Agent-invoked workflow (R14)

**Paste this prompt:**
```
Have a sub-agent (use the Agent tool) invoke the "hello" workflow with args { name: "Spike1c" }
and return what the workflow returned. I want to verify that an agent can call Workflow as a tool.
```

**Expected**: an agent launches, calls Workflow, returns the greeting.
**If the agent says "Workflow tool not available"**: spawned agents don't inherit the Workflow tool. This is important — it gates the Penny/Alex/Oscar persona architecture.

---

## After the spikes — record results

Open `spikes/blackboard-mcp/README.md` and fill in the Status section at the bottom:
- Mark each checkbox with ✅ / ❌ / ⚠️
- Write a one-line note per item explaining what happened
- For Spike 2, especially: capture the R11 and R12 verdicts clearly

Then commit:
```bash
git add spikes/blackboard-mcp/README.md
git commit -m "Spike results — R11/R12/R13/R14 outcomes"
```

---

## What to bring back to the next strategy session

When you come back to the architecture conversation:

1. **R12 verdict** is the headline. If yes, the MCP Blackboard section of `docs/architecture.md` is a real upgrade path. If no, we need to rethink that section — the v2 architecture as written is dead and we need to plan around it (HTTP via curl from a Bash agent is a fallback, but ugly).

2. **R13 verdict** affects how Penny invokes workflows for the user. If slash commands pass args cleanly as JSON, Penny can offer one-liners. If not, args have to be programmatic and Penny becomes the wrapper.

3. **R14 verdict** gates the entire Penny/Alex/Oscar persona architecture. If agents can't invoke workflows, the personas can only *recommend* workflows for you to run — they can't actually run them.

4. **Performance feel** — was Spike 2 noticeably faster than `remember()`-based workflows? Was the MCP latency invisible? Worth noting subjectively even before we measure properly.

5. **Anything surprising** — gotchas, weird error messages, behavior that contradicts the docs. Add to `docs/workflow-tool-authoring-notes.md` Part 4 with a `[tested]` tag.

---

## Quick reference — file map

```
spikes/blackboard-mcp/
├── server.mjs                          ← the MCP server (already smoke-tested standalone)
├── README.md                           ← full setup + test details
├── HANDOVER.md                         ← this file
└── package.json

.claude/workflows/
├── hello.workflow.js                   ← used for Spike 1
└── hello-blackboard.workflow.js        ← used for Spike 2

.claude/settings.local.json (gitignored, already updated):
  env.CLAUDE_CODE_WORKFLOWS=1
  mcpServers.blackboard → server.mjs
  permissions for Workflow(hello), Workflow(hello-blackboard), 4 mcp__blackboard__* tools
```

---

## If something is fundamentally wrong

If Workflow tool still won't enable after the env var fix:
- Check `claude --version` — we know the gate was removed around 2026-05-23
- Check if anything in `~/.claude/settings.json` overrides the project-local env
- Check the user-global `~/.claude/.claude.json` for env settings

If the MCP server connects but agents can't see its tools:
- Check `/permissions` — tools may need explicit allow even if registered
- Try `claude --debug` to see MCP-related log lines on startup

If everything works, the next thing to think about is **Phase B** — building `prepare-ingestion-brief.workflow.js` and `ingest.workflow.js`. See `docs/architecture.md` §12 for the roadmap.
