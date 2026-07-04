# HANDOVER — external-research-agent queue, ready to execute

**Written:** 2026-07-04 (Roamy). **For:** a fresh conversation with access to David's friend-operated
online research agent. **Status:** queue built, 3 tickets seeded, nothing executed yet.

---

## 0. What this is

Dark Factory's engine (`engine/`) already runs a ticket-first queue (`engine/store/queue/ → running/ →
done/`) for internal Claude Code workers. This handover adds a **new ticket kind for a different kind of
worker**: David has a friend-operated online research agent — **not** a Claude Code session, **no file
access**, capabilities/API unknown, likely one consumer processing things one at a time (not a swarm — an
earlier framing in the sourcing conversation wrongly assumed parallel fan-out; corrected).

Three tickets are seeded in `engine/store/queue/`, `"kind": "external-research"`. Each is fully
self-contained (question + context pasted as literal text) because the receiving agent can't read files.

**⚠️ Do not run `engine/orchestrator.py` while these sit in `queue/`** — it does not filter by `kind`, it
claims every `.json` file in the directory. Handle these tickets manually per the steps below before (or
instead of) running the pool.

## 1. The three seeded tickets

| Ticket file | Question (short) |
|---|---|
| `20260704T034440Z-research-heterogeneous-worker-pools.json` | How do CrewAI/AutoGen/LangGraph handle a worker with no file/tool access needing fully self-contained context? |
| `20260704T034441Z-research-async-human-in-loop-queues.json` | What's the minimal real-world mechanism (GH Actions approvals, Zapier human-input steps, shared-sheet-as-queue, etc.) for async hand-off to one external no-file-access consumer? |
| `20260704T034442Z-research-machine-mined-decision-confidence.json` | Beyond Lore (arXiv:2603.15566), find machine-mined decision-record confidence schemes that RISE over time with corroborating evidence, and see how any handle later contradicting evidence. |

Each ticket's `question` + `context` fields are the complete, self-contained packet — read the ticket JSON,
there is nothing else to fetch.

## 2. Execution steps, per ticket

```bash
cd ~/dev/ad/apps/dark-factory
ls engine/store/queue/*.json    # find the "kind": "external-research" ones
```

For each:

1. **Claim it** — move it from `queue/` to `running/` (mirrors the existing atomic-claim convention, a
   plain `mv` is fine for a single manual consumer):
   ```bash
   mv engine/store/queue/<ticket>.json engine/store/running/<ticket>.json
   ```
2. **Relay it** — take the ticket's `question` + `context` fields and hand them to the friend's online
   agent however that conversation actually talks to it (paste into its chat UI, call its API, whatever
   the real mechanism turns out to be — that's for this conversation to discover/use, it wasn't knowable
   from the DF side).
3. **Capture the result** — write the agent's answer into `engine/store/results/<ticket>.json`, matching
   the ticket's own `output_schema` field as closely as the agent's actual answer allows. Shape:
   ```json
   {"ticket": "<ticket>.json", "status": "done", "answer": "...", "sources": ["..."], "confidence": "...", "notes": "anything that didn't fit the schema, or where the agent's answer fell short"}
   ```
4. **Mark it done**:
   ```bash
   mv engine/store/running/<ticket>.json engine/store/done/<ticket>.json
   ```
5. No `audit.jsonl` entry needed (see `engine/store/queue/.CONVENTION.md`) — the file's own queue → running
   → done movement plus its `results/<ticket>.json` is the record.

## 3. If the friend's agent turns out to support something better than manual relay

If it turns out to have a real API, a shared doc it watches, or anything more automatable than
copy-paste — **don't build that integration silently**. Come back and update
`backlog/2026-07-04-external-research-agent-queue.md` (the original capture) with what was actually
learned about its capabilities, since the open questions there were explicitly gated on "ask, don't guess."

## 4. When all 3 are done

Report back (to David, or in whatever surfaces this handover) with:
- The 3 results, briefly
- Whether the manual relay process worked cleanly or hit friction worth fixing
- Whether it's worth seeding more research tickets this way, or whether this pattern doesn't hold up in
  practice

## Key paths

| What | Path |
|---|---|
| Queue (new tickets go here) | `~/dev/ad/apps/dark-factory/engine/store/queue/` |
| Running (claimed) | `~/dev/ad/apps/dark-factory/engine/store/running/` |
| Done | `~/dev/ad/apps/dark-factory/engine/store/done/` |
| Results | `~/dev/ad/apps/dark-factory/engine/store/results/` |
| Convention doc (kind/executor rules) | `~/dev/ad/apps/dark-factory/engine/store/queue/.CONVENTION.md` |
| Original idea capture (open questions) | `~/dev/ad/apps/dark-factory/backlog/2026-07-04-external-research-agent-queue.md` |
