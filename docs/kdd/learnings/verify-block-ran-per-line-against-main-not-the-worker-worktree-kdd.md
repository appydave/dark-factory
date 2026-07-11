---
topic: "Verification execution model"
issue: "Verify ran each check per-line against the main tree, so worktree-isolated artifacts were invisible and correct work false-failed"
created: "2026-07-11"
story_reference: "wg-t1-21, wg-t3-03, wg-t3-04"
category: "tooling"
severity: "high"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: live-capture
provenance_grain: candidate
files: ["engine/orchestrator.py", "backlog/wargames/T1-21-verify-runs-in-worktree-as-one-script.md"]
commits: ["2b9e291", "a97c1d0"]
---

# Verification execution model — verify ran per-line against main, not the worker's worktree

## Problem Signature

**Symptoms**: Two workers built correct tools (`verify-provenance.py`, `style-check.py`, self-tests
11/11 and 15/15) in their own git worktrees, committed them, and BOTH false-failed reap verification
with "file not found" — `$DF/tools/x.py` resolving to `/tools/x.py`, `test -f tools/x.py` failing.

**Environment**: dark-factory engine `verify_wargame` reaping worktree-isolated (wg-t1-19) workers.

**Triggering Conditions**: Any war-game `## Verification` block that (a) used a variable/heredoc/`cd`
across lines, or (b) checked a file the worker created — once per-worker worktrees were live.

## Root Cause

Two compounding defects. (1) The engine ran **each verification line as its own subprocess**, so
`DF=…`, `T=$(mktemp)`, heredocs, and `cd` reset every line — state the war-game format itself
recommends. (2) It ran verify from the **main repo tree**, but the worker built + committed its
artifact **inside its worktree**; consolidation to main only happens *after* a passing verify — so
verify could never see the artifact. A deadlock: verify → not-found → fail → never consolidates.

## Solution

`verify_wargame` now runs the **entire block as one script** (`/bin/bash -c script`, each check
followed by a marker echo capturing its `$?` so per-check detail survives) with **`cwd` = the
worker's worktree** (fallback REPO at pool=1). State persists; worktree artifacts are visible.
(wg-t1-21, commit 2b9e291.)

```bash
# wrong — per-line, cwd=main:   `$DF` empty on line 2, worktree file invisible
grep -E "^(import|from) " $DF/tools/verify-provenance.py   # -> grep: /tools/...: No such file
# right — whole block, one shell, cwd=worktree
r = subprocess.run(["/bin/bash", "-c", script], cwd=run_cwd, capture_output=True)
```

## Prevention

When a harness runs author-supplied check scripts, run the **whole block in one shell at the
artifact's real location**, not line-by-line against a canonical tree. A per-line runner silently
breaks the exact multi-line idioms authors are told to use, and an isolation model (worktrees) that
verifies against the shared tree can never see isolated work. See [[hitl-ratification-pipeline]] and
the `promote-wargame go` verification-block lint (guards the authoring side).
