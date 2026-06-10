# Switchboard Greenfield Charter — KICKOFF (paste into a fresh `claude` window in ~/dev/ad/apps/dark-factory)

> Paste the block below as your first message in a FRESH window (needed so `/agent-skills:spec` loads — it isn't in the session that wrote this). Everything it references is on disk.

---

We're writing a **greenfield design charter for Switchboard** (the Dark Factory comms/state-plane app). This is a DESIGN doc — timebox to a charter, NOT a rebuild; the working bus is a real asset. Do this in order, and ORIENT + ASK me before authoring — don't auto-build.

**1. Read the seed (master doc):** `backlog/2026-06-09-switchboard-greenfield-seed.md` — it has the trigger, current Switchboard state, the bounded-responsibility lines, the CRUD-vs-kill rule, DF-7 (the state-plane spec) as an INPUT with all 5 decisions ruled, the 7 open design questions, and tooling context. Also auto-load `MEMORY.md`.

**2. Batch-mine these session transcripts** (via the `abridge` subagent, one per transcript, in parallel, with a "what-is-Switchboard / what-should-it-be / greenfield-design" lens). Dedupe net-new findings against the seed + memories; consolidate the additive material into one grounding doc. Path prefix `~/.claude/projects/`:
   - **switchboard-repo build cluster (HIGHEST value — design-while-building, never distilled):** `-Users-davidcruwys-dev-ad-apps-switchboard/`
     - `b9153637-d47e-4675-9617-413e208c0a5d.jsonl`
     - `992e121b-4702-4924-a1d6-102a2d690761.jsonl`
     - `0d7ebe05-d6cb-4b60-b829-87b583f6d20d.jsonl`
     - `5d7e5dfe-ef0f-4fc4-98ba-18d5f09e75ff.jsonl`
     - `0cc44f83-51a3-40ad-bdb0-cb2fc586e266.jsonl`
     - `6396f590-5c99-45e5-94ba-65dd152716d4.jsonl`
     - `74659a99-7ec4-49f5-a54c-bc5ae3156302.jsonl`
   - **design-origin (15MB, partly already in memories — mine for compressed-away detail):** `-Users-davidcruwys-dev-ad-apps-dark-factory/627e86a2-ecc2-4057-bfa7-619a1c1de676.jsonl`
   - **optional moderate (dark-factory):** `215b9cee-ce91-4b8c-9ade-dc22062358b7.jsonl`, `940816e3-a5b4-4bc5-a6b4-2175c421ca7b.jsonl`

**3. Read the written design sources** (the real material — NOT in the transcript that wrote the seed):
   - `docs/watchtower/symphony-spec.md` (**80KB — richest; Switchboard's job/claim/state model derives from it**) + `symphony-relook-2026-06-07.md`
   - `backlog/2026-06-06-dark-factory-sentinel.md` (the Sentinel design plan)
   - `docs/watchtower/{DECISIONS,schemas,spec,plan}.md`, `watchtower-from-symphony.md`, `reaper-brief.md`
   - AppySentinel template: `~/dev/ad/apps/appysentinal/{CONTEXT.md,DEVELOPMENT.md}` + Switchboard's own `~/dev/ad/apps/switchboard/{README.md,CLAUDE.md,appysentinel.json}` + `src/coordination/staleness-detector.ts` (the model recipe)
   - DF-7 inputs: `backlog/specs/df7-switchboard-state-plane-spec.md` (+ `…osmani.md`, `df7-osmani-vs-appydave-delta.md`)
   - Memories: `watchtower-sentinel-bus-direction`, `dark-factory-is-a-constellation-of-apps`, `cleanup-is-harness-driven-not-remembered`, `constellation-first-placement`, `osmani-agent-skills`, `adversarial-delta-technique`, `requirements-first-store-for-future-ticketing`, `hitl-at-marshall-gates`

**4. THEN author the charter via `/agent-skills:spec`** (Osmani `spec-driven-development`, interview-first — the right greenfield author, and the fair "re-test Osmani as author on a greenfield capability" the DF-7 delta asked for). **I (David) am the primary source** — the charter must INTERVIEW me on the §5 open questions (full message-type surface · N-Marshall/multi-machine federation · event-log retention · DF-3 relationship without duplication · how much accreted bus to reshape · the "factory builds the apps" doctrine · scope of "awareness of communication"). Do NOT fabricate answers from the mined material — use it to make the interview sharp.

**5. Optional:** capture an adversarial delta (Osmani-on-greenfield vs the appydave method) as the 2nd data point for DF-8 (`backlog/specs/df8-comparison-registry-spec.md`).

Deliverable: a Switchboard greenfield **charter** (what it IS · bounded responsibility · full intended surface · where the state-plane + DF-3 telemetry fit · what of the current bus stays/reshapes), with DF-7 re-evaluated as a slice of it. Then surface to me — don't greenlight a build.
