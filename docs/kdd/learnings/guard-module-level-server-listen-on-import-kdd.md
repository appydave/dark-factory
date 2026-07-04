---
topic: "guard module-level server.listen() on import"
issue: "Guard module-level server.listen() on import"
created: "2026-06-07"
story_reference: "5f7a1870"
category: "debugging"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: candidate
files: ["experiments/watchtower-board/selfcheck-promote.mjs", "experiments/watchtower-board/server.mjs"]
commits: []
---

# guard module-level server.listen() on import — Guard module-level server.listen() on import

## Problem Signature

**Symptoms**: Running `node experiments/watchtower-board/selfcheck-promote.mjs` (which imports pure functions from server.mjs) crashed with `Error: listen EADDRINUSE: address already in use :::7430` even though the self-check touches no servers itself.

**Environment**: experiments/watchtower-board/server.mjs — a Node ESM module that doubles as both an importable library (pure functions like buildPromoteTicket/slugify) and a directly-runnable HTTP server

**Triggering Conditions**: A new self-check script (`selfcheck-promote.mjs`) did `import { buildPromoteTicket, slugify } from './server.mjs'` while the real watchtower-board server was already listening on port 7430 in another process; the unconditional top-level `server.listen(PORT, ...)` call fired again on import.

## Root Cause
server.mjs called `server.listen(...)` unconditionally at module top level, so ANY import of the file — not just direct execution via `node server.mjs` — re-ran the listen call and collided with the port already bound by the running instance.

## Solution
Guarded the listen call so it only runs when the file is executed directly, not when imported: `if (process.argv[1] === fileURLToPath(import.meta.url)) { server.listen(...) }`. This let selfcheck-promote.mjs import the pure functions without ever touching the live :7430 server.

```diff-before
server.listen(PORT, () => console.log(`watchtower-board on http://localhost:${PORT} (engine: ${ENGINE})`));
```
```diff-after
// Only bind the port when run directly (node server.mjs), not when imported
// (e.g. by selfcheck-promote.mjs) — so importing the pure functions can't
// collide with the already-running :7430 server.
if (process.argv[1] === fileURLToPath(import.meta.url)) {
  server.listen(PORT, () => console.log(`watchtower-board on http://localhost:${PORT} (engine: ${ENGINE})`));
}
```

## Prevention
Any Node ESM module meant to be BOTH importable (for pure-function reuse / self-checks) and directly runnable as a server/daemon must guard side-effecting top-level calls (`listen`, `connect`, timers, etc.) behind an entrypoint check (`process.argv[1] === fileURLToPath(import.meta.url)`) before extracting pure functions out of it for testing.

## Related
- Sessions: 5f7a1870
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): 5f7a1870 · 2026-06-07
- **Files** (candidate-level): experiments/watchtower-board/selfcheck-promote.mjs, experiments/watchtower-board/server.mjs
- **Commits** (candidate-level): —
