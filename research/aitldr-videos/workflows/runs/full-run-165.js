// full-run-165.js — GENERATED run script (do not hand-edit).
// Processes the 140 not-yet-enriched videos of @AITLDR (165 total, 25 already done).
// LINES + PATH are baked as literals to avoid args propagation issues and to record
// exactly which rows this run covered.

export const meta = {
  name: 'aitldr-enrich-full',
  description: 'Enrich the remaining 140 AI-TLDR videos (idempotent: skips already-enriched)',
  phases: [{ title: 'Enrich', detail: 'one sub-agent per remaining video' }],
}

const PATH = "/Users/davidcruwys/dev/ad/apps/dark-factory/research/aitldr-videos/raw/videos.jsonl"
const LINES = [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165]
log(`enrich-full start: path=${PATH} lines=${LINES.length}`)

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
