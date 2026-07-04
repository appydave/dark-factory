---
topic: "Switchboard event-ingest gap"
issue: "Switchboard has no generic event-ingest endpoint"
created: "2026-06-08"
story_reference: "215b9cee"
category: "architecture"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["experiments/watchtower-engine/bin/dispatch-swagger.sh", "experiments/watchtower-engine/bin/emit-event.sh", "experiments/watchtower-engine/bin/reaper.sh"]
commits: []
---

# Switchboard event-ingest gap — Switchboard has no generic event-ingest endpoint

## Problem Signature

**Symptoms**: While wiring dispatch/teardown telemetry emitters into the engine, inspection of the Switchboard app's routes showed only one inbound HTTP path.

**Environment**: `~/dev/ad/apps/switchboard` (AppySentinel-based comms bus), `src/access/bindings/api-binding.ts`.

**Triggering Conditions**: Attempting to implement DF-3 MVP telemetry per its spec, which stated 'lifecycle events → Switchboard' as the placement-correct transport.

## Root Cause
Switchboard's only inbound binding is `POST /jobs` (:5100), which validates a JobTicket and enqueues it for SSE delivery — a job-queue side-effect, not a generic append-to-log side-effect. There is no `/events`-style ingest endpoint for arbitrary lifecycle telemetry.

## Solution
Built the engine-side emitters against a local, transport-swappable sink instead: `bin/emit-event.sh` appends JSON lines to a local `telemetry/events.jsonl`, with the transport isolated to one `_sink` function so it can later be swapped to curl a Switchboard `/events` endpoint once that binding is added (a separate, Ralphy-in-app job on the switchboard repo, since 'the app owns its features'). Note: this specific engine build was subsequently reverted at the user's request for unrelated process reasons (see the cold-start-dispatch learning), but the architectural finding about Switchboard itself remains valid.

```bash
#!/usr/bin/env bash
# emit-event.sh — DF-3 dispatch-loop telemetry emitter (external, worker-independent).
# TRANSPORT NOTE: today the sink is a local JSONL (telemetry/events.jsonl) — the
# smallest slice that yields metrics with zero cross-app dependency (spec §3.3).
# The placement-correct end state is Switchboard's durable bus; when a generic
# event-ingest endpoint exists, swap ONLY the `_sink` function below to curl it.
set -uo pipefail
BASE="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$BASE/telemetry"
LOG="$LOG_DIR/events.jsonl"
mkdir -p "$LOG_DIR"

EVENT="${1:?event name (dispatched|teardown|...)}"; shift
QID="${1:?queue_id}"; shift
TS="$(date -u +%FT%TZ)"

attrs=""
for kv in "$@"; do
  key="${kv%%=*}"; val="${kv#*=}"
  attrs="$attrs,\"$key\":\"$val\""
done

# _sink — the ONLY transport-aware line. Swap this to curl Switchboard later.
_sink() { printf '%s\n' "$1" >> "$LOG"; }

_sink "{\"ts\":\"$TS\",\"event\":\"$EVENT\",\"queue_id\":\"$QID\"$attrs}"
```

## Prevention
Before designing a telemetry/eventing feature that assumes a shared bus has a given capability, verify the bus's actual inbound routes (read its source, not just its spec-doc description) before committing to the transport in a spec.

## Related
- Sessions: 215b9cee
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 215b9cee · 2026-06-08
- **Files** (candidate-level): experiments/watchtower-engine/bin/dispatch-swagger.sh, experiments/watchtower-engine/bin/emit-event.sh, experiments/watchtower-engine/bin/reaper.sh
- **Commits** (candidate-level): —
