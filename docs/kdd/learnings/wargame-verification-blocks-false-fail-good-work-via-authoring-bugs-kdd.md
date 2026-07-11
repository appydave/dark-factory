---
topic: "War-game Verification-block authoring"
issue: "Verification blocks repeatedly false-failed correct work via authoring bugs — placeholder tokens, inverted grep polarity, cross-line variables"
created: "2026-07-11"
story_reference: "wg-t1-16, wg-t1-20, wg-t3-03, wg-t3-04"
category: "tooling"
severity: "high"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: live-capture
provenance_grain: candidate
files: ["bin/promote-wargame.py", "backlog/wargames/T1-16-durable-verdict-ledger.md", "backlog/wargames/T1-20-reap-settles-verify-fail.md"]
commits: ["d708367", "e689b57"]
---

# War-game Verification-block authoring — good work false-failed by broken checks

## Problem Signature

**Symptoms**: In one session, three distinct authoring bugs in `## Verification` blocks each
false-failed a job whose actual work was correct, and (pre-T1-20) each wedged the engine for ~30
min re-running the failing check:
1. **Placeholder token** — `python3 status.py --resume <a-real-done-ticket>` (literal `<…>`) → bash
   syntax error (T1-16).
2. **Inverted grep polarity** — a bare `grep PATTERN file` meant to prove something was *removed*;
   no-match exits 1, which the engine reads as FAIL, so a correct fix fails the check (T1-20).
3. **Cross-line `$VAR`** under per-line execution — `DF=…` on line 1 empty by line 2 (T3-03/04; see
   [[verify-block-ran-per-line-against-main-not-the-worker-worktree]]).

**Environment**: dark-factory `verify_wargame` running author-written check blocks.

## Root Cause

Verification blocks are hand-authored bash written for a human's mental model (substituted
placeholders, "grep to confirm absence", variables that persist) but executed literally by a
machine. Nothing checked the block before dispatch.

## Solution

Added a **lint to `promote-wargame go`** (commit e689b57): blocks a ticket whose `## Verification`
has a `<placeholder>` token, warns on bare-`grep` polarity risk — runs before promotion.

```bash
# blocked:  grep -n "def foo" file          # bare grep, proving ABSENCE -> exit 1 = FAIL
# right:    ! grep -q "def foo" file && echo ok     # assert absence explicitly
#           grep -q "def foo" file && echo ok       # assert presence explicitly
```

## Prevention

Author verification checks as **self-contained, explicit-polarity** commands (no `<placeholder>`, no
grep-for-absence without `!`, no cross-line state until the engine runs the block as one script) —
and **lint them before dispatch**. Assert positively (`grep -q P && echo ok`) rather than relying on
a bare command's implicit exit code. Note: recurred 3× within one session (not yet across sessions)
→ learning, not a pattern; watch for cross-session recurrence.
