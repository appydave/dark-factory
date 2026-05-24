# Blackboard MCP — Spike Setup and Test Procedure

A minimal MCP server that exposes a file-backed key-value blackboard, plus the workflow that exercises it. Together they verify the MCP Blackboard pattern described in `docs/architecture.md` § 5.5.

---

## What this spike answers

| Research question | What success looks like |
|-------------------|------------------------|
| **R11** — Does the MCP Blackboard pattern eliminate dedicated I/O agents in practice? | `hello-blackboard.workflow.js` completes; consumer reads back exactly what producer wrote |
| **R12** — Can workflow subagents call MCP tools at all? | The producer's `mcp__blackboard__bb_set` call succeeds |
| **R13** — Slash-command args (`/hello-blackboard {...}`) — do they land in `args`? | Slash invocation works (manual test) |
| **R14** — Agent-invoked `Workflow({name, args})` — can it fire from an agent's tool call? | Manual test (see below) |

---

## Files in this spike

```
spikes/blackboard-mcp/
├── server.mjs        — the MCP server (Node, stdio JSON-RPC, ~180 lines)
├── package.json      — empty manifest for clarity
└── README.md         — this file

.claude/workflows/
├── hello.workflow.js              — minimal workflow (Spike 1)
└── hello-blackboard.workflow.js   — blackboard workflow (Spike 2)
```

Storage: by default the MCP server writes to `~/.claude/blackboard/store.json`. Override with `BLACKBOARD_STORE_PATH=/some/path/store.json`.

---

## Setup — one-time

### 1. Confirm the Workflow tool is enabled

Workflows are gated behind an environment variable. In your shell:

```bash
echo "${CLAUDE_CODE_WORKFLOWS:-not set}"
```

If it prints `not set`, enable it persistently for this project by adding to `.claude/settings.local.json` (gitignored — machine-local, no risk of leaking to the repo):

```jsonc
{
  "env": { "CLAUDE_CODE_WORKFLOWS": "1" }
}
```

Restart Claude Code. You should now see `Workflow` available as a tool, and `/workflows` as a command.

> **⚠️ Known problem: Workflow tool "exists but is not enabled in this context"**
>
> If you've previously had the Workflow tool working and it stops mid-session, this is almost certainly an environment-inheritance issue, not a bug in the workflow itself. Diagnosis:
>
> 1. You set `CLAUDE_CODE_WORKFLOWS=1` in a terminal and launched Claude → workflows worked
> 2. You moved Claude to background / agent view / a different surface that did *not* inherit that env var
> 3. New agent invocations in the background context don't see the env var → Workflow tool is gated off for them
> 4. You return to the running Claude session and try to use Workflow → error "exists but is not enabled in this context"
>
> The shell `echo $CLAUDE_CODE_WORKFLOWS` is empty in such sessions even though you "definitely set it" — because the new context didn't inherit it.
>
> **Permanent fix**: put the env var in `.claude/settings.local.json` as shown above. Claude Code reads this file at session start regardless of how the session was launched. After adding, fully exit Claude (`/exit`) and relaunch — `env` changes don't apply to a running session.
>
> **Quick check**: run `env | grep CLAUDE_CODE_WORKFLOWS` from inside Claude (via the Bash tool). If it's empty, no workflows. If it's `1`, workflows should work.

### 2. Register the blackboard MCP server

Add to `.claude/settings.local.json` under `mcpServers`:

```jsonc
{
  "mcpServers": {
    "blackboard": {
      "command": "node",
      "args": ["/Users/davidcruwys/dev/ad/apps/dark-factory/spikes/blackboard-mcp/server.mjs"]
    }
  }
}
```

Restart Claude Code (MCP servers connect at session start). Verify it's connected by typing `/mcp` in the TUI — you should see `blackboard` in the list with status `connected`.

The four tools will be exposed as:
- `mcp__blackboard__bb_set`
- `mcp__blackboard__bb_get`
- `mcp__blackboard__bb_list`
- `mcp__blackboard__bb_delete`

### 3. Pre-approve the MCP tools (optional, avoids prompts)

Add to `.claude/settings.local.json` permissions allow-list:

```jsonc
{
  "permissions": {
    "allow": [
      "mcp__blackboard__bb_set",
      "mcp__blackboard__bb_get",
      "mcp__blackboard__bb_list",
      "mcp__blackboard__bb_delete"
    ]
  }
}
```

---

## Smoke-test the MCP server directly (no Claude needed)

Confirms the server works before involving Claude:

