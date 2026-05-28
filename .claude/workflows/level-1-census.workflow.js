export const meta = {
  name: "level-1-census",
  description: "Level 1 artifact census — reads a batch of artifacts from artifacts.jsonl, fans out in parallel to assess each one, appends census records to census.jsonl. Run in batches of 5 for testing.",
  phases: [
    { title: "Load",    detail: "Read artifacts.jsonl and extract the requested batch." },
    { title: "Assess",  detail: "Fan out in parallel — one agent per artifact reads the source file and produces a census record." },
    { title: "Store",   detail: "Append all census records to research/census.jsonl." }
  ]
};

const A = typeof args === "string" ? JSON.parse(args) : args || {};
if (!A.artifactsPath || !A.censusPath) {
  return { error: "args required: artifactsPath, censusPath" };
}

const batchStart = A.batchStart ?? 0;
const batchSize  = A.batchSize  ?? 5;
const assessedAt = A.ts ? A.ts.slice(0, 10) : "2026-05-26";

// === CENSUS RECORD SCHEMA ===
const CENSUS_SCHEMA = {
  type: "object",
  required: ["artifact_id", "cluster", "quality_tier", "verdict", "verdict_reason"],
  properties: {
    artifact_id:    { type: "string" },
    cluster:        { type: "string" },
    quality_tier:   { type: "integer", minimum: 1, maximum: 5 },
    verdict:        { enum: ["adopt", "evaluate", "skip", "defer"] },
    verdict_reason: { type: "string" }
  }
};

// === PHASE: LOAD ===
phase("Load");

const loaded = await agent(
  `Read the JSONL file at ${A.artifactsPath}.
Parse every line as JSON. Extract lines ${batchStart} through ${batchStart + batchSize - 1} (0-indexed).
Return { artifacts: [ ...array of those records... ] }.
Each record has fields: id, repo, file_path, artifact_type, name, description_normalized, cluster_facet.`,
  {
    label: "load-batch",
    phase: "Load",
    schema: {
      type: "object",
      required: ["artifacts"],
      properties: {
        artifacts: {
          type: "array",
          items: {
            type: "object",
            required: ["id", "file_path", "artifact_type", "name", "description_normalized", "cluster_facet"],
            properties: {
              id:                    { type: "string" },
              file_path:             { type: "string" },
              artifact_type:         { type: "string" },
              name:                  { type: "string" },
              description_normalized:{ type: "string" },
              cluster_facet:         { type: "array", items: { type: "string" } }
            }
          }
        }
      }
    }
  }
);

if (!loaded?.artifacts?.length) return { error: "failed to load artifact batch" };
log(`Loaded ${loaded.artifacts.length} artifacts (batch ${batchStart}–${batchStart + loaded.artifacts.length - 1})`);

// === PHASE: ASSESS (parallel) ===
phase("Assess");

const assessJobs = loaded.artifacts.map(artifact => () => agent(
  `You are performing a Level 1 census assessment of an agent skill/command/artifact for the Dark Factory capability library.

ARTIFACT METADATA:
- ID: ${artifact.id}
- Type: ${artifact.artifact_type}
- Name: ${artifact.name}
- Description: ${artifact.description_normalized}
- Cluster facets: ${artifact.cluster_facet.join(", ")}
- Source file: ${artifact.file_path}

STEP 1: Read the source file at ${artifact.file_path} using your Read tool (or Bash cat if Read fails).

STEP 2: Based on what you read, produce a census record with these fields:

- artifact_id: use the ID exactly as given above
- cluster: pick the SINGLE best cluster from this list: code-review, code-implementation, spec-writing, documentation, delivery-readiness, orchestration, knowledge-capture, system-comprehension, verification-validation, workflow-architecture, refactor, test-authoring, security, performance, other
- quality_tier: integer 1–5
    5 = exceptional — clear mechanism, would immediately improve David's stack
    4 = strong — worth deep evaluation
    3 = adequate — some useful elements, not standout
    2 = weak — duplicates something better elsewhere
    1 = poor signal/noise
- verdict: one of:
    adopt   — so clearly useful it could skip straight to distillation
    evaluate — worth a full Level 2a deep eval scorecard
    skip    — not relevant or too low quality
    defer   — potentially useful but not now (too specialised, wrong domain)
- verdict_reason: one concise sentence explaining the verdict

Return exactly: { artifact_id, cluster, quality_tier, verdict, verdict_reason }`,
  {
    label: `assess:${artifact.name}`,
    phase: "Assess",
    schema: CENSUS_SCHEMA
  }
));

const assessments = await parallel(assessJobs);
const valid = assessments.filter(Boolean);
log(`Assessed ${valid.length}/${loaded.artifacts.length} artifacts`);

if (!valid.length) return { error: "all assessments failed" };

// === PHASE: STORE ===
phase("Store");

const records = valid.map(r => JSON.stringify({
  ...r,
  assessed_at: assessedAt,
  batch: batchStart
}));

const stored = await agent(
  `Append the following ${records.length} lines to the JSONL file at ${A.censusPath}.
Create the file if it does not exist.
Append each line followed by a newline. Do not reformat or pretty-print.

Lines to append:
${records.join("\n")}

Use Bash with printf or a heredoc to append verbatim. Return { ok: true, count: ${records.length} }.`,
  {
    label: "store-census",
    phase: "Store",
    schema: {
      type: "object",
      required: ["ok", "count"],
      properties: { ok: { type: "boolean" }, count: { type: "integer" } }
    }
  }
);

if (!stored?.ok) return { error: "census store write failed" };

log(`Census batch ${batchStart}–${batchStart + valid.length - 1} written to ${A.censusPath}`);

return {
  ok: true,
  batchStart,
  batchSize: valid.length,
  censusPath: A.censusPath,
  records: valid
};
