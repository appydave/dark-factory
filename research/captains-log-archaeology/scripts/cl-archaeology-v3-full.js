export const meta = {
  name: 'captains-log-archaeology-full-6mo',
  description: 'Full 6-month run: 1250 captures newest-first, durable per-batch record writes, map-reduce merge into timeline + recency/supersession-aware live tickets',
  phases: [
    { title: 'Vocab', detail: 'freeze a shared thread registry + entity dictionary (seeded from v2)' },
    { title: 'Extract', detail: '84 Fable readers, newest-first, each writes durable JSONL records' },
    { title: 'ThreadAtlas', detail: 'one agent per thread writes its 6-month timeline' },
    { title: 'Loops+Tickets', detail: 'loop registry + recency/supersession-aware live tickets by target' },
    { title: 'Summary', detail: 'executive summary across the whole corpus' },
  ],
}

const A = typeof args === 'string' ? JSON.parse(args) : args
const RUN = A.runDir
const N = A.batchCount
const V2 = '/Users/davidcruwys/dev/ad/apps/dark-factory/research/captains-log-archaeology/calibration-2026-07-13/v2'
if (!RUN || !N) throw new Error(`need {runDir, batchCount}; got ${JSON.stringify(args)}`)
const pad = (i) => String(i).padStart(3, '0')

// ---------- Vocab ----------
phase('Vocab')
const VOCAB = {
  type: 'object',
  properties: {
    threads: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, label: { type: 'string' }, aliases: { type: 'array', items: { type: 'string' } } }, required: ['id', 'label'] } },
    entities: { type: 'array', items: { type: 'object', properties: { canonical: { type: 'string' }, type: { type: 'string' }, aliases: { type: 'array', items: { type: 'string' } } }, required: ['canonical'] } },
  },
  required: ['threads', 'entities'],
}
const vocab = await agent(
  `Freeze a controlled vocabulary that will be used to classify SIX MONTHS (Jan–Jul 2026) of David's voice captures. Read the proven 2-week vocab as a seed:\n- ${V2}/01-thread-atlas.md\n- ${V2}/04-loop-registry.md\nThe seed covers only the recent fortnight. This registry covers Jan–Jul, so it must ALSO anticipate older threads not in the seed: early OMI/device onboarding, personal/health/family, travel/visa, earlier client work, content/YouTube production, brand/business strategy, meetups/learning. Produce ~18-26 canonical threads (stable kebab ids + aliases), plus a \`misc\` and \`personal-noise\` catch-all; and ~40-70 canonical entities with alias/misspelling lists (people, apps, projects, orgs, tools). Return ONLY the object.`,
  { label: 'derive-vocab', phase: 'Vocab', model: 'fable', schema: VOCAB }
)
const threads = (vocab && vocab.threads) || []
const entities = (vocab && vocab.entities) || []
const threadMenu = threads.map(t => `${t.id}`).join(' | ')
const entityMenu = entities.map(e => e.canonical).join(', ')
log(`Vocab frozen: ${threads.length} threads, ${entities.length} entities`)

// ---------- Extract (durable) ----------
const RECORD = {
  type: 'object',
  properties: {
    file: { type: 'string' }, date: { type: 'string' }, source: { type: 'string' },
    thread_id: { type: 'string', description: 'a registry id, or new:<kebab> if none fit' },
    kind: { type: 'string', enum: ['idea', 'decision', 'feedback', 'direction', 'question', 'research', 'meeting', 'personal', 'noise'] },
    essence: { type: 'string' },
    entities: { type: 'array', items: { type: 'string' } },
    actions: { type: 'array', items: { type: 'object', properties: { text: { type: 'string' }, target: { type: 'string' } }, required: ['text'] } },
    loop: { type: 'object', properties: { is_open: { type: 'boolean' }, label: { type: 'string' } }, required: ['is_open', 'label'] },
    fingerprint: { type: 'string' },
  },
  required: ['file', 'date', 'source', 'thread_id', 'kind', 'essence', 'loop'],
}
const BATCH = { type: 'object', properties: { records: { type: 'array', items: RECORD } }, required: ['records'] }

