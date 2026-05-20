---
name: store
description: Use when a workflow step needs to append an EAV record to a JSONL store, recall the current projected value of a key, or project the full store into a JSON view. Implements the durable blackboard store from blackboard-workflow-pattern.md §4. Backend is a JSONL file on disk.
allowed-tools: Bash
---

# Store — bash+jq JSONL blackboard operations

The store is an **append-only JSONL file**. Every line is one EAV record. Reads project the log (last-write-wins per key). Never mutate existing lines.

## Record envelope (§11.3)

```json
{
  "key": "<string>",
  "group": null,
  "index": null,
  "value": <any JSON>,
  "meta": {
    "step": "<step-id>",
    "by": "subagent:<step-id>",
    "ts": "<ISO-8601>",
    "attempt": 1,
    "status": "ok"
  }
}
```

## Operations

### remember — append one record

```bash
# Usage: remember STORE_PATH KEY VALUE_JSON STEP_ID
# VALUE_JSON must be a valid JSON string (use jq to escape if needed)
remember() {
  local store_path="$1" key="$2" value_json="$3" step_id="$4"
  local ts
  ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local record
  record=$(jq -nc \
    --arg key "$key" \
    --argjson value "$value_json" \
    --arg step "$step_id" \
    --arg ts "$ts" \
    '{key: $key, group: null, index: null, value: $value, meta: {step: $step, by: ("subagent:" + $step), ts: $ts, attempt: 1, status: "ok"}}')
  echo "$record" >> "$store_path"
  echo "✓ wrote $key to $(basename $store_path)"
}
```

Inline (no function — for subagent bash blocks):

```bash
STORE_PATH="..."
KEY="mainTopic"
VALUE_JSON='"some extracted text"'   # must be valid JSON
STEP_ID="analyze-main-topic"
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
jq -nc \
  --arg key "$KEY" \
  --argjson value "$VALUE_JSON" \
  --arg step "$STEP_ID" \
  --arg ts "$TS" \
  '{key:$key,group:null,index:null,value:$value,meta:{step:$step,by:("subagent:"+$step),ts:$ts,attempt:1,status:"ok"}}' \
  >> "$STORE_PATH"
echo "✓ wrote $KEY"
```

### recall — project the current value of a key (last-write-wins)

```bash
# Usage: recall STORE_PATH KEY
recall() {
  local store_path="$1" key="$2"
  jq -r --arg key "$key" 'select(.key == $key) | .value' "$store_path" | tail -1
}
```

Inline:

```bash
jq -r --arg key "mainTopic" 'select(.key == $key) | .value' "$STORE_PATH" | tail -1
```

### project — fold the full log into store.view.json (≥12 top-level keys)

```bash
# Usage: project STORE_PATH VIEW_PATH
# Result: one JSON object with each key set to its last-written value.
project() {
  local store_path="$1" view_path="$2"
  jq -s '
    reduce .[] as $r ({};
      . + {($r.key): $r.value}
    )
  ' "$store_path" > "$view_path"
  echo "✓ projected $(jq -r keys_unsorted[] "$view_path" | wc -l | tr -d " ") keys to $(basename $view_path)"
}
```

Inline:

```bash
jq -s 'reduce .[] as $r ({}; . + {($r.key): $r.value})' "$STORE_PATH" > "$VIEW_PATH"
```

## Contract for write-store-directly workers

A worker using this store must:
1. Read its inputs from the declared input paths (never from orchestrator context).
2. Compute its output.
3. Append **exactly one** EAV record to `STORE_PATH` using the inline `remember` block above.
4. Return a single-line ack to the orchestrator: `✓ wrote <key> to store.jsonl`.
5. **Never** return the extracted payload to the orchestrator.

This enforces §3.3 write-store-directly — the orchestrator sees only the ack, not the payload.

## Validation

After all steps complete, verify the store:

```bash
# All records have required EAV fields
jq -c 'select(.key and .value != null and .meta.step and .meta.ts and .meta.by)' "$STORE_PATH" | wc -l
# Should equal total line count of store.jsonl

# All 12 keys present
jq -r '.key' "$STORE_PATH" | sort -u
```
