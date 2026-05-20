---
name: conductor
description: Use when executing a blackboard workflow — load workflow.json, resolve inputs from the store, spawn write-store-directly subagents for each transform step, and loop until all steps are complete. Implements the §5 orchestrator loop from blackboard-workflow-pattern.md. The main Claude Code session IS the conductor; this skill describes its role and obligations.
allowed-tools: Bash, Agent
---

# Conductor — §5 Orchestrator Loop

The conductor is **not a separate process**. It is the role the main Claude Code session plays when running a blackboard workflow. This skill defines that role and its hard constraints.

## The §5 Loop

```
load workflow.json                          # spec: steps, store paths, seed
load store projection (keys only — NOT payloads)
while steps remain:
  pick next step whose inputs are satisfied
  resolve step.inputs from the store        ← THE ISOLATION BOUNDARY
  switch step.type:
    transform | action:                     # automated
      render prompt from step.promptFile with resolvedInputs
      spawn SUBAGENT:
        - clean context (no parent history)
        - prompt = rendered prompt
        - task = "read transcript, analyze, write result to store key <step.stores>"
        - store = { backend: jsonl, path: STORE_PATH }
        - contract = write-store-directly
      await one-line ack from subagent
      log ack to conductor-session.log      # ONE LINE ONLY — no payloads
    elicit | checkpoint:
      present relevant key(s) to human; await response
  append result record(s) to store
  loop
on completion:
  project store → store.view.json
  write run-summary.md
```

## Hard constraints (load-bearing — do not relax)

1. **The orchestrator NEVER ingests full step payloads.** Workers write store directly; orchestrator sees only one-line acks. Violating this causes the Oscar failure (context poisoning).
2. **The orchestrator NEVER reads the transcript.** The transcript path is passed to subagents; subagents read it. The orchestrator holds only the path string.
3. **conductor-session.log contains only**: step dispatches, ack records, timing, error flags. No transcript fragments. No extraction text.
4. **Each subagent has a clean context.** No subagent inherits the parent conversation history.
5. **Parallel fan-out**: all 12 Bulk Content Analysis steps share only `transcriptPath` as input and write to distinct keys. Spawn all 12 concurrently (Agent tool, parallel calls).

## Subagent task template (write-store-directly)

Dispatch each subagent with a prompt in this form:

```
You are a content analysis worker. Your task is to analyze a transcript and extract [FIELD_NAME].

Do NOT return the extracted content to me. Instead, write it directly to the store file using bash.

Inputs:
  Transcript path: [TRANSCRIPT_PATH]
  Store path: [STORE_PATH]
  Step ID: [STEP_ID]
  Store key to write: [STORE_KEY]

Instructions:
1. Read the transcript: TRANSCRIPT=$(cat "[TRANSCRIPT_PATH]")
2. Analyze the transcript using the following prompt:
   [RENDERED_PROMPT_BODY — with {{transcriptAbridgement}} replaced by the transcript content]
3. Parse the JSON result.
4. Write the value to the store using this exact bash:

TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
jq -nc \
  --arg key "[STORE_KEY]" \
  --argjson value VALUE_FROM_STEP_2 \
  --arg step "[STEP_ID]" \
  --arg ts "$TS" \
  '{key:$key,group:null,index:null,value:$value,meta:{step:$step,by:("subagent:"+$step),ts:$ts,attempt:1,status:"ok"}}' \
  >> "[STORE_PATH]"

5. Return ONLY this one-line ack: "✓ wrote [STORE_KEY] to store.jsonl"
```

## Conductor-session.log format

Write one line per event:

```
[ISO-TS] DISPATCH step=analyze-main-topic key=mainTopic
[ISO-TS] ACK      step=analyze-main-topic key=mainTopic status=ok
[ISO-TS] DISPATCH step=analyze-keywords   key=keywords
[ISO-TS] ACK      step=analyze-keywords   key=keywords   status=ok
...
[ISO-TS] PROJECT  keys=12 view=store.view.json
[ISO-TS] DONE     elapsed=Xs steps=12 keys=12
```

Never write payload content to this log.

## Input resolution (isolation boundary)

The orchestrator resolves inputs by looking up keys in the store **projection** (not the raw log). For the Bulk Content Analysis sub-workflow, all 12 steps share the same resolved input:

```bash
TRANSCRIPT_PATH=$(jq -r '.value' <(jq -c 'select(.key == "transcriptPath")' "$STORE_PATH" | tail -1))
```

This gives the orchestrator only a file path — not the transcript content.

## Store seeding (before loop starts)

Seed the store with the two required keys before dispatching any steps:

```bash
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
# Seed videoId
jq -nc --arg k "videoId" --arg v "b65" --arg ts "$TS" \
  '{key:$k,group:null,index:null,value:$v,meta:{step:"seed",by:"conductor",ts:$ts,attempt:1,status:"ok"}}' \
  >> "$STORE_PATH"
# Seed transcriptPath
jq -nc --arg k "transcriptPath" --arg v "$TRANSCRIPT_PATH" --arg ts "$TS" \
  '{key:$k,group:null,index:null,value:$v,meta:{step:"seed",by:"conductor",ts:$ts,attempt:1,status:"ok"}}' \
  >> "$STORE_PATH"
```

## Resumability

The workflow is resumable from any point: re-load the store projection, identify which keys are already present, skip those steps, continue with unsatisfied steps. The store is the source of truth — not the orchestrator's memory.