```bash
(printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
  '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"bb_set","arguments":{"key":"hello","value":{"msg":"world"}}}}' \
  '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"bb_get","arguments":{"key":"hello"}}}' ; \
  sleep 0.3) \
| BLACKBOARD_STORE_PATH=/tmp/bb-smoke.json node spikes/blackboard-mcp/server.mjs
```

Should print four JSON-RPC responses, the last one returning `{"key":"hello","value":{"msg":"world"},"found":true}`. This has already been verified to work.

---

## Spike 1 — args invocation paths (hello workflow)

`hello.workflow.js` is the minimum-viable workflow. Use it to verify all three args invocation paths.

### 1a — Programmatic (already verified)

In a Claude session with workflows enabled:

```
> use the Workflow tool: Workflow({ name: "hello", args: { name: "Dark Factory" } })
```

**Expected**: returns `{ greeting: "Hello, Dark Factory!" }` (or similar one-sentence).
**Verifies**: programmatic invocation with object args.

### 1b — Slash command

In the Claude TUI, type:

```
/hello {"name": "Dark Factory"}
```

**Expected**: the workflow runs, returns a greeting. Watch `/workflows` for the run.
**Verifies (R13)**: the JSON string after the command name parses cleanly into `args`.
**Possible gotcha**: if slash commands pass `args` as a bare string (not JSON-parsed), our guarded `JSON.parse` falls back to `{}` — the workflow runs with default `name="world"`. Either outcome is informative.

### 1c — Agent-invoked

In a Claude session, ask:

```
> Have an agent invoke the hello workflow with args { name: "Penny test" }
> and tell me what it returns.
```

**Expected**: an agent launches, calls the Workflow tool with those args, returns the result.
**Verifies (R14)**: agents can invoke workflows as tool calls. This gates the Penny/Alex/Oscar persona architecture.
**Possible gotcha**: the spawned agent might not have Workflow in its allowed tools — check `agentType` defaults.

Record results in the Status section at the bottom of this README.

---

## Spike 2 — MCP Blackboard (hello-blackboard workflow)

Once setup is complete and the MCP server is registered:

```
> use the Workflow tool: Workflow({ name: "hello-blackboard", args: { runId: "smoke-1" } })
```

### Expected execution

1. **Produce phase**: agent generates 3 titles, calls `mcp__blackboard__bb_set` with key `hello-blackboard.smoke-1.titles`, returns `{ bbKey, wrote: true }`.
2. **Consume phase**: a *fresh* agent (no context from producer) calls `mcp__blackboard__bb_get` with the same key, returns the 3 titles.
3. **Verify phase**: workflow returns `{ ok: true, ... }` with `notes: "R11 + R12 verified..."`.

### Confirm out-of-band

```bash
cat ~/.claude/blackboard/store.json
```

Should contain the key `hello-blackboard.smoke-1.titles` with the 3 titles.

### What success means

If the spike passes:
- **R12 is verified**: workflow subagents CAN call MCP tools (the bigger architectural question)
- **R11 is verified for the simple case**: a workflow can use the blackboard pattern instead of `remember()`
- **Architecture § 5.5** is no longer aspirational — it's a working pattern we can extend

### What failure means

Most likely failure modes and what they tell us:

| Failure | What it means | Next step |
|---------|---------------|-----------|
| Producer agent says "I don't have access to mcp__blackboard__bb_set" | Workflow subagents don't inherit MCP tools (R12 = no) | Major: blocks the v2 architecture as designed. Either work around (HTTP via curl from a Bash agent) or wait for Anthropic to fix |
| Producer agent has the tool but call returns an error | MCP server connection issue | Check `/mcp`, restart Claude, check server.mjs runs standalone |
| Consumer reads back wrong/empty data | Race condition or schema mismatch | Inspect `~/.claude/blackboard/store.json` between phases |
| Workflow itself errors before agents run | Workflow tool config issue | Re-verify `CLAUDE_CODE_WORKFLOWS=1`, check `/workflows` |

---

## Status

(Update this section after running the spikes.)

### Spike 1 results
- [ ] 1a — Programmatic invocation: ___
- [ ] 1b — Slash command: ___
- [ ] 1c — Agent-invoked: ___

### Spike 2 results
- [ ] MCP server connects: ___
- [ ] Producer can call mcp__blackboard__bb_set: ___
- [ ] Consumer can call mcp__blackboard__bb_get: ___
- [ ] Round-trip data integrity: ___
- [ ] R11 verdict: ___
- [ ] R12 verdict: ___

### Findings to fold back
- (Things to add to `docs/workflow-tool-authoring-notes.md` Part 4 once verified)
- (New gotchas discovered)
- (Whether the MCP overhead is genuinely lower than `remember()` overhead — measure both)
