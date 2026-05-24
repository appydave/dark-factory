export const meta = {
  name: "content-analysis",
  description: "Extract 12 content-analysis fields from a transcript in parallel. Replicates YLO probe #1 using the native Workflow Tool parallel() primitive.",
  phases: [
    { title: "Load",    detail: "Load transcript text." },
    { title: "Analyze", detail: "Run 12 analysis agents concurrently via parallel()." },
    { title: "Persist", detail: "Write all results to the EAV JSONL store." },
  ],
};

// ─── Args ─────────────────────────────────────────────────────────────────────

const A = typeof args === "string" ? JSON.parse(args) : args || {};
if (!A.transcriptPath || !A.storePath) {
  return { error: "args required: transcriptPath, storePath" };
}
const RUN_TS = A.ts || "2026-05-25T00:00:00.000Z";

// ─── EAV store helpers ────────────────────────────────────────────────────────

async function remember(key, value, meta = {}) {
  const record = {
    key,
    group: meta.group ?? null,
    index: meta.index ?? null,
    value,
    meta: {
      step:    meta.step    ?? "unknown",
      by:      meta.by      ?? "workflow:content-analysis",
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

// ─── Schemas ──────────────────────────────────────────────────────────────────

const STR_S   = (key) => ({ type: "object", required: [key], properties: { [key]: { type: "string" } } });
const ARR_S   = (key) => ({ type: "object", required: [key], properties: { [key]: { type: "array", items: { type: "string" } } } });

// ─── Workflow ─────────────────────────────────────────────────────────────────

log(`content-analysis start — store=${A.storePath}`);

phase("Load");

const transcript = await loadFile(A.transcriptPath, "transcript");
if (!transcript) return { error: "could not load transcript" };
await remember("transcriptPath", A.transcriptPath, { step: "seed" });

phase("Analyze");

const TRANSCRIPT_BLOCK = `Transcript:\n${transcript}`;

const [
  mainTopicR,
  keywordsR,
  audienceInsightsR,
  emotionalTriggersR,
  statisticsR,
  catchyPhrasesR,
  ctaPhrasesR,
  keyTakeawaysR,
  overallToneR,
  questionsPosedR,
  searchTermsR,
  uspR,
] = await parallel([

  agent(
    `Analyze the transcript and identify the primary topic or theme.\n\n${TRANSCRIPT_BLOCK}\n\n` +
    `Return ONLY a JSON object: { "mainTopic": "..." } — 1-2 sentences. No explanation, no markdown wrapper.`,
    { label: "analyze-main-topic", phase: "Analyze", schema: STR_S("mainTopic") }
  ),

  agent(
    `Analyze the transcript and extract relevant SEO keywords.\n\n${TRANSCRIPT_BLOCK}\n\n` +
    `Return ONLY a JSON object: { "keywords": ["...", "..."] } — minimum 3, maximum 15. No explanation, no markdown wrapper.`,
    { label: "analyze-keywords", phase: "Analyze", schema: ARR_S("keywords") }
  ),

  agent(
    `Analyze the transcript and identify references to specific audience groups, demographics, skill levels, or characteristics.\n\n${TRANSCRIPT_BLOCK}\n\n` +
    `Return ONLY a JSON object: { "audienceInsights": ["...", "..."] } — observations about who this content is aimed at. No explanation, no markdown wrapper.`,
    { label: "analyze-audience-insights", phase: "Analyze", schema: ARR_S("audienceInsights") }
  ),

  agent(
    `Analyze the transcript and identify the emotional triggers or tones that influence audience response.\n\n${TRANSCRIPT_BLOCK}\n\n` +
    `Return ONLY a JSON object: { "emotionalTriggers": ["...", "..."] } — emotional tones or hooks present. No explanation, no markdown wrapper.`,
    { label: "analyze-emotional-triggers", phase: "Analyze", schema: ARR_S("emotionalTriggers") }
  ),

  agent(
    `Analyze the transcript and extract any important statistics, numbers, percentages, or counts mentioned.\n\n${TRANSCRIPT_BLOCK}\n\n` +
    `Return ONLY a JSON object: { "statistics": "..." } — a string summarizing the important numbers found. Empty string if none. No explanation, no markdown wrapper.`,
    { label: "analyze-statistics", phase: "Analyze", schema: STR_S("statistics") }
  ),

  agent(
    `Analyze the transcript and extract memorable or unique expressions suitable for marketing or promotional copy.\n\n${TRANSCRIPT_BLOCK}\n\n` +
    `Return ONLY a JSON object: { "catchyPhrases": ["...", "..."] } — direct quotes only. No explanation, no markdown wrapper.`,
    { label: "analyze-catchy-phrases", phase: "Analyze", schema: ARR_S("catchyPhrases") }
  ),

  agent(
    `Analyze the transcript and extract the specific call-to-action phrases explicitly stated by the presenter.\n\n${TRANSCRIPT_BLOCK}\n\n` +
    `Return ONLY a JSON object: { "ctaPhrases": ["...", "..."] } — only CTAs explicitly stated. No explanation, no markdown wrapper.`,
    { label: "analyze-cta-phrases", phase: "Analyze", schema: ARR_S("ctaPhrases") }
  ),

  agent(
    `Analyze the transcript and extract the key takeaways — concise insights viewers will gain.\n\n${TRANSCRIPT_BLOCK}\n\n` +
    `Return ONLY a JSON object: { "keyTakeaways": ["...", "..."] } — minimum 3, maximum 8. No explanation, no markdown wrapper.`,
    { label: "analyze-key-takeaways", phase: "Analyze", schema: ARR_S("keyTakeaways") }
  ),

  agent(
    `Analyze the transcript and determine the overall tone or style of the content.\n\n${TRANSCRIPT_BLOCK}\n\n` +
    `Return ONLY a JSON object: { "overallTone": "..." } — a short phrase (e.g. "casual tutorial", "conversational and practical"). No explanation, no markdown wrapper.`,
    { label: "analyze-overall-tone", phase: "Analyze", schema: STR_S("overallTone") }
  ),

  agent(
    `Analyze the transcript and identify the rhetorical and engagement questions posed or answered.\n\n${TRANSCRIPT_BLOCK}\n\n` +
    `Return ONLY a JSON object: { "questionsPosedOrAnswered": ["...", "..."] } — questions asked or addressed by the presenter. No explanation, no markdown wrapper.`,
    { label: "analyze-questions-posed", phase: "Analyze",
      schema: { type: "object", required: ["questionsPosedOrAnswered"], properties: { questionsPosedOrAnswered: { type: "array", items: { type: "string" } } } } }
  ),

  agent(
    `Analyze the transcript and extract key phrases suitable for Google and YouTube competitor research.\n\n${TRANSCRIPT_BLOCK}\n\n` +
    `Return ONLY a JSON object: { "searchTerms": ["...", "..."] } — minimum 3 phrases a viewer might search to find this content. No explanation, no markdown wrapper.`,
    { label: "analyze-search-terms", phase: "Analyze", schema: ARR_S("searchTerms") }
  ),

  agent(
    `Analyze the transcript and identify unique selling points that differentiate this content from others on the same topic.\n\n${TRANSCRIPT_BLOCK}\n\n` +
    `Return ONLY a JSON object: { "usp": ["...", "..."] } — unique angles, approaches, or value propositions. No explanation, no markdown wrapper.`,
    { label: "analyze-usp", phase: "Analyze", schema: ARR_S("usp") }
  ),

]);

phase("Persist");

const fields = {
  mainTopic:              mainTopicR?.mainTopic,
  keywords:               keywordsR?.keywords,
  audienceInsights:       audienceInsightsR?.audienceInsights,
  emotionalTriggers:      emotionalTriggersR?.emotionalTriggers,
  statistics:             statisticsR?.statistics,
  catchyPhrases:          catchyPhrasesR?.catchyPhrases,
  ctaPhrases:             ctaPhrasesR?.ctaPhrases,
  keyTakeaways:           keyTakeawaysR?.keyTakeaways,
  overallTone:            overallToneR?.overallTone,
  questionsPosedOrAnswered: questionsPosedR?.questionsPosedOrAnswered,
  searchTerms:            searchTermsR?.searchTerms,
  usp:                    uspR?.usp,
};

const nulls = Object.entries(fields).filter(([, v]) => v == null).map(([k]) => k);
if (nulls.length > 0) {
  log(`WARNING: ${nulls.length} fields returned null (schema failure): ${nulls.join(", ")}`);
}

// Write each field as its own store record (wire-compatible with blackboard)
for (const [key, value] of Object.entries(fields)) {
  if (value != null) {
    await remember(key, value, { step: "bulk-content-analysis", attempt: 1 });
  }
}

log(`content-analysis done — ${Object.keys(fields).length - nulls.length}/12 fields persisted`);

return {
  ok: true,
  fields,
  nullFields: nulls,
  storePath: A.storePath,
};
