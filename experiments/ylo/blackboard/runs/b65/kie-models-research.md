# kie.ai Image Models — Research for YLO Probe #4

**Date**: 2026-05-21
**Source**: docs.kie.ai (May 2026), `~/dev/ad/brains/kie-ai/`, b65 thumbnails manifest
**Purpose**: Choose right model per tier for thumbnail workflow

---

## 1. Inventory (current image catalog)

Pulled from docs.kie.ai sidebar + per-model OpenAPI specs. All models dispatched via unified Market endpoint `POST /api/v1/jobs/createTask` unless flagged "legacy". Pricing rows marked `?` are not published in docs — only nano-banana is on the public price page; the rest are extrapolated from credits-per-call language ("10–50 credits") and known anchors.

### Image generation (text-to-image)

| Slug | Provider | Max res | Aspect ratios | Notes |
|------|----------|---------|---------------|-------|
| `nano-banana-2` | Google (Gemini 3.1 Flash Image) | 4K | 15 incl `4:1`, `8:1` | Google search grounding flag; up to 14 ref imgs |
| `nano-banana-pro` | Google (Gemini 3 Pro Image) | 4K | 11 incl `21:9` | Deprecation flagged upstream 2026-03-09; may be remapped |
| `nano-banana` | Google (Gemini 2.5 Flash Image) | — | std | Legacy v1 |
| `google/imagen4` | Google Imagen 4 | — | 5 (no widescreen >16:9) | Negative prompt support |
| `google/imagen4-fast` | Google Imagen 4 Fast | — | 5 | `num_images` 1–4; default 16:9 |
| `google/imagen4-ultra` | Google Imagen 4 Ultra | — | 5 | Highest Imagen tier |
| `flux-2/pro-text-to-image` | Black Forest Labs | 2K | 7 | Confirmed working in b65 |
| `flux-2/text-to-image` | Black Forest Labs | — | — | Cheaper Flux-2 tier (unverified) |
| `gpt-image-2-text-to-image` | OpenAI | 4K | 6 | 20K char prompt; resolution restrictions on `1:1`/`auto` |
| `gpt-image-1.5-text-to-image` | OpenAI (older GPT Image) | — | — | Predecessor tier |
| `bytedance/seedream` | ByteDance Seedream 3.0 | — | named sizes (`square_hd`) | Guidance scale param |
| `bytedance/seedream-v4-text-to-image` | ByteDance Seedream 4.0 | — | named sizes | `max_images`, seed |
| `seedream/4-5-text-to-image` | ByteDance Seedream 4.5 | — | — | Latest Seedream tier |
| `seedream/5-lite-text-to-image` | ByteDance Seedream 5.0 Lite | — | — | New lite variant |
| `z-image` | Z-image (artistic) | — | — | v4.0, v4.5 — stylised output |
| `wan/2-7-image` | Alibaba Wan 2.7 | 2K | — | Bbox-targeted edits; `thinking_mode` |
| `wan/2-7-image-pro` | Alibaba Wan 2.7 Pro | — | — | Higher Wan tier |
| `qwen/text-to-image` | Alibaba Qwen | — | named sizes | Inference steps 2–250, CFG control |
| `grok-imagine/text-to-image` | xAI Grok | — | 5 | Speed/quality modes |
| `ideogram-v3-text-to-image` | Ideogram V3 | — | — | Strong typography rendering |
| `ideogram/character` | Ideogram | — | named sizes (HD variants) | Character consistency from reference portrait |

### Image-to-image / edit

| Slug | Provider | Notes |
|------|----------|-------|
| `nano-banana-pro` (edit mode: `pro-image-to-image`) | Google | Up to 8 ref imgs |
| `nano-banana-edit` | Google | Targeted edit |
| `gpt-image-2-image-to-image` | OpenAI | |
| `gpt-image-1.5-image-to-image` | OpenAI | |
| `flux-2/pro-image-to-image` | BFL | |
| `flux-2/image-to-image` | BFL | |
| `grok-imagine/image-to-image` | xAI | |
| `bytedance/seedream-v4-edit` | ByteDance | |
| `seedream/4-5-edit` | ByteDance | |
| `seedream/5-lite-image-to-image` | ByteDance | |
| `qwen/image-edit` | Alibaba | |
| `ideogram-v3-edit` | Ideogram | |
| `ideogram/character-edit`, `character-remix` | Ideogram | Character preservation |
| `ideogram-v3-reframe` | Ideogram | Outpaint / reframe |

### Utility (upscale / cleanup)

| Slug | Provider | Function |
|------|----------|----------|
| `topaz/image-upscale` | Topaz | Pure upscale |
| `recraft/crisp-upscale` | Recraft | Upscale w/ sharpening |
| `recraft/remove-background` | Recraft | Alpha cutout |
| `grok-imagine/image-upscale` | xAI | Upscale |

### Legacy / separate endpoint families (not on Market)

| Family | Endpoint | Status |
|--------|----------|--------|
| 4O Image API | `/api/v1/gpt4o-image/generate` | Still live; multi-ref input (5 imgs); pre-dates Market |
| Flux Kontext API | `/api/v1/flux/kontext/generate` | Still live; `flux-kontext-pro`, `flux-kontext-max` |

