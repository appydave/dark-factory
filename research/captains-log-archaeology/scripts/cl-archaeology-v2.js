export const meta = {
  name: 'captains-log-archaeology-calibration-v2',
  description: 'Calibration slice v2: registry-constrained threads + entity dictionary + noise short-circuit + loop registry, over the same fortnight, to prove the fixes before the 6-month run',
  phases: [
    { title: 'Vocab', detail: 'derive thread registry + entity dictionary from run-1 atlas' },
    { title: 'Read', detail: 'readers classify into the registry, short-circuit noise' },
    { title: 'Weave', detail: 'thread atlas + loop registry (ids + lifecycle)' },
    { title: 'Harvest', detail: 'tickets / CL punch-list / brain / ideas / calibration verdict' },
  ],
}

const RUN1 = '/Users/davidcruwys/dev/ad/apps/dark-factory/research/captains-log-archaeology/calibration-2026-07-13'
const OUT = RUN1 + '/v2'

// FIX 2 (partial, deterministic): drop a raw X.md when its X.clean.md twin is present
const raw = Array.isArray(args) ? args : JSON.parse(args)
if (!Array.isArray(raw) || raw.length === 0) throw new Error(`args did not resolve to a non-empty array (got ${typeof args})`)
const cleanBases = new Set(raw.filter(p => p.endsWith('.clean.md')).map(p => p.replace(/\.clean\.md$/, '')))
const paths = raw.filter(p => !(p.endsWith('.md') && !p.endsWith('.clean.md') && cleanBases.has(p.replace(/\.md$/, ''))))
log(`Input ${raw.length} → ${paths.length} after clean/raw twin dedup`)

// ---------- Phase: Vocab (FIX 1 + FIX 3) ----------
phase('Vocab')
const VOCAB = {
  type: 'object',
  properties: {
    threads: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string', description: 'stable kebab id, e.g. captains-log' },
      label: { type: 'string' },
      aliases: { type: 'array', items: { type: 'string' } },
    }, required: ['id', 'label'] } },
    entities: { type: 'array', items: { type: 'object', properties: {
      canonical: { type: 'string' },
      type: { type: 'string', enum: ['person', 'app', 'project', 'org', 'tool', 'concept'] },
      aliases: { type: 'array', items: { type: 'string' } },
    }, required: ['canonical', 'type'] } },
  },
  required: ['threads', 'entities'],
}
const vocab = await agent(
  `Derive a CONTROLLED VOCABULARY from a completed archaeology run so a re-run stops fragmenting labels. Read these run-1 outputs IN FULL:\n- ${RUN1}/01-thread-atlas.md\n- ${RUN1}/04-open-loops.md\n- ${RUN1}/12-brain-improvements.md\n- ${RUN1}/13-idea-register.md\n\nProduce:\n1. threads[]: the canonical thread/area registry. Run-1 fragmented (one Linda engagement got 3 names; extension work got 5). Collapse those into a SMALL set of stable ids (aim ~10-16 threads) with an \`aliases\` list capturing every variant name you saw, so a reader can map free-text back to one id. Include a catch-all \`misc\` and \`personal-noise\`.\n2. entities[]: the canonical entity dictionary — recurring people (David, Ian, Martin, Mary, Jan, Linda, Angela, Lars...), apps (Captain's Log, Dark Factory, KyberAgent, AWB, Switchboard...), projects, orgs, tools — each with aliases/misspellings you observed (e.g. "carbonetics"→Kybernesis, "chiber agent"/"dart factory" mis-hearings). Aim ~30-50 entities.\nReturn ONLY the structured object.`,
  { label: 'derive-vocab', phase: 'Vocab', model: 'fable', schema: VOCAB }
)
const threads = (vocab && vocab.threads) || []
const entities = (vocab && vocab.entities) || []
log(`Vocab: ${threads.length} canonical threads, ${entities.length} entities`)
const threadMenu = threads.map(t => `${t.id} (${t.label})`).join(' | ')
const entityMenu = entities.map(e => e.canonical).join(', ')

// ---------- Phase: Read (registry-constrained + noise short-circuit = FIX 1/3 + FIX 2) ----------
const RECORD = {
  type: 'object',
  properties: {
    file: { type: 'string' },
    date: { type: 'string' },
    source: { type: 'string', enum: ['omi', 'plaud'] },
    thread_id: { type: 'string', description: 'MUST be one of the registry ids, or "new:<kebab-label>" if genuinely none fit' },
    kind: { type: 'string', enum: ['idea', 'decision', 'feedback', 'direction', 'question', 'research', 'meeting', 'personal', 'noise'] },
    essence: { type: 'string' },
    entities: { type: 'array', items: { type: 'string', description: 'canonical names from the dictionary where they match' } },
    actions: { type: 'array', items: { type: 'object', properties: { text: { type: 'string' }, target: { type: 'string' } }, required: ['text'] } },
    loop: { type: 'object', properties: {
      is_open: { type: 'boolean' },
      label: { type: 'string', description: 'short STABLE phrase naming the unresolved item (reuse identical wording across captures so the same loop collides); "" if none' },
    }, required: ['is_open', 'label'] },
    fingerprint: { type: 'string' },
  },
  required: ['file', 'date', 'source', 'thread_id', 'kind', 'essence', 'loop', 'fingerprint'],
}
const BATCH = { type: 'object', properties: { records: { type: 'array', items: RECORD } }, required: ['records'] }

