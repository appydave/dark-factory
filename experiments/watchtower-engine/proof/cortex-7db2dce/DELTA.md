# DELTA.md — Cortex comprehension delta: a129a5d (v0.8.2) → 7db2dce (v0.12.0)

**Produced:** 2026-06-15  
**Baseline:** `a129a5d` (~v0.8.2, digest dated 2026-06-08)  
**Current HEAD:** `7db2dce` (v0.12.0)  
**~59 commits across 4 minor versions (0.9.0, 0.10.0, 0.11.0, 0.12.0)**

---

## Factual corrections — the existing brain deck is now wrong

These are claims the old digest made that are no longer true at HEAD.

### 1. Package count: 7 → 8

The baseline stated "7 ESM-only TypeScript npm packages." At HEAD there are **8 packages**: the 7 public ones plus `@kybernesis/brain-bench` (`private: true`, never published with the public set). Any slide or diagram stating "7 packages" is incorrect.

**Source:** `packages/` directory listing; `brain-bench/package.json` (`"private": true`); `brain-bench/README.md`.

---

### 2. Version: 0.8.2 → 0.12.0

The baseline stated "currently 0.8.2." At HEAD the public packages are at **0.12.0**. The arc covers 0.9.0 (migration), 0.10.0 (file provenance + reconcile), 0.11.0 (reconcile boundary), 0.12.0 (retrieval arc). Any version number in a deck is stale.

**Source:** `docs/versions.md` release ledger; `f33fe29` release commit.

---

### 3. Recall channels: 4 → 5

The baseline described **4 channels** (semantic, keyword, temporal, entity-augmented). At HEAD there are **5 channels**:
- Channel 4 (`expandQuery` entity-augmentation) is still present but **refuted and default off** — it degrades every faculty.
- Channel 5 (relational graph arm, `relationalCandidates`) is **new and default on** — it fires only when `parseRelationalQuery` returns non-null.

Any diagram showing 4-channel RRF is incorrect. Channel 4 should be labelled "off (refuted)" not "optional".

**Source:** `docs/architecture/retrieval-model.md` channel table; `brain-core/src/hybrid-search.ts`; ADR-0013.

---

### 4. Main flows: 5 → 6 (RECONCILE is new)

The baseline listed 5 flows (ingest, recall, fact-first recall, sleep, watched-folder). At HEAD there is a **6th flow: RECONCILE** — the kernel-owned file-inventory diff and repair system introduced in v0.10.0–0.11.0.

**Source:** `brain-core/src/reconcile.ts`.

---

### 5. Schema: timeline_events gained file_path + content_hash

The baseline schema table showed `timeline_events` with no file provenance columns. At HEAD, `timeline_events` has **`file_path TEXT`** and **`content_hash TEXT`** (nullable), a partial index `idx_timeline_file_path`, and a migration ledger table `_migrations` (one per DB file). The `addEvent` path uses dual-key upsert on `file_path` so re-ingesting the same file converges to one row.

**Source:** `brain-storage-sqlite/src/migrations/timeline/002-file-provenance.ts`; `src/timeline.ts`; `src/index.test.ts` (lines 160–162).

---

### 6. ADR-0003 port-faithful rule is retired (superseded)

The baseline digest did not mention governance. The old "port-faithful" rule (ADR-0003) required Cortex to match KAD exactly and mandated same-day KAD PRs for every behaviour change. **ADR-0015 (2026-06-13) supersedes it**: Cortex is now canonical and may improve freely, gated only on the brain-bench no-regression test. This is a structural change to how the library is governed.

**Source:** `docs/decisions/0015-cortex-canonical-supersedes-port-faithful.md`.

---

## New concepts worth teaching

Each entry: what changed + brain metaphor framing + audience tag.

---

### A. Multi-arm intent-gated recall + the flat-score-displacement principle

**What changed:** `hybridSearch` now has a 5th channel (relational graph walk) that fires only when `parseRelationalQuery` identifies a relationship-shaped query. Three independently-measured experiments all showed the same mechanism: an always-on arm that injects flat-scored candidates into RRF crowds the right answer out of top-k. The math: RRF sums `1/(k+rank+1)` per arm; an arm emitting N candidates at rank 1..N fills N slots in the fixed top-k window, displacing genuinely relevant results. Always-on entity arm: entity +23, recall −21 (net zero). Solution: arms fire only when the query intent matches what the arm provides.

