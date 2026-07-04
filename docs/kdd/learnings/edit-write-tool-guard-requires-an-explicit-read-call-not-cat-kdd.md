---
topic: "Write needs Read, not cat"
issue: "Edit/Write tool guard requires an explicit Read call, not cat or prior viewing"
created: "2026-06-15"
story_reference: "7a973797, f4f3d282"
category: "tooling"
severity: "low"
status: "proposed"
recurrence_count: 2
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["context/CONTEXT.md", "context/context.globs.json", "docs/watchtower/context.md", "docs/watchtower/spec.md"]
commits: ["ef4d618"]
---

# Write needs Read, not cat — Edit/Write tool guard requires an explicit Read call, not cat or prior viewing

## Problem Signature

**Symptoms**: Write to context/CONTEXT.md and, separately, to context/context.globs.json both failed with `<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>` despite the same content having been displayed earlier in the session via a Bash `cat` command.

**Environment**: Claude Code session running the system-context skill against the dark-factory repo, refreshing context/CONTEXT.md and context/context.globs.json.

**Triggering Conditions**: The existing target file's content was inspected via Bash `cat` (not the Read tool) before attempting a Write to that same file.

## Root Cause
The harness's read-before-write guard only registers state from an explicit Read tool call; content surfaced through another tool (Bash `cat`) does not satisfy it, so Write refuses to overwrite a file it considers 'unread'.

## Solution
Call Read on the target file immediately before Write whenever overwriting an existing file, even if its content was already seen via another tool such as Bash cat.

Failing sequence (Write attempted after only a Bash `cat`, no Read tool call):
```
→ [Write] context/context.globs.json
...
⟵ result: <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
```

Fix — insert an explicit Read immediately before the Write:
```
→ [tool:Read] context/context.globs.json
⟵ result: 1  {
2    "pattern": "unknown",
...
→ [Write] context/context.globs.json
⟵ result: The file .../context/context.globs.json has been updated successfully.
```
The same pattern occurred and was fixed identically for context/CONTEXT.md earlier in the session.

## Prevention
Dev: always issue a Read tool call on a file immediately before a Write that overwrites it — never rely on Bash `cat` (or other non-Read tools) output as a substitute for the read-before-write guard.

## Related
- Sessions: 7a973797, f4f3d282
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (2): 7a973797, f4f3d282 · 2026-06-15 → 2026-06-16
- **Files** (candidate-level): context/CONTEXT.md, context/context.globs.json, docs/watchtower/context.md, docs/watchtower/spec.md
- **Commits** (candidate-level): ef4d618
