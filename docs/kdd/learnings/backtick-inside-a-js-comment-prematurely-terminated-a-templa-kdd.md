---
topic: "Backtick in JS comment breaks template literal"
issue: "Backtick inside a JS comment prematurely terminated a template literal"
created: "2026-06-07"
story_reference: "f8b8051a"
category: "debugging"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["experiments/watchtower-board/server.mjs"]
commits: []
---

# Backtick in JS comment breaks template literal — Backtick inside a JS comment prematurely terminated a template literal

## Problem Signature

**Symptoms**: node --check server.mjs failed with `SyntaxError: Unexpected identifier 'sel'` right after adding a comment inside the file's embedded page template literal

**Environment**: experiments/watchtower-board/server.mjs — a Node http server whose client-facing HTML/JS page is built as one large backtick template literal

**Triggering Conditions**: Added a comment line that backtick-quoted an identifier (the `sel` Set) while writing inside the outer PAGE template literal string; the inner backtick closed the outer literal early

## Root Cause
The surrounding page markup is itself a JS template literal, so an unescaped backtick anywhere inside it — even inside a plain-text comment — terminates the string and desyncs the rest of the file

## Solution
Removed the backticks from the comment and described the variable name in plain prose instead of backtick-quoting it

```diff-before
// v5: click-to-toggle multi-SELECT (no per-card button). Selection survives the
// innerHTML rebuild each tickLanes via the `sel` Set, keyed concept|||lane.
```
```diff-after
// v5: click-to-toggle multi-SELECT (no per-card button). Selection survives the
// innerHTML rebuild each tickLanes via the sel Map, keyed concept then lane.
```

## Prevention
Never backtick-quote identifiers inside a comment that lives inside a JS template literal (e.g. an inlined HTML/JS page string) — use plain words, and run `node --check` immediately after edits to such files

## Related
- Sessions: f8b8051a
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): f8b8051a · 2026-06-07
- **Files** (candidate-level): experiments/watchtower-board/server.mjs
- **Commits** (candidate-level): —
