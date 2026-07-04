---
topic: "scoped commit in shared working tree"
issue: "Blind git add in a dirty shared working tree risks sweeping in unrelated files"
created: "2026-06-16"
story_reference: "2fdc2412, 7a973797"
category: "process"
severity: "low"
status: "proposed"
recurrence_count: 2
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["dev/raw-intake (external repo)"]
commits: ["ef4d618"]
---

# scoped commit in shared working tree — Blind git add in a dirty shared working tree risks sweeping in unrelated files

## Problem Signature

**Symptoms**: `git diff --stat` after this session's edits showed `context/CONTEXT.md` and `context/context.globs.json` as modified, plus untracked files (an audit doc, a backlog item, a plans/ dir) that predated this session's work.

**Environment**: dark-factory repo working tree at end-of-session commit time; a single repo shared across concurrent threads/sessions.

**Triggering Conditions**: Multiple concurrent threads touching the same working tree without committing between them, so unrelated changes accumulate before any one thread commits.

## Root Cause
A shared working tree accumulates uncommitted changes from other in-flight work; a blanket stage-everything commit would sweep unrelated changes into this session's commit.

## Solution
Stage only the specific files this session's review touched (`docs/INDEX.md`, `docs/watchtower/spec.md`, `docs/watchtower/context.md`, `docs/watchtower/chatgpt-brief.md`, `docs/watchtower/HANDOVER.md`, `docs/watchtower/REVIEW.md`) via explicit `git add` of those paths, rather than `git add -A`, then commit and push just those.

## Prevention
Before committing, check `git status` / `git diff --stat` for changes that predate the current session's work and explicitly exclude them from `git add`; never use a blanket add when the working tree may hold other threads' in-flight edits.

## Related
- Sessions: 2fdc2412, 7a973797
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (2): 2fdc2412, 7a973797 · 2026-06-16 → 2026-06-23
- **Files** (candidate-level): dev/raw-intake (external repo)
- **Commits** (candidate-level): ef4d618
