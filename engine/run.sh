#!/usr/bin/env bash
# Dark Factory engine runner — the ONE launch path. Run it from engine/:
#   ./run.sh          -> 1 worker  (drain one ticket)
#   ./run.sh 2        -> 2 workers in parallel (need 2+ queued; each in its own git worktree)
#   ./run.sh 2 --teardown   -> extra orchestrator flags pass straight through
# Self-cds (cwd-proof), tees store/orchestrator.log. CAP is 3, enforced by the engine.
# Rare overrides via env: MODEL= MAX_WALL= WORKER_TIMEOUT=
set -uo pipefail
cd "$(dirname "$0")"
POOL=1
if [[ "${1:-}" =~ ^[0-9]+$ ]]; then POOL="$1"; shift; fi
python3 orchestrator.py --pool "$POOL" --model "${MODEL:-sonnet}" \
  --max-wall "${MAX_WALL:-3600}" --worker-timeout "${WORKER_TIMEOUT:-1800}" "$@" \
  2>&1 | tee -a store/orchestrator.log
