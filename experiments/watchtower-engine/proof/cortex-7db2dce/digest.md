# Cortex — comprehension digest

**Source:** `~/dev/kybernesis/cortex` @ `7db2dce` (M4 Mini, read-only over SSH)
**Extracted:** 2026-06-15 · **Phase:** comprehend-only (read, cite, synthesize). No shapes picked, nothing rendered.
**Method:** enumerate → cited reads (per package, per ADR, architecture docs, versions ledger) → merge.
**Baseline diff against:** `a129a5d` (~v0.8.2, 2026-06-08 digest)

> Legend: ✅ = read directly in source · ⚠️ = inference from code/docs · ❓ = unknown

---

## What cortex is

**Cortex** (`@kybernesis/brain-*`) is a portable second-brain library — a family of **8 ESM-only TypeScript npm packages** (7 public + 1 private) that give an application persistent, portable memory. You feed it conversations, notes, transcripts and files; it stores them on a **timeline**, recalls them **by meaning** (not keywords), and quietly builds a **knowledge graph** of the people, facts and relationships inside them. ✅ (`README.md`)

It is **provider-pluggable by design**: the kernel (`brain-core`) holds the algorithms and depends only on the **interfaces** in `brain-contracts`. At startup you inject concrete implementations of three seams; swap any provider without touching the kernel, and an unwired seam **degrades gracefully** (vectors no-op, LLM features skip). ✅ (`README.md`, `brain-core/src/{storage,vectors,claude-call}.ts`)

> Cortex powers the memory layer in **KyberAgent Desktop (KAD)** and **KyberAgent Enterprise (KBDE)** — the library is the single source of truth for the algorithm; both products consume it. As of HEAD, **Cortex is the canonical algorithm and may move ahead of KAD** (ADR-0015 supersedes the old port-faithful rule). ✅ (`README.md`, `docs/decisions/0015-cortex-canonical-supersedes-port-faithful.md`)

Monorepo: pnpm workspace, **7 public packages versioned in lockstep** (currently **0.12.0**), TypeScript strict, released together via `scripts/release.sh`. The 8th package (`brain-bench`) is `private: true` and is never bumped/published with the public set. ✅ (`package.json`, `README.md`, `docs/versions.md`, `brain-bench/package.json`)

---

## The three seams (the architecture)

`brain-core` is programmed against `brain-contracts`; providers are wired at startup. ✅ (`README.md` provider-seams diagram, `docs/architecture/provider-seams.md`)

| Seam | Wired with | Default impl | Powers |
|---|---|---|---|
| **Storage** | `setStorageProvider()` | `brain-storage-sqlite` (+ `brain-storage-vec`) | All persistence — timeline, entities, facts, sleep, vectors; now also migration + reconcile |
| **Embedding** | `setEmbeddingProvider()` | `brain-embed-openai` | Semantic indexing + recall (`indexChunk`, `semanticSearch`, `hybridSearch`) |
| **LLM** | `setLLMProvider()` | `brain-llm-claude` | Relationship/fact extraction, contradiction detection, profiles, sleep reasoning |

The **StorageProvider is two-plane** — **Repositories** plane (CRUD, one repo per kind) and **Domain** plane (business-logic SQL: `SearchQueries`, `FactRetrievalQueries`, `SleepMaintenance`). New at HEAD: `SearchQueries` gained `relationalCandidates`; `FactRetrievalQueries` gained `resolveSourceTitles`; `TimelineRepository` gained `listAllFilePaths` / `relabelFilePath` / `stampContentHash` / `removeFileCluster` (the reconcile SQL primitives). ✅ (`brain-contracts/src/storage.ts`)

---

## The 8 packages

### Kernel & seam definitions
- **`brain-core`** — the kernel. Timeline, entity-graph, facts, vectors, retrieval, sleep, **and now reconcile** (`src/reconcile.ts`). No backends of its own; everything routes through the three DI seams. Public surface is a flat set of async exports in `src/index.ts`. A **per-tenant single-fiber write queue** (`queue.ts`) serialises writes. New at HEAD: `diffFilePaths` (pure diff), `reconcile()` (applies repairs via SQL primitives), `factFirstSearch` now resolves `source_title`, `effectiveConfidence` / `factDecay` exported (`fact-decay.ts`), `parseRelationalQuery` intent parser (`relational-intent.ts`). ✅

- **`brain-contracts`** — the seam definitions: Zod schemas, provider interfaces, shared constants. New at HEAD: `DiskFileEntry`, `BrainFileEntry`, `FilePathsDiff`, `RelationalCandidateParams` types; `SearchQueries.relationalCandidates`, `FactRetrievalQueries.resolveSourceTitles`, `TimelineRepository` reconcile primitives. `HybridSearchResult` gains `rawSemanticDistance?`, `rawKeywordScore?`, `source_title?`. `HybridSearchOptions` gains `useRelational`, `useLookup`, `useDecay` flags. ✅

