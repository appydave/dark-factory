# 14 — CALIBRATION NOTES (Critical Assessment)

**Purpose**: Honest assessment of the calibration run against a REAL 102-record corpus — did the schema hold, what breaks at 1,250-capture / 6-month scale, what to tune BEFORE the full run.

**For Agents**:
- This is the gating document for the full archaeology run. The P0/P1 items below are prerequisites, not suggestions.
- This file replaces a zero-record stub. The prior run's P0 (silent empty hand-off) was real: keep stage-boundary record-count assertions + manifests as a permanent invariant even though this run received data.

---

## Headline verdict

**Pipeline SHAPE: SOUND. Scale AS-IS: NO.**

The three-layer decomposition (per-record extraction → weave → harvest) produced genuinely useful output: 66 routed tickets, a punchlist that both matches and extends David's own asks, and arc-detection (doc-watcher planned 3× never started; Challenge DV price walk) that no single capture contains. The layering works. But four schema fields degraded under only 102 records in ways that are fatal at 12× volume: free-text threads fragment, fingerprints don't cluster, open-loops have no identity, and noise costs full extraction. Fix those four; the architecture itself doesn't need rethinking.

## What held up

| Element | Verdict | Evidence |
|---------|---------|----------|
| Per-record `essence` | **Strong** | Weave + harvest ran almost entirely off essences; raw files never needed re-reading. This is the compression layer earning its keep. |
| `kind` taxonomy | **Mostly held** | noise/meeting/feedback/direction were reliable. Failure mode: `decision` applied to non-decisions — omi 07-03-1401 is `kind: decision` yet carries 2 open items (org name, loading gap); omi 07-06-0904 is a `decision` that was never acted on and got re-planned twice. `decision` needs a `decided:` payload (what exactly was settled) or it's just a confident-sounding `direction`. |
| `open_loop` boolean | **Held as flag, failed as system** | 57% flagged correctly — but a boolean over 70 distinct items gives no identity, no cross-capture linkage, no closure. See P1-3. |
| `actions[]` extraction | **Held** | ~70 loop items → 66 tickets with modest dedup effort. But `target` is free-text and drifted (dark-factory vs Dart Factory vs dark-factory/app-pipeline) — needs a routing table. |
| Noise identification | **Accurate but expensive** | All 30 noise records were correctly flagged — AFTER paying full LLM extraction on each. Wrong place to pay. |
| Zero-fabrication provenance | **Held** | Every harvest claim traces to capture ids. Keep as invariant. |

## What broke (and will break worse at scale)

### 1. Thread taxonomy fragmented — the worst offender
Free-text `thread` produced fragmentation within ONE fortnight:
- One engagement, three threads: `client/linda-coaching`, `client/linda-challengedv`, `client/challenge-dv` (same Linda, same deal).
- One cluster, five threads: `kyber-extensions`, `kybernesis-extensions`, `kybernesis-extension-sdk`, `iframe-extension-dev`, `kyberagent-learning`.
- KDD work split across `kdd-lisa`, `kdd-librarians`, `dark-factory-kdd`, plus KDD actions filed under `dark-factory-engine`.
- Junk-drawer drift: `noise` vs `noise/ambient` vs `personal/ambient` used interchangeably.

