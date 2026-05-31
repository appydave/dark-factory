export const meta = {
  name: "nail-salon-video",
  description: "Generate a 30s educational nail-art video. Prime domain → write transcript → split into beats → per-beat (scene → image prompt → image → video) → ffmpeg stitch.",
  phases: [
    { title: "Prime",  detail: "Gather Chiang Mai nail-artist domain context for the topic." },
    { title: "Script", detail: "Write a 30-second educational transcript in salon-floor voice." },
    { title: "Beats",  detail: "Split the transcript into 3–4 beats of 7–10 seconds each." },
    { title: "Scenes", detail: "Per beat: design scene → write image prompt → generate image → image→video." },
    { title: "Stitch", detail: "ffmpeg concat all beat videos into a single ~30s mp4." },
  ],
};

// ─── Args ─────────────────────────────────────────────────────────────────────

const A = typeof args === "string" ? JSON.parse(args) : args || {};
if (!A.topic || !A.outputDir) {
  return { error: "args required: topic, outputDir" };
}
const TARGET_SECONDS = A.targetSeconds ?? 30;
const BEAT_COUNT     = A.beatCount     ?? 3;
const SLUG           = A.slug          ?? "nail-salon-video";
const KIE_IMG_MODEL  = A.kieImageModel ?? "gpt-image-2";       // verify against kie.ai catalog
const KIE_VID_MODEL  = A.kieVideoModel ?? "kling-v2-master";   // verify against kie.ai catalog
const KIE_ENV_PATH   = A.envPath       ?? "/Users/davidcruwys/dev/ad/apps/dark-factory/.env";

// ─── Design constants (injected into every visual prompt) ─────────────────────

const DESIGN = {
  setting: "Chiang Mai nail-art salon — NYC-pro polish blended with warm Thai accents",
  palette: "soft whites, blush pink, coral accent, brushed gold trim",
  cast: [
    { name: "Mei",  hair: "pink",   role: "lead artist" },
    { name: "Ploy", hair: "purple", role: "co-host / assistant" },
  ],
  style: "Pixar-style 3D render, soft key light, shallow depth of field, warm friendly mood",
  tone:  "educational, peer-to-peer, no jargon dumps",
};
const ZONES = ["manicure-bar", "pedi-lounge", "nail-art-station", "window-seat"];

// ─── KIE.AI image generation (same pattern as thumbnails.workflow.js) ────────

async function generateImage(prompt, outputPath, label) {
  return await agent(
    `Call kie.ai to generate one image.

Steps:
1. Read KIE_API_KEY: grep KIE_API_KEY ${KIE_ENV_PATH} | cut -d= -f2
2. POST https://api.kie.ai/api/v1/jobs/createTask
   Headers: Authorization: Bearer <KIE_API_KEY>, Content-Type: application/json
   Body: { "prompt": ${JSON.stringify(prompt)}, "model": "${KIE_IMG_MODEL}", "aspectRatio": "9:16", "outputFormat": "jpg" }
3. Extract taskId (field may be taskId, id, or data.taskId — inspect response).
4. Poll GET https://api.kie.ai/api/v1/jobs/recordInfo/<taskId> every 10s (max 20 polls / 200s) until complete.
5. Download the resulting image URL to ${outputPath} with curl.
6. Return { ok: true, taskId, path: "${outputPath}", bytes: <size> }.

Abort on any non-2xx and return { ok: false, error: "<reason>" }.`,
    {
      label: `image:${label}`,
      phase: "Scenes",
      schema: {
        type: "object",
        required: ["ok"],
        properties: {
          ok:     { type: "boolean" },
          taskId: { type: "string" },
          path:   { type: "string" },
          bytes:  { type: "integer" },
          error:  { type: "string" },
        },
      },
    }
  );
}

// ─── KIE.AI image-to-video ───────────────────────────────────────────────────

