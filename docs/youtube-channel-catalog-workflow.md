# NEXT-WORKFLOWS — AI-TLDR pipeline backlog

Captured 2026-05-30. These are NOT done. Parked for a later "best technique" conversation.

---

## A. Transcript ingestion (the bigger, separate job)

> Quoted from the session, verbatim, so the rationale isn't lost:
> *"If you want transcripts, that's a separate, bigger job (yt-dlp can pull auto-captions
> per video — that's where real disk/time cost would start). We haven't done it and
> nothing here depends on it."*

**What it is:** pull the spoken-word transcript (auto-captions) for each video, not just
the metadata card. This is the first phase that actually costs disk + time + tokens at scale.

**Why it's separate from the enrich run we did:**
- The enrich run touched **metadata only** (~220 KB for 25 videos, zero media files).
- Transcripts are per-video text pulls — 324 of them — plus a cleaning pass, plus
  (optionally) summarisation/chaptering. Different cost class entirely.

**Rough shape (to be designed, not committed):**
1. `fetch-captions` — `yt-dlp --write-auto-subs --skip-download --sub-format vtt`
   per video → `transcripts/<youtubeId>.vtt`. Inline (network), not in a sub-agent.
2. `clean` — strip VTT timestamps/dedupe lines → `transcripts/<youtubeId>.txt`.
3. `enrich-from-transcript` — fan-out: better category, real summary, chapter markers,
   key-tool extraction, quotable lines. One agent per transcript.
4. `assemble` — fold transcript-derived fields back into `business-data.json`
   (as **generated**, with provenance back to the caption source).

**Open technique questions for the later conversation:**
- Auto-captions vs. uploaded captions vs. Whisper re-transcription — quality vs. cost.
- Where transcripts live (in-repo vs. external store) given 324 × multi-KB text.
- Whether transcript enrichment REPLACES or AUGMENTS the metadata-only category/summary.
- Idempotency: skip videos whose `transcripts/<id>.txt` already exists (same Layer-2
  driver pattern as the enrich workflow — see `workflows/aitldr-enrich.js` header).

**Status:** NOT STARTED. No code, no data. Discuss best technique first.

---

## B. Scale the existing enrich run to the full channel (~324)

**What it is:** the exact pipeline we already proved on 25, run over every video.
No new technique — just `subset: all` + a longer fetch + a wider fan-out.

**Steps (unchanged from the proving pass):**
1. Inline fetch: `yt-dlp --skip-download` over `@AITLDR/videos` (no `--playlist-end`)
   → overwrite `raw/videos.jsonl` (~324 lines).
2. Driver computes idempotent line-list (skip youtubeIds already in `enriched/`).
3. Run `workflows/aitldr-enrich.js` over that line-list.
4. Re-assemble `business-data.json` + `report.md`.

**Cost estimate (extrapolated from the 25-run):** ~830 K tokens for 25 → order of
~10 M tokens for 324; ~57 s wall for 25 (capped at ~14 concurrent) → a few minutes
for 324. Still in-session, still no metered billing, still trivial disk (metadata only).

**Status:** IN PROGRESS (paced). 65/165 enriched. See lesson C below.

---

## C. LESSON — wide schema fan-outs hit a burst throttle (~40)

**Observed 2026-05-30:** a single 100-wide enrich fan-out (140 agents, ~14 concurrent)
succeeded for the first ~40 then shed the remaining 100 — all failing identically with
"subagent completed without calling StructuredOutput." Not data, not the script (the
same script enriched 65 cleanly); it's cumulative burst pressure on the schema/StructuredOutput
path tripping a rate limit around the 40-completion mark.

**The robust pattern (now in use):**
- **Batch size ~20** per run (half the safe ceiling).
- **Pace one batch every 30 min** via in-session `ScheduleWakeup` (NOT headless cron —
  that path is metered billing, which we avoid; see Watchtower trigger-architecture note).
- **Idempotent skip** — recompute todo from `enriched/` each run; never reprocess.
- **Persist between batches** — write `enriched/<slug>.json` before the next batch so a
  throttle costs at most one batch.
- **Self-terminate** — when todo is empty, assemble and stop re-arming.
- **Per-agent retry once** — a lone schema miss retries without re-running the batch.

100 remaining ÷ 20 = ~5 runs ≈ 2.5 h, unattended, in-session, no metered billing.
Trade-off: session must stay alive across the window (in-session wakeups die on quit).
