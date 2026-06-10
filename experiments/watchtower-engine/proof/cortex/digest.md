# Cortex — comprehension digest

**Source:** `~/dev/kybernesis/cortex` @ `a129a5d50ba8a140c288b6f2eb03ddadcee873a9` (M4 Mini, read-only over SSH)
**Extracted:** 2026-06-08 · **Phase:** comprehend-only (Phase 0–2). No shapes picked, nothing rendered.
**Method:** enumerate → 8 parallel cited readers (one per package + db-model + flows) → merge.

> Legend: ✅ = read in source · ⚠️ = inference from code/docs · ❓ = unknown

---

## What cortex is

**Cortex** (`@kybernesis/brain-*`) is a portable second-brain library — a family of **7 ESM-only TypeScript npm packages** that give an application persistent, portable memory. You feed it conversations, notes, transcripts and files; it stores them on a **timeline**, recalls them **by meaning** (not keywords), and quietly builds a **knowledge graph** of the people, facts and relationships inside them. ✅ (`README.md`)

It is **provider-pluggable by design**: the kernel (`brain-core`) holds the algorithms and depends only on the **interfaces** in `brain-contracts`. At startup you inject concrete implementations of three seams; swap any provider without touching the kernel, and an unwired seam **degrades gracefully** (vectors no-op, LLM features skip). ✅ (`README.md`, `brain-core/src/{storage,vectors,claude-call}.ts`)

> Cortex powers the memory layer in **KyberAgent Desktop (KAD)** and **KyberAgent Enterprise (KBDE)** — the library is the single source of truth for the algorithm; both products consume it. ✅ (`README.md`)

Monorepo: pnpm workspace, 7 packages **versioned in lockstep** (currently **0.8.2**), TypeScript strict, released together via `scripts/release.sh`. ✅ (`package.json`, `README.md`)

---

## The three seams (the architecture)

`brain-core` is programmed against `brain-contracts`; providers are wired at startup. ✅ (`README.md` provider-seams diagram, `docs/architecture/provider-seams.md`)

| Seam | Wired with | Default impl | Powers |
|---|---|---|---|
| **Storage** | `setStorageProvider()` | `brain-storage-sqlite` (+ `brain-storage-vec`) | All persistence — timeline, entities, facts, sleep, vectors |
| **Embedding** | `setEmbeddingProvider()` | `brain-embed-openai` | Semantic indexing + recall (`indexChunk`, `semanticSearch`, `hybridSearch`) |
| **LLM** | `setLLMProvider()` | `brain-llm-claude` | Relationship/fact extraction, contradiction detection, profiles, sleep reasoning |

A notable design point: the **StorageProvider is two-plane** — a **Repositories** plane (CRUD, one repo per kind) and a **Domain** plane (business-logic SQL: `SearchQueries`, `FactRetrievalQueries`, `SleepMaintenance`). This split was the "storage untangle" (0.6.0, commits `U0…U5`) that moved business logic out of the data layer. ✅ (`brain-contracts/src/storage.ts`, git log)

---

## The 7 packages

### Kernel & seam definitions
- **`brain-core`** — the kernel. Timeline, entity-graph, facts, vectors, retrieval, sleep. No backends of its own; everything routes through the three DI seams. Public surface is a flat set of async exports in `src/index.ts`. A **per-tenant single-fiber write queue** (`queue.ts`) serialises writes (SQLite WAL has one writer). ✅
- **`brain-contracts`** — the seam definitions: Zod schemas, the `StorageProvider`/`EmbeddingProvider`/`LLMProvider` interfaces, and shared constants (`EMBEDDING_DIM=1536`, `RRF_K=60`, `SOURCE_CONFIDENCE`, enums, Claude model aliases). Depends only on Zod. Domain row fields are **snake_case by design** to match KAD's DB columns, enforced by a `schema-naming.test.ts` guard (a silent camelCase drift broke v0.2.0). ✅

### Providers (swappable)
- **`brain-storage-sqlite`** — default `StorageProvider`, a `better-sqlite3` backend. Splits a brain across separate SQLite files per tenant (timeline / entity-graph / sleep) and lazy-loads the vector store. Per-slug-per-kind connection pooling. ✅
- **`brain-storage-vec`** — `VectorRepository` over `sqlite-vec`. Fixed **1536-dim**, brute-force `vec_distance_l2` search ("brain scale" — no HNSW). Lazy-loaded by the SQLite provider; **no static import**, so if the native binary can't load, vector ops no-op rather than crash. ✅
- **`brain-embed-openai`** — tenant-aware `EmbeddingProvider` wrapping OpenAI **`text-embedding-3-small`**. `embed(t, text) → number[1536] | null`. Per-tenant API-key resolution (`<home>/.env` → `process.env.OPENAI_API_KEY`) with per-tenant client caching; missing key / failure degrades to `null`. ✅
- **`brain-llm-claude`** — `LLMProvider` invoking Claude through the local **`claude` CLI subprocess** (the reasoning seam). **Never throws** — resolves to `null` on spawn/exit/empty/timeout with an optional `onError` hook; 60s timeout with SIGTERM on hang (P1 hardening, commit `880816e`). Model aliases haiku/sonnet/opus. ✅

