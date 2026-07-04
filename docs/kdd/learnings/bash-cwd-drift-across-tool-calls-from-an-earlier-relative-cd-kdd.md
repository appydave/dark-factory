---
topic: "Bash cwd drift across tool calls"
issue: "Bash cwd drift across tool calls from an earlier relative cd"
created: "2026-06-06"
story_reference: "bb4024fd"
category: "tooling"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["experiments/watchtower-board/", "experiments/watchtower-engine/"]
commits: []
---

# Bash cwd drift across tool calls — Bash cwd drift across tool calls from an earlier relative cd

## Problem Signature

**Symptoms**: `cd experiments/watchtower-board && node --check server.mjs ...` failed with `no such file or directory: experiments/watchtower-board`; running `pwd` afterward showed the shell was already sitting inside `experiments/watchtower-board` from an earlier command. A prior `mkdir -p experiments/watchtower-engine/proof experiments/watchtower-engine/reports`, run against that same drifted cwd, had created a nested duplicate `experiments/watchtower-board/experiments/watchtower-engine/{proof,reports}` instead of the real `experiments/watchtower-engine/{proof,reports}`.

**Environment**: Dark Factory repo, experiments/watchtower-board + experiments/watchtower-engine, Swagger job-agent session running the run-next-workflow ticket processor

**Triggering Conditions**: The Bash tool's working directory persists between calls within a session (shell state does not). An earlier `cd experiments/watchtower-board` left the cwd inside that subfolder; a later command assumed cwd was repo root and used a relative path (`experiments/watchtower-engine/...`) instead of confirming or using an absolute path.

## Root Cause
Assumed the working directory was still the repo root after several intervening tool calls, but it had drifted to `experiments/watchtower-board` from an earlier `cd`. The subsequent relative-path `mkdir -p` resolved against the drifted cwd, silently creating a misplaced nested tree rather than erroring.

## Solution
Ran `pwd` to reveal the actual cwd, confirmed the misplaced nested tree at `experiments/watchtower-board/experiments/watchtower-engine`, removed it with `rm -rf`, then switched to a single absolute `cd /Users/davidcruwys/dev/ad/apps/dark-factory && ...` for the remaining bookkeeping (run record write, proof file, moving the queue entry to `done/`) so cwd could no longer drift silently.

```bash
# failed relative-path check — cwd had already drifted
cd experiments/watchtower-board && node --check server.mjs && echo "server.mjs OK" && node --check parse-concepts.mjs && echo "parse-concepts.mjs OK" && node parse-concepts.mjs
# => Exit code 1
# => (eval):cd:1: no such file or directory: experiments/watchtower-board
```

```bash
# diagnose + clean up the misplaced nested tree
pwd; echo "=== wrong dirs created here? ==="; ls -la /Users/davidcruwys/dev/ad/apps/dark-factory/experiments/watchtower-board/experiments 2>/dev/null && rm -rf /Users/davidcruwys/dev/ad/apps/dark-factory/experiments/watchtower-board/experiments
# =>
# /Users/davidcruwys/dev/ad/apps/dark-factory/experiments/watchtower-board
# === wrong dirs created here? ===
# total 0
# drwxr-xr-x   3 davidcruwys  staff   96 Jun  6 18:58 .
# drwxr-xr-x   7 davidcruwys  staff  224 Jun  6 18:58 ..
# drwxr-xr-x   4 davidcruwys  staff  128 Jun  6 18:58 watchtower-engine
# removed misplaced tree
```

```bash
# recovery: pin an absolute cwd for the rest of the bookkeeping
cd /Users/davidcruwys/dev/ad/apps/dark-factory && pwd && ls experiments/watchtower-engine/ && echo "=== running ===" && ls experiments/watchtower-engine/running/
```

## Prevention
After any `cd` in a multi-step Bash sequence, don't trust that a later step's cwd is repo root — either `pwd` first or use absolute paths for writes/mkdir that must land at a fixed location (bookkeeping dirs, run records, queue moves). This applies to any agent role driving multi-step shell sequences within one persistent-cwd session, not just this ticket's executor.

## Related
- Sessions: bb4024fd
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): bb4024fd · 2026-06-06
- **Files** (candidate-level): experiments/watchtower-board/, experiments/watchtower-engine/
- **Commits** (candidate-level): —