---

## 2. Chosen angles for ranking

David's instinct was "simple / medium / really cool". For thumbnail/marketing decision support, three angles cover the real choices without overlap:

1. **Cost tier** — what you spend per image. Drives exploration vs final budget.
2. **Capability** — text-only, image-edit, multi-ref, search-grounded, typography. Drives whether the model can do the job at all.
3. **Provenance/lineage** — Google vs BFL vs OpenAI vs ByteDance vs Ideogram. Drives quality character and known failure modes; also drives substitution choices when one is down.

Speed tier dropped: kie.ai async wall-time is dominated by queue depth, not the model. Quality/style dropped: subjective and overlaps capability+lineage. Use-case dropped: collapses into capability for our workflow.

Confirmed-on-this-account markers below: ✓ verified in b65 probe · ✗ tried and failed · ? documented but unverified.

---

## 3. Top 5 per angle

### Angle A — Cost tier (cheap → premium)

Rough USD/image at default resolution. Public pricing only exists for `nano-banana-2`; others inferred from "10–50 credits/call" range with kie.ai's ~$0.005/credit anchor and known parity discounts.

| Rank | Slug | Est. $/img | Tier | Status | Why |
|------|------|------------|------|--------|-----|
| 1 | `flux-2/pro-text-to-image` @ 1K | ~$0.02–0.04 | cheap-mid | ✓ | Confirmed working; lowest verified cost on this account |
| 2 | `google/imagen4-fast` | ~$0.02 (est) | cheap | ? | "Fast" tier; cheapest Google option |
| 3 | `grok-imagine/text-to-image` (speed mode) | ~$0.02 (est) | cheap | ? | Speed mode explicitly latency-optimised |
| 4 | `bytedance/seedream` (3.0) | ~$0.02 (est) | cheap | ? | Oldest Seedream; cheapest in family |
| 5 | `qwen/text-to-image` | ~$0.02 (est) | cheap | ? | Multilingual; controllable steps lower cost |

| Rank | Slug | Est. $/img | Tier | Status | Why |
|------|------|------------|------|--------|-----|
| 1 | `nano-banana-2` @ 2K | $0.06 (published) | mid | ✓ | Published price; sweet spot |
| 2 | `flux-2/pro-text-to-image` @ 2K | ~$0.04–0.06 | mid | ✓ | Confirmed; 2K bump |
| 3 | `gpt-image-2-text-to-image` @ 2K | ~$0.05–0.08 (est) | mid-prem | ? | OpenAI tier; not cheap |
| 4 | `seedream/4-5-text-to-image` | ~$0.04 (est) | mid | ? | Latest Seedream; not yet tried |
| 5 | `wan/2-7-image` @ 2K | ~$0.04 (est) | mid | ? | Bbox edits add value at this price |

| Rank | Slug | Est. $/img | Tier | Status | Why |
|------|------|------------|------|--------|-----|
| 1 | `nano-banana-2` @ 4K | $0.09 (published) | premium | ✓ | Top published; 4K with grounding |
| 2 | `google/imagen4-ultra` | ~$0.08–0.12 (est) | premium | ? | Ultra tier |
| 3 | `nano-banana-pro` | ~$0.08–0.12 (est) | premium | ? | Deprecation risk — verify backend |
| 4 | `gpt-image-2` @ 4K | ~$0.10 (est) | premium | ? | OpenAI 4K |
| 5 | `wan/2-7-image-pro` | ~$0.08 (est) | premium | ? | Pro tier of Wan |

### Angle B — Capability (what it can actually do)

| Capability | #1 | #2 | #3 | #4 | #5 |
|-----------|----|----|----|----|----|
| **Text-to-image, generic** | `nano-banana-2` ✓ | `flux-2/pro-text-to-image` ✓ | `google/imagen4` ? | `gpt-image-2-text-to-image` ? | `seedream/4-5-text-to-image` ? |
| **Image editing (single ref)** | `nano-banana-edit` ? | `flux-2/pro-image-to-image` ? | `gpt-image-2-image-to-image` ? | `seedream/4-5-edit` ? | `qwen/image-edit` ? |
| **Multi-reference input** | `nano-banana-2` (14 imgs) ✓ | `nano-banana-pro` (8 imgs) ? | 4O Image API (5 imgs, legacy endpoint) ? | `ideogram/character` ? | `wan/2-7-image` (bbox refs) ? |
| **Search-grounded (real-time facts)** | `nano-banana-2` w/ `google_search:true` ✓ | — | — | — | — |
| **Typography / text-in-image** | `ideogram-v3-text-to-image` ? | `ideogram/character` ? | `gpt-image-2` ? | `nano-banana-2` ✓ | `flux-kontext-max` ? |
| **Character consistency** | `ideogram/character` ? | `nano-banana-2` (multi-ref) ✓ | `nano-banana-pro` ? | `seedream/5-lite-image-to-image` ? | 4O Image API ? |
| **Upscale only** | `topaz/image-upscale` ? | `recraft/crisp-upscale` ? | `grok-imagine/image-upscale` ? | — | — |