**Brain metaphor:** Your brain doesn't consult its "social network recall" for every thought — only when you're asked "who introduced you to X?" Activating relationship-memory for a factual recall question floods working memory with the wrong kind of evidence.

**Tag:** `[architecture-set]`  
**Source:** `docs/architecture/retrieval-model.md` §"The one principle"; ADR-0013; gap-analysis experiments #3, #0, #8.

---

### B. Read-time fact decay + the use-recency/decay≠deletion reframe

**What changed:** `useDecay` (default off) weights fact scores by `effectiveConfidence = confidence × 2^(-age_days/halflife)` before the factFirst final sort. A full 8-brain A/B showed it halves quality on knowledge corpora (25%→11% overall) because in a document brain, fact timestamp = ingest time not recency of relevance. The 2026-06-14 Ian reframe (KYB-85) promotes access-based decay as the correct target: key decay on `last_reinforced_at` (time-since-last-use) not assertion age. Key constraint: **decay ≠ deletion** — a decayed fact must still surface on a targeted query.

**Brain metaphor:** A real brain doesn't forget a fact just because it was learned long ago — it forgets what it hasn't used. A math formula you haven't used in years fades; one you use daily stays crisp. Date-of-writing is the wrong signal; date-of-last-use is right.

**Tag:** `[architecture-set]`; the "recency ≠ relevance" reversal is also `[audience-deck]`  
**Source:** ADR-0014 (2026-06-14 update section); `brain-core/src/fact-decay.ts`; `docs/research/decay-by-source.md`.

---

### C. Reconcile / provenance + the kernel-never-touches-disk boundary

**What changed:** Files ingested into a brain now carry `file_path` + `content_hash` on their `timeline_events` row. The kernel can answer the question "what files does this brain know about?" (`listAllFilePaths`) and a new `reconcile()` call takes a host-supplied `diskList`, runs a pure diff (`diffFilePaths`), and repairs via SQL primitives: relabels renames, stamps missing hashes, removes orphaned clusters, calls back to the consumer's `reingest` for missing/stale files. **The kernel never touches the filesystem.** The host walks and hashes; the kernel owns the diff and repair policy.

**Brain metaphor:** Your brain knows it read a document but doesn't go back to check if the document still exists on the shelf. A librarian (the host) periodically audits the shelves and tells your brain: "this book moved to a new shelf location, this one was thrown away, this one was replaced." Your brain updates its index; it never leaves the reading room.

**Tag:** `[architecture-set]`; the kernel-never-touches-disk boundary is `[audience-deck]`  
**Source:** `brain-core/src/reconcile.ts` header comment; `docs/versions.md` v0.10.0–0.11.0 entries; `brain-contracts/src/storage.ts` TimelineRepository reconcile primitives.

---

### D. brain-bench self-grading / 6 faculties

**What changed:** A new private package (`brain-bench`) measures whether the brain is actually good at being a brain — not whether the code conforms to the contract. It is the **no-regression gate**: every retrieval arm must show a clean before/after on a frozen brain snapshot before going default-on. Three suites: LoCoMo public corpus (reproducible gate), personal probes (live brain quality), ingestion fidelity. Six faculties: recall, entity, temporal, multi_hop, currency, abstention. Abstention is `measurable: false` until the threshold is calibrated. Scoring: source-hit@k (partial credit for source-hit faculties), currency checks the current source outranks superseded in top-k.

**Brain metaphor:** You wouldn't just test that your memory *stores* information — you'd test that it *recalls* the right thing at the right time (recall), knows who people are (entity), remembers when things happened (temporal), can connect two facts across a gap (multi_hop), and surfaces the most current version when something changed (currency).

**Tag:** `[architecture-set]`; the "does the brain know things?" framing is `[audience-deck]`  
**Source:** `brain-bench/README.md`; `src/score/faculty.ts`; `src/datasets/probes.ts` (FACULTIES array); ADR-0015.

