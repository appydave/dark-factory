#!/usr/bin/env bash
# Dark Factory — ONE command, run from engine/:
#   ./run.sh                 run whatever's queued        (1 worker)
#   ./run.sh T1-21           stage T1-21 AND run it       (1 worker)
#   ./run.sh T3-03 T3-04     stage both AND run parallel  (2 workers, worktree-isolated)
#   ./run.sh 2               run what's queued at 2 workers
# Ticket ids (T<n>-<n>, any case) are staged first (lint + empty-run guard). Plain number = pool.
# Self-cds (cwd-proof), tees store/orchestrator.log. CAP 3. Rare overrides: MODEL= MAX_WALL= WORKER_TIMEOUT=
set -o pipefail   # NOT -u: macOS bash 3.2 errors on "${empty_array[@]}" under set -u
cd "$(dirname "$0")"
PROMOTE="../bin/promote-wargame.py"

tickets=(); pool=""; extra=()
for a in "$@"; do
  if [[ "$a" =~ ^[Tt][0-9]+-[0-9]+$ ]]; then
    tickets+=("$(printf '%s' "$a" | tr '[:lower:]' '[:upper:]')")
  elif [[ "$a" =~ ^[0-9]+$ ]]; then
    pool="$a"
  else
    extra+=("$a")
  fi
done

# stage any tickets named on the command line (promote-wargame lints + guards)
if (( ${#tickets[@]} )); then
  python3 "$PROMOTE" go --quiet "${tickets[@]}" || { echo "run.sh: nothing staged — not launching."; exit 1; }
fi

# pool: explicit number wins; else size to ticket count; else 1. Capped at 3.
if [[ -z "$pool" ]]; then
  (( ${#tickets[@]} > 1 )) && pool="${#tickets[@]}" || pool=1
fi
(( pool > 3 )) && pool=3

python3 orchestrator.py --pool "$pool" --model "${MODEL:-sonnet}" \
  --max-wall "${MAX_WALL:-3600}" --worker-timeout "${WORKER_TIMEOUT:-1800}" "${extra[@]}" \
  2>&1 | tee -a store/orchestrator.log
