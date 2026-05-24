export const meta = {
  name: "thumbnails",
  description: "Generate 6 design briefs → 6 exploration thumbnails (parallel, cheap) → fixture selection → 3 final thumbnails (parallel, high-res) → manifest. Replicates YLO probe #4 using the Workflow Tool.",
  phases: [
    { title: "Briefs",      detail: "Generate 6 design briefs (2 per selected title × 3 titles)." },
    { title: "Explore",     detail: "Generate 6 cheap exploration thumbnails in parallel via kie.ai." },
    { title: "Select",      detail: "Apply fixture selection [0, 2, 4] from selection-fixture.json." },
    { title: "Finals",      detail: "Generate 3 final high-res thumbnails in parallel via kie.ai." },
    { title: "Manifest",    detail: "Write thumbnails-manifest.md with paths, sizes, and phase timings." },
  ],
};

// ─── Args ─────────────────────────────────────────────────────────────────────

const A = typeof args === "string" ? JSON.parse(args) : args || {};
if (!A.storePath || !A.outputDir || !A.selectionFixturePath) {
  return { error: "args required: storePath, outputDir, selectionFixturePath" };
}
const RUN_TS        = A.ts              || "2026-05-25T00:00:00.000Z";
const MANIFEST_PATH = A.manifestPath   || A.outputDir.replace(/\/$/, "") + "/../thumbnails-manifest.md";
const KIE_MODEL_EXP = A.kieModelExplore || "flux-schnell";
const KIE_MODEL_FIN = A.kieModelFinals  || "nano-banana-2";

// ─── EAV store helpers ────────────────────────────────────────────────────────

async function remember(key, value, meta = {}) {
  const record = {
    key,
    group: meta.group ?? null,
    index: meta.index ?? null,
    value,
    meta: {
      step:    meta.step    ?? "unknown",
      by:      meta.by      ?? "workflow:thumbnails",
      ts:      RUN_TS,
      attempt: meta.attempt ?? 1,
      status:  meta.status  ?? "ok",
      ...(meta.source ? { source: meta.source } : {}),
    },
  };
  const line = JSON.stringify(record);
  const r = await agent(
    `Append exactly one line (followed by a single newline) to the file at this absolute path:\n` +
    `${A.storePath}\n\n` +
    `The line to append (do not reformat, do not pretty-print, do not add quotes around it):\n` +
    `${line}\n\n` +
    `Use the Bash tool with a heredoc or printf so the JSON is appended verbatim. Then return { ok: true }.`,
    {
      label:  `store:${key}`,
      phase:  "Persist",
      schema: { type: "object", required: ["ok"], properties: { ok: { type: "boolean" } } },
    }
  );
  if (!r?.ok) throw new Error(`store write failed for key=${key}`);
}

async function loadFile(path, label) {
  const r = await agent(
    `Read the entire contents of the file at ${path} and return { text: "<full file contents>" }. Preserve newlines.`,
    {
      label:  `load:${label}`,
      phase:  "Load",
      schema: { type: "object", required: ["text"], properties: { text: { type: "string" } } },
    }
  );
  return r?.text ?? null;
}

// ─── kie.ai image gen helper ─────────────────────────────────────────────────
// Mirrors the blackboard image-gen skill:
//   POST /api/generate → poll /api/record/{taskId} → curl download