async function generateVideo(imagePath, motionPrompt, outputPath, label) {
  return await agent(
    `Call kie.ai to convert an image into a short ~8s video clip.

Steps:
1. Read KIE_API_KEY: grep KIE_API_KEY ${KIE_ENV_PATH} | cut -d= -f2
2. ${KIE_VID_MODEL} expects a source image. Most kie.ai i2v models accept either a public URL or base64 data URI; check https://docs.kie.ai for the ${KIE_VID_MODEL} schema. If the model needs a URL and no upload endpoint is available, encode ${imagePath} as a base64 data URI inline.
3. POST https://api.kie.ai/api/v1/jobs/createTask
   Headers: Authorization: Bearer <KIE_API_KEY>, Content-Type: application/json
   Body: { "model": "${KIE_VID_MODEL}", "imageUrl": "<url-or-data-uri>", "prompt": ${JSON.stringify(motionPrompt)}, "duration": 8, "aspectRatio": "9:16" }
4. Extract taskId.
5. Poll GET https://api.kie.ai/api/v1/jobs/recordInfo/<taskId> every 20s (max 30 polls / 600s) until complete.
6. Download the resulting video URL to ${outputPath} with curl.
7. Return { ok: true, taskId, path: "${outputPath}", bytes: <size> }.

Abort on any non-2xx and return { ok: false, error: "<reason>" }.`,
    {
      label: `video:${label}`,
      phase: "Scenes",
      schema: {
        type: "object",
        required: ["ok"],
        properties: {
          ok:     { type: "boolean" },
          taskId: { type: "string" },
          path:   { type: "string" },
          bytes:  { type: "integer" },
          error:  { type: "string" },
        },
      },
    }
  );
}

// ─── Schemas ──────────────────────────────────────────────────────────────────

const BEATS_S = {
  type: "object",
  required: ["beats"],
  properties: {
    beats: {
      type: "array",
      minItems: BEAT_COUNT, maxItems: BEAT_COUNT,
      items: {
        type: "object",
        required: ["idx", "seconds", "narration"],
        properties: {
          idx:       { type: "integer" },
          seconds:   { type: "number" },
          narration: { type: "string" },
        },
      },
    },
  },
};

const SCENE_S = {
  type: "object",
  required: ["zone", "lead", "supporting", "action", "mood"],
  properties: {
    zone:       { enum: ZONES },
    lead:       { enum: DESIGN.cast.map(c => c.name) },
    supporting: { type: "string" },
    action:     { type: "string" },
    mood:       { type: "string" },
  },
};

const PROMPT_S = {
  type: "object",
  required: ["imagePrompt", "motionPrompt"],
  properties: {
    imagePrompt:  { type: "string" },
    motionPrompt: { type: "string" },
  },
};

// ─── Workflow ─────────────────────────────────────────────────────────────────

log(`nail-salon-video start — topic="${A.topic}" → ${A.outputDir}`);

await agent(
  `Run: mkdir -p ${A.outputDir}/beats\nReturn { ok: true }.`,
  { label: "mkdir", phase: "Prime", schema: { type: "object", required: ["ok"], properties: { ok: { type: "boolean" } } } }
);

// ── Prime: domain context ─────────────────────────────────────────────────────
phase("Prime");

const primer = await agent(
  `You are briefing a content writer for a Chiang Mai nail-art salon's short-form education channel.

Topic: "${A.topic}"

Produce a tight brief covering:
- What an experienced Chiang Mai nail artist actually knows about this topic
- 3–5 concrete, accurate facts the video must convey
- One common misconception worth debunking
- Tone notes (warm peer-to-peer, salon-floor, not clinical)

Return { brief: "<markdown>" }.`,
  {
    label:  "domain-prime",
    phase:  "Prime",
    schema: { type: "object", required: ["brief"], properties: { brief: { type: "string" } } },
  }
);
const brief = primer?.brief ?? "";

// ── Script: 30s educational transcript ────────────────────────────────────────
phase("Script");

const scriptR = await agent(
  `Write a ${TARGET_SECONDS}-second educational transcript for a vertical short video.

Topic: "${A.topic}"

Domain brief:
${brief}

Tone: ${DESIGN.tone}
Speakers (visual only — don't name them in dialogue unless natural): ${DESIGN.cast.map(c => `${c.name} (${c.hair} hair, ${c.role})`).join("; ")}
Setting (visual only — don't describe in dialogue): ${DESIGN.setting}

Hard constraints:
- ~${TARGET_SECONDS} seconds of spoken English at a natural pace (~${Math.round(TARGET_SECONDS * 2.5)} words).
- No intro fluff, no "hi everyone". Open on the lesson, close with one memorable line.
- Avoid jargon dumps; one concrete tip beats three vague ones.

Return { transcript: "<single block of dialogue>" }.`,
  {
    label:  "write-transcript",
    phase:  "Script",
    schema: { type: "object", required: ["transcript"], properties: { transcript: { type: "string" } } },
  }
);
if (!scriptR?.transcript) return { error: "transcript generation failed" };
const transcript = scriptR.transcript;

// ── Beats: split into N beats of 7–10s ────────────────────────────────────────
phase("Beats");

