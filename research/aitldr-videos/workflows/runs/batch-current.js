// batch run (GENERATED) — 30 videos.
export const meta = {
  name: 'aitldr-enrich-batch',
  description: 'Enrich a paced batch of 30 AI-TLDR videos (idempotent)',
  phases: [{ title: 'Enrich', detail: 'one sub-agent per video' }],
}

const PATH = "/Users/davidcruwys/dev/ad/apps/dark-factory/research/aitldr-videos/raw/videos.jsonl"
const LINES = [285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314]
log(`batch start: lines=${LINES.length}`)

const CATS = 'ai-tools | workflows | video-creation | content | automation | community'


const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['title','slug','youtubeId','format','duration','published','category','description','tags','featured_candidate','verified','generated'],
  properties: {
    title: { type: 'string' },
    slug: { type: 'string' },
    youtubeId: { type: 'string' },
    format: { type: 'string', enum: ['video','short'], description: 'copied verbatim from source.format' },
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
The object has: id, title, format ("video" or "short"), duration (seconds, integer), upload_date (YYYYMMDD), description, tags.

Step 2 — produce the record. Rules:
- title:       COPY verbatim from source.title.
- youtubeId:   COPY source.id (the 11-char video id, NOT a URL).
- format:      COPY source.format verbatim — exactly "video" or "short". Do NOT guess from duration.
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
- verified:    list the fields copied verbatim from source — MUST be exactly ["title","youtubeId","format","duration","published"].
- generated:   list the derived fields — MUST be exactly ["slug","category","description","tags"].

Return ONLY the structured record.`,
    { label: `enrich:L${lineNo}`, phase: 'Enrich', schema: SCHEMA }
  )
))

return { count: results.filter(Boolean).length, records: results }
