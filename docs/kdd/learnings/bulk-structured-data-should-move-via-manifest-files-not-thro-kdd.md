---
topic: "Bulk data via manifest files, not LLM"
issue: "Bulk structured data should move via manifest files, not through an LLM agent"
created: "2026-06-24"
story_reference: "f85d2bbd"
category: "architecture"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: session
files: [".claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/MEMORY.md", ".claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/project_swagger_lineage.md", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/bmad_mining_wf.js", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/build_args.py", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/build_manifests.py", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/c44_extract.json", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_cluster.py", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_cluster2.py", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_final.py", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_index.py", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_loose.py", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_probe.py", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbdή-903a-4fbe-8806-9f4305e934ed/scratchpad/c44_extract.json", "dev/ad/apps/dark-factory/research/bmad-pattern-mining/bmad-machinery-pattern.md", "dev/ad/apps/dark-factory/research/bmad-pattern-mining/kickoff.md"]
commits: []
---

# Bulk data via manifest files, not LLM — Bulk structured data should move via manifest files, not through an LLM agent

## Problem Signature

**Symptoms**: The bootstrap agent, asked to "Read the file and output its ENTIRE contents VERBATIM as raw JSON only", instead returned prose beginning with "The...", which crashed `JSON.parse`.

**Environment**: dark-factory app, dynamic Workflow fan-out mining ~650 Claude Code session JSONL transcripts across 71 clusters.

**Triggering Conditions**: Needing to hand a large per-cluster work-list (session UUIDs + roles) to a Workflow's fan-out readers, where each reader only needs its own slice of the data.

## Root Cause
LLM agents paraphrase/summarize rather than verbatim-echo large content, so using an agent step as a data-passthrough is inherently lossy; the same design also routed hundreds of session UUIDs through an LLM, risking silent transcription errors on IDs that must be exact.

## Solution
Replaced the single 64KB inline/agent-relayed work-list with 75 small manifest files written to disk (`manifests/cluster-00.txt` … `cluster-70.txt`, `queue-0.txt` … `queue-3.txt`), each listing KEY/BUCKET/STAGES/SPAN plus one `role  full-path-to-.jsonl` line per session. Each reader agent's prompt was changed to read its own manifest file directly via a tool call as its first step — no UUID or bulk data passes through an intermediary LLM at all.

```diff-before
phase('Bootstrap')
const ARGS_PATH = args.args_path
const raw = await agent(
  `Read the file ${ARGS_PATH} and output its ENTIRE contents VERBATIM as raw JSON only. ` +
  `No markdown fences, no commentary, no truncation — the very first character must be '{' and the last '}'.`,
  { label: 'load-worklist' }
)
let DATA
try {
  DATA = JSON.parse(raw.trim().replace(/^```(json)?/,'').replace(/```$/,'').trim())
} catch (e) {
  throw new Error('bootstrap JSON parse failed: ' + e.message)
}
```
```diff-after
// Work-list lives on disk as per-cluster manifest files. Each manifest lists KEY/BUCKET/STAGES
// + role->session-path lines. Readers read their own manifest, so session UUIDs never pass
// through an LLM or the args (zero transcription risk).
function readerPrompt(manifestPath) {
  return `... STEP 1 — Read your manifest FIRST: ${manifestPath}
 It lists KEY (story id), BUCKET, STAGES, SPAN, and one line per session as
 "role  full-path-to-.jsonl" ... Then read every session file listed.`
}
```
```
# manifest writer (python)
for i,c in enumerate(a['clusters']):
    lines=[f"KEY: {c['key']}", f"BUCKET: {c['bucket']}", f"STAGES: {','.join(c['stages'])}",
           f"SPAN: {'-'.join(x for x in c['span'] if x)}", "SESSIONS (role  full-path):"]
    for m in c['members']:
        lines.append(f"  {m['role']}  {DIR}/{m['sid']}.jsonl")
    open(f"{MAN}/cluster-{i:02d}.txt","w").write("\n".join(lines)+"\n")
```

## Prevention
When a Workflow's readers each need a distinct slice of a large work-list, write one manifest file per item to disk and have each reader read its own file directly — never funnel bulk or ID-bearing data (UUIDs, paths, large JSON) through an LLM agent as a relay step.

## Related
- Sessions: f85d2bbd
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): f85d2bbd · 2026-06-24
- **Files** (session-level): .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/MEMORY.md, .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/project_swagger_lineage.md, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/bmad_mining_wf.js, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/build_args.py, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/build_manifests.py, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/c44_extract.json, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_cluster.py, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_cluster2.py, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_final.py, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_index.py, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_loose.py, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_probe.py, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbdή-903a-4fbe-8806-9f4305e934ed/scratchpad/c44_extract.json, dev/ad/apps/dark-factory/research/bmad-pattern-mining/bmad-machinery-pattern.md, dev/ad/apps/dark-factory/research/bmad-pattern-mining/kickoff.md
- **Commits** (session-level): —
