# Workflow Tool — Authoring Notes

**Status**: living document — updated after each experiment session  
**Last updated**: 2026-05-25 (session 2 — probes #1–#4 complete)  
**Related**: `docs/ingestion-workflow.md`, `experiments/ylo/workflow-tool/runs/b65/comparison.md`

---

## How to use this doc

The 9 issues below split into two categories:

- **Checklist issues** — obvious once known; a creation-time check or QA pass catches them. These should eventually live in a `workflow-creator` skill or pre-run lint script.
- **Systemic issues** — architectural constraints of the Workflow Tool VM that require design patterns or further research. Don't try to work around them ad hoc; use the documented pattern.

---

## Part 1 — Authoring checklist (obvious, preventable)

Run this checklist before invoking a workflow for the first time.

### ✅ C1 — `parallel()` requires thunks, not promises

**The bug:**
```js
// WRONG — agent() is called immediately, parallel() gets promises
await parallel([ agent("do A"), agent("do B") ])

// CORRECT — thunks; parallel() calls them when a slot is free
await parallel([ () => agent("do A"), () => agent("do B") ])
```
Same applies to `.map()`:
```js
// WRONG
items.map(x => agent(`process ${x}`))

// CORRECT
items.map(x => () => agent(`process ${x}`))
```
This is the most common mistake. Every script in session 2 had it wrong. The error message is clear (`parallel() expects an array of functions, not promises`) but only appears at runtime.

**QA check**: grep the script for `parallel([` and verify every item inside starts with `() =>`.

---

### ✅ C2 — Phase labels must exactly match `meta.phases` titles

**The bug:**
```js
export const meta = {
  phases: [{ title: "Explore" }, { title: "Finals" }]
}
// ...
async function generateImage(...) {
  return agent("...", { phase: "image-gen" })  // ← not in meta.phases
}
```
Result: the agent runs and produces output, but the `/workflows` view shows "not started" for that phase forever. Files appear on disk with no visual progress — looks like a hang.

**Fix**: always pass phase as a parameter to helper functions. Never hardcode a phase string inside a helper that's called from multiple phases.

```js
async function generateImage(prompt, path, label, model, phase = "Explore") {
  return agent("...", { phase })
}
// call sites:
() => generateImage(..., "Explore")
() => generateImage(..., "Finals")
```

**QA check**: grep for `phase:` strings in the script; each must appear verbatim in `meta.phases`.

---

### ✅ C3 — `Date.now()` and `new Date()` are banned in workflow scripts

The Workflow VM throws if you call these — they would break resume caching (a resumed agent call with a different timestamp wouldn't match the journal). 

**Pattern**: always pass `ts` via args:
```js
const A = typeof args === "string" ? JSON.parse(args) : args || {};
const RUN_TS = A.ts || "2026-01-01T00:00:00.000Z";
```
The caller supplies `ts` at invocation time. Stamp results after the workflow returns if you need wall-clock precision.

---

### ✅ C4 — Resume always requires re-passing args

`resumeFromRunId` restores the journal (cached agent results) but does NOT restore `args`. The script sees `args = undefined` and typically returns `{ error: "args required" }` immediately.

**Pattern**: always include `args` in every `Workflow({scriptPath, resumeFromRunId, args: {...}})` call.

---

### ✅ C5 — The Workflow tool snapshots scripts at launch

When you invoke a workflow by `name`, the tool reads `.claude/workflows/foo.workflow.js` and writes a copy to the session's `workflows/scripts/` dir. That copy is what actually runs. Edits to the source file after launch have no effect on the running instance.

**To fix a failing run**: edit the generated copy (path shown in the Workflow tool result) and re-invoke with `scriptPath` + `resumeFromRunId`.

**To fix the source for future runs**: edit `.claude/workflows/foo.workflow.js` — new invocations by name will pick it up.

---

## Part 2 — Systemic issues (architectural, need design patterns)

---

### 🔬 S1 — No filesystem access in the VM: the state-sharing problem

**What's happening:**  
The Workflow JS VM is a sandboxed `vm.createContext` environment. It has only the workflow primitives (`agent`, `parallel`, `pipeline`, `phase`, `log`, `args`, `budget`). No `fs`, no `fetch`, no Node APIs. Every file read or write must go through `agent()`.

This means every `remember()` call (append one line to a JSONL file) costs one full agent round-trip: ~15–30s, plus token overhead. For `title-gen` with 5 store writes, that's the majority of wall-clock time.

**Is this actually no shared state?**  
No — state IS shared, just expensively. The JSONL store is the shared state. Any agent can read or write it. The VM just can't touch it directly; it delegates to agents who can. The problem is latency, not capability.

**Solutions — ranked by practicality:**

| Approach | Cost | Latency | Notes |
|----------|------|---------|-------|
| **Batch writes** — collect all records, write once at end | Low | Low | Loses crash-recovery granularity. Fine for fan-out workflows where each item is independent |
| **Haiku for I/O agents** — use `model: "haiku"` on all `remember()`/`recall()` calls | Low | Medium | Haiku is ~5–10× faster than Sonnet for simple append tasks. Cuts store overhead ~80% |
| **End-of-workflow return** — return all results from the workflow, let caller persist | Low | Low | No agent cost at all. Works when the caller is another workflow or the main loop |
| **HTTP sidecar** — spin up a tiny local server before the workflow, have agents `curl` it | Medium | Low | Requires a pre-step agent to start the server. Stateful between agents. More complex |
| **MCP tool** — a `store_write` / `store_read` MCP tool available to agents | Medium | Low | Would require an MCP server with file I/O. Agents call it natively. Worth exploring for future sessions |

**Immediate recommendation**: use `model: "haiku"` for all `remember()`/`recall()` agents. It costs almost nothing and cuts store overhead significantly. No architectural change required.

**Research question**: Can the workflow VM call MCP tools directly (not via agent)? If yes, a lightweight `store` MCP would eliminate the overhead entirely. If no, the haiku pattern is the pragmatic answer.

---

### 🔬 S2 — Agent API calls don't fail fast

**What happened:**  
The `generateImage` agents were told to POST to a wrong endpoint (`/api/generate`, which returns 404), then poll until `status === "completed"`. With a 404 on the initial POST, there's no `taskId` to poll — but the agents didn't return `{ ok: false }`. They hung for 20+ minutes.

**Is this our fault or a Workflow Tool limitation?**  
Mostly our fault. The prompt said "poll until completed" but didn't say "return `{ ok: false }` immediately on any non-2xx response from step 2". The agent followed the happy-path instructions and didn't know when to bail.

**Pattern — defensive API agent prompts:**
```
Steps:
1. POST to https://api.example.com/endpoint ...
   - If response is not HTTP 2xx, immediately return { ok: false, error: "createTask failed: <status> <body>" }
2. Extract taskId. If missing, return { ok: false, error: "no taskId in response: <full response>" }  
3. Poll GET .../status/<taskId> every 10s. Stop after 20 polls (200s max).
   - If any poll returns non-2xx, return { ok: false, error: "poll failed: <status>" }
   - If 20 polls complete without "completed", return { ok: false, error: "timeout after 200s" }
4. Extract image URL. Download to <path>. Return { ok: true, taskId, path, bytes }.
If any step throws or produces unexpected output, return { ok: false, error: "<reason>" }.
```

The key additions: explicit non-2xx bail, explicit no-taskId bail, explicit poll cap.

**QA check**: any agent prompt that calls an external API must have: (a) non-2xx early return, (b) missing-field early return, (c) explicit max-retry / timeout instruction.

---

### 🔬 S3 — API keys don't flow into workflow subagents

**What happened:**  
`$KIE_API_KEY` was in the shell env but workflow subagents couldn't see it. The agents silently got an empty string and every API call was unauthorized — but they didn't fail fast (see S2), so it looked like a hang.

**Why this happens:**  
Workflow subagents run in a separate process context. Shell env vars from the parent terminal are not guaranteed to flow through. This is the same issue that bites people with `dotenv` in Node — the env is per-process.

**What we know works:**
- Reading directly from a `.env` file inside the agent prompt: `grep KIE_API_KEY /path/to/.env | cut -d= -f2`
- Storing the key in the project `.env` at repo root

**What might work (needs verification):**
- Adding keys to `.claude/settings.json` under an `env` section — Claude Code may forward these to subagent processes
- `direnv` auto-loading a `.env` at session start

**Canonical pattern for this project:**
1. Key lives in `flivideo/fligen/server/.env` (canonical source — where it was first set up)
2. Mirrored to `dark-factory/.env` (project-local copy)
3. Agent prompts use: `` `grep KIE_API_KEY /Users/davidcruwys/dev/ad/apps/dark-factory/.env | cut -d= -f2` ``

**Research question**: Does `env` in `.claude/settings.json` or `.claude/settings.local.json` flow into workflow subagent processes? If yes, document it as the cleaner pattern and deprecate the grep approach.

**Creation checklist item**: any workflow that calls an external API must document where its key comes from and use the explicit-read pattern in the agent prompt. Never rely on `$VAR` shell expansion inside an agent instruction.

---

### 🔬 S4 — Recall agents can return double-nested values

**What happened:**  
The store record has structure `{ key, value, meta }`. When we asked a recall agent to "find the record where `key === 'selectedTitles'` and return `{ value: <the value field> }`", it sometimes returned `{ value: { value: [...] } }` — treating the whole record as the value rather than extracting `record.value`.

**Why it happens:**  
The agent reads the JSONL, finds the matching line, and has to decide what "the value field" means. If the stored value is itself a complex object (like `{ value: [...] }`), the agent can get confused about nesting depth. The schema `{ value: {} }` (empty schema for the value property) gives no guidance — it accepts anything.

**Solution — always use an unwrap helper:**
```js
function unwrap(v) {
  if (Array.isArray(v)) return v;
  if (v && Array.isArray(v.value)) return v.value;  // double-nested
  if (typeof v === "string") { try { return unwrap(JSON.parse(v)); } catch(_) {} }
  return v;
}
```
And for recall agents, be explicit in the prompt:
```
Read the JSONL at <path>. Find the LAST line where the parsed JSON has `key === "selectedTitles"`.
Extract the `value` property of that record.
Return { value: <exactly that property — not the whole record, not re-wrapped> }.
```

**Deeper fix**: use a stricter schema for the recall that constrains the type of `value`. If you know `selectedTitles` is an array of `{ emotion, chars, title }` objects, say so in the schema. The agent will retry until it returns the right shape.

**Research question**: Is double-nesting consistent? Does it happen when the stored value is a primitive vs. object vs. array differently? A targeted test (store string / number / array / object, recall each) would characterise the pattern and let us write a single canonical `recall()` helper that handles all cases.

---

## Part 3 — Ideas for automation

### Workflow creator checklist (pre-run QA)

A future `workflow-creator` skill or `/lint-workflow` command could automate these checks before first run:

- [ ] All `parallel([...])` items start with `() =>`
- [ ] All `phase:` strings in `agent()` calls appear verbatim in `meta.phases`
- [ ] No `Date.now()` or `new Date()` calls
- [ ] All external API agent prompts have non-2xx early-return instructions and explicit poll caps
- [ ] All external API agent prompts use file-based key read, not `$VAR` expansion
- [ ] `meta.phases` has at least one entry
- [ ] `meta.name` matches the filename (e.g. `title-gen.workflow.js` → `name: "title-gen"`)
- [ ] `args` validated at top of script with clear error message

### Recall helper — canonical pattern

Every workflow that reads from a JSONL store should use a single `recall()` implementation:

```js
async function recall(key, schema = null) {
  const r = await agent(
    `Read the JSONL at ${A.storePath}. ` +
    `Find the LAST line where the parsed JSON object has key === "${key}". ` +
    `Extract the value property of THAT LINE ONLY — not the whole record, not any outer wrapper. ` +
    `Return { value: <the extracted value> } or { value: null } if not found.`,
    {
      label: `recall:${key}`,
      model: "haiku",
      schema: { type: "object", required: ["value"], properties: { value: schema ?? {} } }
    }
  );
  const raw = r?.value ?? null;
  // unwrap double-nesting defensively
  if (raw && typeof raw === "object" && !Array.isArray(raw) && "value" in raw) return raw.value;
  return raw;
}
```

Key additions vs. naive version: `model: "haiku"` (cheap/fast for I/O), explicit "THAT LINE ONLY" instruction, defensive unwrap on return.

---

## Part 4 — Primitives we didn't know about

Discovered from Ray Amjad's introduction video and the workflow-creator skill (now at `/Users/davidcruwys/dev/upstream/repos/claude-code-workflow-creator/`). These are first-class workflow primitives.

### Verification status legend

Used throughout the rest of this document. Trust accordingly.

- **[tested]** — we ran it in a workflow this project and observed the behaviour
- **[docs-only]** — described in the workflow-creator api-reference.md or patterns.md but not yet verified by us
- **[inferred]** — extrapolated from related behaviour or third-party sources (the video). Lowest trust.

When you write code based on a primitive, check the tag. `[inferred]` items deserve a 5-min spike before being depended on.

### P1 — `budget` (token-aware loop control) **[docs-only]**

The workflow VM exposes a `budget` object with `budget.remaining()`. Use it to make loops self-terminating when token usage hits a cap.

```js
while (budget.remaining() > 50_000) {
  await agent('find one more bug')
}
```

The run scales itself to the budget you gave it — no fixed agent count, no manual stop condition. Perfect for:
- **Shadow Runs** — keep running benchmark variants until budget exhausted
- **Upstream Pulse** — scan provider repos until daily budget hit
- **Dry-streak loops** — combined with a counter (see Part 5: P2-loop-until-dry)

**Caveat**: still pair with a hard `MAX_ROUNDS` cap as a safety net. Budget can be wrong if a single agent spikes.

### P2 — Pipeline streaming (not batched) **[docs-only + video-shown]**

`pipeline()` is not "do all of stage 1, then all of stage 2." It's truly streaming: as soon as item 0 finishes stage 1, item 0 enters stage 2 — while items 1..N are still in stage 1. This means a fan-out workflow gets natural pipeline parallelism for free.

```js
const results = await pipeline(
  leads,                       // 8 items
  lead => agent(`research`),   // stage 1 — runs concurrently per item
  (research, lead) => agent(`write`)  // stage 2 — starts as soon as that item's research is done
)
```

For 8 leads with research averaging 30s and write averaging 20s, naive batching would take 30+20=50s. Streaming pipeline is ~30s total (stage 2 of item 0 overlaps with stage 1 of items 1-7).

Implication for our workflows: any time you have a multi-stage per-item operation, reach for `pipeline()` not `parallel()` + sequential.

### P3 — Automatic agent retry **[docs-only — 5×, not 3×]**

The Workflow Tool automatically retries failed `agent()` calls — per the workflow-creator's api-reference, **5×** for stall timeouts. The video said 3×; the docs say 5×. Trust the docs.

What this means:
- You don't need a try/catch wrapper for transient failures
- Schema mismatches trigger a retry with feedback (already known)
- MCP server hiccups, network blips, transient model errors → retried automatically
- After 3 failures, the agent call returns null/error

Implication: our S2 "fail fast" pattern still applies for *known unrecoverable* failures (404 endpoints, missing keys) — return `{ ok: false }` immediately so the retry doesn't waste 2 more attempts. But for *transient* failures, let the retry handle it.

---

## Part 5 — Patterns from production workflow examples

The workflow-creator skill ships 6 complete example workflows. Patterns worth lifting:

### Pattern 1 — Model-per-phase (cost discipline)

Declare the model on each phase or each agent call. Use cheap models for mechanical work, expensive models for quality-sensitive work.

```js
export const meta = {
  phases: [
    { title: 'Load leads',  model: 'haiku' },    // parsing — mechanical
    { title: 'Research',    model: 'haiku' },    // gathering — cheap
    { title: 'Write message', model: 'opus' },   // quality — expensive
  ],
}
```

**Rule of thumb**: Haiku for parsing/filtering/extraction/store-I/O. Sonnet for most reasoning. Opus only for final-quality outputs where the cost is justified by user-visible value.

Applied to our YLO probes: `remember()`/`recall()` → haiku. `analyze-*` content extraction → haiku. Title generation, image generation → sonnet/opus.

Estimated savings: cutting the 4 store-I/O agents in probe #2 from sonnet to haiku alone should drop wall-clock by ~50s.

### Pattern 2 — Loop-until-dry (with safety net)

The dead-code-sweep example uses a `DRY_STREAK` + `MAX_ROUNDS` pattern. Loop until N consecutive rounds find nothing, with a hard cap so it always terminates.

```js
const DRY_STREAK = 2  // stop after this many empty rounds in a row
const MAX_ROUNDS = 8  // hard cap so the loop always terminates
let emptyRounds = 0
let round = 0

while (emptyRounds < DRY_STREAK && round < MAX_ROUNDS) {
  round++
  const { items } = await agent(`Find unused symbols. Ignore: ${alreadyRemoved.join(', ')}`)
  if (items.length === 0) { emptyRounds++; continue }
  emptyRounds = 0
  // ... process items ...
}
```

Applies directly to Dark Factory:
- **Upstream Pulse**: scan provider repos until 2 consecutive providers return no new artifacts
- **Shadow Runs**: keep benchmarking until 2 consecutive runs produce no rubric change
- **Recon discover loop**: stop when 2 consecutive clusters reveal no new patterns

### Pattern 3 — Conditional escalation (cheap-first, expensive-fallback)

Try a cheap model/method first. If it fails to find what's needed, escalate to a more expensive one. This is plain JS in the workflow file — no special primitive needed.

```js
let info = await agent(`research lead ${lead.name}`, { model: 'haiku' })
if (!info || info.confidence < 0.5) {
  // escalate
  info = await agent(`research lead ${lead.name} thoroughly using web search`, { model: 'opus' })
}
```

This is the architectural superpower of code-wrapper workflows — branching logic is free. In a model-wrapper system this conditional would be a tool call from the orchestrator; here it's an `if`.

### Pattern 4 — Plain JS between phases (filter, transform, log)

Between agent calls, the workflow can do ordinary JS — filter arrays, compute statistics, log progress, early-return. This is free (no tokens, no agent overhead).

```js
const { issues } = await agent(`pull sentry issues`)
const bigOnes = issues.filter(i => i.userCount > threshold)
log(`${bigOnes.length} of ${issues.length} issues affect more than ${threshold} users`)
if (bigOnes.length === 0) return { fixed: 0, message: `No issues affect more than ${threshold} users` }
// continue...
```

This pattern is everywhere in the examples. Anytime your data could be smaller before the next agent call, filter it in JS. Anytime you have a yes/no decision, branch in JS. Saves the orchestrator the cost of "remembering" intermediate state across agent calls.

### Pattern 5 — args is a string, guard the parse

`args` arrives as a JSON string when invoked from the Workflow tool, but slash commands can pass non-JSON strings ("do it then"). Always guard the parse:

```js
const opts = typeof args === 'string'
  ? (() => { try { return JSON.parse(args) } catch { return {} } })()
  : (args ?? {})
const threshold = opts.minUsers ?? 20
```

We had this issue when probe #3 resume "lost args" — actually the args were never re-parsed correctly. The pattern above handles all invocation modes.

### Pattern 6 — Workflow-launching pattern

When you build a workflow that's invokable as a slash command, the description should make the trigger conditions clear and the doc-comment should show example args. From workflow-creator example:

```js
/**
 * triage-sentry — fix the Sentry issues that affect the most users.
 *
 * Pull unresolved issues, keep only those over a user-count threshold
 * (default 20), then fix and verify each one. The threshold is a single line
 * of ordinary JavaScript — workflow files run real JS, if-statements and all.
 *
 * Workflow({ name: 'triage-sentry', args: { minUsers: 20 } })
 */
export const meta = { /* ... */ }
```

The Workflow line in the doc-comment becomes the invocation hint shown in `/workflows`.

---

## Part 6 — The framing that ties it all together

From the video: **"Code wrapper vs model wrapper."** This is the central architectural concept.

**Model wrapper** (the old way):
- Claude is the orchestrator
- Every subagent result returns to Claude's context
- Claude reads the result, decides what to pass to the next subagent
- Pays a "token tax" at every join
- Orchestrator's context fills, eventually compacts, and starts forgetting

**Code wrapper** (the Workflow Tool way):
- A `.workflow.js` file is the orchestrator
- Subagent results return to plain JS variables
- The next subagent receives data through prompt template interpolation
- Zero token tax at joins
- No orchestrator context to fill

This is why our YLO comparison showed Workflow Tool was actually **slower** than blackboard for probe #2 — we used `remember()` heavily, which converts code-wrapper back into model-wrapper at the I/O layer (every store write is a subagent call). The fix isn't to abandon Workflow Tool; it's to use it correctly: pass state through JS variables, write to store only when the data needs to persist beyond the workflow run.

The Hybrid recommendation still holds for HITL-heavy and store-granular flows, but the boundary moves significantly toward Workflow Tool when workflows are redesigned to minimize cross-agent I/O.

---

## When is a workflow the right tool?

From the workflow-creator skill (Step 1 — "Decide whether a workflow is even the right tool"):

| The job | Right tool |
|---|---|
| One subagent, one task | The plain `Agent` tool — no workflow |
| A reusable procedure where **Claude** picks the steps each run | A **Skill** |
| Many subagents in a **fixed** shape (fan-out / pipeline / loop), same every run, worth resuming | A **Workflow** ✅ |

A workflow earns its cost when **all** of these are true:
- The work is parallel or multi-stage
- You want the orchestration deterministic and resumable
- Isolating each step in its own fresh context window is an advantage

For dark-factory: most of our planned automation (ingestion, evaluation, upstream pulse, shadow runs) fits this profile. One-off reads and analyses do not.

---

## Open research agenda

| # | Question | Priority |
|---|----------|----------|
| R1 | Can workflow scripts call MCP tools directly (not via agent)? | High — would solve S1 if yes |
| R2 | Does `env` in `.claude/settings.json` flow to workflow subagents? | High — would solve S3 cleanly |
| R3 | Is `model: "haiku"` usable for `remember()`/`recall()` agents? What's the latency improvement? | Medium — strong prior says yes, measure to confirm |
| R4 | Is double-nesting (S4) consistent? Characterise with a type matrix test | Medium |
| R5 | Does `isolation: "worktree"` work inside workflow `agent()` calls? | Low — needed for parallel file writers |
| R6 | What's the max `parallel()` concurrency? Docs hint at `min(16, cpu-2)` — confirm | Medium — affects fan-out sizing |
| R7 | Can workflows nest? Can a workflow call another workflow (not just agents)? | High — needed for compositional architecture |
| R8 | `budget` API — is it the input budget or remaining-tokens of the run? Where's the cap defined? | High — needed for budget-driven loops |
| R9 | What happens to `parallel()` retries when one item fails 3×? Whole batch fails, or one item returns null? | Medium |
| R10 | Does the workflow-creator's `scripts/validate-workflow.mjs` linter catch our C1-C5 issues? | High — adopt as pre-run check |
| R11 | MCP Blackboard pattern — does an MCP server-backed KV blackboard eliminate `remember()` overhead in practice? | **High — gates the v2 architecture upgrade** |
| R12 | Can workflow subagents call MCP tools at all? (R11 depends on this) | **High — answers via Spike 2 (hello-blackboard)** |
| R13 | Slash-command args (`/foo {json}`) — does the JSON string land cleanly in `args`? | Medium — answers via Spike 1 (hello-world) |
| R14 | Agent-invoked workflow — can an agent's tool call `Workflow({name, args})` fire and return a result? | Medium — answers via Spike 1 (hello-world) — gates Penny/Alex/Oscar |

---

## References

- **Ray Amjad's introduction video transcript**: `/Users/davidcruwys/dev/ad/apps/dark-factory/x.txt` (full transcript from the "Anthropic Just Dropped the Update Claude Code Always Needed" video)
- **workflow-creator skill** (cloned): `/tmp/dark-factory-upstream/claude-code-workflow-creator/`
  - `SKILL.md` — full authoring procedure
  - `references/api-reference.md` — every primitive, option, cap, constant
  - `references/patterns.md` — copy-paste orchestration patterns
  - `assets/examples/` — 6 complete runnable workflows (triage-sentry, dead-code-sweep, personalize-outreach, api-contract-drift-detector, implement-and-review, review-branch, customer-feedback-theme-extractor)
  - `assets/templates/` — starter files for fan-out, pipeline, loop shapes
  - `scripts/validate-workflow.mjs` — linter
- **YLO empirical comparison**: `experiments/ylo/workflow-tool/runs/b65/comparison.md`
- **Architecture context**: `docs/architecture.md` — how workflows fit into the Factory/Warehouse/Watchtower model
