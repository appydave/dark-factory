// aitldr-enrich.js — Dark Factory enrich workflow for AI-TLDR videos.
//
// This is the version-controlled copy of the workflow the harness ran.
// To run it: invoke the Workflow tool with { scriptPath: "<this file>" }.
//
// ─────────────────────────────────────────────────────────────────────────
// HOW SKIPPING / RESUME WORKS — read this before scaling to 324.
//
//   Layer 1 — harness resume (automatic):
//     Workflow({ scriptPath, resumeFromRunId: "<prior run id>" }) returns the
//     CACHED result of every agent() call whose (prompt, opts) is unchanged,
//     and only re-runs new/edited calls. Same script + same args = 100% cache
//     hit. This is how you recover from a crash mid-run for free.
//
//   Layer 2 — content idempotency (driver's job, NOT this script's):
//     Workflow scripts have NO filesystem access, so this script CANNOT look
//     at enriched/*.json to decide what's already done. That decision is made
//     ONE LAYER UP by the inline driver before launch: it lists which
//     youtubeIds already have an enriched/<slug>.json, and passes ONLY the
//     remaining line numbers in via `LINES`. So "skip already-processed" =
//     the driver hands this script a shorter LINES array. The script itself
//     faithfully processes whatever line-list it is given.
// ─────────────────────────────────────────────────────────────────────────

export const meta = {
  name: 'aitldr-enrich',
  description: 'Enrich AI-TLDR videos: classify category, summarize, normalize — one agent per video',
  phases: [{ title: 'Enrich', detail: 'one sub-agent per video row' }],
}

const PATH = (args && args.path) || '/Users/davidcruwys/dev/ad/apps/dark-factory/research/aitldr-videos/raw/videos.jsonl'

// LINES = the 1-indexed line numbers in videos.jsonl to process this run.
// Default: all 1..count. The driver overrides this with only the NOT-YET-DONE
// lines to make the run idempotent/resumable (see "Layer 2" above).
const COUNT = (args && args.count) || 25
const LINES = (args && args.lines) || Array.from({ length: COUNT }, (_, i) => i + 1)
log(`enrich start: path=${PATH} lines=${LINES.length}`)

const CATS = 'ai-tools | workflows | video-creation | content | automation | community'

const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['title','slug','youtubeId','duration','published','category','description','tags','featured_candidate','verified','generated'],
  properties: {
    title: { type: 'string' },
    slug: { type: 'string' },
    youtubeId: { type: 'string' },
    duration: { type: 'string', description: 'M:SS or H:MM:SS' },
    published: { type: 'string', description: 'YYYY-MM-DD' },
    category: { type: 'string', enum: ['ai-tools','workflows','video-creation','content','automation','community'] },
    description: { type: 'string', description: '<=160 chars, fresh summary' },
    tags: { type: 'array', items: { type: 'string' } },
    featured_candidate: { type: 'boolean' },
    verified: { type: 'array', items: { type: 'string' } },
    generated: { type: 'array', items: { type: 'string' } },
  },
}

phase('Enrich')

const results = await parallel(LINES.map((lineNo) => () =>
  agent(
    `You are enriching ONE AI-TLDR YouTube video into a website content record.

Step 1 — fetch your row. Run this bash command and parse the single JSON object it prints:
    sed -n '${lineNo}p' ${PATH}
The object has: id, title, duration (seconds, integer), upload_date (YYYYMMDD), description, tags.

Step 2 — produce the record. Rules:
- title:       COPY verbatim from source.title.
- youtubeId:   COPY source.id (the 11-char video id, NOT a URL).
- duration:    NORMALIZE source.duration seconds -> "M:SS" (or "H:MM:SS" if >=3600). e.g. 282 -> "4:42".
- published:   CONVERT source.upload_date "YYYYMMDD" -> "YYYY-MM-DD".
- slug:        DERIVE kebab-case from the title: lowercase, strip punctuation, spaces->hyphens, collapse repeats, no leading/trailing hyphen. Keep it readable (<=70 chars).
- category:    CLASSIFY into exactly ONE of: ${CATS}. The channel has NO native topic tags, so you must judge from title+description. Guidance:
                 ai-tools=reviewing/walkthrough of a specific AI tool;
                 workflows=multi-step recipe combining tools for a task;
                 video-creation=making video/animation/cinematic content;
                 content=AI writing/thumbnails/infographics/content strategy;
                 automation=no-code/low-code automation, Claude Code skills, scripted pipelines;
                 community=Skool/community updates. Pick the single best fit.
- description:  WRITE a FRESH summary, <=160 chars, sharp and concrete (AI-TLDR voice: direct, no fluff). Do NOT copy the YouTube description. Must be <=160 characters.
- tags:        Take up to 8 of source.tags; if empty, derive 3-5 from the title. Lowercase.
- featured_candidate: false (featured is decided later by recency rule).
- verified:    list the fields copied verbatim from source — MUST be exactly ["title","youtubeId","duration","published"].
- generated:   list the derived fields — MUST be exactly ["slug","category","description","tags"].

Return ONLY the structured record.`,
    { label: `enrich:L${lineNo}`, phase: 'Enrich', schema: SCHEMA }
  )
))

return { count: results.filter(Boolean).length, records: results }