### Providers (swappable)
- **`brain-storage-sqlite`** — default `StorageProvider`, a `better-sqlite3` backend. Splits a brain across separate SQLite files per tenant. Now includes a **migration subsystem** (`src/migrations/`): runner, registry, backup, error types, `runMigrations`, `setAutoMigrate`. Current migrations: `001-baseline` (marker, no DDL) and `002-file-provenance` (adds `file_path` + `content_hash` to `timeline_events`). Migration ledger table `_migrations` (one per DB file, only materialises when migration is triggered). `addEvent` uses dual-key upsert on `file_path` so file re-ingests converge to one row. ✅

- **`brain-storage-vec`** — `VectorRepository` over `sqlite-vec`. Fixed 1536-dim, brute-force `vec_distance_l2` search. Lazy-loaded; degrades to no-op if native binary can't load. Unchanged from 0.8.2. ✅

- **`brain-embed-openai`** — tenant-aware `EmbeddingProvider` wrapping OpenAI `text-embedding-3-small`. `embed(t, text) → number[1536] | null`. Per-tenant API-key resolution with per-tenant client caching. Unchanged from 0.8.2. ✅

- **`brain-llm-claude`** — `LLMProvider` invoking Claude via the local `claude` CLI subprocess. Never throws — resolves to `null` on failure, 60s timeout with SIGTERM on hang, optional `onError` hook. Unchanged from 0.8.2. ✅

### Testing
- **`brain-testkit`** — in-memory fakes + conformance/parity harness. `storageConformanceCases`, `runParityHarness` (top-N overlap, N=10, threshold 0.8), `makeLLMStub`. ✅

### Quality instrument (private, not published)
- **`brain-bench`** — the 8th package, `private: true`. A diagnostic quality instrument that asks "is the brain actually *good* at being a brain?" (vs `brain-testkit` which asks "does the backend honour the contract?"). CLI binary `brain-bench`. Three suites ship today:
  - **`--suite locomo`** — LoCoMo public corpus gate, fresh ingest per run. Baseline source-hit@5 ≈ 0.65. Zero query-time model calls.
  - **`--suite probes`** — 6-faculty personal-probe suite against a frozen copy of the live brain store (probe files live at `~/dev/ad/brains/.probes/<brain>/<faculty>.json`, not in the cortex repo).
  - **ingestion fidelity** — verifies that ingest preserves source material.
  - Also has a **synthetic conversational fixture** suite (`synthetic-convo-bench`).
  Six faculties: `recall`, `entity`, `temporal`, `multi_hop`, `currency`, `abstention`. `abstention` is `measurable: false` until the signal is calibrated (KYB-81). Scoring for source-hit faculties is recall@k (partial credit); `currency` checks the current source outranks superseded sources in top-k. This is the **no-regression gate** (ADR-0015): every retrieval behaviour change must show a clean before/after on a frozen snapshot before going default-on. ✅ (`brain-bench/README.md`, `src/score/faculty.ts`, `src/datasets/probes.ts`, `package.json`)

---

## The data model — 4 schema domains (databases)

A brain is up to **five SQLite files per tenant**; the library owns **four** (the 5th, `messages.db`, is KAD-app session storage). ✅ (`docs/architecture/storage-model.md`)

| File | Domain | Tables (additions at HEAD in **bold**) |
|---|---|---|
| **timeline.db** | Episodic — what happened, when | `timeline_events` (+ **`file_path`**, **`content_hash`** columns, **`idx_timeline_file_path`** index via migration 002), `timeline_fts`, `facts`, `facts_fts` (+ triggers); **`_migrations` ledger** (materialises only when migration is triggered) |
| **entity-graph.db** | Semantic — who/what, how connected | `entities`, `entity_mentions`, `entity_relations`, `entity_merges`, `entity_profiles`, `contradictions`, `entity_insights`; **`_migrations`** (baseline-only, no real migrations yet) |
| **sleep.db** | Housekeeping — consolidation/maintenance | `sleep_runs`, `maintenance_queue`, `memory_edges`, `sleep_telemetry`, `tier_transitions`; **`_migrations`** (baseline-only) |
| **vectors.db** (lazy) | Associative — recall by meaning | `chunks` (vec0 virtual, `float[1536]`), `chunk_meta`; **`_migrations`** (baseline-only) |

Key schema correctness fix at HEAD: **expired-fact leak** — `expires_at` comparisons using `datetime('now')` produced string comparisons where `T` > space, so same-day-expired facts leaked. Fixed by `sql-temporal.ts` helper (`julianday()` normalises both formats), applied across 9 sites. ✅ (`docs/architecture/storage-model.md`)

---

## Main flows (6 — RECONCILE is new)