At 6 months this destroys the recurrence analysis (the pipeline's whole point): a 40-mention arc reads as six 6-mention threads. **Fix: two-level controlled taxonomy (`area/thread`) seeded from this run's atlas, with an `emergent/` prefix for new threads and a mandatory per-batch merge pass that reconciles emergent threads into the registry.** The thread registry becomes persistent state carried between batches.

### 2. Fingerprints don't cluster across captures
`fingerprint` worked for exact duplicates (the .clean/raw pair got identical fingerprints — good) and failed for the actual clustering job: the Captain's Log arc produced ~10 unrelated fingerprints ("unify omi plaud transcription pipeline", "captains log telemetry observability", "captains log kybernesis extension build"...). Human weaving, not fingerprints, found the arc. **Fix: keep fingerprints as human-scannable labels, add a global embedding index (embed every essence once, cluster corpus-wide, not per-slice) as the real recurrence mechanism.** Per-batch fingerprinting can never link week 2 to week 19.

### 3. Open loops have no identity or lifecycle
The corpus's most valuable finding — doc-watcher planned 07-06 (twice, both devices) and again 07-13 with zero progress — was only detectable by a human reading the weave. A boolean can't represent "same loop, third mention, 7 days stale." **Fix: loop registry with stable IDs, first-seen/last-seen, mention count, closure events, staleness. New captures match against open loops (embedding similarity) before minting new ones.** This is also punchlist item #2 — the pipeline and the product need the same machinery.

### 4. Noise costs full extraction
30/102 records (29%) — including Plaud files whose entire body is "." — went through complete LLM extraction. At 1,250 captures that's ~360 wasted extractions. **Fix: pre-LLM gate: body < ~15 words, single-char bodies, and repetition-loop detection (the "thank you for watching" hallucination signature) → auto-noise, never extracted.** Expect the gate to catch ~80% of noise for near-zero cost.

### 5. Duplicate triage doesn't exist
Three phenomena need three treatments and currently get one:
| Type | Example | Correct handling |
|------|---------|------------------|
| Same file twice | omi 07-03-1137 .clean + raw | File-level dedup pre-extraction (content hash) |
| Same speech, two devices | 07-06 bake-off OMI+Plaud pairs | Merge by timestamp-proximity + similarity; keep both transcripts for quality comparison, count ONE event |
| Same idea, different days | Captain's Log × 15 | NEVER dedup — this IS the recurrence signal |

The weave summary correctly warns the bake-off inflates counts; at scale nobody will remember to correct manually.

### 6. Entity names polluted by transcription
"Dart Factory", "Romy", "Kubernetes extension", "chiber" all appear in entities/filenames. Entity-based queries and brain promotion will silently fork on these. **Fix: entity normalization dictionary applied at extraction time — the SAME dictionary Captain's Log's vocabulary feature (CL-08) needs. Build once.**

## Scale math and batching

- This slice: 102 records → ~60KB of extraction JSON; weave comfortably fit one context. 1,250 records ≈ 12×: single-pass weave is impossible and shouldn't be attempted.
- **Recommended design**: 2-week slices (~100-130 records — this run proves the size works) → per-slice weave → persistent state carried forward (thread registry, loop registry, embedding index) → cross-slice merge stage (does not exist yet; must be designed BEFORE the full run, it is the new hard part).
- Extraction batch size: ~50-70 records per extraction call kept quality high here; don't exceed.
- Cost control: the noise gate (#4) + skipping re-extraction of already-processed files (manifest with content hashes) matter more than model choice.

## Prior-run invariants to keep

1. **Stage-boundary assertions**: miner fails loudly on 0 records; weaver/extractor refuse `[]`. (The prior stub run proved this failure mode is real — 9 confidently-empty artifacts were written from nothing.)
2. **Inter-stage manifest.json**: record count, date window, source glob, schema version, content hashes.
3. **Provenance**: no citation, no claim.

## Tune-before-full-run checklist (ordered)

1. **P0** — Thread registry: seed controlled `area/thread` list from 01-thread-atlas; add alias table (linda → challenge-dv).
2. **P0** — Pre-LLM noise gate + file-level dedup (hash) + cross-device pair merge.
3. **P0** — Entity dictionary (share with CL-08).
4. **P1** — Loop registry with IDs/lifecycle; migrate this run's ~70 items as the seed.
5. **P1** — Global embedding index over essences; retire fingerprint-as-clustering (keep as label).
6. **P1** — Design the cross-slice merge stage.
7. **P2** — Tighten `kind`: `decision` requires `decided:`; consider adding `plan` (distinct from `direction`) since "planned but never started" proved to be a key signal.
8. **P2** — Controlled `target` routing table for actions (maps to the 6 harvest groups used in 10-tickets.md).

## Bottom line

Yes to the shape — extraction/weave/harvest with 2-week slices is the right machine, and this run's outputs are directly usable. No to scaling naively: without the thread registry, loop IDs, noise gate, and embedding index, the 6-month run would produce fragmented threads, inflated counts, and ~$-and-hours wasted extracting silence. One more 2-week calibration slice AFTER items 1-4 land would de-risk the full run almost entirely.

---

*Calibration run 2026-07-13 — real corpus, 102 records (66 OMI, 36 Plaud). Replaces the zero-record stub; prior P0 (silent empty hand-off) resolved upstream and retained here as a permanent invariant.*