async function generateImage(prompt, outputPath, label, model, phase = "Explore") {
  const r = await agent(
    `You are calling the kie.ai image generation API to produce one thumbnail.\n\n` +
    `Steps:\n` +
    `1. Read KIE_API_KEY: run \`grep KIE_API_KEY /Users/davidcruwys/dev/ad/apps/dark-factory/.env | cut -d= -f2\` to get the key.\n` +
    `2. POST to https://api.kie.ai/api/v1/jobs/createTask with body:\n` +
    `   { "prompt": ${JSON.stringify(prompt)}, "model": "${model}", "aspectRatio": "16:9", "outputFormat": "jpg" }\n` +
    `   Header: Authorization: Bearer <KIE_API_KEY>, Content-Type: application/json\n` +
    `3. Extract the taskId from the response (field may be called taskId, id, or data.taskId — inspect the full response).\n` +
    `4. Poll GET https://api.kie.ai/api/v1/jobs/recordInfo/<taskId> with the same Authorization header every 10s until the response indicates completion (status === "completed" or similar). Stop after 20 polls (200s max).\n` +
    `5. Extract the image URL from the completed response.\n` +
    `6. Download the image to ${outputPath} using curl.\n` +
    `7. Return { ok: true, taskId: "<taskId>", path: "${outputPath}", bytes: <file size in bytes> }.\n\n` +
    `If any step fails, return { ok: false, error: "<reason>" }.`,
    {
      label:  `image:${label}`,
      phase,
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
  return r;
}

// ─── Schemas ──────────────────────────────────────────────────────────────────

const BRIEF_ITEM_S = {
  type: "object",
  required: ["index", "title_ref", "composition_pattern", "ground", "hook_text", "ghost_watermark", "prompt"],
  properties: {
    index:               { type: "integer" },
    title_ref:           { type: "string" },
    composition_pattern: { type: "string" },
    ground:              { type: "string" },
    hook_text:           { type: "string" },
    hook_text_colour:    { type: "string" },
    ghost_watermark:     { type: "object" },
    glyph_or_panel:      { type: "string" },
    prompt:              { type: "string" },
  },
};

const BRIEFS_S = {
  type: "object",
  required: ["designBriefs"],
  properties: {
    designBriefs: { type: "array", minItems: 6, maxItems: 6, items: BRIEF_ITEM_S },
  },
};

// ─── Workflow ─────────────────────────────────────────────────────────────────

log(`thumbnails start — outputDir=${A.outputDir}`);

// Ensure output dir exists
await agent(
  `Run: mkdir -p ${A.outputDir}\nThen return { ok: true }.`,
  { label: "mkdir", phase: "setup", schema: { type: "object", required: ["ok"], properties: { ok: { type: "boolean" } } } }
);

// Load context from store (populated by earlier workflows)
phase("Briefs");

const [selectedTitlesR, mainTopicR, audienceInsightsR, emotionalTriggersR] = await parallel([
  () => agent(`Read the JSONL at ${A.storePath}. Latest line where key==="selectedTitles". Return { value: <value> } or { value: null }.`,
    { label: "recall:selectedTitles",   phase: "recall", schema: { type: "object", required: ["value"], properties: { value: {} } } }),
  () => agent(`Read the JSONL at ${A.storePath}. Latest line where key==="mainTopic". Return { value: <value> } or { value: null }.`,
    { label: "recall:mainTopic",        phase: "recall", schema: { type: "object", required: ["value"], properties: { value: {} } } }),
  () => agent(`Read the JSONL at ${A.storePath}. Latest line where key==="audienceInsights". Return { value: <value> } or { value: null }.`,
    { label: "recall:audienceInsights", phase: "recall", schema: { type: "object", required: ["value"], properties: { value: {} } } }),
  () => agent(`Read the JSONL at ${A.storePath}. Latest line where key==="emotionalTriggers". Return { value: <value> } or { value: null }.`,
    { label: "recall:emotionalTriggers",phase: "recall", schema: { type: "object", required: ["value"], properties: { value: {} } } }),
]);

const selectedTitles   = selectedTitlesR?.value;
const mainTopic        = mainTopicR?.value        ?? "Unknown";
const audienceInsights = audienceInsightsR?.value ?? [];
const emotionalTriggers= emotionalTriggersR?.value?? [];

if (!selectedTitles || selectedTitles.length < 3) {
  return { error: "selectedTitles not found in store or fewer than 3 — run titles workflow first" };
}

const top3 = selectedTitles.slice(0, 3);

const briefsR = await agent(
  `You are a thumbnail concept designer working in the AppyDave brand system.\n` +
  `Produce 6 design briefs (2 concepts per title × 3 titles) optimised for YouTube thumbnail CTR.\n\n` +
  `Selected titles (3, indices 0/1/2):\n${JSON.stringify(top3, null, 2)}\n\n` +
  `Main topic: ${mainTopic}\n` +
  `Audience insights: ${JSON.stringify(audienceInsights)}\n` +
  `Emotional triggers: ${JSON.stringify(emotionalTriggers)}\n\n` +
  `## Brand rules (AppyDave — typography-first)\n` +
  `- Palette: brown #342d2d, gold #ccba9d, yellow #ffde59, cream #faf5ec, dark-surface #25201e\n` +
  `- Yellow reserved for hook text or ONE attention element\n` +
  `- Hook text: Bebas Neue, uppercase, 2–5 words, left-aligned, 30–60% frame width\n` +
  `- Ghost watermark: bold uppercase Oswald/Bebas, brown @8-15% on cream OR cream @6-12% on dark brown, bleeds one edge\n` +
  `- Composition patterns: Type-Dominant / Type+Glyph / Split Panel / Sequence Badge / Ghost-Forward\n` +
  `- Anti-patterns: NO humans, NO halftone, NO 3D render, NO neon, NO small text\n\n` +
  `Return ONLY JSON: { "designBriefs": [ { index, title_ref, composition_pattern, ground, hook_text, hook_text_colour, ghost_watermark: {word, edge, opacity}, glyph_or_panel, prompt }, ... ] }\n` +
  `Exactly 6 briefs. Briefs 0-1 → title[0], briefs 2-3 → title[1], briefs 4-5 → title[2]. title_ref must match verbatim.`,
  { label: "generate-design-briefs", phase: "Briefs", schema: BRIEFS_S }
);
if (!briefsR) return { error: "design brief generation failed (schema null)" };
const designBriefs = briefsR.designBriefs;
await remember("designBriefs", designBriefs, { step: "generate-design-briefs", attempt: 1 });

// ── Explore: 6 cheap thumbnails in parallel ───────────────────────────────────

phase("Explore");

const explorePaths = designBriefs.map((b, i) => `${A.outputDir}/exp-${i}.jpg`);

const explorationResults = await parallel(
  designBriefs.map((brief, i) =>
    () => generateImage(brief.prompt, explorePaths[i], `exp-${i}`, KIE_MODEL_EXP, "Explore")
  )
);

const explorationImages = explorationResults.map((r, i) => ({
  index: i,
  path:  r?.path  ?? explorePaths[i],
  bytes: r?.bytes ?? null,
  ok:    r?.ok    ?? false,
  taskId: r?.taskId ?? null,
}));
await remember("explorationImages", explorationImages, { step: "explore-cheap-batch", attempt: 1 });

// ── Select: read fixture ──────────────────────────────────────────────────────

phase("Select");

const fixtureText = await loadFile(A.selectionFixturePath, "selection-fixture");
const fixture = fixtureText ? JSON.parse(fixtureText) : { selectedIndices: [0, 2, 4] };
const selectedIndices = fixture.selectedIndices ?? [0, 2, 4];
await remember("selectedExplorationIndices", selectedIndices, { step: "apply-selection", attempt: 1, source: "fixture" });

// ── Finals: 3 high-res thumbnails in parallel ─────────────────────────────────

phase("Finals");

const selectedBriefs = selectedIndices.map(i => designBriefs[i]);
const finalPaths     = selectedIndices.map((_, n) => `${A.outputDir}/final-${n}.jpg`);

const finalResults = await parallel(
  selectedBriefs.map((brief, n) =>
    () => generateImage(brief.prompt, finalPaths[n], `final-${n}`, KIE_MODEL_FIN, "Finals")
  )
);

const finalImages = finalResults.map((r, n) => ({
  index:    selectedIndices[n],
  path:     r?.path   ?? finalPaths[n],
  bytes:    r?.bytes  ?? null,
  ok:       r?.ok     ?? false,
  taskId:   r?.taskId ?? null,
  titleRef: selectedBriefs[n].title_ref,
}));
await remember("finalImages", finalImages, { step: "build-finals", attempt: 1 });

// ── Manifest ──────────────────────────────────────────────────────────────────

phase("Manifest");

const manifestLines = [
  `# Thumbnails Manifest`,
  ``,
  `**Generated**: ${RUN_TS}`,
  `**Workflow**: thumbnails.workflow.js`,
  ``,
  `## Exploration (${explorationImages.length} images — ${KIE_MODEL_EXP})`,
  ``,
  ...explorationImages.map(img =>
    `- exp-${img.index}.jpg → ${img.ok ? `✅ ${img.bytes ?? "?"}b` : "❌ failed"} | brief: "${designBriefs[img.index]?.title_ref}"`
  ),
  ``,
  `## Selected indices`,
  ``,
  `${selectedIndices.join(", ")} (from fixture)`,
  ``,
  `## Finals (${finalImages.length} images — ${KIE_MODEL_FIN})`,
  ``,
  ...finalImages.map((img, n) =>
    `- final-${n}.jpg → ${img.ok ? `✅ ${img.bytes ?? "?"}b` : "❌ failed"} | "${img.titleRef}"`
  ),
  ``,
  `## Design briefs`,
  ``,
  ...designBriefs.map(b =>
    `### Brief ${b.index}: ${b.title_ref}\n` +
    `- Pattern: ${b.composition_pattern}\n` +
    `- Ground: ${b.ground}\n` +
    `- Hook: "${b.hook_text}" (${b.hook_text_colour})\n` +
    `- Watermark: ${JSON.stringify(b.ghost_watermark)}`
  ),
].join("\n");

await agent(
  `Write the following content to the file at ${MANIFEST_PATH}.\n` +
  `Create parent directories if needed (mkdir -p).\n` +
  `Use the Write tool or bash redirect — do not truncate.\n` +
  `Content:\n\n${manifestLines}\n\nThen return { ok: true }.`,
  {
    label:  "write-manifest",
    phase:  "Manifest",
    schema: { type: "object", required: ["ok"], properties: { ok: { type: "boolean" } } },
  }
);
await remember("thumbnailsManifest", MANIFEST_PATH, { step: "assemble-output", attempt: 1 });

log(`thumbnails done — ${finalImages.filter(i => i.ok).length}/3 finals generated`);

return {
  ok:               true,
  designBriefs,
  explorationImages,
  selectedIndices,
  finalImages,
  manifestPath:     MANIFEST_PATH,
  storePath:        A.storePath,
};
