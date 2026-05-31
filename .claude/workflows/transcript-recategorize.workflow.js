// transcript-recategorize.workflow.js
// Upgrade a video's category + description using its TRANSCRIPT as evidence.
//
// NON-DESTRUCTIVE: never overwrites the title-based `category` / `description`.
// It ADDS  category_transcript, description_transcript, transcript_enriched, transcript_changed.
//
// IDEMPOTENT: the driver selects only folders where transcript.txt exists AND
// transcript_enriched != true, then bakes that worklist into FOLDERS. Re-running
// processes only the new/pending stuff — never redoes a folder already marked.
//
// The VM can't touch disk, so: each AGENT reads its own files (it has Bash/Read),
// and the DRIVER writes the results back into meta.json after the run.

export const meta = {
  name: 'transcript-recategorize',
  description: 'Re-derive category + a fresh description from the video transcript (non-destructive, idempotent). One agent per pending video.',
  phases: [{ title: 'Recategorize', detail: 'one agent per video — read transcript, reclassify, resummarize' }],
}

const FOLDERS = (args && args.folders) || []
log(`transcript-recategorize start: ${FOLDERS.length} folders`)

const CATS = 'ai-tools | workflows | video-creation | content | automation | community'

const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['youtubeId', 'category_transcript', 'description_transcript', 'current_category', 'changed'],
  properties: {
    youtubeId:              { type: 'string' },
    category_transcript:    { type: 'string', enum: ['ai-tools','workflows','video-creation','content','automation','community'] },
    description_transcript: { type: 'string', description: '<=160 chars, transcript-grounded fresh summary' },
    current_category:       { type: 'string', description: 'the title-based category copied from meta.json (for audit)' },
    changed:                { type: 'boolean', description: 'true if category_transcript differs from current title-based category' },
  },
}

phase('Recategorize')

const results = await parallel(FOLDERS.map((folder) => () =>
  agent(
    `You are upgrading ONE AI-TLDR video's category and description using its TRANSCRIPT as evidence — not just the title.

Step 1 — read both files from this folder:
    cat ${folder}/meta.json
    cat ${folder}/transcript.txt
meta.json has the current title-based "category" and "youtubeId". transcript.txt is the actual spoken words.

Step 2 — produce the upgrade:
- youtubeId:           COPY from meta.json verbatim.
- current_category:    COPY meta.json's existing "category" (the title-based guess), for audit.
- category_transcript: Read the TRANSCRIPT and classify into EXACTLY ONE of: ${CATS}.
                         ai-tools = review/walkthrough of a specific AI tool;
                         workflows = multi-step recipe combining tools for a task;
                         video-creation = making video/animation/cinematic content;
                         content = AI writing/thumbnails/infographics/content strategy;
                         automation = no-code/low-code automation, agent skills, scripted pipelines;
                         community = Skool/community updates.
                       Judge from what the video ACTUALLY teaches in the transcript. If the
                       transcript contradicts the title-based guess, change it — that's the point.
- description_transcript: Write a FRESH summary, MAX 160 characters, grounded in what the transcript
                       actually says (real tools, the real outcome). AI-TLDR voice: direct, specific,
                       no fluff. Do NOT copy the title or meta's old description. Must be <= 160 chars.
- changed:             true if category_transcript != current_category, else false.

Return ONLY the structured object.`,
    { label: `recat:${folder.split('--').pop()}`, phase: 'Recategorize', schema: SCHEMA }
  )
))

return { count: results.filter(Boolean).length, records: results }
