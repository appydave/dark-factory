---
name: image-gen
description: Use when a workflow step needs to generate an image via the kie.ai async pattern — POST createTask, poll recordInfo until success, download the result to a local path, and write a JSONL store record with localPath + kieTaskId + prompt. Bash + curl + jq only. Supports flux-schnell (exploration, cheap) and nano-banana-2 (finals, 2K). Bytes are written directly to disk by the worker; the orchestrator only sees a one-line ack and never the image data or kie response bodies.
allowed-tools: Bash
---

# Image-Gen — bash+curl+jq kie.ai wrapper

The image-gen step uses the **kie.ai async pattern**: POST a task, poll for completion, download the resulting URL, write a local-path EAV record. **Image bytes never touch the orchestrator** — the worker writes the file to disk and the store record carries only the path.

## Endpoints

- POST `https://api.kie.ai/api/v1/jobs/createTask` (returns `taskId`)
- GET `https://api.kie.ai/api/v1/jobs/recordInfo?taskId=<id>` (poll for state)
- Authorization: `Bearer $KIE_AI_API_KEY` (sourced from `~/.secrets`)

## Model lanes (two-tier cost strategy)

| Lane | Model | Resolution | ~Cost | Use for |
|------|-------|------------|-------|---------|
| Exploration | `flux-schnell` (Market Models) | 1K → cropped/displayed at 512×288 | ~$0.003 | 6 cheap concepts to compare |
| Finals | `nano-banana-2` (default) | 2K = 2048×1152 | ~$0.04 | 3 production-ready outputs |

Both lanes use `aspect_ratio: "16:9"`, `output_format: "jpg"`.

## The 4-stage worker pattern

```bash
# Stage 1 — Create task
TASK_RESPONSE=$(curl -sS -X POST "https://api.kie.ai/api/v1/jobs/createTask" \
  -H "Authorization: Bearer $KIE_AI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -nc \
        --arg model "$MODEL" \
        --arg prompt "$PROMPT" \
        --arg aspect "16:9" \
        --arg resolution "$RESOLUTION" \
        '{model:$model, input:{prompt:$prompt, aspect_ratio:$aspect, resolution:$resolution, output_format:"jpg"}}')")
TASK_ID=$(echo "$TASK_RESPONSE" | jq -r '.data.taskId')

# Stage 2 — Poll recordInfo until state ∈ {success, completed, failed, error}
for i in $(seq 1 60); do
  sleep 5
  POLL=$(curl -sS -H "Authorization: Bearer $KIE_AI_API_KEY" \
    "https://api.kie.ai/api/v1/jobs/recordInfo?taskId=$TASK_ID")
  STATE=$(echo "$POLL" | jq -r '.data.state // "unknown"')
  case "$STATE" in
    success|completed)
      RESULT_URL=$(echo "$POLL" | jq -r '.data.resultJson' | jq -r '.resultUrls[0]')
      break ;;
    failed|error)
      echo "task failed: $TASK_ID" >&2; exit 1 ;;
  esac
done
[[ -z "$RESULT_URL" ]] && { echo "timeout: $TASK_ID" >&2; exit 1; }

# Stage 3 — Download to local path
curl -sS -o "$OUTPUT_PATH" "$RESULT_URL"
[[ ! -s "$OUTPUT_PATH" ]] && { echo "download empty: $OUTPUT_PATH" >&2; exit 1; }

# Stage 4 — Write store record (localPath, NOT bytes)
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
jq -nc \
  --arg key "$STORE_KEY" \
  --arg group "$GROUP" \
  --argjson index "$INDEX" \
  --arg localPath "$OUTPUT_PATH" \
  --arg taskId "$TASK_ID" \
  --arg model "$MODEL" \
  --arg prompt "$PROMPT" \
  --arg titleRef "$TITLE_REF" \
  --argjson sourceIdx "${SOURCE_EXPLORATION_IDX:-null}" \
  --arg step "$STEP_ID" \
  --arg ts "$TS" \
  '{key:$key, group:$group, index:$index,
    value:{localPath:$localPath, kieTaskId:$taskId, model:$model, prompt:$prompt, title_ref:$titleRef,
           sourceExplorationIdx:(if $sourceIdx==null then null else $sourceIdx end)},
    meta:{step:$step, by:("subagent:"+$step), ts:$ts, attempt:1, status:"ok"}}' \
  >> "$STORE_PATH"

# Stage 5 — Return ONLY a one-line ack to orchestrator
echo "✓ wrote $STORE_KEY index:$INDEX → $(basename $OUTPUT_PATH)"
```

## Hard rules

1. **Never echo image bytes** to the orchestrator. Bytes go directly to `$OUTPUT_PATH` via `curl -o`.
2. **Never include kie.ai response bodies** in the ack or any output. The poll/create responses are JSON — they stay inside the subagent's bash buffer, never bubble up.
3. **Store record carries `localPath` only** — never `data:image/...`, never base64, never inline URL. The download URL is consumed once during stage 3 and discarded.
4. **One record per image.** Use `group` + `index` for collections (e.g. `group:"exploration"`, `index:0..5`).
5. **Title pairing.** For thumbnail workflows, every record MUST carry a `title_ref` field linking back to exactly one `selectedTitles[]` entry. For finals, also carry `sourceExplorationIdx`.

## Worker invocation contract

The conductor dispatches one subagent per image with:
- `STORE_PATH` — path to the workflow's store.jsonl
- `STORE_KEY` — `"explorationImages"` or `"finalImages"`
- `GROUP` — `"exploration"` or `"final"`
- `INDEX` — 0-based position
- `MODEL` — `flux-schnell` or `nano-banana-2`
- `RESOLUTION` — `1K` (exploration) or `2K` (finals)
- `OUTPUT_PATH` — absolute path like `runs/b65/thumbs/exp-1.jpg`
- `PROMPT` — the design-brief prompt text (composed by the conductor from store inputs)
- `TITLE_REF` — exact title string from `selectedTitles[]`
- `SOURCE_EXPLORATION_IDX` — only for finals; identifies the exploration index this final was selected from
- `STEP_ID` — `"explore-cheap-batch"` or `"build-finals"`

Worker runs the 4-stage pattern above. Returns exactly one ack line.

## Negative prompt (default for all lanes)

```
photorealism, human figures, human faces, halftone, newsprint texture, comic-book outlines, 3D render, gradients beyond subtle paper texture, neon colours, watermark, blurry, low quality
```

Append to the prompt body or pass separately depending on model support. For models without explicit negative_prompt input, fold into the main prompt as "avoid: ...".
