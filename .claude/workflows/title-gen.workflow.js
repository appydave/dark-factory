export const meta = {
  name: "title-gen",
  description: "Generate 10 YouTube titles via Three Emotions Framework, apply scripted critique, refine. Persists every step to an EAV JSONL store. Replicates YLO probe #2 using the native Workflow Tool.",
  phases: [
    { title: "Generate", detail: "Generate 10 titles from the transcript using the Three Emotions Framework (CURIOSITY/DESIRE/FEAR), 40–50 chars." },
    { title: "Critique", detail: "Load the scripted critique fixture as the simulated human-gate response." },
    { title: "Refine",   detail: "Regenerate 10 titles applying the critique. Persist as selectedTitles." }
  ]
};

const A = typeof args === "string" ? JSON.parse(args) : args || {};
if (!A.transcriptPath || !A.storePath || !A.critiqueFixturePath) {
  return { error: "args required: transcriptPath, storePath, critiqueFixturePath" };
}
const RUN_TS = A.ts || "2026-05-25T00:00:00.000Z";

// === EAV STORE HELPERS (no imports allowed — every I/O goes through agent()) ===
// Format matches experiments/ylo/blackboard/runs/b65/store.jsonl:
//   { key, group?, index?, value, meta: { step, ts, attempt, source, by, status } }

async function remember(key, value, meta = {}) {
  const record = {
    key,
    group: meta.group ?? null,
    index: meta.index ?? null,
    value,
    meta: {
      step: meta.step ?? "unknown",
      by: meta.by ?? "workflow:title-gen",
      ts: RUN_TS,
      attempt: meta.attempt ?? 1,
      status: meta.status ?? "ok",
      ...(meta.source ? { source: meta.source } : {})
    }
  };
  const line = JSON.stringify(record);
  const r = await agent(
    `Append exactly one line (followed by a single newline) to the file at this absolute path:
${A.storePath}

The line to append (do not reformat, do not pretty-print, do not add quotes around it):
${line}

Use the Bash tool with a heredoc or printf so the JSON is appended verbatim. Then return { ok: true }.`,
    {
      label: `store:${key}`,
      phase: meta.step ?? "store",
      schema: { type: "object", required: ["ok"], properties: { ok: { type: "boolean" } } }
    }
  );
  if (!r?.ok) throw new Error(`store write failed for key=${key}`);
}

async function recall(key) {
  const r = await agent(
    `Read the JSONL file at ${A.storePath}. Find the LATEST line (highest line number) where the parsed JSON has key === "${key}". Return { value: <that record's value field> }. If no such record exists, return { value: null }.`,
    {
      label: `recall:${key}`,
      phase: "recall",
      schema: { type: "object", required: ["value"], properties: { value: {} } }
    }
  );
  return r?.value ?? null;
}

async function loadFile(path, label) {
  const r = await agent(
    `Read the entire contents of the file at ${path} and return { text: "<full file contents>" }. Preserve newlines.`,
    {
      label: `load:${label}`,
      phase: "load",
      schema: { type: "object", required: ["text"], properties: { text: { type: "string" } } }
    }
  );
  return r?.text ?? null;
}

// === SCHEMAS ===
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
          title:   { type: "string" }
        }
      }
    }
  }
};

// === WORKFLOW ===
log(`title-gen start — store=${A.storePath}`);

// Seed: load transcript + critique fixture text
const transcript = await loadFile(A.transcriptPath, "transcript");
if (!transcript) return { error: "could not load transcript" };
await remember("transcriptPath", A.transcriptPath, { step: "seed" });

phase("Generate");
const gen = await agent(
  `You are a YouTube title strategist for AppyDave (technical/AI content).

Generate exactly 10 candidate titles for the video whose transcript follows. Apply the Three Emotions Framework — each title is tagged with one of CURIOSITY, DESIRE, or FEAR. Distribute roughly evenly. Target 40–50 characters (optimal mobile-truncation window). Include 'chars' = the exact character count.

Return { titles: [{ emotion, chars, title }, ... 10 items] }.

TRANSCRIPT:
${transcript}`,
  { label: "generate-titles", phase: "Generate", schema: TITLES_S }
);
if (!gen) return { error: "title generation failed (schema null)" };
await remember("generatedTitles", gen.titles, { step: "generate-titles", attempt: 1 });

phase("Critique");
const critiqueText = await loadFile(A.critiqueFixturePath, "critique-fixture");
if (!critiqueText) return { error: "could not load critique fixture" };
await remember("titleCritiqueLog", critiqueText, { step: "apply-critique", attempt: 1, source: "fixture" });

phase("Refine");
const original = gen.titles.map(t => `[${t.emotion} ${t.chars}c] ${t.title}`).join("\n");
const refined = await agent(
  `You are refining YouTube titles based on a critique from the channel owner.

ORIGINAL 10 TITLES:
${original}

CRITIQUE:
${critiqueText}

Apply the critique and regenerate exactly 10 titles. Keep the Three Emotions Framework (CURIOSITY/DESIRE/FEAR distributed roughly evenly) and the 40–50 character target. Include exact char counts.

Return { titles: [{ emotion, chars, title }, ... 10 items] }.`,
  { label: "refine-titles", phase: "Refine", schema: TITLES_S }
);
if (!refined) return { error: "title refinement failed (schema null)" };
await remember("generatedTitles", refined.titles, { step: "refine-titles", attempt: 2 });
await remember("selectedTitles",  refined.titles, { step: "refine-titles", source: "refined" });

log(`title-gen done — ${refined.titles.length} refined titles persisted`);

return {
  ok: true,
  generated: gen.titles,
  critique: critiqueText,
  refined: refined.titles,
  storePath: A.storePath
};
