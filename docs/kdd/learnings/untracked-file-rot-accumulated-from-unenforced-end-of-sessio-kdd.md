---
topic: "untracked-file rot cleanup"
issue: "Untracked-file rot accumulated from unenforced end-of-session commit discipline"
created: "2026-06-10"
story_reference: "f68c5f1c"
category: "process"
severity: "high"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: [".claude/skills/comprehend-visualise/", ".claude/skills/millwright/", ".gitignore", "CLAUDE.md", "backlog/specs/tickets.json", "backlog/specs/untracked-rot-sweep-spec.md", "docs/appyradar.md", "docs/capture-service-brief.md", "docs/dark-factory-constellation.md", "docs/david-design-patterns.md", "experiments/watchtower-engine/", "skills-lock.json", "tools/design-lint/", "tools/mocha-census/"]
commits: ["0368d81", "221ab87", "3ef7fce", "8c7c68c", "ba66109", "ed218be", "f572b0b"]
---

# untracked-file rot cleanup — Untracked-file rot accumulated from unenforced end-of-session commit discipline

## Problem Signature

**Symptoms**: git status showed 72 untracked files, 8 modified tracked files, and 1 deleted-but-uncommitted file in the dark-factory working tree — real deliverables (tools/design-lint, tools/mocha-census, two new skills, several docs, ~11 backlog items/specs, experiment engine outputs) built across multiple prior sessions but never committed.

**Environment**: dark-factory repo working tree (~/dev/ad/apps/dark-factory)

**Triggering Conditions**: the CLAUDE.md end-of-session rule ('mark complete, commit') was followed inconsistently session after session, so uncommitted deliverables kept piling up until a git status check surfaced the full backlog.

## Root Cause
commit-at-session-end is a remembered convention, not an enforced mechanism — nothing detected or surfaced the growing pile automatically, so it went unnoticed until manually inspected.

## Solution
Reviewed each diff for legitimacy (git diff on the modified tracked files), added a .gitignore entry for the transient/generated bucket (.mochaccino/, .playwright-mcp/, *.serve.log, root *.png), then committed the remaining real deliverables in 7 logical, scoped commits grouped by concern (gitignore, tools, skills, docs, backlog, experiments, lockfile) rather than one bulk commit.

```diff-before
# Env / secrets
.env
.env.local
*.pem
```
```diff-after
# Env / secrets
.env
.env.local
*.pem

# Transient tool working dirs (local cache / capture output — never track)
.mochaccino/
.playwright-mcp/
.serve.log

# Scratch render proofs / screenshots at repo root (real assets belong in a subfolder)
/*.png
```

## Prevention
Build a standing detect-and-tell sentinel (spec'd as DF-9, see the paired decision candidate) that scans configured repos for untracked/modified/deleted state and surfaces it at session-open preflight, instead of relying on every session remembering to commit.

## Related
- Sessions: f68c5f1c
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): f68c5f1c · 2026-06-10
- **Files** (candidate-level): .claude/skills/comprehend-visualise/, .claude/skills/millwright/, .gitignore, CLAUDE.md, backlog/specs/tickets.json, backlog/specs/untracked-rot-sweep-spec.md, docs/appyradar.md, docs/capture-service-brief.md, docs/dark-factory-constellation.md, docs/david-design-patterns.md, experiments/watchtower-engine/, skills-lock.json, tools/design-lint/, tools/mocha-census/
- **Commits** (candidate-level): 0368d81, 221ab87, 3ef7fce, 8c7c68c, ba66109, ed218be, f572b0b
