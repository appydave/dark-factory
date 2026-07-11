#!/usr/bin/env bash
# Dark Factory engine runner — the ONE launch path for the orchestrator.
# Self-cds so it is cwd-proof (run it from anywhere), tees a readable log, and passes
# any extra flags straight through. Defaults match the war-game run profile.
#   ./run.sh                    # pool 1, sonnet, max-wall 3600, worker-timeout 1800
#   POOL=2 ./run.sh             # env-var override (POOL / MODEL / MAX_WALL / WORKER_TIMEOUT)
#   ./run.sh --teardown         # extra flags pass through to orchestrator.py
set -uo pipefail
cd "$(dirname "$0")"
python3 orchestrator.py \
  --pool "${POOL:-1}" --model "${MODEL:-sonnet}" \
  --max-wall "${MAX_WALL:-3600}" --worker-timeout "${WORKER_TIMEOUT:-1800}" "$@" \
  2>&1 | tee -a store/orchestrator.log
