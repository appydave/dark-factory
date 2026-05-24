export const meta = {
  name: "titles-human",
  description: "Generate 10 titles, pause for real human critique, refine. Replicates YLO probe #3. Two-pass HITL: run without args.critique to generate; run again with args.critique to refine.",
  phases: [
    { title: "Generate", detail: "Generate 10 candidate titles from store context." },
    { title: "Gate",     detail: "Pause — human reads titles and provides critique via args.critique on next invocation." },
    { title: "Refine",   detail: "Regenerate 10 titles applying the human critique." },
  ],
};

// ─── Args ─────────────────────────────────────────────────────────────────────

const A = typeof args === "string" ? JSON.parse(args) : args || {};
if (!A.storePath) {
  return { error: "args required: storePath" };
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
      by:      meta.by      ?? "workflow:titles-human",
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

async function recall(key) {
  const r = await agent(
    `Read the JSONL file at ${A.storePath}. Find the LATEST line where the parsed JSON has key === "${key}". ` +
    `Return { value: <that record's value field> }. If not found, return { value: null }.`,
    {
      label:  `recall:${key}`,
      phase:  "recall",
      schema: { type: "object", required: ["value"], properties: { value: {} } },
    }
  );
  return r?.value ?? null;
}

// ─── Schema ───────────────────────────────────────────────────────────────────

const TITLES_S = {
  type: "object",
  required: ["titles"],
  properties: {
    titles: {
      type: "array",
      minItems: 10,
      maxItems: 10,
      items: {
        type: "object",
        required: ["emotion", "chars", "title"],
        properties: {
          emotion: { enum: ["CURIOSITY", "DESIRE", "FEAR"] },
          chars:   { type: "integer" },
          title:   { type: "string" },
        },
      },
    },
  },
};

// ─── Workflow ─────────────────────────────────────────────────────────────────
//
// HITL two-pass design:
//   Pass 1 (no args.critique): generate titles, write to store, return them for
//   human review. Human types critique and re-invokes with args.critique = "...".
//   Pass 2 (args.critique present): read generatedTitles from store, apply critique,
//   write refined titles as selectedTitles.
//
// This is the cleanest HITL pattern available in the Workflow Tool — the human
// types critique into the next invocation's args, not mid-run stdin.

log(`titles-human start — storePath=${A.storePath}`);

// ── Pass 2: refine ────────────────────────────────────────────────────────────

if (A.critique) {
  log(`Pass 2 — critique received, refining...`);
  phase("Refine");

  const generated = await recall("generatedTitles");
  if (!generated) return { error: "no generatedTitles in store — run Pass 1 first" };

  await remember("titleCritiqueLog", A.critique, { step: "apply-critique", attempt: 1, source: "human-stdin" });

  const original = generated.map(t => `[${t.emotion} ${t.chars}c] ${t.title}`).join("\n");

  const refined = await agent(
    `You are refining YouTube titles based on a critique from the channel owner.\n\n` +
    `ORIGINAL 10 TITLES:\n${original}\n\n` +
    `CRITIQUE:\n${A.critique}\n\n` +
    `Apply the critique and regenerate exactly 10 titles. ` +
    `Keep the Three Emotions Framework (CURIOSITY/DESIRE/FEAR distributed roughly evenly) ` +
    `and the 40–50 character target. Include exact char counts.\n\n` +
    `Return { titles: [{ emotion, chars, title }, ... 10 items] }.`,
    { label: "refine-titles", phase: "Refine", schema: TITLES_S }
  );
  if (!refined) return { error: "title refinement failed (schema null)" };

  await remember("generatedTitles", refined.titles, { step: "refine-titles", attempt: 2 });
  await remember("selectedTitles",  refined.titles, { step: "refine-titles", source: "human-refined" });

  log(`titles-human Pass 2 done — ${refined.titles.length} refined titles persisted`);

  return {
    ok: true,
    pass: 2,
    refined: refined.titles,
    storePath: A.storePath,
  };
}

// ── Pass 1: generate ──────────────────────────────────────────────────────────

log(`Pass 1 — generating titles from store context...`);
phase("Generate");

// Read content-analysis fields from store (populated by content-analysis workflow)
const [mainTopic, statistics, catchyPhrases, audienceInsights, shortTitle] = await parallel([
  agent(`Read the JSONL file at ${A.storePath}. Find the LATEST line where key === "mainTopic". Return { value: <value field> } or { value: null }.`,
    { label: "recall:mainTopic", phase: "recall", schema: { type: "object", required: ["value"], properties: { value: {} } } }),
  agent(`Read the JSONL file at ${A.storePath}. Find the LATEST line where key === "statistics". Return { value: <value field> } or { value: null }.`,
    { label: "recall:statistics", phase: "recall", schema: { type: "object", required: ["value"], properties: { value: {} } } }),
  agent(`Read the JSONL file at ${A.storePath}. Find the LATEST line where key === "catchyPhrases". Return { value: <value field> } or { value: null }.`,
    { label: "recall:catchyPhrases", phase: "recall", schema: { type: "object", required: ["value"], properties: { value: {} } } }),
  agent(`Read the JSONL file at ${A.storePath}. Find the LATEST line where key === "audienceInsights". Return { value: <value field> } or { value: null }.`,
    { label: "recall:audienceInsights", phase: "recall", schema: { type: "object", required: ["value"], properties: { value: {} } } }),
  agent(`Read the JSONL file at ${A.storePath}. Find the LATEST line where key === "shortTitle". Return { value: <value field> } or { value: null }.`,
    { label: "recall:shortTitle", phase: "recall", schema: { type: "object", required: ["value"], properties: { value: {} } } }),
]);

const ctx = {
  mainTopic:       mainTopic?.value       ?? "Unknown",
  statistics:      statistics?.value      ?? "",
  catchyPhrases:   catchyPhrases?.value   ?? [],
  audienceInsights: audienceInsights?.value ?? [],
  shortTitle:      shortTitle?.value      ?? A.shortTitle ?? "",
};

const gen = await agent(
  `You are a YouTube title strategist for AppyDave (technical/AI content).\n\n` +
  `Generate exactly 10 candidate titles. Apply the Three Emotions Framework — tag each ` +
  `CURIOSITY, DESIRE, or FEAR. Distribute roughly evenly. Target 40–50 characters. ` +
  `Include 'chars' = the exact character count.\n\n` +
  `Base title: ${ctx.shortTitle}\n` +
  `Main topic: ${ctx.mainTopic}\n` +
  `Statistics: ${ctx.statistics}\n` +
  `Catchy phrases: ${JSON.stringify(ctx.catchyPhrases)}\n` +
  `Audience insights: ${JSON.stringify(ctx.audienceInsights)}\n\n` +
  `Return { titles: [{ emotion, chars, title }, ... 10 items] }.`,
  { label: "generate-titles", phase: "Generate", schema: TITLES_S }
);
if (!gen) return { error: "title generation failed (schema null)" };

await remember("generatedTitles", gen.titles, { step: "generate-titles", attempt: 1 });

phase("Gate");

// Format for human readability in the return value
const formatted = gen.titles.map((t, i) =>
  `${i + 1}. [${t.emotion} ${t.chars}c] ${t.title}`
).join("\n");

log(`titles-human Pass 1 done — awaiting human critique`);
log(`Re-invoke with: args.critique = "<your critique text>"`);

return {
  ok: true,
  pass: 1,
  awaitingCritique: true,
  titles: gen.titles,
  titlesFormatted: formatted,
  instructions: `Review the titles above. Re-invoke this workflow with args.critique = "<your critique>" to refine.`,
  storePath: A.storePath,
};
