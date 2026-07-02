# Drawn View — Generation Provenance

Design 10 (Constellation Map), Slice 2. The HTML render (`../index.html`) is the precise, data-driven
view — every app, flow, and channel from `mochaccino/data/constellation.json`, schema → data → view.
This poster is the deliberate opposite: the **coarse, absorbable at-a-glance view**. Image models garble
dense small text, so the brief was 3 bands + ~8 load-bearing app names only, large type, nothing else.

- **Date**: 2026-07-02
- **API**: kie.ai, `POST /api/v1/jobs/createTask` → poll `GET /api/v1/jobs/recordInfo?taskId=...`
- **Model**: `nano-banana-2` (Gemini 3.1 Flash Image)
- **Params**: `aspect_ratio: 16:9`, `resolution: 4K`, `output_format: png`
- **Calls made**: 4 (of a ≤5 budget) — all 4 succeeded on the first attempt, no retries needed.
- **Layer mapping used** (from constellation.json layers, collapsed to 3 bands):
  - DATA = data-source + data-plane → **OMI** (omi-ingester), **CORTEX**, **BLACKBOARD** (blackboard-mcp)
  - SURFACES = surface-core + surface-utility + surface-prototyping → **ANGELEYE**, **APPYRADAR**, **WATCHTOWER**, **MOCHACCINO**
  - HOST = host → **KYBERAGENT** (kbde-kyberagent)
  - (engine/business/own-world/parked/dead layers excluded — out of scope for the at-a-glance poster)

---

## Variant A — "drawn-blueprint" (hand-drawn technical sketch)

**Prompt (used for both v1 and v2, same text, independent generations):**

