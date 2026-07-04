---
topic: "Doc-drift audit findings"
issue: "Doc-drift audit found docs silently out of step with shipped code"
created: "2026-06-16"
story_reference: "84ec3614"
category: "documentation"
severity: "high"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["CLAUDE.md", "README.md", "docs/INDEX.md", "docs/appyradar.md", "docs/architecture.md", "docs/dark-factory-constellation.md", "docs/tool-registry.md", "docs/ylo-to-poem-blueprint.md", "experiments/watchtower-engine/README.md", "experiments/ylo/README.md", "experiments/ylo/blackboard/README.md", "tools/design-lint/README.md", "tools/mocha-census/README.md"]
commits: ["6b91d46"]
---

# Doc-drift audit findings — Doc-drift audit found docs silently out of step with shipped code

## Problem Signature

**Symptoms**: A doc-drift audit of the repo's code-anchored docs (README, CLAUDE.md, docs/INDEX, tool-registry, constellation, architecture, appyradar, plus 4 tool/experiment READMEs) turned up 21 findings (1 critical, 9 major, 9 minor). The critical one: experiments/watchtower-engine/README.md stated the end-to-end claim-to-Workflow-tool-to-record-to-done path was 'Not yet run (next step…)', while the engine actually had 34 run records, a proof-of-first-real-run writeup, a failure register, a reaper, and retry-with-backoff — none of it documented. Other findings were a stale directory reference (`ylo-experiment/` renamed to `experiments/ylo/` months earlier but still referenced in 3 places, including a self-contradiction within the same file), a subsystem rename that never propagated (`appyradar-sentinal` typo repo vs the live `appyradar-sentinel`), and registries (tool-registry.md, INDEX.md) missing tools that had already shipped (mocha-census, design-lint).

**Environment**: dark-factory repo docs (README.md, CLAUDE.md, docs/*.md, tool and experiment READMEs) vs the actual code/filesystem state

**Triggering Conditions**: Directories were relocated, a subsystem was renamed, and new tooling/capability (34 engine runs, reaper, retry, failure register) shipped without anyone going back to update the docs that described the old state

## Root Cause
No automated or habitual check keeps docs in sync with code as it moves — docs are written once and then only manually revisited, so drift accumulates invisibly until someone reads the doc against current reality

## Solution
Ran the doc-drift skill (code = canonical, doc = derivative), fanning out 5 parallel verifier agents across doc clusters, each required to prove drift by locating exact code/filesystem truth (ls/grep/read) rather than trusting the doc text. Consolidated 21 findings into a report, then applied surgical fixes to 15 docs (not full rewrites — targeted corrections), then re-ran a grep sweep for the old stale strings to confirm they were gone and that newly-added references resolved to real files.

```diff-before
## What's proven vs not

- **Proven**: the atomic claim mutex under concurrency (the thing that makes 4 sessions safe).
- **Not yet run**: the end-to-end claim → Workflow-tool → record → done path (next step; needs the skill invoked once for real).
- **Out of scope here**: the AppyStack surface (writes queue entries + visualizes state) — the "easy half", built after the engine is validated.
```

```diff-after
## Added since the original spike

- **Failure register** (`failures/`) — every factory failure is a structured, countable record: `register.jsonl` + `record-failure.sh` (append) + `audit.sh` (count by category; investigate at 3–4).
- **Reaper** (`bin/reaper.sh`) — reaps orphan tmux windows, keyed off `done/<queue_id>.json` mtime + a grace period (only successes land in `done/`). Proven live (`proof/reaper-live.md`).
- **Retry-with-backoff** (`bin/retry.sh`) — re-queues `failed/` → `queue/` with exponential backoff `RETRY_BASE_SECONDS * 2^(attempt-1)` (30/60/120s), then terminal.
- **Swagger dispatch** (`bin/dispatch-swagger.sh`) — spawns a job-agent in tmux for a claimed ticket.

## What's proven vs not

- **Proven**: the atomic claim mutex under concurrency…
```

Verification sweep after all fixes applied:
```bash
grep -rn "ylo-experiment/" README.md CLAUDE.md docs/ 2>/dev/null
grep -rn "appyradar-sentinal" ... # etc — expect no hits
```

## Prevention
Don't rely on memory to keep docs honest — dispatch a periodic doc-health sweep (doc-drift for doc-vs-code drift, doc-review --crossref/--topology/--gaps for doc-vs-doc-set drift) in report mode. When Dev ships a feature or renames/moves a subsystem, updating the doc that describes it should be part of done, not a later audit's job.

## Related
- Sessions: 84ec3614
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 84ec3614 · 2026-06-16
- **Files** (candidate-level): CLAUDE.md, README.md, docs/INDEX.md, docs/appyradar.md, docs/architecture.md, docs/dark-factory-constellation.md, docs/tool-registry.md, docs/ylo-to-poem-blueprint.md, experiments/watchtower-engine/README.md, experiments/ylo/README.md, experiments/ylo/blackboard/README.md, tools/design-lint/README.md, tools/mocha-census/README.md
- **Commits** (candidate-level): 6b91d46
