/**
 * hello-blackboard — Spike 2: verify the MCP Blackboard pattern works.
 *
 * Demonstrates:
 *   1. Agent A writes data to the blackboard via mcp__blackboard__bb_set
 *   2. Agent B reads the same data via mcp__blackboard__bb_get
 *   3. The VM only holds the blackboard ID — the payload never crosses the VM
 *
 * Verifies research questions:
 *   R11 — Does the MCP Blackboard pattern eliminate dedicated I/O agents in practice?
 *   R12 — Can workflow subagents call MCP tools at all?
 *
 * Pre-reqs:
 *   - blackboard-mcp server registered in Claude settings (see spikes/blackboard-mcp/README.md)
 *   - The MCP tool names will be prefixed: mcp__blackboard__bb_set, etc.
 *
 * Invocation:
 *   Workflow({ name: 'hello-blackboard', args: { runId: '<unique>' } })
 *   Default runId is "spike-default" — pass a unique one for clean test runs.
 */

export const meta = {
  name: "hello-blackboard",
  description: "Spike — verify MCP Blackboard pattern: Agent A writes, Agent B reads, VM passes only the ID.",
  phases: [
    { title: "Produce", detail: "Agent A generates data and writes to blackboard via MCP" },
    { title: "Consume", detail: "Agent B reads same data from blackboard via MCP" },
    { title: "Verify",  detail: "Compare what was written vs what was read" }
  ]
};

const A = typeof args === "string"
  ? (() => { try { return JSON.parse(args) } catch { return {} } })()
  : (args ?? {});

const RUN_ID  = A.runId  ?? "spike-default";
const BB_KEY  = `hello-blackboard.${RUN_ID}.titles`;

// ─── Phase 1 — Producer agent ────────────────────────────────────────────────
//
// Agent A generates 3 titles AND writes them to the blackboard.
// Returns only the blackboard key — the titles themselves never cross the VM.

phase("Produce");

const produceResult = await agent(
  `You have access to a blackboard MCP server. Available tools include:
   - mcp__blackboard__bb_set({ key, value })
   - mcp__blackboard__bb_get({ key })

   Steps:
   1. Generate exactly 3 YouTube-style title ideas about "context engineering for non-developers".
      Each title is 40-60 characters, action-oriented.
   2. Call mcp__blackboard__bb_set with:
        key: "${BB_KEY}"
        value: { titles: [<your 3 titles as strings>], generatedBy: "produce-agent" }
   3. Confirm the write succeeded.
   4. Return ONLY this object — do NOT include the titles themselves:
        { bbKey: "${BB_KEY}", wrote: true }

   The point of this test is that the workflow VM should never see the title text —
   it only sees the blackboard key. So do NOT echo the titles in your return value.`,
  {
    label: "produce-agent",
    phase: "Produce",
    schema: {
      type: "object",
      required: ["bbKey", "wrote"],
      properties: {
        bbKey: { type: "string" },
        wrote: { type: "boolean" }
      }
    }
  }
);

if (!produceResult?.wrote) {
  return { ok: false, error: "producer did not confirm write", produceResult };
}

log(`Producer wrote to blackboard key: ${produceResult.bbKey}`);

// ─── Phase 2 — Consumer agent ────────────────────────────────────────────────
//
// Agent B reads the data from the blackboard using only the key passed via prompt.
// The VM never held the payload.

phase("Consume");

const consumeResult = await agent(
  `You have access to a blackboard MCP server. Available tool:
   - mcp__blackboard__bb_get({ key })

   Steps:
   1. Call mcp__blackboard__bb_get with key: "${produceResult.bbKey}"
   2. Inspect the returned value — it should have shape { titles: [...], generatedBy: "..." }
   3. Return:
        { bbKey: "${produceResult.bbKey}",
          titlesReadBack: <the array of titles you read from the blackboard>,
          count: <number of titles read>,
          generatedBy: <the generatedBy string from the value> }`,
  {
    label: "consume-agent",
    phase: "Consume",
    schema: {
      type: "object",
      required: ["bbKey", "titlesReadBack", "count", "generatedBy"],
      properties: {
        bbKey:          { type: "string" },
        titlesReadBack: { type: "array",   items: { type: "string" } },
        count:          { type: "integer" },
        generatedBy:    { type: "string" }
      }
    }
  }
);

// ─── Phase 3 — Verify ────────────────────────────────────────────────────────

phase("Verify");

const ok = consumeResult?.count === 3
        && consumeResult?.generatedBy === "produce-agent"
        && consumeResult?.bbKey === produceResult.bbKey;

if (ok) {
  log(`SPIKE PASSED — blackboard round-trip worked. Read back ${consumeResult.count} titles.`);
} else {
  log(`SPIKE FAILED — readback did not match producer's claim.`);
}

return {
  ok,
  bbKey: produceResult.bbKey,
  producerSaid: { wrote: produceResult.wrote },
  consumerSaw:  consumeResult,
  notes: ok
    ? "R11 + R12 verified: MCP blackboard pattern works; workflow subagents can call MCP tools."
    : "Spike failed. Inspect agent transcripts under .claude/projects/*/subagents/workflows/ for details."
};
