---
topic: "Workflow args binding failure"
issue: "Dynamic Workflow tool args parameter didn't reliably bind to the script's args global"
created: "2026-06-24"
story_reference: "f85d2bbd"
category: "infrastructure"
severity: "high"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: session
files: [".claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/MEMORY.md", ".claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/project_swagger_lineage.md", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/bmad_mining_wf.js", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/build_args.py", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/build_manifests.py", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/c44_extract.json", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_cluster.py", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_cluster2.py", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_final.py", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_index.py", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_loose.py", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_probe.py", "/private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbdή-903a-4fbe-8806-9f4305e934ed/scratchpad/c44_extract.json", "dev/ad/apps/dark-factory/research/bmad-pattern-mining/bmad-machinery-pattern.md", "dev/ad/apps/dark-factory/research/bmad-pattern-mining/kickoff.md"]
commits: []
---

# Workflow args binding failure — Dynamic Workflow tool args parameter didn't reliably bind to the script's args global

## Problem Signature

**Symptoms**: Run 1 crashed 3 seconds in with `JSON Parse error: Unexpected identifier "The"` — a bootstrap agent read `args.args_path` as `undefined` and returned prose instead of the file's JSON. Run 2 reported `status: completed` but only spawned 2 agents instead of 75, with `clusters_read: 0, queue_read: 0`; the synth prompt literally rendered `WRITE the full spec to: undefined`, `repo (undefined)`, `0 story-run extracts`.

**Environment**: dark-factory app, dynamic multi-agent Workflow tool (background-executed JS orchestration script), invoked with an `args` object at launch.

**Triggering Conditions**: Launching a Workflow script that reads configuration via the `args` global (e.g. `args.manifest_dir`, `args.repo_path`) passed in at tool-invocation time.

## Root Cause
The `args` parameter passed to the Workflow tool call never reached the script's `args` global in this runtime — every `args.<field>` reference resolved to `undefined`, and both failures traced back to the exact same binding bug (the first failure just manifested differently, as a JSON.parse crash instead of an empty-evidence synthesis).

## Solution
Stopped depending on `args` entirely and hardcoded the (fully known) configuration as constants directly in the script body — scratch dir, manifest dir, cluster/queue counts, repo path, skill path, session dir, and output path. The fan-out then executed correctly (75 readers spawned vs. 2).

```diff-before
const MAN = args.manifest_dir
const N_CLUSTERS = args.n_clusters
const N_QUEUE = args.n_queue
const REPO = args.repo_path
const SKILL = args.skill_path
const SESSION_DIR = args.session_dir
const OUT_PATH = args.out_path
log(`Work-list: ${N_CLUSTERS} run-cluster manifests + ${N_QUEUE} queue manifests in ${MAN}`)
```
```diff-after
// CONFIG — hardcoded (the `args` global does not bind reliably in this runtime; values are fixed/known).
const SCRATCH = '/private/tmp/.../scratchpad'
const MAN = `${SCRATCH}/manifests`
const N_CLUSTERS = 71
const N_QUEUE = 4
const REPO = '/Users/<user>/dev/clients/supportsignal/app.supportsignal.com.au'
const SKILL = '/Users/<user>/dev/ad/appydave-plugins/appydave/skills/bmad-story-lifecycle'
const SESSION_DIR = '/Users/<user>/.claude/projects/-Users-<user>-dev-clients-supportsignal-app-supportsignal-com-au'
const OUT_PATH = '/Users/<user>/dev/ad/apps/dark-factory/research/bmad-pattern-mining/bmad-machinery-pattern.md'
```

## Prevention
For dynamic Workflow scripts, do not rely on the `args` launch parameter binding correctly — hardcode known config as constants in the script body, or run a trivial smoke-test step that logs each `args.<field>` value before committing to a full fan-out, so a silent binding failure is caught before it burns a multi-agent run on zero real work.

## Related
- Sessions: f85d2bbd
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): f85d2bbd · 2026-06-24
- **Files** (session-level): .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/MEMORY.md, .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/project_swagger_lineage.md, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/bmad_mining_wf.js, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/build_args.py, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/build_manifests.py, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/c44_extract.json, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_cluster.py, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_cluster2.py, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_final.py, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_index.py, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_loose.py, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbd-903a-4fbe-8806-9f4305e934ed/scratchpad/phase0_probe.py, /private/tmp/claude-501/-Users-davidcruwys-dev-ad-apps-dark-factory/f85d2bbdή-903a-4fbe-8806-9f4305e934ed/scratchpad/c44_extract.json, dev/ad/apps/dark-factory/research/bmad-pattern-mining/bmad-machinery-pattern.md, dev/ad/apps/dark-factory/research/bmad-pattern-mining/kickoff.md
- **Commits** (session-level): —
