---
topic: "Dev server cache-busting gap"
issue: "Dev server cache-busting gap serves stale content after re-render"
created: "2026-06-08"
story_reference: "f7a95652"
category: "infrastructure"
severity: "medium"
status: "proposed"
recurrence_count: 1
promoted_to_pattern: ""
provenance: reconstructed-from-sessions
provenance_grain: session
files: [".claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/MEMORY.md", ".claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/design-taste-spec-is-canonical.md", ".claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/factory-failure-register.md", ".claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/its-mochaccino-not-comprehend-visualise.md", ".claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/shapes-are-annotation-not-the-medium.md", "/tmp/cortex-shots/02-brain-remembers.png", "/tmp/cortex-shots/03-four-memories.png", "/tmp/cortex-shots/04-brain-sleeps.png", "/tmp/cortex-shots/06-brain-anatomy.png", "/tmp/cortex-shots/proof-03-four-memories.png", "/tmp/cortex-shots/proof-06-brain-anatomy.png", "/tmp/cortex-shots/v3-02-brain-remembers.png", "/tmp/cortex-shots/v3-03-four-memories.png", "/tmp/cortex-shots/v3-04-brain-sleeps.png", "/tmp/cortex-shots/v3-06-brain-anatomy.png"]
commits: []
---

# Dev server cache-busting gap — Dev server cache-busting gap serves stale content after re-render

## Problem Signature

**Symptoms**: After a re-render, opening the design URLs in an ordinary browser showed two of four pages in an old version (previous colour scheme and layout elements) and two in a half-built state, even though a fresh check of the actual files on disk confirmed the current, correct version was being served.

**Environment**: A local design workspace's http server (Python `http.server` on :7422) and its generated `index.html` views, which fetch their JSON data at a fixed relative path.

**Triggering Conditions**: A design is regenerated in place at a URL that was already visited earlier in the same session (same design slug, same server, same fetch path) — the returning browser tab reuses its cache instead of re-fetching.

## Root Cause
A HEAD request against the served data JSON returned only a `Last-Modified` header and no `Cache-Control` directive, and the view's fetch call carries no cache-busting query parameter (e.g. `?v=<hash>`) — so a browser is free to reuse a cached response across re-renders of the same URL.

## Solution
Diagnosed and proposed but not applied in this session: cache-bust the data fetch with a version/commit-sha query parameter and serve the workspace with no-cache headers; add 'renders must cache-bust' to the render skill's hard expectations so future designs cannot reproduce the same reviewer-facing staleness.

```bash
# Server sends no Cache-Control:
curl -sI http://localhost:7422/data/06-brain-anatomy.json | grep -iE "cache"
# → only: Last-Modified: Mon, 08 Jun 2026 21:47:43 GMT
```

```js
// View fetches with no cache-bust param:
fetch('../../data/06-brain-anatomy.json')
```

## Prevention
Any local render/preview server used for iterative human review should either disable browser caching (no-cache headers) or have its views cache-bust data fetches with a version/commit identifier, so a re-render at the same URL is guaranteed to show the reviewer the current file, not a stale cached one.

## Related
- Sessions: f7a95652
- Related learnings: []
- Related patterns: []

## Provenance
- **Sessions** (1): f7a95652 · 2026-06-08
- **Files** (session-level): .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/MEMORY.md, .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/design-taste-spec-is-canonical.md, .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/factory-failure-register.md, .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/its-mochaccino-not-comprehend-visualise.md, .claude/projects/-Users-davidcruwys-dev-ad-apps-dark-factory/memory/shapes-are-annotation-not-the-medium.md, /tmp/cortex-shots/02-brain-remembers.png, /tmp/cortex-shots/03-four-memories.png, /tmp/cortex-shots/04-brain-sleeps.png, /tmp/cortex-shots/06-brain-anatomy.png, /tmp/cortex-shots/proof-03-four-memories.png, /tmp/cortex-shots/proof-06-brain-anatomy.png, /tmp/cortex-shots/v3-02-brain-remembers.png, /tmp/cortex-shots/v3-03-four-memories.png, /tmp/cortex-shots/v3-04-brain-sleeps.png, /tmp/cortex-shots/v3-06-brain-anatomy.png
- **Commits** (session-level): —