> A hand-drawn technical blueprint poster, 16:9 landscape. Warm cream parchment paper background
> (#faf5ec), dark warm-brown ink line-work (#342d2d) for every diagram line and border, like an
> architects hand sketch, not a slick vector render. Exactly THREE horizontal rectangular bands
> stacked bottom to top, each band outlined in brown ink with one large bold hand-lettered uppercase
> label centered in the band: bottom band labeled DATA, middle band labeled SURFACES, top band labeled
> HOST. Between DATA and SURFACES, and between SURFACES and HOST, draw large upward-pointing
> hand-drawn arrows in warm gold (#ccba9d) showing flow moving upward through the bands. Inside the
> DATA band place three large bold hand-lettered word labels evenly spaced left to right: OMI, CORTEX,
> BLACKBOARD. Inside the SURFACES band place four large bold hand-lettered word labels evenly spaced
> left to right: ANGELEYE, APPYRADAR, WATCHTOWER, MOCHACCINO. Inside the HOST band place one large bold
> hand-lettered word label centered: KYBERAGENT, highlighted in bright yellow (#ffde59) so it reads as
> the biggest architectural anchor. Small hand-drawn factory-gear and constellation-star sketch motifs
> may decorate the corners and margins sparingly, never obscuring or crowding the labels. CRITICAL TEXT
> RULES: all text must be LARGE, BOLD, and MINIMAL. Spell each word EXACTLY as given above, nothing
> else — no additional text, no small print, no paragraph text, no extra labels beyond DATA, SURFACES,
> HOST, OMI, CORTEX, BLACKBOARD, ANGELEYE, APPYRADAR, WATCHTOWER, MOCHACCINO, KYBERAGENT. Do not invent
> or add any other words or numbers. Overall mood: warm, hand-crafted, confident blueprint sketch,
> architecture first, decoration second. Absolutely no cool blue, teal, or purple as a dominant color —
> keep the palette warm brown, cream, gold, and yellow throughout. Never place muddy amber/orange as a
> flat fill directly on the dark brown ink color.

| File | Task ID | Verdict | Notes |
|---|---|---|---|
| `drawn-blueprint-v1.png` | `886a3a77d5aaaa14ceef24e823604a96` | **KEEP (alternate)** | Correct layer order, all 11 labels spelled correctly, yellow KYBERAGENT highlight reads well. Band heights slightly uneven (HOST band has more empty space) and gear/star motifs sit a touch close to the top-right corner text — minor, not disqualifying. |
| `drawn-blueprint-v2.png` | `5e5de9b4d2ddf2d7177fb9e5d46aff8c` | **KEEP — chosen poster** | Same prompt, independent generation. Cleanest composition of all 4: even band heights, evenly spaced labels, no motif crowds text, correct bottom→top DATA/SURFACES/HOST order, all text spelled exactly as specified. Best match to the brief's "hand-drawn blueprint-sketch" primary aesthetic direction. |

---

## Variant B — "warm-poster" (flat modern poster)

**Prompt (used for both v1 and v2, same text, independent generations):**

> A clean warm technical poster illustration, 16:9 landscape, in a warm confident brand style. Warm
> cream background (#faf5ec) with dark warm-brown (#342d2d) structural elements, warm gold (#ccba9d)
> secondary accents, and bright yellow (#ffde59) as the single vivid highlight color. Exactly THREE
> solid horizontal bands stacked bottom to top like factory floors, separated by clean warm-brown
> dividing lines, each band carrying one large bold uppercase sans-serif label centered in the band:
> bottom band labeled DATA, middle band labeled SURFACES, top band labeled HOST. Large upward-pointing
> arrows in bright yellow rise from the DATA band through the SURFACES band into the HOST band, showing
> energy and data flowing upward through the factory. Inside the DATA band place three large bold
> labels evenly spaced left to right: OMI, CORTEX, BLACKBOARD. Inside the SURFACES band place four
> large bold labels evenly spaced left to right: ANGELEYE, APPYRADAR, WATCHTOWER, MOCHACCINO. Inside
> the HOST band place one large bold centered label: KYBERAGENT. A subtle constellation-of-stars motif
> and a small stylised factory silhouette may appear faintly in the background of the HOST band only,
> decorative and never overlapping or obscuring any text. CRITICAL TEXT RULES: text must be LARGE and
> MINIMAL, spelled EXACTLY as given above, nothing else — no other words, no fine print, no captions, no
> extra labels beyond DATA, SURFACES, HOST, OMI, CORTEX, BLACKBOARD, ANGELEYE, APPYRADAR, WATCHTOWER,
> MOCHACCINO, KYBERAGENT. Style: confident modern technical poster, flat warm color blocks, no
> gradients, no glassmorphism, no cool blue, teal, or purple as a dominant color. Do not use muddy
> amber/orange as a flat fill on the dark brown background — yellow is the only bright accent used
> directly on dark brown.

| File | Task ID | Verdict | Notes |
|---|---|---|---|
| `warm-poster-v1.png` | `74730eda1adaacd3f061d4e33ee3fb93` | **KEEP (alternate)** | Correct layer order and all labels correct. Deliberate dark near-black DATA band with cream text (bold, on-brand — dark as accent, not inverted hierarchy). Yellow arrows read strongly. Faint constellation + factory silhouette in HOST band exactly as briefed, doesn't compete with text. |
| `warm-poster-v2.png` | `829f0498cc7b9fafc0e9dc19deb30db6` | **KEEP (alternate)** | Same prompt, independent generation. SURFACES band rendered as 4 sub-divided cells (one per app) rather than one continuous band — an unrequested but harmless layout choice, still reads clearly as one SURFACES layer. Some arrows show a soft double-exposure halo (e.g. above APPYRADAR/WATCHTOWER) — a minor render artifact, not text garbling. All labels spelled correctly, correct order, on-brand palette. |

---

## Selection rationale

All 4 generations succeeded with **zero garbled or misspelled text**, correct DATA→SURFACES→HOST
bottom-to-top order, and no cool-dominant or amber-on-brown palette violations — a clean run, no
retries needed. **`drawn-blueprint-v2.png`** was chosen as the primary poster embedded in
`../index.html` for having the most even, uncrowded composition of the four. The other three are kept
as linked alternates in the same section rather than discarded, since none had a disqualifying defect —
this was a "pick the best of several goods," not a "reject the bad ones" pass.