**INGEST** (`store-conversation.ts`, fire-and-forget): extract relationships (LLM) → filter noise entities → write timeline event (dedupe; file rows use dual-key upsert on `file_path`) → segment + embed to vectors → create/link entities + mentions → real-time fact extraction (Haiku, ≤3/call). Now persists `file_path` and `content_hash` on timeline events for file-type ingests. ✅

**RECALL** (`hybrid-search.ts`): **5 channels** (not 4) fused with RRF (k=60):
1. semantic (vectors) — always
2. keyword FTS5 — always
3. temporal — fires on date terms
4. entity-augment (`expandQuery`) — **default off, refuted** (degrades every faculty)
5. relational graph arm (`relationalCandidates`, `parseRelationalQuery`) — **new, default on**; fires only when query parses as a relationship/lookup question (intent-gated, zero regression on knowledge corpora)

Post-fusion: cap 3 segments/parent, tier/priority enrichment, filter, optional Haiku rerank, sleep-edge related memories. Now surfaces `rawSemanticDistance?` and `rawKeywordScore?` (pre-RRF per-arm scores). `source_title?` on results when factFirst path resolves it. ✅ (`docs/architecture/retrieval-model.md`)

**FACT-FIRST RECALL** (`fact-retrieval.ts`): 4-layer enrichment (unchanged) — direct fact FTS+semantic → entity-graph BFS expansion → scene + bridge discovery → supporting segments → assemble to token budget. Now resolves `source_title` via `resolveSourceTitles` cross-table join for scorability. Optional `useDecay` flag applies read-time confidence decay (default off). ✅

**SLEEP** (`sleep/index.ts`, `runSleepCycleNow`): concurrency-guarded **9-step** cycle — unchanged from 0.8.2: decay → tag → consolidate → link → tier → summarize → observe → profile → entity-hygiene. ✅

**WATCHED-FOLDER INGESTION** (daemon, KAD/KBDE): 60s scheduler sweep, per-agent throttle+mutex → walk + mtime/size diff → new/changed → `storeConversation(channel=watched-folder)`, deleted/unwatched → cleanup. Lives in the consuming daemon. ⚠️

**RECONCILE** (new at 0.10.0–0.11.0, `brain-core/src/reconcile.ts`): the brain never touches the filesystem. **The HOST walks+hashes; the KERNEL owns the diff + repair.** The host passes a `diskList` (array of `{file_path, content_hash}`) and calls `reconcile(t, diskList, opts)`. `diffFilePaths` (pure, zero I/O) classifies into: `missing` (on disk, no row), `stale` (both, hashes differ), `orphaned` (brain row, not on disk), `renamed` (missing path whose hash matches an orphaned row — resolves via `relabelFilePath`, no re-ingest). `reconcile()` applies repairs through SQL primitives: `relabelFilePath`, `stampContentHash`, `removeFileCluster`. Fail-safe: validates disk entries (empty path or non-sha256-hex hash throws); refuses to remove orphans when `diskList` is empty (host walk failure protection). Report-only by default; re-ingest delegated to `opts.reingest` callback. ✅ (`brain-core/src/reconcile.ts`)

---

## Change story 0.9.0 → 0.12.0 (~59 commits since a129a5d)

| Version | Title | Key change |
|---|---|---|
| **0.8.3** | ISO date parsing | `detectTemporalExpiry` parses absolute + ISO dates |
| **0.8.4** | brain-bench milestone A | LoCoMo retrieval gate |
| **0.9.0** | Schema migration (Spec A) | versioned forward-only idempotent migration runner, ledger, backup, baseline |
| **0.10.0** | File provenance (Spec B) | `file_path` + `content_hash` on `timeline_events`; first real migration (002); report-only reconcile |
| **0.11.0** | Reconcile core (Spec C) | kernel owns the diff (PR #2); host-seam boundary locked; fail-safety at 7 sites |
| **0.12.0** | Retrieval arc | relational arm default-on (intent-gated); `useDecay`/`useLookup` dark (default off); expired-fact leak fixed; raw per-arm scores; `source_title` scorability; ADR-0015 canonical supersedes port-faithful |

Also shipped in the arc: brain-bench milestones B (ingestion fidelity) and C (personal probe suite + live-store scoring); 8-brain decay A/B study; ADR-0013, ADR-0014, ADR-0015; SupportSignal × Cortex brain integration investigation. ✅ (`docs/versions.md`, git log)

---

## Provenance & confidence

- All package/contract/storage/retrieval/migration/reconcile/bench claims tagged ✅ were read directly in source over SSH at `7db2dce`.
- ⚠️ items: watched-folder daemon lives partly in the consuming daemon (KBDE), not the library packages. Several sleep sub-steps (tag/link/tier/summarize/observe/profile) not re-read line-by-line at this commit.
- `meta.source` in `data.json` carries the path + commit_sha so this comprehension is **refreshable** by re-running against a new HEAD.