phase('Extract')
const batchIdx = Array.from({ length: N }, (_, i) => i)
const extracted = await parallel(batchIdx.map((i) => () => {
  const batchFile = `${RUN}/batches/batch-${pad(i)}`
  const outFile = `${RUN}/records/batch-${pad(i)}.jsonl`
  return agent(
    `Extract one record per capture. STEP 1: Read the batch manifest ${batchFile} — it lists ~15 absolute capture paths, one per line. STEP 2: Read EACH capture file in full. STEP 3: emit one record per capture.\n\nTHREAD REGISTRY (classify thread_id to ONE id; use new:<kebab> only if truly none fit):\n${threadMenu}\nENTITY DICTIONARY (normalize to these):\n${entityMenu}\n\nRULES:\n- NOISE SHORT-CIRCUIT: ambient/farewell/errand/empty(".")/background → kind="noise", 3-word essence, empty entities/actions, loop.is_open=false. Do not deep-analyze.\n- Real captures: decay-proof one-sentence essence; actions = genuine tickets/decisions only, each with a target app/system; loop.label = a STABLE phrase reused verbatim if the same unresolved thing recurs.\n- Use the DATE from the capture's frontmatter/filename (YYYY-MM-DD).\nSTEP 4 (durable): also write your records as JSONL (one JSON object per line) to ${outFile} using the Write tool, so the work survives even if the run stops.\nReturn the records array.`,
    { label: `extract:${pad(i)}`, phase: 'Extract', model: 'fable', schema: BATCH }
  )
}))
const all = extracted.filter(Boolean).flatMap(r => (r && r.records) || []).filter(r => r && r.date && r.thread_id)
all.sort((a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : 0))
if (all.length === 0) throw new Error('Extract produced 0 records — aborting (durable JSONLs may still exist in records/)')
const noise = all.filter(r => r.kind === 'noise').length
log(`Extracted ${all.length} records (${noise} noise) from ${N} batches; ${all[0].date} → ${all[all.length - 1].date}`)

// deterministic grouping (pure JS)
const byThread = {}
all.forEach(r => { (byThread[r.thread_id] = byThread[r.thread_id] || []).push(r) })
const byLoop = {}
all.forEach(r => { if (r.loop && r.loop.is_open && r.loop.label) { const k = r.loop.label.toLowerCase().trim(); (byLoop[k] = byLoop[k] || []).push(r) } })
const loopTable = Object.entries(byLoop).map(([label, rs]) => ({ label, first: rs[0].date, last: rs[rs.length - 1].date, count: rs.length, threads: [...new Set(rs.map(r => r.thread_id))], recent: rs.slice(-2).map(r => `${r.date}: ${r.essence}`) })).sort((a, b) => b.count - a.count)
const actions = []
all.forEach(r => (r.actions || []).forEach(a => actions.push({ text: a.text, target: a.target || 'unassigned', date: r.date, thread: r.thread_id })))
const byTarget = {}
actions.forEach(a => { (byTarget[a.target] = byTarget[a.target] || []).push(a) })
const targetsRanked = Object.entries(byTarget).sort((a, b) => b[1].length - a[1].length)
const topTargets = targetsRanked.slice(0, 12)
const threadCounts = Object.entries(byThread).map(([id, rs]) => `${id}: ${rs.length} (${rs[0].date}→${rs[rs.length - 1].date})`).sort()

