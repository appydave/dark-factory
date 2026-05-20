# YLO Experiment — Blackboard Workflow Probe

Minimal bash+jq instantiation of the **blackboard workflow pattern** (see `~/dev/ad/brains/anthropic-claude/claude-code/blackboard-workflow-pattern.md`). Runs the Bulk Content Analysis sub-workflow against a video transcript.

## What this is

This is **Test #1** of the blackboard pattern. It proves that 12 parallel content-analysis steps can run with:
- The orchestrator (main Claude Code session) **never ingesting transcript content or extraction payloads**
- Each worker running in **clean context** (isolated subagent)
- Results written **directly to the JSONL store** by workers (write-store-directly contract)
- The store as the **single source of truth**, not the orchestrator's memory

## Directory layout

```
ylo-experiment/
├── workflow.json          ← 12-step workflow spec (§11.1 shape)
├── prompts/               ← 12 .hbs prompt files lifted verbatim from AWB Gen 3
│   └── analyze-*.hbs
├── runs/
│   └── b65/               ← per-video outputs
│       ├── transcript.txt ← SRT concatenation, timestamps stripped
│       ├── store.jsonl    ← append-only EAV store (14 records: 2 seeds + 12 steps)
│       ├── store.view.json← projected snapshot (14 top-level keys)
│       ├── conductor-session.log ← orchestrator log (no payloads, no transcript)
│       └── run-summary.md ← run summary
└── README.md              ← this file
```

Skills (project-local, not in appydave-plugins):
```
.claude/skills/store/SKILL.md      ← remember/recall/project operations
.claude/skills/conductor/SKILL.md  ← §5 orchestrator loop
```

## How to re-run

1. Delete or move `runs/b65/store.jsonl` (keep `transcript.txt`).
2. In a Claude Code session in this directory, activate the conductor skill.
3. Seed the store:
   ```bash
   STORE_PATH=runs/b65/store.jsonl
   TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
   jq -nc --arg k "videoId" --arg v "b65" --arg ts "$TS" \
     '{key:$k,group:null,index:null,value:$v,meta:{step:"seed",by:"conductor",ts:$ts,attempt:1,status:"ok"}}' >> "$STORE_PATH"
   jq -nc --arg k "transcriptPath" --arg v "$(pwd)/runs/b65/transcript.txt" --arg ts "$TS" \
     '{key:$k,group:null,index:null,value:$v,meta:{step:"seed",by:"conductor",ts:$ts,attempt:1,status:"ok"}}' >> "$STORE_PATH"
   ```
4. Dispatch all 12 analysis workers in parallel (Agent tool, write-store-directly contract).
5. Project: `jq -s 'reduce .[] as $r ({}; . + {($r.key): $r.value})' runs/b65/store.jsonl > runs/b65/store.view.json`

## Where the store lives

`runs/<videoId>/store.jsonl` — one directory per video. Append-only JSONL. Each line is one EAV record (`{key, group, index, value, meta: {step, by, ts, attempt, status}}`).

## How to extend to other workflows

1. Add a new directory under `runs/` for the new video.
2. Concatenate its SRT files (strip timestamps) into `runs/<id>/transcript.txt`.
3. Copy `workflow.json` if reusing the same 12-step analysis, or create a new workflow spec.
4. Seed the store with `videoId` and `transcriptPath`.
5. Dispatch workers per the conductor skill.

To add a new workflow (e.g. Title Generation): create a new `workflow-title.json` with the additional steps. Each step declares its `inputs` (keys that must exist in the store before it can run) and `stores` (the key it writes). The conductor resolves these at dispatch time.

## Verification commands

```bash
# Step count
jq '.steps | length' workflow.json          # → 12

# Prompt files
ls prompts/analyze-*.hbs | wc -l            # → 12

# Store record count
wc -l < runs/b65/store.jsonl                # → ≥12

# EAV validation
jq -c 'select(.key and .value != null and .meta.step and .meta.ts and .meta.by)' \
  runs/b65/store.jsonl | wc -l              # → equals total lines

# All 12 keys present
jq -r '.key' runs/b65/store.jsonl | sort -u

# View keys
jq 'keys | length' runs/b65/store.view.json # → ≥12

# No TypeScript/Python in implementation
find ylo-experiment .claude/skills/store .claude/skills/conductor \
  -name "*.ts" -o -name "*.py" -o -name "*.js" -o -name "*.tsx"  # → empty

# No transcript fragments in conductor log
head -c 200 runs/b65/transcript.txt > /tmp/probe
grep -Ff /tmp/probe runs/b65/conductor-session.log | wc -l  # → 0
```
