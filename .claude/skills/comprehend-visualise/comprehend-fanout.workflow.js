export const meta = {
  name: 'comprehend-fanout',
  description: 'Comprehend a codebase target into Mochaccino-ready data: parallel readers per package + git history, merged into one cited model.',
  phases: [
    { title: 'Enumerate', detail: 'list packages / databases' },
    { title: 'Read', detail: 'one cited reader per package' },
    { title: 'Merge', detail: 'git change story + assemble' },
  ],
}

// args: { target: "<repo/folder path>", host?: "<ssh host for remote>", sinceDays?: 14 }
const target = args?.target
const host = args?.host ? `ssh ${args.host} ` : ''
const sinceDays = args?.sinceDays ?? 14

phase('Enumerate')
const survey = await agent(
  `Enumerate the codebase at ${target} (use ${host}shell read-only). List package/module directories and any databases/schemas. Return JSON.`,
  { label: 'enumerate', schema: { type: 'object', properties: {
      packages: { type: 'array', items: { type: 'string' } },
      databases: { type: 'array', items: { type: 'string' } },
    }, required: ['packages'] } }
)
const packages = (survey?.packages ?? []).slice(0, 24)

phase('Read')
const READ_SCHEMA = { type: 'object', properties: {
  name: { type: 'string' }, what: { type: 'string' },
  key_files: { type: 'array', items: { type: 'string' } },
  deps: { type: 'array', items: { type: 'string' } },
  data_shapes: { type: 'array', items: { type: 'string' } },
  citations: { type: 'array', items: { type: 'string' } },
}, required: ['name', 'what'] }
const digests = await parallel(packages.map(pkg => () =>
  agent(`Read package "${pkg}" under ${target} (use ${host}shell read-only). Return a CITED mini-digest: what it is, key files (path:line), deps, data shapes. Tag claims verified/inference/unknown.`,
    { label: `read:${pkg}`, phase: 'Read', schema: READ_SCHEMA })
))

phase('Merge')
const history = await agent(
  `Run: ${host}git -C ${target} log --since='${sinceDays} days ago' --oneline. Summarise the change story as ordered {sha, summary}. Return JSON.`,
  { label: 'git-history', schema: { type: 'object', properties: {
      changes: { type: 'array', items: { type: 'object', properties: {
        sha: { type: 'string' }, summary: { type: 'string' } } } },
    }, required: ['changes'] } }
)

// Mochaccino-ready model. The skill writes this to .mochaccino/data/NN-*.json with meta.source = target + commit_sha.
return {
  target,
  databases: survey?.databases ?? [],
  packages: digests.filter(Boolean),
  history: history?.changes ?? [],
}