// ---------- ThreadAtlas (fan-out per thread) ----------
phase('ThreadAtlas')
const bigThreads = Object.entries(byThread).filter(([id]) => id !== 'personal-noise').sort((a, b) => b[1].length - a[1].length)
await parallel(bigThreads.map(([id, rs]) => () =>
  agent(
    `Write the 6-month timeline for ONE thread of David's captures. Thread id: "${id}" (${rs.length} records, chronological). \`mkdir -p ${RUN}/threads\` then Write ${RUN}/threads/${id.replace(/[^a-z0-9-]/gi, '_')}.md: a dated narrative — how this thread STARTED, EVOLVED, SPLIT/MERGED, went DORMANT and RE-EMERGED, and its CURRENT status. Call out superseded decisions. Records JSON:\n${JSON.stringify(rs.map(r => ({ date: r.date, kind: r.kind, essence: r.essence, loop: r.loop && r.loop.is_open ? r.loop.label : null })))}\nReturn a 2-sentence status line for this thread.`,
    { label: `atlas:${id}`, phase: 'ThreadAtlas', model: 'fable' }
  )
))

// ---------- Loops + Tickets ----------
phase('Loops+Tickets')
const loopAndTickets = await parallel([
  () => agent(
    `Build the 6-MONTH LOOP REGISTRY from this deterministically-clustered table of OPEN loops (already grouped by stable label with first/last-seen + count computed from real dates). Assign each a LOOP-ID, a status (open / stale / likely-resolved / superseded), and a priority (age × importance). Oldest-open-important first. \`mkdir -p ${RUN}\` then Write ${RUN}/loop-registry.md. Loop table JSON:\n${JSON.stringify(loopTable)}\nReturn the top 5 highest-priority live loops as a list.`,
    { label: 'loop-registry', phase: 'Loops+Tickets', model: 'fable' }
  ),
  ...topTargets.map(([target, acts]) => () =>
    agent(
      `Produce a RECENCY & SUPERSESSION-AWARE ticket list for target "${target}" from ${acts.length} raw actions extracted across 6 months (each has a date). \`mkdir -p ${RUN}/tickets\` then Write ${RUN}/tickets/${target.replace(/[^a-z0-9-]/gi, '_').slice(0, 40)}.md. CRITICAL: dedupe; for each resulting ticket mark status = LIVE (recent & still valid), STALE (old, unvalidated — needs a David yes/no before doing), SUPERSEDED (a later action replaced it), or LIKELY-DONE. Only LIVE ones are presented as actionable; the rest are listed separately with their age. Actions JSON:\n${JSON.stringify(acts)}\nReturn: count of LIVE vs STALE vs SUPERSEDED for this target.`,
      { label: `tickets:${target.slice(0, 20)}`, phase: 'Loops+Tickets', model: 'fable' }
    )
  ),
])

// ---------- Summary ----------
phase('Summary')
const summary = await agent(
  `Write the top-level executive summary of David's 6-month Captain's Log archaeology (${all.length} captures, ${all[0].date}→${all[all.length - 1].date}). \`mkdir -p ${RUN}\` then Write ${RUN}/00-EXECUTIVE-SUMMARY.md covering: the biggest threads by weight; the hottest LIVE open loops (deadlines, revenue, blockers); how many live vs stale/superseded tickets exist and where; the clearest decision-drifts; and the 5 things you'd tell David to act on FIRST. Inputs:\nTHREAD SIZES:\n${threadCounts.join('\n')}\nTOP LOOPS:\n${JSON.stringify(loopTable.slice(0, 20))}\nTICKET TARGETS (by volume):\n${targetsRanked.map(([t, a]) => `${t}: ${a.length}`).join(', ')}\nLOOP+TICKET AGENT SUMMARIES:\n${loopAndTickets.filter(Boolean).join('\n---\n').slice(0, 6000)}\nReturn a <250-word headline summary for David.`,
  { label: 'exec-summary', phase: 'Summary', model: 'fable' }
)

return { captures: all.length, noise, threads: threads.length, entities: entities.length, dateRange: `${all[0].date}→${all[all.length - 1].date}`, liveThreads: bigThreads.length, loops: loopTable.length, ticketTargets: targetsRanked.length, out: RUN, summary }