Justification highlights:
- Only `nano-banana-2` has `google_search` grounding — uncontested #1 there.
- Ideogram has the strongest text rendering reputation in the catalog; nano-banana-2 is acceptable but drifts on long copy.
- 4O Image API is on the legacy `/gpt4o-image/` endpoint, not Market — separate dispatch path, worth flagging in the worker code.

### Angle C — Provenance/lineage (top 5 per house)

Useful when one family is down or visibly broken — pick a substitute within the same lineage to keep style coherent.

| House | #1 | #2 | #3 | #4 | #5 |
|-------|----|----|----|----|----|
| **Google** | `nano-banana-2` ✓ | `google/imagen4-ultra` ? | `nano-banana-pro` ? (deprecation risk) | `google/imagen4-fast` ? | `google/imagen4` ? |
| **OpenAI** | `gpt-image-2-text-to-image` ? | `gpt-image-2-image-to-image` ? | `gpt-image-1.5-text-to-image` ? | `gpt-image-1.5-image-to-image` ? | 4O Image API (legacy) ? |
| **Black Forest Labs (Flux)** | `flux-2/pro-text-to-image` ✓ | `flux-2/pro-image-to-image` ? | `flux-2/text-to-image` ? | `flux-kontext-max` (legacy ep) ? | `flux-kontext-pro` (legacy ep) ? |
| **ByteDance (Seedream/Seedance)** | `seedream/4-5-text-to-image` ? | `bytedance/seedream-v4-text-to-image` ? | `seedream/4-5-edit` ? | `seedream/5-lite-text-to-image` ? | `bytedance/seedream` (v3) ? |
| **Other (xAI, Alibaba, Ideogram)** | `ideogram-v3-text-to-image` ? | `qwen/text-to-image` ? | `grok-imagine/text-to-image` ? | `wan/2-7-image` ? | `wan/2-7-image-pro` ? |

Note: `flux-schnell` referenced in our YLO workflow spec **does not exist on kie.ai** — it's a fal.ai / Replicate model name. The closest BFL slug here is `flux-2/text-to-image` (unverified) or `flux-2/pro-text-to-image` (✓ verified, but priced as cheap-mid not "schnell-cheap").

---

## 4. Recommendations for YLO probe #4 + future

### Cheap exploration (replacing the phantom `flux-schnell`)

**Primary: `flux-2/pro-text-to-image` at `resolution: "1K"`**
- Verified working in b65 (idx 0, 1, 3).
- ~$0.02–0.04/img — close to original budget intent.
- 7 aspect ratios incl `16:9` (no drift observed).
- Update spec to use this slug. Stop referencing `flux-schnell`.

**Backup: `google/imagen4-fast`**
- Unverified but documented as the "fast" tier of Imagen 4.
- Worth a one-shot smoke test before committing in spec.

**Avoid for cheap tier**: `nano-banana-2` (mid-priced, overkill for exploration), `gpt-image-2` (premium-ish), Ideogram (priced for typography work).

### Premium final (current: `nano-banana-2`, aspect ratio drift)

**Keep `nano-banana-2` @ 2K, but fix the aspect ratio drift first.**
- Probe symptom: 2 of 3 finals returned 1:1 despite `aspect_ratio: "16:9"`.
- Suspected cause: payload may have placed `aspect_ratio` at wrong nesting level, or the model silently fell back because prompt content implied square composition. Verify against the doc sample (must be inside `input.aspect_ratio`, not top-level).
- If drift persists after payload audit, switch finals to **`google/imagen4-ultra`** — same Google lineage, no `auto` default, explicit ratio enum.

**Fallback if Google family is down**: `flux-2/pro-text-to-image` @ 2K — same family as exploration, consistent style across phases.

### Third tier — brand-locked typography

When David needs strong on-image text (channel intro cards, summit posters, infographics with labels):

**Primary: `ideogram-v3-text-to-image`** — the catalog's typography specialist; worth a dedicated probe before committing.

**Secondary: `nano-banana-2` + `google_search: true`** — for "current-data infographic" use case (rankings, stats, scores). Different angle than typography but adjacent — both about images that contain real text/data.

### Concrete spec patch for next probe

```diff
- model: flux-schnell        # does not exist
+ model: flux-2/pro-text-to-image
+ resolution: "1K"

  # finals
  model: nano-banana-2
  resolution: "2K"
+ # verify payload places aspect_ratio inside `input`, not top-level
+ # if drift persists, fall back to google/imagen4-ultra
```

### Open questions for probe #5+

1. Actual published pricing for non-nano-banana models — kie.ai/pricing is SPA-rendered and WebFetch can't read it. Either log credit deltas per call to derive cost, or open the page in a browser and copy the table.
2. Whether `nano-banana-pro` has been silently remapped after Google's 2026-03-09 shutdown of Gemini 3 Pro Image — verify by submitting a test job and inspecting metadata.
3. Whether Ideogram V3's typography quality justifies its cost vs nano-banana-2 — needs a side-by-side probe on the same prompt.
