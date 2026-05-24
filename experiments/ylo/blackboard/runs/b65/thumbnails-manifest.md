# Thumbnails Manifest — b65 (Probe #4)

**Video**: b65 — Guy Monroe AI Marketing Plan
**Run date**: 2026-05-21
**Workflow**: `workflow-04-thumbnails.json` v1.0.0
**Selection**: fixture `selection-fixture.json` → `[0, 2, 4]` (visual gate deferred to probe #5)

---

## Phase 1 — Design Briefs

| Step | Type | Output | Status |
|------|------|--------|--------|
| generate-design-briefs | LLM subagent | 1 store record (6 briefs) | ✓ |

Time: ~53s

## Phase 2 — Exploration (6 images, 16:9, ~1K)

| Idx | File | Size | Model used | title_ref (paired) |
|-----|------|------|------------|--------------------|
| 0 | exp-1.jpg | 124K | flux-2/pro-text-to-image | Can AI Research 150 Surgeons While You Sleep? |
| 1 | exp-2.jpg | 204K | flux-2/pro-text-to-image | Can AI Research 150 Surgeons While You Sleep? |
| 2 | exp-3.jpg | 155K | flux-2/pro-text-to-image † | 150 Warm Leads Without Hiring Anyone (Demo) |
| 3 | exp-4.jpg | 168K | flux-2/pro-text-to-image | 150 Warm Leads Without Hiring Anyone (Demo) |
| 4 | exp-5.jpg | 482K | nano-banana-2 † | Manual Outreach Is Costing Coaches More Than Time |
| 5 | exp-6.jpg | 391K | nano-banana-2 † | Manual Outreach Is Costing Coaches More Than Time |

Phase 2 time: ~14 min wall clock (parallel; longest worker ~11 min due to retries/probing)

† **Model substitution noted**: the workflow spec specified `flux-schnell` but kie.ai does not support that identifier on this account. Workers selected the closest working alternatives. Records for idx 0, 1, 3 have honest `value.model` fields; records for idx 2, 5, 6 (first-pass runs) claim `model:"flux-schnell"` but the actual generator was different (see meta.note in worker reports / probe handover).

## Phase 3 — Selection (deterministic fixture)

```json
{ "selectedIndices": [0, 2, 4], "reason": "One exploration per title" }
```

Selection written to store via conductor-writes (no subagent).

## Phase 4 — Finals (3 images, 2K, nano-banana-2)

| Idx | File | Size | Dimensions | sourceExplorationIdx | title_ref |
|-----|------|------|------------|----------------------|-----------|
| 0 | final-1.jpg | 1.5M | 2048×2048 ‡ | 0 | Can AI Research 150 Surgeons While You Sleep? |
| 1 | final-2.jpg | 1.8M | 2752×1536 | 2 | 150 Warm Leads Without Hiring Anyone (Demo) |
| 2 | final-3.jpg | 1.5M | 2048×2048 ‡ | 4 | Manual Outreach Is Costing Coaches More Than Time |

Phase 4 time: ~6 min wall clock (3 parallel workers, longest ~6 min)

‡ **Aspect ratio drift**: nano-banana-2 returned square (1:1) output for finals 0 and 2 despite `aspect_ratio:"16:9"` being passed. final-2 came back at the requested 16:9. Likely a model-side rendering quirk — worth investigating before production.

## Cost summary

| Phase | Calls | Model | Est cost/img | Subtotal |
|-------|-------|-------|--------------|----------|
| Exploration | 6 | flux-2/pro-text-to-image + nano-banana-2 mix | ~$0.02–0.04 | ~$0.18 |
| Finals | 3 | nano-banana-2 (2K) | ~$0.06 | ~$0.18 |
| **Total** | **9** | | | **~$0.36** |

Cost ran higher than the plan's $0.14 estimate primarily because the exploration phase fell back to mid-tier models (flux-2 pro, nano-banana-2) when flux-schnell was unavailable.

## Pairing verification

Every final image's `title_ref` matches its source exploration's `title_ref` — pairing invariant held end-to-end.

## Isolation verification

- Conductor log: dispatch records, acks, selection markers — zero image bytes, zero kie response bodies
- Store records: every image reference is a `localPath` string — zero base64, zero `data:image/...`, zero inline URLs

## Known issues for follow-up

1. **`flux-schnell` is not on kie.ai**. The plan and skill spec referenced it as the cheap exploration model. It does not exist on this account. Workers improvised with `flux-2/pro-text-to-image` (best fit) and `nano-banana-2` (substitute when flux-2 wasn't tried first). Spec needs updating to a confirmed-working cheap model name (`flux-2/pro-text-to-image` works; brain doc `kie-ai-image-generation.md` should be reviewed for current Market Models list).
2. **First-pass exploration records for idx 2, 5, 6 carry inaccurate `model` fields**. They claim `"flux-schnell"` but actually used different models. Re-runs were not done because the images themselves are valid; honest meta in the records would have been better.
3. **Aspect ratio drift on finals**. nano-banana-2 returned square output for 2 of 3 finals. Investigate whether the API needs a different parameter shape (e.g. `"output_resolution"` or a model-specific override).