---

### E. Safe schema migration (Spec A)

**What changed:** v0.9.0 shipped a versioned, forward-only, idempotent migration runner for the brain SQLite DBs. Each DB file carries its own `_migrations` ledger. The trigger is consumer-chosen: local auto-on-open (`setAutoMigrate`) or managed per-tenant migrator (Arcana). Migrations are checksummed (drift = hard error). Pre-migration backup hook. Baseline detection: if the DB predates the migration system (sentinel table exists, `_migrations` doesn't), it gets a baseline stamp without running DDL. Currently one real migration: `002-file-provenance` (adds `file_path`/`content_hash` to `timeline_events`).

**Brain metaphor:** Your brain's "filing system" needs to evolve without losing what's already stored. The migration runner is the upgrade protocol: it checks what version the filing system is at, applies only what's new, keeps a receipt, and backs up before touching anything.

**Tag:** `[architecture-set]`  
**Source:** `brain-storage-sqlite/src/migrations/runner.ts`; `migrations/registry.ts`; `docs/versions.md` v0.9.0 entry.

---

### F. ADR-0015 — canonical supersedes port-faithful

**What changed:** The old ADR-0003 port-faithful rule required Cortex to be byte-identical to KAD and mandated same-day KAD PRs for every change. With KAD and KBDE now *consuming* Cortex (not the other way around), that rule blocks improvement rather than enabling adoption. ADR-0015 retired it: Cortex is the algorithm source of truth, may improve freely, must prove no-regression via brain-bench, must start from KAD's shapes, and must inform consumers on version bumps. No same-day-PR obligation; no behavioural parity ceiling.

**Brain metaphor:** In the port-faithful era, the library was "a copy of KAD's brain." In the canonical era, the library *is* the brain; KAD/KBDE are consumers. The copy relationship is inverted.

**Tag:** `[architecture-set]`  
**Source:** `docs/decisions/0015-cortex-canonical-supersedes-port-faithful.md`.

---

## Schema diff summary (for deck diagram updates)

| Element | Was (a129a5d / v0.8.2) | Is (7db2dce / v0.12.0) |
|---|---|---|
| `timeline_events` columns | standard set | + `file_path TEXT`, `content_hash TEXT`, `idx_timeline_file_path` partial index |
| `_migrations` table | not present | present in all 4 DB files (only materialises when migration triggered) |
| `HybridSearchResult` fields | hybridScore, semanticScore, metadataScore | + `rawSemanticDistance?`, `rawKeywordScore?`, `source_title?` |
| `HybridSearchOptions` flags | expandQuery, factFirst, rerank | + `useRelational` (default on), `useLookup` (default off), `useDecay` (default off) |
| StorageProvider TimelineRepository | addEvent, getEvent, etc. | + `listAllFilePaths`, `relabelFilePath`, `stampContentHash`, `removeFileCluster` |
| SearchQueries | metadataCandidates, temporalCandidates, enrichByPath | + `relationalCandidates` |
| FactRetrievalQueries | direct/entity/scene/bridge/assemble | + `resolveSourceTitles` |

---

## Source citations key

| Claim | Primary source |
|---|---|
| 8 packages | `packages/` ls; `brain-bench/package.json` |
| Version 0.12.0 | `docs/versions.md`; git tag |
| 5-channel retrieval | `docs/architecture/retrieval-model.md`; ADR-0013 |
| 6 flows | `brain-core/src/reconcile.ts` |
| file_path/content_hash | `brain-storage-sqlite/src/migrations/timeline/002-file-provenance.ts`; `src/index.test.ts:160-162` |
| MEASURABLE map / 6 faculties | `brain-bench/src/score/faculty.ts`; `src/datasets/probes.ts` |
| Decay A/B numbers | ADR-0014 table |
| Kernel-never-touches-disk | `brain-core/src/reconcile.ts` header |
| ADR-0015 port-faithful retired | `docs/decisions/0015-cortex-canonical-supersedes-port-faithful.md` |
| julianday fix (9 sites) | `docs/architecture/storage-model.md` §"SQL-layer correctness" |