phase('Read')
const SIZE = 15
const chunks = []
for (let i = 0; i < paths.length; i += SIZE) chunks.push(paths.slice(i, i + SIZE))
const batches = await parallel(chunks.map((chunk, idx) => () =>
  agent(
    `Mine a batch of David's voice-capture notes into one record per file. Read EACH file IN FULL.\n\nTHREAD REGISTRY (classify thread_id into ONE of these ids; only use "new:<label>" if truly none fit):\n${threadMenu}\n\nENTITY DICTIONARY (normalize names you find to these canonical forms):\n${entityMenu}\n\nFiles:\n${chunk.map(p => `- ${p}`).join('\n')}\n\nRULES:\n- NOISE SHORT-CIRCUIT: if a capture is ambient/noise (coughing, farewells, errands, empty/"." bodies, background chatter), set kind="noise", give a 3-word essence, leave entities/actions empty, loop.is_open=false — do NOT deep-analyze it.\n- For real captures: essence = decay-proof one sentence; actions = only genuine tickets/decisions, each with a target app/system; loop.label = a STABLE phrase you'd reuse verbatim if the same unresolved thing recurs on another day.\nReturn ONLY the records array.`,
    { label: `read:batch-${idx + 1}`, phase: 'Read', model: 'fable', schema: BATCH }
  )
))
const records = batches.filter(Boolean).flatMap(r => (r && r.records) || [])
if (records.length === 0) throw new Error('Read phase produced 0 records — aborting before weave')
const noise = records.filter(r => r.kind === 'noise').length
log(`Read: ${records.length} records (${noise} noise short-circuited) from ${chunks.length} batches`)

// ---------- Phase: Weave (FIX 4 loop registry) ----------
phase('Weave')
const weave = await agent(
  `Weave the connective fabric from ${records.length} registry-classified records (v2 of a calibration; run-1 lives one dir up). \`mkdir -p ${OUT}\` then Write:\n1. ${OUT}/01-thread-atlas.md — cluster by thread_id (now a controlled registry, so clusters should be clean). Per thread: timeline, evolution, splits/merges, dormant→re-emerged gaps, status.\n2. ${OUT}/02-recurrence.md — cluster on fingerprint within thread; "said X times over N days", ranked.\n3. ${OUT}/03-decision-drift.md — beliefs/plans that changed; superseded-but-current-looking decisions.\n4. ${OUT}/04-loop-registry.md — THE FIX-4 ARTIFACT. Build a real registry: cluster records by loop.label into distinct loops, each with a stable LOOP-ID, first_seen date, last_seen date, mention count, owning thread, and status (open / stale / likely-resolved). Oldest-open first. This replaces run-1's flat boolean.\n\nRECORDS (JSON):\n${JSON.stringify(records)}\n\nReturn a <400-word summary: top 5 threads (with record counts), loudest recurring idea, and the 3 highest-priority open loops from the registry (by age+importance).`,
  { label: 'weave', phase: 'Weave', model: 'fable' }
)

// ---------- Phase: Harvest ----------
phase('Harvest')
const harvest = await agent(
  `Harvest actionable outcomes (v2). You have the records + weave summary. \`mkdir -p ${OUT}\` then Write under ${OUT}/:\n1. 10-tickets.md — deduped, routed, build-ready tickets from actions, grouped by target app/system.\n2. 11-captains-log-punchlist.md — CL product improvements: David's own critiques + what the corpus structurally demands, ranked by leverage.\n3. 12-brain-improvements.md — knowledge to promote to brains; misfiled/cross-project insights.\n4. 13-idea-register.md — novel ideas worth keeping, by theme.\n5. 14-CALIBRATION-NOTES.md — compare v2 to run-1 HONESTLY: did the thread registry stop fragmentation? did the loop registry give loops real identity/lifecycle? did noise short-circuit cleanly? entity normalization quality? What (if anything) still breaks at 1,250/6-month scale — especially the still-undesigned cross-slice merge (how do thread ids + loop ids stay stable ACROSS slices)? Give a crisp GO/NO-GO on the full run.\n\nWEAVE SUMMARY:\n${weave}\n\nRECORDS (JSON):\n${JSON.stringify(records)}\n\nReturn a <350-word summary: tickets by target, top 3 CL improvements, and the headline v2 verdict (is it now ready to scale — yes/no + the single biggest remaining risk).`,
  { label: 'harvest', phase: 'Harvest', model: 'fable' }
)

return { input: raw.length, deduped: paths.length, threads: threads.length, entities: entities.length, records: records.length, noise, weave, harvest, out: OUT }