const beatsR = await agent(
  `Split this transcript into exactly ${BEAT_COUNT} beats of 7–10 seconds each (total ≈ ${TARGET_SECONDS}s). Each beat must be a coherent narrative unit — not a sentence fragment.

TRANSCRIPT:
${transcript}

Return { beats: [{ idx, seconds, narration }, ... ${BEAT_COUNT} items] }, idx starting at 0.`,
  { label: "split-beats", phase: "Beats", schema: BEATS_S }
);
if (!beatsR?.beats) return { error: "beat split failed" };
const beats = beatsR.beats;

// ── Scenes pipeline: scene → prompts → image → video, per beat ───────────────
phase("Scenes");

const beatResults = await pipeline(
  beats,
  // stage 1: scene design
  async (beat) => {
    const scene = await agent(
      `Design ONE scene inside our nail salon for this beat. The salon and the two artists stay constant across beats; only the zone, lead artist, and action change.

Beat ${beat.idx}: "${beat.narration}"

Cast: ${JSON.stringify(DESIGN.cast)}
Zones available: ${ZONES.join(", ")}
Setting: ${DESIGN.setting}

Return { zone, lead, supporting, action, mood }.`,
      { label: `scene:b${beat.idx}`, phase: "Scenes", schema: SCENE_S }
    );
    return { beat, scene };
  },
  // stage 2: image + motion prompts
  async ({ beat, scene }) => {
    const prompts = await agent(
      `Write two prompts for beat ${beat.idx}.

Beat narration: "${beat.narration}"
Scene: ${JSON.stringify(scene)}
Style: ${DESIGN.style}
Palette: ${DESIGN.palette}
Setting: ${DESIGN.setting}

1) imagePrompt — one rich prompt for a still image (9:16 vertical). Include style, palette, character details (hair colours), action, framing, lighting. No text overlays.
2) motionPrompt — 1–2 sentences describing gentle motion to animate the still into (camera move + character action). Subtle, not dramatic.

Return { imagePrompt, motionPrompt }.`,
      { label: `prompt:b${beat.idx}`, phase: "Scenes", schema: PROMPT_S }
    );
    return { beat, scene, prompts };
  },
  // stage 3: image
  async ({ beat, scene, prompts }) => {
    const imagePath = `${A.outputDir}/beats/beat-${beat.idx}.jpg`;
    const image = await generateImage(prompts.imagePrompt, imagePath, `b${beat.idx}`);
    return { beat, scene, prompts, image, imagePath };
  },
  // stage 4: image → video
  async ({ beat, scene, prompts, image, imagePath }) => {
    if (!image?.ok) return { beat, scene, prompts, image, imagePath, video: { ok: false, error: "image failed" } };
    const videoPath = `${A.outputDir}/beats/beat-${beat.idx}.mp4`;
    const video = await generateVideo(imagePath, prompts.motionPrompt, videoPath, `b${beat.idx}`);
    return { beat, scene, prompts, image, imagePath, video, videoPath };
  }
);

const okBeats = beatResults.filter(b => b?.video?.ok);
if (okBeats.length === 0) return { error: "no beat videos generated", beatResults };

// ── Stitch: ffmpeg concat ─────────────────────────────────────────────────────
phase("Stitch");

const finalPath      = `${A.outputDir}/${SLUG}.mp4`;
const concatListPath = `${A.outputDir}/beats/concat.txt`;
const concatList     = okBeats.map(b => `file '${b.videoPath}'`).join("\n");

const stitchR = await agent(
  `Use ffmpeg to concatenate beat videos into the final video.

Step 1 — Write the concat list to ${concatListPath} using the Write tool. Content (literal, no extra lines):
${concatList}

Step 2 — Run: ffmpeg -y -f concat -safe 0 -i ${concatListPath} -c copy ${finalPath}
If -c copy fails with a codec mismatch, retry with re-encode:
ffmpeg -y -f concat -safe 0 -i ${concatListPath} -c:v libx264 -pix_fmt yuv420p -movflags +faststart ${finalPath}

Step 3 — Stat the final file for size in bytes.

Return { ok: true, path: "${finalPath}", bytes: <size> } or { ok: false, error: "<reason>" }.`,
  {
    label:  "ffmpeg-concat",
    phase:  "Stitch",
    schema: {
      type: "object",
      required: ["ok"],
      properties: {
        ok:    { type: "boolean" },
        path:  { type: "string" },
        bytes: { type: "integer" },
        error: { type: "string" },
      },
    },
  }
);

log(`nail-salon-video done — ${okBeats.length}/${beats.length} beats stitched → ${finalPath}`);

return {
  ok:         !!stitchR?.ok,
  topic:      A.topic,
  brief,
  transcript,
  beats,
  beatResults,
  finalVideo: stitchR,
};
