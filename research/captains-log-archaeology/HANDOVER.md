# Captain's Log Archaeology — Handover

**Status as of 2026-07-13/14:** extraction COMPLETE + durable; deterministic merge DONE; LLM narrative synthesis BLOCKED on the monthly spend limit (resets next month).

This doc is self-contained. Absolute paths throughout. No chat access required to resume.

---

## What this is

A one-off analysis harness that reads David's 6 months of voice captures (OMI + Plaud, the "Captain's Log" corpus) and turns 1,250 opaque transcripts into a dated, threaded, deduped map — threads over time, recurring ideas, open loops, and recency/supersession-aware tickets. Built 2026-07-13 to spend the remaining Fable-5 usage on something durable. **This is throwaway tooling, NOT part of the Captain's Log app** (`localhost:7100`, untouched).

## Source corpus

- `/Users/davidcruwys/dev/raw-intake/omi/*.md` (1,215) + `/Users/davidcruwys/dev/raw-intake/plaud/*.md` (37) = 1,250 captures, 2026-01-09 → 2026-07-13.

## What exists on disk (all under `/Users/davidcruwys/dev/ad/apps/dark-factory/research/captains-log-archaeology/`)

- `calibration-2026-07-13/` — run-1 (v1, proved the pipeline works) + `v2/` (proved the 4 fixes: thread registry, entity dict, noise short-circuit, loop registry).
- `full-run-2026-07-13/`
  - `records/*.jsonl` — **THE ASSET: 1,250 extracted records** (84 files). Each: file, date, source, thread_id, kind, essence, entities, actions[{text,target}], loop{is_open,label}, fingerprint. Cost ~11.3M Fable tokens. Durable.
  - `manifest-newest-first.txt` + `batches/` — the newest-first processing order + 84 batch manifests (regenerable).
  - `00-EXECUTIVE-SUMMARY.md`, `loop-registry.md` (593 loops), `tickets-by-target.md` (1,342 actions / 491 targets) — **written by the deterministic Python merge** (`/private/tmp/.../scratchpad/reduce.py`; copy is inlined below-ish — see repo history).

## Headline findings (6-month, deterministic)

- Heaviest threads: **SupportSignal 121, fleet-infra 114, content-production 108, ai-meetups 82, skills-tooling 77, brains-knowledge 57** (personal-noise 226 discarded). NOTE: Captain's Log / Dark Factory dominated only the LAST FORTNIGHT — the 6-month centre of gravity is client + infra + content. The recent obsession is recency bias.
- 593 distinct open loops (64 live, last-seen ≥ 2026-06-22); 1,342 actions across 491 targets (119 in the last 3 weeks).
- Ticket volume by target: Agent Workflow Builder 95, SupportSignal 58, Signal Studio 48, AngelEye 34, brains repo 31.
- ⚠️ **Time-critical real-world loop (from v2):** Challenge DV retainer proposal — $2,750 incl GST (supersedes $3,300), start 15 July, contact name "Lisa/Lindy" UNVERIFIED. A David action, not the pipeline's.

## Pipeline scripts

- v1: `/Users/davidcruwys/.claude/projects/-Users-davidcruwys-dev-ad-brains/0b38cc1e-0ebd-45e3-aa9f-9193546048be/workflows/scripts/captains-log-archaeology-calibration-wf_b4eadc2c-64a.js`
- v2 (registry+entities+noise+loops): `/private/tmp/claude-501/-Users-davidcruwys-dev-ad-brains/0b38cc1e-0ebd-45e3-aa9f-9193546048be/scratchpad/cl-archaeology-v2.js`
- v3 (full run, map-reduce, durable): `/private/tmp/claude-501/-Users-davidcruwys-dev-ad-brains/0b38cc1e-0ebd-45e3-aa9f-9193546048be/scratchpad/cl-archaeology-v3-full.js`
- deterministic reducer (no model spend): `/private/tmp/claude-501/-Users-davidcruwys-dev-ad-brains/0b38cc1e-0ebd-45e3-aa9f-9193546048be/scratchpad/reduce.py`

> `/private/tmp` is ephemeral — if these matter, copy them into the repo before relying on them. `reduce.py` is the important one; re-paste it from this session or rebuild from `records/`.

## To finish the LLM narrative synthesis next month (when the limit resets)

The extraction agents are cached in the workflow run. Resume replays them free and only re-runs the failed merge agents live:

```
Workflow({
  scriptPath: ".../scratchpad/cl-archaeology-v3-full.js",
  resumeFromRunId: "wf_c5f0f651-fa6",
  args: {"runDir":"/Users/davidcruwys/dev/ad/apps/dark-factory/research/captains-log-archaeology/full-run-2026-07-13","batchCount":84}
})
```

That produces the per-thread narrative atlas, the LLM loop-registry (status/priority), the recency/supersession-aware ticket lists, and `00-EXECUTIVE-SUMMARY.md` prose. The deterministic versions already on disk are the fallback if you never re-run.

## Known issues / fixes before any future full run

1. **args arrive JSON-stringified** — every script needs `const A = typeof args === 'string' ? JSON.parse(args) : args`. (Cost one silent-empty run + one instant fail.)
2. **`fingerprint` was misused** — readers put the capture's file-hash there instead of a topic phrase, so fingerprint-based recurrence is useless. Recurrence currently rides on `loop.label`. Fix the prompt.
3. **Cross-slice identity drift** — thread/loop ids are re-derived per run, so ids aren't stable across separate runs. For incremental/append use, persist `threads.yaml` / `loops.yaml` and feed them in. (v2 CALIBRATION-NOTES has the spec.)
4. **`new:` thread sprawl** — 26 seeded threads became 48 as readers coined `new:` labels for older material; a reconcile pass should fold these back.

## Related session work (committed alongside)

- Lexi brain-health sweep (brains repo): link-health 92.4%→100%, file_count 96/96 synced, `validate_tags.py` false-positive FIXED (appydave-plugins), proposals in `/Users/davidcruwys/dev/ad/brains/LEXI-PROPOSALS-2026-07-13.md` (staleness relabels, 3 brain revives incl. ansible, negative-knowledge gaps) — awaiting David's review.