### Testing
- **`brain-testkit`** — in-memory fakes + conformance/parity harness. `storageConformanceCases` (~18 vitest-free behavioural cases), `runParityHarness` (top-N overlap, default N=10, threshold 0.8 — guards backend swaps), `makeLLMStub` (records `.calls`), `createTestTenant`. ✅

---

## The data model — 4 schema domains (databases)

A brain is up to **five SQLite files per tenant**; the library owns **four** (the 5th, `messages.db`, is KAD-app session storage, not library). The split is a deliberate cognitive-architecture separation buying write concurrency (WAL per file) and independent lifecycle; the trade-off is **soft cross-file links** (JSON denormalisation, no cross-file foreign keys). ✅ (`docs/architecture/storage-model.md`)

| File | Domain | Tables |
|---|---|---|
| **timeline.db** | Episodic — what happened, when | `timeline_events`, `timeline_fts`, `facts`, `facts_fts` (+ triggers) |
| **entity-graph.db** | Semantic — who/what, how connected | `entities`, `entity_mentions`, `entity_relations`, `entity_merges`, `entity_profiles`, `contradictions`, `entity_insights` |
| **sleep.db** | Housekeeping — consolidation/maintenance | `sleep_runs`, `maintenance_queue`, `memory_edges`, `sleep_telemetry`, `tier_transitions` |
| **vectors.db** (lazy) | Associative — recall by meaning | `chunks` (vec0 virtual, `float[1536]`), `chunk_meta` |

---

## Main flows

**INGEST** (`store-conversation.ts`, fire-and-forget): extract relationships (LLM) → filter noise entities → write timeline event (dedupe) → segment + embed to vectors → create/link entities + mentions → real-time fact extraction (Haiku, ≤3/call). ✅

**RECALL** (`hybrid-search.ts`): four channels — semantic (vectors), metadata FTS5, temporal, optional entity-augmented — fused with **Reciprocal Rank Fusion (k=60)**, capped to 3 segments/parent, enriched by tier/priority, filtered, optionally Haiku-reranked, then decorated with related memories from sleep `memory_edges`. ✅

**FACT-FIRST RECALL** (`fact-retrieval.ts`): a 4-layer enrichment — direct fact FTS+semantic → entity-graph BFS expansion (hop penalty) → scene + bridge discovery → supporting segments → assemble to a token budget with deterministic source-priority tie-breaking. ✅/⚠️

**SLEEP** (`sleep/index.ts`, `runSleepCycleNow`): a concurrency-guarded **9-step** cycle — decay → tag → consolidate → link → tier → summarize → observe → profile → entity-hygiene — each step checkpointed and telemetered, full run lifecycle in `sleep_runs`. ✅ (decay/consolidate/entity-hygiene read in full; tag/link/tier/summarize/observe/profile ⚠️ referenced not fully read)

**WATCHED-FOLDER INGESTION** (daemon, KAD/KBDE — `docs/architecture/watched-folders-ingestion.md`): 60s scheduler sweep, per-agent throttle+mutex → walk + mtime/size diff vs a regenerable JSON state file → new/changed → `storeConversation(channel=watched-folder)`, deleted/unwatched → cleanup. ⚠️ (lives in the consuming daemon, not the library packages)

---

## Change story (last 14 days)

The recent arc is **provider-portability + hardening + docs**: the **0.6.0 storage untangle** (two-plane repositories/domain, commits `U0–U5`) → **0.7.0** public-API trim (removed `ensureSleepSchema`, a handle-leak retire) → **0.8.0** the portable, **tenant-aware embedder** (`brain-embed-openai`, `embed(t, text)`) → **0.8.1/0.8.2** delivery-review patches, **brain-llm-claude P1 hardening** (subprocess timeout + onError hook), P3 test coverage → HEAD `a129a5d` root + per-package READMEs and the provider-seam diagram. ✅ (git log)

---

## Provenance & confidence

- All package/contract/storage/vector/embed/llm/testkit claims tagged ✅ were read directly in source over SSH at the pinned commit.
- ⚠️ items: several sleep sub-steps (tag/link/tier/summarize/observe/profile) and the watched-folder daemon were read at doc/reference level, not line-by-line — they live partly in the consuming daemon (KBDE), not the seven library packages.
- `meta.source` in `data.json` carries the path + commit_sha so this comprehension is **refreshable** by re-running the burst against a new HEAD.
