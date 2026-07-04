---
topic: "Safe pull with local edits"
issue: "Cross-machine push/pull conflicts need careful reconciliation, not blind stash/rebase"
created: "2026-06-10"
story_reference: "84ec3614, 903d8c01"
category: "tooling"
severity: "low"
status: "proposed"
recurrence_count: 2
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["apps/appysentinel/docs/architecture-refactor-v2.md", "context/CONTEXT.md", "context/context.globs.json"]
commits: ["619f981", "6b91d46", "8010121"]
---

# Safe pull with local edits — Cross-machine push/pull conflicts need careful reconciliation, not blind stash/rebase

## Problem Signature

**Symptoms**: A dirty working tree blocks `git pull --ff-only`; stashing the entire tree and popping it back risks losing track of which specific file actually collides with the incoming commit.

**Environment**: apps/appysentinel (formerly appysentinal) — local repo with several uncommitted doc edits, only one of which overlapped an incoming upstream commit.

**Triggering Conditions**: Local uncommitted edits existed on several files; only one of those files also had upstream changes in the commits being pulled.

## Root Cause
Not a defect — a technique for handling a real merge-collision risk safely rather than a bug fix.

## Solution
Diff local changes against `HEAD..origin/main` per-file first to find the actual overlap (only `docs/architecture-refactor-v2.md` collided, on different line ranges than the incoming change). Stash only that one file, fast-forward with `git merge --ff-only origin/main`, then pop the stash so git 3-way-merges the local edit back on top of the newly-pulled content, leaving the rest of the dirty tree untouched.

```bash
git stash push -- docs/architecture-refactor-v2.md
git merge --ff-only origin/main
# restore the local edit (auto 3-way)
git stash pop
```
Result: "Saved working directory and index state WIP on main: 8010121 fix(cli): exclude template node_modules/dist from published tarball" ... "10 files changed, 14 insertions(+), 14 deletions(-)" ... stash popped cleanly, leaving only the pre-existing untouched dirty files (`docs/pattern-catalogue.md`, `.mochaccino/client/`, `docs/tunneling-guide.md`) as before.

## Prevention
Before any `git pull --ff-only` on a dirty tree, diff `HEAD..origin/main --stat` against the locally-modified file list to isolate genuine collisions, and stash only the colliding file(s) rather than the whole tree — keeps the rest of the working state untouched and makes the eventual restore a clean, reviewable 3-way merge.

## Related
- Sessions: 84ec3614, 903d8c01
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (2): 84ec3614, 903d8c01 · 2026-06-10 → 2026-06-16
- **Files** (candidate-level): apps/appysentinel/docs/architecture-refactor-v2.md, context/CONTEXT.md, context/context.globs.json
- **Commits** (candidate-level): 619f981, 6b91d46, 8010121
